-- migrate_nvd.sql
-- nvd.db に対して以下の2つの変更を適用する。
-- 実行: sqlite3 /path/to/nvd.db < migrate_nvd.sql
--
-- 冪等設計（何度実行しても安全）。
-- product/vendor カラムはすでに存在する場合は無視される。

-- ── 優先度2: cves テーブルに製品情報カラムを追加 ──────────────────────────────
-- ALTER TABLE は既存カラムがあるとエラーになるため、なければ追加するアプローチ。
-- SQLite は IF NOT EXISTS を ALTER TABLE でサポートしないため、
-- Python 側の et_cve_backfill.py 等でカラム存在チェックを行うこと。
-- （このSQLは初回マイグレーション専用として使用）

ALTER TABLE cves ADD COLUMN product TEXT;
ALTER TABLE cves ADD COLUMN vendor  TEXT;

-- 既存レコードへのバックフィルは et_cve_backfill.py で行う。
-- （NVD API の configurations/cpeMatch から vendor/product を取得して UPDATE）

-- ── 優先度3: observed_cves テーブルを作成 ────────────────────────────────────
-- ハニーポットログと照合して「CVEが観測された最初の日付」を記録するテーブル。
-- correlate.py 等から INSERT OR REPLACE して更新する。

CREATE TABLE IF NOT EXISTS observed_cves (
    cve_id     TEXT PRIMARY KEY,
    first_seen TEXT NOT NULL,    -- 'YYYY-MM-DD' 形式
    updated_at TEXT NOT NULL     -- 最終更新日時 (ISO 8601)
);

CREATE INDEX IF NOT EXISTS idx_observed_cves_first_seen
    ON observed_cves (first_seen);
