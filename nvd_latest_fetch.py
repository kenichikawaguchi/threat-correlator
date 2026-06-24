#!/usr/bin/env python3
# nvd_latest_fetch.py
import os, sqlite3, requests, datetime, time, random

MAX_RETRIES = 5
RETRYABLE_STATUS = {429, 500, 502, 503, 504}

from typing import Optional

# ── NVD ───────────────────────────────────────────────────────────────────────
NVD_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"
API_KEY  = os.environ.get("NVD_API_KEY")
SLEEP_SEC = 0.6 if API_KEY else 6.0
RESULTS_PER_PAGE = 2000

# ── CIRCL ─────────────────────────────────────────────────────────────────────
CIRCL_BASE        = "https://cve.circl.lu/api/last"
CIRCL_FETCH_COUNT = 500   # 1日分の余裕を持った件数（通常100〜260件/日）

# ── 共通 ──────────────────────────────────────────────────────────────────────
DB      = "nvd.db"
TS_FILE = "last_timestamp.txt"


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


# ── DB ────────────────────────────────────────────────────────────────────────
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
    for url in item.get("refs", []):
        cur.execute(
            "INSERT OR IGNORE INTO cve_refs(cve_id, url) VALUES(?, ?)",
            (item["cve_id"], url),
        )
    conn.commit()


# ── NVD fetch ─────────────────────────────────────────────────────────────────
def nvd_fetch(params: dict) -> dict:
    headers = {"Accept": "application/json", "User-Agent": "nvd-sqlite/1.0"}
    if API_KEY:
        headers["apiKey"] = API_KEY

    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(NVD_BASE, params=params, headers=headers, timeout=30)

            if r.status_code in RETRYABLE_STATUS:
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

    raise last_err or RuntimeError("nvd_fetch: all retries exhausted")


def nvd_extract_summary(v: dict) -> dict:
    cve = v.get("cve", {})
    cve_id = cve.get("id") or cve.get("CVE_data_meta", {}).get("ID")
    published = v.get("published") or cve.get("published", "")

    descs = cve.get("descriptions") or cve.get("description", {}).get("description_data", [])
    desc = ""
    if isinstance(descs, list):
        for d in descs:
            if d.get("lang") in ("en", "eng", None) and d.get("value"):
                desc = d.get("value")
                break
        if not desc and descs:
            desc = descs[0].get("value", "")

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

    cwes = []
    for w in cve.get("weaknesses", []):
        for d in w.get("description", []):
            if d.get("value"):
                cwes.append(d["value"])
    weaknesses = ";".join(cwes) if cwes else None

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


def build_nvd_params(last_ts: Optional[str]) -> dict:
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


def run_nvd(conn: sqlite3.Connection, last_ts: Optional[str]) -> tuple[int, int, str]:
    """NVDからCVEを取得。(fetched, new, api_ts) を返す。失敗時は例外を上げる。"""
    params = build_nvd_params(last_ts)
    start_index = 0
    total_results = None
    total_fetched = 0
    new_count = 0
    last_data = {}

    print(f"[NVD] Fetching (API key: {'yes' if API_KEY else 'no'}) ...")

    while True:
        params["startIndex"] = str(start_index)
        data = nvd_fetch(params)
        last_data = data

        if total_results is None:
            total_results = data.get("totalResults", 0)
            print(f"[NVD] Total results: {total_results}")

        vulns = data.get("vulnerabilities", [])
        if not vulns:
            break

        for v in vulns:
            s = nvd_extract_summary(v)
            if not s["cve_id"]:
                continue
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM cves WHERE cve_id=?", (s["cve_id"],))
            if cur.fetchone() is None:
                new_count += 1
            upsert(conn, s)

        total_fetched += len(vulns)
        print(f"[NVD]   fetched {total_fetched}/{total_results} ...")

        if total_fetched >= total_results:
            break

        start_index += len(vulns)
        time.sleep(SLEEP_SEC)

    api_ts = last_data.get("timestamp") or now_z()
    return total_fetched, new_count, api_ts


# ── CIRCL fallback ────────────────────────────────────────────────────────────
def circl_fetch(count: int = CIRCL_FETCH_COUNT) -> list:
    url = f"{CIRCL_BASE}/{count}"
    headers = {"Accept": "application/json", "User-Agent": "nvd-sqlite/1.0"}
    r = requests.get(url, headers=headers, timeout=60)
    r.raise_for_status()
    return r.json()


def circl_extract_summary(item: dict) -> dict:
    cve_id    = item.get("id", "")
    published = item.get("Published", "")
    desc      = item.get("summary", "") or ""

    # CVSS: v3 優先、なければ v2
    score = None
    vec   = None
    cvss3 = item.get("cvss3")
    if cvss3:
        try:
            score = float(cvss3)
        except (ValueError, TypeError):
            pass
        vec = item.get("cvss3-vector")
    if score is None:
        cvss2 = item.get("cvss")
        if cvss2:
            try:
                score = float(cvss2)
            except (ValueError, TypeError):
                pass
            vec = vec or item.get("cvss-vector")

    # weaknesses
    cwe = item.get("cwe", "") or ""
    weaknesses = cwe if cwe and cwe not in ("NVD-CWE-Other", "NVD-CWE-noinfo") else None

    # refs
    refs_raw = item.get("references", [])
    refs = [r for r in refs_raw if isinstance(r, str) and r.startswith("http")]

    return {
        "cve_id":      cve_id,
        "published":   published,
        "description": desc,
        "cvss":        score,
        "vector":      vec,
        "weaknesses":  weaknesses,
        "refs":        refs,
        "raw":         item,
    }


def _parse_ts(ts: str) -> Optional[datetime.datetime]:
    """タイムスタンプ文字列をUTC datetimeに変換。失敗時はNone。"""
    if not ts:
        return None
    try:
        dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    except Exception:
        return None


def run_circl(conn: sqlite3.Connection, last_ts: Optional[str]) -> tuple[int, int, str]:
    """CIRCLからCVEを取得。(fetched, new, now_ts) を返す。失敗時は例外を上げる。"""
    print(f"[CIRCL] Fetching last {CIRCL_FETCH_COUNT} CVEs ...")
    items = circl_fetch()

    since_dt = _parse_ts(last_ts)

    total_fetched = 0
    new_count = 0

    for item in items:
        s = circl_extract_summary(item)
        if not s["cve_id"]:
            continue

        # last_ts以降に公開されたものだけ処理
        if since_dt:
            pub_dt = _parse_ts(s["published"])
            if pub_dt and pub_dt <= since_dt:
                continue

        cur = conn.cursor()
        cur.execute("SELECT 1 FROM cves WHERE cve_id=?", (s["cve_id"],))
        if cur.fetchone() is None:
            new_count += 1
        upsert(conn, s)
        total_fetched += 1

    print(f"[CIRCL] Done. processed={total_fetched}, new={new_count}")
    return total_fetched, new_count, now_z()


# ── main ──────────────────────────────────────────────────────────────────────
def main():
    conn  = ensure_db()
    last  = read_ts()

    source       = "unknown"
    total_fetched = 0
    new_count    = 0
    api_ts       = now_z()

    # ── Step 1: NVD を試みる ─────────────────────────────────────────────────
    try:
        total_fetched, new_count, api_ts = run_nvd(conn, last)
        source = "NVD"
    except Exception as nvd_err:
        print(f"[NVD] All retries failed: {nvd_err}")
        print("[NVD] Switching to CIRCL fallback ...")

        # ── Step 2: CIRCL にフォールバック ───────────────────────────────────
        try:
            total_fetched, new_count, api_ts = run_circl(conn, last)
            source = "CIRCL"
        except Exception as circl_err:
            print(f"[CIRCL] Also failed: {circl_err}")
            conn.close()
            raise RuntimeError(
                f"Both NVD and CIRCL failed.\n  NVD:   {nvd_err}\n  CIRCL: {circl_err}"
            )

    write_ts(api_ts)
    conn.close()
    print(f"Done. source={source}, fetched={total_fetched}, new={new_count}, timestamp={api_ts}")


if __name__ == "__main__":
    main()
