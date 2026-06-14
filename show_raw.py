#!/usr/bin/env python3
# show_raw.py
import sqlite3, json, ast, sys

DB = "nvd.db"
CVE = "CVE-2026-54420"

def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT raw_json FROM cves WHERE cve_id=?", (CVE,))
    row = cur.fetchone()
    if not row:
        print("No row found for", CVE)
        conn.close()
        return
    raw = row[0]
    obj = None
    # まず json.loads を試す
    try:
        obj = json.loads(raw)
    except Exception:
        try:
            obj = ast.literal_eval(raw)
        except Exception as e:
            print("Could not parse raw_json:", e, file=sys.stderr)
    if obj is not None:
        print(json.dumps(obj, indent=2, ensure_ascii=False))
    conn.close()

if __name__ == "__main__":
    main()

