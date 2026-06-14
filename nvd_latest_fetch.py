#!/usr/bin/env python3
# nvd_to_sqlite.py
import os, sqlite3, requests, datetime, time
from typing import Optional

BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"
DB = "nvd.db"
TS_FILE = "last_timestamp.txt"
API_KEY = os.environ.get("NVD_API_KEY")

def now_z():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

def read_ts() -> Optional[str]:
    if not os.path.exists(TS_FILE): return None
    s = open(TS_FILE,"r",encoding="utf-8").read().strip()
    return s or None

def write_ts(ts: str):
    with open(TS_FILE,"w",encoding="utf-8") as f: f.write(ts)

def fetch(params):
    headers = {"Accept":"application/json","User-Agent":"nvd-sqlite/1.0"}
    if API_KEY: headers["apiKey"] = API_KEY
    r = requests.get(BASE, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def ensure_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cves (
      cve_id TEXT PRIMARY KEY,
      published TEXT,
      description TEXT,
      cvss REAL,
      vector TEXT,
      raw_json TEXT,
      inserted_at TEXT
    )""")
    conn.commit()
    return conn

def extract_summary(v):
    cve = v.get("cve",{})
    cve_id = cve.get("id") or cve.get("CVE_data_meta",{}).get("ID")
    published = v.get("published") or cve.get("published","")
    # description
    descs = cve.get("descriptions") or cve.get("description",{}).get("description_data",[])
    desc = ""
    if isinstance(descs, list):
        for d in descs:
            if d.get("lang") in ("en","eng",None) and d.get("value"):
                desc = d.get("value"); break
        if not desc and descs:
            desc = descs[0].get("value","")
    # cvss
    metrics = cve.get("metrics") or v.get("metrics") or {}
    score = None; vec = None
    for key in ("cvssMetricV31","cvssMetricV30","cvssMetricV3","cvssMetricV2"):
        arr = metrics.get(key)
        if isinstance(arr,list) and arr:
            first = arr[0]
            score = (first.get("cvssData") or first.get("cvss") or {}).get("baseScore")
            vec = (first.get("cvssData") or first.get("cvss") or {}).get("vectorString")
            break
    return {"cve_id":cve_id,"published":published,"description":desc,"cvss":score,"vector":vec,"raw":str(v)}

def upsert(conn, item):
    cur = conn.cursor()
    cur.execute("""
      INSERT INTO cves(cve_id,published,description,cvss,vector,raw_json,inserted_at)
      VALUES(?,?,?,?,?,?,?)
      ON CONFLICT(cve_id) DO UPDATE SET
        published=excluded.published,
        description=excluded.description,
        cvss=excluded.cvss,
        vector=excluded.vector,
        raw_json=excluded.raw_json
    """, (item["cve_id"], item["published"], item["description"], item["cvss"], item["vector"], item["raw"], now_z()))
    conn.commit()

def main(results=50):
    conn = ensure_db()
    last = read_ts()
    if last:
        # 境界回避で +1s
        try:
            dt = datetime.datetime.fromisoformat(last.replace("Z","+00:00"))
            dt = dt.astimezone(datetime.timezone.utc) + datetime.timedelta(seconds=1)
            start = dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        except Exception:
            start = last
        params = {"pubStartDate": start, "pubEndDate": now_z(), "resultsPerPage": str(results)}
    else:
        params = {"resultsPerPage": str(results)}
    data = fetch(params)
    vulns = data.get("vulnerabilities",[])
    new_count = 0
    for v in vulns:
        s = extract_summary(v)
        if not s["cve_id"]: continue
        # check if exists
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM cves WHERE cve_id=?", (s["cve_id"],))
        if cur.fetchone() is None:
            new_count += 1
        upsert(conn, s)
    api_ts = data.get("timestamp") or now_z()
    write_ts(api_ts)
    print(f"Fetched {len(vulns)} items, new: {new_count}, saved timestamp: {api_ts}")

if __name__ == "__main__":
    main()

