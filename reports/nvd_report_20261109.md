# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-08 15:00 UTC
- **対象期間**: `2026-11-07T15:01:34.000Z` 〜 `2026-11-08T15:00:32.000Z`
- **重要CVE数**: 129 件（Critical 9.0+: 14 件 / High 7.0〜: 115 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVSS 7.0 以上の脆弱性は、**Web アプリケーションフレームワーク／医療情報システム系**（OpenEMR、OpenAM）と **Kubernetes 用ポリシーエンジン（Kyverno）**、**CMS（Craft、SunEditor）**、**画像プロキシ（imgproxy）** に集中しています。  
- 認証バイパスや権限昇格が多く、**未認証でもリモートからコード実行や機密情報取得が可能**になるケースが目立ちます。  
- 多くは **古いメジャーバージョンが長期間サポートされていない** ことが根本原因で、アップストリームのパッチがすでに提供されているにも関わらず、アップデートが遅れている組織がリスクに晒されています。  
- 影響範囲は **医療情報（患者データ、FAX/SMTP 設定）** や **認証トークン、SAML アサーション** など、機密性・完全性が極めて重要な情報が対象です。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・攻撃シナリオ |
|-----|------|----------|------------------------|
| **CVE‑2026‑123551** | 10.0 | OpenAM 14.0.0‑16.1.3 の情報漏洩・認証バイパス | WebSocket の通知チャネルからライブセッショントークンが取得可能。未認証攻撃者がトークンを抜き取り、任意のユーザーとしてログインできる。SAML SP が unsigned アサーションを受け入れる設定がデフォルトで残っている点が根本原因。 |
| **CVE‑2026‑124490** | 9.4 | OpenEMR 8.3.0 未満のパストラバーサル（RCFaxClient） | 認証済みユーザーが `file_path` パラメータを操作し、任意のサーバーファイルを読み書きできる。`sqlconf.php` 取得により DB 資格情報が漏洩し、以降の完全なシステム侵害が可能。 |
| **CVE‑2026‑124440** | 9.4 | Kyverno 1.19.1‑1.19.2 の名前空間横断権限バイパス | URL パスに不正な percent‑escape を付与するだけで、テナントが他名前空間・クラスタスコープのリソースを作成・変更できる。ポリシーエンジンがクラスタ全体のガバナンスを担うため、最悪ケースでクラスタ全体が乗っ取られる。 |
| **CVE‑2026‑124427** | 9.3 | Craft CMS 5.0.0‑5.11.1 の GraphQL 認可バイパス | 匿名 GraphQL クライアントが `prev/next` フィールドを辿ることで、スコープ外のエントリ情報（タイトル・スラッグ・カスタムフィールド）を取得できる。情報漏洩に留まらず、後続の RCE につながる可能性がある。 |
| **CVE‑2026‑124494** | 9.3 | SunEditor < 3.4.0 のストアド XSS | HTML サニタイズロジックの URL 正規化バグにより `javascript&colon;` 形式のスキームが通過。保存型 XSS が永続化し、管理者がエディタを開くたびに任意コードが実行される。 |

> **※ 同一製品（OpenEMR）に複数の高リスク脆弱性が集中しています。** まずは **OpenEMR のバージョンアップ** が最優先です。

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンのアップデート（必須）  
| 製品 | 現行脆弱バージョン | 推奨バージョン | アップデート手順のポイント |
|------|-------------------|----------------|---------------------------|
| **OpenAM** | 14.0.0‑16.1.3 | **≥ 16.1.4** | `yum/apt` で `openam` を更新し、`saml.wantAssertionsSigned=true` を明示的に設定。WebSocket 通知は TLS 終端で保護。 |
| **OpenEMR** | < 8.4.0（特に 8.3.0 未満） | **≥ 8.4.0** | `composer install` 後に `php artisan migrate --force` を実行。`rcfaxclient` と `faxsms` の `file_path` バリデーションが修正済み。 |
| **Kyverno** | 1.19.1‑1.19.2 | **≥ 1.19.2** (最新 1.22.x 推奨) | `kubectl apply -f https://github.com/kyverno/kyverno/releases/download/v1.22.0/install.yaml` で置き換え。`apiCall` ルートの URL エンコードチェックが追加。 |
| **Craft CMS** | 5.0.0‑5.11.1 | **≥ 5.11.2** (最新 5.12.x 推奨) | `composer update craftcms/cms` 後、`.env` の `GRAPHQL_PUBLIC_ACCESS` を `false` に設定し、不要な GraphQL エンドポイントを無効化。 |
| **SunEditor** | < 3.4.0 | **≥ 3.4.0** | `npm install suneditor@^3.4.0` または CDN の最新版に差し替え。`html.clean()` のサニタイズロジックが修正。 |
| **imgproxy** | < 4.0.16 | **≥ 4.0.17** (4.0.18 以上推奨) | Docker イメージ `docker pull darthsim/imgproxy:4.0.18` で更新。`--max-ico-size` フラグでサイズ上限を設定。 |
| **Scriban** | < 7.5.3 | **≥ 7.5.3** | `dotnet add package Scriban --version 7.5.3` で更新。再帰深度制限とメモリガードが有効化。 |
| **Hickory DNS** | < 0.26.2 | **≥ 0.26.2** | `cargo update -p hickory-proto` または OS パッケージで最新版をインストール。NSEC 解析ロジックが修正。 |

### 3.2 設定・運用上の緊急対策  
1. **OpenAM**  
   - `WantAssertionsSigned` を必ず

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-123551

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-08T02:16:46.603 |

OpenAM from 14.0.0 before 16.1.4 contains an information disclosure vulnerability that allows unauthenticated attackers to read live session tokens from the notification WebSocket. Attackers can bypass the agent-only check through an unvalidated internal forward on legacy Liberty ID-FF endpoints, collecting iPlanetDirectoryPro tokens to hijack user and administrator sessions.

### CVE-2026-124490

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-08T14:18:18.667 |

OpenEMR before 8.3.0 contains a path traversal vulnerability in the RingCentral RCFaxClient disposeDocument() method of oe-module-faxsms that allows authenticated attackers to read and write arbitrary files via the file_path parameter. Attackers can use action=download to read credentials and source code, or action=setup with base64 content to write web-executable files for code execution.

### CVE-2026-124469

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-08T14:18:15.130 |

OpenEMR before 8.3.0 contains an SQL injection vulnerability in the Fee Sheet drug-inventory lookup (DrugSalesService::sellDrug) that interpolates the prod[N][warehouse] POST field into an ORDER BY clause. Low-privileged authenticated users can submit Fee Sheet product lines with constant subqueries to run a time-based blind oracle, extracting patient data and users_secure bcrypt hashes.

### CVE-2026-124440

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-08T14:18:10.633 |

Kyverno from 1.19.1 before 1.19.2 contains an authorization bypass vulnerability in the apiCall namespace clamp that allows namespace tenants to issue cross-namespace and cluster-scoped API requests by appending malformed percent-escapes to urlPath. Attackers can create namespaced Policies whose apiCall runs as the admission-controller ServiceAccount to read other namespaces' resources and create mutating webhooks, escalating to cluster admin.

### CVE-2026-124494

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-08T14:18:19.277 |

SunEditor before 3.4.0 contains a stored cross-site scripting vulnerability because the html.clean() sanitizer's _normalizeURL() function decodes named entities like &colon; to an empty string. Attackers can inject href values such as javascript&colon; that pass the _isSafeURL() check but are decoded by browsers, executing JavaScript when victims click stored links.

### CVE-2026-124493

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-08T14:18:19.130 |

SunEditor before 3.4.0 contains a stored cross-site scripting vulnerability in the DocumentType constructor that injects header textContent into innerHTML without HTML escaping. Attackers can store entity-encoded HTML in h1-h6 headers that executes JavaScript when editors using document:header mode initialize, enabling session cookie theft.

### CVE-2026-124463

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-08T14:18:14.167 |

OpenEMR before 8.3.0 contains a stored cross-site scripting vulnerability that allows authenticated users with CAMOS access to inject HTML by saving malicious CAMOS content through ajax_save.php. Attackers can store a script payload that executes unencoded when the entry is printed via the non-print_html branch of rx_print.php, performing actions and reading data as the victim user.

### CVE-2026-124450

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-08T14:18:12.260 |

OpenEMR before 8.3.0 contains a broken access control and path traversal vulnerability in the fax/sms module disposeDocument action via an unvalidated file_path parameter. Authenticated low-privilege users can read sqlconf.php to recover database credentials and write arbitrary files as the web user, enabling remote code execution.

### CVE-2026-124445

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-11-08T14:18:11.487 |

OpenEMR from 7.0.1 before 8.4.0 contains a flaw in src/Common/Auth/OneTimeAuth.php that ignores the enforce_onetime_use and max_access_count flags, never revokes consumed service_auth tokens, and checks login_pin without rate limiting or strict comparison. Attackers holding a captured token can replay it or brute-force the PIN to open patient-portal sessions exposing PHI.

### CVE-2026-124427

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-08T14:18:08.517 |

Craft CMS from 5.0.0 before 5.11.2 contains an authorization bypass vulnerability that allows anonymous GraphQL clients to read out-of-scope section entries via prev/next fields. Attackers can chain next hops from one visible in-scope entry to enumerate entries and read titles, slugs, and custom-field content from withheld sections.

### CVE-2026-123614

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-08T02:16:56.983 |

imgproxy from 4.0.0 before 4.0.16 contains an integer overflow in the ICO loader that allows remote attackers to trigger a heap buffer overflow via a crafted data_size value. Attackers can submit a crafted ICO image whose data_size wraps the allocation in vips/icoload.c, corrupting heap memory to crash the process or achieve code execution.

### CVE-2026-123550

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-08T02:16:46.410 |

OpenAM before 16.1.4 contains an authentication bypass vulnerability in its SAML v2.0 service provider that accepts unsigned assertions on the ECP (PAOS) and HTTP-Artifact bindings when WantAssertionsSigned is false. Unauthenticated remote attackers can submit forged assertions to obtain sessions as any mapped user, including administrators, and hijack single sign-on to dependent applications.

### CVE-2026-123549

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-08T02:16:46.247 |

OpenAM before 16.1.4 fails to enforce the Valid Creation Attributes list during self-registration, allowing anonymous attackers to set restricted attributes including group membership. Attackers can register through the legacy self-service REST endpoint or User Self-Service flow to join administrative groups and gain full administrative control of OpenAM.

### CVE-2026-124438

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-08T14:18:10.320 |

Scriban before 7.5.2 contains an information disclosure and object manipulation vulnerability that allows template authors to access .NET internals of function values through reflection member accessors. Attackers can use array.map to read Target, Method, or ReturnType on imported delegates, exposing and overwriting service properties, captured closure secrets, and assembly paths.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-123587

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-08T02:16:52.637 |

The DNSSEC validation in the Hickory DNS hickory-net crate 0.26.0 before 0.26.2 identifies wraparound NSEC records by comparing the next domain name to an SOA record in the response, accepting that SOA even if it fails validation. Attackers who can supply DNS responses can combine a genuine NSEC record and its RRSIG with a crafted SOA record to forge nonexistence of any RRset.

### CVE-2026-124486

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-08T14:18:18.073 |

OpenEMR before 8.3.0 contains a missing authorization vulnerability in the classic document controller that allows low-privilege authenticated users to recategorize other patients' documents. Attackers can invoke move_action_process to move a document into a patients|demo category, then retrieve it with an empty patient_id to exfiltrate PHI and tamper with charts.

### CVE-2026-124484

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-08T14:18:17.773 |

OpenEMR before 8.4.0 contains a missing authorization vulnerability in portal onsite-document APIs that allows any authenticated core user to access cross-patient documents. Attackers can omit the patientId parameter and supply arbitrary record IDs to list, read, and overwrite other patients' portal documents, signatures, and template data.

### CVE-2026-124483

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-08T14:18:17.617 |

OpenEMR before 8.4.0 contains an incorrect authorization vulnerability because the prescription REST API routes check the patients.med ACL instead of patients.rx and request no specific permission bit, so read-only Medical/History access passes the check. Authenticated staff users can reuse the UI-exposed APICSRFTOKEN to enumerate prescription UUIDs, forge prescriptions for arbitrary patients, and deactivate existing prescriptions tenant-wide.

### CVE-2026-124480

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-08T14:18:17.147 |

OpenEMR before 8.4.0 contains an authorization bypass vulnerability that allows low-privileged authenticated users to read cross-patient FHIR QuestionnaireResponse data by sending the APICSRFTOKEN header. Attackers can reuse the session-exposed api_csrf_token_js value to skip FHIR scope checks and call GET /fhir/QuestionnaireResponse, exfiltrating site-wide questionnaire answer PHI.

### CVE-2026-124477

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-08T14:18:16.653 |

OpenEMR before 8.3.0 contains a missing authorization vulnerability that allows low-privileged authenticated users to delete arbitrary patient recall records via the delete_Recall action. Attackers can send POST requests to /interface/main/messages/save.php with a target pid and r_ID to remove recall data without ACL or ownership checks.

### CVE-2026-124467

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-08T14:18:14.823 |

OpenEMR before 8.4.0 contains a local file inclusion in the ESign router (library/ESign/Router.php), which passes the unsanitized module parameter into a require_once of '<module>/Controller.php', and the fax module's faxProcessUploads writes attacker-named files to a predictable temp path without extension checks. Authenticated attackers can upload a PHP file named Controller.php, then request interface/esign/index.php with a traversing module parameter to include it and execute arbitrary code.

### CVE-2026-124446

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-08T14:18:11.650 |

OpenEMR before 8.3.0 contains a path traversal vulnerability in the FaxSMS module's RCFaxClient and SignalWireClient disposeDocument functions that allows authenticated low-privilege users to read and overwrite arbitrary files via the unsanitized file_path parameter. Attackers can request action=download to retrieve cleartext files like sqlconf.php database credentials and keys, or use action=setup to overwrite web-server-writable files with ciphertext.

### CVE-2026-124441

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-08T14:18:10.800 |

Kyverno before 1.19.2 contains an authorization bypass vulnerability that allows namespaced tenants to generate any resource kind in any namespace by templating the generate rule's kind and namespace with variables. Attackers can create a Policy and trigger ConfigMap in their own namespace, causing the privileged background-controller to write NetworkPolicies or RoleBindings into victim or kube-system namespaces.

### CVE-2026-124439

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-11-08T14:18:10.470 |

Scriban and Scriban.Signed before 7.5.3 contain uncontrolled recursion flaws in which postfix member, indexer, and call chains bypass ExpressionDepthLimit, array comparison lacks depth and cycle checks, and object.eval bypasses RecursiveLimit. Attackers who can supply templates can trigger an uncatchable StackOverflowException that terminates the host process.

### CVE-2026-124437

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-08T14:18:10.163 |

Scriban before 7.5.3 contains a resource exhaustion vulnerability that allows untrusted template authors to exhaust memory and CPU because builtins like math.format, regex.replace and string.escape skip the LimitToString allocation guard. Attackers can submit small templates using huge format precision specifiers, shared-structure array comparison, BigInteger multiplication or exponential function recursion that ignore LoopLimit and CancellationToken, crashing or stalling multi-tenant hosts.

### CVE-2026-124430

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-11-08T14:18:08.990 |

Craft CMS from 5.10.0 before 5.11.2 contains a remote code execution vulnerability that allows non-administrator control panel users to obtain HMAC-signed Twig templates via the app/render-elements endpoint. Attackers can submit the signed templated returnUrl as the login redirect parameter, triggering unsandboxed renderObjectTemplate() evaluation and executing OS commands as the PHP worker.

### CVE-2026-124429

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-08T14:18:08.833 |

Craft CMS from 5.0.0 before 5.11.2 contains a privilege escalation vulnerability that allows unauthenticated public registrants to reclaim deactivated non-admin accounts while retaining their direct permissions. Attackers can register using a deactivated account, set a new password, and inherit permissions stored in userpermissions_users, enabling privileged account takeover when email verification is disabled.

### CVE-2026-123616

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-11-08T02:16:57.307 |

imgproxy from 3.3.0 before 4.0.16 contains an unbounded memory allocation vulnerability in the ICO loader that fails to validate the data_size field. Attackers can supply a crafted 23-byte ICO file declaring a ~4GB data_size to trigger memory exhaustion and worker crashes without authentication.

### CVE-2026-123615

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-08T02:16:57.147 |

imgproxy 3.3.0 before 4.0.17 contains an out-of-bounds heap read and write in the ICO loader's BMP header reconstruction (vips_foreign_load_ico_header in vips/icoload.c) when an ICO entry declares a tiny data size, causing unvalidated header fields to be read and written past the allocated buffer. Unauthenticated remote attackers can supply a crafted ICO image to corrupt adjacent heap chunk metadata, triggering a glibc abort that crashes the worker.

### CVE-2026-123608

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-08T02:16:55.927 |

Hickory DNS hickory-proto from 0.3.1 before 0.26.1 contains a denial of service vulnerability in BinEncoder that allows remote attackers to exhaust CPU through quadratic-time name compression. Attackers can send malicious DNS messages with many records that add many candidate labels and trigger repeated linear scans during encoding, amplifying CPU exhaustion.

### CVE-2026-123607

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-08T02:16:55.747 |

Hickory DNS hickory-proto 0.25.0-alpha.3 through 0.25.2 and hickory-net before 0.26.1 contain an unbounded loop vulnerability in DnssecDnsHandle NSEC3 closest-encloser proof validation when the SOA owner is not an ancestor of the QNAME. Upstream attackers can return NoData or NXDomain responses with a cross-zone SOA record to panic debug builds or exhaust memory in release builds.

### CVE-2026-123606

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-08T02:16:55.583 |

The hickory-dns recursor in hickory-recursor 0.25.0-alpha.3 through 0.25.2 and hickory-resolver 0.26.0-alpha.1 before 0.26.2 iterates every out-of-bailiwick NS target lacking glue in a referral without any per-query work budget. Remote attackers can serve such referrals to force A and AAAA lookups per target, amplifying traffic against remote servers or exhausting recursor resources.

### CVE-2026-123605

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-08T02:16:55.423 |

Hickory DNS hickory-proto 0.1 through 0.25.0-alpha.3 and hickory-net before 0.26.2 contain a DNSSEC validation bypass because the validator verifies an RRSIG against the DNSKEY of whatever name appears in its Signer's Name field without checking that this name is the zone containing the RRset. Attackers controlling any secure zone can produce valid signatures over arbitrary records in unrelated zones, which resolvers, recursors, and clients using DnssecDnsHandle accept as authenticated.

### CVE-2026-123604

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-08T02:16:55.273 |

Hickory DNS hickory-resolver 0.26.0-beta.1 before 0.26.2 contains an unbounded retry loop in NameServerPool::try_send, which re-queues truncated (TC) responses without checking the answering transport or counting iterations. A malicious authoritative server returning TC=1 on every transport keeps the resolver spinning on a persistent TCP connection until the 5-second request deadline expires, causing resource exhaustion.

### CVE-2026-123596

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-11-08T02:16:54.020 |

Hickory DNS hickory-proto through 0.26.0-alpha.1 and hickory-net 0.26.0-beta.1 before 0.26.2 contain a DNSSEC validation flaw in the validating recursor's NSEC handler that accepts parent-side ancestor-delegation NSEC records as proof of nonexistence for names below the zone cut. An on-path attacker, rogue parent nameserver, or attacker winning a port and TXID race can deliver one forged NXDOMAIN response built from genuinely signed parent NSEC records, causing authenticated denial of existing child-zone names cached for the negative TTL.

### CVE-2026-123595

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-11-08T02:16:53.863 |

Hickory DNS hickory-proto 0.25 through 0.26.0-alpha.1 and hickory-net 0.26.0-beta.1 before 0.26.2 contain a DNSSEC validation flaw in the validating recursor's NSEC3 handler, which matches the closest encloser by hash alone without checking the type bitmap and so accepts parent-side ancestor-delegation NSEC3 records as proof of nonexistence. An attacker who delivers one response built from genuinely signed parent NSEC3 records can cause NXDOMAIN or NODATA to be cached with AD=1, denying resolution of existing names at and below the zone cut.

### CVE-2026-123588

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-11-08T02:16:52.790 |

The recursive resolver in Hickory DNS (all versions of the hickory-recursor crate, and hickory-resolver 0.26.0 before 0.26.2) caches an empty connection pool when it follows a referral with no glue records and all queries for the name servers' IP addresses fail. An attacker able to spoof DNS responses can make these lookups fail, causing all subsequent queries for the affected zone to fail until the cache entry expires or is evicted.

### CVE-2026-123586

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-08T02:16:52.477 |

Hickory DNS 0.25.0-alpha.3 through 0.25.2 contains a query amplification vulnerability in its recursive resolver, which mishandles cyclic sibling name server referrals that lack glue records. Attackers controlling two zones whose name servers reference each other without glue records can make the recursor loop, sending many upstream queries, amplified further by zero-TTL NS records.

### CVE-2026-123580

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-08T02:16:51.540 |

Hickory DNS hickory-net 0.26.0-beta.1 before 0.26.2 and hickory-proto through 0.26.0-alpha.1 perform insufficient checks on NSEC3 record names during DNSSEC verification, comparing only the hashed label without confirming the record belongs to the correct zone. Attackers can supply NSEC3 records from another zone with a matching hash label to forge DNSSEC nonexistence proofs.

### CVE-2026-123577

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-08T02:16:51.050 |

Hickory DNS from 0.24.0 before 0.26.2 contains a resource exhaustion vulnerability that allows remote attackers to consume server memory via unbounded DoH request bodies. Attackers can send large request bodies over HTTP/2 or HTTP/3 to a DNS over HTTP server, causing memory exhaustion and denial of service.

### CVE-2026-123576

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-08T02:16:50.780 |

Hickory DNS 0.24.0 through 0.26.1 contains a memory exhaustion vulnerability that allows remote attackers to consume server resources by sending incomplete DNS-over-QUIC request bodies. Attackers can open many connections and send only large length prefixes, causing pre-allocated buffers to persist without timeout and exhausting server memory.

### CVE-2026-123575

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-08T02:16:50.600 |

Hickory DNS before 0.26.2 contains a resource exhaustion vulnerability in its DNS-over-HTTPS HTTP/2 server that lacks sufficient timeouts or limits for incomplete request bodies. Remote attackers can open DoH connections, send incomplete request bodies, and hold connections open to exhaust server memory.

### CVE-2026-123574

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-08T02:16:50.450 |

The zone file parser in the hickory-proto crate of Hickory DNS 0.24.0 before 0.26.2 panics when a single token in a zone file is 4096 bytes or longer. Attackers who can supply untrusted zone files to an application using the parser can trigger the panic to cause a denial of service.

### CVE-2026-123573

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-08T02:16:50.297 |

hickory-dns from 0.20.1 before 0.26.2 contains a denial of service vulnerability in the hickory-proto SVCB and HTTPS record presentation format parser. Attackers can supply untrusted zone files where only a single or double quote replaces a service parameter value, triggering a panic that crashes the parsing process.

### CVE-2026-123572

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1286` |
| Published | 2026-11-08T02:16:50.140 |

Hickory-dns from 0.20.1 before 0.26.2 contains a denial of service vulnerability in the hickory-proto SVCB and HTTPS record presentation format parser, which panics on malformed alpn values. Attackers can supply untrusted zone files with unbalanced quotes, consecutive commas, or invalid escapes in alpn parameters to crash parsing processes.

### CVE-2026-123571

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-08T02:16:49.990 |

Hickory DNS from 0.26.0 before 0.26.2 contains an integer underflow vulnerability in TSIG RDATA decoding that allows remote attackers to trigger a panic via malformed records. Attackers can send a crafted TSIG record in DNS wire format to cause unchecked subtraction underflow, crashing builds with overflow checks enabled and causing denial of service.

### CVE-2026-123570

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-08T02:16:49.830 |

The DNS wire-format message parser in hickory-proto (Hickory DNS) 0.18 before 0.26.2 preallocates record vectors sized by the untrusted ANCOUNT, NSCOUNT, and ARCOUNT header fields before reading record data. Remote attackers can send a UDP datagram, or a spoofed response to a client/resolver, with these counts set to 65535, forcing about 18MB of allocation per message.

### CVE-2026-123569

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-08T02:16:49.673 |

The devalue package for npm before 5.6.3 can consume excessive CPU and memory when serializing sparse arrays with uneval or stringify. An attacker who manages to get a sparse array created on the server, which mainstream wire formats do not allow, and serialized there can cause a denial of service.

### CVE-2026-123566

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-08T02:16:49.197 |

Sveltejs devalue before 5.9.3 contains a denial of service vulnerability that allows attackers to cause CPU amplification by supplying sparse arrays to uneval. Attackers who influence sparse values passed to uneval can force synchronous work proportional to the declared array length, blocking the event loop.

### CVE-2026-123565

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-08T02:16:49.040 |

Sveltejs devalue before 5.9.3 contains a resource exhaustion vulnerability where repeated primitive strings cause quadratic expansion in the uneval function. Attackers can supply a small crafted payload that is parsed and then passed to uneval, producing a very large serialized string that exhausts memory or CPU.

### CVE-2026-123564

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-08T02:16:48.877 |

Sveltejs devalue from 1.0.0 before 5.9.3 contains a memory exhaustion flaw in uneval, whose generated code for sparse arrays allocates memory proportional to the array's declared length when evaluated. Attackers who can influence a very large sparse array serialized by an application can exhaust memory in the browser or runtime evaluating the output.

### CVE-2026-123563

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-11-08T02:16:48.720 |

Devalue before 5.9.3 contains a validation bypass vulnerability that allows custom ArrayBuffer revivers to skip typed-array allocation checks in the parse function. Attackers can supply very small crafted input processed by a malformed ArrayBuffer reviver to allocate massive ArrayBuffers, causing memory exhaustion and denial of service.

### CVE-2026-123562

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-08T02:16:48.567 |

devalue (sveltejs/devalue) 5.8.0 before 5.9.3 contains an unhandled promise rejection in stringifyAsync: when serializing multiple promises, a later promise rejecting before an earlier one settles leaves an internal rejection unhandled, even if the caller catches the returned promise. An attacker able to influence the timing or failure of serialized asynchronous values can terminate the Node.js process.

### CVE-2026-123560

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-459` |
| Published | 2026-11-08T02:16:48.227 |

Zebra before 7.0.0 contains an incomplete cleanup vulnerability that allows unauthenticated peers to stall initial sync by serving a forged checkpoint block body. Attackers can supply a body with forged authorizing data near the final checkpoint, leaving rejected hashes in the sent-hash set so the node stops requesting blocks until restart.

### CVE-2026-123559

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-08T02:16:48.047 |

Zebra before 7.0.0 contains an inefficient algorithmic complexity vulnerability that allows unauthenticated peers to exhaust verification threads by submitting transactions with many transparent inputs. Attackers can relay invalid transactions with tens of thousands of inputs, forcing quadratic ZIP-244 or ZIP-243 digest recomputation that stalls Rayon-backed block verification for minutes.

### CVE-2026-123558

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-460` |
| Published | 2026-11-08T02:16:47.863 |

Zebra zebrad before 7.0.0 contains a denial of service vulnerability that allows a malicious peer to stall checkpoint sync by cancelling the verifier rewind after a failed commit. Attackers can serve a forged block with altered authorizing data plus a restart-triggering block, leaving the verifier rejecting honest blocks until restart.

### CVE-2026-123555

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-755` |
| Published | 2026-11-08T02:16:47.313 |

Zebra from 2.3.0 before 7.0.0 contains a denial of service vulnerability that allows unauthenticated peers to evade misbehavior scoring by sending transactions or blocks with invalid transparent scripts. Attackers can flood mempool with script-failing transactions or serve forged v5 block bodies with altered scriptSig bytes to exhaust CPU and repeatedly stall block sync.

### CVE-2026-123554

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-08T02:16:47.120 |

Zebra zebrad 6.4.0 before 7.0.0 performs quadratic work in the mempool coinbase-maturity check because Transaction::coinbase_spend_restriction() rebuilds the transaction's output list once per spent outpoint. Any connected peer can repeatedly send unsigned transactions with many transparent inputs and outputs, which are rejected without a misbehavior score, to pin verification threads.

### CVE-2026-123543

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-08T02:16:45.253 |

OpenAM before 16.1.4 contains a denial of service vulnerability that allows unauthenticated attackers to exhaust server resources by sending serialized Java data without size or structure limits. Attackers can send small crafted requests to remote SDK endpoints, classic login pages, or the administration console to block authentication, session validation and policy decisions.

### CVE-2026-123531

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-08T02:16:43.190 |

Vikunja from 1.0.0 before 2.7.1 contains an uncontrolled resource consumption vulnerability that allows authenticated users to bypass service.maxitemsperpage by sending page=0 to /api/v1 list endpoints. Attackers can self-register and repeatedly request page=0 to force unbounded SQL queries, memory materialisation, and per-row query fan-out, degrading availability for other users.

### CVE-2026-124488

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-08T14:18:18.370 |

OpenEMR before 8.3.0 contains an authorization bypass vulnerability that allows authenticated clinicians lacking high-sensitivity permission to read and modify encounter-bound forms via load_form.php. Attackers can request the Clinical Notes or Care Plan direct loader to obtain restricted content and a CSRF token, then submit save.php to tamper with clinical records.

### CVE-2026-124472

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-08T14:18:15.610 |

OpenEMR before 8.3.0 contains a missing authorization vulnerability in interface/billing/sl_eob_patient_note.php that allows any authenticated user to read and modify patient billing notes. Attackers with low-privilege accounts can enumerate the patient_id parameter and submit POST requests using the embedded CSRF token to view or tamper with confidential billing data.

### CVE-2026-124471

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:15.447 |

OpenEMR before 8.3.0 contains a missing authorization vulnerability in interface/billing/sl_eob_invoice.php that allows any authenticated user to read and modify billing data for any encounter. Attackers can iterate the id parameter to read patient names and billing notes, and post payments, adjustments, deletions, or billing notes against any patient's account.

### CVE-2026-124461

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-08T14:18:13.853 |

OpenEMR before 8.3.0 contains a missing authorization vulnerability in library/ajax/upload.php that allows any authenticated user to read and overwrite document data by supplying an arbitrary doc_id. Low-privilege users can enumerate doc_id values with the fetch and save actions to disclose patient health information and tamper with medical records across all patients.

### CVE-2026-124459

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:13.550 |

OpenEMR before 8.3.0 contains an insecure direct object reference vulnerability in many encounter-form view and save endpoints that lack patient/encounter ownership checks. Authenticated clinical users can enumerate sequential form id values in requests such as soap/view.php and save.php to read and overwrite other patients' clinical records.

### CVE-2026-124448

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-08T14:18:11.960 |

OpenEMR before 8.3.0 contains a stored cross-site scripting vulnerability in the CCDA/CCD preview stylesheets, where cda.xsl copies event-handler attributes whose values evade a character denylist and ccd.xsl copies table-cell attributes unsanitized into preview HTML. Authenticated users can upload a crafted CCDA/CCD document with onmouseover, onclick, or onfocus handlers to execute script in a clinician's session when previewed.

### CVE-2026-124447

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:11.803 |

OpenEMR before 8.3.0 contains an insecure direct object reference vulnerability in OnsitePortalActivityController::Update() that checks the request's patientId instead of the stored record's owner. Authenticated portal patients can send PUT requests to the onsiteportalactivity API with another patient's activity id and their own patientId to disclose tableArgs and checksum data, overwrite narratives and status, and take ownership of the record.

### CVE-2026-124436

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-08T14:18:10.000 |

OpenRemote before 1.32.2 contains an improper authorization vulnerability that allows realm administrators to access and modify global resources by calling admin endpoints lacking super administrator checks. Attackers can change the global keycloakUrl via /configuration/manager to redirect other realms' console authentication for credential phishing, inject CSS, replace map tiles, and delete logs.

### CVE-2026-114713

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-140` |
| Published | 2026-11-08T03:16:33.410 |

The labeled-response module in UnrealIRCd 6.0.0 before 6.2.7.1 does not escape the IRCv3 "label" message tag when echoing it into replies, which allows any user on a network with two or more linked servers to inject server-to-server commands that are executed with server authority.

### CVE-2026-124318

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-07T15:17:16.270 |

Treeio through 2.0 contains an insecure deserialization vulnerability in UpdateRecord.get_format_strings and ModuleSetting.loads that allows staff users to execute code via unverified pickle data. Attackers can store a crafted base64 pickle payload in an UpdateRecord format_strings field through the Django admin, executing Python code as the web server user when news feeds render.

### CVE-2026-124060

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-11-07T21:17:00.150 |

A vulnerability was detected in TOTOLINK CA300-PoE 6.2c.884. Affected by this issue is the function UploadCustomModule of the file /cgi-bin/cstecgi.cgi. The manipulation of the argument File results in buffer overflow. The attack may be launched remotely. The exploit is now public and may be used.

### CVE-2026-124059

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-11-07T19:17:28.480 |

A security vulnerability has been detected in TOTOLINK CA300-PoE 6.2c.884. Affected by this vulnerability is the function setWiFiWdsAddConfig of the file /cgi-bin/cstecgi.cgi. The manipulation of the argument ApCliKeyStr leads to buffer overflow. The attack may be initiated remotely. The exploit has been disclosed publicly and may be used.

### CVE-2026-124058

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-11-07T19:17:28.263 |

A weakness has been identified in TOTOLINK CA300-PoE 6.2c.884. Affected is the function setWiFiRepeaterConfig of the file /cgi-bin/cstecgi.cgi. Executing a manipulation of the argument ApCliKeyStr can lead to buffer overflow. The attack can be launched remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-124057

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-11-07T18:17:21.607 |

A security flaw has been discovered in TOTOLINK CA300-PoE 6.2c.884. This impacts the function setWiFiMultipleConfig of the file /cgi-bin/cstecgi.cgi. Performing a manipulation of the argument Key1Str1 results in buffer overflow. The attack can be initiated remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-123512

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-11-08T02:16:39.847 |

Vikunja before 2.7.1 embeds live password-reset, email-confirmation and account-deletion tokens in the URL query string of emailed links, so the full request URI, including the token, is written to Vikunja's HTTP access log and any reverse-proxy logs when a user clicks the link. Attackers with read access to those logs can replay an unredeemed password-reset token to take over the account or an account-deletion token to confirm the deletion.

### CVE-2026-124492

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-08T14:18:18.980 |

SunEditor before 3.4.0 contains a stored cross-site scripting vulnerability in ModalAnchorEditor's #createBookmarkList, which inserts entity-decoded h1-h6 header textContent into the bookmark list via innerHTML without escaping. Attackers can store HTML-encoded payloads in editor headers that execute JavaScript when a victim opens the link modal and types # in the URL input.

### CVE-2026-123601

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-480` |
| Published | 2026-11-08T02:16:54.797 |

Hickory DNS hickory-proto 0.25.0 through 0.26.0-alpha.1 and hickory-net 0.26.0-beta.1 before 0.26.2 invert the relational operators in the wrap-around branch of find_covering_record() in nsec3.rs, so the last NSEC3 record in a zone's hash ring covers every hash except its owner. Attackers able to inject DNS responses can replay that NSEC3 record and its RRSIG to forge DNSSEC-validated negative responses denying legitimate names.

### CVE-2026-123534

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-08T02:16:43.727 |

Tornado before 6.6 contains a path traversal vulnerability in RequestHandler.static_url() and get_version() that allows attackers to hash files outside static_path using ../ sequences. Attackers controlling input passed to static_url() can obtain SHA-512 hashes of readable files to confirm their existence, or reference /dev/zero to block the event loop indefinitely.

### CVE-2026-123602

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-672` |
| Published | 2026-11-08T02:16:54.960 |

The Hickory DNS recursor in all versions of hickory-recursor and in hickory-resolver 0.26.0-beta.1 before 0.26.2 (recursor feature) is vulnerable to ghost domain names attacks because it reuses child-side apex NS RRsets cached from zone NS queries for iterative resolution. By repeatedly querying a zone's NS records, an attacker keeps the stale RRset cached indefinitely, letting name servers whose delegation the parent revoked keep answering for the zone.

### CVE-2026-123592

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1025` |
| Published | 2026-11-08T02:16:53.413 |

The hickory-net crate in Hickory DNS 0.26.0-beta.1 before 0.26.2 allows DNSSEC validation bypass because Name's Hash ignores label lengths and ValidationCacheKey compares only that hash. An attacker controlling an unsigned delegation whose name differs from a signed target only in dot positions can prime an Insecure verdict, causing forged answers for the target to skip signature verification instead of returning SERVFAIL.

### CVE-2026-123591

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-11-08T02:16:53.253 |

Hickory DNS hickory-net 0.26.0-beta.1 before 0.26.2 and hickory-proto through 0.26.0-alpha.1 fail to verify, per RFC 6840 §4.4, that an NSEC or NSEC3 record denying a DS RRset also proves the delegation's NS record exists. Attackers can reuse child-side NSEC or NSEC3 records to fake an insecure delegation and forge child-zone records.

### CVE-2026-123584

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-696` |
| Published | 2026-11-08T02:16:52.160 |

The hickory-net crate in Hickory DNS 0.26.0 before 0.26.2 stops listening and returns an error when a client UDP connection receives a datagram that cannot be parsed as a DNS message. Remote attackers who guess the query's source port, without knowing the transaction ID, can spoof malformed responses to abort client queries, causing denial of service.

### CVE-2026-123557

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-11-08T02:16:47.687 |

ZcashFoundation Zebra zebrad before 7.0.0 contains a reachable assertion race condition that allows unauthenticated remote peers to abort the node by triggering disconnection during a blocked outbound send. Malicious peers can return empty FindBlocks or FindHeaders replies and stop reading their socket, dropping an unresolved MustUseClientResponseSender and terminating syncing nodes.

### CVE-2026-123542

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-358` |
| Published | 2026-11-08T02:16:45.100 |

OpenAM before 16.1.4 fails to enforce PKCE in the OAuth 2.0 device authorization flow, never validating the code verifier when device codes are exchanged for tokens. Attackers who obtain an approved device code from client logs or shared device storage can redeem it for access and ID tokens to impersonate the user.

### CVE-2026-123528

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-11-08T02:16:42.657 |

Vikunja before 2.7.1 contains an insufficient session expiration vulnerability that allows holders of revoked access tokens to keep authenticating because SetupTokenMiddleware skips session and account-status checks. Attackers with a stolen token can, after logout, password reset, or account disabling, mint OAuth sessions via /oauth/authorize or tk_ API tokens for persistent access.

### CVE-2026-123513

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-08T02:16:40.013 |

Vikunja before 2.7.1 contains a credential exposure vulnerability that allows attackers to steal stored auth tokens by inducing users to switch the frontend API URL. Because checkAndSetApiUrl leaves origin-independent localStorage tokens in place, the bearer token and desktop OAuth refresh token are sent to the attacker's server, enabling account takeover.

### CVE-2026-123497

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-11-08T02:16:37.160 |

Vikunja veans before 2.7.1 contains a protocol downgrade vulnerability in serverCandidates that allows on-path attackers to force plain HTTP during veans init and login. Attackers can block HTTPS ports so discovery accepts an unverified HTTP response, capturing passwords, TOTP codes or bot tokens and persisting cleartext API traffic.

### CVE-2026-123538

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-08T02:16:44.460 |

OpenAM before 16.1.4 does not verify that a signed SAML 1.x assertion or response was signed by the partner named as its issuer, accepting a signature from any certificate in OpenAM's keystore. An attacker holding such a private key, such as a trusted SAML 1.x partner, can forge assertions claiming another partner's issuer and sign in as that partner's users, including privileged ones.

### CVE-2026-124457

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-08T14:18:13.240 |

OpenEMR before 8.3.0 contains a path traversal vulnerability in interface/billing/sl_eob_process.php that allows authenticated users to write and read files by supplying unsanitized eraname values. Attackers without billing privileges can inject ../ sequences to create ERA report .html files anywhere the web user can write and parse arbitrary .edi files echoed into the report.

### CVE-2026-120531

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T22:16:36.090 |

The Subscribe2 – Form, Email Subscribers & Newsletters plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the ‘data[ip]’ parameter in all versions up to, and including, 10.47 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-124489

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:18.520 |

OpenEMR before 8.3.0 contains a broken access control vulnerability in portal/portal_payment.php that allows low-privilege authenticated users to bypass billing ACL checks by tampering patient identifiers. Attackers can modify the pid and form_pid parameters to view payment pages and record fraudulent payment receipts for arbitrary patients, corrupting billing records.

### CVE-2026-124487

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-08T14:18:18.223 |

OpenEMR before 8.4.0 contains an improper authorization vulnerability in the non-patient POST /fhir/DocumentReference/$docref route that allows low-privileged users to generate any patient's CCDA. Attackers with only demographics and documents permissions can supply a victim patient parameter, then download the full-chart CCDA from Patient Documents to exfiltrate clinical data.

### CVE-2026-124485

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:17.927 |

OpenEMR before 8.3.0 contains an authorization bypass vulnerability in the patient portal onsitedocuments API that allows authenticated patients to read other patients' documents by overriding query criteria. Attackers can send empty pid_Equals and denialReason_IsNotLike parameters to remove patient scoping and locked filters, exposing consent bodies, signatures, file paths, and template data.

### CVE-2026-124482

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:17.457 |

OpenEMR before 8.4.0 contains an authorization bypass allowing low-privileged SMART standalone-launch users to bind arbitrary patient UUIDs into the OAuth token context. Attackers with only the patients|demo ACL can select a victim during authorization and read that patient's clinical notes and documents through patient-scoped DocumentReference and Binary FHIR endpoints.

### CVE-2026-124481

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:17.300 |

OpenEMR before 8.4.0 contains an improper authorization vulnerability in Rainforest patient portal payments that trusts browser-supplied patientId, encounter, and amount values instead of deriving them from the portal session. Authenticated portal patients can tamper with JSON sent to portal_payment.rainforest.php so the payin.authorized webhook writes forged ar_activity credits to other patients' encounters exceeding the amount actually paid.

### CVE-2026-124479

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-08T14:18:17.000 |

OpenEMR before 8.4.0 contains an arbitrary local file read vulnerability in REST document download, where the controller passes stored uploaded document bytes to Symfony's BinaryFileResponse as a filesystem path instead of returning them as content. Authenticated users with document upload and download access can upload a document containing an absolute pathname, such as the sqlconf.php location, then download it to read server files and recover database credentials.

### CVE-2026-124478

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-08T14:18:16.843 |

OpenEMR before 8.3.0 contains a missing authorization vulnerability in the addRecall action of /interface/main/messages/save.php that allows low-privileged authenticated users to modify arbitrary patients' recall data. Attackers can submit a crafted new_pid with recall, contact, provider, facility, and notification preference fields to overwrite records of patients they cannot access.

### CVE-2026-124476

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:16.463 |

OpenEMR before 8.3.0 contains an insecure direct object reference in portal/lib/paylib.php, which writes the request-supplied form_pid (or the patient_id_cc value in Sphere data) to onsite_portal_activity without checking it against the session patient. Authenticated portal patients can submit portal-save, review-save, AuthorizeNet, Stripe, or Sphere requests to insert or modify forged payment-audit records in other patients' billing records.

### CVE-2026-124475

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:16.320 |

OpenEMR before 8.3.0 contains an insecure direct object reference vulnerability in portal/lib/persist.php that allows authenticated portal patients to modify other patients' settings by supplying an arbitrary setting_patient value. Attackers can insert or overwrite patient_settings rows for victims to suppress notifications, tamper with consent flags, or alter portal preferences.

### CVE-2026-124473

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:16.017 |

OpenEMR before 8.3.0 contains a broken object-level authorization vulnerability in the SOAP note update API, which does not verify that the supplied SOAP note ID (sid) belongs to the supplied patient and encounter. Authenticated users with encounters/notes permission can send PUT requests to /api/patient/:pid/encounter/:eid/soap_note/:sid with another patient's sid to overwrite that clinical note and reassign its pid.

### CVE-2026-124470

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:15.287 |

OpenEMR before 8.3.0 contains a broken object level authorization vulnerability in portal/report/portal_custom_report.php that allows authenticated portal patients to read other patients' problem list entries. Attackers can enumerate sequential IDs in issue_ parameter names to retrieve other patients' problem titles, clinical notes, ICD diagnosis codes, and IPPF contraceptive records.

### CVE-2026-124468

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-08T14:18:14.977 |

OpenEMR before 8.3.0 contains an SQL injection vulnerability in the Standard REST API patient insurance and employer search, which concatenates query-string parameter names into SQL as column identifiers without escaping. Authenticated clients, including low-privilege patient-portal OAuth2 tokens, can send crafted parameter names to /api/patient/{puuid}/insurance or /api/patient/{puuid}/employer to extract patient PHI, user records, and API client secrets.

### CVE-2026-124465

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-11-08T14:18:14.470 |

Trendyol kafka-konsumer from 2.3.3 before 2.6.18 contains a denial of service vulnerability in batch_consumer.go that panics when a single record exceeds MessageGroupByteSizeLimit. Attackers able to produce to the consumed topic can publish one oversized record that terminates the consumer before offset commit, causing a persistent crash loop.

### CVE-2026-124464

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:14.320 |

OpenEMR before 8.4.0 contains an authorization bypass vulnerability that allows patient-scoped SMART tokens to read other patients' questionnaire responses because FhirQuestionnaireResponseService does not implement IPatientCompartmentResourceService. Attackers holding a patient/QuestionnaireResponse.rs token can request responses by uuid or list the unfiltered bundle to obtain cross-patient clinical assessment answers.

### CVE-2026-124462

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:14.010 |

OpenEMR before 8.3.0 contains an insecure direct object reference vulnerability in OnsiteDocumentController::Query() that allows authenticated portal patients to bypass the lowercase pid authorization guard by supplying a capitalised Pid parameter. Attackers can request the api/onsitedocuments endpoint with Pid set to another patient's id to overwrite the session-pinned criteria and read other patients' onsite documents containing PHI.

### CVE-2026-124460

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:13.707 |

OpenEMR before 8.3.0 contains an insecure direct object reference vulnerability in PortalPatientController::Read() that allows authenticated patients to read other patients' pending demographic change requests. Attackers can supply another patient's ID in the patientId query string parameter to retrieve PHI including names, addresses, SSNs, and insurance information.

### CVE-2026-124458

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-08T14:18:13.390 |

OpenEMR before 8.4.0 contains an authorization bypass vulnerability in the FHIR GET /fhir/Person/:uuid route that allows patient-portal users to read any staff member's demographics by bypassing compartment enforcement. Attackers holding a patient SMART token with patient/Person.read can harvest staff Person UUIDs from Appointment references to retrieve names, home addresses, phone numbers, and personal emails.

### CVE-2026-124456

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-08T14:18:13.090 |

OpenEMR before 8.3.0 contains missing authorization and insecure direct object reference vulnerabilities in the oe-module-prior-authorizations module that allow authenticated low-privilege users to access and modify other patients' records. Attackers can request public/reports/list_report.php to view all patients' names, MRNs, insurance and prior-auth data, or submit arbitrary id values to public/index.php to overwrite other patients' prior-authorization records.

### CVE-2026-124455

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:12.943 |

OpenEMR before 8.3.0 contains an insecure direct object reference vulnerability in OnsiteDocumentController::Query() that allows authenticated portal patients to read other patients' documents by overriding Pid_Equals criteria. Attackers can supply Pid_Equals, Pid_GreaterThan, or Pid_In request parameters to the onsitedocuments API to retrieve signed consent forms, signatures, and PHI of any patient.

### CVE-2026-124453

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:12.790 |

OpenEMR before 8.3.0 contains an insecure direct object reference vulnerability in portal/lib/persist.php that allows authenticated portal patients to write settings for other patients. Attackers can modify the setting_patient parameter in a JSON POST request to another patient's PID, altering that patient's portal settings such as the portal theme.

### CVE-2026-124449

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T14:18:12.110 |

OpenEMR before 8.4.0 contains a missing authorization vulnerability in FHIR Media/:uuid and QuestionnaireResponse read routes that skip ACL checks. Non-patient API tokens lacking OpenEMR ACLs can request resources by uuid, bypassing compartment filtering to read any patient's documents and questionnaire responses.

### CVE-2026-124444

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-08T14:18:11.310 |

OpenEMR before 8.4.0 contains a mass assignment vulnerability in the patient portal OnsiteDocument query API that lets request parameters set bitwise criteria filters whose values are placed unquoted into the SQL WHERE clause. Authenticated patient portal users can inject SQL via parameters such as Id_BitwiseAnd to read any database table, including other patients' records and staff password hashes.

### CVE-2026-124442

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-08T14:18:10.957 |

AzuraCast before 0.24.0 contains a server-side request forgery vulnerability that allows users with station WebHooks permission to bypass the UserUrlFilter SSRF guard through HTTP redirects. Attackers can configure Mastodon, Telegram, GroupMe, or RadioReg webhooks pointing to a redirecting URL, causing the Guzzle client to reach internal services and expose responses via test logs.

### CVE-2026-124434

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-08T14:18:09.663 |

Grav Lightbox Gallery plugin 1.1.0 before 1.3.2 on Grav 2.x calls any medium method named in image, thumb or thumb_options shortcode values without core's allowed media action check. A page editor can chain addMetaFile with value, toYaml or toJson to read server-readable YAML files, such as account password hashes, 2FA secrets and API keys, into a publicly viewable page.

### CVE-2026-124428

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-08T14:18:08.677 |

Craft CMS from 5.7.0 before 5.11.2 contains an arbitrary file read vulnerability that allows authenticated control panel users to read SVG files by posting arbitrary paths to the app/icon-svg endpoint. Attackers can supply aliases or absolute paths, which are resolved without permission checks, to read any SVG-content file readable by the PHP process, including files outside the Craft installation.

### CVE-2026-124424

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-08T14:18:07.930 |

WWBN AVideo contains a path traversal vulnerability in plugin/AI/receiveAsync.json.php that allows holders of any valid AI token to write arbitrary .vtt files by injecting traversal sequences into the unsanitized response[lang] parameter. Attackers can send a type=translation request with a crafted lang value to plant attacker-controlled content in the webroot or overwrite other users' subtitle files.

### CVE-2026-123545

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-08T02:16:45.597 |

OpenAM from 14.5.1 before 16.1.4 contains a cross-site request forgery vulnerability in the OAuth 2.0 device authorization flow that allows attackers to approve device codes when consent is skipped for implied-consent clients. Attackers can start a device authorization and lure a logged-in user to a crafted page, obtaining access and ID tokens to call APIs as that user.

### CVE-2026-123532

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-08T02:16:43.367 |

gix-fs in gitoxide before 0.24.1 contains a credential disclosure vulnerability that allows remote attackers to capture NTLM credentials by supplying UNC symlink targets in a crafted repository. When a victim checks out the repository on Windows with symlinks enabled, gix_fs::symlink::create calls is_dir() on the UNC target, triggering SMB authentication that leaks the username, domain, and NTLMv2 hash.

### CVE-2026-123525

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-08T02:16:42.133 |

Vikunja before 2.7.1 allocates memory without limits in its Trello, Todoist and Microsoft To Do migration importers, which buffer remote attachment downloads and API responses in memory without size caps. Authenticated users can start a migration that references huge attacker-served attachments or yields oversized API responses, exhausting memory and crashing the shared API process for all tenants.

### CVE-2026-123523

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-08T02:16:41.780 |

Vikunja before 2.7.1 contains an uncontrolled resource consumption vulnerability that allows authenticated users to exhaust server memory by requesting avatars at many distinct sizes. Attackers can upload a noisy avatar and fetch it at each size up to 1024, caching roughly a gigabyte per account without eviction and causing the API process to be OOM-killed.

### CVE-2026-123522

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-08T02:16:41.607 |

Vikunja before 2.7.1 contains an authorization bypass vulnerability that allows authenticated users to read any task by injecting a crafted task object into a no-op Kanban bucket move. Attackers can set task.id to a victim task and task.project_id to their own project, routing full task contents to their webhook and forging mention notifications.

### CVE-2026-123520

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-08T02:16:41.247 |

Vikunja from 0.18.0 before 2.7.1 contains a privilege escalation vulnerability that allows team owners to gain admin or ownership of read-only shared projects by deleting accounts. Attackers can create a bot, add it to their team, and delete it through the bots endpoint, triggering ensureProjectAdminUser to promote read-only shares and lock out the real owner.

### CVE-2026-123519

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-08T02:16:41.070 |

Vikunja before 2.7.1 contains a denial of service vulnerability that allows authenticated users to exhaust API process memory by uploading WeKan or vikunja-file imports with no item-count cap. Attackers can submit a ~22 MB WeKan JSON with hundreds of thousands of cards or duplicate IDs to the wekan migrate endpoint, triggering OOM and crashing the instance.

### CVE-2026-123517

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-204` |
| Published | 2026-11-08T02:16:40.720 |

Vikunja before 2.7.1 contains an information disclosure vulnerability that allows authenticated users to determine whether private teams exist by calling the team member self-removal endpoint. Attackers can send DELETE requests to /teams/{id}/members/{own username} for arbitrary team ids and use the distinguishable responses to learn if a team exists, is SSO-managed, or has a single member.

### CVE-2026-123516

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-08T02:16:40.543 |

Vikunja before 2.7.1 contains a resource exhaustion vulnerability in the vikunja-file ZIP importer that allows authenticated users to consume CPU and memory by uploading archives with excessive entries. Attackers can upload export ZIPs containing many empty or non-files/ entries that bypass the per-entry caps, forcing scanArchive to process every entry twice.

### CVE-2026-123501

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-08T02:16:37.853 |

Vikunja before 2.7.1 contains an uncontrolled resource consumption vulnerability that allows authenticated users to exhaust server memory through concurrent image decodes in avatar and background uploads. Attackers can send several parallel tiny, highly compressible PNGs decoded at up to 50 megapixels each, pushing the API process into memory pressure or an OOM kill.

### CVE-2026-124315

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-07T15:17:15.693 |

Frappe ERPNext before 15.121.4 and 16.x before 16.36.0 contains a missing authorization vulnerability in the whitelisted get_bom_items and get_bom_diff methods that skip BOM read permission checks. Any authenticated user, including portal or no-role users, can call get_bom_items with a BOM name to retrieve every raw material, quantity, rate and cost.

### CVE-2026-124314

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-07T15:17:15.503 |

Frappe ERPNext before 15.121.4 and 16.x before 16.36.0 contains a missing authorization vulnerability in erpnext.crm.utils.get_open_activities that exposes ToDo and Event records. Any authenticated user, including portal or no-role users, can supply arbitrary ref_doctype and ref_docname values to enumerate activities and private calendar event details.

### CVE-2026-124433

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-08T14:18:09.487 |

phpMyFAQ before 4.1.11 contains an insufficient authorization vulnerability that allows delegated administrators holding only GROUP_DELETE permission to delete higher-privileged groups. Attackers can submit a target group_list_select value to /admin/group/confirm and then /admin/group/delete to remove privileged groups, their memberships, and permission mappings.
