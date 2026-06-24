#!/usr/bin/env python3
# et_rules_fetch.py - ET OpenルールからCVEマッピングを抽出してDBに格納

import re, sqlite3, urllib.request, datetime, logging, os, gzip

DB = "nvd.db"
ET_URL = "https://rules.emergingthreats.net/open/suricata-5.0/emerging-all.rules.gz"
CACHE_GZ = "/tmp/emerging-all.rules.gz"
CACHE    = "/tmp/emerging-all.rules"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

RE_SID      = re.compile(r'\bsid:(\d+);')
RE_CVE_REF  = re.compile(r'reference:cve,(\d{4}-\d+)', re.IGNORECASE)
RE_CVE_META = re.compile(r'\bcve CVE-(\d{4}-\d+)', re.IGNORECASE)
RE_MSG      = re.compile(r'msg:"([^"]+)"')
RE_CONTENT  = re.compile(r'content:"([^"]+)"', re.IGNORECASE)
RE_HTTP_URI = re.compile(r'http\.uri')
RE_HTTP_UA  = re.compile(r'http\.user_agent')
RE_URICONT  = re.compile(r'uricontent:"([^"]+)"', re.IGNORECASE)

def ensure_table(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS et_signatures (
            sid        INTEGER PRIMARY KEY,
            cve_id     TEXT,
            msg        TEXT,
            source     TEXT DEFAULT 'et/open',
            updated_at TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_et_sig_cve ON et_signatures(cve_id);
    """)
    # uri_patterns / ua_patterns カラムを後付けで追加
    for col in ("uri_patterns", "ua_patterns"):
        try:
            conn.execute(f"ALTER TABLE et_signatures ADD COLUMN {col} TEXT")
        except Exception:
            pass  # already exists
    conn.commit()
    logging.info("et_signatures table ready")

def download_rules():
    path = "/var/lib/suricata/rules/suricata.rules"
    logging.info("Using installed rules: %s", path)
    return path

def parse_rules(path):
    results = []
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            sid_m = RE_SID.search(line)
            if not sid_m:
                continue
            sid = int(sid_m.group(1))
            # reference:cve,XXXX-XXXXX を優先、なければmetadata中のcveを探す
            m = RE_CVE_REF.search(line) or RE_CVE_META.search(line)
            if not m:
                continue
            cve_id = f"CVE-{m.group(1)}"
            msg_m  = RE_MSG.search(line)
            msg    = msg_m.group(1) if msg_m else ""
            # URIパターン抽出
            uri_parts = RE_URICONT.findall(line)
            if RE_HTTP_URI.search(line):
                uri_parts += RE_CONTENT.findall(line)
            uri_patterns = "|".join(dict.fromkeys(
                p for p in uri_parts if len(p) > 3
            )) or None

            # UAパターン抽出
            ua_patterns = None
            if RE_HTTP_UA.search(line):
                ua_parts = RE_CONTENT.findall(line)
                ua_patterns = "|".join(dict.fromkeys(
                    p for p in ua_parts if len(p) > 3
                )) or None

            results.append((sid, cve_id, msg, uri_patterns, ua_patterns))
    return results

def upsert(conn, records):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    conn.executemany("""
        INSERT INTO et_signatures(sid, cve_id, msg, source, updated_at, uri_patterns, ua_patterns)
        VALUES(?, ?, ?, 'et/open', ?, ?, ?)
        ON CONFLICT(sid) DO UPDATE SET
            cve_id=excluded.cve_id, msg=excluded.msg, updated_at=excluded.updated_at,
            uri_patterns=excluded.uri_patterns, ua_patterns=excluded.ua_patterns
    """, [(s, c, msg, now, uri, ua) for s, c, msg, uri, ua in records])
    conn.commit()

def stats(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*), COUNT(DISTINCT cve_id) FROM et_signatures")
    total, ucves = cur.fetchone()
    cur.execute("""
        SELECT COUNT(*) FROM et_signatures e
        JOIN cves c ON e.cve_id = c.cve_id
    """)
    matched = cur.fetchone()[0]
    logging.info("Signatures: %d | Unique CVEs: %d | NVD DB matched: %d", total, ucves, matched)

def main():
    conn = sqlite3.connect(DB)
    ensure_table(conn)
    rules_file = download_rules()
    logging.info("Parsing...")
    records = parse_rules(rules_file)
    logging.info("CVE-tagged rules found: %d", len(records))
    upsert(conn, records)
    stats(conn)
    conn.close()

if __name__ == "__main__":
    main()
