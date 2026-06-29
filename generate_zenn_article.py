#!/usr/bin/env python3
# generate_zenn_article.py — CVE Intel JSON → Zenn 投稿用日本語記事生成
#
# 使い方:
#   python generate_zenn_article.py reports/cve_intel_20260628.json
#   python generate_zenn_article.py reports/cve_intel_20260628.json --days 30
#   python generate_zenn_article.py reports/cve_intel_20260628.json --published
#
# 環境変数:
#   ANTHROPIC_API_KEY  Anthropic API キー（.env からも読み込む）

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests


# ─────────────────────────────────────────────────────────────────────────────
# .env 読み込み
# ─────────────────────────────────────────────────────────────────────────────

def _load_dotenv() -> None:
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip().removeprefix("export").strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

_load_dotenv()


# ─────────────────────────────────────────────────────────────────────────────
# 定数
# ─────────────────────────────────────────────────────────────────────────────

SAKURA_ENDPOINT = os.environ.get("SAKURA_ENDPOINT", "https://api.ai.sakura.ad.jp/v1/chat/completions")
SAKURA_MODEL    = os.environ.get("SAKURA_MODEL",    "gpt-oss-120b")
MAX_TOKENS      = 8000

ZENN_FRONT_MATTER = '''\
---
title: "{title}"
emoji: "🛡️"
type: "tech"
topics: ["security", "cve", "honeypot", "cybersecurity"]
published: {published}
---
'''

SYSTEM_PROMPT = """\
あなたは日本のサイバーセキュリティ専門家で、Zenn に技術記事を執筆しています。
ハニーポット（AIBOT RADAR）で実際に観測された CVE データをもとに、
日本のセキュリティエンジニア・システム管理者向けの実用的な記事を書いてください。

## 執筆ルール
- **全文を日本語**で書く（CVE ID・製品名・バージョン番号・URL は英語のまま）
- NVD の英語 description は自然な日本語に翻訳・要約する（直訳ではなく意訳）
- 「実際に日本向けハニーポットで観測された」という独自性を必ず冒頭で強調する
- **各 CVE の解説には必ず「初回観測日・最終観測日・観測回数・観測国」を具体的に記載する**
  - 例：「2026年5月29日に初めて観測され、6月28日時点で計46回、米国・日本から継続してプローブされている」
- 観測回数が多い CVE（特に100回以上）は積極的に攻撃が試みられていると強調する
- セクション見出しに絵文字を使い、読みやすくする
- front matter（--- で囲まれた部分）は含めない
- Zenn の Markdown 形式を使う

## タイトルの書き方
以下のパターンを参考にし、検索性とクリック率を意識したタイトルをつけること：
- 例1：「【2026年6月】日本向けハニーポットで観測された Critical CVE まとめ」
- 例2：「日本向けハニーポットで観測されたCVE 26件を分析 ― 2026年6月版」
- 例3：「AIBOT RADARが捉えた今月の攻撃トレンド：FortiClientEMS に516回のスキャン」
単純な日付＋件数の羅列は避けること。

## 各 CVE の記載構成（Critical は必ずこの順序で）
各製品ごとに以下の4段階で記載すること：
1. **観測結果**：初回・最終観測日、観測回数、観測国のみ。実際に計測した事実だけを書く
2. **脆弱性概要**：NVD の description をもとにした一般的な説明。「この脆弱性は〜を可能にする」という書き方
3. **攻撃例（想定）**：典型的な悪用手法の例。「実際にこの攻撃が来た」ではなく
   「この脆弱性が悪用される場合、〜という手法が想定される」という書き方を必ず守ること
4. **推奨対策**：具体的なバージョン・設定変更を含める

## 表現の禁止事項と言い換え
以下の断定表現は使わず、必ず言い換えること：
- ❌「システム全体が乗っ取られる」→ ✅「システム全体が侵害される可能性がある」
- ❌「データベースを抽出」→ ✅「データベース内の情報が取得される可能性がある」
- ❌「管理者権限でコマンド実行」→ ✅「状況によっては管理者権限でのコマンド実行につながる可能性がある」
- ❌「攻撃シナリオ」という見出し→ ✅「攻撃例（想定）」

## 必須の構成（この順序で）
1. # タイトル
2. ## はじめに（ハニーポットとは何か、今回の観測期間・件数・方法論を 3〜5 文で）
3. ## 🔴 Critical（CVSS 9.0 以上）の観測 CVE
   - 製品ごとに ### 小見出し
   - 各 CVE：観測結果・脆弱性概要・攻撃例（想定）・推奨対策の4段階で記載
4. ## 🟠 High（CVSS 7.0〜8.9）の観測 CVE（簡潔に、表形式可）
5. ## ⚪ CVSS 未確認の観測 CVE（表形式でまとめる）
   - 「Unknown」「不明」は使わず「CVSS 未確認」で統一すること
   - 未確認の理由（古すぎてスコアがない、評価待ちなど）を一言添えると親切
6. ## まとめと対策の優先順位（優先度順のアクションリスト）
7. ## おわりに
   - 必ず以下の1文で締めること：
     「AIBOT RADAR では今後も日本向けハニーポットで観測した攻撃動向を継続的に公開していきます。」

## トーン
- 技術的に正確であること
- 読者が「今すぐパッチを当てよう」と思えるような緊迫感
- しかし煽りすぎず、冷静で専門的な文体
"""


# ─────────────────────────────────────────────────────────────────────────────
# プロンプト構築
# ─────────────────────────────────────────────────────────────────────────────

def _fmt_entry(e: dict) -> str:
    vendor  = (e.get("vendor") or "").replace("_", " ").strip()
    product = e.get("product") or ""
    ver     = ""
    if e.get("version_end"):
        op  = "<=" if e.get("version_end_inclusive") else "<"
        ver = f" (version {op} {e['version_end']})"

    lines = [
        f"CVE ID      : {e['cve_id']}",
        f"CVSS        : {e['cvss']} ({e['cvss_level']})",
        f"製品        : {vendor} {product}{ver}".strip(),
        f"初回観測    : {str(e.get('first_seen') or '')[:10]}",
        f"最終観測    : {str(e.get('last_seen')  or '')[:10]}",
        f"観測回数    : {e.get('hit_count', 0)} 回",
        f"観測国      : {e.get('countries') or '不明'}",
        f"ET Sig 数   : {e.get('et_sig_count', 0)}",
        f"description : {e.get('description', '')[:500]}",
    ]
    if e.get("weaknesses"):
        lines.append(f"CWE         : {e['weaknesses']}")
    refs = (e.get("refs") or [])[:2]
    if refs:
        lines.append(f"参照 URL    : {' / '.join(refs)}")
    return "\n".join(lines)


def build_user_prompt(data: dict, days: int) -> str:
    entries  = data.get("entries", [])
    summary  = data.get("summary", {}).get("by_level", {})
    gen_at   = str(data.get("generated_at", ""))[:10]

    critical = [e for e in entries if e["cvss_level"] == "Critical"]
    high     = [e for e in entries if e["cvss_level"] == "High"]
    unknown  = [e for e in entries if e["cvss_level"] == "Unknown"]

    lines = [
        "## 観測メタデータ",
        f"生成日      : {gen_at}",
        f"観測期間    : 直近 {days} 日間",
        f"総 CVE 数   : {data.get('total', 0)}",
        f"  Critical  : {summary.get('Critical', 0)}",
        f"  High      : {summary.get('High', 0)}",
        f"  Unknown   : {summary.get('Unknown', 0)}",
        "",
        "---",
        "",
        "## Critical CVE 詳細（CVSS 9.0 以上）",
    ]
    for e in critical:
        lines += ["", _fmt_entry(e)]

    lines += ["", "---", "", "## High CVE 詳細（CVSS 7.0〜8.9）"]
    for e in high:
        lines += ["", _fmt_entry(e)]

    lines += ["", "---", "", "## CVSS 未確認 CVE（実際に観測されたため掲載）"]
    for e in unknown:
        lines += ["", _fmt_entry(e)]

    lines += [
        "",
        "---",
        "",
        "上記のデータをもとに、Zenn 技術記事を日本語で書いてください。",
        "front matter（--- で囲む YAML ブロック）は出力に含めないでください。",
        "記事の最初の行は # タイトル で始めてください。",
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# API 呼び出し
# ─────────────────────────────────────────────────────────────────────────────

def call_sakura(user_prompt: str, api_key: str) -> str:
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    body = {
        "model":      SAKURA_MODEL,
        "max_tokens": MAX_TOKENS,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ],
    }
    print(f"Calling Sakura AI ({SAKURA_MODEL}, max_tokens={MAX_TOKENS}) ...")
    r = requests.post(SAKURA_ENDPOINT, json=body, headers=headers, timeout=180)
    r.raise_for_status()
    resp = r.json()

    usage = resp.get("usage", {})
    print(f"  prompt_tokens={usage.get('prompt_tokens', '?')}, "
          f"completion_tokens={usage.get('completion_tokens', '?')}")

    return resp["choices"][0]["message"]["content"]


# ─────────────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="CVE Intel JSON → Zenn 日本語記事生成"
    )
    parser.add_argument(
        "json_path",
        help="cve_intel_*.json のパス",
    )
    parser.add_argument(
        "--days", type=int, default=30,
        help="記事に記載する観測期間（日）。デフォルト 30",
    )
    parser.add_argument(
        "--qiita", action="store_true",
        help="Qiita向け：今回の考察セクションを末尾に追加する",
    )
    parser.add_argument(
        "--published", action="store_true",
        help="Zenn front matter の published を true にする（デフォルト: false）",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("SAKURA_API_KEY"),
        help="さくら AI API キー（デフォルト: $SAKURA_API_KEY）",
    )
    parser.add_argument(
        "--out-dir", default="reports",
        help="出力ディレクトリ（デフォルト: reports/）",
    )
    args = parser.parse_args()

    # ── API キー確認 ──────────────────────────────────────────────────────────
    if not args.api_key:
        print("ERROR: SAKURA_API_KEY が未設定です。", file=sys.stderr)
        print("  export SAKURA_API_KEY=xxxx", file=sys.stderr)
        print("  または .env ファイルに SAKURA_API_KEY=xxxx を記載してください。",
              file=sys.stderr)
        sys.exit(1)

    # ── JSON 読み込み ─────────────────────────────────────────────────────────
    json_path = Path(args.json_path)
    if not json_path.exists():
        print(f"ERROR: {json_path} が見つかりません。", file=sys.stderr)
        sys.exit(1)

    data = json.loads(json_path.read_text(encoding="utf-8"))
    print(f"Loaded: {json_path} ({data.get('total', 0)} CVEs)")

    # ── プロンプト構築 → API 呼び出し ─────────────────────────────────────────
    user_prompt  = build_user_prompt(data, args.days)

    # Qiita モード：考察セクションの追加指示を付与
    if args.qiita:
        user_prompt += (
            "\n\n---\n\n"
            "## Qiita 向け追加指示\n"
            "「おわりに」の直前に「## 今回の観測で気づいたこと」セクションを追加してください。\n"
            "観測データを見て意外だった点・注目すべき点を 3〜5 点、箇条書きで記載してください。\n"
            "例：\n"
            "- FortiClientEMS（CVE-2026-21643）が516回と突出しており、現在進行形で攻撃が試みられている\n"
            "- SAP NetWeaver は CVSS 10.0 にもかかわらず5月末から継続観測されており、パッチ適用が進んでいない環境が多いと推測される\n"
            "- 1回のみ観測（Netherlands）の CVE が多く、自動スキャナによる横断的な探索と考えられる\n"
            "このような視点で、データから読み取れる傾向を分析的に記載してください。"
        )
    article_body = call_sakura(user_prompt, args.api_key)

    # ── タイトル抽出（本文の最初の # 行） ────────────────────────────────────
    title = "ハニーポット観測 CVE インテリジェンスレポート"
    for line in article_body.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    # ── Zenn front matter を付与して保存 ─────────────────────────────────────
    front_matter = ZENN_FRONT_MATTER.format(
        title=title,
        published="true" if args.published else "false",
    )
    full_article = front_matter + "\n" + article_body

    out_dir  = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = out_dir / f"zenn_{date_str}.md"
    out_path.write_text(full_article, encoding="utf-8")

    print(f"Done: {out_path} ({len(full_article):,} chars)")


if __name__ == "__main__":
    main()
