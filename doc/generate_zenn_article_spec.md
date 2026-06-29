# generate_zenn_article.py 仕様書

> `~/repo/threat-correlator/generate_zenn_article.py`  
> 最終更新: 2026-06-30

---

## 1. 概要

`generate_zenn_article.py` は、`cve_intel_report.py` が生成した CVE Intel JSON を
Sakura AI（`gpt-oss-120b`）に投げ、Zenn 投稿用の日本語記事（Markdown）を生成するスクリプトである。

```
cve_intel_YYYYMMDD.json
        │
        ▼
generate_zenn_article.py
        │  Sakura AI API 呼び出し
        ▼
reports/zenn_YYYYMMDD.md
  （Zenn front matter + LLM 生成記事本文）
```

---

## 2. 実行環境・前提条件

| 項目 | 内容 |
|------|------|
| 実行環境 | Python 3.10 以上 |
| 外部ライブラリ | `requests`（唯一の外部依存） |
| 必須環境変数 | `SAKURA_API_KEY`（未設定時はエラー終了） |
| 前提スクリプト | `cve_intel_report.py` を先に実行して JSON を生成しておくこと |

---

## 3. 設定値

### 3.1 環境変数

| 変数名 | デフォルト | 説明 |
|--------|-----------|------|
| `SAKURA_API_KEY` | （必須・デフォルトなし） | Sakura AI の API キー |
| `SAKURA_ENDPOINT` | `https://api.ai.sakura.ad.jp/v1/chat/completions` | API エンドポイント URL |
| `SAKURA_MODEL` | `gpt-oss-120b` | 使用するモデル名 |

環境変数は `.env` ファイルからも読み込まれる（詳細は [4.1節](#41-_load_dotenv--none)）。

### 3.2 定数

| 定数名 | 値 | 説明 |
|--------|-----|------|
| `MAX_TOKENS` | `4096` | LLM の最大出力トークン数（固定値） |

### 3.3 `ZENN_FRONT_MATTER`

生成記事の冒頭に付与される Zenn front matter テンプレート。

```yaml
---
title: "{title}"
emoji: "🛡️"
type: "tech"
topics: ["security", "cve", "honeypot", "cybersecurity"]
published: {published}
---
```

- `{title}`: 生成記事の最初の `# ` 行から自動抽出
- `{published}`: `--published` フラグが True なら `"true"`、False なら `"false"`

### 3.4 `SYSTEM_PROMPT`

Sakura AI に渡すシステムプロンプト。以下の要素で構成される。

**執筆ルール（抜粋）:**
- 全文日本語（CVE ID・製品名・バージョン番号・URL は英語のまま）
- NVD の英語 description は意訳
- 冒頭で「実際に日本向けハニーポットで観測された」独自性を強調
- 各 CVE に「初回観測日・最終観測日・観測回数・観測国」を必ず記載
- 観測回数 100 回以上は積極的な攻撃試行と強調
- front matter は出力に含めない

**必須の記事構成（6 段階）:**

| セクション | 内容 |
|------------|------|
| `# タイトル` | 観測期間・件数が入ったもの |
| `## はじめに` | ハニーポット説明、観測期間・件数・方法論（3〜5 文） |
| `## 🔴 Critical（CVSS 9.0 以上）` | 製品ごとに ### 小見出し。概要・攻撃シナリオ・推奨対策を含める |
| `## 🟠 High（CVSS 7.0〜8.9）` | 簡潔に（表形式可） |
| `## ⚪ CVSS 不明` | 表形式でまとめる |
| `## まとめと対策の優先順位` | 優先度順のアクションリスト |

**トーン:** 技術的に正確、緊迫感あり、しかし煽りすぎない冷静な専門的文体

---

## 4. 関数仕様

### 4.1 `_load_dotenv() → None`

スクリプトと同じディレクトリにある `.env` ファイルを読み込んで環境変数に設定する。
スクリプト起動直後（モジュールレベル）に自動実行される。

**動作仕様:**

- `.env` が存在しない場合はサイレントにスキップ
- 各行の処理ルール:

| 行の形式 | 処理 |
|----------|------|
| `KEY=VALUE` | `os.environ.setdefault(KEY, VALUE)` |
| `export KEY=VALUE` | `export` を除去してから同上 |
| `#` で始まる行 | スキップ（コメント） |
| `=` を含まない行 | スキップ |
| 値の `"` または `'` 囲み | 除去 |

- `os.environ.setdefault` を使うため、**既に環境変数が設定されている場合は `.env` より環境変数が優先される**

---

### 4.2 `_fmt_entry(e) → str`

JSON エントリ 1 件を LLM 向けのテキスト形式に変換する。

**引数:**

| 引数 | 型 | 説明 |
|------|----|------|
| `e` | `dict` | `cve_intel_*.json` の `entries[]` の 1 要素 |

**返り値:** 以下のフィールドを改行区切りで並べた文字列

| フィールド | 変換処理 |
|------------|---------|
| `CVE ID` | そのまま |
| `CVSS` | スコアとレベル文字列 |
| `製品` | `vendor`（アンダースコア → スペース変換後）と `product` を結合 |
| `初回観測` | `first_seen` の先頭 10 文字（`YYYY-MM-DD`） |
| `最終観測` | `last_seen` の先頭 10 文字 |
| `観測回数` | `hit_count` に「回」を付与 |
| `観測国` | `countries`（未設定時は「不明」） |
| `ET Sig 数` | `et_sig_count` |
| `description` | 先頭 500 文字 |
| `CWE` | `weaknesses` が存在する場合のみ出力 |
| `参照 URL` | `refs` の先頭 2 件を ` / ` で結合（存在する場合のみ） |

**バージョン範囲の生成:**
```
version_end_inclusive = True  → " (version <= X.X)"
version_end_inclusive = False → " (version < X.X)"
version_end が空       → 省略
```

---

### 4.3 `build_user_prompt(data, days) → str`

JSON データ全体から LLM へのユーザープロンプト文字列を構築する。

**引数:**

| 引数 | 型 | 説明 |
|------|----|------|
| `data` | `dict` | `cve_intel_*.json` の全体 |
| `days` | `int` | 記事に記載する観測期間（日数） |

**返り値:** 以下の構造を持つ文字列

```
## 観測メタデータ
生成日      : YYYY-MM-DD
観測期間    : 直近 N 日間
総 CVE 数   : N
  Critical  : N
  High      : N
  Unknown   : N

---

## Critical CVE 詳細（CVSS 9.0 以上）
（_fmt_entry() の結果を CVE ごとに列挙）

---

## High CVE 詳細（CVSS 7.0〜8.9）
（同上）

---

## CVSS 不明 CVE（実際に観測されたため掲載）
（同上）

---

上記のデータをもとに、Zenn 技術記事を日本語で書いてください。
front matter（--- で囲む YAML ブロック）は出力に含めないでください。
記事の最初の行は # タイトル で始めてください。
```

**エントリの分類:**

| セクション | 条件 |
|------------|------|
| Critical | `cvss_level == "Critical"` |
| High | `cvss_level == "High"` |
| Unknown | `cvss_level == "Unknown"` |

> Medium は現状プロンプトに含まれない。`cvss_level == "Medium"` のエントリがある場合、
> ユーザープロンプトに未掲載のまま LLM に渡される。

---

### 4.4 `call_sakura(user_prompt, api_key) → str`

Sakura AI の Chat Completions API を呼び出し、生成テキストを返す。

**引数:**

| 引数 | 型 | 説明 |
|------|----|------|
| `user_prompt` | `str` | `build_user_prompt()` の返り値 |
| `api_key` | `str` | Sakura AI API キー |

**返り値:** `str` — `choices[0].message.content`（LLM が生成した記事本文）

**リクエスト仕様:**

| 項目 | 値 |
|------|----|
| エンドポイント | `SAKURA_ENDPOINT` |
| メソッド | POST |
| Content-Type | `application/json` |
| 認証 | `Authorization: Bearer {api_key}` |
| モデル | `SAKURA_MODEL` |
| max_tokens | `MAX_TOKENS`（4096） |
| タイムアウト | 180 秒 |

**リクエストボディ:**
```json
{
  "model": "gpt-oss-120b",
  "max_tokens": 4096,
  "messages": [
    {"role": "system", "content": "<SYSTEM_PROMPT>"},
    {"role": "user",   "content": "<user_prompt>"}
  ]
}
```

**標準出力（実行ログ）:**
```
Calling Sakura AI (gpt-oss-120b, max_tokens=4096) ...
  prompt_tokens=NNN, completion_tokens=NNN
```

**エラー処理:** `r.raise_for_status()` により HTTP エラー時は例外を送出する（上位でキャッチしない）。

---

## 5. CLI オプション

```
python generate_zenn_article.py <json_path> [OPTIONS]
```

| 引数/オプション | 型 | デフォルト | 説明 |
|-----------------|-----|-----------|------|
| `json_path` | str（位置引数） | （必須） | `cve_intel_*.json` のパス |
| `--days` | int | `30` | 記事に記載する観測期間（日）。JSON の実際のデータ範囲とは独立 |
| `--published` | flag | False | Zenn front matter の `published` を `true` にする |
| `--api-key` | str | `$SAKURA_API_KEY` | Sakura AI API キー |
| `--out-dir` | str | `reports` | 出力ディレクトリ |

### 実行例

```bash
# 通常実行（下書き状態で保存）
python generate_zenn_article.py reports/cve_intel_20260628.json

# 観測期間を 30 日と記載
python generate_zenn_article.py reports/cve_intel_20260628.json --days 30

# 公開状態で生成
python generate_zenn_article.py reports/cve_intel_20260628.json --published
```

---

## 6. 実行フロー

```
main()
  │
  ├─ argparse でオプション解析
  │
  ├─ SAKURA_API_KEY 確認
  │   └─ 未設定なら stderr にエラー出力 → sys.exit(1)
  │
  ├─ json_path の存在確認
  │   └─ 存在しなければ stderr にエラー出力 → sys.exit(1)
  │
  ├─ JSON 読み込み（UTF-8）
  │
  ├─ build_user_prompt(data, args.days) → user_prompt
  │
  ├─ call_sakura(user_prompt, api_key) → article_body
  │   └─ Sakura AI API に POST（タイムアウト 180 秒）
  │
  ├─ タイトル抽出
  │   └─ article_body の先頭から "# " で始まる最初の行を探す
  │       └─ 見つからない場合のフォールバック:
  │           "ハニーポット観測 CVE インテリジェンスレポート"
  │
  ├─ ZENN_FRONT_MATTER を付与して full_article を構成
  │
  ├─ out_dir を作成（parents=True, exist_ok=True）
  │
  └─ reports/zenn_YYYYMMDD.md に書き込み（UTF-8）
```

---

## 7. 出力ファイル

### 7.1 ファイル命名規則

| ファイル | パターン | 例 |
|----------|----------|----|
| Zenn 記事 | `{out_dir}/zenn_{YYYYMMDD}.md` | `reports/zenn_20260630.md` |

- 日付は実行時 UTC 日付
- 同日に複数回実行すると **上書き** される

### 7.2 ファイル構造

```markdown
---
title: "（LLM が生成した記事の # タイトル行）"
emoji: "🛡️"
type: "tech"
topics: ["security", "cve", "honeypot", "cybersecurity"]
published: false
---

（空行）
（LLM が生成した記事本文 — # タイトルから始まる）
```

### 7.3 Zenn 公開フロー（参考）

```bash
# 1. 下書き生成（published: false）
python generate_zenn_article.py reports/cve_intel_20260630.json

# 2. 内容を確認・手動編集

# 3. Zenn CLI でデプロイ（zenn.dev の Zenn CLI を使用する場合）
npx zenn preview   # ローカルプレビュー
npx zenn publish   # 公開
```

---

## 8. 推奨実行順序

```bash
python3 correlate.py             # observed_cves を最新化
python3 cve_intel_report.py      # Markdown + JSON 生成
python3 generate_zenn_article.py reports/cve_intel_$(date +%Y%m%d).json
```

---

## 9. 既知の制限・注意事項

### 9.1 Medium CVE がプロンプトに含まれない

`build_user_prompt()` は CVE を Critical / High / Unknown の 3 セクションに分類する。
`cvss_level == "Medium"` のエントリはユーザープロンプトに含まれないため、
LLM が生成する記事にも反映されない。

Medium を含めたい場合は `build_user_prompt()` に High セクションと同様の処理を追加すること。

### 9.2 --days はプロンプト記載用のみ

`--days` オプションは記事本文に記載する「観測期間 N 日間」という文言を制御するだけで、
JSON からのエントリ抽出には影響しない。
JSON 自体のフィルタリングは `cve_intel_report.py` の `--days` オプションで行う。

### 9.3 同日実行時の上書き

出力ファイル名に日付は含まれるが時刻は含まれないため、
同日中の複数回実行で前回の出力が上書きされる。
バージョン管理が必要な場合は `--out-dir` で日時付きディレクトリを指定すること。

### 9.4 API タイムアウト（180 秒）

`gpt-oss-120b` は大規模モデルのため応答が遅い場合がある。
`max_tokens=4096` での生成は場合によっては 180 秒に近づく可能性があり、
ネットワーク状態によってはタイムアウトが発生する。
その場合は再実行するか、`MAX_TOKENS` を小さくすること。

### 9.5 front matter の topics は固定

`ZENN_FRONT_MATTER` の `topics` は `["security", "cve", "honeypot", "cybersecurity"]` で固定。
特定記事で変更する場合は出力ファイルを手動編集すること。

---

## 10. 変更履歴

| バージョン | 変更内容 |
|------------|---------|
| 初版 | Sakura AI (`gpt-oss-120b`) を使った基本実装 |
| v2 | `--days` / `--published` / `--api-key` / `--out-dir` オプション追加 |
| 現在 | `.env` 読み込み対応（`export KEY=VALUE` 形式サポート）。タイトル自動抽出対応 |
