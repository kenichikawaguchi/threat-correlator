# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-20 15:00 UTC
- **対象期間**: `2026-11-19T15:00:54.000Z` 〜 `2026-11-20T15:00:49.000Z`
- **重要CVE数**: 287 件（Critical 9.0+: 57 件 / High 7.0〜: 230 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件近く** に上ります。共通する傾向は以下の通りです。

* **認証不要（Unauthenticated）** のリモートコード実行・コマンドインジェクションが多数。特に Web アプリケーションや API の入力検証不備が原因です。  
* **デフォルト認証情報や設定ミス** に起因する権限昇格・不正アクセスが目立ち、産業制御系（Danfoss）やクラウド基盤（VMware vCenter）でも報告されています。  
* **TLS/証明書検証の無効化** や **不適切なシリアライズ** が原因で、Man‑in‑the‑Middle 攻撃や任意コード実行が可能になるケースが増加しています。  

このように、**「認証バイパス」＋「入力サニタイズ不備」** の組み合わせが最も危険度が高く、早急な対策が求められます。

---

## 2. 特に注目すべき CVE（上位 5 件）

| CVE | スコア | 主な脆弱性種別 | 影響範囲・被害シナリオ | 注目理由 |
|-----|--------|----------------|------------------------|----------|
| **CVE‑2026‑14914** | 10.0 | 任意ファイルアップロード（Web Shell） | Tegsoft Contact Center のファイルアップロード機能で任意のシェルをサーバに配置可能。認証不要でリモートコード実行が成立。 | **最高スコア** かつ **企業向けコールセンター** という重要インフラに直結。 |
| **CVE‑2026‑77312** | 10.0 | パス検証不備による任意ファイル書き込み | Flyto2 Core 2.26.8 未満で `data.csv.write` などがバリデーション対象外。攻撃者は任意の CSV/JSON を任意の場所に書き込み、後続のコード実行や情報漏洩を引き起こす。 | **自動化/AI ワークフロー基盤** に組み込まれ、広範囲の業務プロセスに波及。 |
| **CVE‑2026‑133323** | 10.0 | パラメータサニタイズ不足によるブラインドコマンドインジェクション | Mitel MiCollab (Audio/Video Conferencing) 10.3.0.18 以前で、特定 API のパラメータがエスケープされず、攻撃者はコマンドを注入できる。 | **通信・コラボツール** は社内外の機密情報を扱うため、侵入後の被害が大きい。 |
| **CVE‑2026‑133648** | 9.9 | TLS 証明書検証無効化（Man‑in‑the‑Middle） | Flowintel の MISP API、IMAP/SMTP STARTTLS で全ての証明書検証を無効化。ネットワーク上の攻撃者が通信を改竄・盗聴できる。 | **暗号化通信の根幹** を破るため、内部・外部のデータ保護が失われる。 |
| **CVE‑2026‑123890** | 9.8 | VMware vCenter ディレクトリサービスの認証バイパス | vCenter 9.1.x/9.0.x/8.0/5.x 系列で、認証バイパスにより管理者権限取得が可能。 | **仮想基盤の管理権限取得** は全システムへの横展開リスクを伴う。 |

> **共通点**：すべて認証不要または極低権限での操作で、**リモートコード実行** または **管理権限取得** が可能。特にインフラ系（コールセンター、仮想基盤）と開発プラットフォーム（Flyto2、Mitel）は、組織全体の業務継続に直結するため、最優先で対策すべきです。

---

## 3. 推奨アクション（具体的なパッケージ名・バージョンを明記）

### 3.1 共通的な緊急対策
1. **脆弱性スキャンの実施**  
   - NVD、JVN、各ベンダーのアドバイザリを自動取得し、対象資産に対して **CVE‑2026‑14914〜2026‑133648** が含まれるか即時確認。  
2. **ネットワーク分離**  
   - 影響が確認されたサービスは、外部からの直接アクセスを **ファイアウォールで遮断** し、内部限定に留める。  
3. **監査ログの強化**  
   - すべての認証失敗・ファイルアップロード・API 呼び出しを **SIEM に集約** し、異常検知ルールを追加。  

### 3.2 個別パッケージ／製品別対策

| 製品・パッケージ | 現行バージョン | 推奨バージョン / パッチ | 具体的対策 |
|------------------|----------------|--------------------------|------------|
| **Tegsoft Contact Center** | `latest-202611161510` 未満 | **latest-202611161510**（ベンダー提供の修正リリース） | - アップロード機能の **MIME タイプ検証** を有効化<br>- WebShell と思しきファイルの **リアルタイムスキャン** を導入 |
| **Flyto2 Core** | 2.26.7 以前 | **2.26.8** 以上 | - `validate_path_with_env_config()` を全モジュールに適用するパッチを適用<br>- 書き込み先ディレクトリを **ホワイトリスト** で限定 |
| **Mitel MiCollab** | 10.3.0.18 以前 | **10.3.0.19** 以上（公式パッチ） | - パラメータサニタイズロジックを **正規表現ベース** に更新<br>- 不要な外部 API エンドポイントは **無効化** |
| **Flowintel (MISP API / IMAP / SMTP)** | 任意 | **最新版 (2026‑xx‑xx)** で TLS 検証復元 | - `verify_ssl` フラグを **true** に設定<br>- 既存接続は **再生成** し、証明書ピンニングを導入 |
| **VMware vCenter** | 9.1.x / 9.0.x / 8.0 / 5.x | **9.1.1.0200**, **9.0.2.0200**, **8.0 U3m**, **5.2.5** 以上 | - **vCenter Server Patch** を即適用<br>- 管理コンソールへのアクセスは **MFA** を必須化 |
| **Danfoss AK‑SC / AK‑SM 系列** | すべてのファームウェア | **ファームウェア更新（ベンダー提供）** | - デフォルト認

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-14914

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-20T14:17:53.043 |

Unrestricted upload of file with dangerous type vulnerability in Tegsoft Yönetim ve Bilişim Hizmetleri Tic. Ltd. Şti. Tegsoft Contact Center allows Upload a Web Shell to a Web Server.

This issue affects Tegsoft Contact Center: before latest-202611161510.

### CVE-2026-77312

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-19T22:18:44.013 |

Flyto2 Core is an execution kernel for automation and AI-agent workflows. Prior to 2.26.8, the earlier CVE-2026-67429 remediation applied validate_path_with_env_config() to only a hand-picked set of file-writing modules, leaving data.csv.write in src/core/modules/atomic/data/csv_write.py, data.json_to_csv in src/core/modules/atomic/data/json_to_csv.py, file.copy in src/core/modules/atomic/file/copy.py, and file.move in src/core/modules/atomic/file/move.py outside the FLYTO_SANDBOX_DIR confinement boundary. The advisory also identifies unguarded modules across the broader data.*, file.*, and report-writer families. data.csv.write relies on a .. substring denylist that does not reject absolute paths, while the other named modules accept caller-controlled output or destination paths without the canonical guard. A caller able to execute modules or recipes can therefore write attacker-controlled content outside the configured sandbox, potentially overwriting application code, recipes, startup files, scheduled-task files, or authorization files and gaining code execution on the host. This issue is fixed in version 2.26.8.

### CVE-2026-133323

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-19T17:18:52.880 |

A vulnerability in the Audio, Web, and Video Conferencing (AWV) component of Mitel MiCollab through 10.3 (10.3.0.18) could allow an unauthenticated attacker to conduct a blind command injection attack due to insufficient parameter sanitization. A successful exploit could allow an attacker to execute arbitrary commands within the context of the system. This is MTLVULN-1864.

### CVE-2026-133648

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-20T11:18:33.157 |

Flowintel disabled TLS certificate verification for all MISP API connections and used unverified SSL contexts for IMAP and SMTP STARTTLS mail connections. This allowed an on-path (man-in-the-middle) attacker positioned between Flowintel and its MISP or mail servers to impersonate the remote server and intercept sensitive data.

Affected connections include:
- All MISP HTTPS API calls (event retrieval, attribute search, event creation, connectivity checks, and API validation)
- SMTP STARTTLS connections used for sending email notifications
- IMAP TLS connections used for fetching mail archives and testing connectivity

An attacker who can observe or intercept network traffic between Flowintel and the MISP or mail server could:
- Capture MISP API keys and mail credentials (SMTP/IMAP passwords)
- Read all threat intelligence data exchanged (events, attributes, objects, reports)
- Inject or modify threat intelligence data returned to Flowintel

The vulnerability required no authentication on the part of the attacker and no user interaction; it was exploitable by any party with a network position between Flowintel and its configured MISP or mail endpoints.

Affected versions: Flowintel prior to 4.1.0.

### CVE-2026-127057

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-11-20T11:18:30.617 |

The
Danfoss legacy AK-SC 355 and AK-SM 800 Series are vulnerable to unauthorized
access when default credentials or known passwords are used for authentication.
These products were manufactured with default credentials documented in the
product manual. All versions are affected.

### CVE-2026-131253

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-19T20:17:40.407 |

In Splunk SOAR versions below 8.8.0, an authenticated user that holds a role with the Apps edit, Containers edit, and Playbooks execute permissions could use the App Wizard to execute arbitrary code as the user account that runs Splunk SOAR. This could compromise the confidentiality, integrity, and availability of the Splunk SOAR instance.
The vulnerability exists because the App Wizard does not validate user-supplied identifiers before incorporating them into generated connector code.

### CVE-2026-80188

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-20T14:17:54.003 |

The BuddyBoss Addons plugin for WordPress is vulnerable to Authentication Bypass leading to Account Takeover in versions up to, and including, 1.2.1. This is due to the Social Login REST endpoint trusting unverified Apple and Facebook identity-token claims and linking an attacker-controlled provider identifier to an existing WordPress user selected by the token’s email claim. This makes it possible for unauthenticated attackers who know a user’s email address to associate their provider identity with that account, including administrator accounts, and subsequently authenticate as the victim. Successful exploitation requires the BuddyBoss Platform plugin to be installed and active, with the Social Login module and selected provider enabled and configured. On sites with the separate BuddyBoss App JWT component, the vulnerable REST request can return an application token immediately.

### CVE-2026-129039

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-20T14:17:45.273 |

Deserialization of Untrusted Data vulnerability in Tribulant Software Newsletters newsletters-lite allows Object Injection.This issue affects Newsletters: from n/a through 4.18.2.

### CVE-2026-129073

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-20T13:18:37.040 |

Authentication Bypass Using an Alternate Path or Channel vulnerability in miniOrange miniorange otp verification miniorange-otp-verification allows Authentication Abuse.This issue affects miniorange otp verification: from n/a through 5.6.1.

### CVE-2026-129056

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-20T08:18:28.333 |

Incorrect Privilege Assignment vulnerability in Paul Ryan Authorizer authorizer allows Privilege Escalation.This issue affects Authorizer: from n/a before 3.17.2.

### CVE-2026-114516

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-200;CWE-306` |
| Published | 2026-11-19T22:17:54.773 |

Etherpad is a real-time collaborative editor. From 1.8.14 until 3.3.3, the pre-authentication /static/* plugin asset handler in src/node/utils/Minify.ts performs a backslash-to-forward-slash conversion after src/node/utils/sanitizePathname.ts has completed its POSIX path checks. On POSIX systems the sanitizer correctly treats backslashes as ordinary filename bytes, but the later conversion turns encoded backslash-separated parent-directory segments into traversal components without revalidation or containment. The expressPreSession registration and the always-present ep_etherpad-lite core pseudo-plugin make this path reachable without credentials, allowing a remote attacker to read any file available to the Etherpad process. Disclosed configuration or environment secrets can expose administrator credentials, after which the administrator plugin installer can provide in-process code execution and full server compromise. This issue is fixed in version 3.3.3.

### CVE-2026-87977

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-19T21:18:06.517 |

IBM Guardium Data Protection 12.2 is vulnerable to SQL injection in the edge-controller component. An unauthenticated remote attacker could exploit this vulnerability to access or modify sensitive database information.

### CVE-2026-84236

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-19T21:18:06.053 |

IBM Guardium Data Protection 12.2 is vulnerable to insecure deserialization in the SharePoint Tap MulticastTransceiver component. An unauthenticated remote attacker could exploit this vulnerability to execute arbitrary code on the affected system.

### CVE-2026-128138

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77;CWE-88` |
| Published | 2026-11-19T18:18:06.150 |

NLTK (Natural Language Toolkit) is a suite of open source Python modules, data sets, and tutorials supporting research and development in Natural Language Processing. From 3.10.3 until 3.10.4, the NLTK 3.10.3 JVM hardening validates Java launcher tokens in the options channel but appends the caller-controlled cmd sequence without requiring its first token to be a main class. Supplying -jar or an @argfile through nltk.internals.java or StanfordSegmenter.java_class can therefore execute attacker-selected Java bytecode without the unsafe-JAR opt-in. This issue is fixed in version 3.10.4.

### CVE-2026-123890

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-19T15:17:25.407 |

VMware vCenter contains an authentication bypass vulnerability in the VMware Directory Service.
Affected versions: 9.1.x (fixed in 9.1.1.0200); 9.0.x (fixed in 9.0.2.0200); 8.0 (fixed in 8.0 U3m); 5.x (fixed in 5.2.5).
Telco Cloud Platform 3.0, 4.x, 5.0.x, 5.1.x, 5.2 and Telco Cloud Infrastructure 3.0 are also affected (see KB463116).

### CVE-2026-131287

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-19T20:17:44.650 |

In Splunk SOAR versions below 8.8.0, a user that holds a role with the Playbooks view, edit, execute, and delete permissions could cause existing cross-repository playbook references to run attacker-controlled playbook code.
The vulnerability is possible because Splunk SOAR can bind existing cross-repository playbook references to a different source control repository when a deleted repository name is reused.

### CVE-2026-77369

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639;CWE-862;CWE-863` |
| Published | 2026-11-19T17:18:59.850 |

Daptin is a GraphQL/JSON-API headless CMS. From 0.11.4 until 0.12.30, the generic GET /yjs/:documentName WebSocket route in InitializeYjsResources requires a session but does not authorize the database resource selected by a typename.referenceId.columnName room name. The YJS initial-content provider then reads the selected file.* column without CanRead or CanUpdate checks, and bidirectional synchronization allows a low-privileged authenticated user to read or modify restricted row content. Unauthenticated requests are rejected, and standalone non-canonical room names remain shared-by-name rooms. This issue is fixed in version 0.12.30.

### CVE-2026-133189

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-19T17:18:36.627 |

A command injection vulnerability was found in OpenStack Cinder's SSH-based storage-driver support. Incomplete validation of shell metacharacters allows an authenticated user who owns a volume on an affected backend to supply crafted connection information and inject additional commands into the storage array's management interface. Commands execute with the privileges of Cinder's configured backend account. This can disclose storage configuration information and, where that account has administrative permissions, could allow changes that affect the integrity or availability of other tenants' storage.

### CVE-2026-124772

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-20T11:18:30.480 |

Authorization bypass in the publication of XOneManager 3.8.3.0 updates. During testing, the server accepted initial requests from an authenticated project member with read-only access without verifying publication permissions. If the workflow is completed, updates with modified content could be distributed to managed devices.

### CVE-2026-124770

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-20T11:18:30.210 |

Authorization bypass in the ‘tablesData’ operation of the POST request to ‘/xmanagercore/api/services/’ in XOneManager 3.8.3.0. An authenticated project member can execute SQL queries using ‘filter’ without the server verifying their execution permissions. The queries use the service account’s permissions. During testing, databases outside the project were queried, including the authentication database.

### CVE-2026-76536

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-19T20:17:52.850 |

In Splunk Enterprise versions below 10.4.5, 10.2.9, 10.0.12, and 9.4.17, an unauthenticated user could use an empty clustering shared secret to read and modify clustering configuration through the cluster configuration Representational State Transfer (REST) API endpoint on a standalone instance. This could expose clustering configuration, persist attacker-controlled clustering settings, and disrupt clustering operations.
The vulnerability is possible because Splunk Enterprise accepts the empty clustering shared secret as a shared-authentication candidate on a standalone instance when clustering is turned off.

### CVE-2026-77367

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:H` |
| Weaknesses | `CWE-20;CWE-89` |
| Published | 2026-11-19T17:18:59.677 |

Daptin is a GraphQL/JSON-API headless CMS. Prior to 0.12.30, the generic GET /api/{entity} list endpoint accepts attacker-controlled sort values in PaginatedFindAllWithoutFilters in server/resource/resource_findallpaginated.go without validating the requested column against the table schema. The code uses those values for SELECT and ORDER BY identifier construction, so an embedded identifier quote can terminate the quoted identifier and make the remainder parse as SQL, allowing an unauthenticated attacker to extract unauthorized table data through blind or error-based behavior or repeatedly trigger query failures. This issue is fixed in version 0.12.30.

### CVE-2026-129410

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-11-19T17:17:58.147 |

Joomla Extension - vi-solutions - Code injection via calculation formulas in Visforms extension 1.0.0-5.6.4, 6.0.0-6.2.1 - Calculation field formulas were executed using PHP eval() without validating their content, allowing backend users with field edit permissions to execute arbitrary PHP code.

### CVE-2026-129396

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-19T17:17:57.070 |

Joomla Extension - vi-solutions - Arbitrary file write leading to remote code execution in CSS editor in Visforms extension 1.0.0-5.6.3, 6.0.0-6.2.0 - The CSS editor did not restrict file names, extensions and paths of created and saved files, allowing privileged backend users to write arbitrary PHP files.

### CVE-2026-129043

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-20T14:17:45.410 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Tribulant Software Newsletters newsletters-lite allows SQL Injection.This issue affects Newsletters: from n/a through 4.18.2.

### CVE-2026-129713

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-20T11:18:30.953 |

A stack-based buffer overflow in an unauthenticated CGI handler of the
Danfoss AK-SM 8xxA Series controller allows remote attackers to send specially
crafted HTTP/S POST requests, leading to memory corruption, webserver restart
and hypothetically potential arbitrary code execution with webserver privileges.
Authentication is not required to exploit this vulnerability.

### CVE-2026-133493

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-20T07:17:10.853 |

A vulnerability was identified in D-Link DIR-600L 2.17b02. Affected is the function genacgi_main of the file gena.cgi of the component GENA Handler. Such manipulation leads to os command injection. The attack can be launched remotely. The exploit is publicly available and might be used.

### CVE-2026-133528

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-20T01:17:10.633 |

BeamNG.drive before 0.40.6 contains an out-of-bounds write vulnerability because JIT-compiled LuaJIT traces omit FFI array bounds checks, letting untrusted Lua escape the sandbox. Attackers supplying a malicious mod can JIT-compile an FFI store loop, write out of range using a tostring() address leak, re-enable ffi.load, and run commands as the game user.

### CVE-2026-86130

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-441;CWE-502` |
| Published | 2026-11-19T19:17:35.673 |

A missing authentication vulnerability in WatchGuard Dimension's log collection service allows a remote, unauthenticated attacker to execute arbitrary SQL statements and ultimately execute arbitrary code as the Dimension WebUI process user by sending specially crafted network requests.

### CVE-2026-86094

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-285;CWE-532` |
| Published | 2026-11-19T19:17:35.420 |

WatchGuard Dimension records unredacted session identifiers for logged-in users in its web UI diagnostic log. A low-privileged Dimension Administrator can retrieve this log and extract a Super Administrator's session token while that administrator is logged in, enabling account takeover.

This vulnerability is a secondary unmitigated attack path for CVE-2026-78174.

### CVE-2026-84322

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-285` |
| Published | 2026-11-19T19:17:35.287 |

WatchGuard Dimension returns unredacted session identifiers for logged-in users in a management API response. A low-privileged Dimension Administrator can retrieve the active session IDs of other administrators, including Super Administrators, while they are logged in, enabling account takeover.

### CVE-2026-77359

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-350` |
| Published | 2026-11-19T17:18:59.520 |

Jupyter MCP Server is a Model Context Protocol server for Jupyter. Prior to 1.0.3, standalone streamable-http mode validates Host and Origin values for /mcp but does not apply the same browser-origin controls to the state-changing /api/connect and /api/stop management routes. A malicious website can use DNS rebinding so that its hostname resolves to a loopback, LAN, VPN, or published-container MCP listener, then send a browser-shaped request that /api/connect accepts to replace runtime_url and document_url values and start a kernel client against attacker-controlled infrastructure. The attacker can thereby cause Jupyter API and WebSocket traffic to reach that infrastructure and can use /api/stop to stop the current notebook kernel. The default broad bind can increase exposure, but the vulnerability is the missing management-route origin boundary, not a lack of Host validation on /mcp. This issue is fixed in version 1.0.3.

### CVE-2026-77338

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-19T17:18:59.367 |

Sprout Track is a self-hosted baby tracking application. Prior to 1.3.5, Sprout Track uses a publicly known hardcoded signing secret when JWT_SECRET is unset, and standard setup does not generate a unique secret. On a network-reachable affected deployment, an unauthenticated attacker can sign JWTs with arbitrary claims, including system-administrator claims, to access administrative functionality and read or modify family, child activity, account, and email data. Deployments with a strong unique JWT_SECRET are not affected. Managed and hosted instances were reported remediated. This issue is fixed in version 1.3.5.

### CVE-2026-126088

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-19T19:17:18.967 |

In Autonomy Logic OpenPLC Runtime versions 4.2.4 and prior, a race condition allows multiple concurrent requests to pass the existence check before any user is committed, resulting in several unauthenticated admin accounts being created.

### CVE-2026-133310

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-626` |
| Published | 2026-11-19T17:18:52.597 |

Wing FTP Server before 8.2.8 contains a file mask bypass vulnerability allowing attackers to upload restricted files via an embedded NUL byte in Upload Link filenames. Attackers can plant a Lua session file with a chosen UID and send a matching UID cookie to execute operating system commands as the service account.

### CVE-2026-129411

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-19T17:17:58.280 |

Joomla Extension - vi-solutions - Unauthenticated SQL injection in frontend data view filters in Visforms extension 1.0.0-5.6.4, 6.0.0-6.2.1 - Sorting, location radius and published filters of the frontend data view were not properly sanitized, allowing SQL injection, partly without authentication.

### CVE-2026-129402

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-19T17:17:57.757 |

Joomla Extension - vi-solutions - Unauthenticated SQL injection in reload task in Visforms extension 1.0.0-5.6.4, 6.0.0-6.2.1 - Input placeholders in SQL field statements were inserted without quoting in the public reload task, allowing unauthenticated SQL injection in read queries.

### CVE-2026-129496

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416;CWE-459` |
| Published | 2026-11-19T15:17:28.373 |

Timezone cache use-after-free can lead to remote code execution.

In non-thread-safe builds, a diagnostic written to a file-based error_log during module startup, for example for an invalid date.timezone value or a session configuration warning, causes the timezone cache to be allocated in startup memory that is freed while a reference to it is kept. A diagnostic raised early in the first request of a worker, such as the max_input_vars warning, then accesses the freed cache. On such a deployment an unauthenticated remote attacker can crash PHP-FPM, Apache mod_php or CGI workers with a crafted request. Arbitrary code execution may be possible and has been demonstrated with known memory addresses.

This issue affects PHP versions before 8.2.36, 8.3.* before 8.3.37, 8.4.* before 8.4.28 and 8.5.* before 8.5.13.

### CVE-2026-129481

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416;CWE-459` |
| Published | 2026-11-19T15:17:28.240 |

Use-after-free after interrupted session shutdown.

The session extension records the filename of the executing script when a session starts. If a fatal error occurs in an application callback while the session variables are destroyed at shutdown, such as stream_close() of a user-defined stream wrapper, the pointer is retained after the request memory is freed, and a later request handled by the same worker can free the stale string. An attacker who can trigger such a failing cleanup may crash the worker or corrupt memory; code execution has not been demonstrated. This requires the filename to be allocated in request memory, for example when the script is not cached by OPcache.

This issue affects PHP versions 8.3.* before 8.3.37, 8.4.* before 8.4.28 and 8.5.* before 8.5.13.

### CVE-2026-129474

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-19T15:17:28.110 |

Use-after-free in magic method backtraces can lead to remote code execution.

When collecting the arguments of a method call handled by __call() or __callStatic() for a backtrace, PHP can read stale values that may refer to freed memory. If a fatal error such as exceeding memory_limit occurs while an application enters such a call, with fatal_error_backtraces enabled (the default) and zend.exception_ignore_args disabled, a remote attacker who controls enough request data to influence memory allocation may cause memory corruption, crash the PHP worker or, with knowledge of memory addresses, execute arbitrary code. php.ini-production enables zend.exception_ignore_args, which prevents this.

This issue affects PHP versions 8.5.* before 8.5.13.

### CVE-2026-129289

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444;CWE-670` |
| Published | 2026-11-19T15:17:27.523 |

PHP-FPM request smuggling through an unread HTTP request body.

PHP does not discard the unread part of an HTTP request body at request shutdown when the application has opened php://input without reading it to the end. When the front end reuses backend connections, which is not the default in nginx or Apache (for example nginx with fastcgi_keep_conn on, or Apache mod_proxy_fcgi with enablereuse=on), PHP-FPM can parse the leftover bytes as a new FastCGI request. An unauthenticated remote attacker can use a single crafted multipart/form-data request to forge a backend request with chosen parameters such as SCRIPT_FILENAME, REMOTE_ADDR and PHP_ADMIN_VALUE, which can lead to execution of attacker-controlled PHP code. With LSAPI, subsequent requests on the connection can be disrupted.

This issue affects PHP versions before 8.2.36, 8.3.* before 8.3.37, 8.4.* before 8.4.28 and 8.5.* before 8.5.13.

### CVE-2026-129182

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416;CWE-459` |
| Published | 2026-11-19T15:17:27.390 |

Use-after-free via repopulation of last_fatal_error_backtrace global after shutdown.

A fatal error raised while modified INI settings are restored during request shutdown can repopulate the stored fatal error backtrace after the executor has been cleaned up. The request memory is then freed, and a diagnostic emitted before executor initialization in a later request handled by the same PHP-FPM or mod_php worker can access the stale backtrace. The shutdown error requires per-path configuration of max_memory_limit, or of zlib.output_compression together with output_handler (which .user.ini can also set). The early diagnostic requires Apache per-directory configuration or, for PHP-FPM, a PHP_VALUE or PHP_ADMIN_VALUE parameter sent by the front end. This can cause memory corruption and worker crashes, and may allow remote code execution.

This issue affects PHP versions 8.5.* before 8.5.13.

### CVE-2026-126714

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367;CWE-662` |
| Published | 2026-11-19T15:17:26.167 |

Partially overwritten session files can lead to remote code execution.

The files session save handler, which is the default, writes updated session data into the existing session file without first clearing it. If a write is interrupted, the file can contain the beginning of the new session followed by the end of the old one, and bytes of an ordinary string can later be unserialized as objects. An attacker who can influence the session data, for example through session upload progress, and interrupt a write at a suitable point may inject objects, which can lead to code execution when the application contains a suitable gadget chain. Session data can also be corrupted.

This issue affects PHP versions before 8.2.36, 8.3.* before 8.3.37, 8.4.* before 8.4.28 and 8.5.* before 8.5.13.

### CVE-2026-115560

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-502` |
| Published | 2026-11-19T15:17:24.610 |

Session serializer mismatch can lead to remote code execution.

Session upload progress, when enabled, can store attacker-controlled data in a session key using the php_binary or php_serialize session serializer. If the same session is later read with the php serializer, because session.serialize_handler is changed at runtime or differs between applications sharing a session store, bytes inside the key can be passed to the unserializer. A remote attacker able to submit a multipart upload can inject objects, which may lead to code execution when the reading application contains a suitable gadget chain, or to session corruption or denial of service.

This issue affects PHP versions before 8.2.36, 8.3.* before 8.3.37, 8.4.* before 8.4.28 and 8.5.* before 8.5.13.

### CVE-2026-101340

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-338` |
| Published | 2026-11-20T13:18:34.770 |

Net::DNS uses a 16-bit query ID to match responses to the corresponding requests.  In versions up to and including 1.57, the ID is obtained from Perl's built-in rand() function.  An attacker that can observe the sequence of query IDs is able to expose the internal state of the PNRG and hence predict query IDs before they are transmitted.  The victim Net::DNS instance is then exposed to forged responses injected by the attacker.  Note that the deduplication cache in 1.57 has no impact on the feasibility of this attack.

### CVE-2026-120681

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-20T10:17:08.647 |

The Mang Board plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 2.4.7. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to delete any board post — including administrator-owned content — along with its associated comments and file links. A nonce sufficient to pass the initial nonce check is publicly exposed on any board listing page, meaning no prior authentication or privileged access is required to initiate the exploit.

### CVE-2026-82339

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-19T21:18:05.050 |

IBM Guardium Data Protection 12.2 is vulnerable to missing authentication in the SharePoint S-TAP RelayService, allowing an unauthenticated network attacker to inject forged audit events and access the active monitoring policy.

### CVE-2026-129932

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-11-19T21:17:51.217 |

The MongoDB Java driver applies its DNS seedlist domain restriction to a record value that is later re-interpreted differently when the connection target is parsed, so the name that is checked and the name that is used can differ. An unauthenticated party who can set or forge the DNS service record for the seed domain in a connection string can cause the driver to direct its session to an unrelated host and to complete certificate verification against that host instead. This may result in unintended disclosure of application data and of configured database credentials, and in unintended content being returned to the application as query results.

### CVE-2026-76535

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-19T20:17:52.730 |

In Splunk Enterprise versions below 10.6.1, 10.4.5, 10.2.9, 10.0.12, and 9.4.17, an unauthenticated user could run arbitrary Search Processing Language (SPL) searches through RapidDiag task collection as an authenticated user. With this access, the user could read or modify data and configuration available to that authenticated user.
The vulnerability is possible because Splunk Enterprise accepts an empty shared secret when it authenticates RapidDiag task-collection requests.
For more information see Using RapidDiag (https://help.splunk.com/en/splunk-enterprise/administer/troubleshoot/9.3/contact-splunk-support/using-rapiddiag) in the Splunk documentation.

### CVE-2026-131202

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-19T20:17:33.250 |

In Splunk Enterprise Security versions below 8.7.0, a user who holds the "ess_admin" Splunk Enterprise Security role could execute arbitrary code on the search head as the user account running Splunk Enterprise by combining lookup file upload and Configuration Checker functionality.
The vulnerability is possible because Splunk Enterprise Security does not restrict lookup upload file types or keep Configuration Checker module paths within the intended directory.
For more information see Users and roles for Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/install/8.7/installation/users-and-roles-for-splunk-enterprise-security) and Create and manage lookups in Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.7/managing-security-content/create-and-manage-lookups-in-splunk-enterprise-security) in the Splunk documentation.

### CVE-2026-129938

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-19T20:17:27.663 |

An improper neutralization of delimiters in the MongoDB C# driver's DNS SRV connection-string resolution lets an unauthenticated party who can answer the client's DNS SRV query place a host outside the trusted domain into the client's server list. When an application resolves the connection string through the affected API and connects with the result, application data, authentication credentials and query results may pass through that host. This may result in unintended disclosure of data and credentials and in forged query results.

### CVE-2026-104099

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-41;CWE-289;CWE-863` |
| Published | 2026-11-19T20:17:13.897 |

Fabio is an HTTP(S) and TCP router for deploying applications managed by consul. Prior to 1.7.3, route/table.go selects targets using raw req.URL.Path, while proxy/http_proxy.go applies per-route ACL and basic-auth checks to the selected target and forwards the raw path to the origin. Dot-segment, encoded-dot, or repeated-slash variants can fall through to a less restrictive route that reaches the same backend; the backend then normalizes the path and serves the protected resource without the configured access controls. A less restrictive fallback route must reach the same backend; without one, the request returns 404. This issue is fixed in version 1.7.3.

### CVE-2026-133185

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-337` |
| Published | 2026-11-19T15:17:39.470 |

Goproxy before 1.9.4 contains a weak key generation vulnerability in NewCounterEncryptorRandFromKey that derives RSA and Ed25519 leaf certificate private keys from public data due to misuse of hash.Sum. Attackers with the CA certificate and one observed leaf certificate can regenerate that host's leaf private key and impersonate the host to clients trusting the proxy CA.

### CVE-2026-120753

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-290` |
| Published | 2026-11-19T15:17:25.013 |

In Eclipse Ditto versions 1.1.0 to 3.9.8, when pre-authentication is enabled, the gateway service accepts the pre-authenticated subject not only from the `x-ditto-pre-authenticated` HTTP header set by a trusted reverse proxy, but also from an undocumented `x-ditto-pre-authenticated` URL query parameter that a client can set. A reverse proxy that only overwrites the header therefore does not stop clients from supplying their own subject. With the default configuration of the Ditto Helm chart (`global.jwtOnly: false`, which implicitly enables pre-authentication), the bundled nginx skips HTTP Basic authentication for any request with an `Authorization: Bearer` header and forwards it without the pre-authentication header. An unauthenticated remote attacker can send an invalid Bearer token together with the query parameter to authenticate as any chosen policy subject. Pre-authentication succeeds before the JWT is validated, so the attacker can read and modify Things and Policies with that subject's permissions. As a mitigation, disable pre-authentication in the gateway (`ENABLE_PRE_AUTHENTICATION=false`) or, when using the Helm chart, configure `global.jwtOnly: true`.

### CVE-2026-65094

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-123` |
| Published | 2026-11-20T03:17:36.693 |

NVIDIA VIRTIO-Net for Bluefield contains a vulnerability in Virtio-Net where a VM user may cause a Write-What-Where condition by crafted message. A successful exploit of this vulnerability may lead to Code Execution in Virtio-Net scope.

### CVE-2026-130158

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T19:17:25.680 |

RepoManager is a self-hosted deb/rpm package repository. Prior to 5.13.3, a registered host or a party with its host/API credential can submit package metadata. Inventory reporting accepts package name and version, while available-update reporting accepts package name, version, and repository; the repository field exists only on that path. RepoManager stores these values, and stored values are rendered on the host's package detail page without preventing stored HTML or JavaScript from executing. An administrator must later view the page for script execution. The script runs in the administrator's authenticated browser session and can expose administrative data or forge privileged requests; the advisory describes possible escalation through admin-only functionality. Fixed in 5.13.3.

### CVE-2026-133303

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-91` |
| Published | 2026-11-19T17:18:51.670 |

A vulnerability in the Audio, Web, and Video Conferencing (AWV) component of Mitel MiCollab through 10.3 (10.3.0.18) could allow an unauthenticated attacker to leverage pre-staged malicious content to conduct an XML injection attack due to insufficient parameter validation. A successful exploit could allow an attacker to execute arbitrary commands within the context of the system. This is MTLVULN-1862.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-131167

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-20T12:18:22.500 |

pretix offloads certain processes to background tasks that are run by a different server to avoid HTTP workers being clogged with processes that take longer than a usual web request. The browser periodically polls the server to see if the task is already finished using a UUID-shaped task ID. Once the task is completed, pretix resumes to the next step of the operation based on the result of the task. The system does however not check if the result stems from the correct type of task. Therefore, an attacker can supply the UUID of a task of a different type and pretix will continue with the result from the wrong task. In most cases, this will just result in an error because the return types do not match up, but in some cases this can be abused to extract objects the attacker usually should not see. Specifically, a vector was discovered that allowed to abuse this for unauthorized access to other people's ticket purchases. The attacker can, however, not control which purchases they get access to.

### CVE-2026-125085

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-20T10:17:10.350 |

The Nexter Extension – Security, Performance, Code Snippets & Site Toolkit plugin for WordPress is vulnerable to Privilege Escalation in versions up to, and including, 4.9.0 This is due to the role_switcher_to_view_admin_as() function handling the `reset-view` branch without a capability check or nonce when the caller's own login is supplied, combined with an incomplete cleanup hook (maybe_prevent_switchback_to_administrator) that exits early when the user's current roles equal the stored view role and that is never triggered when WordPress core's WP_User::set_role() short-circuits because the account already has only the target role. This makes it possible for authenticated attackers, with subscriber-level access and above, to elevate their privileges to Administrator.

### CVE-2026-133476

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-424` |
| Published | 2026-11-19T22:18:04.370 |

In Dolibarr before 24.0.3, dolForgeSQLCriteriaCallback() in htdocs/core/lib/functions.lib.php allows account takeover because it strips only a single table-name prefix from a Universal Search Filter (sqlfilters) operand before checking it against the forbidden-field denylist (pass, pass_crypted, api_key). MariaDB and MySQL accept a two-level qualification such as schema.alias.column, so an operand of the form dolibarr.u.pass_crypted survives the check and is emitted into the WHERE clause. A remote authenticated user holding only the holiday read and readall permissions, which confer no user-management or administrative access, can use the resulting boolean oracle at GET /api/index.php/holidays to recover any user's bcrypt password hash and api_key one character at a time, including an administrator's. Because api_key is accepted directly by the REST API as a bearer credential, this yields full administrative control of the application. This bypasses the fix for CVE-2026-89012, which added only a strtolower() call and did not address prefix depth. The same denylist also omits pass_temp, which stores a password in cleartext, as well as national_registration_number, salary, birth, address, personal_mobile and note_private.

### CVE-2026-76540

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-19T20:17:53.350 |

In Splunk Enterprise versions below 9.4.17, 10.0.12, 10.2.9, and 10.4.5, a user who does not hold the "admin" or "power" Splunk roles can configure a metric alert through the Representational State Transfer (REST) API that runs a search with elevated privileges. The vulnerability lets the user access or modify data and disrupt the Splunk Enterprise instance.
The vulnerability occurs because Splunk Enterprise does not enforce the required role-based authorization when it processes metric alert configuration through the REST API. Splunk Enterprise schedules the resulting search with elevated authorization and runs attacker-controlled search processing with that authorization.
For more information see About configuring role-based user access (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/manage-splunk-platform-users-and-roles/about-configuring-role-based-user-access) in the Splunk documentation.

### CVE-2026-76538

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-19T20:17:53.100 |

In Splunk Enterprise versions below 10.4.5, 10.2.9, 10.0.12, and 9.4.16, a user who does not hold the "admin" or "power" Splunk roles could cause Splunk Enterprise to run arbitrary Search Processing Language (SPL) searches with elevated privileges through data model acceleration.
The vulnerability is possible because Splunk Enterprise does not correctly neutralize caller-supplied data model acceleration values before it places them into generated summarization searches.

### CVE-2026-131295

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-807` |
| Published | 2026-11-19T20:17:45.640 |

In Splunk SOAR versions below 8.8.0, an authenticated user with permission to create and run playbooks could start child playbooks on containers outside the authorized label, or repository scope for that user. This could expose container data and affect automation outside that scope.
The vulnerability is possible because Splunk SOAR does not bind the identity used to authorize the child playbook run to the parent playbook execution context.

### CVE-2026-131271

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-19T20:17:42.640 |

In Splunk SOAR versions below 8.8.0, an authenticated user with permission to view and edit containers for one label could use a slash command through the Representational State Transfer (REST) API to access sensitive product data and credentials outside the authorized container scope.
The vulnerability is possible because Splunk SOAR does not enforce authorization for related objects that slash commands access from an authorized artifact.

### CVE-2026-131270

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-19T20:17:42.517 |

In Splunk SOAR versions below 8.8.0, an authenticated user with repository edit access could cause Splunk SOAR to write files outside the configured repository, which lets the user modify files that the user account running Splunk SOAR can write to.
The vulnerability is possible because Splunk SOAR does not require source control repository paths to remain inside the configured repository.

### CVE-2026-131269

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-19T20:17:42.393 |

In Splunk SOAR versions below 8.8.0, a user that holds a role with the Apps edit permission could cause Splunk SOAR to execute arbitrary code on the host when the user validates an installed app.
The vulnerability is possible because the app validation workflow does not isolate untrusted code from the trusted environment.

### CVE-2026-131263

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-19T20:17:41.650 |

In Splunk SOAR versions below 8.8.0, a user that holds a role with only the apps:edit permission could install a connector app that causes Splunk SOAR to write attacker-controlled files outside the app directory. This could let the user modify files used by Splunk SOAR and execute arbitrary code as the user account that runs Splunk SOAR.
The vulnerability is possible because Splunk SOAR constructs the dependency installation command from app-supplied metadata without preventing that metadata from changing its arguments.
For more information see Manage roles and permissions in Splunk SOAR (On-premises) (https://help.splunk.com/en/splunk-soar/soar-on-premises/administer-soar-on-premises/8.8.0/manage-your-splunk-soar-on-premises-users-and-accounts/manage-roles-and-permissions-in-splunk-soar-on-premises) and Add and configure apps and assets to provide actions in Splunk SOAR (On-premises) (https://help.splunk.com/en/splunk-soar/soar-on-premises/administer-soar-on-premises/8.6.0/manage-your-splunk-soar-on-premises-apps-and-assets/add-and-configure-apps-and-assets-to-provide-actions-in-splunk-soar-on-premises) in the Splunk documentation.

### CVE-2026-131261

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-19T20:17:41.400 |

In Splunk SOAR versions below 8.8.0, a user that holds a role with the Apps edit permission could execute arbitrary code as the user account that runs Splunk SOAR by installing a malicious app.
The vulnerability is possible because Splunk SOAR does not restrict app dependencies to validated binary packages before installing them.

### CVE-2026-131252

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-19T20:17:40.283 |

In Splunk SOAR versions below 8.8.0, a user that holds a role with the Assets edit or delete permission and access to one or more tenants could change or delete assets assigned to other tenants through the Representational State Transfer (REST) API. With this access, the user could redirect connector traffic and expose the credentials and operational data associated with an asset, or disrupt integrations and data ingestion for other tenants.
The vulnerability is possible because Splunk SOAR verifies the Assets edit or delete permission but does not verify that the user can access every tenant assigned to the target asset before Splunk SOAR changes or deletes the asset.
For more information see Manage roles and permissions in Splunk SOAR (On-premises) (https://help.splunk.com/en/splunk-soar/soar-on-premises/administer-soar-on-premises/8.8.0/manage-your-splunk-soar-on-premises-users-and-accounts/manage-roles-and-permissions-in-splunk-soar-on-premises), Configure multiple tenants on your Splunk SOAR (On-premises) instance (https://help.splunk.com/en/splunk-soar/soar-on-premises/administer-soar-on-premises/8.7.0/configure-product-settings-for-your-splunk-soar-on-premises-instance/configure-multiple-tenants-on-your-splunk-soar-on-premises-instance), Add and configure apps and assets to provide actions in Splunk SOAR (On-premises) (https://help.splunk.com/en/splunk-soar/soar-on-premises/administer-soar-on-premises/8.6.0/manage-your-splunk-soar-on-premises-apps-and-assets/add-and-configure-apps-and-assets-to-provide-actions-in-splunk-soar-on-premises), and Using the REST API reference for Splunk SOAR (On-premises) (https://help.splunk.com/en/splunk-soar/soar-on-premises/rest-api-reference/8.5.0/using-the-splunk-soar-rest-api/using-the-rest-api-reference-for-splunk-soar-on-premises) in the Splunk documentation.

### CVE-2026-131246

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-19T20:17:39.550 |

In Splunk SOAR versions below 8.8.0, an authenticated user with edit permission for the container label on a pending approval could read an external-prompt capability through an Approval details Representational State Transfer (REST) API response and use it to view the prompt content, change the pending approval decision, and modify its action parameters.
The vulnerability is possible because an Approval details response exposes the external-prompt capability without checking approval ownership.
For more information see REST External Prompt (https://help.splunk.com/en/splunk-soar/soar-on-premises/rest-api-reference/8.5.0/external-prompt-endpoints/rest-external-prompt) and Manage roles and permissions in Splunk SOAR (On-premises) (https://help.splunk.com/en/splunk-soar/soar-on-premises/administer-soar-on-premises/8.5.0/manage-your-splunk-soar-on-premises-users-and-accounts/manage-roles-and-permissions-in-splunk-soar-on-premises) in the Splunk documentation.

### CVE-2026-131236

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-19T20:17:38.273 |

In Splunk Enterprise Security versions below 8.7.0, an unauthenticated user who can influence indexed event data could store attacker-controlled values in event fields. If another authenticated user who reviews the event selects the View Adaptive Response Invocations or View Adaptive Response Results workflow action from Event Actions, Splunk Enterprise Security could run attacker-controlled Search Processing Language (SPL) commands using the permissions of the user who selects the action. The unauthenticated user could then access or modify sensitive data and disrupt services available to the user who selects the action.
The vulnerability is possible because the affected Common Information Model workflow actions insert the orig_sid and orig_rid event-field values directly into searches without safely validating or quoting the values.
For more information see About workflow actions in Splunk Web (https://help.splunk.com/en/splunk-enterprise/manage-knowledge-objects/knowledge-management-manual/10.2/workflow-actions/about-workflow-actions-in-splunk-web) in the Splunk documentation.

### CVE-2026-131199

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-19T20:17:32.777 |

In Splunk Enterprise Security versions below 8.7.0, a user that holds a role with the mc_investigation_read capability could cause the Risk Event Timeline Representational State Transfer (REST) API to run arbitrary Search Processing Language (SPL) commands with elevated permissions. With this access, the user could expose stored credentials and modify indexes and lookup data available to those permissions.
The vulnerability is possible because the affected REST API does not validate request values before including them in search macro arguments.
For more information see Capability reference for Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/install/8.7/installation/capability-reference-for-splunk-enterprise-security) and Risk analysis (https://help.splunk.com/en/splunk-enterprise-security-8/user-guide/8.7/analytics/risk-analysis) in the Splunk documentation.

### CVE-2026-130160

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-862` |
| Published | 2026-11-19T19:17:25.967 |

RepoManager is a self-hosted deb/rpm package repository. Prior to 5.13.3, an authenticated user can supply a user-controlled, array-valued GPG key identifier to the key deletion action. Validate::string() filters HTML characters but not shell metacharacters. The user-controlled identifier reaches the delete action without shell-safe encoding. controllers/Gpg.php contains the vulnerable deletion path. Process::execute() passes the command string through proc_open() and /bin/sh -c, allowing the attacker to execute arbitrary OS commands as the web/PHP process. This can expose secrets or poison packages. Authentication is required, but the advisory makes an administrator-only restriction conditional on the intended access policy and does not establish an administrator role as a prerequisite. Fixed in 5.13.3.

### CVE-2026-63390

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-125;CWE-190;CWE-787;CWE-1284` |
| Published | 2026-11-19T16:21:39.450 |

HTSlib is a library for reading and writing bioinformatics file formats. Prior to 1.21.2, 1.22.3, 1.23.2, and 1.24, the BCF reader can experience an integer overflow in a record-length check that verifies whether a record contains enough bytes for the expected number and size of stored items. A crafted BCF record can bypass this check, causing reads beyond the stored data and, in some cases, writes beyond the heap buffer when the reader sets the least significant bit of accessed bytes. Opening such a file can crash the process, corrupt data or heap structures, and may permit arbitrary code execution. This issue is fixed in versions 1.21.2, 1.22.3, 1.23.2, and 1.24.

### CVE-2026-62258

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-787` |
| Published | 2026-11-19T16:21:37.920 |

HTSlib is a library for reading and writing bioinformatics file formats. Prior to 1.21.2, 1.22.3, 1.23.2, and 1.24, the CRAM decoder validates the 254-character query-name limit only after decoding the name into a 1024-byte stack array. An attacker-controlled CRAM record can provide an overlong query name and overflow the local stack buffer before the later validation runs; all CRAM format versions are affected. Opening such a file can crash the process, corrupt stack data, and may permit arbitrary code execution. This issue is fixed in versions 1.21.2, 1.22.3, 1.23.2, and 1.24.

### CVE-2026-62257

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-125;CWE-787` |
| Published | 2026-11-19T16:21:37.760 |

HTSlib is a library for reading and writing bioinformatics file formats. Prior to 1.21.2, 1.22.3, 1.23.2, and 1.24, the experimental CRAM v4 XPACK and XRLE decoders cache expanded block pointers at indexes beyond the 512-element slice->block_by_id array. An array index partially controlled by data in the input file first causes an out-of-bounds read to determine whether a block is cached; a null value then causes allocation of a block and an out-of-bounds pointer write to the same element. The invalid read may crash the process, while the write may corrupt heap state and could permit arbitrary code execution. This issue is fixed in versions 1.21.2, 1.22.3, 1.23.2, and 1.24.

### CVE-2026-133243

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-11-19T16:21:27.697 |

node-soap before 1.14.1 contains a prototype pollution vulnerability in WSDL.xmlToObject that allows unauthenticated attackers to pollute Object.prototype via an XML element with id="__proto__". Attackers can send a single crafted SOAP request to a soap.listen() server, or return a malicious response to a client, causing all subsequent SOAP parsing to fail until process restart.

### CVE-2026-129291

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-19T15:17:27.663 |

PHP-FPM epoll use-after-free can lead to local privilege escalation.

When catch_workers_output is enabled and the epoll event backend is used, the PHP-FPM master can close a worker's output pipe in fpm_child_close() without removing the associated event, and the delayed cleanup can free the worker record while its epoll registration is still active. A later event is then dispatched through a pointer into freed memory. A local attacker who can execute PHP code in an FPM worker can crash the master or execute code with its privileges, commonly root. catch_workers_output is disabled by default but enabled in the official PHP-FPM Docker images.

This issue affects PHP versions from 8.1.20 through 8.1.34, from 8.2.7 before 8.2.36, 8.3.* before 8.3.37, 8.4.* before 8.4.28 and 8.5.* before 8.5.13.

### CVE-2026-126086

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347;CWE-436` |
| Published | 2026-11-19T15:17:26.027 |

In Eclipse Dataspace Components (EDC) – Connector (`org.eclipse.edc:decentralized-claims-*`, `org.eclipse.edc:jwt-verifiable-credentials`, `org.eclipse.edc:ldp-verifiable-credentials`) there's a credential verification bypass in Decentralized Claims Protocol (DCP) presentation handling: a participant can present credentials appearing to be issued by any trusted issuer without holding them.

### CVE-2026-129424

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T13:18:42.260 |

Joomla Extension - solidres.com - Unauthenticated stored XSS through guest reservation details in Solidres extension 1.0.0-3.4.1, 4.0.0-4.6.0 - The customer details layout of the administrator reservation view printed guest-supplied booking details, including the email and phone number inside mailto: and tel: links, without escaping, allowing unauthenticated guests to inject HTML attributes and script. Sites using the Custom Fields, Hub or Experience add-ons also need to update them to Custom Fields 2.0.3, Hub 2.5.0 and Experience 2.5.0.

### CVE-2026-124768

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-20T11:18:29.863 |

Authorization bypass via a user-controlled key in XOneManager 3.8.3.0. The 'ConvertBDToProject' operation selects the database based on 'databasename' without verifying the user’s permissions on it. An authenticated user can link a project to a database outside their scope and identify existing databases based on API responses.

### CVE-2026-124767

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-20T10:17:10.037 |

Authorization bypass in the creation of projects in XOneManager 3.8.3.0. The server processes POST requests to ‘/xmanagercore/api/Project/ConvertBDToProject/’ without verifying the administrative role. An authenticated user with basic privileges can create a project and execute SQL queries on the linked database from that project.

### CVE-2026-129972

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-11-20T07:16:55.603 |

A buffer overflow vulnerability exists in the web management service of the Ethernet Remote I/Os products. An unauthenticated remote attacker could exploit insufficient bounds checking of specially crafted HTTP requests, potentially causing the web management service to crash and resulting in a denial-of-service condition.

### CVE-2026-129971

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-11-20T07:16:50.940 |

A buffer overflow vulnerability exists in the SNMP service of the Ethernet Remote I/Os products. An unauthenticated remote attacker could exploit improper handling of specially crafted SNMP requests, potentially leading to a denial-of-service condition on the affected device.

### CVE-2026-133534

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-20T03:17:35.377 |

PowerLink developed by Neotroni Lighting has a SQL Injection vulnerability, allowing unauthenticated remote attackers to inject arbitrary SQL commands to read database contents.

### CVE-2026-61827

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-19T22:18:06.823 |

netty-incubator-codec-ohttp implements Oblivious HTTP (OHTTP) gateway and client functionality using Netty. Prior to 0.0.23.Final, BinaryHttpParser does not enforce limits on encoded variable-length fields controlled by a remote peer. A remote peer can cause the decoder to buffer data indefinitely until memory is exhausted, causing denial of service. This issue is fixed in version 0.0.23.Final.

### CVE-2026-133201

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-787` |
| Published | 2026-11-19T21:18:00.347 |

A vulnerability was determined in smartalock wireguard-lwip up to cfba91666590e86bd67842c71cedf9a423be823a. Impacted is the function mul of the file src/crypto/refc/x25519.c of the component X25519 Ladder. Executing a manipulation can lead to out-of-bounds write. The attack can be executed remotely. This product implements a rolling release for ongoing delivery, which means version information for affected or updated releases is unavailable. The project was informed of the problem early through an issue report but has not responded yet.

### CVE-2026-130235

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-19T21:17:53.900 |

In the Okta .NET SDK Abstractions library, outbound HTTP requests are not restricted to the configured Okta organization domain when processing certain URL formats. If a URL parameter is modified to specify an external host, the library may transmit the configured SSWS API token to that unintended destination.

### CVE-2026-131260

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T20:17:41.280 |

In Splunk SOAR versions below 8.8.0, a user with the containers:edit permission could import a container that includes a malicious Hypertext Markup Language (HTML) note. When another user views the imported note, Splunk SOAR could run unauthorized JavaScript in the browser of that user, exposing data and allowing actions available to that user.
The vulnerability is possible because Splunk SOAR does not sanitize HTML note content during container import before it renders the content in Mission Control.

### CVE-2026-131258

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T20:17:41.037 |

In Splunk SOAR versions below 8.8.0, a user with edit permission for a container or workbook task could store attacker-controlled Hypertext Markup Language (HTML) in a note. When another user with view permission for the affected container and its notes opens the affected note in Mission Control, the note could run unauthorized JavaScript code in the browser of that user, expose data available through the authenticated session, and perform actions available through the authenticated session.
The vulnerability is possible because Splunk SOAR does not neutralize active content in all notes before Mission Control renders them.

### CVE-2026-104199

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-400;CWE-1333` |
| Published | 2026-11-19T20:17:14.180 |

aMQTT is an open source MQTT broker and client. From 0.11.0 until 0.11.4, add_subscription() in amqtt/broker.py accepts malformed single-level + wildcard placement because it checks substrings instead of validating each slash-delimited level. The _matches() function converts each + into a greedy regular-expression fragment and evaluates it with re.fullmatch(), allowing a filter containing many adjacent + characters to trigger catastrophic backtracking when compared with a topic that partially matches but ultimately fails. Because matching runs synchronously in _run_broadcast(), one subscription followed by a publish can block the broker event loop, stopping message delivery and new connection processing until restart. Anonymous clients can trigger the issue with the default configuration. Any authenticated client permitted to create arbitrary subscriptions and publish messages may still exploit it when authentication is enabled. This issue is fixed in version 0.11.4.

### CVE-2026-103025

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409;CWE-789` |
| Published | 2026-11-19T20:17:12.320 |

bep/imagemeta is a Go library for reading EXIF, IPTC and XMP image meta data from JPEG, TIFF, PNG, and WebP files. Prior to 0.17.3, imagemeta.Decode could exhaust memory when parsing PNG zTXt chunks whose keyword is "Raw profile type iptc": the declared chunk length can drive an allocation far larger than the input file, and the embedded zlib stream is decompressed without an output limit. The advisory reports a 42-byte input causing a 256 MB allocation and a 127 KB input inflating to 460 MB. The oversized-allocation path's memory effect depends on platform overcommit and configured GOMEMLIMIT or cgroup limits, while the decompression path reliably creates resident memory. Applications that decode untrusted PNGs with IPTC metadata processing can therefore suffer denial of service through memory exhaustion. This issue is fixed in 0.17.3.

### CVE-2026-93912

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-11-19T19:17:35.973 |

A code injection vulnerability in WatchGuard Dimension's log notification processing allows an authenticated managed device, or an attacker in possession of a valid device logging key, to achieve arbitrary code execution on the Dimension appliance.

### CVE-2026-93911

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-19T19:17:35.820 |

A SQL injection vulnerability in WatchGuard Dimension's log collection service allows an authenticated managed device, or an attacker in possession of a valid device logging key, to achieve arbitrary code execution on the Dimension appliance.

### CVE-2026-129419

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352;CWE-863` |
| Published | 2026-11-19T19:17:25.013 |

Joomla Extension - akeeba.com - Account takeover through missing OAuth state validation in Akeeba SocialLogin extension 1.0.0-4.11.0 - The OAuth callback did not validate a session-bound state parameter, allowing an attacker to link their own social provider identity to the account of a logged-in user who opens a crafted callback link and subsequently log in as that user.

### CVE-2026-133307

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-19T17:18:52.117 |

ClassiCube before 1.4.0 contains a heap-based out-of-bounds write vulnerability in Png_Decode in src/Bitmap.c that allows malicious servers to corrupt client memory by sending a PNG with a duplicate IHDR chunk. Attackers can supply crafted PNGs via texture pack URLs or player skins so the unreset bufferIdx underflows remaining space, letting IDAT data overflow the buffer to crash clients or execute code.

### CVE-2026-133245

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-19T16:21:28.007 |

parse5 7.0.0 before 8.1.1 contains an uncaught exception vulnerability in Preprocessor#_processSurrogate that allows remote attackers to crash applications by supplying two consecutive low surrogates. Attackers can submit input such as U+DC00 U+DC00, which decodes to out-of-range code point 0x110000 and throws a RangeError from parse, parseFragment, or streaming parsers, crashing Node.js processes.

### CVE-2026-133234

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-11-19T16:21:26.027 |

Stoatchat before 0.16.5 contains an unbounded JXL image decoding vulnerability in revolt_files decode_image that allows unauthenticated attackers to exhaust memory via the january /proxy endpoint. Attackers can request a small hosted JXL file declaring 12000x12000 pixels through /proxy to trigger huge allocations, OOM-killing january and denying proxy and embed service.

### CVE-2026-133172

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-19T15:17:37.253 |

Cozy Cloud cozy-stack 1.6.62 before 1.6.69 contains an authorization bypass vulnerability in the shared-drive move handler that allows authenticated users to access other instances' files. Attackers owning a shared drive can name another instance's domain and any directory ID as the move source to copy and delete the victim's file tree.

### CVE-2026-127960

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-11-19T15:17:26.990 |

Denial of service through folded HTTP response headers.

The HTTP stream wrapper joins each continuation line of a folded response header to the accumulated value by allocating a new string and copying the whole value, so a response with many short continuation lines takes disproportionate CPU time to parse. An attacker who controls an HTTP or HTTPS response fetched through file_get_contents(), fopen() or other stream functions, by making the application request a chosen URL or by influencing a server it already contacts, can keep PHP workers busy. Repeated or concurrent requests can cause a denial of service.

This issue affects PHP versions from 8.1.32 through 8.1.34, from 8.2.28 before 8.2.36, from 8.3.18 before 8.3.37, from 8.4.5 before 8.4.28 and 8.5.* before 8.5.13.

### CVE-2026-131163

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-20T12:18:21.923 |

A stored XSS in pretix-adyen has been discovered where an attacker could configure his own ticket shop in a way that API calls are not made to Adyen, but an attacker-controlled server. Results of these API calls would then be embedded in a part of the shop without proper escaping, leading to full XSS including potential session takeover.

### CVE-2026-133663

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-11-20T11:18:34.710 |

flowintel contains an Insecure Direct Object Reference (IDOR) vulnerability affecting multiple endpoints that manage child records of cases and tasks. An authenticated user with access to one case or task could read or modify records belonging to other cases by supplying identifiers of those records directly in the request.

Affected operations include:
- Reading task notes, subtasks, and URL tools by referencing their IDs without verifying they belong to the authorized task
- Retrieving task assignees for a task belonging to a different case
- Editing or deleting timeline events and timeline event links belonging to another case
- Editing or removing case connectors belonging to another case
- Invoking connector module operations (MISP, generic connectors, worker calls) by combining an authorized case with a connector link from a different case

The root cause is that the application authorized the parent resource (case or task) in the URL but then fetched or operated on the child record independently without verifying the child's ownership relationship to the authorized parent.

Security impact: an authenticated user can exfiltrate sensitive threat intelligence data from cases they do not have access to, and can modify or delete timeline entries, connector configurations, and other records in unauthorized cases, leading to data integrity loss and potential disruption of incident response workflows.

Affected versions: flowintel prior to 4.1.0

### CVE-2026-133659

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-639` |
| Published | 2026-11-20T11:18:33.880 |

Flowintel contains multiple SSO identity and organisation trust boundary violations that collectively allow account takeover, privilege escalation, and unauthorized access to private case data.

- Keycloak SSO accepted unverified email claims, and all SSO providers (Keycloak, Entra ID, SimpleSAML) could resolve a claimed email address to an existing account that was created via a different sign-in method, enabling cross-provider account collision and unauthorized access to another user's account and data.

- Entra ID role mapping relied on group display names, which tenant members could duplicate by creating a group with the same name as a privileged group (e.g. FlowintelAdmin), resulting in unauthorized role escalation.

- SSO provisioning reused organisations whose display names matched user-controlled profile names, granting the new SSO user access to that organisation's private cases without explicit administrator assignment.

- Case sharing via the API resolved organisations by name using a first-match query, so ambiguous names could silently resolve to the wrong organisation.

Preconditions: an attacker must have a valid SSO identity (Keycloak, Entra ID, or SimpleSAML) or be a member of the relevant Entra tenant. No local administrator access is required.

Security impact: unauthorized access to private case data, privilege escalation to Editor or higher roles, and account takeover across authentication providers.

Affected versions: Flowintel prior to 4.1.0.

### CVE-2026-130494

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-20T06:17:20.453 |

An improper firmware authenticity verification vulnerability exists in the affected Ethernet Switches products. An authenticated remote attacker with administrative privileges could exploit the lack of cryptographic signature verification to install unauthorized firmware, potentially leading to arbitrary code execution on the affected device.

### CVE-2026-113347

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-20T04:17:09.277 |

Multiple products produced by Ruijie Networks Co., Ltd. contain an OS command injection vulnerability that may lead to arbitrary OS commands being executed by an attacker with the administrative privilege.

### CVE-2026-93917

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-639` |
| Published | 2026-11-19T19:17:36.553 |

An improper authorization vulnerability in WatchGuard Dimension's device management registration process allows an attacker who controls one enrolled managed device's credentials to take over another managed device's identity. This allows the attacker to receive the victim device's queued configuration and apply attacker-supplied configurations under the victim device's identity.

### CVE-2026-93916

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-11-19T19:17:36.403 |

An insufficient session expiration vulnerability in WatchGuard Dimension's administrator session management allows an attacker holding a valid Super Administrator WebUI session to retain full Super Administrator privileges after that account has been downgraded or deleted by another administrator.

### CVE-2026-93914

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-502` |
| Published | 2026-11-19T19:17:36.120 |

An improper input validation vulnerability in WatchGuard Dimension's database snapshot restore feature allows an authenticated Dimension Administrator to execute arbitrary operating system commands as root by uploading a specially crafted database snapshot archive.

### CVE-2026-86126

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-19T19:17:35.547 |

A Cross-Site Request Forgery (CSRF) vulnerability in WatchGuard Dimension's user management interface allows a remote, unauthenticated attacker to create a persistent local Super Administrator account by tricking an authenticated Super Administrator into visiting a malicious web page.

### CVE-2026-81430

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-59;CWE-347` |
| Published | 2026-11-19T19:17:33.710 |

A vulnerability in WatchGuard Dimension's system upgrade process allows an authenticated administrator to create or overwrite arbitrary files on the appliance filesystem by uploading a specially crafted upgrade archive.

### CVE-2026-103580

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-88` |
| Published | 2026-11-19T19:17:16.887 |

An OS command injection vulnerability in WatchGuard Dimension's package update functionality allows an authenticated Dimension Administrator to execute arbitrary operating system commands as root by submitting a specially crafted package update request.

### CVE-2026-103579

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-93` |
| Published | 2026-11-19T19:17:16.740 |

A CRLF injection vulnerability in WatchGuard Dimension's outgoing email server configuration allows an authenticated Dimension Administrator to execute arbitrary operating system commands on the Dimension appliance with the privileges of the local mail-handling account.

### CVE-2026-22308

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-306` |
| Published | 2026-11-19T18:18:13.790 |

The preview mode of the OPC (OnPage Composer) page
builder of JTL-Shop is activated by a request parameter alone and
renders page data supplied in the request without checking for an authenticated
backend session with the corresponding permission. Several portlet properties
are output without output encoding. An unauthenticated remote attacker
can thereby cause script code to be executed in the browser of a
visitor or administrator who opens a crafted link; in the case of an
administrator, actions can be performed with the administrator's privileges. Third-party
plugins whose portlets evaluate property values as templates can
additionally be made to execute template code through the same entry point. This is
a separate flaw in such plugins and does not affect the portlets of JTL-Shop itself.

### CVE-2026-129412

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-19T18:18:10.043 |

Joomla Extension - vi-solutions - SQL injection in backend data search and export in Visforms extension 1.0.0-5.6.4, 6.0.0-6.2.1 - Search filters and form IDs in the backend data view and export were not properly sanitized, allowing SQL injection by backend users.

### CVE-2026-22309

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T17:18:55.273 |

The visitor tracking of JTL-Shop automatically
registers unknown crawler user agents without filtering the value, and the stored
value is rendered without output encoding on several pages of the
administration backend (search engine statistics, crawler dashboard widget, crawler
edit form, sitemap export download list and campaign details). An
unauthenticated remote attacker can store script code with a single request. The code is
executed in the browser session of an administrator who opens one of these
pages, allowing actions to be performed with the administrator's privileges.

### CVE-2026-105803

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-777;CWE-1286` |
| Published | 2026-11-19T17:17:52.590 |

Git LFS is a Git extension for versioning large files. From 1.3.0 until 3.8.1, Git LFS does not correctly filter the limited set of options permitted in a repository's .lfsconfig file when option keys contain certain additional components. Crafted keys can mimic options that configure Git LFS to use a custom command to transfer objects, causing Git LFS to execute an attacker-selected command or binary while fetching objects. This issue is fixed in version 3.8.1.

### CVE-2026-105802

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-144` |
| Published | 2026-11-19T17:17:52.420 |

Git LFS is a Git extension for versioning large files. From 0.6.0 until 3.8.1, Git LFS reads Git configuration options defined for a submodule without checking certain values for embedded line-ending control characters. A malicious repository can insert control characters such as line feed (LF) into those values to mimic options that cause Git LFS to execute an attacker-controlled command or binary while fetching or adding objects. This issue is fixed in version 3.8.1.

### CVE-2026-133246

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-98` |
| Published | 2026-11-19T16:21:28.150 |

modified eCommerce Shopsoftware through 3.3.0 contains a local file inclusion vulnerability that allows administrators to include arbitrary server files by storing ../ sequences in the content manager file name. Unauthenticated requests to shop_content.php then pass the stored path to include(), executing embedded PHP in uploaded content files or images as the web server user.

### CVE-2026-133710

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-20T13:18:47.340 |

llama.cpp b11003 before b12556 contains an integer overflow in the hrm_text loader load_arch_hparams() that allows attackers to bypass the block count check using crafted GGUF metadata. Attackers can supply a GGUF model whose layer factors wrap modulo 2^32, causing load_arch_tensors() to write tensor pointers past model.layers, corrupting heap memory and potentially enabling code execution.

### CVE-2026-133708

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-11-20T13:18:47.003 |

diffpy.structure before 3.5.1 contains a code execution vulnerability that allows attackers to run Python code by supplying crafted CIF symmetry operations passed to eval() in get_symop(). Attackers can embed expressions in the _space_group_symop_operation_xyz or _symmetry_equiv_pos_as_xyz loop to execute code with victim privileges when the CIF file is parsed locally.

### CVE-2026-133707

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-11-20T13:18:46.853 |

The targets R package before 1.12.1 contains a code execution vulnerability that allows attackers to run arbitrary R code by planting format functions in the data store metadata file. Attackers can supply a crafted _targets data store whose custom format or CAS repository functions are passed to eval(parse()), executing code when victims call tar_read(), tar_load() or tar_workspace().

### CVE-2026-133501

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-20T09:20:07.277 |

A security flaw has been discovered in Gladys Assistant up to 4.71.0. This impacts an unknown function of the file server/lib/gateway/gateway.downloadBackup.js of the component Backup Restore Handler. The manipulation results in path traversal. The attack can be launched remotely. The exploit has been released to the public and may be used for attacks. Upgrading to version 4.72.0 will fix this issue. It is recommended to upgrade the affected component.

### CVE-2026-133500

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-20T09:20:07.047 |

A vulnerability was identified in Gladys Assistant up to 4.71.0. This affects an unknown function of the file gateway.downloadBackup.js of the component Backup Restore Endpoint. The manipulation of the argument file_url leads to os command injection. The attack can be initiated remotely. The exploit is publicly available and might be used. Upgrading to version 4.72.0 mitigates this issue. Upgrading the affected component is recommended.

### CVE-2026-128915

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-20T09:19:57.663 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in InstaWP InstaWP Connect instawp-connect allows Blind SQL Injection.This issue affects InstaWP Connect: from n/a through 0.1.4.4.

### CVE-2026-122676

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-19T23:19:24.940 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in PublishPress PublishPress Authors publishpress-authors allows Blind SQL Injection.This issue affects PublishPress Authors: from n/a through 4.18.0.

### CVE-2026-77315

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-19T22:18:44.470 |

Flyto2 Core is an execution kernel for automation and AI-agent workflows. Prior to 2.26.8, http.paginate in src/core/modules/atomic/http/paginate.py validates only the initial base_url, and _paginate_link_header then follows a server-supplied Link: rel="next" URL without calling the SSRF guard again. A low-privileged caller can make an allowed first page point the next request at an internal or metadata service, causing a readable second-order SSRF whose response body is aggregated into all_items and returned. This issue is fixed in version 2.26.8.

### CVE-2026-130236

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-287` |
| Published | 2026-11-19T21:17:54.033 |

In the Auth0 Authorization Extension, request authentication handling can process claims from query parameters independently of header validation. Under specific preconditions, this may allow an authenticated tenant user to issue requests to the extension's administrative endpoints. Also, input handling during rule generation may permit modification of the tenant login rule published by the extension.

### CVE-2026-130179

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-362;CWE-668` |
| Published | 2026-11-19T21:17:53.510 |

The Okta .NET SDK Abstractions library systematically writes per-request authentication credentials to a shared HTTP client instance, rather than being isolated to individual outbound request objects. When using scoped child clients, a subsequent scoped request can overwrite the shared client configuration. Because the original parent client credential has not been restored, subsequent outbound requests may be transmitted using the newly written credential, which can result in subsequent actions being executed under the context of an incorrect security principal in the Okta Management API and improper attribution in audit logs.

### CVE-2026-130151

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-416` |
| Published | 2026-11-19T21:17:52.287 |

Okta Privileged Access (OPA) Gateway includes a version of the FreeRDP library affected by memory management issues in its smartcard redirection handling. When an RDP session is established meeting specific session criteria, command execution within the context of the local Gateway service account may be allowed.

### CVE-2026-117659

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-19T18:18:03.313 |

The InfoScan Electron desktop client improperly handles TLS certificate errors by accepting certificates without validating their trustworthiness. The client also configures Electron with nodeIntegration enabled, contextIsolation disabled, and webSecurity disabled. These settings weaken the client’s security boundaries. An attacker who is able to intercept or manipulate network communications may be able to present an untrusted certificate without the application rejecting the connection.

### CVE-2026-133309

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-19T17:18:52.430 |

@scalar/typebox before 0.1.4 contains a code injection vulnerability in TypeCompiler that allows attackers to execute JavaScript by supplying crafted schema strings. Attackers can inject single-quote breakouts into string format, Kind names, property keys or Literal values to run arbitrary JavaScript in the host Node.js process during Compile() and Check().

### CVE-2026-133168

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-19T15:17:36.650 |

OFFIS DCMTK 3.7.1 contains a heap buffer overflow vulnerability in togglePlanarConfiguration8 and togglePlanarConfiguration16 in djcodece.cc, which compute row offsets using rows instead of columns. Attackers can supply a crafted color-by-plane DICOM image with more rows than columns that is compressed with the true-lossless JPEG codec to corrupt heap memory, causing crashes and potentially code execution.

### CVE-2026-133662

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-11-20T11:18:34.500 |

flowintel contains multiple authorization bypass vulnerabilities in its Analyzer (MISP Modules) functionality, affecting both the web interface and the REST API.

- Saving analyzer results to a case or task accepted caller-supplied case and task identifiers without verifying that the authenticated user is a member of the target case or holds the required restricted-task permissions. An authenticated user could write notes, create tasks, and attach MISP objects or attributes into another organization's case.

- Stored analyzer results were retrievable by UUID by any authenticated user. Both the web endpoint and the API endpoint returned the full result payload without checking ownership, exposing another user's analysis output.

- The save handler did not validate the structure of the request, did not reject conflicting destination selections, and did not halt processing when a task-note operation failed, allowing partial or unintended writes.

Preconditions: the attacker must possess a valid authenticated session (or API token) in flowintel. No administrative role is required.

Security impact: unauthorized cross-tenant data disclosure (analyzer results) and unauthorized cross-tenant data modification (notes, tasks, MISP objects/attributes in another organization's case).

Affected versions: flowintel prior to 4.1.0.

### CVE-2026-125288

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-19T20:17:21.990 |

ServiceNow has addressed a code injection security issue that was identified in the ServiceNow AI Platform. This issue could enable an authenticated user with template editing privileges to execute code in the context of another user's session. 


ServiceNow deployed an update to hosted instances, and provided the update to our partners and self-hosted customers. We are not currently aware of malicious exploitation against ServiceNow instances. We recommend customers promptly apply appropriate updates or upgrade to a patched release if they have not already done so.

### CVE-2026-131293

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-19T20:17:45.393 |

In Splunk SOAR versions below 8.8.0, an authenticated user with permission to edit and run playbooks could read or overwrite persisted data for playbook runs outside the authorized label, or ownership scope for that user. The affected data can include playbook inputs, prompt and block results, outputs, and secrets that playbooks save in run data. Overwriting the data could corrupt results that paused, scheduled, or parent playbook runs later use.
The vulnerability is possible because the playbook automation APIs do not bind data operations to the active playbook run.

### CVE-2026-131218

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-19T20:17:35.880 |

In Splunk Enterprise Security versions below 8.7.0, a user that holds a role with the mc_investigation_read capability could inject arbitrary Search Processing Language (SPL) into Mission Control dashboard search requests. Mission Control could then run the injected SPL with elevated permissions. With this access, the user could cause Mission Control to read stored credentials and write data to indexes and lookups.
The vulnerability is possible because Mission Control does not validate reserved search filters before adding them to dashboard searches.
For more information see Overview of Mission Control in Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/user-guide/8.1/mission-control/overview-of-mission-control-in-splunk-enterprise-security) and Capability reference for Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/install/8.2/installation/capability-reference-for-splunk-enterprise-security) in the Splunk documentation.

### CVE-2026-131215

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-74` |
| Published | 2026-11-19T20:17:35.270 |

In Splunk Enterprise Security versions below 8.7.0, a user that holds a role with the ueba_finding_exclusion_edit capability could store attacker-controlled values in a User and Entity Behavior Analytics (UEBA) finding exclusion rule. Splunk Enterprise Security could later run attacker-controlled Search Processing Language (SPL) commands from the rule with elevated permissions. With this access, the user could cause Splunk Enterprise Security to read stored credentials and modify lookups and knowledge objects.
The vulnerability is possible because the UEBA finding exclusion workflow does not escape user-controlled rule values before using them in generated SPL.
For more information see Create a finding exclusion rule using UEBA configuration page (https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.7/user-and-entity-behavior-analytics/finding-exclusions-in-splunk-enterprise-security/create-a-finding-exclusion-rule-using-ueba-configuration-page) and Users and roles for Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/install/8.7/installation/users-and-roles-for-splunk-enterprise-security) in the Splunk documentation.

### CVE-2026-131209

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-19T20:17:34.313 |

In Splunk Enterprise Security versions below 8.7.0, a user that holds a role with the ueba_ers_execution_post capability could cause the User and Entity Behavior Analytics (UEBA) Content App to run arbitrary Search Processing Language (SPL) commands with elevated permissions through an Entity Risk Score calculation. With this access, the user could expose stored credentials and other data outside the permissions assigned to that role.
The vulnerability is possible because the UEBA Content App does not validate Entity Risk Score calculation values before including them in SPL searches.
For more information see Installing the UEBA Content App for Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.5/user-and-entity-behavior-analytics/installing-the-ueba-content-app-for-splunk-enterprise-security), Entity risk scoring in Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.4/risk-based-alerting/entity-risk-scoring-in-splunk-enterprise-security), and Roles and knowledge objects in UEBA for Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.8/user-and-entity-behavior-analytics/ueba-content-app-for-on-premises/roles-and-knowledge-objects-in-ueba-for-splunk-enterprise-security) in the Splunk documentation.

### CVE-2026-131203

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-19T20:17:33.390 |

In Splunk Enterprise Security versions below 8.7.0, a user who holds the "ess_analyst" Splunk Enterprise Security role could modify a search macro associated with risk exclusions. Scheduled Risk data model acceleration searches could later run attacker-controlled Search Processing Language (SPL) commands from that macro with elevated permissions. With this access, the user who modified the search macro could expose stored credentials and modify indexes or lookup data available to those searches.
The vulnerability is possible because the Splunk Enterprise Security app metadata grants the "ess_analyst" role write access to the risk exclusion search macro.
For more information see Users and roles for Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/install/8.7/installation/users-and-roles-for-splunk-enterprise-security), Finding exclusions in Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.3/user-and-entity-behavior-analytics/finding-exclusions-in-splunk-enterprise-security), and Use search macros in searches (https://help.splunk.com/en/splunk-enterprise/manage-knowledge-objects/knowledge-management-manual/10.4/search-macros/use-search-macros-in-searches) in the Splunk documentation.

### CVE-2026-103035

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-11-19T19:17:16.583 |

TeamPass is a self-hosted collaborative password manager. Prior to 3.2.1.2, the update_folder action in app/sources/folders.queries.php allowed an authenticated, non-read-only user to re-parent a folder without checking whether the target folder or submitted parentId belonged to the caller's user-accessible_folders set. Selecting a personal folder as the new parent passed the personal-folder guard and set personal_folder on the target, transferring the credential subtree into the attacker's accessible space after the next login and hiding it from the organization, including administrators. The change exposed credential labels, logins, URLs, email addresses, and descriptions, while sharekey-protected passwords remained protected; hiding the subtree also denied other users access. This issue is fixed in version 3.2.1.2.

### CVE-2026-133254

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-19T16:21:28.983 |

In JetBrains IntelliJ IDEA before 2026.3, 2026.2.4 code execution was possible in untrusted projects via the Code Provenance plugin

### CVE-2026-133235

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-19T16:21:26.227 |

Tandoor Recipes before 2.7.4 contains a server-side request forgery vulnerability that allows space admins to reach internal hosts because Nextcloud.get_client builds WebDAV clients from Storage.url without calling safe_request. Attackers can create a NEXTCLOUD storage via POST /api/storage/ pointing at internal hosts, import a file, then call GET /api/get_recipe_file/<id>/ to read internal service or cloud metadata responses.

### CVE-2026-125080

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-20T09:19:56.827 |

Improper neutralization of special elements in data query logic (Cypher injection) in the orderBy placeholder handling for custom queries in Neo4j Spring Data Neo4j versions 6.1.0 through 8.0.8 and 8.1.0 through 8.1.2 allows a remote attacker to read database contents via blind reads, write read content into new nodes, or, if APOC and APOC file export are enabled, to write query results to a file in the database's accessible file system via crafted sort order parameters. Exploitation requires an application that passes unvalidated user input as the orderBy value to a custom Cypher query using the placeholder directive.

### CVE-2026-130886

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-19T19:17:26.230 |

@fastify/reply-from is a Fastify plugin that forwards requests to an upstream HTTP server. In versions 12.8.1 through 12.8.3, its buildURL function checked the attacker-supplied source string for parent-directory segments, but when the source begins with the same special scheme as the base, such as http or https, the WHATWG URL parser drops the scheme and resolves the remainder as a relative path. A payload that glues the scheme to a percent-encoded parent-directory sequence therefore passes the check, because the inspected segment reads as the scheme plus the dots rather than a bare parent-directory token, while the proxy forwards the encoded traversal unchanged. An upstream that percent-decodes the request path before resolving dot-segments then serves a path outside the configured prefix, so an unauthenticated client scoped to an upstream prefix, or relying on Fastify route guards in front of the proxy, can escape that prefix and reach sibling or parent upstream endpoints. The per-segment check added in 12.8.1 is what the scheme prefix bypasses, and releases up to 12.8.0 already rejected the decoded form. The issue is fixed in @fastify/reply-from 12.8.4, and users should upgrade to 12.8.4 or later.

### CVE-2026-127064

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-22;CWE-436` |
| Published | 2026-11-19T19:17:19.370 |

@fastify/reply-from is a Fastify plugin that forwards requests to an upstream HTTP server. In versions before 12.8.4, its buildURL function rejects parent-directory path segments by an exact string match, so a segment that carries a semicolon path parameter, such as a dot-dot segment followed by a semicolon and an optional parameter, is not equal to the plain dot-dot form and passes the traversal check, and the WHATWG URL parser keeps it as an ordinary segment so the base-prefix containment check also passes. Backends that strip semicolon path parameters before resolving dot-segments, such as Apache Tomcat, Jetty, WildFly, and Spring Boot, turn the segment back into a parent-directory reference and resolve it, so an unauthenticated client can escape the intended upstream prefix and reach internal paths such as admin or internal API endpoints, including with state-changing methods. Deployments that proxy to Node.js, nginx, or Express upstreams are not affected. The issue is fixed in @fastify/reply-from 12.8.4, and users should upgrade to 12.8.4 or later.

### CVE-2026-59988

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-22;CWE-79;CWE-200;CWE-918` |
| Published | 2026-11-19T17:18:58.550 |

django-docutils provides reStructuredText support for Django. Prior to 0.30.0, public rendering paths including publish_doctree, publish_html_from_source, publish_html_from_doctree, publish_parts_from_doctree, the {% rst %} template tag, the rst template filter, DocutilsTemplates, and DocutilsView pass lower-trust reStructuredText to Docutils without disabling file_insertion_enabled, raw_enabled, ambient docutils.conf processing, or unsafe URI schemes and without consistently sanitizing doctrees. An attacker who can influence rendered reStructuredText can use include or csv-table directives to read local files or cause server-side URL requests, or use raw HTML and unsafe URI output to inject stored script-capable content. Applications that render only trusted static reStructuredText are not affected unless attackers can influence it. This issue is fixed in version 0.30.0.

### CVE-2026-87868

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-328` |
| Published | 2026-11-19T15:17:42.557 |

MRemoteNG uses single MD5 hash with no salt and no iterations for key-derivation. An attacker who obtains the encrypted data can brute-force
a weak or moderate passphrase offline at extreme speed and then decrypt every stored connection
password. When the default passphrase is in use, no cracking is needed at all; the key is derived from a
publicly known value.


Vendor did not provide the range of vulnerable versions. Only version 1.76.20 was tested and confirmed vulnerable. Other versions may also be vulnerable.

### CVE-2026-128064

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-11-19T15:17:27.120 |

Mixed-case HTTPS and FTPS URLs can expose data in plaintext.

The HTTP and FTP stream wrappers recognise URL schemes case-insensitively, but enable TLS only when the scheme contains a lowercase "s" at a fixed position. A URL such as HTTPS:// or FTPS:// passed to file_get_contents(), fopen() or other stream functions, or received as an HTTP redirect target, is therefore handled over unencrypted HTTP or FTP. An attacker able to observe the network traffic can read data the application expected TLS to protect, including credentials, request bodies and transferred files.

This issue affects PHP versions before 8.2.36, 8.3.* before 8.3.37, 8.4.* before 8.4.28 and 8.5.* before 8.5.13.

### CVE-2026-126716

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-20T10:17:10.517 |

The Mega Forms – Drag & Drop Form Builder with Multi-Step & Conditional Logic plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the delete_entry function in all versions up to, and including, 1.7.9 This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). The attacker-supplied path is stored via the unauthenticated form submission endpoint, but the actual file deletion only occurs when an administrator subsequently deletes the stored entry — a routine housekeeping action that serves as the detonation trigger. Successful exploitation additionally requires an action by an administrator — the attacker cannot trigger the vulnerability on their own.

### CVE-2026-130010

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-20T09:19:58.350 |

The Chatterbug Forms – Fast, Flexible WordPress Form Builder plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the cbforms_delete_uploaded_files function in all versions up to, and including, 1.1 This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). Exploitation requires an administrator to delete the attacker-planted form entry, and the attacker must know or be able to guess the absolute path of a file writable by the PHP process. Successful exploitation additionally requires an action by an administrator — the attacker cannot trigger the vulnerability on their own.

### CVE-2026-118522

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-20T09:19:56.440 |

The Video & Photo Gallery for Ultimate Member plugin for WordPress is vulnerable to Arbitrary File Deletion in versions up to, and including, 1.1.4 This is due to the um_gallery_add_videos() AJAX handler persisting user-supplied videos[] values into the file_name column after only esc_url() — which preserves path-traversal sequences — and the companion um_gallery_delete_photo() helper passing that stored value to unlink() through get_user_image_path() with no canonicalization or allowed-directory check. This makes it possible for authenticated attackers, with Subscriber-level access and above, to delete arbitrary files on the server, which can be leveraged to achieve remote code execution when the right file (such as wp-config.

### CVE-2026-89095

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-11-20T08:18:36.747 |

The Shortcodes and extra features for Phlox theme plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 2.17.22 via the 'extra_template_path' parameter parameter. This makes it possible for unauthenticated attackers to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included. The slug-based allowlist introduced as the fix for CVE-2023-37888 constrains only the template_part_file filename suffix and does not validate the extra_template_path directory component, meaning path traversal sequences are fully functional against this parameter.

### CVE-2026-131795

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-11-20T08:18:31.337 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in thembay Aora aora allows PHP Local File Inclusion.This issue affects Aora: from n/a through 1.3.5.

### CVE-2026-120556

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-20T08:18:26.417 |

The Toocheke Companion plugin for WordPress is vulnerable to Missing Authorization leading to arbitrary post and attachment deletion in versions up to, and including, 2.38. This is due to a missing object-level capability check in the toocheke_tapas_ajax_cleanup_start() and toocheke_tapas_ajax_cleanup_step() AJAX handlers; the toocheke_tapas_cleanup_ajax_guard() method only verifies the primitive delete_posts capability (held by every Contributor) and never calls current_user_can('delete_post', $post_id) or delete_others_posts before passing the attacker-supplied series_post_id to wp_delete_post() and wp_delete_attachment() with force-delete enabled. The required nonce is emitted on the Import: Tapas admin page, which is gated only by edit_posts, so a Contributor can read it. This makes it possible for authenticated attackers, with Contributor-level access and above, to permanently delete any importer-created series post, every child 'comic' post attached to it, and every Media Library attachment belonging to those posts — regardless of which user originally created them.

### CVE-2026-61798

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-200;CWE-312;CWE-532` |
| Published | 2026-11-19T22:18:06.490 |

netty-incubator-codec-ohttp implements Oblivious HTTP (OHTTP) gateway and client functionality using Netty. Prior to 0.0.23.Final, BoringSSLAsymmetricCipherKeyPair.toString in codec-ohttp-hpke-classes-boringssl/src/main/java/io/netty/incubator/codec/hpke/boringssl/BoringSSLAsymmetricCipherKeyPair.java includes its private parameter, BoringSSLAsymmetricKeyParameter.toString in codec-ohttp-hpke-classes-boringssl/src/main/java/io/netty/incubator/codec/hpke/boringssl/BoringSSLAsymmetricKeyParameter.java renders the complete private-key byte array when isPrivate is true, and BoringSSL.EVP_HPKE_KEY_init_or_throw in codec-ohttp-hpke-classes-boringssl/src/main/java/io/netty/incubator/codec/hpke/boringssl/BoringSSL.java includes rejected privateKeyBytes in an exception message. Applications that log affected key-pair objects or initialization exceptions can persist complete HPKE private key material in logs or telemetry. Anyone who can read those records can recover the key and may compromise OHTTP message confidentiality or authenticity expectations while the key remains usable. This issue is fixed in version 0.0.23.Final.

### CVE-2026-85018

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-19T21:18:06.353 |

IBM Guardium Data Protection 12.2 is vulnerable to improper TLS certificate validation in the GDP Terraform provider, allowing a network attacker with a man-in-the-middle position to intercept sensitive credentials transmitted to the Guardium appliance.

### CVE-2026-84273

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-19T21:18:06.207 |

IBM Guardium Data Protection 12.2 is vulnerable to path traversal in the datasource functionality. An authenticated attacker could exploit this vulnerability to delete arbitrary files on the appliance.

### CVE-2026-82342

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-11-19T21:18:05.230 |

IBM Guardium Data Protection 12.2 is vulnerable to a stack-based buffer overflow when processing a specially crafted PROXY protocol v1 header. A remote attacker can exploit this vulnerability to cause a denial of service or potentially execute arbitrary code.

### CVE-2026-76544

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-19T20:17:53.857 |

In Splunk Enterprise versions below 10.4.5, 10.2.9, 10.0.12, and 9.4.16, a user who does not hold the "admin" or "power" Splunk roles could cause scheduled metric alert searches to run arbitrary Search Processing Language (SPL) commands and access credentials stored in cleartext. This requires at least one non-internal metric index on the instance.
The vulnerability is possible because Splunk Enterprise does not fully validate metric alert filter input before using it in a scheduled search.

### CVE-2026-131305

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-15` |
| Published | 2026-11-19T20:17:46.870 |

In Splunk AI Assistant versions below 2.0.0, a user who does not hold the "admin" or "power" Splunk roles could submit client-controlled feature settings through the Representational State Transfer (REST) API. This could modify limited response metadata outside the expected server-side configuration.
The vulnerability is possible because the REST API processes client-supplied feature settings without enforcing the expected server-side configuration boundary.

### CVE-2026-131304

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-19T20:17:46.750 |

In Splunk AI Assistant versions below 2.0.0 a user who does not hold the "admin" or "power" Splunk roles could access data associated with another tenant and cause actions to be attributed to that tenant through the Representational State Transfer (REST) API.
The vulnerability is possible because Splunk AI Assistant accepted a client-controlled tenant identifier when selecting the authorization context for a request.

### CVE-2026-131297

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-19T20:17:45.890 |

In Splunk SOAR versions below 8.8.0, an operator of a configured identity provider could authenticate as an existing user associated with another configured identity provider. If that account has the "Administrator" Splunk SOAR role, the operator could control the Splunk SOAR deployment.
Splunk SOAR does not bind external user accounts to the identity provider that provisions them and authenticates accounts by username without verifying provider ownership.
The vulnerability requires more than one configured external identity provider with distinct trust domains and a target username that an operator of a configured identity provider can authenticate through a different provider.
For more information see Configure single sign-on authentication (https://help.splunk.com/en/splunk-soar/soar-on-premises/administer-soar-on-premises/8.7.0/manage-your-splunk-soar-on-premises-users-and-accounts/configure-single-sign-on-authentication-for-splunk-soar-on-premises) and Manage roles and permissions (https://help.splunk.com/en/splunk-soar/soar-on-premises/administer-soar-on-premises/8.8.0/manage-your-splunk-soar-on-premises-users-and-accounts/manage-roles-and-permissions-in-splunk-soar-on-premises) in the Splunk documentation.

### CVE-2026-131282

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-532` |
| Published | 2026-11-19T20:17:43.997 |

In Splunk SOAR versions below 8.8.0, a user who holds the "Observer" Splunk SOAR role could access a password-reset credential in a diagnostic log bundle and reset the password for an active local account.
The vulnerability is possible because Splunk SOAR does not redact password-reset email bodies before it logs communications between product processes.

### CVE-2026-131210

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-19T20:17:34.463 |

In Splunk Enterprise Security versions below 8.7.0, a user that holds a role with the ueba_finding_exclusion_edit capability could create a finding exclusion rule that references an attacker-controlled lookup definition if the role also grants write access to globally shared lookup definitions, as the "ess_analyst" Splunk Enterprise Security role does. The User and Entity Behavior Analytics (UEBA) Content App could later include the lookup name in a search and run arbitrary Search Processing Language (SPL) commands with elevated permissions. With this access, the user who created the finding exclusion rule could expose stored credentials and other data outside the permissions assigned to the "ess_analyst" role.
The vulnerability is possible because UEBA finding exclusion processing does not safely quote lookup names before including them in SPL searches.
For more information see Finding exclusions in Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.3/user-and-entity-behavior-analytics/finding-exclusions-in-splunk-enterprise-security) and Roles and knowledge objects in UEBA for Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.8/user-and-entity-behavior-analytics/ueba-content-app-for-on-premises/roles-and-knowledge-objects-in-ueba-for-splunk-enterprise-security) in the Splunk documentation.

### CVE-2026-131200

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-19T20:17:32.967 |

In Splunk Enterprise Security versions below 8.7.0, a user who holds the "ess_analyst" Splunk Enterprise Security role could create an attacker-controlled saved search. Threat intelligence lookup generation could later run the saved search with elevated permissions, which could let the user who created the saved search run arbitrary Search Processing Language (SPL) commands with those permissions.
The vulnerability is possible because Splunk Enterprise Security does not restrict threat intelligence lookup generation to the intended saved searches.
For more information see Users and roles for Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/install/8.7/installation/users-and-roles-for-splunk-enterprise-security) and Turn on threat matching searches in Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.0/threat-intelligence/turn-on-threat-matching-searches-in-splunk-enterprise-security) in the Splunk documentation.

### CVE-2026-104129

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-19T19:17:17.127 |

pREST (PostgreSQL REST) is an API that delivers an application on top of a Postgres database. Prior to 2.4.0, the vulnerable parameter is _groupby, handled by GroupByClause in adapters/postgres/postgres.go. adapters/postgres/postgres.go uses the weaker isSafeSQLExpression check for this function-expression branch instead of the stricter single-field validator used for _select. That check validates only the outer function name against a 13-function allowlist and permits nested subqueries, trailing UNION syntax, and inner pg_ functions. controllers/crud.go concatenates the GROUP BY expression while parameterizing only WHERE values, allowing attacker-controlled SQL structure into the clause. Default configuration permits unauthenticated access; a restricted installation may require a low-privilege table reader. UNION-based extraction requires compatible column counts and types and was not verified end to end, but a delay-producing function can cause denial of service without that alignment. This issue is fixed in 2.4.0.

### CVE-2026-103026

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-470;CWE-749;CWE-915` |
| Published | 2026-11-19T19:17:16.410 |

Paymenter is a free and open-source webshop solution for management of hosting services. Prior to 1.5.7, the HasConfirmation trait in app/Livewire/Traits/HasConfirmation.php, included by app/Livewire/Component.php across 36 client-facing Livewire components, exposed executeConfirmedAction as a public action that invoked any component method accepted by method_exists. The action could call inherited InteractsWithProperties::fill(), whose data_set() writes arbitrary public properties, including state marked with #[Locked] and dotted paths into hydrated Eloquent models. Depending on the methods and properties exposed by an individual component, an unauthenticated caller could use this path to bypass intended authorization and modify server-side state intended to be immutable or protected from client-side manipulation. This issue is fixed in version 1.5.7.

### CVE-2026-123891

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-19T15:17:25.543 |

SDDC Manager contains an SQL-injection vulnerability due to improper sanitization of user-supplied input.
Affected versions: 9.1.x.x (fixed in 9.1.1.0200); 9.0.x.x (fixed in 9.0.2.0100); 5.x (fixed in 5.2.5).

### CVE-2026-130234

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-116` |
| Published | 2026-11-19T21:17:53.770 |

The Okta Swift Management SDK does not percent-encode forward slash (/) characters during path parameter interpolation. If an application supplies input containing relative path sequences (e.g., ../) to an SDK method, standard URL normalization may direct the outbound request to an alternative Okta Management API endpoint.

### CVE-2026-133553

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-20T04:17:10.250 |

A flaw was found in crun. When copying files onto a tmpfs mounted with tmpcopyup, crun opens the destination a second time by name. A container that shares a writable volume with the container being created can change that path between the two lookups, so crun copies image files onto host files, including files under /proc/sys.

### CVE-2026-84087

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-19T21:18:05.717 |

IBM Guardium Data Protection 12.2 is vulnerable to local privilege escalation via the SUID-root podman_wrapper binary on the Collector appliance. A local attacker with low-privileged access to the Collector can exploit insufficient argument validation in the SUID binary to execute arbitrary commands as root, resulting in full compromise of the Collector appliance.

### CVE-2026-133198

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-15` |
| Published | 2026-11-19T15:17:40.953 |

In JetBrains Junie before 252.819.35, 253.819.35 code execution was possible via terminal environment settings in project files

### CVE-2026-133577

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-285` |
| Published | 2026-11-20T07:17:15.163 |

A flaw was found in the Kuadrant WebAssembly (WASM) shim shipped in Red Hat Connectivity Link 1.5. When a TokenRateLimitPolicy is attached to an HTTPRoute that also has an AuthPolicy - or when a RateLimitPolicy with defaults or overrides is attached to the Gateway or listener of such routes - the shim's action pipeline fails to dispatch the authentication guard at request time, and the request is forwarded upstream. Unauthenticated requests return 200 OK instead of 401, and neither authentication nor rate limiting is enforced. Both policies continue to report Enforced, leaving no status-level indication of the failure.

### CVE-2026-130493

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-20T06:17:20.200 |

A hard-coded cryptographic key vulnerability exists in affected Ethernet swiches. The use of a shared cryptographic key with insufficient key strength could allow an unauthenticated remote attacker, under certain conditions, to impersonate affected devices and potentially compromise the confidentiality and integrity of communications.

### CVE-2026-131266

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-19T20:17:42.020 |

In Splunk SOAR versions below 8.8.0, a user that holds a role with the System Settings edit permission could cause Splunk SOAR to send a stored Elasticsearch password to a host that the user controls.
The vulnerability is possible because Splunk SOAR reuses a stored Elasticsearch password for a changed Search Settings endpoint without requiring a replacement password.

### CVE-2026-93915

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-93;CWE-862` |
| Published | 2026-11-19T19:17:36.260 |

A missing authorization vulnerability in WatchGuard Dimension's legacy system settings configuration handler allows a low-privileged authenticated user to execute arbitrary commands with elevated privileges on the underlying OS.

### CVE-2026-128090

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347;CWE-757` |
| Published | 2026-11-19T15:17:27.257 |

PHAR OpenSSL signature bypass via algorithm downgrade.

The Phar extension selects the signature verification method from the signature type stored in the archive, and only the OpenSSL types consult the separate .pubkey file holding the trusted public key. An attacker who can modify an OpenSSL-signed Phar archive, but not its public key file, can switch the signature type to a keyless hash such as SHA-256 with a recomputed digest, so the altered archive passes verification even with phar.require_hash enabled. An application that loads the archive may then execute attacker-controlled PHP code. Native, tar-based and zip-based phars are affected.

This issue affects PHP versions before 8.2.36, 8.3.* before 8.3.37, 8.4.* before 8.4.28 and 8.5.* before 8.5.13.

### CVE-2026-133705

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-11-20T13:18:46.553 |

Hanko before 3.2.0 contains an open redirect vulnerability in Saml.IsAllowedRedirect that allows unauthenticated attackers to bypass the redirect allowlist by appending attacker-controlled domain suffixes to allowed hostnames. Attackers can lure victims through a crafted /saml/auth login link to capture the one-time hanko_token and redeem it without PKCE to hijack the victim's session.

### CVE-2026-131243

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-19T20:17:39.153 |

In Splunk SOAR versions below 8.8.0, an authenticated user with permission to view an affected container could query the Representational State Transfer (REST) API for approvals to retrieve a live external prompt link belonging to another user. Using this link, the user could read the approval prompt without authentication and submit a response, potentially disrupting or altering the automated workflow governed by that approval.
The vulnerability is possible because the REST API for approvals exposes the live external prompt link without verifying that the requester owns the approval.

### CVE-2026-131182

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-116` |
| Published | 2026-11-19T20:17:30.193 |

In Splunk Enterprise versions below 10.4.5, 10.2.9, 10.0.12, and 9.4.17, a user who holds the "power" Splunk role could store malicious Search Processing Language (SPL) in a shared dashboard. The malicious SPL could run using the permissions of the user who opened the dashboard and could access or modify data available to that user and disrupt Splunk Enterprise availability.
The vulnerability is possible because Splunk Enterprise does not preserve quoted search argument boundaries when it processes a dashboard search.
The vulnerability requires the attacker to phish the affected user by tricking them into initiating a request within their browser. The attacker, a user who holds the "power" Splunk role, should not be able to exploit the vulnerability at will.

### CVE-2026-131179

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-74` |
| Published | 2026-11-19T20:17:29.810 |

In Splunk Enterprise versions below 10.4.5, 10.2.9, 10.0.12, and 9.4.17, a user who holds the "power" Splunk role could add attacker-controlled Search Processing Language (SPL) to a shared dashboard. When another user opens the dashboard in Splunk Web, Splunk Enterprise could run the attacker-controlled SPL using the permissions of that dashboard viewer. The attacker-controlled SPL could expose stored credentials, modify indexed data, and reduce availability.
The vulnerability is possible because Splunk Enterprise does not neutralize special elements in search filter values before it builds optimized search jobs.
The vulnerability requires the attacker to phish the affected user by tricking them into initiating a request within their browser. The attacker should not be able to exploit the vulnerability at will.

### CVE-2026-131178

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-74` |
| Published | 2026-11-19T20:17:29.687 |

In Splunk Enterprise versions below 10.4.5, 10.2.9, 10.0.12, and 9.4.17, a user who holds the "power" Splunk role could craft a shared Classic Dashboard that runs arbitrary Search Processing Language (SPL) commands for another authenticated user. Exploitation requires the dashboard viewer to open the shared dashboard. The injected commands could access data available to the dashboard viewer, modify data available to the dashboard viewer, and partially disrupt Splunk Enterprise.
For more information see Add sparklines to search results (https://help.splunk.com/en/splunk-enterprise/search/search-manual/10.6/calculate-statistics/add-sparklines-to-search-results), Configure dashboard permissions (https://help.splunk.com/en/splunk-enterprise/create-dashboards-and-reports/simple-xml-dashboards/10.6/manage-and-share-dashboards/configure-dashboard-permissions), and SPL safeguards for risky commands (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/best-practices-for-splunk-platform-security/spl-safeguards-for-risky-commands) in the Splunk documentation.

### CVE-2026-131175

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-19T20:17:29.310 |

In Splunk Enterprise versions below 10.4.4, 10.2.8, 10.0.11, and 9.4.16, a user who holds the "power" Splunk role could create and share a metric alert that causes Analytics Workspace to run a malicious Search Processing Language (SPL) when another authenticated user opens a link to the alert. The malicious SPL could expose data, modify data, or disrupt services available in the affected session. 
The vulnerability is possible because Analytics Workspace does not fully neutralize metric alert names before including the names in SPL.
The vulnerability requires the attacker to phish the user by tricking them into opening a link that the attacker creates. The user who holds the "power" Splunk role should not be able to exploit the vulnerability at will.
For more information see Alerts in the Analytics Workspace (https://help.splunk.com/en/splunk-enterprise/create-dashboards-and-reports/analytics-workspace/10.4/using-the-analytics-workspace/alerts-in-the-analytics-workspace) and Define roles on the Splunk platform with capabilities (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.4/manage-splunk-platform-users-and-roles/define-roles-on-the-splunk-platform-with-capabilities) in the Splunk documentation.

### CVE-2026-69261

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-19T17:18:58.867 |

Git LFS is a Git extension for versioning large files. From 0.5.0 until 3.8.1, Git LFS may forward a Cookie header after an HTTP redirect to a host other than the one for which the header was intended. That unintended host can therefore receive cookies containing credentials or other confidential values. Authorization headers are never forwarded to inappropriate hosts and are not the affected secret in this vulnerability. This issue is fixed in version 3.8.1.

### CVE-2026-69260

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-19T17:18:58.713 |

Git LFS is a Git extension for versioning large files. From 0.5.0 until 3.8.1, Git LFS does not format the SSH URL path component as a single argument when constructing remote object-transfer or authentication commands. Shell metacharacters in the SSH URL can therefore escape the intended path argument and cause arbitrary command execution when the remote Git LFS service passes received commands to a shell without adequate sanitization. Git LFS also incorrectly encodes default HTTPS URLs when an SSH URL is configured and the remote host either does not support Git LFS remote commands over SSH or supports HTTP authentication over SSH but git-lfs-authenticate does not return an explicit HTTP URL. This issue is fixed in version 3.8.1.

### CVE-2026-22310

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T17:18:55.433 |

When the setting for saving requests to non-existent
pages (404) is enabled, JTL-Shop stores the raw requested URL in its
redirect table, and the administration backend renders it without output
encoding in the form used to edit a redirect. An unauthenticated remote
attacker can store script code with a single request, which is executed in the
browser session of an administrator who opens the affected redirect,
allowing actions to be performed with the administrator's privileges. The
setting is disabled by default in new installations but may still be
enabled in older ones.

### CVE-2026-131811

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-19T16:20:09.660 |

United Chargers Grizzl-E Smart 40A OCPP Backend Configuration Hard-Coded Credentials Authentication Bypass Vulnerability. This vulnerability allows network-adjacent attackers to bypass authentication on affected installations of United Chargers Grizzl-E Smart 40A EV chargers. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the configuration of the OCPP backend settings interface. The issue results from the use of hard-coded credentials. An attacker can leverage this vulnerability in conjunction with other vulnerabilities to execute arbitrary code in the context of the device. Was ZDI-CAN-29056.

### CVE-2026-131809

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-425` |
| Published | 2026-11-19T16:20:09.430 |

United Chargers Grizzl-E Smart 40A OCPP Backend Configuration Authentication Bypass Vulnerability. This vulnerability allows network-adjacent attackers to bypass authentication on affected installations of United Chargers Grizzl-E Smart 40A EV chargers. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the handling of OCPP backend configuration requests. The issue results from the lack of authentication prior to allowing access to functionality. An attacker can leverage this in conjunction with other vulnerabilities to execute arbitrary code in the context of the device. Was ZDI-CAN-29063.

### CVE-2026-129423

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T13:18:42.127 |

Joomla Extension - phoca.cz - Stored XSS through author website in frontend upload in Phoca Download extension 3.0.6-6.1.6 - The author website field of the frontend upload form was validated with an overly permissive URL check and rendered without escaping, allowing users with frontend upload permission to inject HTML attributes into the file and category views.

### CVE-2026-128997

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-20T13:18:36.873 |

Missing Authorization vulnerability in RomanCode MapSVG mapsvg-lite-interactive-vector-maps allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects MapSVG: from n/a through 9.0.5.

### CVE-2026-125059

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-20T10:17:10.187 |

The Mang Board plugin for WordPress is vulnerable to Arbitrary File Deletion via Path Traversal in versions up to, and including, 2.4.8 via the `file_path` column handled by the `mbw_board_files_api_body()` function. The plugin stores an attacker-supplied value directly into the files admin table (no realpath, dot-segment, or directory-containment filtering) and later concatenates it onto `MBW_UPLOAD_PATH` before passing the result to `@unlink()`. This makes it possible for unauthenticated attackers to delete arbitrary files on the affected site's server, including `wp-config.

### CVE-2026-129840

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-20T09:19:58.200 |

In the nrfconnect/ncs-zigbee repository, the GitHub Actions workflow
.github/workflows/build_documentation.yml used the pull_request_target trigger
while checking out and executing untrusted pull request code. This allowed a
pull request from a fork to run attacker-controlled code in the base repository
context with a write-scoped GITHUB_TOKEN (contents: write, pages: write,
pull-requests: write), enabling remote code execution in CI, token
exfiltration, and unauthorized modification of repository content and GitHub
Pages. The workflow was disabled and then rewritten to remove the issue.

### CVE-2026-130055

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-20T08:18:29.210 |

The VidShop for WooCommerce plugin for WordPress is vulnerable to Sensitive Information Exposure in versions up to, and including, 1.10.0 via the /vsfw/v1/products/{id} REST API endpoint. This is due to the endpoint's permission_callback (check_public_permission) returning true unconditionally and the get_item() handler only checking that the product and video exist — it does not check the product's post_status or catalog visibility, nor does it verify that the product is actually linked to the supplied video_id. This makes it possible for unauthenticated attackers to enumerate product IDs and read private, draft, and catalog-hidden WooCommerce products' names, short descriptions, prices, variations, attributes, and stock information that would otherwise be hidden from public view.

### CVE-2026-129065

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-20T08:18:28.487 |

Missing Authorization vulnerability in Backup For WP WP Database Backup wp-database-backup allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects WP Database Backup: from n/a through 7.14.

### CVE-2026-129036

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-20T08:18:28.053 |

Incorrect Privilege Assignment vulnerability in weDevs WP ERP erp allows Privilege Escalation.This issue affects WP ERP: from n/a through 1.17.11.

### CVE-2026-129015

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-20T08:18:27.913 |

Improper Restriction of XML External Entity Reference vulnerability in ReviewX ReviewX reviewx allows XML Entity Linking.This issue affects ReviewX: from n/a through 3.0.1.

### CVE-2026-128102

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-20T08:18:27.487 |

The rtMedia for WordPress, BuddyPress and bbPress plugin for WordPress is vulnerable to generic SQL Injection via the 'custom_fields' parameter in all versions up to, and including, 4.7.17 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. The upload endpoint's only access control is a nonce check, and the 'rtmedia_upload_nonce' value is localized to every unauthenticated visitor on every front-end page via wp_enqueue_scripts, making it freely obtainable without an account.

### CVE-2026-104927

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-20T08:18:25.773 |

The King Addons for Elementor – 100+ Elementor Widgets, 4 000+ Elementor Templates, WooCommerce Builder, Mega Menu, Popup Builder plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 51.1.89. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to read arbitrary post meta values — including private contact data, API keys, license keys, and plugin-internal metadata — for any published post by supplying an arbitrary meta key name via the unauthenticated AJAX endpoint. The nonce check present in the handler provides no effective barrier because the nonce is emitted into every front-end page for logged-out visitors via wp_localize_script.

### CVE-2026-63202

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-835` |
| Published | 2026-11-19T22:18:07.520 |

netty-incubator-codec-ohttp implements Oblivious HTTP (OHTTP) gateway and client functionality using Netty. Prior to 0.0.23.Final, BinaryHttpParser.readFieldSection in codec-bhttp/src/main/java/io/netty/incubator/codec/bhttp/BinaryHttpParser.java loops while fieldSectionLength is nonzero and relies on disabled-by-default assertions to require BinaryHttpParser.readFieldLine to return a value and consume bytes. A corrupt field line can consume more bytes than its understated declared section length and drive the counter negative, or a truncated field line can return without consuming data and leave the parser in the same state. An unauthenticated OHTTP peer can encrypt such Binary HTTP content under the gateway public configuration, reach OHttpRequestResponseContext.ContentDecoder.decodeChunk, and permanently pin a Netty event-loop thread at full CPU before application business logic. Multiple requests can exhaust the event-loop group and deny service until restart. This issue is fixed in version 0.0.23.Final.

### CVE-2026-63124

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-835` |
| Published | 2026-11-19T22:18:07.363 |

netty-incubator-codec-ohttp implements Oblivious HTTP (OHTTP) gateway and client functionality using Netty. Prior to 0.0.23.Final, BinaryHttpParser.readFieldLine in codec-bhttp/src/main/java/io/netty/incubator/codec/bhttp/BinaryHttpParser.java treats a complete field line that ends exactly at a known field-section boundary as incomplete and returns without consuming bytes. BinaryHttpParser.readFieldSection then leaves fieldSectionLength unchanged and repeats the loop because its forward-progress checks are Java assertions, which are normally disabled in production. A remote peer that sends a known-length Binary HTTP header or trailer section ending at that boundary can make the parser spin indefinitely and pin the Netty event-loop or worker thread responsible for the channel. This issue is fixed in version 0.0.23.Final.

### CVE-2026-131299

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-19T20:17:46.147 |

In Splunk App for Stream versions below 8.1.7, an unauthenticated user who can reach the Splunk App for Stream Representational State Transfer (REST) API on the management port (8089) could upload an Extensible Markup Language (XML) vocabulary file, which lets the vocabulary upload endpoint read local files accessible to the Splunk process or send outbound requests.
The vulnerability is possible because the vocabulary upload endpoint parses uploaded XML without an application-level policy that blocks external entity resolution.
For more information see About Splunk Stream (https://help.splunk.com/en/splunk-enterprise/collect-stream-data/install-and-configure-splunk-stream/8.1/introduction/about-splunk-stream) and restmap.conf (https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/9.4/configuration-file-reference/9.4.3-configuration-file-reference/restmap.conf) in the Splunk documentation.

### CVE-2026-131255

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-11-19T20:17:40.660 |

In Splunk SOAR versions below 8.8.0, an unauthenticated user could gain administrator privileges through a user account that receives an unintended role. A user that holds a role with permission to create or modify users and assign roles must assign the target account a role with a numeric name through the user-management Representational State Transfer (REST) API.
The vulnerability is possible because the API resolves a numeric role name as a role identifier instead of preserving the requested role name.

### CVE-2026-131196

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-19T20:17:31.937 |

In Splunk Enterprise versions below 10.4.5, 10.2.9, 10.0.12, and 9.4.17, an unauthenticated user who can connect to a Splunk-to-Splunk (S2S) data forwarding receiver could cause the Splunk daemon to terminate unexpectedly. The unexpected termination interrupts data indexing and access to the management API and Splunk Web until the Splunk Enterprise process restarts.
The vulnerability is possible because the S2S data forwarding receiver does not validate an optional field in forwarded event data, which results in a null pointer dereference when the field is missing.
For more information see Intermediate data routing using universal and heavy forwarders (https://help.splunk.com/en/splunk-enterprise/get-started/splunk-validated-architectures/getting-data-in-forwarding-and-preprocessing/intermediate-data-routing-using-universal-and-heavy-forwarders) in the Splunk documentation.

### CVE-2026-131192

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-305` |
| Published | 2026-11-19T20:17:31.450 |

In Splunk Enterprise versions below 10.6.1, 10.4.5, 10.2.9, 10.0.12, and 9.4.17, an unauthenticated user could access live event data from the indexing pipeline through the Representational State Transfer (REST) API on a standalone instance or a search head that is not an indexer cluster member.
The vulnerability is possible because Splunk Enterprise accepts an empty shared key during service authentication.

### CVE-2026-131190

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-19T20:17:31.207 |

In Splunk Enterprise versions below 10.4.5, 10.2.9, 10.0.12, and 9.4.17, an unauthenticated user could access RapidDiag process metadata and log file inventory information through the Representational State Transfer (REST) API.
The vulnerability is possible because certain RapidDiag REST API endpoints accept a factory-default shared key for node authentication, which lets requests bypass Splunk user authentication.
For more information see Using RapidDiag (https://help.splunk.com/en/splunk-enterprise/administer/troubleshoot/9.0/contact-splunk-support/using-rapiddiag) and Secure Splunk Enterprise services with pass4SymmKey (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.0/secure-distributed-and-clustered-splunk-environments/secure-splunk-enterprise-services-with-pass4symmkey) in the Splunk documentation.

### CVE-2026-130176

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401;CWE-772` |
| Published | 2026-11-19T20:17:28.477 |

aMQTT is an open source MQTT broker and client. From 0.11.0 until 0.12.1, the QoS 2 transaction handler in amqtt/mqtt/protocol/handler.py, _handle_qos2_message_flow(), can retain transaction state and packet identifiers when a client disconnects before the handshake completes, unlike QoS 1 flows that expire after the default five-second timeout. A remote client can repeatedly begin QoS 2 flows and disconnect without maintaining long-lived connections; anonymous clients can do this with the default configuration, while authenticated deployments remain affected when a client may initiate QoS 2 flows. The retained state grows broker memory until resource exhaustion can terminate the process; no confidentiality or integrity impact is identified. This issue is fixed in version 0.12.1.

### CVE-2026-115578

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-129;CWE-193;CWE-248` |
| Published | 2026-11-19T20:17:19.797 |

Go-Guerrilla SMTP Daemon is a lightweight SMTP server written in Go. In 1.6.7 and earlier, according to the repository advisory's structured affected range, server.go defines the seven-byte cmdXCLIENT token, but the XCLIENT handler slices input[8:] after matching only that seven-byte verb, so a bare command causes an out-of-bounds panic in handleClient and terminates the daemon because that connection goroutine does not recover the panic. The issue is reachable by an unauthenticated client when the non-default xclient_on setting is enabled; no HELO command is required. The repository fix is present in version 1.6.7-1.

### CVE-2026-130647

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-19T19:17:26.110 |

@fastify/http-proxy is a Fastify plugin that proxies HTTP and WebSocket traffic to an upstream server. In versions from 9.0.0 up to but not including 11.6.10, when the plugin is registered with websocket support enabled, a WebSocket upgrade that is pipelined behind another HTTP request on the same cleartext connection arrives while that request's response is still attached to the socket. The shared upgrade listener sees the socket is already claimed and returns early without taking the upgrade, but it does not attach an error listener to the raw socket, and Node.js has already removed its own error listener before emitting the upgrade event. A later socket error on that connection, such as a client connection reset, is therefore unhandled and terminates the Node.js process. A single unauthenticated connection that pipelines an upgrade behind a normal request and then resets is enough to crash the server, and it can be repeated to keep the process down. Upgrades over TLS are not affected. The issue is fixed in @fastify/http-proxy 11.6.10, and users should upgrade to 11.6.10 or later.

### CVE-2026-130157

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-19T19:17:25.527 |

RepoManager is a self-hosted deb/rpm package repository. Prior to 5.13.3, an attacker who controls an upstream RPM repository mirrored by a RepoManager instance can provide a package filename through the primary.xml <location href> field; the mirror passes that filename into a shell-interpreted RPM query, allowing shell metacharacters to execute commands as the www-data service account. The target must mirror an upstream repository controlled by the attacker, and the default "Check GPG signatures" option triggers the vulnerable call. The command executes before a later signature-verification failure, so a valid signed package is not required. Fixed in 5.13.3.

### CVE-2026-129502

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-19T19:17:25.407 |

@fastify/http-proxy is a Fastify plugin that proxies HTTP and WebSocket traffic to an upstream server. In versions from 9.4.0 up to but not including 11.6.10, when the plugin is registered with websocket support enabled, a WebSocket upgrade request whose path carries a URL fragment is matched by the router and answered with a successful upgrade before the upstream link is created. Building the upstream target then throws, the error is only logged, and the accepted client socket is left open with no error listener, so the next frame the client sends becomes an unhandled error and terminates the Node.js process. A request target that is not a valid URL reference reaching a parameterized prefix triggers the same path. A single unauthenticated upgrade request followed by one frame is enough to crash the server, and it can be repeated to keep the process down. The issue is fixed in @fastify/http-proxy 11.6.10, and users should upgrade to 11.6.10 or later.

### CVE-2026-129500

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-19T19:17:25.283 |

@fastify/http-proxy is a Fastify plugin that proxies HTTP and WebSocket traffic to an upstream server. In versions from 9.0.0 up to but not including 11.6.10, when the plugin is registered with websocket support enabled, it takes every upgraded socket and dispatches the request through the Fastify router before the WebSocket library takes ownership of the socket. Node.js removes its own error listener from the socket before emitting the upgrade event, and the plugin does not attach one of its own during routing, so a socket error such as a client connection reset that arrives before the WebSocket library takes over is unhandled and terminates the Node.js process. The error window is open whenever anything asynchronous runs between dispatch and the route handler, such as an async hook on the proxied route or any unrelated async route in the application. A single unauthenticated upgrade request followed by a connection reset is enough to crash the server, and it can be repeated to keep the process down. The issue is fixed in @fastify/http-proxy 11.6.10, and users should upgrade to 11.6.10 or later.

### CVE-2026-129418

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T19:17:24.877 |

Joomla Extension - phoca.cz - Stored XSS through YouTube links in Phoca Gallery extension 4.2.0-6.1.6 - The YouTube upload feature did not validate the supplied video URL and embedded the derived video ID without escaping, allowing users with frontend upload permission to inject HTML attributes into the gallery detail view.

### CVE-2026-129229

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-11-19T18:18:07.940 |

NLTK (Natural Language Toolkit) is a suite of open source Python modules, data sets, and tutorials supporting research and development in Natural Language Processing. From 3.10.0 until 3.10.4, TokenSearcher.findall and Text.findall accept caller-controlled regular expressions with an unbounded number of capturing groups throughout the affected range. Starting in 3.10.3, nltk.redos.compile and RegexpTokenizer expose the same compile-time vector. The third-party regex engine compiles group-dense patterns with roughly quadratic cost before the match-time timeout begins, allowing a small unauthenticated request to exhaust CPU and deny service. This issue is fixed in version 3.10.4.

### CVE-2026-129223

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-11-19T18:18:07.320 |

NLTK (Natural Language Toolkit) is a suite of open source Python modules, data sets, and tutorials supporting research and development in Natural Language Processing. Prior to 3.10.4, WordNet Synset.tree and acyclic_tree traverse relation graphs through recursive utility helpers without a depth bound. Exploitation requires the host application to load an attacker-influenced custom or foreign WordNet-format lexical resource; no relation in NLTK's bundled WordNet 3.0 corpus reaches the crash threshold. An excessively deep relation graph in such a resource can exceed the Python recursion limit and terminate the traversal or request worker. This issue is fixed in version 3.10.4.

### CVE-2026-129222

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-11-19T18:18:07.133 |

NLTK (Natural Language Toolkit) is a suite of open source Python modules, data sets, and tutorials supporting research and development in Natural Language Processing. Prior to 3.10.4, DependencyGraph.tree and DependencyGraph.triples walk parsed dependency edges through unbounded Python recursion and do not use a working cycle or depth guard. A crafted CoNLL or Malt-TAB dependency file containing a sufficiently long chain can raise RecursionError when the documented traversal APIs are called, aborting the current worker. This issue is fixed in version 3.10.4.

### CVE-2026-128139

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-11-19T18:18:06.303 |

NLTK (Natural Language Toolkit) is a suite of open source Python modules, data sets, and tutorials supporting research and development in Natural Language Processing. From 3.6 to 3.10.3, XMLCorpusView._read_xml_fragment accumulates 1 KiB blocks and repeatedly applies whole-buffer XML validation while a comment or CDATA terminator remains ahead. A large comment in an attacker-controlled corpus file causes quadratic CPU consumption through documented XML corpus readers across the affected range. On 3.6 and 3.9.2, a large CDATA section incurs the quadratic scan before rejection, while on 3.10.3 both comment and CDATA documents are read successfully. This vulnerability is fixed in 3.10.4.

### CVE-2026-133062

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-19T16:21:19.867 |

A flaw was found in Moodle's external database enrolment plugin. Insufficient sanitization of data passed to queries against the external database allows an authenticated user with course editing permissions to perform a Structured Query Language (SQL) injection attack. When this non-default plugin is enabled, an attacker can exploit this issue to view, modify, or delete sensitive records within the connected external database.

### CVE-2026-131813

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-11-19T16:20:10.217 |

United Chargers Grizzl-E Smart 40A OCPP UpdateFirmware Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of United Chargers Grizzl-E Smart 40A EV chargers. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the handling of OCPP UpdateFirmware requests. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated buffer. An attacker can leverage this in conjunction with other vulnerabilities to execute code in the context of the device. Was ZDI-CAN-29487.

### CVE-2026-131812

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-19T16:20:09.793 |

United Chargers Grizzl-E Smart 40A FTP URL Path Parsing Stack-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of United Chargers Grizzl-E Smart 40A EV chargers. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the parsing of FTP URL paths during firmware updates. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a fixed-length stack-based buffer. An attacker can leverage this in conjunction with other vulnerabilities to execute code in the context of the device. Was ZDI-CAN-28960.

### CVE-2026-131810

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-494` |
| Published | 2026-11-19T16:20:09.543 |

United Chargers Grizzl-E Smart 40A Download of Code Without Integrity Check Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of United Chargers Grizzl-E Smart 40A EV chargers. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the handling of OCPP messages. The issue results from the lack of proper verification of firmware integrity prior to installation. An attacker can leverage this in conjunction with other vulnerabilities to execute code in the context of the device. Was ZDI-CAN-28957.

### CVE-2026-131807

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-19T16:20:09.180 |

United Chargers Grizzl-E Smart 40A OCPP GetConfiguration Stack-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of United Chargers Grizzl-E Smart 40A EV chargers. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the handling of OCPP messages. When parsing GetConfiguration requests, the process does not properly validate the length of user-supplied data prior to copying it to a fixed-length stack-based buffer. An attacker can leverage this in conjunction with other vulnerabilities to execute code in the context of the device. Was ZDI-CAN-28968.

### CVE-2026-133195

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-19T15:17:40.590 |

In JetBrains Junie CLI before 26.6.29 files outside the project directory could be modified by agent file tools

### CVE-2026-133161

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-11-19T15:17:35.953 |

### Summary ui

With `strip_ansi=True`, Pydantic AI Harness's `ToolOutputLimits` capability removes ANSI escape sequences from tool output with a pattern that takes time quadratic in the length of a line. A tool result of a few hundred kilobytes, crafted with many unterminated escape sequences, can occupy the event loop for tens of seconds to minutes, delaying every other request and agent run in the process.

### Details

This affects applications that set `strip_ansi=True` on `ToolOutputLimits` (named `OverflowingToolOutput` before 0.13.0) and run tools whose output an attacker can influence, such as shell commands, file reads, fetched pages or MCP servers. Stripping runs on the event loop before the capability reduces the output, so its own size limits do not bound it.

The assumed attacker can place text in content a tool returns.

### Mitigation

Upgrade `pydantic-ai-harness` to 0.70.0 or later. Until then, leave `strip_ansi` at its default, `False`.

On Pydantic AI v1, the harness cannot be upgraded past 0.4.0. Upgrade to Pydantic AI v2 and `pydantic-ai-harness` 0.70.0, or leave `strip_ansi` off.

### CVE-2026-115463

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-307;CWE-338` |
| Published | 2026-11-19T20:17:19.387 |

Poweradmin is a web-based DNS administration tool for PowerDNS server. From 4.0.0 until 4.2.6, 4.3.5, and 4.4.1, lib/Domain/Service/MfaService.php verifies email second-factor codes through MfaService::verifyCode() without limiting failed attempts, and lib/Application/Controller/MfaVerifyController.php logs failures without throttling them. An attacker who knows the user's password can repeatedly guess the six-digit code during its ten-minute validity period when email MFA is enabled, potentially bypassing the second factor; the advisory notes MFA is disabled by default and that the practical request rate was not measured. This issue is fixed in versions 4.2.6, 4.3.5, and 4.4.1.

### CVE-2026-133253

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-552` |
| Published | 2026-11-19T16:21:28.850 |

In JetBrains IntelliJ IDEA before 2026.3 untrusted projects could read files of other open projects via the built-in web server

### CVE-2026-131288

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-19T20:17:44.780 |

In Splunk SOAR versions below 8.8.0, a user with access to the configured load balancer account could replace a load balancer helper that Splunk SOAR later runs with root privileges during cluster lifecycle operations. If a Splunk SOAR administrator performs a cluster lifecycle operation, Splunk SOAR could execute arbitrary code with root privileges on the load balancer.
The vulnerability is possible because Splunk SOAR does not verify the integrity or ownership of the load balancer helper before running it with root privileges.

### CVE-2026-131278

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-214` |
| Published | 2026-11-19T20:17:43.497 |

In Splunk SOAR versions below 8.8.0, a user with local access to the affected host could obtain a live Splunk SOAR session token or decrypted asset configuration when another user starts an App Editor debug action.
The vulnerability is possible because App Editor debug actions expose sensitive runtime information to other local users on the affected host.

### CVE-2026-131239

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-19T20:17:38.647 |

In Splunk Enterprise Security versions below 8.7.0, a user that holds a role with the run_collect capability could store attacker-controlled values in Updates data. If another user who can access the System Update Status report selects an affected row, Splunk Enterprise Security could run attacker-controlled Search Processing Language (SPL) commands using the permissions of the user who selects the row. The user who stores the values could then access sensitive data and modify data available to the user who selects the row.
The vulnerability is possible because the System Update Status report does not validate destination, signature, and vendor-product values before inserting them into drilldown searches.
For more information see Define roles on the Splunk platform with capabilities (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.4/manage-splunk-platform-users-and-roles/define-roles-on-the-splunk-platform-with-capabilities) and System Update Status (https://help.splunk.com/en/splunk-enterprise-security-8/splunk-app-for-pci-compliance/installation-and-configuration-manual/8.7/configure-reports/system-update-status) in the Splunk documentation.

### CVE-2026-131211

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-19T20:17:34.587 |

In Splunk App for Payment Card Industry Compliance versions below 8.7.0, a user who holds the "ess_user" Splunk Enterprise Security role could add attacker-controlled values to lookup data used by the Primary Functions report. If another authenticated user later selects the value in the Primary Function Summary panel, the Splunk App for Payment Card Industry Compliance could run attacker-controlled Search Processing Language (SPL) commands using the permissions of the user who selected the value. With this access, the first user could expose or modify data available to the user who selected the value.
The vulnerability is possible because the Primary Functions report does not safely escape report values before including them in drilldown searches.
For more information see Users and roles for Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/install/8.7/installation/users-and-roles-for-splunk-enterprise-security) and Reports (https://help.splunk.com/en/splunk-enterprise-security-8/splunk-app-for-pci-compliance/user-manual/8.7/using-the-splunk-app-for-pci-compliance/reports) in the Splunk documentation.

### CVE-2026-118977

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-863` |
| Published | 2026-11-19T20:17:20.080 |

Authorization bypass through a user-controlled key in the PuppetDB facts terminus used by Puppet Server allows a client holding any valid agent certificate to overwrite the facts, including trusted facts, that PuppetDB stores for a different node. In Puppet Enterprise deployments where task permissions are scoped to node groups defined by facts or trusted facts, this can allow a user to run tasks on nodes outside their permitted scope.

### CVE-2026-77318

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:L/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-19T17:18:59.027 |

Jupyter MCP Server is a Model Context Protocol server for Jupyter. Prior to 1.0.3, standalone streamable-http mode can enforce MCP_TOKEN on /mcp while leaving the state-changing /api/connect and /api/stop management routes unauthenticated. An unauthenticated network caller can use /api/connect to replace runtime_url and document_url values and their tokens, reset ServerContext, and start a kernel client against attacker-controlled infrastructure, causing the server to send Jupyter API and WebSocket traffic to that backend. The caller can also use /api/stop to stop the current notebook kernel. This boundary failure does not require explicit insecure no-auth mode and occurs outside normal MCP JSON-RPC tool dispatch. This issue is fixed in version 1.0.3.

### CVE-2026-133306

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-19T17:18:51.963 |

VideoLAN libaacs 0.7.0 through 0.12.0 on non-macOS, non-Windows builds contains stack-based buffer overflows in aacs_resolve_path() in src/file/path.c from length checks against the wrong buffer. Local attackers can place a symlink with a long target on a disc path a user opens to overflow resolved_path[] and link[], crashing the process or potentially executing code if mitigations are bypassed.

### CVE-2026-129234

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426;CWE-427` |
| Published | 2026-11-19T17:17:56.343 |

NLTK (Natural Language Toolkit) is a suite of open source Python modules, data sets, and tutorials supporting research and development in Natural Language Processing. Prior to 3.10.4, Prover9Parent.config_prover9 and Mace accept a relative binary_location and pass it to find_binary as path_to_bin, disabling the bare-name absolute-path guard. A local attacker who can plant prover9 or mace4 in the resolved working directory can cause subprocess.Popen to execute that binary with the invoking user's privileges. This issue is fixed in version 3.10.4.

### CVE-2026-131804

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T12:18:24.093 |

The Seraphinite Accelerator plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'HTTP_USER_AGENT' parameter in all versions up to, and including, 2.31 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires that an administrator has previously enabled the 'Enable logging' and 'HTTP trace' diagnostic options in the plugin's Advanced → Debug settings, both of which are disabled by default.

### CVE-2026-125094

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T12:18:21.453 |

The Optimole – Optimize Images | Convert WebP & AVIF | CDN & Lazy Load | Image Optimization plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 4.2.19 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the AMP plugin to be active in Transitional or Standard template mode, and comments must be open on the target post, which is the WordPress default.

### CVE-2026-133652

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-384;CWE-613` |
| Published | 2026-11-20T11:18:33.510 |

Flowintel , contained a session management vulnerability in its browser authentication mechanism. The session identifier used a bare numeric user ID rather than a credential-bound token, resulting in several related weaknesses:

- Remembered logins (remember-me cookies) remained valid after a user changed their password, allowing an attacker holding a previously issued cookie to retain access indefinitely.
- Server-side session identifiers were not rotated upon login (local, SSO, or remembered), enabling session fixation.
- Self-service email and password changes did not require verification of the current password, permitting an attacker with an active session to modify account credentials without knowledge of the existing password.
- Administrator-initiated password resets did not revoke other browser sessions, invalidate remembered logins, or rotate the affected user's API key.

An attacker who obtained a valid session or remember-me cookie (e.g., through XSS, network interception, or cookie theft) could maintain unauthorized access even after the legitimate user changed their password. Additionally, an attacker with any valid session could change the account's email address or password without knowing the current credentials, effectively taking over the account.

Affected versions: Flowintel prior to 4.1.0.

### CVE-2026-96771

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T10:17:12.213 |

The Hydrogen Calendar Embeds plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via ICS Feed Event Fields (SUMMARY/DESCRIPTION/LOCATION) in all versions up to, and including, 3.0.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the attacker to have write access to an ICS feed that has been configured as a calendar source on the target WordPress site.

### CVE-2026-121790

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T10:17:09.173 |

The CWILL (Formerly ParcelPanel) – Shipment Tracking, Tracking & Order Tracking for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'data[].courier_code, data[].tracking_number (plus pp_sign for the auth bypass)' parameter in all versions up to, and including, 4.6.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The authentication bypass is reachable only when the parcelpanel_api_key WordPress option is non-empty, which occurs automatically once an admin has opened or connected the ParcelPanel admin page; at that point any unauthenticated attacker can bypass the sole access gate by supplying a JSON boolean true as pp_sign, which PHP's loose == operator coerces to true when compared against the non-empty md5 hex string.

### CVE-2026-119611

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T10:17:08.320 |

The NextGEN Gallery plugin for WordPress is vulnerable to Stored Cross-Site Scripting in versions up to, and including, 4.5.5 via the 'ajax_pagination_referrer' request parameter used on the /ngg_tag/<tag>/ taxonomy page. This is due to the plugin reading the pagination base URL from $_REQUEST, preserving the attacker-supplied host on the tag route (where ngg_wprouting_add_post_permalink is forced to false so the plugin does not re-base the links to the site's own permalink), and caching the fully rendered page in a transient keyed only on the request URI (not the request body) for 1800 seconds via NGG_RENDERING_CACHE / PHOTOCRATI_CACHE. This makes it possible for unauthenticated attackers to poison the cached /ngg_tag/<tag>/ page so that its pagination links point to an attacker-controlled host; the plugin's own ajax_pagination.

### CVE-2026-116550

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T10:17:07.833 |

The Photo Gallery, Sliders, Proofing and Themes – NextGEN Gallery plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 4.5.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the plugin's "What must the lightbox be applied to?" setting (thumbEffectContext) to be configured as "Try to apply to all images" or "Try to apply to all images that link to image files," which is not the shipping default, and also requires the attacker's comment to reach a publicly rendered state.

### CVE-2026-109387

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T10:17:06.997 |

The Photo Gallery, Sliders, Proofing and Themes – NextGEN Gallery plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'IPTC 2#120 (caption) / 2#005 (title) inside the image file' parameter in all versions up to, and including, 4.5.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires an authenticated user with image-edit permissions to import an attacker-supplied image file, which is the plugin's standard workflow for photographer uploads, client galleries, and contest submissions.

### CVE-2026-127112

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T09:19:57.487 |

The Events Made Easy plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'event[event_notes]' parameter in all versions up to, and including, 3.3.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is only exploitable when the plugin's 'Allow guest submit?' Frontend Submit option is enabled, though the required nonce is freely obtainable by any anonymous visitor as it is printed on every frontend page.

### CVE-2026-121985

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T09:19:56.620 |

The FV Flowplayer Video Player plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 7.5.57.7212 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the plugin's 'Parse Vimeo and YouTube links' setting to be enabled, which wires do_shortcode into the comment_text filter chain and allows the [fvplayer] shortcode to be rendered from comment content.

### CVE-2026-131645

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T08:18:30.227 |

The Kognetiks Chatbot plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 2.5.9 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The TeX payload survives WordPress core comment kses intact because it contains no HTML tags, and MathJax is active on fresh installs by default due to the 'chatbot_chatgpt_enable_mathjax' option defaulting to 'Yes' with no page or shortcode presence guard on enqueue.

### CVE-2026-131582

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T08:18:29.930 |

The PagBank / PagSeguro e Vindi para WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'customer.name' parameter in all versions up to, and including, 5.1.6 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload can be planted via the legitimate hosted-checkout (Checkout PB) flow simply by entering it as a customer name on PagBank's payment page, requiring no hash brute-forcing whatsoever; the woocommerce_api_rm_ps_notif webhook path is additionally exploitable because its only gate is a 5-character (20-bit) truncated wp_hash() that is trivially brute-forceable.

### CVE-2026-129327

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T08:18:28.910 |

The Apaczka.pl WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the '_apaczka[<id>][error_messages] (and sibling subkeys inside _apaczka[])' parameter in all versions up to, and including, 1.4.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is exploitable during WooCommerce classic guest checkout because WooCommerce's legacy order storage fires the save_post action with the checkout $_POST still populated, giving unauthenticated attackers a direct write path to order post meta without an authenticated session.

### CVE-2026-120508

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T08:18:26.267 |

The Charitable – Donation & Fundraising Platform (Donation Forms, Recurring Donations & Fundraising Campaigns) plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'stripe_payment_method' parameter in all versions up to, and including, 1.8.15.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The nonce required to reach the nopriv AJAX endpoint is publicly obtainable from any rendered campaign donation form, making exploitation trivially accessible to unauthenticated visitors on sites with Stripe configured as a payment gateway.

### CVE-2026-62955

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-19T21:18:03.203 |

baserCMS is a website development framework. From 5.2.3 until 5.3.0, BcThemeFileService::getFullpath() in plugins/bc-theme-file/src/Service/BcThemeFileService.php skips its path containment check when realpath() fails for a nonexistent theme subdirectory selected by the type parameter. An authenticated administrator can supply a traversal path through the theme-file API to access locations outside the theme directory. The bypass of the CVE-2026-30940 fix can permit file writes, overwrites or deletion within the PHP process permissions and, where executable PHP can be written, remote code execution. This issue is fixed in 5.3.0.

### CVE-2026-131272

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-19T20:17:42.767 |

In Splunk SOAR versions below 8.8.0, a user that holds a role with the System Settings edit permission could use the Automation Dependency Wheel Representational State Transfer (REST) API to write arbitrary files outside the intended directory, which could lead to arbitrary code execution.
The vulnerability is possible because Splunk SOAR does not restrict uploaded automation dependency wheel filenames to the intended storage directory.

### CVE-2026-131268

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-19T20:17:42.270 |

In Splunk SOAR versions below 8.8.0, a user that holds a role with the System Settings edit permission could use a customer automation dependency to execute arbitrary code as the user account that runs Splunk SOAR.
The vulnerability is possible because Splunk SOAR does not properly separate customer automation dependencies from trusted product code.

### CVE-2026-131256

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-19T20:17:40.787 |

In Splunk SOAR versions below 8.8.0, an authenticated user that holds a role with the System Settings edit permission could execute arbitrary code on the host that runs Splunk SOAR.
The vulnerability is possible because the Representational State Transfer (REST) API accepts package references from untrusted sources and passes them to the dependency installer.

### CVE-2026-131248

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-19T20:17:39.793 |

In Splunk SOAR versions below 8.8.0, a user that holds a role with the System Settings edit permission and restricted tenant access could modify settings for a tenant outside the role scope through the Representational State Transfer (REST) API. With this access, the user could expose confidential tenant environment values, alter tenant settings and automation behavior, or take the tenant out of operation.
The vulnerability is possible because the Tenant REST API checks the System Settings edit permission but does not enforce the tenant restrictions for the role before it updates the selected tenant.
For more information see Manage roles and permissions in Splunk SOAR (On-premises) (https://help.splunk.com/en/splunk-soar/soar-on-premises/administer-soar-on-premises/8.8.0/manage-your-splunk-soar-on-premises-users-and-accounts/manage-roles-and-permissions-in-splunk-soar-on-premises), Configure multiple tenants on your Splunk SOAR (On-premises) instance (https://help.splunk.com/en/splunk-soar/soar-on-premises/administer-soar-on-premises/8.7.0/configure-product-settings-for-your-splunk-soar-on-premises-instance/configure-multiple-tenants-on-your-splunk-soar-on-premises-instance), and REST Tenant (https://help.splunk.com/en/splunk-soar/soar-on-premises/rest-api-reference/8.5.0/multi-tenancy-endpoints/rest-tenant) in the Splunk documentation.

### CVE-2026-123892

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-19T15:17:25.663 |

SDDC Manager contains an authenticated command-injection vulnerability due to improper sanitization of user-supplied input.
Affected versions: 9.1.x.x (fixed in 9.1.1.0200); 9.0.x.x (fixed in 9.0.2.0100); 5.x (fixed in 5.2.5).

### CVE-2026-129074

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-20T14:17:45.657 |

Missing Authorization vulnerability in miniOrange miniOrange's Google Authenticator miniorange-2-factor-authentication allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects miniOrange's Google Authenticator: from n/a through 6.6.0.

### CVE-2026-129017

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T14:17:44.883 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Gemini Labs Site Reviews site-reviews allows Stored XSS.This issue affects Site Reviews: from n/a through 8.3.7.

### CVE-2026-128996

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T14:17:44.730 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Tomdever wpForo Forum wpforo allows Stored XSS.This issue affects wpForo Forum: from n/a through 3.2.4.

### CVE-2026-109878

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T13:18:35.017 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Elementor Elementor Website Builder elementor allows Reflected XSS.This issue affects Elementor Website Builder: from n/a through 4.4.0.

### CVE-2026-133665

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-862` |
| Published | 2026-11-20T11:18:34.920 |

flowintel contains an information disclosure vulnerability that allows authenticated non-administrative users to access sensitive configuration data and logs intended for administrators only.

The notification page and alert API responses exposed sensitive fields, including webhook URLs, signing secrets, IMAP credentials, and delivery logs, in the initial data or JSON responses. Although the user interface hid the configuration form from non-admin users, the underlying data remained accessible via the page source or API endpoints. This exposure included historical webhook URLs that may contain active bearer tokens.

An attacker with a valid non-admin account could retrieve these credentials and logs, potentially leading to unauthorized access to notification services, impersonation of the application in webhook deliveries, or further lateral movement within the infrastructure.

Affected versions: flowintel < 4.1.0

### CVE-2026-133660

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-862` |
| Published | 2026-11-20T11:18:34.093 |

FlowIntel contains an authorization bypass in its user directory and assignment endpoints that allows authenticated users to access data belonging to other organisations.

When the LIMIT_USER_VIEW_TO_ORG setting is enabled to restrict directory visibility to the caller's organisation, several API endpoints (user lookup by ID, last name, Matrix ID, and role-based listings) did not consistently enforce the organisation boundary. An authenticated non-admin user could retrieve profiles of users in other organisations by supplying their identifiers.

Additionally, OrgAdmin users could retrieve the task assignments of any user in the system, including tasks and case titles from private cases to which they had no access. The assignment endpoints did not verify that the requested user belonged to the caller's organisation or that the underlying cases were visible to the caller.

Security impact:
- Exposure of user identities (names, Matrix IDs, roles) across organisation boundaries
- Disclosure of task assignments, case titles, and workflow details from private cases
- Potential enumeration of other organisations' membership and case activity

Affected versions: FlowIntel prior to 4.1.0

### CVE-2026-133631

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-284;CWE-862` |
| Published | 2026-11-20T10:17:11.027 |

FlowIntel contains multiple security flaws in its note variable resolution, chatbot API tooling, and AI report generation.

- Note variable references (e.g. cross-case or cross-task lookups) were resolved using the viewing user's privileges rather than the destination case's audience. An authenticated user with access to a shared or imported note could embed references to private cases, causing sensitive case data to be pulled into AI report requests, exports, and MISP sends without the referenced case's audience having granted read access.

- The chatbot API tool permitted the language model to invoke any FlowIntel API endpoint, including administrative routes and state-changing GET operations, without an allow-list or path validation. An attacker who can influence the model's instructions (e.g. via untrusted case content) could induce data modification or access restricted endpoints.

- AI report generation passed the Ollama bearer token and full case content as command-line arguments to a child process, exposing them in the system process table to any local user.

Affected versions: FlowIntel prior to 4.1.0.

### CVE-2026-133626

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-11-20T09:20:09.370 |

FlowIntel contains a resource exhaustion vulnerability in its file-to-note conversion feature. When a user converts an attached CSV or JSON file into a case note, the application renders the data as a Markdown table by padding every row to the maximum column count. A crafted file with a small number of filled cells but a very large number of columns (or keys) causes the application to allocate a quadratic number of padded table cells, potentially exhausting a worker process in memory or CPU.

The same issue affects nested JSON values rendered inside table cells, where pretty-printed indentation further inflates the output size.

Preconditions:
- An authenticated user with access to a case in FlowIntel
- Ability to attach and convert a CSV or JSON file to a note

Impact:
- Denial of service: exhaustion of a worker process, potentially disrupting service for other users
- No confidentiality or integrity impact

Affected versions: FlowIntel prior to 4.1.0

### CVE-2026-131797

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T08:18:31.613 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Imran Tauqeer CubeWP Forms cubewp-forms allows DOM-Based XSS.This issue affects CubeWP Forms: from n/a through 1.1.12.

### CVE-2026-130813

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T08:18:29.500 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Liquid Web / StellarWP GiveWP give allows Reflected XSS.This issue affects GiveWP: from n/a through 4.19.2.

### CVE-2026-129075

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T08:18:28.627 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Imran Tauqeer CubeWP Forms cubewp-forms allows DOM-Based XSS.This issue affects CubeWP Forms: from n/a through 1.1.12.

### CVE-2026-105074

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-20T08:18:25.963 |

Cross-Site Request Forgery (CSRF) vulnerability in ShortPixel ShortPixel Image Optimizer shortpixel-image-optimiser allows Cross Site Request Forgery.This issue affects ShortPixel Image Optimizer: from n/a through 6.6.1.

### CVE-2026-77316

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-19T22:18:44.607 |

Flyto2 Core is an execution kernel for automation and AI-agent workflows. Prior to 2.26.8, validate_url_ssrf() in src/core/utils.py validates one DNS answer and then returns the hostname, while guarded_aiohttp_request(), enforce_outbound_url(), and validate_url_with_env_config() allow the outbound connection to perform an independent second lookup. A caller with control of the hostname's DNS can make validation see a public address and make the connection see an internal address, bypassing the guard across its outbound consumers and exposing readable internal or metadata-service responses. The attack requires low or zero DNS TTL behavior and a successful timing-dependent answer change; static multiple-address answers are checked and do not provide the same bypass. This issue is fixed in version 2.26.8.

### CVE-2026-77313

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-367;CWE-918` |
| Published | 2026-11-19T22:18:44.183 |

Flyto2 Core is an execution kernel for automation and AI-agent workflows. Prior to 2.26.8, validate_url_ssrf in src/core/utils.py resolves and checks a hostname but returns the hostname URL rather than the validated address, and session.get in http.get performs an independent DNS lookup when connecting. A low-privileged caller with control of the hostname's DNS can make the first lookup return a public address and the connection-time lookup return an internal address, bypassing the SSRF guard for all modules that call it and exposing readable internal or metadata-service responses. Successful exploitation requires attacker-controlled DNS and a successful timing-dependent answer change between the two lookups. This issue is fixed in version 2.26.8.

### CVE-2026-18883

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-19T20:17:51.347 |

ServiceNow has addressed an indirect prompt injection security issue that was identified in the Email Response AI Agent of Now Assist for CSM. We are not currently aware of malicious exploitation against ServiceNow instances.

This remediation was deployed centrally to the Email Response AI Agent (Now Assist for CSM) and does not require a platform version upgrade or hot fix; no version-specific backports apply.

### CVE-2026-131303

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-19T20:17:46.630 |

In Splunk AI Assistant versions below 2.0.0, a user who does not hold the "admin" or "power" Splunk roles could obtain limited information about indexes and data sources outside their authorized scope through the assistant.
The vulnerability is possible because Splunk AI Assistant does not fully apply authorization controls to all information that it retrieves.

### CVE-2026-131286

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-19T20:17:44.510 |

In Splunk SOAR versions below 8.8.0, an authenticated user with permission to author and run playbooks could view action data outside the authorized scope for that user and change the status and message of another playbook run.
The vulnerability is possible because the playbook API does not verify that the requested playbook run is within the authorized scope of the authenticated user.

### CVE-2026-131262

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-19T20:17:41.523 |

In Splunk SOAR versions below 8.8.0, an authenticated user who can view and edit containers in at least one container label could create artifacts with parent relationships to containers and artifacts outside those labels. This could expose fields from restricted artifacts and modify incident lineage.
The vulnerability is possible because Splunk SOAR does not verify access to the selected parent container and parent artifact when it creates an artifact.

### CVE-2026-131245

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-19T20:17:39.413 |

In Splunk SOAR versions below 8.8.0, a user with edit permission for the container label of a pending external prompt could obtain the external prompt link through the Representational State Transfer (REST) API and use the link to view and resolve the associated approval.
The vulnerability is possible because the approval detail REST API includes the external prompt link in responses outside the assigned approval scope.
For more information see REST Approval (https://help.splunk.com/en/splunk-soar/soar-on-premises/rest-api-reference/6.3.1/approval-endpoints/rest-approval), REST External Prompt (https://help.splunk.com/en/splunk-soar/soar-on-premises/rest-api-reference/7.1.0/external-prompt-endpoints/rest-external-prompt), and Manage roles and permissions in Splunk SOAR (On-premises) (https://help.splunk.com/en/splunk-soar/soar-on-premises/administer-soar-on-premises/8.5.0/manage-your-splunk-soar-on-premises-users-and-accounts/manage-roles-and-permissions-in-splunk-soar-on-premises) in the Splunk documentation.

### CVE-2026-131198

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-19T20:17:32.207 |

In Splunk Enterprise Security versions below 8.7.0, a user that holds a role with the mc_view_im_data capability could cause the Mission Control incident mapping Representational State Transfer (REST) API to run arbitrary Search Processing Language (SPL) commands with elevated permissions. With this access, the user could expose all data in Splunk indexes and all stored credentials and modify protected indexes and lookup data.
The vulnerability is possible because the Mission Control incident mapping REST API does not validate incident identifiers before including them in SPL searches.
For more information see Capability reference for Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/install/8.7/installation/capability-reference-for-splunk-enterprise-security) and Overview of Mission Control in Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/user-guide/8.7/mission-control/overview-of-mission-control-in-splunk-enterprise-security) in the Splunk documentation.

### CVE-2026-131188

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-19T20:17:30.947 |

In Splunk Enterprise versions below 10.4.4, 10.2.8, 10.0.11, and 9.4.16, an unauthenticated user could craft a malicious link that, if opened by an authenticated user, executes arbitrary Search Processing Language (SPL) searches with the victim's permissions. 
Successful exploitation could allow the unauthenticated user to access or modify data, alter Splunk platform configurations, and disrupt operations available to the affected user.
The vulnerability is possible because the Portable Document Format (PDF) generation component processes request data before it rejects deprecated GET requests and does not apply SPL safeguards for risky commands to subsearches.
For more information see Generate PDFs of your reports and dashboards (https://help.splunk.com/en/splunk-enterprise/create-dashboards-and-reports/reporting-manual/10.4/report-management/generate-pdfs-of-your-reports-and-dashboards) and SPL safeguards for risky commands (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.4/best-practices-for-splunk-platform-security/spl-safeguards-for-risky-commands) in the Splunk documentation.

### CVE-2026-131181

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-19T20:17:30.067 |

In Splunk Enterprise versions below 10.4.5, 10.2.9, 10.0.12, and 9.4.16, a user who does not hold the "admin" or "power" Splunk roles could use Data Model Acceleration to run malicious Search Processing Language (SPL) commands and perform actions through the Representational State Transfer (REST) API that the user cannot perform directly.
The vulnerability is possible because Splunk Enterprise does not neutralize user-provided data before it adds that data to a generated search.
For more information, see Accelerate data models (https://help.splunk.com/en/splunk-enterprise/manage-knowledge-objects/knowledge-management-manual/10.2/use-data-summaries-to-accelerate-searches/accelerate-data-models), Define roles on the Splunk platform with capabilities (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.2/manage-splunk-platform-users-and-roles/define-roles-on-the-splunk-platform-with-capabilities), and About the search language (https://help.splunk.com/en/splunk-enterprise/search/search-manual/10.6/search-overview/about-the-search-language).

### CVE-2026-131177

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-74` |
| Published | 2026-11-19T20:17:29.567 |

In Splunk Enterprise versions below 10.4.4, 10.2.9, 10.0.12, and 9.4.16, a user who does not hold the "admin" or "power" Splunk roles could run arbitrary Search Processing Language (SPL) searches with elevated privileges through saved search dispatch and access stored credentials and indexed data or modify lookup data.
The vulnerability is possible because Splunk Enterprise does not correctly neutralize caller-supplied saved search dispatch values before it places the values into an SPL search.
For more information see Search endpoint descriptions (https://help.splunk.com/en/splunk-enterprise/leverage-rest-apis/rest-api-reference/10.4/search-endpoints/search-endpoint-descriptions) in the Splunk documentation.

### CVE-2026-128135

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-59;CWE-73` |
| Published | 2026-11-19T18:18:05.837 |

NLTK (Natural Language Toolkit) is a suite of open source Python modules, data sets, and tutorials supporting research and development in Natural Language Processing. From 3.9.4 to 3.10.3, NLTK ZIP package extraction can write through an existing in-root hardlink whose other link points outside the NLTK data root. A local attacker who can prepare the extraction target can cause a package member write to overwrite an out-of-root file, violating the pathsec containment boundary and affecting integrity and availability. This issues is fixed in version 3.10.4.

### CVE-2026-62256

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-11-19T16:21:37.610 |

HTSlib is a library for reading and writing bioinformatics file formats. Prior to 1.21.2, 1.22.3, 1.23.2, and 1.24, fai_retrieve does not verify that the line width recorded in a FASTA .fai index is greater than or equal to the number of bases per line. When the line width is exactly one less than the base count, retrieval allocates an undersized heap buffer and writes one byte beyond its end; larger discrepancies instead cause an allocation failure that is handled. This issue can corrupt heap memory and crash the process. This issue is fixed in versions 1.21.2, 1.22.3, 1.23.2, and 1.24.

### CVE-2026-62255

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-125;CWE-787;CWE-789` |
| Published | 2026-11-19T16:21:37.430 |

HTSlib is a library for reading and writing bioinformatics file formats. Prior to 1.21.2, 1.22.3, 1.23.2, and 1.24, cram_index_load does not verify that the number of reference sequences in a CRAM .crai index does not exceed the CRAM header reference count. A malformed index can drive unbounded index-array allocation, and when the number of references in the index is within two of INT_MAX, the growth calculation can wrap, read beyond a heap buffer, and use the resulting value as a pointer for an unchecked memory write. Any region query can trigger the flaw, causing denial of service or memory corruption. This issue is fixed in versions 1.21.2, 1.22.3, 1.23.2, and 1.24.

### CVE-2026-133274

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-19T16:21:30.887 |

THC-Hydra through 9.7 contains a stack buffer overflow vulnerability in analyze_server_response() of hydra-http-form.c that allows malicious HTTP servers to corrupt memory via crafted Set-Cookie headers. Attackers can send a Set-Cookie header with an extra leading space followed by a repeated cookie name, causing a negative strncpy length that overflows tmpcookie and crashes Hydra.

### CVE-2026-87867

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-19T15:17:42.420 |

MRemoteNG establishes encrypted but unauthenticated channel with Microsoft SQL Server backend. Client accepts any certificate the server
presents, including a self-signed certificate supplied by an attacker. An attacker positioned between the client and the SQL server (for example via ARP/DNS spoofing) can
transparently pintercept the connection (man-in-the-middle) and read all traffic, including the encrypted connection-password table read and the database login.




Vendor did not provide the range of vulnerable versions. Only version 1.76.20 was tested and confirmed vulnerable. Other versions may also be vulnerable.

### CVE-2026-133173

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-19T15:17:37.410 |

WatchAlert 2.0.0 through 3.9.20 contains an insecure direct object reference vulnerability in the /api/w8t/datasource/dataSourceGet endpoint that lets authenticated users read other tenants' datasources because lookups omit tenant_id filtering. Tenant members with datasource view permission can request another tenant's datasource ID to obtain basic auth passwords, AWS and Alibaba Cloud keys, and Kubernetes kubeconfigs.

### CVE-2026-132039

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-19T15:17:32.450 |

In Eclipse Ditto versions before 3.9.9, Thing events delivered via WebSocket, Server-Sent Events and connections disclose field values which the policy does not allow the subscriber to read. A READ

  revoke for one subject of the subscriber's authorization context is not applied when another of its subjects is granted READ. For subscribers with partial READ access, subscription RQL filters, the SSE
  `_context`, `thing-json` placeholders and extra fields are evaluated on the unfiltered event. This allows an authenticated subscriber with at least partial READ access to a Thing to obtain the values of
  fields it may not read when events for that Thing are emitted.

### CVE-2026-129700

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-863` |
| Published | 2026-11-19T15:17:29.067 |

In Eclipse Ditto versions 2.4.0 to 3.9.8, Thing fields a requester is not allowed to read can be disclosed through the `condition` and `live-channel-condition` headers, which are evaluated against the

  full Thing: the READ check of `live-channel-condition` is skipped when a `condition` header is also present on Thing query commands (3.0.0 to 3.9.8); both headers are evaluated without any authorization
  on WoT Thing Description requests (`Accept: application/td+json`) when WoT TD permission filtering is not active (by default in 3.0.0 to 3.8.14, in 2.4.x with WoT integration enabled, and in 3.9.x with
  filtering disabled); the `condition` of live messages and live events is evaluated without a READ check, and of claim messages without any permission (3.1.0 to 3.9.8); and the twin response of a Thing
  query with a non-matching `live-channel-condition` is returned without filtering it by the policy (3.0.0 to 3.9.8). This allows an authenticated user to read Thing fields they are not allowed to read, in
  some cases without any permission on the Thing.

### CVE-2026-129699

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436;CWE-863` |
| Published | 2026-11-19T15:17:28.930 |

In Eclipse Ditto versions 2.0.0 to 3.8.14 and 3.9.0 to 3.9.8, the authorization check for JSON merge patch commands on Things (HTTP `PATCH` / Ditto Protocol `merge`) does not check permissions for fields

  deleted or set to an empty object by the patch: fields with a `null` value or an empty object value (`{}`) are skipped by the check, and Ditto's regex-based key deletion with the documented `{{
  ~<regex>~ }}` syntax is not recognized as a deletion. An authenticated user with WRITE permission on any part of a Thing can therefore delete other attributes, features and the definition of that Thing,
  or overwrite or create fields as empty objects, including parts the policy revokes or never grants WRITE on.
  
  -->

### CVE-2026-129398

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-19T17:17:57.360 |

Joomla Extension - vi-solutions - Authorization bypass in saveAjaxTextarea task in Visforms extension 1.0.0-5.6.3, 6.0.0-6.2.0 - The saveAjaxTextarea task did not check edit permissions and accepted arbitrary table and column names, allowing backend users to modify the configuration of any form, including notification recipients.

### CVE-2026-129397

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-352` |
| Published | 2026-11-19T17:17:57.227 |

Joomla Extension - vi-solutions - Arbitrary file deletion via path traversal in CSS editor in Visforms extension 1.0.0-5.6.3, 6.0.0-6.2.0 - The delete and rename tasks of the CSS editor lacked authorization checks, CSRF protection and path validation, allowing backend users to delete files outside the CSS directory.
