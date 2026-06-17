#!/usr/bin/env python3
# nvd_report.py
"""
NVD 新着CVEレポート生成スクリプト
- 直近取得分の重要CVEをSQLiteから抽出
- さくらのAI Engineで日本語サマリー生成
- Markdownファイルとして保存

使い方:
  python nvd_report.py

環境変数（.envに記載）:
  SAKURA_API_KEY        さくらのAI Engine APIキー
  SAKURA_ENDPOINT       APIエンドポイントURL
  SAKURA_MODEL          モデル名（デフォルト: gpt-oss-120b）
  CVSS_HIGH             High閾値（デフォルト: 7.0）
  CVSS_CRITICAL         Critical閾値（デフォルト: 9.0）
  REPORT_WINDOW_HOURS   取得ウィンドウ（デフォルト: 25時間）
  MAX_AI_CVES           AIに渡す最大CVE数（デフォルト: 30）
"""
import os
import sqlite3
import datetime
import textwrap
from pathlib import Path
from typing import Optional

import requests

# ── 設定 ──────────────────────────────────────────────────────────────────────
DB             = "nvd.db"
REPORT_DIR     = Path("reports")
REPORT_TS_FILE = "last_report_ts.txt"

CVSS_HIGH     = float(os.environ.get("CVSS_HIGH", "7.0"))
CVSS_CRITICAL = float(os.environ.get("CVSS_CRITICAL", "9.0"))
MAX_AI_CVES   = int(os.environ.get("MAX_AI_CVES", "30"))
WINDOW_HOURS  = int(os.environ.get("REPORT_WINDOW_HOURS", "25"))

SAKURA_API_KEY  = os.environ.get("SAKURA_API_KEY", "")
SAKURA_ENDPOINT = os.environ.get("SAKURA_ENDPOINT", "")
SAKURA_MODEL    = os.environ.get("SAKURA_MODEL", "gpt-oss-120b")


# ── タイムスタンプ管理 ────────────────────────────────────────────────────────
def read_report_ts() -> Optional[str]:
    if not Path(REPORT_TS_FILE).exists():
        return None
    s = Path(REPORT_TS_FILE).read_text(encoding="utf-8").strip()
    return s or None


def write_report_ts(ts: str) -> None:
    Path(REPORT_TS_FILE).write_text(ts, encoding="utf-8")


def since_ts() -> str:
    """前回レポートタイムスタンプ。なければ WINDOW_HOURS 時間前を使用。"""
    ts = read_report_ts()
    if ts:
        return ts
    dt = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=WINDOW_HOURS)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")


# ── DB クエリ ─────────────────────────────────────────────────────────────────
def fetch_new_cves(conn: sqlite3.Connection, since: str) -> list[dict]:
    """inserted_at >= since かつ CVSS >= CVSS_HIGH のCVEをスコア降順で取得。"""
    cur = conn.cursor()
    cur.execute("""
        SELECT cve_id, published, cvss, vector, description, weaknesses
        FROM cves
        WHERE inserted_at >= ?
          AND cvss        >= ?
        ORDER BY cvss DESC, published DESC
    """, (since, CVSS_HIGH))
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


# ── AI 要約 ───────────────────────────────────────────────────────────────────
def build_prompt(cves: list[dict]) -> str:
    lines = []
    for c in cves:
        desc = (c["description"] or "")[:300]
        lines.append(f"- {c['cve_id']} (CVSS {c['cvss']}, {c['vector'] or 'N/A'}): {desc}")
    cve_text = "\n".join(lines)

    return textwrap.dedent(f"""\
        以下は直近に公開された重要なCVE一覧です（CVSS {CVSS_HIGH}以上）。
        セキュリティエンジニア向けに日本語で分析レポートを作成してください。

        ## 出力形式（Markdownで）
        1. **全体サマリー**（3〜5文。傾向・特徴を述べる）
        2. **特に注目すべきCVE**（上位3〜5件を選び、理由と影響範囲を説明）
        3. **推奨アクション**（箇条書き。具体的なパッケージ名・バージョンに言及する）

        ## CVE一覧
        {cve_text}
    """)


def call_sakura_ai(prompt: str) -> str:
    if not SAKURA_API_KEY or not SAKURA_ENDPOINT:
        return "_（AI分析スキップ: SAKURA_API_KEY または SAKURA_ENDPOINT が未設定）_"

    payload = {
        "model": SAKURA_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
        "temperature": 0.3,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SAKURA_API_KEY}",
    }
    try:
        r = requests.post(SAKURA_ENDPOINT, json=payload, headers=headers, timeout=90)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"_（AI分析エラー: {e}）_"


# ── Markdown 生成 ─────────────────────────────────────────────────────────────
def _cve_block(c: dict) -> list[str]:
    return [
        f"### {c['cve_id']}",
        "",
        f"| 項目 | 値 |",
        f"|------|-----|",
        f"| CVSS | `{c['cvss']}` |",
        f"| Vector | `{c['vector'] or 'N/A'}` |",
        f"| Weaknesses | `{c['weaknesses'] or 'N/A'}` |",
        f"| Published | {c['published']} |",
        "",
        f"{c['description'] or ''}",
        "",
    ]


def generate_report(cves: list[dict], ai_summary: str, since: str) -> str:
    now     = datetime.datetime.now(datetime.timezone.utc)
    now_str = now.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    critical = [c for c in cves if (c["cvss"] or 0) >= CVSS_CRITICAL]
    high     = [c for c in cves if CVSS_HIGH <= (c["cvss"] or 0) < CVSS_CRITICAL]

    lines = [
        "# NVD 脅威インテリジェンスレポート",
        "",
        f"- **生成日時**: {now.strftime('%Y-%m-%d %H:%M UTC')}",
        f"- **対象期間**: `{since}` 〜 `{now_str}`",
        f"- **重要CVE数**: {len(cves)} 件"
        f"（Critical {CVSS_CRITICAL}+: {len(critical)} 件 / "
        f"High {CVSS_HIGH}〜: {len(high)} 件）",
        "",
        "---",
        "",
        "## AI 分析サマリー",
        "",
        ai_summary,
        "",
        "---",
        "",
    ]

    if critical:
        lines += [f"## 🔴 Critical（CVSS {CVSS_CRITICAL}+）", ""]
        for c in critical:
            lines += _cve_block(c)

    if high:
        lines += [f"## 🟠 High（CVSS {CVSS_HIGH}〜{CVSS_CRITICAL} 未満）", ""]
        for c in high:
            lines += _cve_block(c)

    return "\n".join(lines)


# ── メイン ────────────────────────────────────────────────────────────────────
def main():
    REPORT_DIR.mkdir(exist_ok=True)

    conn  = sqlite3.connect(DB)
    since = since_ts()

    print(f"Querying new CVEs since {since} (CVSS >= {CVSS_HIGH}) ...")
    cves = fetch_new_cves(conn, since)
    conn.close()

    print(f"Found {len(cves)} important CVEs")

    if not cves:
        print("No important CVEs found. Skipping report generation.")
        # タイムスタンプだけ更新して次回の重複取得を防ぐ
        write_report_ts(
            datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        )
        return

    # AI 要約（上限件数まで）
    ai_cves = cves[:MAX_AI_CVES]
    print(f"Calling Sakura AI Engine [{SAKURA_MODEL}] with {len(ai_cves)} CVEs ...")
    ai_summary = call_sakura_ai(build_prompt(ai_cves))

    # レポート生成・保存
    report_md = generate_report(cves, ai_summary, since)
    today     = datetime.datetime.now().strftime("%Y%m%d")
    out_path  = REPORT_DIR / f"nvd_report_{today}.md"
    out_path.write_text(report_md, encoding="utf-8")
    print(f"Report saved: {out_path}")

    # タイムスタンプ更新
    write_report_ts(
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    )


if __name__ == "__main__":
    main()
