# correlate.py 仕様書

> `~/repo/threat-correlator/correlate.py`  
> 最終更新: 2026-06-30

---

## 1. 概要

`correlate.py` は、ハニーポットのアクセスログ（`monitor_accesslog`）を
Suricata ET Open シグネチャ（`et_signatures`）および CVE メタデータ（`cves`）と
突合し、脅威インテリジェンスを生成するスクリプトである。

主な処理は以下の 3 段階で構成される。

1. **突合（correlate）** — アクセスログ × ET シグネチャ → マッチ一覧生成
2. **レポート（report）** — マッチ一覧を標準出力にサマリー表示
3. **観測 CVE 保存（_save_observed_cves）** — `observed_cves` テーブルを UPSERT

---

## 2. 実行環境・前提条件

| 項目 | 内容 |
|------|------|
| 実行環境 | Python 3.10 以上（型ヒント `dict[str, str]` 使用のため） |
| 実行サーバー | ashiya（本番ハニーポットサーバー） |
| 依存ライブラリ | 標準ライブラリのみ（`re`, `sqlite3`, `sys`, `datetime`, `os`） |

---

## 3. 設定値

### 3.1 定数

| 定数名 | デフォルト値 | 説明 |
|--------|-------------|------|
| `HONEYPOT_DB` | `/opt/honeypot-dev/db.sqlite3` | ハニーポット SQLite DB パス |
| `NVD_DB` | `nvd.db` | ET シグネチャ・CVE・観測結果を格納する SQLite DB パス |
| `DAYS` | `30` | 集計対象期間（日数）。環境変数 `DAYS` で上書き可能 |

**DAYS の上書き例:**
```bash
DAYS=7 python3 correlate.py
```

### 3.2 RECON_PATH_CVE

ET rules が POST 必須またはクエリパラメータ必須のためにシグネチャ突合でマッチしない、
偵察系 GET probe を補完するための対応表。

```python
RECON_PATH_CVE: dict[str, str] = {
    "/developmentserver/metadatauploader": "CVE-2025-31324",
}
```

- キー: アクセスログの `path` に含まれるべきサブ文字列（小文字比較）
- 値: 対応する CVE-ID
- `report()` の集計には **含まれない**。`_save_observed_cves()` の `first_seen` 算出のみに使用する。
- 新しい偵察パスが判明したらここに追記する。

---

## 4. データベース構造

### 4.1 ハニーポット DB（HONEYPOT_DB）

#### `monitor_accesslog`（読み取り専用）

| カラム | 型 | 説明 |
|--------|----|------|
| `id` | INTEGER | 主キー |
| `timestamp` | TEXT | アクセス日時（`YYYY-MM-DD HH:MM:SS`） |
| `ip` | TEXT | 送信元 IP アドレス |
| `method` | TEXT | HTTP メソッド（GET / POST など） |
| `path` | TEXT | リクエストパス |
| `user_agent` | TEXT | User-Agent ヘッダ（NULL 許容） |
| `country` | TEXT | 送信元国コード |

### 4.2 NVD DB（NVD_DB）

#### `et_signatures`（読み取り専用）

| カラム | 型 | 説明 |
|--------|----|------|
| `sid` | INTEGER | Suricata rule SID |
| `cve_id` | TEXT | 関連 CVE-ID |
| `msg` | TEXT | ルールメッセージ |
| `uri_patterns` | TEXT | URI マッチパターン（`|` 区切り。NULL 許容） |
| `ua_patterns` | TEXT | User-Agent マッチパターン（`|` 区切り。NULL 許容） |

#### `cves`（読み取り専用）

| カラム | 型 | 説明 |
|--------|----|------|
| `cve_id` | TEXT | CVE-ID（主キー） |
| `cvss` | REAL | CVSS スコア |
| `description` | TEXT | CVE 説明文 |

#### `observed_cves`（読み書き。このスクリプトが管理）

| カラム | 型 | 説明 |
|--------|----|------|
| `cve_id` | TEXT | CVE-ID（主キー） |
| `first_seen` | TEXT | 最初に観測した日付（`YYYY-MM-DD`） |
| `last_seen` | TEXT | 最後に観測した日付（`YYYY-MM-DD`） |
| `hit_count` | INTEGER | 当該実行期間（DAYS 日分）のヒット数 |
| `countries` | TEXT | 観測国コードのカンマ区切りリスト |
| `updated_at` | TEXT | レコード更新日時（ISO 8601 UTC） |

> **注意:** テーブルが存在しない場合は `CREATE TABLE IF NOT EXISTS` で自動作成される。
> `last_seen` / `hit_count` / `countries` カラムが存在しない旧スキーマには
> `ALTER TABLE` で自動追加される（冪等対応済み）。

---

## 5. 関数仕様

### 5.1 `load_signatures(nvd_conn) → list[tuple]`

NVD DB から、URI パターンまたは UA パターンを持つ ET シグネチャを全件取得する。

**引数:**

| 引数 | 型 | 説明 |
|------|----|------|
| `nvd_conn` | `sqlite3.Connection` | nvd.db への接続 |

**返り値:** `list[tuple]` — `(sid, cve_id, msg, uri_patterns, ua_patterns, cvss, description)` のリスト

**フィルタ条件:**
- `uri_patterns IS NOT NULL OR ua_patterns IS NOT NULL` を満たすもののみ取得
- `et_signatures` と `cves` を `cve_id` で LEFT JOIN

---

### 5.2 `correlate(hp_conn, sigs, days) → list[dict]`

アクセスログと ET シグネチャを突合してマッチ一覧を返す。

**引数:**

| 引数 | 型 | 説明 |
|------|----|------|
| `hp_conn` | `sqlite3.Connection` | ハニーポット DB への接続 |
| `sigs` | `list[tuple]` | `load_signatures()` の返り値 |
| `days` | `int` | 集計対象日数 |

**返り値:** `list[dict]` — 以下のキーを持つ辞書のリスト

| キー | 型 | 説明 |
|------|----|------|
| `timestamp` | str | アクセス日時 |
| `ip` | str | 送信元 IP |
| `country` | str | 送信元国コード |
| `method` | str | HTTP メソッド |
| `path` | str | リクエストパス（最大 80 文字） |
| `cve_id` | str | マッチした CVE-ID |
| `cvss` | float\|None | CVSS スコア |
| `match` | str | マッチ種別（`uri` / `ua` / `uri+ua`） |
| `msg` | str | ET ルールメッセージ（最大 60 文字） |

**マッチングロジック:**

```
URIマッチ（AND条件）:
  uri_patterns を "|" で分割し、8文字未満のパターンを除外
  残りの全パターンが path（小文字）に含まれる場合 → match_type に "uri" を追加

UAマッチ（AND条件）:
  ua_patterns を "|" で分割
  全パターンが user_agent（小文字、None は "" 扱い）に含まれる場合 → "ua" を追加

いずれか一方でも真なら matched = True
```

> **重要:** URI パターンの 8 文字未満除外は false positive 低減のための意図的な設計。
> 短すぎるパターン（例: `/cgi`）は誤検知の原因となるため除外する。

---

### 5.3 `report(results)`

突合結果を標準出力に整形表示する。

**引数:**

| 引数 | 型 | 説明 |
|------|----|------|
| `results` | `list[dict]` | `correlate()` の返り値 |

**出力内容:**
1. マッチ総数と ユニーク CVE 数のサマリー
2. CVE 別ヒット数 Top 20（CVSS スコア付き）
3. 直近 20 件のマッチ詳細（CVE-ID × IP の重複は除外）

> `RECON_PATH_CVE` による偵察トラフィック（`collect_recon()` の結果）は
> この関数の集計に **含まれない**。

---

### 5.4 `collect_recon(hp_conn, days) → list[dict]`

`RECON_PATH_CVE` に登録されたパスへの GET アクセスを収集する。

**引数:**

| 引数 | 型 | 説明 |
|------|----|------|
| `hp_conn` | `sqlite3.Connection` | ハニーポット DB への接続 |
| `days` | `int` | 集計対象日数 |

**返り値:** `list[dict]` — `{"cve_id": str, "timestamp": str}` のリスト

**動作:**
- `RECON_PATH_CVE` が空の場合は即時 `[]` を返す
- 1 ログ行につき 1 件のみ追加（複数パスにマッチする場合は最初の 1 件）
- HTTP メソッドによるフィルタは行わない（GET 以外も取得される）

---

### 5.5 `_save_observed_cves(nvd_conn, entries) → int`

`entries` を CVE-ID で集約し、`observed_cves` テーブルを UPSERT する。

**引数:**

| 引数 | 型 | 説明 |
|------|----|------|
| `nvd_conn` | `sqlite3.Connection` | nvd.db への接続 |
| `entries` | `list[dict]` | `correlate()` の results + `collect_recon()` の recon の結合リスト |

**返り値:** `int` — UPSERT した CVE の種類数（0 = マッチなし）

**UPSERT の意味論:**

| カラム | 衝突時の挙動 |
|--------|-------------|
| `first_seen` | 既存値と新値の **MIN**（より古い日付を保持） |
| `last_seen` | 新値で **上書き** |
| `hit_count` | 新値で **上書き**（累積ではなく今回 DAYS 日分の集計値） |
| `countries` | 新値で **上書き** |
| `updated_at` | 新値で **上書き** |

> `hit_count` は「累積」ではなく「今回の実行で集計した DAYS 日分の件数」である点に注意。
> 毎回上書きされるため、実行タイミングによって増減する。

**スキップ条件:**
- `cve_id` が空文字列の場合
- `timestamp` が `YYYY-MM-DD` 形式でない場合

---

## 6. 実行フロー

```
main()
  │
  ├─ sqlite3.connect(NVD_DB)      → nvd_conn
  ├─ sqlite3.connect(HONEYPOT_DB) → hp_conn
  │
  ├─ load_signatures(nvd_conn)    → sigs
  │   └─ et_signatures × cves を JOIN して取得
  │
  ├─ correlate(hp_conn, sigs, DAYS) → results
  │   └─ monitor_accesslog × sigs を突合
  │
  ├─ report(results)
  │   └─ 標準出力にサマリー表示
  │
  ├─ collect_recon(hp_conn, DAYS) → recon
  │   └─ RECON_PATH_CVE パスへのアクセスを収集
  │
  ├─ _save_observed_cves(nvd_conn, results + recon) → n
  │   └─ observed_cves を UPSERT
  │
  └─ 接続クローズ（nvd_conn, hp_conn）
```

**標準エラー出力:**
```
[INFO] observed_cves: N CVEs updated (et_matches=M, recon=K)
```

---

## 7. 推奨実行順序

threat-correlator パイプライン全体での推奨実行順序は以下の通り。

```bash
python3 correlate.py          # 突合 + observed_cves 更新
python3 cve_intel_report.py   # 構造化レポート（Markdown / JSON）生成
python3 generate_zenn_article.py  # Zenn 記事生成（Sakura AI 呼び出し）
```

---

## 8. 既知の制限・注意事項

### 8.1 CVE-2025-31324 GET probe が report() に現れない件

**原因:** ET rule（sid: 2061924, 2064148, 2064149）はリクエスト条件として
POST メソッドまたはクエリパラメータを要求するが、zgrab によるスキャンは
`/developmentserver/metadatauploader` への素の GET リクエストのため、
`correlate()` の URI/UA マッチに該当しない。

**暫定対応:** `RECON_PATH_CVE` に登録し、`collect_recon()` で補足している。
これにより `observed_cves` の `first_seen` には反映されるが、
`report()` の「Top CVEs」には表示されない。

**恒久対応の方向性（未実装）:**
- `correlate()` にメソッド非依存のパスマッチモードを追加する
- または `collect_recon()` の結果も `report()` に別セクションとして表示する

### 8.2 hit_count の意味

`observed_cves.hit_count` は累積値ではなく、直近 `DAYS` 日間のカウントである。
毎回上書きされるため、実行間隔によって増減する点に注意。

### 8.3 URI パターンの AND 条件

複数の URI パターンはすべて一致する必要がある（AND 条件）。
単一のパターンでも 8 文字未満のものは除外される。

---

## 9. 変更履歴

| バージョン | 変更内容 |
|------------|---------|
| 初版 | `correlate()` / `report()` / `load_signatures()` の基本実装 |
| v2 | `ua` が NULL の場合のバグ修正（`(ua or "")` による防御） |
| v3 | `observed_cves` テーブル追加（`first_seen` のみ） |
| v4 | `hit_count` / `last_seen` / `countries` カラム追加。旧スキーマへの `ALTER TABLE` 自動追加対応 |
| v5 | `RECON_PATH_CVE` / `collect_recon()` 追加（CVE-2025-31324 GET probe 対応） |
| 現在 | 上記すべてを統合した現行版 |
