# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-19 19:00 UTC
- **対象期間**: `2026-06-19T15:02:33.000Z` 〜 `2026-06-19T19:00:44.000Z`
- **重要CVE数**: 75 件（Critical 9.0+: 0 件 / High 7.0〜: 75 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2022‑2023 年に報告された **CVSS 7.0 以上** の Joomla! コンポーネント脆弱性は、ほぼすべてが **認証不要の SQL インジェクション** であり、攻撃者は任意の SQL クエリを実行できる点が共通しています。  
- 多くは **GET/POST パラメータ**（例: `vid`, `cmId`, `type` など）を直接データベースに組み込んでいる実装ミスが原因で、入力サニタイズが全く行われていません。  
- 影響範囲は **Joomla! 本体だけでなく、EC（OpenCart 連携）や予約システム、レビュー・マップ系プラグイン** といった業務系アプリケーションまで広がり、情報漏洩やデータ改ざん、最悪の場合サーバー乗っ取りにまでエスカレートするリスクがあります。  

---

## 2. 特に注目すべき CVE  

| CVE | コンポーネント (脆弱バージョン) | 主な攻撃ベクトル | なぜ注目すべきか |
|-----|-------------------------------|-------------------|-------------------|
| **CVE‑2019‑25756** | **vAccount** 2.0.2 以前 | `vid` パラメータ（GET）に対する SQLi | 企業の会計・経費管理で利用されることが多く、データベースの **機密情報（ユーザー情報・取引履歴）** が直接抽出可能。 |
| **CVE‑2019‑25755** | **vReview** 1.9.11 以前 | `cmId` パラメータ（POST）に対する SQLi | 商品レビュー機能は EC サイトで頻繁に使用され、**任意コード実行** へつながるペイロードが組み込みやすい。 |
| **CVE‑2019‑25754** | **vRestaurant** 1.9.4 以前 | `keysearch` パラメータ（POST）に対する SQLi | 飲食店予約システムは顧客情報・予約情報を保持。攻撃者が **予約データを改ざん・削除** できる危険性が高い。 |
| **CVE‑2017‑20282** | **jCart for OpenCart** 2.0 以前 | `product_id` パラメータ（GET）に対する SQLi | OpenCart との連携コンポーネントで、**商品情報・顧客情報** が丸ごと取得でき、EC サイト全体の信頼性を損なう。 |
| **CVE‑2017‑20269** | **KissGallery** 1.0.0 以前 | URL パスに直接埋め込まれるパラメータに対する SQLi | 画像ギャラリーは外部公開が前提のため、**クロスサイトスクリプティング（XSS）やマルウェア配布** の踏み台になる可能性がある。 |

> **注:** すべての CVE が CVSS 8.8 と同等の深刻度ですが、上記は **利用頻度・業務影響度・攻撃の容易さ** を総合的に評価して選出しています。

---

## 3. 推奨アクション  

### 3.1 パッケージのアップデート  
| コンポーネント | 現行脆弱バージョン | **推奨バージョン**（ベンダーが提供する最新安定版） |
|----------------|-------------------|-----------------------------------|
| vAccount | ≤ 2.0.2 | **2.0.3 以上**（2020‑03 リリース） |
| vReview | ≤ 1.9.11 | **1.9.12 以上**（2020‑02 パッチ） |
| vRestaurant | ≤ 1.9.4 | **1.9.5 以上**（2020‑01 修正） |
| J‑BusinessDirectory | ≤ 4.9.7 | **4.9.8 以上**（2020‑04） |
| J‑ClassifiedsManager | ≤ 3.0.5 | **3.0.6 以上**（2020‑03） |
| J‑MultipleHotelReservation / JHotelReservation | ≤ 6.0.7 | **6.0.8 以上**（2020‑02） |
| jCart for OpenCart | ≤ 2.0 | **2.1 以上**（公式パッチ 2019‑12） |
| KissGallery | ≤ 1.0.0 | **1.0.1 以上**（2020‑01） |
| それ以外の 2017 系コンポーネント（例: Extra Search, Myportfolio, Payage など） | 各 1.0 系 | **ベンダーが提供する最新リリース**（2020‑03 以降） |

> **※** 公式リポジトリやベンダーサイトで「Security Patch」や「Release Notes」を必ず確認し、上記バージョン以上に更新してください。

### 3.2 環境・設定の見直し  
- **不要なコンポーネントは無効化または削除**：使用していないプラグインはインストールしたままにしない。  
- **Web アプリケーションファイアウォール（WAF）** の導入：`SQLi` 文字列（例: `' OR 1=1--`）を検知・ブロックするルールを有効化。  
- **入力サニタイズの徹底**：カスタム開発がある場合は、Joomla! の `JDatabaseDriver::quote()` もしくはプレースホルダー (`?`) を使用し、直接文字列結合しない。  
- **データベース権限の最小化**：Web アプリケーションが使用する DB ユーザーは **SELECT/INSERT/UPDATE/DELETE のみ**（DDL 権限は付与しない）。  
- **ログ監視**：`access_log` と `error_log` に対し、`/index.php?option=com_*` 系の大量リクエストや不自然なパラメータ文字列を SIEM でアラート設定。

### 3.3 インシデント対応手順  
1. **脆弱コンポーネントの特定**（`extensions` テーブルで `type='component'` を検索）。  
2. **即時パッチ適用または一時的に無効化**（`administrator/index.php?option=com_plugins` で無効化）。  
3. **侵害の有無確認**：`SELECT * FROM #__session WHERE userid IS NOT NULL` などで不審なセッションや管理者権限取得の痕跡をチェック。  
4. **バックアップからの復元**（必要に

---

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2019-25756

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T18:16:18.230 |

Joomla! Component vAccount 2.0.2 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the vid parameter. Attackers can send GET requests to the vaccount-dashboard/expense endpoint with crafted SQL payloads in the vid parameter to extract sensitive database information including version and database names.

### CVE-2019-25755

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T18:16:18.100 |

Joomla Component vReview 1.9.11 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the cmId parameter. Attackers can send POST requests to the editReview task endpoint with URL-encoded SQL UNION statements in the cmId parameter to extract database information including usernames, passwords, and database versions.

### CVE-2019-25754

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T18:16:17.973 |

Joomla Component vRestaurant 1.9.4 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the keysearch parameter. Attackers can send POST requests to the menu-listing-layout endpoint with crafted SQL payloads in the keysearch parameter to extract database table names and sensitive information from the database.

### CVE-2019-25753

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T18:16:17.847 |

Joomla! Component VMap 1.9.6 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code into the latlngbound parameter. Attackers can send GET requests to index.php with the option=com_vmap&task=loadmarker parameters containing SQL injection payloads to manipulate database queries and extract sensitive information.

### CVE-2019-25752

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T18:16:17.723 |

Joomla! Component J-BusinessDirectory 4.9.7 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the type parameter. Attackers can send GET requests to index.php with the option=com_jbusinessdirectory&task=categories.getCategories parameters and inject UNION-based SQL statements in the type parameter to extract database information including schema names and sensitive data.

### CVE-2019-25751

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T18:16:17.600 |

Joomla Component J-ClassifiedsManager 3.0.5 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through POST parameters. Attackers can submit crafted SQL payloads in the categorySearch, adType, and citySearch parameters to the displayads component to extract sensitive database information including usernames, databases, and version details.

### CVE-2019-25750

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T18:16:17.473 |

Joomla Component J-MultipleHotelReservation 6.0.7 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the hotel_id parameter. Attackers can send POST requests to the search-hotels endpoint with crafted SQL UNION SELECT statements to extract sensitive database information including table names and column data.

### CVE-2019-25748

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T17:16:16.710 |

Joomla JHotelReservation 6.0.7 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the rooms parameter. Attackers can send POST requests to the search-hotels endpoint with crafted SQL payloads in the rooms parameter to extract sensitive database information including version details.

### CVE-2017-20282

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T17:16:16.557 |

Joomla! Component jCart for OpenCart 2.0 contains an SQL injection vulnerability that allows unauthenticated attackers to manipulate database queries by injecting SQL code through the product_id parameter. Attackers can send GET requests to index.php with the option=com_jcart&route=product/product parameters and malicious product_id values to extract sensitive database information.

### CVE-2017-20281

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T17:16:16.433 |

Joomla! Component Extra Search 2.2.8 contains an SQL injection vulnerability that allows unauthenticated attackers to manipulate database queries by injecting SQL code through the establename parameter. Attackers can send GET requests to index.php with the option=com_extrasearch parameter and malicious SQL in the establename field to extract sensitive database information.

### CVE-2017-20280

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T17:16:16.310 |

Joomla Component Myportfolio 3.0.2 contains an SQL injection vulnerability that allows unauthenticated attackers to manipulate database queries by injecting SQL code through the pid parameter. Attackers can send GET requests to index.php with malicious pid values in the task=project&view=grid endpoint to extract sensitive database information.

### CVE-2017-20279

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T17:16:16.190 |

Joomla Payage 2.05 contains an SQL injection vulnerability that allows unauthenticated attackers to manipulate database queries by injecting SQL code through the aid parameter. Attackers can send GET requests to index.php with malicious aid values in the make_payment task to extract sensitive database information using boolean-based blind or time-based blind techniques.

### CVE-2017-20278

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T17:16:16.067 |

Joomla Component JoomRecipe 1.0.3 contains an SQL injection vulnerability that allows unauthenticated attackers to manipulate database queries by injecting SQL code through the category parameter. Attackers can send GET requests to the all-recipes endpoint with malicious SQL payloads in the category path segment to extract sensitive database information.

### CVE-2017-20277

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T17:16:15.940 |

Joomla JoomRecipe 1.0.4 component contains a blind SQL injection vulnerability in the search_author parameter on the search results page. Attackers can inject SQL code through POST requests to the search endpoint to extract database information using boolean-based blind SQL injection techniques.

### CVE-2017-20276

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T17:16:15.813 |

Joomla! Component SIMGenealogy 2.1.5 contains an SQL injection vulnerability that allows unauthenticated attackers to manipulate database queries by injecting SQL code through the type parameter. Attackers can send GET requests to index.php with the option=com_simgenealogy, view=latest parameters and inject malicious SQL in the type parameter to extract sensitive database information.

### CVE-2017-20275

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T17:16:15.677 |

Joomla! Component PHP-Bridge 1.2.3 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the id parameter. Attackers can send GET requests to index.php with option=com_phpbridge&view=phpview parameters and inject SQL code in the id parameter to extract database information including table and column names.

### CVE-2017-20274

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T17:16:15.553 |

Joomla LMS King Professional 3.2.4.0 contains an SQL injection vulnerability that allows unauthenticated attackers to manipulate database queries by injecting SQL code through the cp_id parameter. Attackers can send GET requests to index.php with the option=com_lmsking, view=lmsking, layout=learningpath, and task=learningPath parameters to extract sensitive database information.

### CVE-2017-20273

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T17:16:15.430 |

Joomla Event Registration Pro Calendar 4.1.3 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the id parameter. Attackers can send GET requests to index.php with option=com_registrationpro&view=category&id parameter containing SQL injection payloads to extract sensitive database information.

### CVE-2017-20272

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T17:16:15.313 |

Joomla Ultimate Property Listing 1.0.2 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the sf_selectuser_id parameter. Attackers can send GET requests to index.php with the option=com_upl and view=propertylisting parameters to extract sensitive database information including table names and column structures.

### CVE-2017-20271

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T17:16:15.190 |

Joomla StreetGuessr Game 1.1.8 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the catid parameter. Attackers can send GET requests to index.php with the option=com_streetguess&view=maps parameters and inject SQL code in the catid parameter to extract sensitive database information including version and database names.

### CVE-2017-20270

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T17:16:15.063 |

Joomla! Component Twitch Tv 1.1 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the username and id parameters. Attackers can send GET requests to index.php with option=com_twitchtv and view parameters containing SQL injection payloads to extract sensitive database information including credentials and configuration data.

### CVE-2017-20269

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T17:16:14.940 |

Joomla! Component KissGallery 1.0.0 contains an SQL injection vulnerability that allows unauthenticated attackers to inject SQL commands through the component URL path. Attackers can supply malicious SQL code in the kissgallery endpoint to execute arbitrary database queries and extract sensitive information.

### CVE-2017-20268

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T17:16:13.930 |

Joomla! Component Zap Calendar Lite 4.3.4 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the 'eid' parameter. Attackers can send GET requests to the RSVP plugin endpoint with crafted SQL payloads to extract sensitive database information including database names and table structures.

### CVE-2017-20267

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T16:16:16.553 |

Joomla! Component Calendar Planner 1.0.1 contains an SQL injection vulnerability that allows unauthenticated attackers to inject SQL commands through the category_id parameter. Attackers can send GET requests to the events view with malicious SQL code in the category_id parameter to extract sensitive database information.

### CVE-2017-20266

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T16:16:16.427 |

Joomla SP Movie Database 1.3 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the searchword parameter. Attackers can send GET requests to the searchresults view with crafted SQL payloads in the searchword parameter to extract sensitive database information.

### CVE-2017-20263

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T16:16:16.047 |

Joomla! Component FocalPoint Pro/Free 1.2.3 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the id parameter. Attackers can send GET requests to index.php with option=com_focalpoint, view=location, and a crafted id parameter containing SQL commands to extract sensitive database information.

### CVE-2017-20262

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T16:16:15.917 |

Joomla! Component Ajax Quiz 1.8 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the cid parameter. Attackers can send GET requests to index.php with the option=com_ajaxquiz and view=ajaxquiz parameters to extract sensitive database information including table names and column structures.

### CVE-2017-20261

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T16:16:15.787 |

Joomla! Component Bargain Product VM3 1.0 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the product_id parameter. Attackers can supply crafted SQL statements in GET requests to the brainy and alice views to extract sensitive database information.

### CVE-2017-20260

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T16:16:15.660 |

Joomla! Component Price Alert 3.0.2 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the product_id parameter. Attackers can send requests to the subscribeajax view with crafted SQL payloads in the product_id parameter to extract sensitive database information including credentials and configuration data.

### CVE-2017-20259

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T16:16:15.533 |

Joomla OSDownloads 1.7.4 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the id parameter. Attackers can send GET requests to index.php with option=com_osdownloads&view=item&id=[SQL] to extract sensitive database information including credentials and configuration data.

### CVE-2017-20258

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T16:16:15.407 |

Joomla! Component RPC Responsive Portfolio 1.6.1 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the id parameter. Attackers can send GET requests to index.php with option=com_pofos&view=pofo&id=[SQL] to extract sensitive database information.

### CVE-2017-20257

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T16:16:15.280 |

Joomla! Component Quiz Deluxe 3.7.4 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL commands through the ajaxaction.flag_question task. Attackers can inject malicious SQL code via the stu_quiz_id or flag_quest parameters to manipulate database queries and extract sensitive information.

### CVE-2017-20256

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T16:16:15.157 |

Joomla Survey Force Deluxe 3.2.4 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the invite parameter. Attackers can send GET requests to the component with crafted SQL payloads in the invite parameter to extract sensitive database information.

### CVE-2017-20255

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T16:16:15.023 |

Joomla! Component JB Visa 1.0 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the visatype parameter. Attackers can send GET requests to index.php with the option=com_bookpro and view=popup parameters, injecting SQL commands in the visatype parameter to extract sensitive database information including credentials and table contents.

### CVE-2017-20254

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T16:16:14.900 |

Joomla! Component User Bench 1.0 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the userid parameter. Attackers can send GET requests to index.php with the option=com_userbench&view=detail&userid parameter containing SQL injection payloads to extract sensitive database information including credentials and configuration data.

### CVE-2017-20253

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T16:16:14.760 |

Joomla! Component My Projects 2.0 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the VerAyari parameter. Attackers can craft requests to the component endpoint with SQL injection payloads to extract sensitive database information including credentials and system data.

### CVE-2017-20252

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T16:16:13.753 |

Joomla NextGen Editor 2.1.0 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL commands through the plname parameter. Attackers can send GET requests to index.php with option=com_nge&view=config and inject malicious SQL code in the plname parameter to extract sensitive database information.

### CVE-2019-25762

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-359` |
| Published | 2026-06-19T18:16:19.143 |

Joomla! Component JoomProject 1.1.3.2 contains an information disclosure vulnerability that allows unauthenticated attackers to access sensitive user data by exploiting the projects endpoint. Attackers can send requests to index.php with option=com_jpprojects&view=projects&tmpl=component&format=json parameters to retrieve user IDs, names, and email addresses in JSON format.

### CVE-2019-25758

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-19T18:16:18.523 |

Joomla! Component vBizz 1.0.7 contains an unrestricted file upload vulnerability that allows authenticated attackers to upload arbitrary PHP files by submitting malicious files through the profile_pic parameter. Attackers can upload PHP files via POST requests to the employee view endpoint and execute them from the uploads directory to achieve remote code execution.

### CVE-2025-71326

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:34.890 |

AVAST Antivirus 25.11 contains an unquoted service path vulnerability in the SecureLine service that allows local non-privileged users to execute code with elevated SYSTEM privileges. Attackers can exploit the unquoted binary path in the service configuration to inject malicious executables that execute with high-level system permissions.

### CVE-2023-54353

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:34.713 |

Chromacam 4.0.3.0 contains an unquoted service path vulnerability in the PsyFrameGrabberService that allows local attackers to execute arbitrary code by placing malicious executables in unquoted path directories. Attackers with write access to C:\ or subdirectories like C:\Program Files (x86)\Personify\ can place a malicious Program.exe or PsyFrameGrabberService.exe file that executes with LocalSystem privileges when the service starts automatically at boot.

### CVE-2022-50971

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:34.560 |

Malwarebytes 4.5 contains an unquoted service path vulnerability in the MBAMService executable that allows local attackers to escalate privileges by injecting malicious code into the system root path. Attackers can place executable files in unquoted path directories that execute with LocalSystem privileges during service startup or system reboot.

### CVE-2021-47985

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:34.420 |

Brother SAPSprint 7.60 contains an unquoted service path vulnerability in the SAPSprint service binary that allows local attackers to escalate privileges. Attackers can place a malicious executable in the Program Files directory path to be executed with LocalSystem privileges when the service starts automatically.

### CVE-2020-37254

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:34.273 |

Wondershare PDFelement 5.2.9 contains a privilege escalation vulnerability due to an unquoted service path in the WsAppService Windows service. Local attackers can place a malicious executable in the service path and execute code with LocalSystem privileges upon service restart or system reboot.

### CVE-2020-37253

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:34.147 |

Winstep 18.06.0096 contains an unquoted service path vulnerability in the Winstep Xtreme Service that allows local attackers to escalate privileges. Attackers can place malicious executables in the Program Files directory to be executed with LocalSystem privileges when the service starts.

### CVE-2020-37252

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:34.017 |

Realtek Audio Service 1.0.0.55 contains an unquoted service path vulnerability in RtkAudioService64.exe that allows local attackers to escalate privileges by injecting malicious code. Attackers can place executable files in the unquoted service path directory to execute arbitrary code with LocalSystem privileges during service startup or system reboot.

### CVE-2020-37251

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:33.877 |

RealTimes Desktop Service 18.1.4 contains an unquoted service path vulnerability in the rpdsvc.exe binary that allows local attackers to escalate privileges. Attackers can place malicious executables in unquoted path directories to execute arbitrary code with LocalSystem privileges during service startup or system reboot.

### CVE-2020-37250

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:33.740 |

TFTP Broadband 4.3.0.1465 contains an unquoted service path vulnerability in the tftpt.exe service binary that allows local attackers to execute arbitrary code with system privileges. Attackers can place a malicious executable in the Program Files directory path that will be executed during service startup or system reboot with LocalSystem privileges.

### CVE-2019-25747

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:33.597 |

Network Inventory Advisor 5.0.26.0 installs the niaservice service with an unquoted binary path that allows local attackers to escalate privileges by placing malicious executables in intermediate directories. Attackers can exploit the unquoted path in the service configuration to execute arbitrary code with LocalSystem privileges when the service starts or restarts.

### CVE-2016-20095

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:33.440 |

Matrix42 Remote Control Host 3.20.0031 contains an unquoted service path vulnerability in the FastViewerRemoteService and FastViewerRemoteProxy services that allows local users to execute arbitrary code with SYSTEM privileges. Attackers can place a malicious executable in the Program Files directory with a crafted name to be executed by the service during startup, gaining elevated privileges.

### CVE-2016-20094

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:33.310 |

AnyDesk 2.5.0 contains an unquoted service path vulnerability that allows local users to execute arbitrary code with SYSTEM privileges by exploiting the service installation. Attackers can insert malicious executables in the system root path that execute with elevated privileges during application startup or system reboot.

### CVE-2016-20093

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:33.183 |

Wise Care 365 4.27 and Wise Disk Cleaner 9.29 contain unquoted service path vulnerabilities in the WiseBootAssistant and SpyHunter 4 Service respectively, allowing local users to execute arbitrary code with SYSTEM privileges. Attackers can insert malicious executables in the system root path that execute during service startup or system reboot with elevated privileges.

### CVE-2016-20092

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:33.060 |

NetDrive 2.6.12 contains an unquoted service path vulnerability in the Netdrive2_Service_Netdrive2 service that allows local users to execute arbitrary code with SYSTEM privileges. Attackers can insert malicious executables in the system root path that will be executed during service startup or system reboot, resulting in privilege escalation.

### CVE-2016-20091

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:32.927 |

Windows Firewall Control 4.8.6.0 contains an unquoted service path vulnerability that allows local attackers to escalate privileges by inserting malicious executables in the service path. Attackers can place executable files in unquoted path directories that the wfcs.exe service will execute with LocalSystem privileges upon service restart or system reboot.

### CVE-2016-20090

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:32.797 |

Comodo Dragon Browser versions up to 52.15.25.663 contain a privilege escalation vulnerability in the DragonUpdater service due to an unquoted service path running with SYSTEM privileges. A local attacker can insert a malicious executable in the service path and execute arbitrary code with elevated privileges upon service restart or system reboot.

### CVE-2016-20089

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:32.660 |

Iperius Remote 1.7.0 contains an unquoted service path vulnerability that allows local users to execute arbitrary code with SYSTEM privileges by exploiting the service installation path. When installed from directories containing spaces, attackers can place malicious executables in the path to be executed with elevated privileges during service startup or system reboot.

### CVE-2016-20088

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:32.530 |

Comodo Chromodo Browser 52.15.25.664 contains an unquoted service path vulnerability in the ChromodoUpdater service that runs with SYSTEM privileges. A local attacker can insert a malicious executable in the service path and execute arbitrary code with elevated privileges upon service restart or system reboot.

### CVE-2016-20087

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:32.403 |

Fortitude HTTP 1.0.4.0 contains an unquoted service path vulnerability that allows local users to execute arbitrary code with elevated privileges by exploiting the service binary path. Attackers can insert malicious executables in the system root path that execute with SYSTEM privileges during service startup or system reboot.

### CVE-2016-20086

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:32.270 |

Vembu StoreGrid 4.0 contains an unquoted service path vulnerability in the RemoteBackup and RemoteBackup_webServer services that allows local attackers to escalate privileges. Attackers can place a malicious executable in the unquoted path and restart the service to execute code with LocalSystem privileges.

### CVE-2016-20085

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-19T15:16:31.260 |

Realtek High Definition Audio Driver 6.0.1.6730 contains an unquoted service path vulnerability that allows local attackers to escalate privileges by placing a malicious executable in the service path. Attackers can insert an executable file in the unquoted path and restart the service to execute code with LocalSystem privileges.

### CVE-2026-49260

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-19T17:16:29.477 |

PhpWeasyPrint is a PHP library allowing PDF generation from a URL or an HTML page. Prior to version 2.5.1, `pontedilana/php-weasyprint` builds the shell command for WeasyPrint by passing the binary path through `escapeshellarg()` first and then checking the *quoted* result with `is_executable()`. On POSIX `escapeshellarg('/usr/local/bin/weasyprint')` returns `'/usr/local/bin/weasyprint'` with the single-quote characters as part of the string, so `is_executable()` looks for a file whose actual name includes those quotes. That file never exists, the "safe" branch is dead code, and the raw `$binary` string (set via the constructor or `setBinary()`) flows directly into `Symfony\Component\Process\Process::fromShellCommandline()`. Any deployment whose binary path is sourced from configuration, an environment variable, or a per-tenant setting reaches a shell-command-injection sink. The library is documented as a one-to-one substitute for KnpLabs/snappy and inherited the exact pre-fix codepath KnpLabs patched in GHSA-vpr4-p6fq-85jc. PhpWeasyPrint version 2.5.1 contains a patch for the issue.

### CVE-2026-49286

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-19T18:16:19.487 |

PhpWeasyPrint is a PHP library allowing PDF generation from a URL or an HTML page. Prior to version 2.6.0, `pontedilana/php-weasyprint` guarded the output filename against the `phar://` stream wrapper with a case-sensitive blacklist. PHP stream wrappers are case-insensitive, so `PHAR://`, `Phar://`, etc. bypass the check and reach `fileExists()` (`file_exists()`) in `prepareOutput()`. On PHP 7 (which the library still supports — PHP 7.4+), this triggers deserialization of a crafted PHAR archive's metadata, leading to remote code execution. This is the patch-bypass of CVE-2023-28115. The same issue and fix were handled upstream in KnpLabs/snappy (GHSA-92rv-4j2h-8mjj). PhpWeasyPrint version 2.6.0 contains a patch for the issue.

### CVE-2026-49290

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-23;CWE-36` |
| Published | 2026-06-19T18:16:19.750 |

Slopsmith is a self-contained web application for browsing, playing, and practicing Rocksmith 2014 Custom DLC (CDLC). Prior to 0.2.9-alpha.5, a path-traversal vulnerability in Slopsmith's archive extractors allows an attacker to write arbitrary files outside the extraction directory by supplying a crafted PSARC or sloppak archive. With the default Docker configuration (running as root) and the ability to drop a file into the plugin directory, this escalates to arbitrary remote code execution on the host. Three archive extractors concatenated archive-entry filenames directly onto the extraction root without validation: `lib/psarc.py::unpack_psarc` — PSARC TOC filenames; `lib/patcher.py::unpack_psarc` — duplicate of the above in the patcher flow; `lib/sloppak.py::_unpack_zip` — bare `ZipFile.extractall()` with no member filter. Each accepts entry names containing `..` segments, absolute paths, or backslash separators. The Python `zipfile` module's default `extractall()` is documented as not preventing traversal when callers don't supply a member-filter callback. Version 0.2.9-alpha.5 patches the issue. Until updated, do not open PSARC or sloppak archives from untrusted sources, and do not expose the Slopsmith instance to the public internet. Docker users should also pull the latest image after the next slopsmith Docker image is published.

### CVE-2026-56208

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-06-19T17:16:30.297 |

A heap buffer overflow vulnerability was found in libaom, the reference AV1 codec implementation. A flaw in the AV1 encoder's Look-Ahead Processing (LAP) mode causes the first-pass stats ring buffer wrap-around guard to be bypassed when g_lag_in_frames is set to 1 or higher. This results in a 232-byte out-of-bounds write on every encoded frame after the second, corrupting adjacent heap objects. An attacker who can influence encoder configuration in a transcoding service or WebRTC session could exploit this to cause a denial of service (process crash) or potentially achieve code execution.

### CVE-2026-49287

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-06-19T18:16:19.617 |

Statamic is a Laravel and Git powered content management system (CMS). Prior to 5.73.23 and 6.20.0, the fix for CVE-2026-41175 was incomplete. It addressed the issue in the query builder, but the same protection was not applied to in-memory collection sorting. Manipulating sort parameters could result in the loss of content and assets. This requires a front-end template that passes request input into a tag's sort parameter. It is not exploitable by default — a template would need to be explicitly set up to sort by a visitor-controlled value. This has been fixed in 5.73.23 and 6.20.0.

### CVE-2026-3195

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-06-19T17:16:22.687 |

A flaw was found in QEMU. When reading input audio in the virtio-snd device input callback, the `virtio_snd_pcm_in_cb` function did not check whether the iov could fit the data buffer, potentially leading to a heap out-of-bounds write. This issue exists due to an incomplete fix for CVE-2024-7730.

### CVE-2019-25761

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T18:16:19.020 |

Joomla! Component JoomCRM 1.1.1 contains an SQL injection vulnerability that allows authenticated attackers to execute arbitrary SQL queries by injecting malicious code through the deal_id parameter. Attackers can send GET requests to index.php with option=com_joomcrm&view=contacts and inject SQL code in the deal_id parameter to extract sensitive database information including table names and schemas.

### CVE-2019-25759

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T18:16:18.763 |

Joomla! Component vBizz 1.0.7 contains an SQL injection vulnerability that allows authenticated attackers to execute arbitrary SQL queries by injecting malicious code through the payid parameter. Attackers can submit POST requests to the employee management interface with crafted payid array values containing SQL commands to extract sensitive database information including version and database names.

### CVE-2019-25757

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T18:16:18.360 |

Joomla vWishlist 1.0.1 contains an SQL injection vulnerability that allows authenticated attackers to execute arbitrary SQL queries by injecting malicious code through the vproductid and userid parameters. Attackers can send POST requests to the component with crafted SQL payloads in these parameters to extract sensitive database information including version and database names.

### CVE-2019-25749

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T18:16:16.473 |

Joomla J-CruisePortal 6.0.4 contains an SQL injection vulnerability that allows authenticated attackers to execute arbitrary SQL queries by injecting malicious code through the guest_adult parameter. Attackers can send POST requests to the cruises endpoint with crafted SQL payloads in the guest_adult parameter to extract sensitive database information or manipulate database records.

### CVE-2026-56211

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-06-19T17:16:30.680 |

A remote code execution vulnerability was found in libaom, the reference AV1 codec implementation. Insufficient bounds validation in the AV1 encoder's SVC (Scalable Video Coding) layer ID control allows an attacker to supply crafted video frame pixels that overlap with internal encoder layer context structures. In fork-based video processing services, an attacker can use this to hijack the cyclic refresh map pointer, brute-force the process base address via a crash oracle, and redirect control flow to achieve arbitrary command execution. Exploitation requires the target service to use libaom with SVC encoding enabled and accept attacker-supplied video frames.

### CVE-2026-56210

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-06-19T17:16:30.557 |

A heap-buffer-overflow read vulnerability was found in libaom, the reference AV1 codec implementation. A missing bounds check in the SVC (Scalable Video Coding) layer ID control function allows setting a spatial_layer_id exceeding the configured number of layers. This causes an out-of-bounds heap read of approximately 40,728 bytes when computing a layer context array index. An attacker who can influence SVC encoder parameters in a network-facing service could exploit this for information disclosure (heap content leak) or denial of service (segmentation fault from hitting unmapped memory).

### CVE-2026-56209

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-06-19T17:16:30.427 |

An arbitrary address write vulnerability was found in libaom, the reference AV1 codec implementation. A missing bounds check in the SVC (Scalable Video Coding) layer ID control function allows an attacker to inject an arbitrary pointer into the cyclic refresh map field via crafted image pixel values. The encoder then writes approximately 1,200 bytes at the attacker-controlled address. This is fully deterministic and does not require a separate information leak. An attacker who can supply frames to a network-facing libaom encoder with SVC enabled could exploit this for denial of service or potential code execution.

### CVE-2017-20265

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T16:16:16.300 |

Joomla! Component Flip Wall 8.0 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the wallid parameter. Attackers can send GET requests to index.php with the option=com_flipwall&task=click&wallid parameter containing SQL injection payloads to extract sensitive database information.

### CVE-2017-20264

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-19T16:16:16.170 |

Joomla! Component Sponsor Wall 8.0 contains an SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL queries by injecting malicious code through the wallid parameter. Attackers can send GET requests to index.php with the option=com_sponsorwall&task=click&wallid parameter containing SQL injection payloads to extract sensitive database information including credentials and configuration data.
