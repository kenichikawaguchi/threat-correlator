import sqlite3
conn = sqlite3.connect("nvd.db")
cur = conn.cursor()
cur.execute("SELECT cve_id, refs FROM cves WHERE refs IS NOT NULL")
for cve_id, refs in cur.fetchall():
    for ref in refs.split(';'):
        if ref:
            print(cve_id, ref)
conn.close()

