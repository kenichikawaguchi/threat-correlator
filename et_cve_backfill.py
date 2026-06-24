#!/usr/bin/env python3
# et_cve_backfill.py v2 - CIRCL backend

import os, sqlite3, time, json, importlib.util, urllib.request

spec = importlib.util.spec_from_file_location("nf", "nvd_latest_fetch.py")
mod  = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
upsert = mod.upsert

DB        = "nvd.db"
MIN_YEAR  = int(os.environ.get("MIN_YEAR", "2015"))
SLEEP_SEC = 2.0
CIRCL_BASE = "https://cve.circl.lu/api/cve"

def cve_year(cid):
    try: return int(cid.split("-")[1])
    except: return 0

def fetch_circl(cve_id, max_retry=3):
    import urllib.error
    url = f"{CIRCL_BASE}/{cve_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "threat-correlator/1.0"})
    for attempt in range(max_retry):
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 60 * (attempt + 1)
                print(f"\n  [429] wait {wait}s ...", end=" ", flush=True)
                time.sleep(wait)
            else:
                raise
    raise Exception("429 persists")

def extract_circl(data):
    meta   = data.get("cveMetadata", {})
    cve_id = meta.get("cveId")
    cna    = data.get("containers", {}).get("cna", {})

    desc = ""
    for d in cna.get("descriptions", []):
        if d.get("lang", "").startswith("en"):
            desc = d.get("value", ""); break

    cvss = vector = None
    for m in cna.get("metrics", []):
        for key in ("cvssV4_0", "cvssV3_1", "cvssV3_0", "cvssV2_0"):
            if key in m:
                cvss   = m[key].get("baseScore")
                vector = m[key].get("vectorString")
                break
        if cvss: break

    cwes = [d["cweId"] for pt in cna.get("problemTypes", [])
            for d in pt.get("descriptions", []) if d.get("cweId")]
    refs = [r["url"] for r in cna.get("references", []) if r.get("url")]

    return {"cve_id": cve_id, "published": meta.get("datePublished", ""),
            "description": desc, "cvss": cvss, "vector": vector,
            "weaknesses": ";".join(cwes) or None, "refs": refs, "raw": data}

def get_missing(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT e.cve_id FROM et_signatures e
        LEFT JOIN cves c ON e.cve_id = c.cve_id
        WHERE c.cve_id IS NULL OR c.cvss IS NULL ORDER BY e.cve_id DESC
    """)
    return [r[0] for r in cur.fetchall() if cve_year(r[0]) >= MIN_YEAR]

def backfill(conn, cve_ids):
    total = len(cve_ids)
    ok = skip = err = 0
    for i, cid in enumerate(cve_ids, 1):
        print(f"[{i}/{total}] {cid} ...", end=" ", flush=True)
        try:
            data = fetch_circl(cid)
            if not data:
                print("NOT FOUND"); skip += 1
            else:
                s = extract_circl(data)
                if s["cve_id"]:
                    upsert(conn, s)
                    print(f"OK  cvss={s['cvss']}"); ok += 1
                else:
                    print("PARSE ERR"); err += 1
        except KeyboardInterrupt: raise
        except Exception as e:
            print(f"ERROR {e}"); err += 1
        if i < total:
            time.sleep(SLEEP_SEC)
    return ok, skip, err

def main():
    conn    = sqlite3.connect(DB)
    missing = get_missing(conn)
    est     = len(missing) * SLEEP_SEC / 60
    print(f"MIN_YEAR={MIN_YEAR} | Missing: {len(missing)} | Backend: CIRCL | Est: {est:.0f} min")
    if not missing:
        print("Nothing to fetch."); return
    input("Press Enter to start (Ctrl+C to abort)...")
    ok = skip = err = 0
    try:
        ok, skip, err = backfill(conn, missing)
    except KeyboardInterrupt:
        print("\nInterrupted — re-run to resume.")
    finally:
        conn.close()
    print(f"\nDone. ok={ok} not_found={skip} error={err}")

if __name__ == "__main__":
    main()
