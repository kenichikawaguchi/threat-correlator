#!/usr/bin/env python3
# normalize_raw_json.py
import sqlite3, json, ast, sys, traceback

DB = "nvd.db"

def normalize_one(raw):
    try:
        return json.loads(raw)
    except Exception:
        try:
            return ast.literal_eval(raw)
        except Exception:
            return None

def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT cve_id, raw_json FROM cves")
    rows = cur.fetchall()
    updated = 0
    for cve_id, raw in rows:
        obj = normalize_one(raw)
        if obj is None:
            print("Skipping", cve_id, "- could not parse")
            continue
        new_raw = json.dumps(obj, ensure_ascii=False)
        try:
            cur.execute("UPDATE cves SET raw_json=? WHERE cve_id=?", (new_raw, cve_id))
            updated += 1
        except Exception:
            print("Failed to update", cve_id)
            traceback.print_exc()
    conn.commit()
    conn.close()
    print("Updated rows:", updated)

if __name__ == "__main__":
    main()

