#!/usr/bin/env python3
# correlate.py - monitor_accesslog × et_signatures × cves 突合

import re                                   # ← 追加
import sqlite3
import sys                                  # ← 追加
from datetime import datetime, timedelta, timezone   # ← timezone 追加

HONEYPOT_DB = "/opt/honeypot-dev/db.sqlite3"
NVD_DB      = "nvd.db"
DAYS        = int(__import__('os').environ.get("DAYS", "30"))

# ── ET rules が POST 必須等でマッチしない「偵察系 GET probe」の CVE 対応表 ──
# observed_cves の first_seen 算出専用。report() の集計には含まれない。
RECON_PATH_CVE: dict[str, str] = {
    "/developmentserver/metadatauploader": "CVE-2025-31324",
    # 偵察パスが増えたらここに追加する
}


# ─────────────────────────────────────────────────────────────────────────────
# 既存関数（変更は最小限）
# ─────────────────────────────────────────────────────────────────────────────

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
        ua_list  = ua_pats.split("|") if ua_pats else []
        for log_id, ts, ip, method, path, ua, country in logs:
            matched    = False
            match_type = []
            # URI マッチ（全パターン AND）
            if uri_list and all(p.lower() in path.lower() for p in uri_list):
                matched = True
                match_type.append("uri")
            # UA マッチ（ua が None のケースを防御）  ← バグ修正
            if ua_list and all(p.lower() in (ua or "").lower() for p in ua_list):
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

    from collections import Counter
    cve_counts = Counter(r["cve_id"] for r in results)
    print(f"\n{'='*60}")
    print(f"Total matches: {len(results)} | Unique CVEs: {len(cve_counts)}")
    print(f"{'='*60}")
    print(f"\n--- Top CVEs (by hit count) ---")
    for cve_id, count in cve_counts.most_common(20):
        hit  = next(r for r in results if r["cve_id"] == cve_id)
        cvss = f"{hit['cvss']:.1f}" if hit["cvss"] else "N/A"
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


# ─────────────────────────────────────────────────────────────────────────────
# 追加関数
# ─────────────────────────────────────────────────────────────────────────────

def collect_recon(hp_conn: sqlite3.Connection, days: int) -> list[dict]:
    """
    RECON_PATH_CVE に登録したパスへの GET アクセスを取得する。

    ET rules が POST 必須 / クエリパラメータ必須のために correlate() で
    マッチしない偵察トラフィックを拾うのが目的。
    report() の集計には含めず、_save_observed_cves() の first_seen 算出のみに使う。

    Returns:
        [{"cve_id": str, "timestamp": str}, ...]
    """
    if not RECON_PATH_CVE:
        return []

    since = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    cur   = hp_conn.cursor()
    cur.execute(
        "SELECT timestamp, path FROM monitor_accesslog WHERE timestamp >= ?",
        (since,),
    )

    recon: list[dict] = []
    for ts, path in cur.fetchall():
        path_lower = (path or "").lower()
        for recon_path, cve_id in RECON_PATH_CVE.items():
            if recon_path in path_lower:
                recon.append({"cve_id": cve_id, "timestamp": ts})
                break   # 1 ログ行につき 1 件のみ追加
    return recon


def _save_observed_cves(nvd_conn: sqlite3.Connection, entries: list[dict]) -> int:
    """
    entries の cve_id × timestamp から observed_cves テーブルを UPSERT する。

    hit_count / last_seen / countries を追加管理する。
    各実行の DAYS 日分のトラフィックを反映する（累積ではなく上書き）。

    Args:
        nvd_conn : nvd.db への接続
        entries  : correlate() の results + collect_recon() の recon

    Returns:
        UPSERT した CVE 種類数（0 ならマッチなし）
    """
    nvd_conn.execute("""
        CREATE TABLE IF NOT EXISTS observed_cves (
            cve_id     TEXT PRIMARY KEY,
            first_seen TEXT NOT NULL,
            last_seen  TEXT,
            hit_count  INTEGER DEFAULT 0,
            countries  TEXT,
            updated_at TEXT NOT NULL
        )
    """)
    # 既存 DB へのカラム追加（ALTER TABLE は冪等ではないため個別に try）
    for col, typedef in [
        ("last_seen", "TEXT"),
        ("hit_count", "INTEGER DEFAULT 0"),
        ("countries", "TEXT"),
    ]:
        try:
            nvd_conn.execute(f"ALTER TABLE observed_cves ADD COLUMN {col} {typedef}")
        except Exception:
            pass  # 既に存在する場合は無視

    # cve_id → {first_seen, last_seen, hit_count, countries} に集約
    cve_agg: dict[str, dict] = {}
    for m in entries:
        cve_id   = (m.get("cve_id") or "").strip().upper()
        date_str = str(m.get("timestamp") or "")[:10]
        country  = (m.get("country") or "").strip()

        if not cve_id or not re.match(r"\d{4}-\d{2}-\d{2}", date_str):
            continue

        if cve_id not in cve_agg:
            cve_agg[cve_id] = {
                "first_seen": date_str,
                "last_seen":  date_str,
                "hit_count":  0,
                "countries":  set(),
            }
        agg = cve_agg[cve_id]
        if date_str < agg["first_seen"]:
            agg["first_seen"] = date_str
        if date_str > agg["last_seen"]:
            agg["last_seen"] = date_str
        agg["hit_count"] += 1
        # country フィルタ（"Local" 等を除外）
        SKIP_COUNTRIES = {"local", "localhost", ""}
        if country and country.lower() not in SKIP_COUNTRIES:
            agg["countries"].add(country)

    if not cve_agg:
        return 0

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    nvd_conn.executemany("""
        INSERT INTO observed_cves
            (cve_id, first_seen, last_seen, hit_count, countries, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(cve_id) DO UPDATE SET
            first_seen = MIN(first_seen, excluded.first_seen),
            last_seen  = excluded.last_seen,
            hit_count  = excluded.hit_count,
            countries  = excluded.countries,
            updated_at = excluded.updated_at
    """, [
        (cid,
         agg["first_seen"],
         agg["last_seen"],
         agg["hit_count"],
         ", ".join(sorted(agg["countries"])),
         now)
        for cid, agg in cve_agg.items()
    ])
    nvd_conn.commit()
    return len(cve_agg)


# ─────────────────────────────────────────────────────────────────────────────

def main():
    nvd_conn = sqlite3.connect(NVD_DB)
    hp_conn  = sqlite3.connect(HONEYPOT_DB)

    sigs = load_signatures(nvd_conn)
    print(f"Signatures loaded: {len(sigs)}")

    results = correlate(hp_conn, sigs, DAYS)
    report(results)

    # ── observed_cves 更新 ────────────────────────────────────────────────
    recon = collect_recon(hp_conn, DAYS)
    n     = _save_observed_cves(nvd_conn, results + recon)
    print(
        f"[INFO] observed_cves: {n} CVEs updated "
        f"(et_matches={len(results)}, recon={len(recon)})",
        file=sys.stderr,
    )
    # ──────────────────────────────────────────────────────────────────────

    nvd_conn.close()
    hp_conn.close()


if __name__ == "__main__":
    main()
