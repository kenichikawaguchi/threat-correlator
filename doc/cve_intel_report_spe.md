# cve_intel_report.py 仕様書

> `~/repo/threat-correlator/cve_intel_report.py`  
> 最終更新: 2026-06-30

---

## 1. 概要

`cve_intel_report.py` は、`correlate.py` が更新した `observed_cves` テーブルを起点に、
ハニーポット観測 CVE のインテリジェンスレポートを生成するスクリプトである。

出力は 2 形式。

| ファイル | 用途 |
|----------|------|
| `reports/cve_intel_YYYYMMDD.md` | Zenn / Qiita 投稿用 Markdown |
| `reports/cve_intel_YYYYMMDD.json` | aibot.pontalk.com ダッシュボード用フィード |

---

## 2. 実行環境・前提条件

| 項目 | 内容 |
|------|------|
| 実行環境 | Python 3.10 以上（`float \| None` 型ヒント使用のため） |
| 依存ライブラリ | 標準ライブラリのみ（`argparse`, `json`, `sqlite3`, `collections`, `datetime`, `pathlib`） |
| 前提スクリプト | `correlate.py` を先に実行して `observed_cves` を最新化しておくこと |

---

## 3. CLI オプション

```
python cve_intel_report.py [OPTIONS]
```

| オプション | 型 | デフォルト | 説明 |
|------------|----|-----------|------|
| `--min-cvss` | float | `0.0` | CVSS スコアの下限フィルタ（0.0 = 全件） |
| `--days` | int | `0` | 直近 N 日以内に `first_seen` があるものに絞る（0 = 全期間） |
| `--json-only` | flag | False | JSON のみ生成し Markdown をスキップ |
| `--strict-cvss` | flag | False | CVSS が NULL のエントリを除外（デフォルトは NULL も含める） |
| `--db` | str | `nvd.db` | nvd.db のパス |
| `--out-dir` | str | `reports/` | 出力ディレクトリ（存在しない場合は自動作成） |

### 実行例

```bash
# 通常実行（全件、Markdown + JSON）
python cve_intel_report.py

# High 以上のみ
python cve_intel_report.py --min-cvss 7.0

# 直近 90 日分
python cve_intel_report.py --days 90

# JSON のみ（ダッシュボード更新用）
python cve_intel_report.py --json-only

# CVSS NULL エントリを除外
python cve_intel_report.py --strict-cvss
```

---

## 4. 使用データベーステーブル

すべて `nvd.db` 内のテーブル。すべて **読み取り専用**。

### `observed_cves`

correlate.py が管理するテーブル。このスクリプトの主入力。

| カラム | 型 | 説明 |
|--------|----|------|
| `cve_id` | TEXT | CVE-ID（主キー） |
| `first_seen` | TEXT | 最初に観測した日付（`YYYY-MM-DD`） |
| `last_seen` | TEXT | 最後に観測した日付（`YYYY-MM-DD`） |
| `hit_count` | INTEGER | 直近 DAYS 日間のヒット数 |
| `countries` | TEXT | 観測国コードのカンマ区切りリスト |

### `cves`

| カラム | 型 | 説明 |
|--------|----|------|
| `cve_id` | TEXT | CVE-ID（主キー） |
| `cvss` | REAL | CVSS スコア（NULL 許容） |
| `vector` | TEXT | CVSS ベクトル文字列 |
| `description` | TEXT | CVE 説明文 |
| `vendor` | TEXT | ベンダー名（CPE 由来、アンダースコア形式の場合あり） |
| `product` | TEXT | 製品名（セミコロン区切りで複数存在する場合あり） |
| `version_end` | TEXT | 影響バージョンの上限 |
| `version_end_inclusive` | INTEGER | 1 = 以下（`<=`）、0 = 未満（`<`） |
| `weaknesses` | TEXT | CWE 識別子 |

### `et_signatures`

| カラム | 型 | 説明 |
|--------|----|------|
| `sid` | INTEGER | Suricata rule SID |
| `cve_id` | TEXT | 関連 CVE-ID |
| `msg` | TEXT | ルールメッセージ |

### `cve_refs`

| カラム | 型 | 説明 |
|--------|----|------|
| `cve_id` | TEXT | CVE-ID |
| `url` | TEXT | 参照 URL |

---

## 5. 関数仕様

### 5.1 `load_observed_cves(conn, min_cvss, days, strict_cvss) → list[dict]`

`observed_cves × cves × et_signatures` を JOIN して観測 CVE を取得する。

**引数:**

| 引数 | 型 | デフォルト | 説明 |
|------|----|-----------|------|
| `conn` | `sqlite3.Connection` | — | nvd.db への接続 |
| `min_cvss` | float | `0.0` | CVSS フィルタ下限 |
| `days` | int | `0` | 0 = 全期間、正数 = 直近 N 日以内 |
| `strict_cvss` | bool | `False` | True = CVSS NULL を除外 |

**返り値:** `list[dict]` — 以下のキーを持つ辞書のリスト（CVSS 降順 → first_seen 昇順）

| キー | 説明 |
|------|------|
| `cve_id` | CVE-ID |
| `first_seen` | 初回観測日 |
| `last_seen` | 最終観測日 |
| `hit_count` | ヒット数 |
| `countries` | 観測国 |
| `cvss` | CVSS スコア |
| `vector` | CVSS ベクトル |
| `description` | CVE 説明文 |
| `vendor` | ベンダー名 |
| `product` | 製品名 |
| `version_end` | 影響バージョン上限 |
| `version_end_inclusive` | バージョン条件の包含フラグ |
| `weaknesses` | CWE 識別子 |
| `sig_count` | 対応する ET シグネチャ数（`DISTINCT sid` でカウント） |
| `et_msgs` | ET ルールメッセージのカンマ区切りリスト |

**CVSS フィルタの挙動:**

| `strict_cvss` | SQL 条件 |
|---------------|----------|
| False（デフォルト） | `c.cvss >= ? OR c.cvss IS NULL` |
| True | `c.cvss >= ?` |

**days フィルタの実装:**

```sql
AND date(o.first_seen) >= date(?, '-N days')
```
カットオフ日は実行時 UTC 現在日を使用する。

---

### 5.2 `load_refs(conn, cve_ids) → dict[str, list[str]]`

CVE ID ごとの参照 URL を `cve_refs` テーブルから取得する。

**引数:**

| 引数 | 型 | 説明 |
|------|----|------|
| `conn` | `sqlite3.Connection` | nvd.db への接続 |
| `cve_ids` | `list[str]` | 取得対象の CVE-ID リスト |

**返り値:** `dict[str, list[str]]` — `{cve_id: [url, ...]}` 形式。CVE ごとに最大 5 件。

---

### 5.3 `cvss_level(score) → str`

CVSS スコアをレベル文字列に変換する。

| スコア | 返り値 |
|--------|--------|
| `None` | `"Unknown"` |
| ≥ 9.0 | `"Critical"` |
| ≥ 7.0 | `"High"` |
| ≥ 4.0 | `"Medium"` |
| < 4.0 | `"Low"` |

---

### 5.4 `cvss_badge(score) → str`

Markdown 用の CVSS バッジ文字列を生成する。GitHub / Zenn で太字表示される。

```
**CVSS 10.0 (Critical)**
**CVSS N/A (Unknown)**
```

---

### 5.5 `format_ver_range(row) → str`

`version_end` と `version_end_inclusive` からバージョン範囲文字列を生成する。

| `version_end` | `version_end_inclusive` | 出力例 |
|---------------|------------------------|--------|
| `"7.53"` | 1（True） | `" (version <= 7.53)"` |
| `"7.53"` | 0（False） | `" (version < 7.53)"` |
| NULL / 空文字 | — | `""` |

---

### 5.6 `_normalize_vendor(v) → str | None`

CPE 由来のアンダースコア形式（例: `SAP_SE`）を人間可読な形式（例: `SAP SE`）に変換する。
入力が None または空文字の場合は None を返す。

---

### 5.7 `_group_by_vendor(rows) → (dict[str, list[dict]], list[dict])`

ベンダー別にグルーピングする。

- `_normalize_vendor()` で正規化したベンダー名をキーとする
- ベンダーが None または空文字の行は `no_vendor` リストに分離する

**返り値:** `(by_vendor, no_vendor)`

---

### 5.8 `_sort_rows(rows) → list[dict]`

CVSS 降順 → `first_seen` 昇順でソートする。CVSS が None の場合は 0 扱い。

---

### 5.9 `generate_markdown(rows, refs, generated_at, min_cvss) → str`

Markdown レポート文字列を生成する。

**引数:**

| 引数 | 型 | 説明 |
|------|----|------|
| `rows` | `list[dict]` | `load_observed_cves()` の返り値 |
| `refs` | `dict[str, list[str]]` | `load_refs()` の返り値 |
| `generated_at` | str | ISO 8601 UTC 生成日時 |
| `min_cvss` | float | フィルタに使用した CVSS 下限値（ヘッダ表示用） |

**Markdown の構造:**

```
# ハニーポット観測 CVE インテリジェンスレポート

> 生成日時 / データソース / CVSSフィルタ

## 概要
  統計テーブル（総数、Critical数、High数、製品情報あり数、ET対応数）

## 🔴 Critical CVE ハイライト          ← CVSS≥9.0 のもののみ。該当なし時はセクション自体を省略
  | CVE ID | CVSS | 製品 | 初回観測 | ET Sig |

## 製品別 CVE 詳細
  ### {ベンダー名}（アルファベット順）
    #### [{cve_id}](NVD URL) — {製品名}{バージョン範囲}
      - CVSS バッジ
      - 初回観測
      - ET シグネチャ数
      - CWE（あれば）
      - 概要（300文字でトリム）
      - 参照 URL（最大3件）

  ### その他 / ベンダー不明            ← vendor が None のもの

---
> 注意書き（自動生成レポートの免責）
```

**制限値:**

| 項目 | 上限 |
|------|------|
| Critical ハイライトの製品名表示 | 40 文字（超過時は `…` 付与） |
| CVE 説明文 | 300 文字（超過時は `...` 付与） |
| ET メッセージ（ブロック内） | 80 文字（1 件目のみ） |
| 参照 URL（ブロック内） | 3 件 |

---

### 5.10 `_append_cve_block(lines, row, refs) → None`

`generate_markdown()` から呼ばれる内部関数。
CVE 1 件分の Markdown ブロックを `lines` リストに追記する（破壊的変更）。

---

### 5.11 `generate_json_feed(rows, refs, generated_at) → dict`

JSON フィード辞書を生成する。

**返り値の構造:**

```json
{
  "generated_at": "2026-06-30T12:00:00Z",
  "total": 42,
  "summary": {
    "by_level": {
      "Critical": 3,
      "High": 12,
      "Medium": 20,
      "Unknown": 7
    },
    "by_vendor": {
      "SAP SE": 5,
      "Apache": 4,
      ...
    }
  },
  "entries": [
    {
      "cve_id": "CVE-2025-31324",
      "cvss": 10.0,
      "cvss_level": "Critical",
      "vendor": "SAP_SE",
      "product": "netweaver_application_server_java",
      "version_end": "7.53",
      "version_end_inclusive": true,
      "weaknesses": "CWE-434",
      "description": "...(500文字でトリム)",
      "first_seen": "2025-05-22",
      "last_seen": "2026-06-28",
      "hit_count": 44,
      "countries": "US, NL, CN",
      "et_sig_count": 3,
      "et_msgs": ["ET WEB_SERVER SAP...", "..."],
      "refs": ["https://...", "https://..."]
    }
  ]
}
```

**制限値:**

| 項目 | 上限 |
|------|------|
| `description` | 500 文字 |
| `refs` | `cve_refs` テーブルから最大 5 件 |
| `summary.by_vendor` | Top 20 ベンダーのみ（件数降順） |

> `entries` 内の `vendor` は **正規化しない**（CPE 由来のアンダースコア形式のまま）。
> 正規化が必要な場合は呼び出し側で `replace("_", " ")` を行うこと。

---

## 6. 実行フロー

```
main()
  │
  ├─ argparse でオプション解析
  ├─ out_dir を作成（parents=True, exist_ok=True）
  ├─ sqlite3.connect(args.db) → conn
  │
  ├─ load_observed_cves(conn, min_cvss, days, strict_cvss) → rows
  │   └─ observed_cves × cves × et_signatures を JOIN
  │
  ├─ rows が空なら "No CVEs to report." を出力して終了
  │
  ├─ load_refs(conn, cve_ids) → refs
  │
  ├─ generate_json_feed(rows, refs, generated_at)
  │   └─ reports/cve_intel_YYYYMMDD.json に書き込み
  │
  ├─ --json-only でなければ:
  │   └─ generate_markdown(rows, refs, generated_at, min_cvss)
  │       └─ reports/cve_intel_YYYYMMDD.md に書き込み
  │
  └─ conn.close()
```

---

## 7. 出力ファイル

### 7.1 ファイル命名規則

| ファイル | パターン | 例 |
|----------|----------|----|
| Markdown | `{out_dir}/cve_intel_{YYYYMMDD}.md` | `reports/cve_intel_20260630.md` |
| JSON | `{out_dir}/cve_intel_{YYYYMMDD}.json` | `reports/cve_intel_20260630.json` |

- 日付は実行時 UTC 日付
- 同日に複数回実行すると **上書き** される

### 7.2 文字コード

いずれも UTF-8 で書き込む（`ensure_ascii=False`）。

---

## 8. 推奨実行順序

```bash
python3 correlate.py             # observed_cves を最新化
python3 cve_intel_report.py      # Markdown + JSON 生成
python3 generate_zenn_article.py # Zenn 記事生成（Sakura AI）
```

---

## 9. 既知の制限・注意事項

### 9.1 vendor の正規化スコープ

`_normalize_vendor()` は Markdown 出力（セクション見出し）にのみ適用される。
JSON フィードの `entries[].vendor` は CPE 由来の生の値（例: `SAP_SE`）のまま出力される。

### 9.2 同日実行時の上書き

出力ファイル名に日付は含まれるが時刻は含まれないため、
同日中に複数回実行すると前回の出力が上書きされる。
バージョン管理が必要な場合は `--out-dir` で日時付きディレクトリを指定すること。

```bash
python3 cve_intel_report.py --out-dir reports/$(date +%Y%m%d_%H%M%S)
```

### 9.3 et_msgs の分割

`et_msgs` は `GROUP_CONCAT(DISTINCT e.msg)` の結果（カンマ区切り文字列）を
Python 側でカンマ split している。
ET ルールの `msg` にカンマが含まれる場合、分割結果が意図しないものになる可能性がある。

### 9.4 CVSS NULL エントリの扱い

デフォルト（`--strict-cvss` 未指定）では CVSS が NULL のエントリも取得される。
これらは `cvss_level()` で `"Unknown"` に分類され、
`_sort_rows()` では CVSS = 0 として昇順最下位に配置される。

---

## 10. 変更履歴

| バージョン | 変更内容 |
|------------|---------|
| 初版 | 基本実装（Markdown + JSON 生成） |
| v2 | `--strict-cvss` オプション追加。CVSS NULL エントリをデフォルト包含に変更 |
| v3 | `last_seen` / `hit_count` / `countries` を JSON フィードに追加 |
| 現在 | `--db` / `--out-dir` オプション追加。`_normalize_vendor()` 追加 |
