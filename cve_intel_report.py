#!/usr/bin/env python3
# cve_intel_report.py — ハニーポット観測CVEの製品別インテリジェンスレポート生成
#
# 出力:
#   reports/cve_intel_YYYYMMDD.md   - Zenn / Qiita 投稿用 Markdown
#   reports/cve_intel_YYYYMMDD.json - aibot.pontalk.com フィード用 JSON
#
# 使い方:
#   python cve_intel_report.py                     # 通常実行
#   python cve_intel_report.py --min-cvss 7.0      # High以上のみ
#   python cve_intel_report.py --days 90           # 90日以内に観測されたもの
#   python cve_intel_report.py --json-only         # JSON のみ生成

import argparse
import json
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

NVD_DB      = "nvd.db"
REPORTS_DIR = Path("reports")


# ─────────────────────────────────────────────────────────────────────────────
# データ取得
# ─────────────────────────────────────────────────────────────────────────────

def load_observed_cves(
    conn: sqlite3.Connection,
    min_cvss: float = 0.0,
    days: int = 0,
    strict_cvss: bool = False,
) -> list[dict]:
    """
    observed_cves × cves × et_signatures を JOIN して観測CVEを取得する。

    Args:
        min_cvss    : CVSS フィルタ（0.0 で全件）
        days        : 0 で全期間、正数なら直近 N 日以内に first_seen があるもののみ
        strict_cvss : True のとき CVSS NULL エントリを除外する
                      False（デフォルト）のとき NULL も含める
    """
    date_filter = ""
    params: list = [min_cvss]
    if days > 0:
        cutoff = (datetime.now(timezone.utc)
                  .replace(tzinfo=None)
                  .strftime("%Y-%m-%d"))
        date_filter = "AND date(o.first_seen) >= date(?, '-{} days')".format(days)
        params.append(cutoff)

    # --strict-cvss のとき NULL を除外、デフォルトは NULL も含める
    cvss_filter = "c.cvss >= ?" if strict_cvss else "(c.cvss >= ? OR c.cvss IS NULL)"

    cur = conn.cursor()
    cur.execute(f"""
        SELECT
            o.cve_id,
            o.first_seen,
            o.last_seen,
            o.hit_count,
            o.countries,
            c.cvss,
            c.vector,
            c.description,
            c.vendor,
            c.product,
            c.version_end,
            c.version_end_inclusive,
            c.weaknesses,
            COUNT(DISTINCT e.sid)                    AS sig_count,
            GROUP_CONCAT(DISTINCT e.msg)             AS et_msgs
        FROM observed_cves o
        JOIN cves c ON o.cve_id = c.cve_id
        LEFT JOIN et_signatures e ON o.cve_id = e.cve_id
        WHERE {cvss_filter}
        {date_filter}
        GROUP BY o.cve_id
        ORDER BY c.cvss DESC, o.first_seen
    """, params)

    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def load_refs(conn: sqlite3.Connection, cve_ids: list[str]) -> dict[str, list[str]]:
    """CVE ID ごとの参照 URL を取得する（最大 5 件）。"""
    if not cve_ids:
        return {}
    placeholders = ",".join("?" * len(cve_ids))
    cur = conn.cursor()
    cur.execute(
        f"SELECT cve_id, url FROM cve_refs WHERE cve_id IN ({placeholders})",
        cve_ids,
    )
    refs: dict[str, list[str]] = defaultdict(list)
    for cve_id, url in cur.fetchall():
        if len(refs[cve_id]) < 5:
            refs[cve_id].append(url)
    return refs


# ─────────────────────────────────────────────────────────────────────────────
# ユーティリティ
# ─────────────────────────────────────────────────────────────────────────────

def cvss_level(score: float | None) -> str:
    if score is None:
        return "Unknown"
    if score >= 9.0:
        return "Critical"
    if score >= 7.0:
        return "High"
    if score >= 4.0:
        return "Medium"
    return "Low"


def cvss_badge(score: float | None) -> str:
    """Markdown 用の CVSS バッジ文字列（GitHub / Zenn で表示できる形式）。"""
    level = cvss_level(score)
    score_str = f"{score:.1f}" if score is not None else "N/A"
    return f"**CVSS {score_str} ({level})**"


def format_ver_range(row: dict) -> str:
    ver = row.get("version_end")
    if not ver:
        return ""
    op = "<=" if row.get("version_end_inclusive") else "<"
    return f" (version {op} {ver})"


def _normalize_vendor(v: str | None) -> str | None:
    """CPE 由来のアンダースコア形式（SAP_SE など）を人間可読な形式に正規化する。"""
    if not v:
        return None
    return v.replace("_", " ").strip()


def _group_by_vendor(rows: list[dict]) -> tuple[dict[str, list[dict]], list[dict]]:
    """vendor でグルーピング。vendor が None のものは別リストに分ける。"""
    by_vendor: dict[str, list[dict]] = defaultdict(list)
    no_vendor: list[dict] = []
    for r in rows:
        v = _normalize_vendor(r.get("vendor")) or ""
        if v:
            by_vendor[v].append(r)
        else:
            no_vendor.append(r)
    return dict(by_vendor), no_vendor


def _sort_rows(rows: list[dict]) -> list[dict]:
    return sorted(rows, key=lambda r: (-(r["cvss"] or 0), r["first_seen"] or ""))


# ─────────────────────────────────────────────────────────────────────────────
# Markdown 生成
# ─────────────────────────────────────────────────────────────────────────────

def generate_markdown(
    rows: list[dict],
    refs: dict[str, list[str]],
    generated_at: str,
    min_cvss: float,
) -> str:
    total      = len(rows)
    critical   = sum(1 for r in rows if (r["cvss"] or 0) >= 9.0)
    high       = sum(1 for r in rows if 7.0 <= (r["cvss"] or 0) < 9.0)
    with_prod  = sum(1 for r in rows if r.get("product") or r.get("vendor"))
    et_covered = sum(1 for r in rows if (r.get("sig_count") or 0) > 0)

    lines: list[str] = []

    # ── ヘッダー ──────────────────────────────────────────────────────────────
    lines += [
        "# ハニーポット観測 CVE インテリジェンスレポート",
        "",
        f"> 生成日時: {generated_at}  ",
        f"> データソース: AIBOT RADAR honeypot × ET Open × NVD / CIRCL  ",
        f"> CVSS フィルタ: {min_cvss:.1f} 以上",
        "",
        "## 概要",
        "",
        "AIBOT RADAR ハニーポットで実際に観測された CVE の一覧です。",
        "Emerging Threats (ET Open) ルールとの突合により、",
        "実際の攻撃トラフィックと紐付けられたものだけを掲載しています。",
        "",
        "| 指標 | 値 |",
        "| --- | --- |",
        f"| 観測 CVE 総数 | {total} |",
        f"| Critical (CVSS≥9.0) | {critical} |",
        f"| High (CVSS≥7.0) | {high} |",
        f"| 製品情報あり | {with_prod} / {total} |",
        f"| ET シグネチャ対応 | {et_covered} / {total} |",
        "",
    ]

    # ── Critical CVE のハイライトテーブル ────────────────────────────────────
    critical_rows = _sort_rows([r for r in rows if (r["cvss"] or 0) >= 9.0])
    if critical_rows:
        lines += [
            "## 🔴 Critical CVE ハイライト",
            "",
            "| CVE ID | CVSS | 製品 | 初回観測 | ET Sig |",
            "| --- | --- | --- | --- | --- |",
        ]
        for r in critical_rows:
            raw_product = r.get("product") or r.get("vendor") or "不明"
            vendor_norm = _normalize_vendor(r.get("vendor")) or ""
            # product 欄はセミコロン区切りの最初の要素のみ、40文字でトリム
            product_first = raw_product.split(";")[0].strip()
            product_display = (product_first[:40] + "…") if len(product_first) > 40 else product_first
            ver      = format_ver_range(r)
            cvss_str = f"{r['cvss']:.1f}" if r["cvss"] else "N/A"
            first    = (r.get("first_seen") or "")[:10]
            sigs     = r.get("sig_count") or 0
            lines.append(
                f"| {r['cve_id']} | {cvss_str} | {product_display}{ver} | {first} | {sigs} |"
            )
        lines += ["", "---", ""]

    # ── 製品別詳細 ────────────────────────────────────────────────────────────
    lines += ["## 製品別 CVE 詳細", ""]

    by_vendor, no_vendor = _group_by_vendor(rows)

    for vendor in sorted(by_vendor.keys()):
        lines.append(f"### {vendor}")
        lines.append("")
        for r in _sort_rows(by_vendor[vendor]):
            _append_cve_block(lines, r, refs)

    if no_vendor:
        lines.append("### その他 / ベンダー不明")
        lines.append("")
        for r in _sort_rows(no_vendor):
            _append_cve_block(lines, r, refs)

    # ── フッター ──────────────────────────────────────────────────────────────
    lines += [
        "---",
        "",
        "> **注意**: 本レポートはハニーポットへの観測トラフィックをもとに自動生成されています。",
        "> 掲載されている CVE が必ずしもお使いの環境に影響を与えるとは限りません。",
        "> 詳細は各 CVE の公式アドバイザリをご確認ください。",
        "",
        f"*Generated by cve_intel_report.py at {generated_at}*",
    ]

    return "\n".join(lines)


def _append_cve_block(
    lines: list[str], row: dict, refs: dict[str, list[str]]
) -> None:
    cve_id   = row["cve_id"]
    product  = (row.get("product") or "").strip() or "不明"
    ver      = format_ver_range(row)
    desc     = (row.get("description") or "")[:300].replace("\n", " ")
    first    = (row.get("first_seen") or "")[:10]
    sig_count = row.get("sig_count") or 0
    et_msg   = (row.get("et_msgs") or "").split(",")[0][:80]
    weaknesses = row.get("weaknesses") or ""
    cve_refs = refs.get(cve_id, [])

    lines += [
        f"#### [{cve_id}](https://nvd.nist.gov/vuln/detail/{cve_id})"
        f" — {product}{ver}",
        "",
        f"- {cvss_badge(row['cvss'])}",
        f"- **初回観測**: {first}",
        f"- **ET シグネチャ数**: {sig_count}"
        + (f"  (`{et_msg}`)" if et_msg else ""),
    ]
    if weaknesses:
        lines.append(f"- **CWE**: {weaknesses}")
    if desc:
        lines.append(f"- **概要**: {desc}{'...' if len(desc) == 300 else ''}")
    if cve_refs:
        lines.append("- **参照**:")
        for url in cve_refs[:3]:
            lines.append(f"  - {url}")
    lines.append("")


# ─────────────────────────────────────────────────────────────────────────────
# JSON フィード生成
# ─────────────────────────────────────────────────────────────────────────────

def generate_json_feed(
    rows: list[dict],
    refs: dict[str, list[str]],
    generated_at: str,
) -> dict:
    entries = []
    for r in rows:
        cve_id = r["cve_id"]
        entries.append({
            "cve_id":                cve_id,
            "cvss":                  r["cvss"],
            "cvss_level":            cvss_level(r["cvss"]),
            "vendor":                r.get("vendor"),
            "product":               r.get("product"),
            "version_end":           r.get("version_end"),
            "version_end_inclusive": bool(r.get("version_end_inclusive")),
            "weaknesses":            r.get("weaknesses"),
            "description":           (r.get("description") or "")[:500],
            "first_seen":            r.get("first_seen"),
            "last_seen":             r.get("last_seen"),
            "hit_count":             r.get("hit_count") or 0,
            "countries":             r.get("countries"),
            "et_sig_count":          r.get("sig_count") or 0,
            "et_msgs": [
                m.strip()
                for m in (r.get("et_msgs") or "").split(",")
                if m.strip()
            ],
            "refs": refs.get(cve_id, []),
        })

    # vendor 別サマリーも付与（ダッシュボード用）
    by_vendor: dict[str, int] = defaultdict(int)
    by_level:  dict[str, int] = defaultdict(int)
    for e in entries:
        by_vendor[e["vendor"] or "Unknown"] += 1
        by_level[e["cvss_level"]] += 1

    return {
        "generated_at": generated_at,
        "total":        len(entries),
        "summary": {
            "by_level":  dict(by_level),
            "by_vendor": dict(sorted(by_vendor.items(), key=lambda x: -x[1])[:20]),
        },
        "entries": entries,
    }


# ─────────────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="ハニーポット観測 CVE インテリジェンスレポート生成"
    )
    parser.add_argument(
        "--min-cvss", type=float, default=0.0,
        help="CVSS フィルタ（デフォルト: 0.0 = 全件）",
    )
    parser.add_argument(
        "--days", type=int, default=0,
        help="直近 N 日以内に観測されたものに絞る（0 = 全期間）",
    )
    parser.add_argument(
        "--json-only", action="store_true",
        help="JSON のみ生成（Markdown をスキップ）",
    )
    parser.add_argument(
        "--strict-cvss", action="store_true",
        help="CVSS が NULL のエントリを除外する（デフォルトは NULL も含める）",
    )
    parser.add_argument(
        "--db", default=NVD_DB,
        help=f"nvd.db のパス（デフォルト: {NVD_DB}）",
    )
    parser.add_argument(
        "--out-dir", default=str(REPORTS_DIR),
        help="出力ディレクトリ（デフォルト: reports/）",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(args.db)
    now  = datetime.now(timezone.utc)
    generated_at = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    date_str     = now.strftime("%Y%m%d")

    print(f"Loading observed CVEs (min_cvss={args.min_cvss}, days={args.days}, strict_cvss={args.strict_cvss}) ...")
    rows = load_observed_cves(conn, min_cvss=args.min_cvss, days=args.days, strict_cvss=args.strict_cvss)
    print(f"  {len(rows)} CVEs found")

    if not rows:
        print("No CVEs to report. Exiting.")
        conn.close()
        return

    cve_ids = [r["cve_id"] for r in rows]
    refs    = load_refs(conn, cve_ids)

    # ── JSON ──────────────────────────────────────────────────────────────────
    json_path = out_dir / f"cve_intel_{date_str}.json"
    feed = generate_json_feed(rows, refs, generated_at)
    json_path.write_text(
        json.dumps(feed, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"JSON:     {json_path}")

    # ── Markdown ──────────────────────────────────────────────────────────────
    if not args.json_only:
        md_path = out_dir / f"cve_intel_{date_str}.md"
        md = generate_markdown(rows, refs, generated_at, args.min_cvss)
        md_path.write_text(md, encoding="utf-8")
        print(f"Markdown: {md_path} ({len(md):,} chars)")

    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
