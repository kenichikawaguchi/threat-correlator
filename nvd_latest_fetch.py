#!/usr/bin/env python3
# nvd_latest_fetch.py
import os, sqlite3, requests, datetime, time, random

MAX_RETRIES = 5
RETRYABLE_STATUS = {429, 500, 502, 503, 504}

from typing import Optional

BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"
DB = "nvd.db"
TS_FILE = "last_timestamp.txt"
API_KEY = os.environ.get("NVD_API_KEY")

# APIキーの有無でウェイトを切り替える
# キーなし: 5req/30sec → 6秒待てば安全
# キーあり: 50req/30sec → ほぼ不要だが念のため0.6秒
SLEEP_SEC = 0.6 if API_KEY else 6.0
RESULTS_PER_PAGE = 2000  # NVD APIの最大値


def now_z() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def read_ts() -> Optional[str]:
    if not os.path.exists(TS_FILE):
        return None
    s = open(TS_FILE, "r", encoding="utf-8").read().strip()
    return s or None


def write_ts(ts: str):
    with open(TS_FILE, "w", encoding="utf-8") as f:
        f.write(ts)


def fetch(params: dict) -> dict:
    headers = {"Accept": "application/json", "User-Agent": "nvd-sqlite/1.0"}
    if API_KEY:
        headers["apiKey"] = API_KEY

    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(BASE, params=params, headers=headers, timeout=30)

            if r.status_code in RETRYABLE_STATUS:
                # 429 は Retry-After ヘッダを優先
                wait = min(120.0, (2 ** attempt) * 5 + random.uniform(0, 2))
                if r.status_code == 429:
                    try:
                        wait = float(r.headers.get("Retry-After", wait))
                    except ValueError:
                        pass
                print(f"  [{r.status_code}] attempt {attempt+1}/{MAX_RETRIES}, "
                      f"retry in {wait:.1f}s ...")
                last_err = requests.exceptions.HTTPError(
                    f"{r.status_code} for url: {r.url}", response=r
                )
                time.sleep(wait)
                continue

            r.raise_for_status()
            return r.json()

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            wait = min(120.0, (2 ** attempt) * 5 + random.uniform(0, 2))
            print(f"  [ConnectionError] attempt {attempt+1}/{MAX_RETRIES}, "
                  f"retry in {wait:.1f}s: {e}")
            last_err = e
            time.sleep(wait)

    raise last_err or RuntimeError("fetch: all retries exhausted")


def ensure_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cves (
          cve_id      TEXT PRIMARY KEY,
          published   TEXT,
          description TEXT,
          cvss        REAL,
          vector      TEXT,
          raw_json    TEXT,
          inserted_at TEXT,
          weaknesses  TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cve_refs (
          id     INTEGER PRIMARY KEY AUTOINCREMENT,
          cve_id TEXT NOT NULL,
          url    TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_cve_refs_unique
        ON cve_refs(cve_id, url)
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_cves_cvss ON cves(cvss)")
    conn.commit()
    return conn


def extract_summary(v: dict) -> dict:
    cve = v.get("cve", {})
    cve_id = cve.get("id") or cve.get("CVE_data_meta", {}).get("ID")
    published = v.get("published") or cve.get("published", "")

    # description
    descs = cve.get("descriptions") or cve.get("description", {}).get("description_data", [])
    desc = ""
    if isinstance(descs, list):
        for d in descs:
            if d.get("lang") in ("en", "eng", None) and d.get("value"):
                desc = d.get("value")
                break
        if not desc and descs:
            desc = descs[0].get("value", "")

    # cvss
    metrics = cve.get("metrics") or v.get("metrics") or {}
    score = None
    vec = None
    for key in ("cvssMetricV40", "cvssMetricV31", "cvssMetricV30", "cvssMetricV3", "cvssMetricV2"):
        arr = metrics.get(key)
        if isinstance(arr, list) and arr:
            first = arr[0]
            cvss_data = first.get("cvssData") or first.get("cvss") or {}
            score = cvss_data.get("baseScore")
            vec = cvss_data.get("vectorString")
            break

    # weaknesses
    cwes = []
    for w in cve.get("weaknesses", []):
        for d in w.get("description", []):
            if d.get("value"):
                cwes.append(d["value"])
    weaknesses = ";".join(cwes) if cwes else None

    # refs
    refs = [r["url"] for r in cve.get("references", []) if isinstance(r, dict) and r.get("url")]

    return {
        "cve_id": cve_id,
        "published": published,
        "description": desc,
        "cvss": score,
        "vector": vec,
        "weaknesses": weaknesses,
        "refs": refs,
        "raw": v,
    }


def upsert(conn: sqlite3.Connection, item: dict):
    import json
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO cves(cve_id, published, description, cvss, vector, weaknesses, raw_json, inserted_at)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(cve_id) DO UPDATE SET
          published   = excluded.published,
          description = excluded.description,
          cvss        = excluded.cvss,
          vector      = excluded.vector,
          weaknesses  = excluded.weaknesses,
          raw_json    = excluded.raw_json
    """, (
        item["cve_id"],
        item["published"],
        item["description"],
        item["cvss"],
        item["vector"],
        item["weaknesses"],
        json.dumps(item["raw"], ensure_ascii=False),
        now_z(),
    ))
    for url in item["refs"]:
        cur.execute(
            "INSERT OR IGNORE INTO cve_refs(cve_id, url) VALUES(?, ?)",
            (item["cve_id"], url),
        )
    conn.commit()


def build_params(last_ts: Optional[str]) -> dict:
    """前回取得タイムスタンプに基づいてAPIパラメータを組み立てる。"""
    params = {"resultsPerPage": str(RESULTS_PER_PAGE)}
    if last_ts:
        try:
            dt = datetime.datetime.fromisoformat(last_ts.replace("Z", "+00:00"))
            dt = dt.astimezone(datetime.timezone.utc) + datetime.timedelta(seconds=1)
            params["pubStartDate"] = dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            params["pubEndDate"] = now_z()
        except Exception:
            params["pubStartDate"] = last_ts
            params["pubEndDate"] = now_z()
    return params


def main():
    conn = ensure_db()
    last = read_ts()
    params = build_params(last)

    start_index = 0
    total_results = None
    total_fetched = 0
    new_count = 0
    last_data = {}

    print(f"Fetching from NVD (API key: {'yes' if API_KEY else 'no'}) ...")

    while True:
        params["startIndex"] = str(start_index)
        data = fetch(params)
        last_data = data

        if total_results is None:
            total_results = data.get("totalResults", 0)
            print(f"Total results: {total_results}")

        vulns = data.get("vulnerabilities", [])
        if not vulns:
            break

        for v in vulns:
            s = extract_summary(v)
            if not s["cve_id"]:
                continue
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM cves WHERE cve_id=?", (s["cve_id"],))
            if cur.fetchone() is None:
                new_count += 1
            upsert(conn, s)

        total_fetched += len(vulns)
        print(f"  fetched {total_fetched}/{total_results} ...")

        if total_fetched >= total_results:
            break

        start_index += len(vulns)
        time.sleep(SLEEP_SEC)

    api_ts = last_data.get("timestamp") or now_z()
    write_ts(api_ts)
    conn.close()
    print(f"Done. fetched={total_fetched}, new={new_count}, timestamp={api_ts}")


if __name__ == "__main__":
    main()
