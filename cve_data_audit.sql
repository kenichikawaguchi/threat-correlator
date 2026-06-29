-- cve_data_audit.sql
-- nvd.db のデータ品質を把握するクエリ集
-- 使い方: sqlite3 nvd.db < cve_data_audit.sql

.headers on
.mode column
.width 30 10 10 10

-- ─────────────────────────────────────────────────────────────────────────────
-- 1. 全体カバレッジ
-- ─────────────────────────────────────────────────────────────────────────────
SELECT '=== 1. 全体カバレッジ ===' AS section;

SELECT
    COUNT(*)                                              AS total_cves,
    SUM(CASE WHEN cvss IS NOT NULL THEN 1 ELSE 0 END)    AS has_cvss,
    SUM(CASE WHEN product IS NOT NULL THEN 1 ELSE 0 END) AS has_product,
    SUM(CASE WHEN vendor  IS NOT NULL THEN 1 ELSE 0 END) AS has_vendor,
    printf("%.1f%%", 100.0 * SUM(CASE WHEN product IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*)) AS product_coverage,
    printf("%.1f%%", 100.0 * SUM(CASE WHEN vendor  IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*)) AS vendor_coverage
FROM cves;

-- ─────────────────────────────────────────────────────────────────────────────
-- 2. ET signatures 紐付き CVE のカバレッジ
-- ─────────────────────────────────────────────────────────────────────────────
SELECT '=== 2. ET signatures 紐付き CVE のカバレッジ ===' AS section;

SELECT
    COUNT(DISTINCT e.cve_id)                                                AS et_cves,
    SUM(CASE WHEN c.cvss    IS NOT NULL THEN 1 ELSE 0 END)                  AS has_cvss,
    SUM(CASE WHEN c.product IS NOT NULL THEN 1 ELSE 0 END)                  AS has_product,
    SUM(CASE WHEN c.vendor  IS NOT NULL THEN 1 ELSE 0 END)                  AS has_vendor,
    printf("%.1f%%", 100.0 * SUM(CASE WHEN c.product IS NOT NULL THEN 1 ELSE 0 END)
        / COUNT(DISTINCT e.cve_id))                                         AS product_coverage
FROM et_signatures e
JOIN cves c ON e.cve_id = c.cve_id;

-- ─────────────────────────────────────────────────────────────────────────────
-- 3. observed_cves のカバレッジ（最重要）
-- ─────────────────────────────────────────────────────────────────────────────
SELECT '=== 3. observed_cves のカバレッジ ===' AS section;

SELECT
    COUNT(DISTINCT o.cve_id)                                                AS observed_total,
    SUM(CASE WHEN c.cvss    IS NOT NULL THEN 1 ELSE 0 END)                  AS has_cvss,
    SUM(CASE WHEN c.product IS NOT NULL THEN 1 ELSE 0 END)                  AS has_product,
    SUM(CASE WHEN c.vendor  IS NOT NULL THEN 1 ELSE 0 END)                  AS has_vendor,
    SUM(CASE WHEN c.cvss >= 9.0 THEN 1 ELSE 0 END)                         AS critical,
    SUM(CASE WHEN c.cvss >= 7.0 AND c.cvss < 9.0 THEN 1 ELSE 0 END)        AS high
FROM observed_cves o
JOIN cves c ON o.cve_id = c.cve_id;

-- ─────────────────────────────────────────────────────────────────────────────
-- 4. 観測済み CVE 一覧（CVSS 降順）
-- ─────────────────────────────────────────────────────────────────────────────
SELECT '=== 4. 観測済み CVE 一覧（CVSS 降順）===' AS section;

SELECT
    o.cve_id,
    printf("%.1f", c.cvss)   AS cvss,
    c.vendor,
    c.product,
    o.first_seen,
    COUNT(DISTINCT e.sid)    AS et_sigs
FROM observed_cves o
JOIN cves c ON o.cve_id = c.cve_id
LEFT JOIN et_signatures e ON o.cve_id = e.cve_id
GROUP BY o.cve_id
ORDER BY c.cvss DESC, o.first_seen;

-- ─────────────────────────────────────────────────────────────────────────────
-- 5. product が NULL で observed な CVE（要フォロー）
-- ─────────────────────────────────────────────────────────────────────────────
SELECT '=== 5. product NULL の observed CVE ===' AS section;

SELECT
    o.cve_id,
    printf("%.1f", c.cvss) AS cvss,
    substr(c.description, 1, 80) AS description_head
FROM observed_cves o
JOIN cves c ON o.cve_id = c.cve_id
WHERE c.product IS NULL AND c.vendor IS NULL
ORDER BY c.cvss DESC;

-- ─────────────────────────────────────────────────────────────────────────────
-- 6. ベンダー別 CVE 数（観測済みのみ）
-- ─────────────────────────────────────────────────────────────────────────────
SELECT '=== 6. ベンダー別 CVE 数（observed のみ）===' AS section;

SELECT
    COALESCE(c.vendor, '(不明)') AS vendor,
    COUNT(*)                     AS cve_count,
    MAX(c.cvss)                  AS max_cvss
FROM observed_cves o
JOIN cves c ON o.cve_id = c.cve_id
GROUP BY c.vendor
ORDER BY cve_count DESC
LIMIT 20;
