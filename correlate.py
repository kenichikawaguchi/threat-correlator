#!/usr/bin/env python3
# correlate.py - monitor_accesslog × et_signatures × cves 突合

import sqlite3
from datetime import datetime, timedelta

HONEYPOT_DB = "/opt/honeypot-dev/db.sqlite3"
NVD_DB      = "nvd.db"
DAYS        = int(__import__('os').environ.get("DAYS", "30"))

def load_signatures(nvd_conn):
    cur = nvd_conn.cursor()
    cur.execute("""
        SELECT e.sid, e.cve_id, e.msg, e.uri_patterns, e.ua_patterns,
               c.cvss, c.description
        FROM et_signatures e
        LEFT JOIN cves c ON e.cve_id = c.cve_id
        WHERE e.uri_patterns IS NOT NULL OR e.ua_patterns IS NOT NULL
    """)
    return cur.fetchall()

def correlate(hp_conn, sigs, days):
    since = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    cur = hp_conn.cursor()
    cur.execute("""
        SELECT id, timestamp, ip, method, path, user_agent, country
        FROM monitor_accesslog
        WHERE timestamp >= ?
        ORDER BY timestamp DESC
    """, (since,))
    logs = cur.fetchall()
    print(f"Logs in last {days} days: {len(logs)}")

    results = []
    for sid, cve_id, msg, uri_pats, ua_pats, cvss, desc in sigs:
        uri_list = [p for p in (uri_pats.split("|") if uri_pats else []) if len(p) >= 8]
        ua_list  = ua_pats.split("|")  if ua_pats  else []
        for log_id, ts, ip, method, path, ua, country in logs:
            matched = False
            match_type = []
            # URIマッチ(全パターンが含まれる場合のみ)
            if uri_list and all(p.lower() in path.lower() for p in uri_list):
                matched = True
                match_type.append("uri")
            # UAマッチ
            if ua_list and all(p.lower() in ua.lower() for p in ua_list):
                matched = True
                match_type.append("ua")
            if matched:
                results.append({
                    "timestamp": ts,
                    "ip":        ip,
                    "country":   country,
                    "method":    method,
                    "path":      path[:80],
                    "cve_id":    cve_id,
                    "cvss":      cvss,
                    "match":     "+".join(match_type),
                    "msg":       msg[:60],
                })
    return results

def report(results):
    if not results:
        print("No matches found.")
        return

    # CVE別集計
    from collections import Counter
    cve_counts = Counter(r["cve_id"] for r in results)
    print(f"\n{'='*60}")
    print(f"Total matches: {len(results)} | Unique CVEs: {len(cve_counts)}")
    print(f"{'='*60}")
    print(f"\n--- Top CVEs (by hit count) ---")
    for cve_id, count in cve_counts.most_common(20):
        hit = next(r for r in results if r["cve_id"] == cve_id)
        cvss = f"{hit['cvss']:.1f}" if hit['cvss'] else "N/A"
        print(f"  {cve_id} (CVSS:{cvss:>5}) hits={count:>4}  {hit['msg'][:50]}")

    print(f"\n--- Recent matches (latest 20) ---")
    seen = set()
    for r in sorted(results, key=lambda x: x["timestamp"], reverse=True)[:20]:
        key = (r["cve_id"], r["ip"])
        if key in seen:
            continue
        seen.add(key)
        print(f"  [{r['timestamp'][:16]}] {r['cve_id']} CVSS:{r['cvss']} "
              f"{r['ip']} ({r['country']}) {r['match']} {r['path']}")

def main():
    nvd_conn = sqlite3.connect(NVD_DB)
    hp_conn  = sqlite3.connect(HONEYPOT_DB)
    sigs     = load_signatures(nvd_conn)
    print(f"Signatures loaded: {len(sigs)}")
    results  = correlate(hp_conn, sigs, DAYS)
    report(results)
    nvd_conn.close()
    hp_conn.close()

if __name__ == "__main__":
    main()
