# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-12 15:00 UTC
- **対象期間**: `2026-11-11T15:01:20.000Z` 〜 `2026-11-12T15:00:39.000Z`
- **重要CVE数**: 274 件（Critical 9.0+: 42 件 / High 7.0〜: 232 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公表された CVE のうち、**CVSS 7.0 以上が 45 件**あり、特に **リモートからのコード実行 (RCE) や認証バイパス** が目立ちます。  
- 被害対象は **WordPress プラグイン、Fortinet 系ネットワーク機器、Synology DSM、Microsoft 管理ツール** と多岐にわたり、Web アプリケーションとインフラ機器の両方で深刻な脆弱性が集中しています。  
- 多くは **入力検証・エスケープ不足、権限チェックの不備、デフォルト設定の緩さ** が根本原因で、**パッチ適用が最も効果的な対策**となります。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な脆弱種別 | 影響範囲・被害シナリオ | 推奨修正バージョン |
|-----|------|--------------|------------------------|-------------------|
| **CVE‑2026‑124815** | 10.0 | 未認証 SQL インジェクション（レコード削除） | Clockinator Lite WordPress プラグイン (≤ 1.1.0) がテーブル名を直接組み立てるため、攻撃者は任意の SQL を実行しデータベース全体を削除可能。 | **1.1.0 以上** |
| **CVE‑2026‑12591** | 9.9 | 権限昇格 → RCE | ManageEngine M365 Manager Plus (v4818 未満) の委任管理画面で権限チェックが不十分。認証済み技術者が管理者権限を取得し、任意コード実行が可能。 | **v4818 以降** (2026‑03 リリース) |
| **CVE‑2026‑124814** | 9.8 | 任意ファイルアップロード → RCE | Ultimate Addons for Elementor Forms (≤ 1.0.8) がアップロードファイルの拡張子を検証しない。PHP スクリプトをアップロードしてサーバ上で実行できる。 | **1.0.8 以上** |
| **CVE‑2026‑76954** | 9.8 | 任意ファイル読取/書込・DoS | Synology DiskStation Manager (DSM) Auth API (7.2.1‑69057‑13 以前、7.3.2‑86009‑5 以前等) の SQL エスケープ欠如により、リモートから任意ファイルの読み書き、サービス停止が可能。 | **7.4.1‑90080‑2** 以降 (2026‑04) |
| **CVE‑2026‑126259** | 9.8 | 認証なしで HA/FGSP 同期機能利用 → 超権限コマンド実行 | FortiOS (7.2.0‑7.4.12, 7.6.0‑7.6.7, 8.0.0‑8.0.1) の HA/FGSP 同期機能に認証が無く、攻撃者が HA パケットを偽装すると super‑admin 権限でコマンド実行できる。 | **FortiOS 8.0.2 以降** (2026‑05) |

> **選定理由**  
> - **CVSS が 9.8 以上**で、**リモートから直接コード実行や権限取得**が可能な点が共通。  
> - **広く利用されている製品/プラグイン**（WordPress、Fortinet、Synology、ManageEngine）であり、放置すると企業全体の情報資産が危険に晒される。  

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 / パッケージ | 現行脆弱バージョン | 対応バージョン | 取得先・備考 |
|-------------------|-------------------|----------------|--------------|
| Clockinator Lite (WordPress) | < 1.1.0 | **≥ 1.1.0** | WordPress プラグインディレクトリ |
| Ultimate Addons for Elementor Forms | < 1.0.8 | **≥ 1.0.8** | Elementor Marketplace |
| Descope (WordPress) | < 1.2.0 | **≥ 1.2.0** | WordPress プラグインディレクトリ |
| ManageEngine M365 Manager Plus | < 4818 | **≥ 4818** | ManageEngine ダウンロードセンター |
| Synology DSM (Auth API) | 7.2.1‑69057‑13 以前、7.3.2‑86009‑5 以前、7.4.1‑90080‑1 以前 | **7.4.1‑90080‑2** 以降 | Synology Update Center |
| FortiOS (HA/FGSP) | 7.2.0‑7.4.12、7.6.0‑7.6.7、8.0.0‑8.0.1 | **8.0.2** 以降 | Fortinet Support Portal |
| FortiMail / FortiAnalyzer / FortiManager | 7.4.0‑7.6.6、8.0.0‑8.0.1 等 | **7.6.7 以降** (各製品最新ファームウェア) | Fortinet Support Portal |
| Red Hat Quay | 任意バージョン (脆弱) | **最新版 (2026‑06 リリース)** | Red Hat Customer Portal |
| Portabase | < 1.21.2 | **≥ 1.21.2** | Portabase GitHub Releases |
| Azul Payara Server / Micro | 任意バージョン | **5.2026.0 以降** | Azul 官方サイト |

### 3.2 直ちに実施すべき防御策
- **WAF ルール追加**  
  - `Clockinator Lite`・`Ultimate Addons` の SQL インジェクション系リクエストをブロック（`UNION SELECT`、`/*` など）。  
  - Synology DSM の Auth API への `LIKE` パターン文字列（`%`, `_`）をエスケープする正規表現ルール。  
- **最小権限の徹底**  
  - ManageEngine の「委任管理」ロールは不要なら無効化し、`admin` 権限は MFA で保護。  
  - FortiOS の HA/FGSP 機能は使用しない場合は **無効化**（`config system ha` → `set enable false`）。  
- **デフォルト設定の見直し**  
  - WordPress では `DISALLOW_FILE_EDIT` と `DISALLOW_FILE_MODS`

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-124815

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-12T06:17:13.853 |

The Clockinator Lite WordPress plugin before 1.1.0 does not restrict access to several of its record deletion actions, and uses a user-supplied table name in a SQL query without validating or escaping it, allowing unauthenticated users to perform SQL injection attacks, deleting data from any database table and extracting sensitive information such as password hashes.

### CVE-2026-12591

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-12T07:16:47.260 |

Zohocorp ManageEngine M365 Manager Plus versions below 4818 is affected by an authenticated technician may exploit insufficient permission validation in the delegated administration interface to escalate privileges beyond their intended scope, which could result in remote code execution during administrative processing.

### CVE-2026-110697

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-11T17:17:14.897 |

A flaw was found in Quay where the robot account listing function constructs a SQL LIKE pattern from user-controlled namespace names without escaping wildcard metacharacters. An attacker who creates a namespace containing an underscore character can match and retrieve robot accounts and their decrypted authentication tokens from other tenants' namespaces, leading to cross-tenant credential theft and unauthorized image operations.

### CVE-2026-124814

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-12T06:17:13.743 |

The Ultimate Addons for Elementor Forms WordPress plugin before 1.0.8 does not properly validate the extension of uploaded files in its bundled file upload field, allowing unauthenticated users to upload arbitrary files such as PHP scripts and achieve remote code execution.

### CVE-2026-110959

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-12T06:17:11.100 |

The Descope WordPress plugin before 1.2.0 does not validate the authentication token it receives before creating a WordPress session, accepting any non-empty token, so an unauthenticated attacker can obtain a session for any existing account, including an administrator, by supplying that account's email address.

### CVE-2026-76954

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-12T04:17:20.407 |

An improper neutralization of special elements used in an SQL command vulnerability in the Auth API in Synology DiskStation Manager (DSM) before 7.2.1-69057-13, 7.2.2-72806-10, 7.3.2-86009-5, and 7.4.1-90080-1 allows remote attackers to read or write arbitrary files and conduct denial-of-service attacks.

### CVE-2026-67449

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-306` |
| Published | 2026-11-11T22:17:28.257 |

Portabase is a database backup and restore tool for PostgreSQL, MySQL, MsSQL, MariaDB, Firebird SQL, SQLite, MongoDB, Redis, Files and Docker Volume. Prior to version 1.21.2, a path traversal in the TUS upload webhook handler (app/api/tus/hooks/route.ts) allowed an unauthenticated attacker to overwrite arbitrary files under the private data directory, including /data/private/keys/master_key.bin (the AES-256-GCM master key). This issue has been patched in version 1.21.2.

### CVE-2026-126263

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-11T22:17:26.520 |

A improper neutralization of special elements used in an sql command ('sql injection') vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.4, FortiMail 7.4.0 through 7.4.6 may allow an authenticated attacker to execute unauthorized code or commands via specifically crafted requests.

### CVE-2026-126262

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-11T22:17:26.343 |

A improper neutralization of special elements used in an sql command ('sql injection') vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiManager 8.0.0, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12 may allow an unauthenticated attacker who has access to the oftp port to execute code or command on the system via crafted OFTP packets.

### CVE-2026-126259

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-11T22:17:26.200 |

A missing authentication for critical function vulnerability in Fortinet FortiOS 8.0.0, FortiOS 7.6.0 through 7.6.7, FortiOS 7.4.0 through 7.4.12, FortiOS 7.2.0 through 7.2.13 may allow an unauthenticated attacker with HA FGSP + standalone-config-sync, or autoscale to execute command as super admin via crafted HA packets.

### CVE-2026-126170

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-116` |
| Published | 2026-11-11T22:17:15.340 |

A improper encoding or escaping of output vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.2, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer Cloud 8.0.1 through 8.0.2, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer-BigData 7.6.0 through 7.6.2, FortiManager 8.0.0 through 8.0.2, FortiManager 7.6.0 through 7.6.7, FortiManager Cloud 8.0.1 through 8.0.2, FortiManager Cloud 7.6.0 through 7.6.7 may allow an unauthenticated attacker to execute unauthorized code or commands via a specially crafted HTTP request

### CVE-2026-126148

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-11T22:17:12.010 |

A improper neutralization of special elements used in an os command ('os command injection') vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6 may allow an unauthenticated attacker to execute unauthorized code or commands via crafted HA join-request packets.

### CVE-2026-126147

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-11T22:17:11.880 |

A improper limitation of a pathname to a restricted directory ('path traversal') vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow an unauthenticated attacker to execute unauthorized code or commands via crafted requests.

### CVE-2026-123710

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1287` |
| Published | 2026-11-11T15:17:18.340 |

A flaw was found in Red Hat Quay. An unauthenticated client can obtain an anonymous registry token with an audience it controls, present that token to the service key rotation endpoint, and install its own approved signing key with no expiry. Registry tokens signed with that key are accepted for any repository, allowing read and write access to private images and replacement of repository tags.

### CVE-2026-126254

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-197` |
| Published | 2026-11-11T22:17:25.490 |

A numeric truncation error vulnerability in Fortinet FortiOS 8.0.0 through 8.0.1, FortiOS 7.6.0 through 7.6.7, FortiOS 7.4.0 through 7.4.12, FortiOS 7.2.0 through 7.2.13 may allow a configured ibgp neighbor to send malicious/malformed attributes to all connected routers via a specially crafted request

### CVE-2026-65840

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-11T19:17:43.937 |

Fider is a feedback portal for feature requests and suggestions. Prior to version 0.36.0, in multi-tenant mode (HOST_MODE=multi), an attacker can use an email verification key issued by Tenant A to authenticate as the same email address on Tenant B. This completely bypasses tenant isolation and allows unauthorized account takeover across tenants. Single-host deployments (HOST_MODE=single, the default) are NOT affected. This issue has been patched in version 0.36.0.

### CVE-2026-8333

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-12T07:16:49.413 |

A stored cross-site scripting vulnerability in Microchip the TimePictra platform could allow an authenticated, low-privileged attacker to store malicious script content that executes when another user views the affected page

### CVE-2026-126164

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-11T22:17:14.537 |

A improper neutralization of special elements used in an sql command ('sql injection') vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow an unauthenticated attacker to execute unauthorized code or commands via crafted requests.

### CVE-2026-120869

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-12T14:17:23.990 |

An unauthenticated attacker can bypass authentication controls to access restricted resources on the Citrix NetScaler Console appliance

### CVE-2026-90908

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-807` |
| Published | 2026-11-12T09:16:40.297 |

A vulnerability in the GenericAdminAuthenticator component of Azul Payara Server and Azul Payara Micro allows a remote, unauthenticated attacker to bypass JMX/RMI administrative access restrictions by spoofing the client host address. Successful exploitation can grant administrative access to the MBean server and lead to remote code execution. Azul Payara Micro is affected only when its JMX connector is enabled.

### CVE-2026-110003

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-12T09:16:39.813 |

A vulnerability in the administration REST interface of Azul Payara allows a remote, unauthenticated attacker to bypass secure-admin remote-access restrictions by supplying an arbitrary value in the X-GlassFish-authToken HTTP header. The header's presence waives the remote-rejection check before the token is validated, and an invalid token falls through to password-based authentication, which succeeds without credentials on default domains configured with an empty administrative password. Successful exploitation grants execution of arbitrary administrative commands, equivalent to complete compromise of the server.

### CVE-2026-126785

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-276` |
| Published | 2026-11-12T01:17:11.603 |

A vulnerability has been found in rmalright TR-VISION HOME 2.0.5. Impacted is the function sub_11504 in the library WFanManager.sys of the component IOCTL Handler. Such manipulation leads to incorrect default permissions. The attack must be carried out locally. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-126253

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-305` |
| Published | 2026-11-11T22:17:25.347 |

A authentication bypass by primary weakness vulnerability in Fortinet FortiOS 8.0.0 through 8.0.1, FortiOS 7.6.0 through 7.6.7, FortiOS 7.4.0 through 7.4.12, FortiOS 7.2.0 through 7.2.13 may allow an unauthenticated attacker to broadcast LSA via specially crafted request

### CVE-2026-126812

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-258` |
| Published | 2026-11-11T21:16:45.690 |

blueprintUE Self-Hosted Edition before 4.3.7 contains an insecure default configuration in its Docker Compose examples that sets MYSQL_ALLOW_EMPTY_PASSWORD=yes in database.env and publishes MariaDB on port 3306. Unauthenticated attackers reaching the Docker host on port 3306 can log in as root without a password to read, modify, or delete user accounts, blueprints, and all databases.

### CVE-2026-126806

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T21:16:44.583 |

WWBN AVideo 14.3 through 29.7.1 contains a stored cross-site scripting vulnerability that allows uploaders to inject scripts via the videoDownloadedLink value stored unescaped through objects/aVideoEncoder.json.php. Attackers can embed event-handler payloads in the URL host rendered as a Source tag in view/managerVideos_body.php, executing in administrator sessions to install plugin archives containing PHP.

### CVE-2026-126800

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T21:16:43.507 |

Hydro @hydrooj/ui-default before 4.59.1 contains a stored cross-site scripting vulnerability that allows registered users to inject script by placing double quotes in language- class tokens within markdown-it-xss.ts. Attackers can store a payload in their profile bio that executes when administrators or other users view it, stealing the non-httpOnly sid session cookie for session hijacking.

### CVE-2026-126797

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-11T21:16:43.027 |

NextScan 1.1.0 through 1.2.0 contains an authentication bypass vulnerability in ns-admin that allows unauthenticated attackers to forge administrator tokens using a hardcoded JWT signing key. Attackers can sign an HS256 X-Access-Token carrying the public super administrator role ID to gain full access to user management, scan tasks and stored vulnerability results.

### CVE-2026-126768

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-11T19:17:37.140 |

OpsTree REMS through 1.0.0 contains an authentication bypass vulnerability that allows unauthenticated attackers to obtain valid JWTs by setting the client-controlled is_local_auth field. Attackers can send a POST /api/v1/user/login/ request for the admin account with an invalid password and is_local_auth true to gain SuperUser administrative access.

### CVE-2026-127046

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-522` |
| Published | 2026-11-12T12:18:23.130 |

The MISP Modules website component contains an information disclosure vulnerability in the external tools management interface. The /external_tools/list endpoint returned stored API keys (the api_key field) in its JSON response via the ExternalTools model serializer. Additionally, the browser-based edit form pre-populated the API key input field with the stored credential value, exposing it in the DOM.

The /external_tools/list endpoint is accessible without authentication (the regression tests verify the response for both authenticated and unauthenticated clients), meaning any network-reachable client could retrieve the API keys for all configured external tools. These keys are used by the server to authenticate submissions to external analysis or enrichment services, so their disclosure allows an attacker to impersonate the MISP instance or directly access those external services.

The vulnerability also affected the edit workflow: the change_config endpoint previously required the API key to be present and non-empty on every save, forcing the key to round-trip through the client. The browser JavaScript stored the key in a reactive state object and updated the in-memory tool list with the credential value, further increasing the window of exposure in client-side memory and network traffic.

Affected component: the website sub-application of MISP Modules, specifically the external_tools module (serializer in models.py, list endpoint, and the external_tools_index.html template). The impact is limited to confidentiality of the stored API keys; no integrity or availability impact on the MISP Modules website itself is indicated by the patch.

### CVE-2026-127016

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-12T10:17:28.960 |

The MISP Modules website component exposes external tool management endpoints (add, delete, change status, and change configuration) that did not enforce the optional administrator authentication policy. When ADMIN_PASSWORD was configured in the application environment, the module configuration endpoints correctly required an authenticated administrator session, but the external tools management handlers processed requests from anonymous users without any authorization check. An unauthenticated attacker with network access to the website could add arbitrary external tools, delete existing tools, toggle their active status, and modify their configurations including API keys and ingestion URLs. This inconsistency allowed bypass of the intended access control for the external tools management functionality. The vulnerability is conditional on ADMIN_PASSWORD being set; installations without an admin password intentionally permit open management access by design. The affected component is the external_tools Flask blueprint within the MISP Modules website application.

### CVE-2026-126325

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:M/U:Amber` |
| Weaknesses | `CWE-20;CWE-502` |
| Published | 2026-11-11T15:17:22.510 |

A critical remote code execution (RCE) vulnerability has been reported in PTC Windchill and PTC FlexPLM. The vulnerability may be exploited through the deserialization of untrusted data.

### CVE-2026-19422

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-12T13:17:16.347 |

Zohocorp ManageEngine DDI Central versions below 6301 is affected by an authentication bypass vulnerability in Windows DNS and DHCP agent synchronization APIs, allowing unauthenticated user to impersonate onboarded Windows servers and perform unauthorized DNS and DHCP modifications.

### CVE-2026-12507

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-12T07:16:46.750 |

Zohocorp ManageEngine AssetExplorer versions below 7860, ServiceDesk Plus versions below 15290, ServiceDesk Plus MSP versions below 15150, and SupportCenter Plus versions below 15150 are affected by a authenticated remote code execution vulnerability in the Reports module. An authenticated user with the Create Query Reports permission could exploit specially crafted database queries to execute arbitrary commands on the underlying server.

### CVE-2026-126251

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-11T22:17:25.087 |

A incorrect authorization vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an attacker to bypass authentication and gain unauthorized access.

### CVE-2026-126229

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-11T22:17:21.447 |

A authorization bypass through user-controlled key vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiAnalyzer 7.0 all versions, FortiAnalyzer Cloud 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiAnalyzer Cloud 7.0 all versions, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager 7.0 all versions, FortiManager Cloud 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12, FortiManager Cloud 7.0 all versions may allow an authenticated administrator to access to other VDOMs via specially crafted HTTP requests.

### CVE-2026-126157

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-11T22:17:13.587 |

A improper authentication vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow an unauthenticated attacker to gain access to other users' secure email accounts via crafted HTTP requests.

### CVE-2026-126156

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-11T22:17:13.450 |

A authorization bypass through user-controlled key vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow an unauthenticated remote attacker to take over an arbitrary IBE recipient account via crafted HTTP requests.

### CVE-2026-126155

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-11T22:17:13.323 |

A incorrect authorization vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow an unauthenticated remote attacker to obtain an authenticated IBE webmail session as any IBE recipient and read or send their encrypted mail via crafted HTTP requests.

### CVE-2026-126150

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-640` |
| Published | 2026-11-11T22:17:12.543 |

A weak password recovery mechanism for forgotten password vulnerability in Fortinet FortiMail 8.0.0, FortiMail 7.6.0 through 7.6.5, FortiMail 7.4.0 through 7.4.7, FortiMail 7.2.0 through 7.2.9 may allow an unauthenticated attacker to reset the password of an arbitrary IBE webmail user and take over their account via specially crafted HTTP requests.

### CVE-2026-126777

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-11T19:17:38.497 |

Traccar 3.15 before 6.17.0 contains an authentication bypass vulnerability in LdapProvider.login() that fails to reject empty passwords, causing LDAP binds to be performed as unauthenticated binds when LDAP authentication is enabled. Unauthenticated attackers who know a valid username can log in via POST /api/session or HTTP Basic authentication with an empty password against directories that permit unauthenticated binds, obtaining sessions for any account including administrators.

### CVE-2026-85632

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306;CWE-354` |
| Published | 2026-11-11T15:17:25.163 |

Missing authentication for critical function and Improper validation of integrity check value vulnerability in Sipay Electronic Money and Payment Services Inc. WooCommerce Virtual POS Module allows Authentication Bypass and Application API Message Manipulation via Man-in-the-Middle.

This issue affects WooCommerce Virtual POS Module: from 26.8.3 before 26.9.1.

### CVE-2026-126257

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-259` |
| Published | 2026-11-11T22:17:25.930 |

A use of hard-coded password vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an unauthenticated attacker to bypass credential validation in certain circumstances outside of the attacker's control and gain unauthorized access.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-91880

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-11T19:17:48.063 |

Dell Terraform Provider for PowerFlex, versions 1.5.0 through 1.8.0, contains an Improper Certificate Validation vulnerability in the SSH client component.Terraform PowerFlex provider uses ssh.InsecureIgnoreHostKey() as the default SSH host key callback. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to information exposure and unauthorized access.

### CVE-2026-75869

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-12T13:17:16.900 |

Zohocorp ManageEngine DDI Central versions below 6301 is affected by an authorization bypass and PowerShell command injection vulnerability that allowed authenticated non-administrative users to target unauthorized Windows DHCP subnets and potentially execute arbitrary commands on managed Windows DHCP servers through crafted DNS suffix values.

### CVE-2026-125285

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-12T13:17:15.003 |

Authentication bypass using an alternate path or channel vulnerability in TIBCO TIBCO Platform’s Self-Hosted Control Plane.

This issue affects TIBCO Platform’s Self-Hosted Control Plane: from 1 through 1.21.

### CVE-2026-19421

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-12T12:18:24.260 |

Zohocorp ManageEngine DDI Central versions below 6301 is affected by a PowerShell injection vulnerability due to insufficient validation of user-supplied TXT record values in Windows DNS operations.

### CVE-2026-16135

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-12T12:18:24.087 |

The VibeBP plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 1.9.9.8.1. This is due to the plugin allowing arbitrary user meta updates through the set_email_notification_settings() function. This makes it possible for authenticated attackers, with Subscriber-level access and above, to grant themselves administrator privileges by updating their own 'wp_capabilities' user meta value.

### CVE-2026-15309

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-12T12:18:23.920 |

The CourseCure Courses plugin for WordPress is vulnerable to Privilege Escalation in versions up to, and including, 1.5.1. This is due to a missing capability check in the ajax_save_settings() function, which accepts arbitrary POST parameters and calls update_option() with attacker-controlled keys and values without any authorization verification. This makes it possible for authenticated attackers, with subscriber-level access and above, to elevate their privileges to administrator by setting the default_role WordPress option to 'administrator' and users_can_register to '1', then registering a new account that is automatically granted full administrator access.

### CVE-2026-13764

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-12T12:18:23.753 |

The Masterstudy - Education WordPress Theme theme for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 4.8.151. This is due to missing authorization and nonce validation on the `masterstudy_ms_stm_set_discard_transient` AJAX action. This makes it possible for authenticated attackers, with Subscriber-level access and above, to elevate their privileges to Administrator by setting the `stm_developer_access_token` transient and using the developer access auto-login flow to obtain administrator session cookies.

### CVE-2026-76173

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-12T10:17:29.353 |

Blind SQL injection vulnerability in the public endpoint `public/webhook/receiver.php` of the WhatsApp module for Dolibarr 1.9. The phone number value derived from the `data.key.remoteJid` parameter, received via a JSON request, is incorporated into an SQL query without escaping or parameterization. With the WHATSAPP_WEBHOOK_ALLOW option enabled, an unauthenticated remote attacker could manipulate this parameter to alter the query. Exploitation using a timing-based technique could allow an attacker to extract information from the database and cause service disruption.

### CVE-2026-125836

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-12T08:16:41.267 |

Cross-Site Request Forgery (CSRF) vulnerability in Nicu Micle Simple JWT Login simple-jwt-login allows Cross Site Request Forgery.This issue affects Simple JWT Login: from n/a through 3.6.8.

### CVE-2026-8332

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-12T07:16:48.747 |

A hard-coded root password in Microchip TimePictra platform installation files could allow an attacker with access to those files to obtain privileged credentials

### CVE-2026-8331

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-12T07:16:47.963 |

An unrestricted upload of files with dangerous type vulnerability in the Microchip TimePictra platform allows functionality not properly constrained by access control lists, potentially resulting in remote code execution.

### CVE-2026-122003

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-12T06:17:12.810 |

The Abilities Bridge WordPress plugin before 1.4.2 does not require a valid nonce before re-authenticating a REST API request from the logged-in session cookie, allowing attackers to make a logged-in administrator perform any REST API action, including creating a new administrator account and taking over the site, by tricking them into opening a crafted page (CSRF).

### CVE-2026-74857

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-304` |
| Published | 2026-11-12T04:17:20.040 |

A missing critical step in authentication vulnerability in the Auth API in Synology DiskStation Manager (DSM) before 7.3.2-86009-5 and 7.4.1-90080-1 allows remote authenticated users to read or write arbitrary files and conduct denial-of-service attacks.

### CVE-2026-18792

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-12T04:17:19.127 |

An improper limitation of a pathname to a restricted directory vulnerability in the Sharing API in Synology DiskStation Manager (DSM) before 7.3.2-86009-5 and 7.4.1-90080-1 allows remote authenticated users to read or write arbitrary files and conduct denial-of-service attacks.

### CVE-2026-13672

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-12T04:17:18.343 |

An authorization bypass through user-controlled key vulnerability in the SSOAuth in Synology DiskStation Manager (DSM) before 7.3.2-86009-5 and 7.4.1-90080-1 allows remote authenticated users to read or write arbitrary files and conduct denial-of-service attacks.

### CVE-2026-122044

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-11-12T03:17:11.247 |

Philips Hue Bridge Pro Protection Mechanism Failure Authentication Bypass Vulnerability. This vulnerability allows network-adjacent attackers to bypass authentication on affected installations of Philips Hue Bridge Pro. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the HTTP service, which listens on TCP port 443 by default. The issue results from the failure to apply a protection mechanism. An attacker can leverage this vulnerability to bypass authentication on the system. Was ZDI-CAN-33086.

### CVE-2026-67547

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-11T22:17:29.710 |

taOS is a self-hosted AI agent OS. Prior to version 1.0.0-beta.23, the POST /api/skill-exec/{skill_id}/call endpoint in taOS executes built-in skills — including the code_exec skill which runs arbitrary Python via subprocess.run(["python3", "-c", code]) — without performing any admin role check, skill ownership check, or agent assignment verification. Any authenticated non-admin user can supply attacker-controlled Python code in the request body and have it executed as the taOS backend process user on the host, achieving full remote code execution with no privilege escalation required beyond a valid (non-admin) session. This issue has been patched in version 1.0.0-beta.23.

### CVE-2026-67546

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-11T22:17:29.533 |

Heym builds and runs agentic systems and business-process automations on self-hosted infrastructure. Prior to version 0.0.75, the same POST /api/mcp/fetch-tools endpoint (any authenticated user, lowest role) also accepts the stdio transport, which spawns the attacker-supplied command with attacker-supplied args and an environment merged over os.environ. The process executes on the shared backend host before MCP protocol validation fails — so side effects fire regardless of whether the command speaks MCP. This is a distinct weakness class and exploit primitive from the SSRF (Advisory 2) on the same endpoint, and needs a different fix (role gating / opt-in trust boundary rather than egress controls). This issue has been patched in version 0.0.75.

### CVE-2026-67544

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-11T22:17:29.180 |

Heym builds and runs agentic systems and business-process automations on self-hosted infrastructure. Prior to version 0.0.71, Heym's workflow engine accepts an arbitrary Python code string in the playwrightCode field of a Playwright node. This string is written to a temporary .py file and executed directly by the backend process via subprocess.Popen([sys.executable, script_path]) with no sandboxing, AST validation, or role gate. Any authenticated user — including a freshly registered account — can achieve full remote code execution (RCE) on the backend host, running as the service process user (observed as root in the default Docker deployment). This issue has been patched in version 0.0.71.

### CVE-2026-67543

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-269` |
| Published | 2026-11-11T22:17:28.997 |

Heym builds and runs agentic systems and business-process automations on self-hosted infrastructure. Prior to version 0.0.70, heym hardens one untrusted-code path but not its sibling. The Python tool executor (python_tool_executor.py) treats user code as untrusted and mandates a Docker sandbox (no network, read-only fs, non-root, no docker socket), failing closed. The skill executor (skill_python_executor.py) runs skill Python via a local backend subprocess with no Docker isolation — only a 512 MB RLIMIT and a 7-key env denylist — so a skill executes inside the backend execution context, with filesystem access, network egress, and non-denylisted environment variables that should not be exposed to untrusted/shared skills. In the shipped Docker config (backend runs as root + /var/run/docker.sock mounted), this escalates to host root. This issue has been patched in version 0.0.70.

### CVE-2026-126241

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-11T22:17:23.753 |

A improper neutralization of special elements used in an sql command ('sql injection') vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an authenticated attacker to execute unauthorized SQL commands on the underlying database.

### CVE-2026-126175

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-11T22:17:15.747 |

A improper neutralization of special elements used in an sql command ('sql injection') vulnerability in Fortinet FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.2 through 7.2.12, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.2 through 7.2.13, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.2 through 7.2.12, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.2 through 7.2.13 may allow an authenticated attacker to execute unauthorized code or commands via crafted JSON-RPC requests.

### CVE-2026-126144

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-11T22:17:11.400 |

A improper neutralization of special elements used in an os command ('os command injection') vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.4, FortiMail 7.4.0 through 7.4.6, FortiMail 7.2 all versions, FortiRecorder 7.6.0 through 7.6.2, FortiRecorder 7.2.0 through 7.2.12, FortiRecorder 7.0.0 through 7.0.6, FortiVoice 8.0.0 through 8.0.1, FortiVoice 7.4.0 through 7.4.2, FortiVoice 7.2.0 through 7.2.5, FortiVoice 7.0.0 through 7.0.8 may allow an authenticated attacker to execute unauthorized code or commands via specifically crafted HTTP requests.

### CVE-2026-126802

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-11T21:16:43.837 |

NextScan 1.1.0 through 1.2.0 contains hardcoded HTTP Basic Auth credentials in ns-admin's AuthAgent and AuthExternal routers that allow unauthenticated attackers to access protected APIs. Attackers can call /agent/config to obtain Redis passwords, etcd details and the server token, and impersonate scan nodes via registration, heartbeat and logging endpoints.

### CVE-2026-126774

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-11T19:17:37.937 |

@tinacms/mdx before 2.4.2 contains a code injection vulnerability in its MDX serializer, which writes rich-text values into MDX expressions without escaping them. Authenticated content editors can save crafted values that break out of list field or highlightColor expressions in the stored .mdx file, executing JavaScript in visitors' browsers or on build and server-side rendering hosts.

### CVE-2026-91879

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-532` |
| Published | 2026-11-11T18:19:53.483 |

Dell Terraform for ObjectScale and Powerstore, versions prior to 1.1.1 (ObjectScale) and versions 1.2.1 through 1.3.0 (PowerStore) contains an insertion of sensitive information into Log File vulnerability in the client initialization component.  A low privileged attacker with remote access could potentially exploit this vulnerability, leading to information exposure and unauthorized access.

### CVE-2026-61619

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-11-11T18:19:47.443 |

The OWASP core rule set (CRS) is a set of generic attack detection rules for use with compatible web application firewalls. Prior to versions 3.3.10, 4.25.1, and 4.28.0, regular-expression denial of service (ReDoS) affects a shared regex-assembly include used to build 12 Unix RCE detection rules in CRS v4, and the same ambiguous pattern was present in the manually-assembled regexes in 4 rules in CRS v3.3. With a single, unauthenticated, crafted request, the generated pattern drives PCRE2 past its backtracking limit. When PCRE2 exceeds that limit, the @rx operator returns an error rather than a match result, which results in detection bypass and CPU denial of service. This issue has been patched in versions 3.3.10, 4.25.1, and 4.28.0.

### CVE-2026-107662

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-11T18:18:24.690 |

Blind SQL injection in Revive Adserver 6.0.8 and earlier allows an authenticated manager restricted to one agency to extract arbitrary database values through the banner-zone.php and campaign-zone.php administration pages. Permission checks and database queries obtain identifiers through inconsistent request-input precedence, allowing an authorized numeric identifier to pass validation while a different, attacker-controlled value reaches an SQL query. Extracted data can include password hashes and active session identifiers. Reusing an unexpired administrator session can grant administrative access, allowing modification of configuration and disruption of ad delivery. The issue is fixed in Revive Adserver 6.0.9 by consistently selecting POST values before GET values in both global input registration and common input helpers, and excluding cookies from these helpers. Both commits e301dbbb7 and 0aa9d0124 are required for the complete correction.

### CVE-2026-106152

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-15` |
| Published | 2026-11-11T18:18:24.290 |

In Progress® Telerik® Report Server prior to version 12.3.26.1110, an external control of a system configuration setting vulnerability allows an unauthenticated remote attacker to influence the server address used by Report Server when generating links and notifications. With user interaction, this can lead to disclosure of sensitive information and account takeover.

### CVE-2026-124628

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-12T14:17:28.587 |

In affected versions of Octopus Server, incorrect validation of changes a user made to their own LDAP identity allowed them to edit that identity even when an Administrator had disabled self-service identity editing. This could result in the user gaining membership of teams mapped to external LDAP groups they do not belong to, and potentially escalating to full administrative privileges if any of those teams are privileged.

### CVE-2026-124627

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-12T14:17:28.443 |

In affected versions of Octopus Server, incorrect validation of the external identity linked to a newly registered user could result in that user receiving the LDAP-mapped team memberships and associated permissions of another user. This issue only affects instances with LDAP authentication enabled and LDAP groups mapped to Octopus teams.

### CVE-2026-116835

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-12T14:17:23.630 |

In affected versions of Octopus Server, insufficient validation of custom claims on OIDC accounts allowed a user with permission to edit accounts to cause Octopus Server to issue signed OIDC tokens that impersonate a different project. This could grant access to external systems, such as cloud providers or other Octopus instances, that trust that project's identity.

### CVE-2026-127056

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-12T13:17:16.177 |

PapaParse before 5.7.1 contains an inefficient algorithmic complexity vulnerability that allows remote unauthenticated attackers to cause denial of service by submitting delimiter-free quoted CSV input to Papa.parse(). Attackers can supply a single-column quoted CSV with no delimiters, triggering repeated full-buffer indexOf scans per row that grow quadratically with input size, exhausting CPU and blocking the Node.js event loop or freezing a browser tab.

### CVE-2026-126217

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-11T22:17:19.240 |

A incorrect authorization vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiAnalyzer Cloud 8.0.0 through 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.0 through 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an authenticated administrator to escalate their privileges, bypass authorization controls or impersonate internal services via specially crafted requests to the GUI.

### CVE-2026-126183

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-11T22:17:17.330 |

A authorization bypass through user-controlled key vulnerability in Fortinet FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an authenticated attacker to execute commands outside of the expected scope via specially crafted HTTP request.

### CVE-2026-126162

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-91` |
| Published | 2026-11-11T22:17:14.270 |

A xml injection (aka blind xpath injection) vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6 may allow a remote unauthenticated attacker to execute unauthorized code or commands via a specially crafted request.

### CVE-2026-65982

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-11T21:16:46.903 |

nginx-http-flv-module is a media streaming server based on nginx-rtmp-module. Prior to version 1.2.14, if a server received an HTTP/1.0 request without a header Host, which was permitted by HTTP core of Nginx, then r->headers_in.host was NULL, nginx-http-flv-module used r->headers_in.host->value to make a pseudo tcUrl, so NULL-pointer dereference happened. This issue has been patched in version 1.2.14.

### CVE-2026-65965

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-862` |
| Published | 2026-11-11T21:16:46.410 |

ideon is a self-hosted visual workspace. Prior to version 0.9.4, several project mutation endpoints under /api/projects/[id]/* resolve the caller's project role but never enforce it, so a user who was granted only the read-only viewer role on a project can perform write operations on that project. The most severe is POST /api/projects/[id]/graph, which deletes every block and link in the project and re-inserts client-supplied ones. A viewer can silently rewrite or wipe the entire canvas of a project they were invited to read. The application clearly intends viewer to be read-only: the collaborators endpoint, the automation endpoints, and the realtime Yjs sync path all reject write attempts from viewers. These specific HTTP handlers simply omit the guard their siblings enforce. This issue has been patched in version 0.9.4.

### CVE-2026-126801

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-11T21:16:43.670 |

Rote 1.2.0 through 2.6.0 contains an authorization bypass in the OAuth bind/merge endpoint that allows authenticated users to merge any OAuth-bound account into their own. Attackers can submit a public existingUserId and GitHub or Apple user ID to take over notes, attachments, and API keys and delete the victim account.

### CVE-2026-100307

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-862` |
| Published | 2026-11-11T21:16:41.933 |

Missing authorization in the external management API in Amazon mcp-gateway-registry 1.0.9 through 1.24.7 might allow an authenticated remote user to assign the registry administrator scope to their own identity group and obtain administrative control of every registered gateway asset via a crafted group import request.



To remediate this issue, users should upgrade to version 1.25.0.

### CVE-2026-91875

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-11T19:17:47.513 |

Dell OpenManage Ansible Modules, versions 9.2.0 through 10.0.3, contains an Improper Certificate Validation vulnerability in the SessionAPI component. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to information exposure and unauthorized access.

### CVE-2026-91874

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-11T19:17:47.373 |

Dell OpenManage Ansible Modules, versions 5.0.0 through 10.0.3, contains an Improper Certificate Validation vulnerability in the iDRACConnection component. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to information exposure and unauthorized access.

### CVE-2026-91873

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-11T19:17:47.230 |

Dell OpenManage Ansible Modules, versions 2.1.2 through 10.0.3, contains an Improper Certificate Validation vulnerability in the iDRACRedfishAPI component. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to information exposure and unauthorized access.

### CVE-2026-65843

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-11T19:17:44.120 |

sync-rpc runs asynchronous commands synchronously by putting them in a separate proces. Prior to version 1.3.7, if an attacker could guess the correct port and it was not blocked via a firewall, it was possible to load and execute arbitrary JavaScript files stored on the server running sync-rpc. This issue has been patched in version 1.3.7.

### CVE-2026-126779

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-11T19:17:38.840 |

Spatie Browsershot 2.2.0 before 5.5.0 contains a local file read vulnerability that allows attackers to read server files by supplying root-relative references in HTML passed to setHtml(). Attackers can embed iframe, img, link or script elements referencing paths like /etc/passwd, which resolve to file:// URLs and render file contents into the returned PDF or screenshot.

### CVE-2026-126769

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-11T19:17:37.293 |

OpsTree REMS through 1.0.0 contains a missing authentication vulnerability that allows unauthenticated remote attackers to access Governance API endpoints, including /api/v1/databases. Attackers can send requests without an Authorization header, or with invalid or tampered JWT tokens, to retrieve stored database hosts, usernames, and passwords.

### CVE-2026-91890

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-11T18:19:53.627 |

Dell Ansible Storage for Unity , versions prior to 1.2.13 contains an Improper Certificate Validation vulnerability in the UnityRESTConnector component. An unauthenticated attacker with remote access could potentially exploit this vulnerability,leading to information exposure and unauthorized access.

### CVE-2026-65820

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-11T18:19:47.940 |

aeon is a scikit-learn compatible Python library for learning from time series. Prior to version 1.5.0, a GitHub Actions workflow used pull_request_target for pre-commit checks on pull requests from forks. In this configuration, fork-controlled code could be checked out and executed in a privileged context. The vulnerable workflow also generated/used elevated credentials and could automatically commit or push fixes back to pull request branches. This created a potential token exposure and repository write path if an attacker submitted a malicious fork pull request designed to execute during the privileged workflow run. This issue has been patched in version 1.5.0.

### CVE-2026-127036

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-11-12T12:18:22.960 |

Improper neutralization of CRLF sequences ('CRLF injection') vulnerability in ibi WebFOCUS.

This issue affects WebFOCUS: 9.1, from 9.2 through 7, and from 9.3 through 7.

### CVE-2026-124647

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-12T06:17:13.150 |

The TI WooCommerce Wishlist WordPress plugin before 2.0.7 does not sanitise and escape user input before using it in a SQL statement in a front-end endpoint, allowing unauthenticated users to perform SQL injection attacks.

### CVE-2026-101107

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-12T06:17:10.053 |

An OS command Injection issue exists in Air Terminal 6 provided by SoftBank Corp. Arbitrary commands may be executed with the root privilege by a user who can log in to the web management console of the affected product.

### CVE-2026-85101

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-12T04:17:21.617 |

An authentication bypass using an alternate path or channel vulnerability in the rsync in Synology DiskStation Manager (DSM) before 7.2.1-69057-13, 7.2.2-72806-10, 7.3.2-86009-5, and 7.4.1-90080-1 allows remote attackers to read specific files, write arbitrary files, and conduct limited denial-of-service attacks.

### CVE-2026-111433

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-61` |
| Published | 2026-11-12T04:17:17.160 |

UNIX symbolic link (symlink) following vulnerability in openEuler iSulad on Linux.

This vulnerability is associated with program file src/daemon/modules/spec/specs_mount.c.



This issue affects iSulad: through 2.1.6.



If an attacker can get the victim or the platform to run their crafted malicious image, they can cause the iSulad daemon to copy sensitive host directories into an anonymous volume when creating a container, which the container can then read.

### CVE-2026-65949

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-94` |
| Published | 2026-11-11T22:17:27.373 |

Improper neutralization of special elements used in an OS command in Lenovo XClarity Integrator for Microsoft Windows Admin Center 5.1.1 and 5.2.0 allows an authenticated remote attacker to execute arbitrary PowerShell commands by submitting a crafted hostname.

### CVE-2026-126238

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-11T22:17:23.313 |

A incorrect authorization vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an unauthenticated attacker to bypass authorization checks and gain unauthorized access to restricted functionality.

### CVE-2026-126805

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-11T21:16:44.373 |

WWBN AVideo through 29.7.1 contains an incorrect authorization vulnerability that allows delegated Videos Admin users to obtain video_id_hash values bound to any video owner via encoder endpoints like aVideoEncoderStatus.json.php. Attackers can request the hash for an administrator-owned video and replay it through useVideoHashOrLogin() for password-less login, gaining plugin upload, configuration, and user management access.

### CVE-2026-126803

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-11T21:16:44.007 |

Rote through 2.6.0 contains a privilege escalation vulnerability that allows authenticated admins to obtain super_admin rights by reading or overwriting JWT signing secrets via /v2/api/admin/settings. Attackers can retrieve the unmasked jwtSecret from the security settings group and forge HS256 tokens for the super administrator to change user roles and escalate their own account.

### CVE-2026-126780

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-11T19:17:38.993 |

Webmin through 2.670 contains a privilege escalation vulnerability in acl/save_group.cgi that allows delegated administrators to grant unauthorized modules by submitting arbitrary module lists in the mod parameter. Attackers with Webmin Users module access can create or edit groups holding modules like Command Shell and assign themselves membership to execute commands as root.

### CVE-2026-106156

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-11T18:18:24.423 |

In Progress® Telerik® UI for ASP.NET Core versions `2015.1.318` through `2026.3.811`, repeated server-side aggregation requests, with or without grouping, cause dynamic assemblies and load contexts to be retained, resulting in accumulating process memory consumption. An unauthenticated remote attacker can exploit this if the application exposes an aggregation endpoint that is reachable without authentication. Repeated requests can cause memory growth that may exhaust available resources and affect application availability. Disabling grouping in the client-side interface does not prevent direct requests containing these descriptors. The issue is fixed in version `2026.3.1015`.

### CVE-2026-106137

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-362;CWE-401` |
| Published | 2026-11-11T18:18:24.160 |

In affected versions of Progress® Telerik® UI for ASP.NET MVC `2012.2.710` through `2026.3.811`, ClassFactory updates a shared class dictionary without exclusive write protection and emits non-collectible dynamic assemblies that remain loaded for the AppDomain's lifetime. The dictionary lookup and insertion are not atomic, and case variations in aggregate descriptors can produce distinct retained types even though member resolution is case-insensitive. An unauthenticated remote attacker can exploit this if the application exposes an aggregation endpoint that is reachable without authentication, by submitting concurrent or repeated crafted requests. These requests may corrupt dictionary state or increase CPU and memory use, potentially degrading availability. The issue is fixed in version `2026.3.1015`.

### CVE-2026-89061

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-11-11T17:17:23.107 |

During an internal security assessment, a potential vulnerability was discovered in Lenovo PC Manager, distributed exclusively in the Chinese market, that could allow a local user to escalate privileges.

### CVE-2026-77882

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-11T17:17:20.130 |

A deserialization of untrusted data vulnerability was discovered in Lenovo System Update that could allow a local authenticated user to execute code with elevated privileges.

### CVE-2026-126180

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-11-11T22:17:16.813 |

A improper neutralization of special elements used in a template engine vulnerability in Fortinet FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2 all versions, FortiManager Cloud 8.0.0 through 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2 all versions may allow a low privileged Device Manager admin to obtain super admin privilege on managed FortiGates via injecting malicious commands.

### CVE-2026-67548

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-11T22:17:29.863 |

taOS is a self-hosted AI agent OS. Prior to version 1.0.0-beta.25, tinyagentos (taOS) registers all system settings routes under a single APIRouter() instance created with no admin authorization dependency. Any authenticated user—including non-admin invited users whose is_admin flag is explicitly False—can read the full system configuration, overwrite it, modify platform settings, trigger a git pull + dependency reinstall + service restart, and switch the tracked update branch. Successful exploitation of the write endpoints causes immediate configuration corruption or a denial of service for all users on the instance from a low-privileged account. This issue has been patched in version 1.0.0-beta.25.

### CVE-2026-126252

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-11T22:17:25.220 |

A improper neutralization of special elements used in an sql command ('sql injection') vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an authenticated attacker to execute unauthorized code or commands via http requests

### CVE-2026-105440

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-11T16:17:24.817 |

Missing authorization in the JSON-RPC web services interface
of Extreme Networks Switch Engine (EXOS) allows an authenticated,
low-privileged (read-only) user to execute CLI show commands that are
restricted to that role through the command line interface. Successful
exploitation results in disclosure of sensitive information, including the
device configuration and the password hashes of local accounts. Configuration,
enable, and debug commands are not affected. Disclosed password hashes can be
attacked offline, and a weak password could lead to administrative access to
the device. This issue is fixed in Switch Engine 33.7.1-patch1-11,
33.1.100.133-patch1-9, and 32.7.4.15-patch1-11.








Extreme Networks would like to thank Toàn Lê (GitHub: https://github.com/toanln-cov) for responsibly disclosing this vulnerability and for working with our PSIRT team through coordinated disclosure.

### CVE-2026-126250

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-11T22:17:24.960 |

A incorrect authorization vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an unauthenticated attacker to cause a denial of service via HTTP requests.

### CVE-2026-126240

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-90` |
| Published | 2026-11-11T22:17:23.617 |

A improper neutralization of special elements used in an ldap query ('ldap injection') vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an authenticated attacker to bypass authentication. Successful exploitation requires either a malicious/compromised upstream IdP, or an IdP configuration that allows the user to control the NameID (or the SAML attribute used as the username).

### CVE-2026-126218

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-11T22:17:19.457 |

A authorization bypass through user-controlled key vulnerability in Fortinet FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11 may allow a remote authenticated attacker with admin permission to elevate their privileges to root via crafted HTTP requests.

### CVE-2026-126215

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-11T22:17:18.860 |

A incorrect authorization vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiAnalyzer Cloud 8.0.0 through 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.0 through 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an authenticated administrator to escalate their privileges, bypass authorization controls or impersonate internal services via specially crafted requests to the GUI.

### CVE-2026-126184

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-11T22:17:17.603 |

A authentication bypass by spoofing vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiAnalyzer Cloud 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an attacker to disrupt the HA state.

### CVE-2026-126160

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-11T22:17:13.990 |

A improper authentication vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow an unauthenticated attacker to escalate privileges and release or delete quarantined messages for arbitrary mailboxes via a crafted quarantine release requests.

### CVE-2026-123863

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2026-11-11T19:17:32.577 |

A reachable assertion in Node.js HTTP/2 session teardown lets any unauthenticated client abort the server, over both TLS and cleartext. A client can arrange for an Http2Stream that still holds nghttp2-allocated header buffers to outlive its session: the stream is removed from the session's stream set but never detached, so when ~Http2Session() runs the memory accounting is nonzero and the CHECK_EQ(current_nghttp2_memory_, 0) assertion fails, terminating the process. The trigger needs only a default http2 server whose handler responds before the request body has ended, which is typical. It is a variant of CVE-2024-27983 that the earlier fix did not cover, because that fix only detached streams still tracked in the session. This vulnerability affects Node.js 26.x (since 26.9.0) and 24.x (since 24.22.0).

### CVE-2026-64855

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-295;CWE-347` |
| Published | 2026-11-11T16:17:25.370 |

soapbar is a SOAP library for Python — client, server, and WSDL handling. Prior to version 0.13.0, verify_envelope_bsp() derived its trust anchor from the message it was verifying. It read the X.509 certificate out of the caller-untrusted wsse:BinarySecurityToken, validated only that certificate's not-before / not-after dates, and then verified the signature against that same certificate. There was no CA-chain validation, no issuer/subject allowlist, and no pinning. A successful verify_envelope_bsp() therefore proved only that the envelope was signed by whoever supplied the embedded certificate — never that it was signed by a trusted party. An attacker who mints their own certificate, signs a forged envelope, and embeds that certificate in the token passes verification. Any consumer that treats a successful BSP verification as authentication can be impersonated (signature forgery / authentication bypass). verify_envelope() (which pins a caller-supplied x509_cert) was not affected — the flaw was specific to the BSP variant whose trust anchor came from the message. This issue has been patched in version 0.13.0.

### CVE-2026-75868

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-12T13:17:16.763 |

Zohocorp ManageEngine DDI Central versions below 6301 is affected by an authorization bypass vulnerability that allowed authenticated non-administrative users to modify DHCP options on subnets belonging to unauthorized clusters.

### CVE-2026-75867

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-12T13:17:16.633 |

Zohocorp ManageEngine DDI Central versions below 6301 is affected by an authorization bypass vulnerability that allowed authenticated non-administrative users to modify Windows DHCP filter-list configurations across unauthorized clusters.

### CVE-2026-75864

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-12T13:17:16.497 |

Zohocorp ManageEngine DDI Central versions below 6301 is affected by an improper authorization vulnerability that allowed authenticated non-administrative users to delete DNS zones outside their assigned scope.

### CVE-2026-76792

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-12T06:17:14.937 |

The User Verification by PickPlugins WordPress plugin before 2.0.49 does not rate limit the verification step of its one-time-password login, and does not expire the generated code, allowing unauthenticated attackers to brute force it and log in as any user, including administrators, where the code is configured to use digits only.

### CVE-2026-81584

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-12T04:17:21.157 |

An improper neutralization of special elements used in an SQL command vulnerability in the User API in Synology DiskStation Manager (DSM) before 7.3.2-86009-5 and 7.4.1-90080-1 allows remote attackers with control over a compromised LDAP or Active Directory server to read or write arbitrary files and conduct denial-of-service attacks.

### CVE-2026-19048

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-12T04:17:19.253 |

An improper link resolution before file access vulnerability in the thumb in Synology DiskStation Manager (DSM) before 7.3.2-86009-5 and 7.4.1-90080-1 allows remote authenticated users to write arbitrary files and conduct denial-of-service attacks.

### CVE-2026-18596

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-12T04:17:18.880 |

An authentication bypass using an alternate path or channel vulnerability in the OTP in Synology DiskStation Manager (DSM) before 7.3.2-86009-5 and 7.4.1-90080-1 allows remote attackers with valid user credentials to read or write arbitrary files and conduct denial-of-service attacks.

### CVE-2026-67541

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-266;CWE-862` |
| Published | 2026-11-11T22:17:28.620 |

Heym builds and runs agentic systems and business-process automations on self-hosted infrastructure. Prior to version 0.0.70, team-member management (add / remove / update) is gated only on team membership, not on the team creator/admin role — and TeamMember has no role column. Any non-creator member can seat an attacker account into the team; because credential team-shares are scoped only by TeamMember.user_id, the newly-added attacker can then decrypt every credential shared into that team (provider API keys, OAuth tokens. This issue has been patched in version 0.0.70.

### CVE-2026-126245

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-11T22:17:24.280 |

A out-of-bounds write vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an unauthenticated attacker to execute unauthorized code or commands via http requests, should the attacker be able to defeat ASLR protections.

### CVE-2026-126177

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-91` |
| Published | 2026-11-11T22:17:16.157 |

A xml injection (aka blind xpath injection) vulnerability in Fortinet FortiAnalyzer 8.0.0, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiAnalyzer Cloud 8.0.0, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.0, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an unauthenticated remote attacker to inject arbitary content into a signed SAML response via crafted SAML requests.

### CVE-2026-126176

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-91` |
| Published | 2026-11-11T22:17:15.950 |

A xml injection (aka blind xpath injection) vulnerability in Fortinet FortiAnalyzer 8.0.0, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiAnalyzer Cloud 8.0.0, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.0, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an unauthenticated remote attacker to inject arbitary content into a signed SAML response via crafted SAML requests.

### CVE-2026-126163

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-11-11T22:17:14.403 |

A use of externally-controlled format string vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1 may allow a remote unauthenticated attacker to execute unauthorized code or commands via a specially crafted SMTP command.

### CVE-2026-121528

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-11T22:17:11.250 |

A improper certificate validation vulnerability in Fortinet FortiOS 7.6.0 through 7.6.4, FortiOS 7.4.0 through 7.4.9, FortiOS 7.2.0 through 7.2.13 may allow a remote and unauthenticated attacker to perform a Man-in-the-Middle attack on the communication channel between the SSLVPN web portal and the backend destination website.

### CVE-2026-126815

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-11T20:17:07.540 |

Pre-account hijacking in the authentication flow in Lagarto Chivato 0.4.1 and earlier on Web allows remote unauthenticated attackers to take over arbitrary accounts via a password planted on an unregistered email address that becomes valid upon the victim’s first passwordless login.

### CVE-2026-123872

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-11T19:17:34.270 |

A client certificate authentication bypass in Node.js TLS lets a client change the servername during TLS 1.2 renegotiation to reach endpoints it was not authorized for. On a server that applies different client-certificate policies per hostname, for example stricter admin-only client-cert auth on one host and ordinary client-cert auth on another, a client that authenticates for a permitted host can renegotiate the TLS 1.2 connection under a different servername and carry its existing authentication to the protected host, bypassing the stricter policy. This vulnerability affects Node.js 26.x, 24.x, and 22.x.

### CVE-2026-123864

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:L/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-11T19:17:32.790 |

A re-entrancy flaw in Node.js HTTPS lets an unauthenticated client read memory belonging to other connections, including TLS private keys and other users' requests. TLSWrap::DoWrite() calls ClearOut() directly when asked to write zero bytes; if that write is issued from JavaScript running inside the HTTP parser's on_body callback, ClearOut() decrypts the next TLS record while the parser is still mid-body, re-entering llhttp_execute() and causing a use-after-free and an out-of-bounds heap read. The server then copies that freed or unrelated heap memory into the response for the request body. Triggering it requires a handler that calls res.flushHeaders() before the request body ends and later calls res.end() with a non-empty chunk, and reading the leaked memory requires any ordinary route that echoes or stores a request body. Cleartext node:http is not affected. This vulnerability affects Node.js 26.x, 24.x, and 22.x.

### CVE-2026-107247

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-11T18:18:24.560 |

An authorization bypass in Revive Adserver 6.0.0 through 6.0.8 allows an authenticated manager restricted to one agency to access or modify resources belonging to another agency. Global input registration gives GET parameters precedence over POST parameters, while submitted administration forms use POST values. By supplying authorized object identifiers in the query string and different identifiers in the POST body, an attacker can cause permission checks and subsequent operations to target different objects. This permits unauthorized cross-agency changes, campaign ownership reassignment and disclosure of campaign and banner data. The regression was introduced in commit 156dee7bc3283c128f35e5a31bb305054cc8de1b and is fixed in Revive Adserver 6.0.9 by restoring POST precedence in global input registration.

### CVE-2026-118632

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-12T03:17:10.190 |

Philips Hue Bridge Pro SQL Injection Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of Philips Hue Bridge Pro. Although authentication is required to exploit this vulnerability, the existing authentication mechanism can be bypassed.

The specific flaw exists within the HTTP service, which listens on TCP port 443 by default. The issue results from the lack of proper validation of a user-supplied string before using it to construct SQL queries. An attacker can leverage this vulnerability to execute code in the context of root. Was ZDI-CAN-33089.

### CVE-2026-126181

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-11T22:17:16.987 |

A use of hard-coded credentials vulnerability in Fortinet FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2 all versions may allow an adjacent-network authenticated attacker with user permission to join the FGFM configuration-sync mesh of the affected FortiGate deployment via the default pre-shared key.

### CVE-2026-92083

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-12T14:17:30.737 |

Missing Authorization vulnerability in TÜBİTAK BİLGEM Yazılım Teknolojileri Araştırma Enstitüsü pardus-image-writer allows Privilege Escalation.

This issue affects pardus-image-writer: before 0.9.0.

### CVE-2026-123039

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732;CWE-862` |
| Published | 2026-11-12T14:17:24.233 |

The Gaia OS DynamicCLI daemon runs as root and listens on a world-writable local socket (/tmp/dynamic_socket) without authenticating connecting processes. An authenticated local user can send a command to the socket and have it executed as root.

### CVE-2026-124705

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-601` |
| Published | 2026-11-12T12:18:22.260 |

In Progress® Telerik® UI for .NET MAUI prior to version 16.0.0, an untrusted URL redirection vulnerability in the RadRichTextEditor hyperlink handling and the RadPdfViewer link annotation handling allows an unauthenticated attacker to launch arbitrary operating system protocol handlers with attacker-controlled arguments via a crafted document or PDF link with a non-allowlisted URI scheme that the user opens.

### CVE-2026-124704

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-12T11:17:10.923 |

In Telerik UI for WPF, versions prior to 2026.4.1110, a deserialization of untrusted data vulnerability exists that allows an attacker to perform unauthorized actions in the context of the affected application.

### CVE-2026-124703

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-12T11:17:10.743 |

In Telerik UI for WPF, versions prior to 2026.4.1110, an improper control of code generation vulnerability exists that allows an attacker to execute unauthorized code in the context of the affected application.

### CVE-2026-124701

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-12T11:17:10.473 |

In Telerik UI for WinForms, versions prior to 2026.4.1111, a deserialization of untrusted data vulnerability exists that allows an attacker to perform unauthorized actions in the context of the affected application.

### CVE-2026-124699

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-12T10:17:28.723 |

In Telerik UI for WinForms, versions prior to 2026.4.1111, an improper control of code generation vulnerability exists that allows an attacker to supply a crafted expression and execute unauthorized code in the context of the affected application.

### CVE-2026-87772

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-12T07:16:47.580 |

Incorrect Authorization vulnerability in TÜBİTAK BİLGEM Software Technologies Research Institute Pardus About allows Privilege Escalation.

This issue affects Pardus About: before 1.2.5.

### CVE-2026-121753

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-12T03:17:11.093 |

Ashlar-Vellum Cobalt XE File Parsing Use-After-Free Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Ashlar-Vellum Cobalt. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of XE files. The issue results from the lack of validating the existence of an object prior to performing operations on the object. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28587.

### CVE-2026-121752

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-12T03:17:10.907 |

Ashlar-Vellum Cobalt LI File Parsing Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Ashlar-Vellum Cobalt. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of LI files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28447.

### CVE-2026-121744

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-12T03:17:10.763 |

Ashlar-Vellum Cobalt XE File Parsing Stack-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Ashlar-Vellum Cobalt. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of XE files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a stack-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28172.

### CVE-2026-121743

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-12T03:17:10.600 |

Ashlar-Vellum Cobalt AR File Parsing Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Ashlar-Vellum Cobalt. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of AR files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28675.

### CVE-2026-121742

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-12T03:17:10.447 |

Ashlar-Vellum Cobalt XE File Parsing Use-After-Free Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Ashlar-Vellum Cobalt. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of XE files. The issue results from the lack of validating the existence of an object prior to performing operations on the object. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28757.

### CVE-2026-121741

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-12T03:17:10.323 |

Trimble SketchUp SKP File Parsing Use-After-Free Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Trimble SketchUp. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of SKP files. The issue results from the lack of validating the existence of an object prior to performing operations on the object. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-30421.

### CVE-2026-114569

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-12T03:17:09.917 |

OriginLab Origin Viewer OGWU File Parsing Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab Origin Viewer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OGWU files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-30430.

### CVE-2026-114568

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-12T03:17:09.783 |

OriginLab Origin Viewer OPJ File Parsing Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab Origin Viewer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OPJ files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-31587.

### CVE-2026-114567

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-12T03:17:09.657 |

OriginLab Origin Viewer OGWU File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab Origin Viewer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OGWU files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated data structure. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-30771.

### CVE-2026-114566

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-11-12T03:17:09.527 |

OriginLab Origin Viewer OGM File Parsing Memory Corruption Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab Origin Viewer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OGM files. The issue results from the lack of proper validation of user-supplied data, which can result in a memory corruption condition. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-30770.

### CVE-2026-114565

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-12T03:17:09.397 |

OriginLab Origin Viewer OGG File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab Origin Viewer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OGG files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated data structure. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-30769.

### CVE-2026-114564

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-12T03:17:09.250 |

OriginLab Origin Viewer OGG File Parsing Out-Of-Bounds Write  Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab Origin Viewer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OGG files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated data structure. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-30768.

### CVE-2026-114563

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-12T03:17:09.110 |

OriginLab Origin Viewer OGWU File Parsing Stack-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab Origin Viewer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OGWU files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a stack-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-30737.

### CVE-2026-114562

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-12T03:17:08.980 |

OriginLab Origin Viewer OGWU File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab Origin Viewer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OGWU files. The issue results from the lack of proper validation of user-supplied data, which can result in a write before the start of an allocated data structure. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-30736.

### CVE-2026-114561

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-12T03:17:08.843 |

OriginLab Origin Viewer OPJU File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab Origin Viewer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OPJU files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated data structure. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-30433.

### CVE-2026-114560

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-12T03:17:08.700 |

OriginLab Origin Viewer OPJ File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab Origin Viewer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OPJ files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated data structure. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-30432.

### CVE-2026-114559

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-12T03:17:08.560 |

OriginLab Origin Viewer OGG File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab Origin Viewer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OGG files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated data structure. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-30431.

### CVE-2026-114558

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-12T03:17:08.417 |

OriginLab Origin Viewer OPJU File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab Origin Viewer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OPJU files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated data structure. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-30738.

### CVE-2025-10935

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-12T03:17:08.107 |

libilbm ILBM File Parsing Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of libilbm. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of ILBM files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-27792.

### CVE-2026-108472

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-11T19:17:29.070 |

A flaw was found in the xfs_admin utility in xfsprogs. The tool does not properly validate user-supplied parameters, allowing operating system command injection. A local attacker can exploit this issue by providing crafted input arguments, which may result in arbitrary command execution and local privilege escalation depending on how xfs_admin is executed.

### CVE-2026-126781

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-11-11T19:17:39.177 |

Webmin through 2.670 contains a users file injection vulnerability in acl/cert_issue.cgi that allows authenticated Webmin users to inject lines by supplying unvalidated certificate DN fields containing newlines. Attackers can end a DN field with a backslash and newline to add a second root entry with a known password hash, gaining Webmin root access after miniserv restarts.

### CVE-2026-65971

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-11T22:17:28.090 |

Livewire PowerGrid creates data tables based on Laravel Livewire library. From version 6.0.0 to before version 6.10.4, the public Livewire property sortDirection is interpolated verbatim into a raw SQL ORDER BY clause and is not restricted to asc/desc, allowing arbitrary SQL injection through POST /livewire/update. This issue has been patched in version 6.10.4.

### CVE-2026-126152

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-11T22:17:12.877 |

A authorization bypass through user-controlled key vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow an authenticated remote attacker to delete arbitrary directories as root, or to access or delete other users' calendar and mailbox data across tenant domains, via crafted HTTP requests to the webmail and administrative interfaces.

### CVE-2026-122095

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T20:17:07.023 |

AsiaInfo BSS Platform 9.2 before 9.2.38 has a stored cross-site scripting (XSS) vulnerability in the menu icon upload function. An authenticated user with ordinary application privileges can upload an SVG file containing embedded JavaScript, which is served from the application origin. Normal menu rendering uses an HTML <img> element and does not execute the SVG script; exploitation requires a victim to load the uploaded SVG as a document (by directly navigating to its URL, or via <object>/<iframe>), in which case the script executes under the application origin.

### CVE-2026-91878

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-91` |
| Published | 2026-11-11T19:17:47.917 |

Dell OpenManage Ansible Modules, versions 6.0.0 through 10.0.3, contains an Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection') vulnerability in the XML data conversion component. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to XML injection, malicious content injection, and XML parsing errors

### CVE-2026-91877

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-11T19:17:47.773 |

Dell OpenManage Ansible Modules, versions 2.0.2 through 10.0.3, contains an Improper Neutralization of Special Elements in Data Query Logic vulnerability in the OData filter processing component. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to unauthorized data access, authorization bypass, and denial of service.

### CVE-2026-110951

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-11-12T13:17:08.390 |

Weak Password Recovery Mechanism for Forgotten Password vulnerability in Hyper Teknoloji Ltd. Şti. Hyper E-Commerce Infrastructure, Hyper Teknoloji Ltd. Şti. Hyper E-Commerce Infrastructure - dealer integration, and Hyper Teknoloji Ltd. Şti. Hyper E-Commerce Infrastructure - Storefront application and management panel allows Password Recovery Exploitation.

This issue affects Hyper E-Commerce Infrastructure: before 1.1; Hyper E-Commerce Infrastructure - dealer integration: before 1.2; Hyper E-Commerce Infrastructure - Storefront application and management panel: before 2.1796.

### CVE-2026-123092

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-12T06:17:13.023 |

The WP Remote Users Sync WordPress plugin before 2.3.0 does not restrict which user metadata keys may be written through its incoming user synchronisation requests, allowing a site that holds the shared synchronisation keys to set the capabilities of any existing account and escalate it to administrator.

### CVE-2026-123044

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-12T06:17:12.920 |

The ContentPen WordPress plugin before 1.1.1 discloses its REST API key to unauthenticated users, who can then use it to create posts containing unfiltered JavaScript, leading to Stored XSS that executes in the browser of any visitor, including administrators.

### CVE-2026-119040

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-12T06:17:12.257 |

The Defender Security  WordPress plugin before 6.4.1 does not limit the number of failed two-factor authentication attempts in its default configuration, allowing an attacker who already knows a victim's password to brute-force the one-time code and defeat the second authentication factor.

### CVE-2026-18633

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-824` |
| Published | 2026-11-12T04:17:19.007 |

An access of uninitialized pointer vulnerability in the nfsd in Synology DiskStation Manager (DSM) before 7.3.2-86009-5 and 7.4.1-90080-1 allows remote attackers to conduct denial-of-service attacks.

### CVE-2026-13270

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-12T03:17:11.913 |

Quest NetVault Backup nvpmgr Integer Underflow Denial-of-Service Vulnerability. This vulnerability allows remote attackers to create a denial-of-service condition on affected installations of Quest NetVault Backup. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the nvpmgr service, which listens on UDP port 20031 by default. The issue results from the lack of proper validation of user-supplied data, which can result in an integer underflow before allocating a buffer. An attacker can leverage this vulnerability to create a denial-of-service condition on the system. Was ZDI-CAN-28744.

### CVE-2026-13269

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-197` |
| Published | 2026-11-12T03:17:11.777 |

Quest NetVault Backup StnzCreateKey Numeric Truncation Error Denial-of-Service Vulnerability. This vulnerability allows remote attackers to create a denial-of-service condition on affected installations of Quest NetVault Backup. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the StnzCreateKey function. The issue results from the lack of proper validation of user-supplied data, which can result in a numeric truncation error before allocating a buffer. An attacker can leverage this vulnerability to create a denial-of-service condition on the system. Was ZDI-CAN-28743.

### CVE-2026-68540

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-405` |
| Published | 2026-11-11T22:17:30.677 |

fulgur converts untrusted HTML/CSS into PDF, commonly on a server that processes input supplied by many tenants. From version 0.6.0 to before version 0.33.0, quadratic style-list reprocessing during containing-block resolution for absolutely-positioned pseudo-elements cause denial of service. This issue has been patched in version 0.33.0.

### CVE-2026-68539

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-11-11T22:17:30.480 |

fulgur converts untrusted HTML/CSS into PDF, commonly on a server that processes input supplied by many tenants. From version 0.4.4 to before version 0.29.0, the CSS string-set named-string values resolved from a document were accumulated per element with no memory budget, letting a small crafted document amplify into large retained memory (and the CPU to copy it) — results in a denial of service. This issue has been patched in version 0.29.0.

### CVE-2026-68538

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-11T22:17:30.313 |

fulgur converts untrusted HTML/CSS into PDF, commonly on a server that processes input supplied by many tenants. From version 0.15.0 to before version 0.27.0, resolving the CSS counters(name, sep) function in generated content was bounded neither in the size of a single expansion nor in the aggregate work across an element tree. An attacker able to submit HTML/CSS to a fulgur-based conversion service can trigger CPU and memory exhaustion with a trivially small payload, denying service to the host and any co-tenants. This issue has been patched in version 0.27.0.

### CVE-2026-126258

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-11T22:17:26.073 |

A stack-based buffer overflow vulnerability in Fortinet FortiOS 8.0.0, FortiOS 7.6.7 may allow an unauthenticated attacker with wad port access to crash proxy or ZTNA sessions via crafted HTTP or HTTPS requests.

### CVE-2026-126248

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-11T22:17:24.693 |

A insufficiently protected credentials vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an unauthenticated attacker to obtain sensitive information via HTTPS requests.

### CVE-2026-126246

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-11T22:17:24.423 |

A null pointer dereference vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an unauthenticated attacker to perform a denial of service attack via http requests.

### CVE-2026-126244

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-11T22:17:24.147 |

A allocation of resources without limits or throttling vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an unauthenticated attacker to exhaust system resources, potentially resulting in a denial of service (DoS).

### CVE-2026-126239

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-11T22:17:23.460 |

A stack-based buffer overflow vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an unauthenticated attacker to crash the FSSO subsystem via crafted http requests

### CVE-2026-126237

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-11T22:17:23.177 |

A loop with unreachable exit condition ('infinite loop') vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an attacker to cause a denial of service via crafted TCP requests.

### CVE-2026-126232

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-11T22:17:22.157 |

A improper certificate validation vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2 all versions, FortiAnalyzer Cloud 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2 all versions, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2 all versions, FortiManager Cloud 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2 all versions may allow a MITM attacker to impersonate the radius server via a rogue RADIUS server.

### CVE-2026-126165

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-11-11T22:17:14.673 |

A memory allocation with excessive size value vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow a remote unauthenticated attacker to cause a denial of service via a specially crafted attachment delivered over SMTP.

### CVE-2026-126161

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-11T22:17:14.123 |

A uncontrolled resource consumption vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.6 may allow a remote unauthenticated attacker to cause a denial of service via repeated unauthenticated POST requests.

### CVE-2026-126159

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-11T22:17:13.857 |

A authorization bypass through user-controlled key vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow an unauthenticated attacker to release or delete quarantined messages for arbitrary mailboxes via a crafted quarantine release request.

### CVE-2026-126154

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-11T22:17:13.190 |

A out-of-bounds write vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow a remote unauthenticated attacker to cause a denial of service via a specially crafted HTTP request.

### CVE-2026-126153

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-11T22:17:13.050 |

A improper limitation of a pathname to a restricted directory ('path traversal') vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow an unauthenticated attacker to execute unauthorized commands via crafted requests.

### CVE-2026-126151

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-303` |
| Published | 2026-11-11T22:17:12.720 |

A incorrect implementation of authentication algorithm vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow an unauthenticated remote attacker to gain elevation of privilege (account takeover) via a crafted request.

### CVE-2026-126149

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-11T22:17:12.137 |

A integer overflow or wraparound vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow a remote unauthenticated attacker to crash the daemon.

### CVE-2026-91891

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-532` |
| Published | 2026-11-11T19:17:48.213 |

Dell Terraform Provider for PowerStore, versions prior to 1.3.1 , contains a  vulnerability that may cause sensitive authentication data to be insufficiently redacted in diagnostic logs. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to information exposure.

### CVE-2026-91150

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-11T19:17:47.043 |

A flaw was found in Cockpit. This vulnerability allows a remote attacker, without prior authentication, to send specially crafted fragmented WebSocket messages. These messages accumulate without a total-size limit, leading to unbounded memory exhaustion and a denial of service in the `cockpit-ws` service.

### CVE-2026-58505

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-11-11T19:17:42.580 |

geojson-vt is a JavaScript library for slicing GeoJSON data into vector tiles on the fly, primarily designed to enable rendering and interacting with large geospatial datasets on the browser side (without a server). Prior to version 6.1.1, @maplibre/geojson-vt contains an uncontrolled recursion vulnerability in its GeoJSON conversion logic. When a GeoJSONVT instance is constructed with a deeply nested GeometryCollection object, the mutually recursive functions featureToInternal and convertGeometryCollection in src/convert.ts exhaust the Node.js call stack, causing an unhandled RangeError: Maximum call stack size exceeded that terminates the process. Because the library is widely used in server-side tile services that accept GeoJSON over the network, a remote unauthenticated attacker can trigger a denial-of-service by sending a single crafted payload. No authentication is required, and no non-default library options are needed. This issue has been patched in version 6.1.1.

### CVE-2026-126051

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-11T19:17:36.600 |

A deferred-callback use-after-destroy in Node.js TLS server handshake handling allows a remote, unauthenticated attacker to terminate the server process. When a TLS server uses any of the SNICallback, OCSPRequest, newSession, or resumeSession hooks, or server.addContext(), the corresponding OpenSSL callbacks are deferred, and the deferred code does not handle the underlying socket being destroyed between scheduling and execution. By sending a client hello that reaches the vulnerable path (for example, no SNI together with an OCSP request) followed by padding and a socket FIN, an attacker makes OpenSSL deliver the client hello and the end-of-file in the same tick, so the socket is destroyed before the deferred callback runs and the process raises an uncaught exception instead of emitting an 'error' event. This vulnerability affects Node.js 26.x and 24.x.

### CVE-2026-123874

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-11T19:17:34.490 |

A use-after-free in Node.js HTTP/2 lets an unauthenticated client corrupt server memory, over both TLS and cleartext, when the server serves files with respondWithFile() or respondWithFD(). A client can make the server free an Http2Stream while a write request that points to it is still queued on the socket; when that write completes, the code dereferences and makes a virtual call through the freed object. The only precondition is that the application serves a file with stream.respondWithFile() or stream.respondWithFD(), with default settings otherwise. This vulnerability affects Node.js 26.x (since 26.9.0) and 24.x (since 24.22.0).

### CVE-2026-123866

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-11T19:17:33.243 |

A use-after-free in Node.js HTTP/2 stream teardown can leak response memory, including the contents of other connections' response buffers, to a peer. When a stream is torn down while a write is still backpressured, for example by a peer RST_STREAM or by the server's own per-stream timeout destroying the stream, the stream's response buffer is freed but a reference to it is still used, so freed or unrelated heap memory is written to the socket instead of the intended response. On Node.js 26.x and 24.x the teardown can be driven purely by a remote peer once the window-size change from 26.9.0 and 24.22.0 is present, and on all supported lines the same defect is reachable through an application-initiated teardown such as a per-stream idle timeout. This vulnerability affects Node.js 26.x, 24.x, and 22.x.

### CVE-2026-123865

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-11T19:17:33.000 |

An unauthenticated HTTP/2 client can permanently leak Node.js server memory and file descriptors. If a peer triggers a protocol error, for example an oversized frame header, while the session is already shutting down, nghttp2 tears the session down internally but Node.js never notices, leaving a dangling session: the socket stays in CLOSE_WAIT and all of Node.js's HTTP/2 state for that connection is held in memory indefinitely, with no further cost to the attacker. The attacker can start the shutdown remotely by sending GOAWAY(NO_ERROR), so it is reliable against default HTTP/2 servers. It is an incomplete-fix case of CVE-2026-48937: that fix detected nghttp2 internal terminations by watching for GOAWAY sent while not shutting down, but missed terminations that arrive while the session is already shutting down. This vulnerability affects Node.js 26.x, 24.x, and 22.x.

### CVE-2026-111435

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-12T04:17:17.483 |

Relative path traversal vulnerability in openEuler iSulad on Linux.

This vulnerability is associated with program file src/daemon/modules/image/oci/oci_load.c.



This issue affects iSulad: through 2.1.6.



In oci_load.c, oci_load_process_manifest() does not sanitize the Config path of manifest.json. A malicious tar package can enable the isulad with the root permission to read any file on the host.

### CVE-2026-114556

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-12T03:17:08.277 |

MailEnable Save Directory Traversal Arbitrary File Creation Vulnerability. This vulnerability allows remote attackers to create arbitrary files on affected installations of MailEnable. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the implementation of the Save method. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this in conjunction with other vulnerabilities to execute code in the context of SYSTEM. Was ZDI-CAN-29161.

### CVE-2026-67545

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-11T22:17:29.360 |

Heym builds and runs agentic systems and business-process automations on self-hosted infrastructure. Prior to version 0.0.73, the HTTP workflow node in Heym makes outbound HTTP requests to user-supplied URLs without validation of the target host or IP address. If a workflow author has already configured an HTTP node that targets internal addresses such as cloud metadata endpoints or private network hosts, and exposed the workflow with anonymous execution, an unauthenticated attacker can trigger the preconfigured SSRF sink. The same project has comprehensive SSRF protection in its MCP integration, which is absent from the HTTP node. This issue has been patched in version 0.0.73.

### CVE-2026-126256

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-11T22:17:25.783 |

A out-of-bounds read vulnerability in Fortinet FortiOS 8.0.0 through 8.0.1, FortiOS 7.6.0 through 7.6.7, FortiOS 7.4.0 through 7.4.12, FortiOS 7.2.0 through 7.2.13 may allow a remote privileged attacker to execute arbitrary code or command via crafted paquets.

### CVE-2026-126255

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-24` |
| Published | 2026-11-11T22:17:25.623 |

A path traversal: '../filedir' vulnerability in Fortinet FortiOS 8.0.0 through 8.0.1, FortiOS 7.6.0 through 7.6.7, FortiOS 7.4.0 through 7.4.12, FortiOS 7.2.0 through 7.2.13, FortiPAM 1.6 all versions, FortiPAM 1.5 all versions, FortiPAM 1.4 all versions, FortiPAM 1.3 all versions, FortiPAM 1.2 all versions, FortiPAM 1.1 all versions, FortiPAM 1.0 all versions may allow an unauthenticated attacker to bypass authentication via specially crafted credentials.

### CVE-2026-126242

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-11T22:17:23.893 |

A incorrect authorization vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an attacker to bypass authentication and gain unauthorized access. Full impersonation however requires the attacker to obtain pre-required id and data via other means.

### CVE-2026-126813

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-11-11T21:16:45.883 |

Roundcube Webmail before 1.6.21 and 1.7.x before 1.7.6 contains an IMAP command injection vulnerability that allows attackers to inject commands via CRLF in the _uid parameter when messages_cache is enabled. Attackers can lure logged-in victims into opening crafted GET links to mail/show or mail/get, executing IMAP commands that delete messages, change flags, or grant mailbox access via SETACL.

### CVE-2026-91871

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-11T18:19:53.223 |

Dell Ansible Storage for PowerStore, versions prior to 3.9.0, contains an Improper Certificate Validation vulnerability in the API client component. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to information exposure and unauthorized access.

### CVE-2026-91870

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-11T18:19:53.087 |

Dell Ansible Storage for PowerFlex, versions prior to 3.2.0, contains an Improper Certificate Validation vulnerability in the API client component. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to information exposure and unauthorized access.

### CVE-2026-107484

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-12T14:17:22.897 |

An input and authorization validation vulnerability in Gaia Portal backend handlers could allow an authenticated, non-administrative user to perform privileged operations that should be restricted to administrators.

### CVE-2026-106140

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-12T10:17:26.987 |

In Progress® Telerik® Reporting prior to version 20.3.26.1110, a deserialization of untrusted data vulnerability in the .NET Framework report designers allows a local attacker with low privileges to execute arbitrary code in the context of the designer process when the user performs certain editing operations.

### CVE-2026-47832

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-11-12T08:16:41.947 |

The vulnerability lies in the way application credentials are handled within the BOSH deployment.
bosh-openstack-cpi-release: all versions from v55 to v55.0.4 (inclusive)

### CVE-2026-91151

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-11T20:17:10.557 |

A flaw was found in Cockpit. A local authenticated user with control over a target account's home directory can exploit a privileged symlink dereference vulnerability in the `ssh-add-public-key.sh` helper. When this helper runs with elevated privileges, it can be tricked into following attacker-controlled symlinks within the `.ssh` or `authorized_keys` paths. This allows the attacker to arbitrarily change file ownership and modes, potentially leading to local privilege escalation and impacting the integrity, confidentiality, and availability of the system.

### CVE-2026-123747

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:R/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-11T19:17:30.467 |

A flaw was found in pappl-retrofit. The application fails to properly sanitize user-supplied filenames when handling the upload and deletion of PostScript Printer Description (PPD) files. A remote, unauthenticated attacker can exploit this directory traversal flaw by submitting filenames containing path traversal sequences. This allows the attacker to upload or delete arbitrary files on the system, which can result in data corruption, denial of service, or arbitrary command execution.

### CVE-2026-118597

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-12T06:17:11.980 |

Akaunting 3.3.0 contains a stored cross-site scripting vulnerability in custom invoice payment terms. An authenticated Manager can save a crafted custom payment-term value. When an authorized user opens Invoice Settings for the same company, Akaunting inserts the stored value into a client-side event-handler expression, causing attacker-controlled JavaScript to execute in the victim's authenticated origin.

### CVE-2026-75785

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-12T04:17:20.213 |

An improper neutralization of special elements used in an OS command vulnerability in the VPN API in Synology DiskStation Manager (DSM) before 7.3.2-86009-5 and 7.4.1-90080-1 allows remote authenticated users with administrator privileges to read or write arbitrary files and conduct denial-of-service attacks.

### CVE-2026-125637

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-11T23:17:10.750 |

A flaw was found in the Konflux UI proxy. Hostname values defined in the KonfluxUI custom resource are inserted directly into proxy configuration files without adequate validation or sanitization. An authenticated user with permissions to modify the custom resource can inject malicious configuration directives to bypass authentication and authorization controls, potentially exposing internal backend services. In addition, providing malformed input can cause the configuration generator to fail, resulting in a denial of service (DoS) by preventing the proxy from starting.

### CVE-2026-126249

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-11T22:17:24.823 |

A improper privilege management vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an authenticated attacker to escalate privileges.

### CVE-2026-126247

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-11-11T22:17:24.560 |

A use of externally-controlled format string vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an authenticated privileged attacker to execute unauthorized code or commands via http requests.

### CVE-2026-126243

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-11T22:17:24.020 |

A incorrect authorization vulnerability in Fortinet FortiAuthenticator 8.0.0 through 8.0.3, FortiAuthenticator 6.6.0 through 6.6.10 may allow an attacker to bypass authentication and gain unauthorized access. Full impersonation however requires the attacker to obtain pre-required id and data via other means.

### CVE-2026-126236

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-11T22:17:22.960 |

A improper neutralization of special elements used in an os command ('os command injection') vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiAnalyzer Cloud 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an authenticated attacker to execute unauthorized code or commands via specially crafted HTTP requests

### CVE-2026-126235

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-11T22:17:22.753 |

A improper limitation of a pathname to a restricted directory ('path traversal') vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.2 through 7.6.7, FortiAnalyzer 7.4.7 through 7.4.11, FortiAnalyzer 7.2.10 through 7.2.12, FortiAnalyzer Cloud 8.0.0 through 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.2 through 7.6.7, FortiManager 7.4.7 through 7.4.11, FortiManager 7.2.10 through 7.2.12, FortiManager Cloud 8.0.0 through 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an authenticated administrator to write arbitrary files via a specially crafted archive.

### CVE-2026-126234

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-11-11T22:17:22.607 |

A improper neutralization of special elements used in a template engine vulnerability in Fortinet FortiAnalyzer 8.0.0, FortiAnalyzer Cloud 8.0.0, FortiManager 8.0.0, FortiManager Cloud 8.0.0 may allow an authenticated attacker with restricted privileges to execute unauthorized code or commands via a specially crafted request.

### CVE-2026-126233

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-11T22:17:22.377 |

A unrestricted upload of file with dangerous type vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiAnalyzer Cloud 8.0.0 through 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.0 through 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an authenticated administrator to upload arbitrary files via specially crafted requests.

### CVE-2026-126231

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-11T22:17:21.930 |

A improper neutralization of special elements used in an os command ('os command injection') vulnerability in Fortinet FortiAnalyzer 8.0.0, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2 all versions, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2 all versions, FortiManager 8.0.0, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2 all versions, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2 all versions may allow an authenticated attacker to execute unauthorized commands via a crafted HTTP request.

### CVE-2026-126230

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-11-11T22:17:21.697 |

A use of externally-controlled format string vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiAnalyzer Cloud 8.0.0 through 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.0 through 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an authenticated administrator to execute unauthorized code or commands or cause a denial of service via specially crafted requests.

### CVE-2026-126228

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-11T22:17:21.243 |

A out-of-bounds write vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.4 through 7.2.12, FortiAnalyzer Cloud 8.0.0 through 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.4 through 7.2.12, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.4 through 7.2.12, FortiManager Cloud 8.0.0 through 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.4 through 7.2.12 may allow an authenticated remote attacker with admin privileges to execute unauthorized code or commands via a specially crafted request.

### CVE-2026-126227

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-11T22:17:21.003 |

A unintended proxy or intermediary ('confused deputy') vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiAnalyzer Cloud 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an authenticated attacker to execute commands outside of the intended scope via specially crafted HTTP request

### CVE-2026-126226

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-11T22:17:20.793 |

A improper neutralization of special elements used in an os command ('os command injection') vulnerability in Fortinet FortiAnalyzer 8.0.0, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiAnalyzer Cloud 8.0.0, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.0, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an authenticated privileged attacker to execute unauthorized code or commands via crafted report schedule name.

### CVE-2026-126224

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-11T22:17:20.437 |

A improper neutralization of argument delimiters in a command ('argument injection') vulnerability in Fortinet FortiAnalyzer 8.0.0, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiAnalyzer Cloud 8.0.0, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.0, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an authenticated privileged admin user to execute unauthorized code or commands.

### CVE-2026-126223

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-11T22:17:20.243 |

A stack-based buffer overflow vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer Cloud 8.0.0 through 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager Cloud 8.0.0 through 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11 may allow an authenticated administrator to execute unauthorized code or commands or cause a denial of service via specially crafted JSON-RPC requests.

### CVE-2026-126222

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-11T22:17:20.100 |

A improper limitation of a pathname to a restricted directory ('path traversal') vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.3 through 7.6.7, FortiAnalyzer Cloud 8.0.0 through 8.0.1, FortiAnalyzer Cloud 7.6.3 through 7.6.7, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.3 through 7.6.7, FortiManager Cloud 8.0.0 through 8.0.1, FortiManager Cloud 7.6.3 through 7.6.7 may allow an authenticated attacker with admin privileges to execute unauthorized code or commands via crafted requests.

### CVE-2026-126221

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-11-11T22:17:19.930 |

A improper neutralization of special elements in output used by a downstream component ('injection') vulnerability in Fortinet FortiAnalyzer 8.0.0, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer Cloud 8.0.0, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiManager 8.0.0, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager Cloud 8.0.0, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11 may allow an authenticated administrator to read or write arbitrary files or execute unauthorized code or commands via specially crafted requests to the GUI.

### CVE-2026-126220

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-11-11T22:17:19.790 |

A improper neutralization of special elements in output used by a downstream component ('injection') vulnerability in Fortinet FortiManager 8.0.0, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11 may allow an authenticated administrator to read or write arbitrary files or execute unauthorized code or commands via specially crafted requests to the GUI.

### CVE-2026-126219

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-11T22:17:19.610 |

A improper limitation of a pathname to a restricted directory ('path traversal') vulnerability in Fortinet FortiAnalyzer 8.0.0, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer Cloud 8.0.0, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiManager 8.0.0, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager Cloud 8.0.0, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11 may allow an authenticated administrator to read or write arbitrary files or execute unauthorized code or commands via specially crafted requests to the GUI.

### CVE-2026-126214

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-11T22:17:18.663 |

A authentication bypass by spoofing vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiAnalyzer Cloud 8.0.0 through 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12 may allow an authenticated administrator to escalate their privileges, bypass authorization controls or impersonate internal services via specially crafted requests to the GUI.

### CVE-2026-126212

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-11T22:17:18.263 |

A heap-based buffer overflow vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer Cloud 8.0.0 through 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager Cloud 8.0.0 through 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11 may allow an authenticated administrator to execute unauthorized code or commands or cause a denial of service via specially crafted JSON-RPC requests.

### CVE-2026-126211

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-11T22:17:18.100 |

A improper privilege management vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.1 through 7.6.7, FortiAnalyzer Cloud 8.0.0 through 8.0.1, FortiAnalyzer Cloud 7.6.1 through 7.6.8, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.1 through 7.6.7, FortiManager Cloud 8.0.0 through 8.0.1, FortiManager Cloud 7.6.1 through 7.6.8 may allow an authenticated privileged attacker to elevate their privileges via crafted JSON-RPC request.

### CVE-2026-126185

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-11T22:17:17.830 |

A improper control of generation of code ('code injection') vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer Cloud 8.0.0 through 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager Cloud 8.0.0 through 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11 may allow an authenticated administrator to execute unauthorized code or commands via specially crafted requests.

### CVE-2026-126182

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-11T22:17:17.133 |

A improper control of generation of code ('code injection') vulnerability in Fortinet FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.0 through 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow a remote authenticated attacker to execute unauthorized code or commands via crafted HTTP requests.

### CVE-2026-126179

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-11T22:17:16.587 |

A improper neutralization of special elements used in an os command ('os command injection') vulnerability in Fortinet FortiAnalyzer 8.0.0, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiAnalyzer Cloud 8.0.0, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.0, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an authenticated administrator to execute unauthorized code or commands via specially crafted requests

### CVE-2026-126178

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-11T22:17:16.370 |

A heap-based buffer overflow vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiAnalyzer Cloud 8.0.0 through 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.0 through 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an authenticated attacker with admin privileges to execute unauthorized code or commands via a crafted request.

### CVE-2026-126171

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-11-11T22:17:15.500 |

A use of externally-controlled format string vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4.0 through 7.4.11, FortiAnalyzer 7.2.0 through 7.2.12, FortiAnalyzer Cloud 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an authenticated attacker to execute unauthorized commands via specially crafted HTTP request

### CVE-2026-126169

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-11T22:17:15.200 |

A improper neutralization of argument delimiters in a command ('argument injection') vulnerability in Fortinet FortiMail 8.0.0 through 8.0.2, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow an authenticated remote attacker with domain admin or admin privileges to delete users of other tenant domains on a paired FortiAuthenticator, execute arbitrary code as root or arbitrary CLI commands, and read or write arbitrary files as root via crafted HTTP requests to the administrative interface.

### CVE-2026-126168

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-11T22:17:15.067 |

A improper neutralization of argument delimiters in a command ('argument injection') vulnerability in Fortinet FortiMail 8.0.0 through 8.0.2, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow an authenticated remote attacker with domain admin or admin privileges to delete users of other tenant domains on a paired FortiAuthenticator, execute arbitrary code as root or arbitrary CLI commands, and read or write arbitrary files as root via crafted HTTP requests to the administrative interface.

### CVE-2026-126167

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-11T22:17:14.940 |

A improper neutralization of special elements used in a command ('command injection') vulnerability in Fortinet FortiMail 8.0.0 through 8.0.2, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow an authenticated remote attacker with domain admin or admin privileges to delete users of other tenant domains on a paired FortiAuthenticator, execute arbitrary code as root or arbitrary CLI commands, and read or write arbitrary files as root via crafted HTTP requests to the administrative interface.

### CVE-2026-126166

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-11T22:17:14.803 |

A improper neutralization of argument delimiters in a command ('argument injection') vulnerability in Fortinet FortiMail 8.0.0 through 8.0.2, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow an authenticated remote attacker with domain admin or admin privileges to delete users of other tenant domains on a paired FortiAuthenticator, execute arbitrary code as root or arbitrary CLI commands, and read or write arbitrary files as root via crafted HTTP requests to the administrative interface.

### CVE-2026-126158

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-11T22:17:13.723 |

A improper neutralization of special elements used in an os command ('os command injection') vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1 may allow an authenticated administrator to execute unauthorized code or commands as root via specially crafted HTTP requests.

### CVE-2026-126146

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-11T22:17:11.720 |

A improper neutralization of special elements used in an os command ('os command injection') vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.4, FortiMail 7.4.0 through 7.4.6, FortiMail 7.2.0 through 7.2.9, FortiRecorder 7.6.0, FortiRecorder 7.2.0 through 7.2.11, FortiRecorder 7.0.0 through 7.0.6 may allow an authenticated privileged attacker to execute unauthorized code or commands via a specifically crafted archive account configuration.

### CVE-2026-126145

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-11T22:17:11.580 |

A improper neutralization of special elements used in an os command ('os command injection') vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2 all versions may allow an authenticated administrator with system-time read-write access to execute unauthorized code or commands as root.

### CVE-2026-126804

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-11T21:16:44.173 |

WWBN AVideo 12.4 through 29.7.1 contains a path traversal vulnerability in the ADs plugin deleteImage.json.php that allows authenticated users with custom ads to delete arbitrary files. Attackers can set the unvalidated is_regular_user parameter to another user's id or ../ sequences to delete other users' ads or files like videos/configuration.php, taking the site offline and re-exposing the installer.

### CVE-2026-76079

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-863` |
| Published | 2026-11-11T19:17:44.727 |

Probo is a self-hostable governance, risk, and compliance (GRC) platform built for engineering and security teams. Prior to version 0.224.0, an organization ADMIN can mint an OWNER membership via createUser, bypassing the owner-only set-owner authorization gate. This issue has been patched in version 0.224.0.

### CVE-2026-62971

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-138` |
| Published | 2026-11-11T18:19:47.603 |

The OWASP core rule set (CRS) is a set of generic attack detection rules for use with compatible web application firewalls. Prior to versions 3.3.10, 4.25.1, and 4.28.0, CRS rules in the 921 (protocol-attack), 930 (LFI), 931 (RFI), 932 (RCE), 933 (PHP), 934 (generic), 941 (XSS), 942 (SQLi), and 943 (session-fixation) families inspect XML request bodies via the XPath expression XML:/*. That expression matches only element text nodes — it does not match XML attribute values. As a result, an attacker who places an attack payload inside an XML attribute (e.g. <a href="javascript:alert(1)=window.name"></a> or <a value="' OR 1=1 --"></a>) bypasses CRS detection entirely. This is verified empirically against a local CRS test instance and against the public CRS sandbox. The bypass affects approximately 159 rules across 9 rule files and applies at every paranoia level (PL1 through PL4), since the variable list is more or less shared across PLs. The 944 (Java) family is the only one that correctly includes XML://@* in addition to XML:/* and is therefore unaffected. This issue has been patched in versions 3.3.10, 4.25.1, and 4.28.0.

### CVE-2026-127050

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-12T13:17:16.010 |

Backup Migration before 2.1.8 for WordPress contains a path traversal vulnerability in its PclZip restore fallback that allows an attacker to achieve arbitrary file write when an administrator restores a malicious backup archive on a server lacking the PHP zip extension. Attackers can craft a zip archive with entry names containing ".." sequences, which PclZip's extract() processes without the PCLZIP_OPT_EXTRACT_DIR_RESTRICTION option, writing a PHP file outside the intended extraction directory into the web-servable tree to achieve remote code execution.

### CVE-2026-111552

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-308` |
| Published | 2026-11-12T13:17:09.637 |

Use of single-factor authentication vulnerability in Hyper Teknoloji Ltd. Şti. Hyper E-Commerce Infrastructure, Hyper Teknoloji Ltd. Şti. Hyper E-Commerce Infrastructure - dealer integration, and Hyper Teknoloji Ltd. Şti. Hyper E-Commerce Infrastructure - Storefront application and management panel allows Authentication Bypass.

This issue affects Hyper E-Commerce Infrastructure: before 1.1; Hyper E-Commerce Infrastructure - dealer integration: before 1.2; Hyper E-Commerce Infrastructure - Storefront application and management panel: before 2.1796.

### CVE-2026-81936

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-11-11T22:17:30.877 |

An internal security review identified a development regression from ThinkSystem v4 XClarity Controller 3 (XCC3) versions (2.51) IHX432Y to (2.56) IHX436K which re-introduces the default OpenBMC root password upon performing an XCC Reset to Default operation.  An attacker can gain access to enabled administrative interfaces of XCC using the default OpenBMC credential re-introduced after Reset to Default. Additionally, this provides access to the underlying XCC Operating System which is not normally accessible. Only these versions are affected and are no longer available for download. Process enhancements have also been made to prevent and identify potential future regression.

### CVE-2026-67542

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-11T22:17:28.813 |

Heym builds and runs agentic systems and business-process automations on self-hosted infrastructure. Prior to version 0.0.70, POST /api/mcp/fetch-tools is reachable by any authenticated user (lowest role; no admin/workflow association) and fetches an attacker-supplied URL through the sse and streamable_http transports with no scheme / private-IP / allowlist / redirect guard. The transport error is reflected in the HTTP 422 response, giving a semi-blind SSRF oracle, and the attacker also controls the outbound request headers. This issue has been patched in version 0.0.70.

### CVE-2026-126225

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-11T22:17:20.660 |

A missing authorization vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.7, FortiAnalyzer Cloud 8.0.0 through 8.0.1, FortiAnalyzer Cloud 7.6.7, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.7, FortiManager Cloud 8.0.0 through 8.0.1, FortiManager Cloud 7.6.7 may allow an authenticated attacker to elevate their privileges via crafted JSON-RPC request.

### CVE-2026-126213

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-11T22:17:18.457 |

A improper neutralization of special elements used in an sql command ('sql injection') vulnerability in Fortinet FortiAnalyzer 8.0.0 through 8.0.1, FortiAnalyzer 7.6.0 through 7.6.7, FortiAnalyzer 7.4 all versions, FortiAnalyzer 7.2 all versions, FortiAnalyzer Cloud 8.0.0 through 8.0.1, FortiAnalyzer Cloud 7.6.0 through 7.6.7, FortiAnalyzer Cloud 7.4.1 through 7.4.11, FortiAnalyzer Cloud 7.2.1 through 7.2.12, FortiManager 8.0.0 through 8.0.1, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.11, FortiManager 7.2.0 through 7.2.12, FortiManager Cloud 8.0.0 through 8.0.1, FortiManager Cloud 7.6.0 through 7.6.7, FortiManager Cloud 7.4.1 through 7.4.11, FortiManager Cloud 7.2.1 through 7.2.12 may allow an authenticated attacker to execute unauthorized SQL commands via specially crafted requests.

### CVE-2026-103980

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-11T21:16:42.083 |

ideon is a self-hosted visual workspace. Prior to version 0.9.6, the SSRF protection in safeFetch is bypassed by IPv6 transition addresses that embed private IPv4 addresses. The isPrivateIP function in src/app/lib/ssrf.ts checks only a narrow set of IPv6 ranges (loopback ::1, ULA fc/fd, link-local fe80) but does not recognize IPv4-mapped (::ffff:), NAT64 well-known (64:ff9b::/96, RFC 6052), NAT64 local-use (64:ff9b:1::/48, RFC 8215), 6to4 (2002::/16, RFC 3056), or Teredo (2001::/32, RFC 4380) encodings. An authenticated user can supply these addresses in link URLs to reach cloud metadata endpoints (169.254.169.254), localhost services, and RFC 1918 internal networks through the link preview metadata fetcher. This issue has been patched in version 0.9.6.

### CVE-2026-65967

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-11T19:17:44.287 |

Fider is a feedback portal for feature requests and suggestions. Prior to version 0.34.0, a Server-Side Request Forgery (SSRF) vulnerability exists in Fider due to insufficient validation of webhook URLs. The application allows user-controlled URLs to be fetched by the server without restricting access to internal or external network resources. This enables attackers with administrative privileges to make arbitrary HTTP requests from the server, potentially accessing internal services or cloud metadata endpoints. This issue has been patched in version 0.34.0.

### CVE-2026-124694

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T17:17:18.517 |

In Progress Kendo UI for jQuery versions 2026.3.1015 up to, but not including, 2026.4.1110, PropertyGrid does not encode bound property values and items[].description in its default configuration. An attacker who can influence either value can cause JavaScript to execute when a user views the grid. Successful exploitation may compromise the confidentiality and integrity of data available in the user's browser context. The first affected release has not been established.

### CVE-2026-124693

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T17:17:18.370 |

In Progress Kendo UI for jQuery versions 2026.3.1015 up to, but not including, 2026.4.1110, PivotGrid and PivotConfigurator axis field names are passed to a chip template without appropriate encoding. An attacker who can influence an axis field name can cause JavaScript to execute when a user views the rendered chip. The field name can be interpreted as HTML in both attribute and element contexts. Successful exploitation may compromise the confidentiality and integrity of data available in the user's browser context. The first affected release has not been established.

### CVE-2026-124692

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T17:17:18.227 |

In Progress Kendo UI for jQuery versions 2026.3.1015 up to, but not including, 2026.4.1110, the Grid and TreeList column-reorder drag clue reparses header text as HTML. An attacker who can influence a column field or title used by an affected application can cause JavaScript to execute when a user drags a column header while column reordering is enabled. Successful exploitation may compromise the confidentiality and integrity of data available in the user's browser context. The first affected release has not been established.

### CVE-2026-124690

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T17:17:18.080 |

In Progress Kendo UI for jQuery, sanitizeSvgContent() parses custom icon markup into a live DOM before filtering it. An attacker who can influence custom icon content can cause JavaScript to execute during icon creation, before an unsafe element is removed. The issue was reported in version 2026.3.1015; the first affected release has not been established. The issue is fixed in version 2026.4.1110.

### CVE-2026-124689

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T17:17:17.933 |

In Progress Kendo UI for jQuery versions 2026.3.1014 up to, but not including, 2026.4.1110, ActionSheet does not encode title, subtitle, and header button label values before rendering them. An attacker who can influence these values can inject markup that executes as JavaScript when a user opens the ActionSheet. Successful exploitation may compromise the confidentiality and integrity of data available in the user's browser context. The report identifies version 2026.3.1014; the first affected release has not been established.

### CVE-2026-124688

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-80` |
| Published | 2026-11-11T17:17:17.783 |

In Progress® Kendo® UI for jQuery prior to 2026.4.1111 the TabStrip, PanelBar, and Menu widgets support mapping a dataSource field to `spriteCssClass`. If an attacker can control the mapped data, they can break out of the attribute and inject markup, including event-handler attributes. The resulting JavaScript executes in the application's origin when a victim loads a page that renders the affected widget, allowing access to data and actions available in the victim's authenticated session.

### CVE-2026-124687

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-80` |
| Published | 2026-11-11T17:17:17.630 |

In Progress® Kendo® UI for jQuery versions from 2022.2.621 prior to 2026.4.1111 the DropDownButton and SplitButton allow markup injection through the `id` and `target` attributes. An attacker who can influence these item values can break out of the attributes and inject markup, including event handlers. The issue is fixed in 2026.4.1111.

### CVE-2026-111024

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-200;CWE-636;CWE-863` |
| Published | 2026-11-11T15:17:14.630 |

A user with the Viewer or Editor role could bypass folder permissions on Git Sync managed resources through the repository files API: a Viewer could read files in folders they could not access, and an Editor could create, modify, move or delete provisioned dashboards and folders there (incorrect authorization).

### CVE-2026-111000

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-269;CWE-863` |
| Published | 2026-11-11T15:17:14.503 |

A user with the Editor role who can edit a folder can move it, through the folders resource API, under a folder they administer, and so gain Admin on the moved folder and its contents, including the right to change their permissions. The legacy folder move API refuses the same move (improper privilege management).

### CVE-2026-102589

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-200;CWE-346;CWE-863` |
| Published | 2026-11-11T15:17:12.447 |

When independent Grafana instances share the same [rendering] renderer_token, an image renderer key issued by one instance is accepted by the others, so a user on one instance could act as the user with the same ID on another (origin validation error). This affects instances with the renderAuthJWT feature toggle enabled, the default from Grafana 13.0.0.

### CVE-2026-118855

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-12T08:16:39.930 |

Akaunting 3.3.0 contains a stored cross-site scripting vulnerability through invoice import. An authenticated user with invoice-creation permission can import HTML in an invoice status field. When another authenticated user opens that invoice's edit form, Akaunting renders the stored status in a hidden input with raw Blade output, allowing attacker-controlled markup to execute in the victim's Akaunting origin.

### CVE-2026-111521

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-11T22:17:10.820 |

Dell Display and Peripheral Manager (DDPM Windows), versions prior to 2.4.0.17, contain a Time-of-check Time-of-use (TOCTOU) Condition vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Code execution.

### CVE-2026-77873

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-11-11T17:17:19.940 |

An improper permissions vulnerability was reported in Lenovo System Update that could allow a local authenticated user to execute code with elevated privileges.
