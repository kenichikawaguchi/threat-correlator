#!/usr/bin/env python3
# nvd_cpe_extractor.py — NVD raw_json の CPE から product/vendor を抽出する
#
# 背景:
#   extract_product_vendor() は CVE JSON 5.0 (CIRCL) の
#   containers.cna.affected を読む。
#   NVD API 2.0 の raw_json は configurations.nodes[].cpeMatch[].criteria
#   （CPE 2.3 形式）に製品情報が入っているが、これを今のパイプラインは
#   一切読んでいない。本モジュールでそのギャップを埋める。
#
# CPE 2.3 形式:
#   cpe:2.3:<part>:<vendor>:<product>:<version>:...
#   例: cpe:2.3:a:apache:log4j:*:*:*:*:*:*:*:*
#
# 使い方:
#   from nvd_cpe_extractor import extract_from_nvd_raw, apply_cpe_backfill
#
#   # 1件だけ試す
#   product, vendor = extract_from_nvd_raw(json.loads(raw_json))
#
#   # DB 全体にバックフィル
#   apply_cpe_backfill("nvd.db", dry_run=True)

import json
import re
import sqlite3
from collections import Counter


# ─────────────────────────────────────────────────────────────────────────────
# CPE パーサー
# ─────────────────────────────────────────────────────────────────────────────

_CPE_RE = re.compile(
    r"^cpe:2\.3:[aho\*\-]:"
    r"(?P<vendor>[^:]+):"
    r"(?P<product>[^:]+):"
)

# 意味のないプレースホルダー
_SKIP = {"*", "-", "n/a", "na", "unknown", "any"}

# ベンダー名のノーマライズ（NVD の vendor フィールドは小文字+アンダースコアが多い）
def _normalize(s: str) -> str:
    return s.replace("_", " ").strip()


def parse_cpe(cpe_uri: str) -> tuple[str | None, str | None]:
    """CPE URI から (vendor, product) のタプルを返す。無効なら (None, None)。"""
    m = _CPE_RE.match(cpe_uri)
    if not m:
        return None, None
    vendor  = _normalize(m.group("vendor"))
    product = _normalize(m.group("product"))
    if vendor.lower() in _SKIP:
        vendor = None
    if product.lower() in _SKIP:
        product = None
    return vendor, product


def extract_from_nvd_raw(data: dict) -> tuple[str | None, str | None]:
    """
    NVD API 2.0 の raw JSON から製品/ベンダー情報を CPE ベースで抽出する。

    configurations → nodes → cpeMatch → criteria を走査し、
    vulnerable=true のエントリを優先してカウント集計する。
    最多出現ベンダー/製品ペアを返す。

    Returns:
        (product, vendor): 取得できない場合は None
    """
    # NVD API 2.0: vulnerabilities[0].cve.configurations[].nodes[].cpeMatch[]
    # もしくは    vulnerabilities[0].cve.configurations[].nodes[].children[].cpeMatch[]
    cve_obj = data.get("cve") or data  # トップが cve オブジェクト直のケースも

    configs = cve_obj.get("configurations", [])
    if not configs:
        # 古い NVD 形式 (1.0) は configurations.CVE_data_version がある
        return None, None

    vendor_count: Counter = Counter()
    product_count: Counter = Counter()

    def _walk_nodes(nodes: list) -> None:
        for node in nodes:
            for cpe_match in node.get("cpeMatch", []):
                cpe_uri   = cpe_match.get("criteria", "")
                vulnerable = cpe_match.get("vulnerable", False)
                vendor, product = parse_cpe(cpe_uri)
                weight = 2 if vulnerable else 1
                if vendor:
                    vendor_count[vendor] += weight
                if product:
                    product_count[product] += weight
            # 再帰で children も走査
            _walk_nodes(node.get("children", []))

    for config in configs:
        _walk_nodes(config.get("nodes", []))

    top_vendor  = vendor_count.most_common(1)[0][0]  if vendor_count  else None
    top_product = product_count.most_common(1)[0][0] if product_count else None

    return top_product, top_vendor


# ─────────────────────────────────────────────────────────────────────────────
# DB バックフィル
# ─────────────────────────────────────────────────────────────────────────────

def apply_cpe_backfill(
    db_path: str = "nvd.db",
    dry_run: bool = False,
    verbose: bool = False,
) -> tuple[int, int, int]:
    """
    nvd.db の cves テーブルのうち product / vendor が NULL なものに対して
    raw_json の CPE 情報をバックフィルする。

    CIRCL 由来（CVE JSON 5.0）のエントリは extract_product_vendor() で
    すでに埋まっているはずなので、空のものだけを対象にする。

    Args:
        db_path : nvd.db へのパス
        dry_run : True なら UPDATE せず結果だけ表示
        verbose : True なら件ごとに出力

    Returns:
        (updated, skipped_already_filled, skipped_no_cpe)
    """
    conn = sqlite3.connect(db_path)
    cur  = conn.cursor()

    # raw カラム名を判別（raw_json / raw）
    cur.execute("PRAGMA table_info(cves)")
    col_names = {row[1] for row in cur.fetchall()}
    raw_col = next((c for c in ("raw_json", "raw") if c in col_names), None)
    if not raw_col:
        print("[CPE backfill] raw JSON カラムが見つかりません。スキップ。")
        conn.close()
        return 0, 0, 0

    cur.execute(f"""
        SELECT cve_id, {raw_col}
        FROM cves
        WHERE (product IS NULL OR vendor IS NULL)
          AND {raw_col} IS NOT NULL
        ORDER BY cve_id DESC
    """)
    rows = cur.fetchall()
    print(f"[CPE backfill] 対象: {len(rows)} 件")

    updated = skipped_filled = skipped_no_cpe = 0

    for cve_id, raw_str in rows:
        try:
            data    = json.loads(raw_str)
            product, vendor = extract_from_nvd_raw(data)
        except Exception as e:
            if verbose:
                print(f"  [WARN] {cve_id}: parse error: {e}")
            skipped_no_cpe += 1
            continue

        if product is None and vendor is None:
            skipped_no_cpe += 1
            continue

        if verbose:
            print(f"  {cve_id}: vendor={vendor!r} product={product!r}"
                  + (" [DRY]" if dry_run else ""))

        if not dry_run:
            conn.execute("""
                UPDATE cves
                SET
                    product = COALESCE(product, ?),
                    vendor  = COALESCE(vendor,  ?)
                WHERE cve_id = ?
                  AND (product IS NULL OR vendor IS NULL)
            """, (product, vendor, cve_id))
        updated += 1

    if not dry_run:
        conn.commit()
    conn.close()

    print(
        f"[CPE backfill] 完了: updated={updated} "
        f"skipped_no_cpe={skipped_no_cpe}"
        + (" (dry run)" if dry_run else "")
    )
    return updated, skipped_filled, skipped_no_cpe


# ─────────────────────────────────────────────────────────────────────────────
# 単体実行
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="NVD CPE ベース product/vendor バックフィル")
    parser.add_argument("--db", default="nvd.db", help="nvd.db のパス")
    parser.add_argument("--dry-run", action="store_true", help="UPDATE せず確認のみ")
    parser.add_argument("--verbose", action="store_true", help="件ごとに出力")
    args = parser.parse_args()

    apply_cpe_backfill(db_path=args.db, dry_run=args.dry_run, verbose=args.verbose)
