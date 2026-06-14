#!/usr/bin/env python3
# update_schema.py
import sqlite3, json, ast, logging, datetime, os, shutil

DB = "nvd.db"
BACKUP = "nvd.db.bak"
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def backup_db():
    if not os.path.exists(BACKUP):
        shutil.copy2(DB, BACKUP)
        logging.info("Backup created: %s", BACKUP)

def parse_raw(raw):
    try:
        return json.loads(raw)
    except Exception:
        try:
            return ast.literal_eval(raw)
        except Exception as e:
            logging.warning("parse failed: %s", e)
            return None

def extract(obj):
    c = obj.get("cve", {})
    cve_id = c.get("id")
    published = c.get("published")
    metrics = c.get("metrics", {}) or obj.get("metrics", {})
    cvss = None
    vector = None
    for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV3", "cvssMetricV2", "cvssMetricV40"):
        arr = metrics.get(key)
        if isinstance(arr, list) and arr:
            first = arr[0]
            cvss_data = first.get("cvssData") or first.get("cvss") or first
            cvss = cvss_data.get("baseScore")
            vector = cvss_data.get("vectorString")
            break
    desc = ""
    for d in c.get("descriptions", []):
        if d.get("lang") in ("en", "eng", None) and d.get("value"):
            desc = d.get("value")
            break
    # refs はリストで返す（cve_refs テーブルへの個別INSERT用）
    refs = [r["url"] for r in c.get("references", []) if isinstance(r, dict) and r.get("url")]
    cwes = []
    for w in c.get("weaknesses", []):
        for d in w.get("description", []):
            if d.get("value"):
                cwes.append(d.get("value"))
    cwes_str = ";".join(cwes) if cwes else None
    return {
        "cve_id": cve_id,
        "published": published,
        "cvss": cvss,
        "vector": vector,
        "description": desc,
        "refs": refs,          # list[str]
        "weaknesses": cwes_str,
    }

def ensure_columns(conn):
    """cves テーブルに不足カラムを追加する。refs は cve_refs テーブルで管理するため対象外。"""
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(cves)")
    cols = {r[1] for r in cur.fetchall()}
    if "weaknesses" not in cols:
        cur.execute("ALTER TABLE cves ADD COLUMN weaknesses TEXT")
        logging.info("Added column: weaknesses")
    conn.commit()

def upsert_refs(cur, cve_id: str, urls: list[str]) -> int:
    """cve_refs に INSERT OR IGNORE し、実際に挿入できた件数を返す。"""
    inserted = 0
    for url in urls:
        cur.execute(
            "INSERT OR IGNORE INTO cve_refs(cve_id, url) VALUES(?, ?)",
            (cve_id, url),
        )
        inserted += cur.rowcount
    return inserted

def main():
    backup_db()
    conn = sqlite3.connect(DB)
    ensure_columns(conn)
    cur = conn.cursor()
    cur.execute("SELECT cve_id, raw_json FROM cves")
    rows = cur.fetchall()
    cves_updated = 0
    refs_inserted = 0
    nowz = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    for cve_id, raw in rows:
        obj = parse_raw(raw)
        if not obj:
            logging.warning("Skipping %s: cannot parse raw_json", cve_id)
            continue
        data = extract(obj)
        if not data["cve_id"]:
            logging.warning("Skipping row without cve_id")
            continue
        # cves テーブル更新（refs カラムは対象外）
        cur.execute("""
            UPDATE cves SET
              published   = COALESCE(?, published),
              cvss        = COALESCE(?, cvss),
              vector      = COALESCE(?, vector),
              description = COALESCE(?, description),
              weaknesses  = COALESCE(?, weaknesses),
              raw_json    = ?,
              inserted_at = COALESCE(inserted_at, ?)
            WHERE cve_id = ?
        """, (
            data["published"],
            data["cvss"],
            data["vector"],
            data["description"],
            data["weaknesses"],
            json.dumps(obj, ensure_ascii=False),
            nowz,
            data["cve_id"],
        ))
        cves_updated += 1
        # cve_refs テーブルに参照URLを登録（重複はスキップ）
        refs_inserted += upsert_refs(cur, data["cve_id"], data["refs"])
    conn.commit()
    conn.close()
    logging.info("Updated cves: %d / Inserted into cve_refs: %d", cves_updated, refs_inserted)

if __name__ == "__main__":
    main()
