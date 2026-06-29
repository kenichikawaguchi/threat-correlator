#!/usr/bin/env python3
# et_cve_backfill.py v3 - CIRCL backend + product/vendor バックフィル対応
#
# 変更点 (v2 → v3):
#   - _ensure_product_columns() : 起動時に cves.product/vendor を自動追加
#   - extract_product_vendor()  : affected リストから product/vendor を抽出
#   - extract_circl()           : product/vendor を戻り値に追加
#   - backfill()                : upsert 後に product/vendor を UPDATE
#   - backfill_product_from_raw(): raw カラムから API なしで高速抽出
#   - get_missing_product()     : product/vendor が NULL な行を取得
#   - main()                    : --product-only / --product-refetch フラグ追加

import argparse
import json
import re
import os
import sqlite3
import time
import urllib.request
import urllib.error
import importlib.util

from metadata_extractor import extract_metadata_from_desc

spec = importlib.util.spec_from_file_location("nf", "nvd_latest_fetch.py")
mod  = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
upsert = mod.upsert

DB         = "nvd.db"
MIN_YEAR   = int(os.environ.get("MIN_YEAR", "2015"))
SLEEP_SEC  = 2.0
CIRCL_BASE = "https://cve.circl.lu/api/cve"


# ─────────────────────────────────────────────────────────────────────────────
# 既存関数（変更最小限）
# ─────────────────────────────────────────────────────────────────────────────

def cve_year(cid):
    try:    return int(cid.split("-")[1])
    except: return 0


def fetch_circl(cve_id, max_retry=3):
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
    """CIRCL API レスポンスから CVE メタデータを抽出する。v3 で product/vendor を追加。"""
    meta   = data.get("cveMetadata", {})
    cve_id = meta.get("cveId")
    cna    = data.get("containers", {}).get("cna", {})

    desc = ""
    for d in cna.get("descriptions", []):
        if d.get("lang", "").startswith("en"):
            desc = d.get("value", "")
            break

    cvss = vector = None
    for m in cna.get("metrics", []):
        for key in ("cvssV4_0", "cvssV3_1", "cvssV3_0", "cvssV2_0"):
            if key in m:
                cvss   = m[key].get("baseScore")
                vector = m[key].get("vectorString")
                break
        if cvss:
            break

    cwes = [d["cweId"] for pt in cna.get("problemTypes", [])
            for d in pt.get("descriptions", []) if d.get("cweId")]
    refs = [r["url"] for r in cna.get("references", []) if r.get("url")]

    # ── v3 追加: affected から product/vendor を抽出 ──────────────────────
    product, vendor = extract_product_vendor(data)

    # affected が空の場合は description から製品名を推定（2026年CVEに多い）
    if product is None:
        product = _extract_product_from_desc(desc)

    return {
        "cve_id":      cve_id,
        "published":   meta.get("datePublished", ""),
        "description": desc,
        "cvss":        cvss,
        "vector":      vector,
        "weaknesses":  ";".join(cwes) or None,
        "refs":        refs,
        "raw":         data,
        "product":     product,   # ← 追加
        "vendor":      vendor,    # ← 追加
    }


def get_missing(conn):
    """cves に未収録 or cvss が NULL な et_signatures の CVE ID を返す（既存動作）。"""
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT e.cve_id FROM et_signatures e
        LEFT JOIN cves c ON e.cve_id = c.cve_id
        WHERE c.cve_id IS NULL OR c.cvss IS NULL
        ORDER BY e.cve_id DESC
    """)
    return [r[0] for r in cur.fetchall() if cve_year(r[0]) >= MIN_YEAR]


def backfill(conn, cve_ids):
    """CVE を CIRCL API から取得して cves に upsert する。v3 で product/vendor UPDATE を追加。"""
    total = len(cve_ids)
    ok = skip = err = 0
    for i, cid in enumerate(cve_ids, 1):
        print(f"[{i}/{total}] {cid} ...", end=" ", flush=True)
        try:
            data = fetch_circl(cid)
            if not data:
                print("NOT FOUND")
                skip += 1
            else:
                s = extract_circl(data)
                if s["cve_id"]:
                    upsert(conn, s)
                    # upsert は product/vendor を知らないので別途 UPDATE ── v3 追加
                    _update_product(conn, s["cve_id"], s.get("product"), s.get("vendor"))
                    print(f"OK  cvss={s['cvss']} product={s.get('product') or '-'}")
                    ok += 1
                else:
                    print("PARSE ERR")
                    err += 1
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"ERROR {e}")
            err += 1
        if i < total:
            time.sleep(SLEEP_SEC)
    return ok, skip, err


def report(results):
    pass  # 元コードに report() はなかったが念のためスタブを保持


# ─────────────────────────────────────────────────────────────────────────────
# v3 追加関数
# ─────────────────────────────────────────────────────────────────────────────

def _ensure_product_columns(conn: sqlite3.Connection) -> None:
    """
    cves テーブルに product / vendor カラムがなければ自動追加する。
    migrate_nvd.sql の ALTER TABLE と同等だが冪等に動作する。
    """
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(cves)")
    existing = {row[1] for row in cur.fetchall()}
    changed  = False
    for col in ("product", "vendor"):
        if col not in existing:
            conn.execute(f"ALTER TABLE cves ADD COLUMN {col} TEXT")
            print(f"[MIGRATE] cves.{col} カラムを追加しました")
            changed = True
    if changed:
        conn.commit()



_VER_BOUNDARY = (
    r'\s+(?:before|through|prior\s+to)\s+(?:version\s+)?v?[\d]'  # "through version 1.1.6"
    r'|\s+up\s+to\s+[\w\d]'                         # "up to 4.4.5"
    r'|\s+<=?\s*v?[\d]'                               # "<= 9.5.9"
    r'|\s+versions?\s+[\d<]'                          # "versions 1.0.0"
    r'|\s+releases?\s+[\d]'                           # "releases 20260320"
    r'|\s+v?\d+\.\d'                                 # " 1.2" " v1.2"
    r'|\s+\d+\.\d{1,3}\b'                           # " 1.18"
)
_VERB_STOP = (
    r'\s+(?:allow|could|can\b|fail|deserializ|iterates?|exposes?'
    r'|mishandl|registers?|contains?\s+a\b|impacted|does\s+not'
    r'|is\s+(?:a\b|an\b|the\b|vuln|affect|open|free|based|data)'
    r'|was\s+(?:a\b|an\b)|has\s+(?:a\b|an\b))'
    r"|'s\s+(?:native|AV1|glob)"
    r"|\s*,\s*it\s+is"
    r"|\s*,\s*(?:special|when|while|if)\b"
)
# \. \s = 文末ピリオド+スペースで停止（GL.iNet 等ドット入り製品名では停止しない）
_DESC_STOP = f'(?={_VER_BOUNDARY}|{_VERB_STOP}|\\s*,\\s|\\s*\\.\\s|\\s*\\()'
_NOISE_PREFIX = re.compile(
    r'^(?:This|A|An|The|Some|Multiple|Several|Various|It'
    r'|Authentication|Authorization|Improper|Incorrect|Missing'
    r'|Insufficient|Denial|Cross\-Site|Broken|Subscriber)\s',
    re.I
)
_IN_ANCHOR = (
    r'(?:(?:was|has\s+been|is|been|have\s+been)\s+)?'
    r'(?:found|identified|detected|discovered|determined|reported|disclosed)'
    r'\s+in'
)


def _clean_product(s: str) -> str | None:
    """抽出した製品名から末尾のバージョン番号・記号を除去して長さチェックする。"""
    s = s.strip().rstrip(",.([]")
    s = re.sub(r'\s+v?\d[\d\.x\/\-]*[-\w]*\s*$', '', s).strip()
    s = re.sub(r"'s\s*$", '', s).strip()
    if not (3 <= len(s) <= 80):
        return None
    if _NOISE_PREFIX.match(s):
        return None
    return s


def _extract_product_from_desc(desc: str) -> str | None:
    """
    affected リストが空の場合に description テキストから製品名を推定する。

    Type A "found/identified/... in X [up to/before] version"  <- 2026年CVEの主流
    Type B "X before/through/up to version"
    Type C "In X through/before/,"
    Type D "The X before/through"
    Type E "vulnerability/flaw in X allows/..."
    """
    if not desc:
        return None
    desc = desc.replace('\n', ' ').replace('\r', ' ')
    desc = re.sub(r'^Impact:\s*', '', desc, flags=re.I)

    # Pattern 1: "found/identified/detected/... in X" (最重要・最高信頼度)
    m = re.search(_IN_ANCHOR + r'\s+(.+?)' + _DESC_STOP, desc, re.I)
    if m:
        p = _clean_product(m.group(1))
        if p:
            return p

    # Pattern 2: "In X through/before/," (NVD-style)
    m = re.match(r'^In\s+(.+?)' + _DESC_STOP, desc, re.I)
    if m:
        p = _clean_product(m.group(1))
        if p:
            return p

    # Pattern 3: "The X before/through" (Plugin-style)
    m = re.match(r'^The\s+(.+?)' + _DESC_STOP, desc, re.I)
    if m:
        p = _clean_product(m.group(1))
        if p:
            return p

    # Pattern 4: "vulnerability/flaw in X allows/..."
    m = re.search(r'(?:vulnerability|flaw|weakness|issue)\s+in\s+(.+?)' + _DESC_STOP, desc, re.I)
    if m:
        p = _clean_product(m.group(1))
        if p and not re.match(r'the\s+\w+\s+(?:UI|interface|module|component)\s+of\b', p, re.I):
            return p

    # Pattern 5: "X through/before/up to/..." (文頭が製品名)
    m = re.match(r'^(.+?)' + _DESC_STOP, desc, re.I)
    if m:
        p = _clean_product(m.group(1))
        if p:
            return p

    return None


def extract_product_vendor(data: dict) -> tuple[str | None, str | None]:
    """
    CVE JSON 5.0 の containers.cna.affected から product と vendor を抽出する。

    - 複数エントリは重複除去してセミコロン連結
    - "n/a" / "unknown" は除外
    - 500文字を超える場合はトリム

    Returns:
        (product, vendor): いずれも str | None
    """
    affected = data.get("containers", {}).get("cna", {}).get("affected", [])
    products: list[str] = []
    vendors:  list[str] = []

    for a in affected:
        v = (a.get("vendor")  or "").strip()
        p = (a.get("product") or "").strip()
        if v and v.upper() not in ("N/A", "UNKNOWN"):
            vendors.append(v)
        if p and p.upper() not in ("N/A", "UNKNOWN"):
            products.append(p)

    # dict.fromkeys で重複除去（挿入順保持）
    product = "; ".join(dict.fromkeys(products))[:500] or None
    vendor  = "; ".join(dict.fromkeys(vendors))[:500]  or None
    return product, vendor


def _update_product(
    conn: sqlite3.Connection,
    cve_id: str,
    product: str | None,
    vendor:  str | None,
) -> None:
    """
    cves テーブルの product / vendor を UPDATE する。
    COALESCE により、すでに値があるカラムは上書きしない（NULL のみ埋める）。
    product も vendor も None なら何もしない。
    """
    if product is None and vendor is None:
        return
    conn.execute(
        "UPDATE cves SET product = COALESCE(product, ?), vendor = COALESCE(vendor, ?) WHERE cve_id = ?",
        (product, vendor, cve_id),
    )
    conn.commit()


def get_missing_product(conn: sqlite3.Connection) -> list[str]:
    """
    cves に収録済み（cvss あり）だが product / vendor が両方 NULL な CVE を返す。
    --product-refetch モード用。
    """
    cur = conn.cursor()
    # product/vendor カラムが存在しない場合はスキップ
    cur.execute("PRAGMA table_info(cves)")
    cols = {row[1] for row in cur.fetchall()}
    if "product" not in cols or "vendor" not in cols:
        print("[WARN] product/vendor カラムがありません。先に --product-only を実行してください。")
        return []

    cur.execute("""
        SELECT DISTINCT e.cve_id
        FROM et_signatures e
        JOIN cves c ON e.cve_id = c.cve_id
        WHERE c.cvss IS NOT NULL
          AND (c.product IS NULL AND c.vendor IS NULL)
        ORDER BY e.cve_id DESC
    """)
    return [r[0] for r in cur.fetchall() if cve_year(r[0]) >= MIN_YEAR]


def backfill_product_from_raw(conn: sqlite3.Connection) -> tuple[int, int]:
    """
    cves.raw カラムに保存済みの JSON から product / vendor を抽出して UPDATE する。
    API コールなし・即時完了の高速バックフィル。

    raw カラムがない場合は (0, 0) を返し、--product-refetch への誘導メッセージを表示する。

    Returns:
        (updated, skipped)
    """
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(cves)")
    cols = {row[1] for row in cur.fetchall()}

    # nvd_latest_fetch.py によりカラム名が raw / raw_json どちらでも動くように対応
    raw_col = next((c for c in ("raw_json", "raw") if c in cols), None)
    if not raw_col:
        print("[INFO] raw JSON カラムが存在しません（raw_json / raw どちらもなし）。")
        print("       --product-refetch で CIRCL API から再取得してください。")
        return 0, 0

    cur.execute(f"""
        SELECT cve_id, {raw_col}, description FROM cves
        WHERE (product IS NULL OR vendor IS NULL OR (version_start IS NULL AND version_end IS NULL))
          AND {raw_col} IS NOT NULL
        ORDER BY cve_id DESC
    """)
    rows = cur.fetchall()
    print(f"{raw_col} → product/vendor 抽出対象: {len(rows)} 件")

    updated = 0
    unchanged = 0
    errors = 0
    for i, (cve_id, raw_json, db_desc) in enumerate(rows, start=1):
        try:
            data = json.loads(raw_json)
            product, vendor = extract_product_vendor(data)
            # affected が空 → cves.description カラムを直接使用
            # （raw_json の形式が NVD/CIRCL どちらでも確実に取れる）

            meta = extract_metadata_from_desc(db_desc or "") or {}
            product = product or meta.get("product")
            vendor = vendor or meta.get("vendor")
            version_start = meta.get("version_start")
            version_start_inclusive = meta.get("version_start_inclusive")
            version_end = meta.get("version_end")
            version_end_inclusive = meta.get("version_end_inclusive")

            # conn.execute(
            #     "UPDATE cves SET product = COALESCE(product, ?), vendor = COALESCE(vendor, ?) WHERE cve_id = ?",
            #     (product, vendor, cve_id),
            # )
            product = product.strip() if isinstance(product, str) else None
            vendor = vendor.strip() if isinstance(vendor, str) else None
            product = product or None
            vendor = vendor or None

            version_start = version_start.strip() if isinstance(version_start, str) else None
            version_end = version_end.strip() if isinstance(version_end, str) else None
            version_start = version_start or None
            version_end = version_end or None

            version_start_inclusive = (
                int(version_start_inclusive)
                if version_start_inclusive is not None
                else None
            )

            version_end_inclusive = (
                int(version_end_inclusive)
                if version_end_inclusive is not None
                else None
            )

            cur = conn.execute(
                """
                UPDATE cves
                SET
                    product = COALESCE(product, ?),
                    vendor  = COALESCE(vendor, ?),
                    version_start = COALESCE(version_start, ?),
                    version_start_inclusive = COALESCE(version_start_inclusive, ?),
                    version_end = COALESCE(version_end, ?),
                    version_end_inclusive = COALESCE(version_end_inclusive, ?)
                WHERE cve_id = ?
                  AND (
                        ((product IS NULL OR product = '') AND ? IS NOT NULL)
                     OR ((vendor  IS NULL OR vendor  = '') AND ? IS NOT NULL)
                     OR ((version_start  IS NULL OR version_start  = '') AND ? IS NOT NULL)
                     OR (version_start_inclusive IS NULL AND ? IS NOT NULL)
                     OR ((version_end  IS NULL OR version_end  = '') AND ? IS NOT NULL)
                     OR (version_end_inclusive  IS NULL AND ? IS NOT NULL)
                  )
                """,
                (
                    product,
                    vendor,
                    version_start,
                    version_start_inclusive,
                    version_end,
                    version_end_inclusive,
                    cve_id,
                    product,
                    vendor,
                    version_start,
                    version_start_inclusive,
                    version_end,
                    version_end_inclusive
                ),
            )

            if cur.rowcount:
                updated += 1
            else:
                unchanged += 1

            # updated += 1
            if i % 100 == 0:
                conn.commit()
                print(f"  {i}/{len(rows)} ...", flush=True)
        except Exception as e:
            print(f"  [WARN] {cve_id}: {e}")
            errors += 1

    conn.commit()
    null_after = conn.execute(
        f"""
        SELECT COUNT(*) FROM cves
         WHERE (
            product IS NULL
            OR vendor IS NULL
            OR (version_start IS NULL
                AND version_end IS NULL)
         )
         AND {raw_col} IS NOT NULL
         """
    ).fetchone()[0]
    # print(f"完了: updated={updated}  skipped={skipped}  残NULL={null_after}")
    print(
        f"完了: updated={updated} "
        f"unchanged={unchanged} "
        f"errors={errors} "
        f"残NULL={null_after}"
    )
    return updated, unchanged, errors


# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="et_cve_backfill.py v3 — CIRCL API + product/vendor バックフィル"
    )
    parser.add_argument(
        "--product-only",
        action="store_true",
        help="raw カラムから product/vendor を抽出（API コールなし・高速）",
    )
    parser.add_argument(
        "--product-refetch",
        action="store_true",
        help="product/vendor が NULL な CVE を CIRCL API から再取得",
    )
    args = parser.parse_args()

    conn = sqlite3.connect(DB)
    _ensure_product_columns(conn)   # ← v3: 起動時に自動マイグレーション

    # ── モード分岐 ──────────────────────────────────────────────────────────

    # --product-only: raw JSON から抽出（API 不要）
    if args.product_only:
        backfill_product_from_raw(conn)
        conn.close()
        return

    # --product-refetch: product/vendor 欠損のみ CIRCL から再取得
    if args.product_refetch:
        missing = get_missing_product(conn)
        est     = len(missing) * SLEEP_SEC / 60
        print(f"MIN_YEAR={MIN_YEAR} | product/vendor欠損: {len(missing)} | Est: {est:.0f} min")
        if not missing:
            print("Nothing to fetch.")
            conn.close()
            return
        input("Press Enter to start (Ctrl+C to abort)...")
        ok = skip = err = 0
        try:
            ok, skip, err = backfill(conn, missing)
        except KeyboardInterrupt:
            print("\nInterrupted — re-run to resume.")
        finally:
            conn.close()
        print(f"\nDone. ok={ok} not_found={skip} error={err}")
        return

    # ── デフォルト: 通常バックフィル（既存動作） ────────────────────────────
    missing = get_missing(conn)
    est     = len(missing) * SLEEP_SEC / 60
    print(f"MIN_YEAR={MIN_YEAR} | Missing: {len(missing)} | Backend: CIRCL | Est: {est:.0f} min")
    if not missing:
        print("Nothing to fetch.")
        conn.close()
        return
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
