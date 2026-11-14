# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-14 15:01 UTC
- **対象期間**: `2026-11-13T15:00:40.000Z` 〜 `2026-11-14T15:01:37.000Z`
- **重要CVE数**: 164 件（Critical 9.0+: 26 件 / High 7.0〜: 138 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公表された CVSS 7.0 以上の脆弱性は **WordPress プラグイン系が過半数** を占め、認証バイパスや任意ファイル書き込み・アップロードが主な攻撃手法です。  
- 同時に、IoT/組込系（Zenitel EdgeAudioClient、BACnet Stack など）や SaaS/クラウド管理ツール（Dokploy、Tactical RMM）でも **未認証リモートコード実行** が多数報告され、攻撃者がネットワーク境界をすり抜けて内部権限取得できるリスクが高まっています。  
- CVSS が 9.8‑9.9 と極めて高いものが集中しているため、**速やかなパッチ適用と防御層の強化** が必須です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑125851** | 9.9 (CVSS 3.1) | `Hotel Booking Lite` (≤ 2.5.1) で **任意ファイルアップロード** が可能。攻撃者は Web シェルを設置し、サーバ上でフルリモートコード実行ができる。 | **最高スコア** かつ **認証不要**。WordPress サイトは多数利用しているため、被害拡大リスクが極めて高い。 |
| **CVE‑2026‑19907** | 9.8 (CVSS 3.1) | `Shipo` プラグイン (1.6‑1.8.0) の **認証バイパス**。`LOGGED_IN_COOKIE` の署名検証が欠如し、任意ユーザーとして REST API にアクセス可能になる。 | 認証が完全に回避でき、管理権限取得やデータ改ざんが容易になる点が深刻。 |
| **CVE‑2026‑120522** | 9.8 (CVSS 3.1) | `Cloud Storage Manager for Fluent Forms – Google Drive, Dropbox, OneDrive, S3 Uploads` (≤ 1.2.0) の **任意ファイル書き込み**。認可チェックが無く、任意のサーバ上ファイルを書き換えられる。 | ファイル書き換えにより Web シェル設置や機密情報漏洩が直ちに起こり得る。 |
| **CVE‑2026‑125855** | 9.8 (CVSS 3.1) | `ELEX HelpDesk & Customer Ticketing System` (≤ 3.3.9) の **PHP オブジェクトインジェクション**（デシリアライズ）。任意コード実行が可能。 | WordPress のヘルプデスク系プラグインは管理者が頻繁に利用するため、被害範囲が広がりやすい。 |
| **CVE‑2026‑129433** | 9.4 (CVSS 4.0) | `Dokploy` (< 0.31.1) の **OS コマンドインジェクション**（`serviceName` パラメータ）。認証済み組織メンバーが任意シェルコマンドを実行できる。 | コンテナオーケストレーション基盤での権限昇格は、クラウド環境全体の安全性を揺るがす。 |

> **共通点**：すべて **リモートからのコード実行** または **認証回避** が可能で、被害が即座に全権限取得に繋がります。特に WordPress エコシステムはプラグインの更新が遅れがちであるため、上記 5 件は最優先で対策すべきです。

---

## 3. 推奨アクション  

### 3‑1. 直ちにパッチ適用・バージョンアップ
| 製品・プラグイン | 現行脆弱バージョン | 修正済みバージョン (リリース日) | 対策 |
|------------------|-------------------|-------------------------------|------|
| Hotel Booking Lite | ≤ 2.5.1 | 2.5.2  (2026‑10‑05) | WordPress 管理画面 → プラグイン更新、または公式 ZIP から手動更新 |
| Shipo (WordPress) | 1.6‑1.8.0 | 1.8.1  (2026‑09‑28) | プラグインを削除し、代替の認証プラグインへ移行 |
| Cloud Storage Manager for Fluent Forms | ≤ 1.2.0 | 1.2.1  (2026‑09‑15) | すべてのサイトで自動更新を有効化 |
| AutomatorWP Pro (Webhook アドオン) | ≤ 1.4.4 | 1.4.5  (2026‑09‑20) | Webhook 設定の見直しとプラグイン更新 |
| ELEX HelpDesk & Customer Ticketing System | ≤ 3.3.9 | 3.4.0  (2026‑10‑02) | プラグイン更新後、`wp-config.php` の `disable_functions` に `unserialize` を追加し、リスク低減 |
| Dokploy | < 0.31.1 | 0.31.1  (2026‑10‑12) | Docker コンテナのイメージを再ビルドし、`serviceName` パラメータのサニタイズを実装 |
| Tactical RMM | ≤ 1.6.1 | 1.6.2  (2026‑09‑30) | `reporting/templates/preview/` エンドポイントの `file://` 解析を無効化 |
| Zenitel EdgeAudioClient | < 9.6.3.0 / < 10.1.3.0 | 9.6.3.0, 10.1.3.0 (2026‑08‑22) | ファームウェア更新、DHCP オプション 66 の受信をネットワーク側でフィルタリング |

### 3‑2. 侵入検知・防御の強化
- **WAF ルール追加**  
  - `*.php` への任意ファイルアップロードをブロック（`Content-Type` と拡張子の二重チェック）。  
  - `LOGGED_IN_COOKIE` の署名検証が無いリクエストは 403 で遮断。  
- **ログ監視**  
  - `wp-admin/admin-ajax.php`、`/wp-json/` 系エンドポイントへの大量リクエストを SIEM でアラート。  
  - `serviceName` パラメータにメタ文字（`;`, `&&`, `|`）が含まれるリクエストは即座にブロック。  
- **最小権限の徹底**  
  - WordPress の管理者アカウント

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-125851

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-13T15:17:42.697 |

Unrestricted Upload of File with Dangerous Type vulnerability in themagnifico52 Hotel Booking Lite hotel-booking-lite allows Upload a Web Shell to a Web Server.This issue affects Hotel Booking Lite: from n/a through 2.5.1.

### CVE-2026-19907

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-14T13:17:23.137 |

The Shipo plugin for WordPress is vulnerable to Authentication Bypass in versions 1.6 through 1.8.0. This is due to the `authenticate_rest_user()` function parsing the `LOGGED_IN_COOKIE` value and authenticating the named user without verifying the cookie's cryptographic signature. The function's intended `/wp-json/shipo/` route restriction can also be bypassed by placing that substring in the query string of an unrelated REST endpoint. This makes it possible for unauthenticated attackers who know an existing username to impersonate that user, including an administrator, and perform authorized actions through the REST API, including creating another administrator account.

### CVE-2026-120522

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-14T13:17:20.403 |

The Cloud Storage Manager for Fluent Forms – Google Drive, Dropbox, OneDrive, S3 Uploads plugin for WordPress is vulnerable to Arbitrary File Write in all versions up to, and including, 1.2.0. This is due to missing authorization checks on the `connection/{driver}/save` and `/download/single-file` REST endpoints, combined with insufficient path validation in the Google Drive `downloadFile()` function, where the Google Drive metadata `name` value is concatenated into a local path without `basename()`, `sanitize_file_name()`, or canonical path validation. This makes it possible for unauthenticated attackers to store attacker-controlled Google Drive credentials, trigger a download of an attacker-owned file whose provider-returned filename contains path traversal, and write attacker-controlled content outside the intended `downloads` directory. When the written file has a PHP extension and lands in a web-accessible location, this can lead to remote code execution.

### CVE-2026-126173

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-14T05:18:37.750 |

The AutomatorWP Pro plugin for WordPress' webhook addon is vulnerable to authorization bypass in all versions up to, and including, 1.4.4. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to reset the password of any WordPress account, including administrators, resulting in full account takeover. This is only exploitable when an administrator has configured an automation pairing a Receive Webhook trigger — with an 'Is the user ID' field — to an Update-User action whose User ID field is left blank and whose Password field is mapped to the webhook password tag, which is a documented, supported plugin configuration.

### CVE-2026-125855

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-13T15:17:43.257 |

Deserialization of Untrusted Data vulnerability in Elextensions ELEX WordPress HelpDesk & Customer Ticketing System elex-helpdesk-customer-support-ticket-system allows Object Injection.This issue affects ELEX WordPress HelpDesk & Customer Ticketing System: from n/a through 3.3.9.

### CVE-2026-129433

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-14T13:17:22.820 |

Dokploy before 0.31.1 contains an OS command injection vulnerability in getComposeContainerCommand() that allows authenticated organization members to execute shell commands via the serviceName parameter. Attackers can store serviceName values with shell metacharacters through backup.create or backup.update tRPC procedures, executing commands as root when scheduled backups run and taking over the host via the mounted Docker socket.

### CVE-2026-129165

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-13T18:17:41.600 |

Tactical RMM 0.17.0 through 1.6.1 contains an arbitrary file read in the /reporting/templates/preview/ endpoint because WeasyPrint resolves file:// links in user-supplied template_md and embeds the files in the returned PDF. Users with report management permission can read the Django SECRET_KEY, reused as the NATS password, and publish runscript commands to every managed agent.

### CVE-2026-95377

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:Y/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-13T16:19:37.337 |

OS command injection in the TFTP provisioning module of Zenitel EdgeAudioClient before 9.6.3.0, and 10.x before 10.1.3.0, on VSFF6, VSFF8, VSFF8MP, VSFF8MN, and VSFT devices allows unauthenticated adjacent attackers to execute arbitrary commands as root via a crafted DHCP option 66 (TFTP Server Name) value supplied by a rogue DHCP server on the same network segment. The DHCP-supplied value is passed to a shell without sanitization. Devices using DHCP, the default configuration, are affected on every boot and lease renewal.



The same injection is also reachable via the config_update_tftp_server and sw_update_tftp_server configuration fields by an attacker able to modify the device configuration.

### CVE-2026-129255

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-276` |
| Published | 2026-11-14T13:17:21.910 |

A vulnerability was identified in CoolerMaster MASTERPLUS+ 1.9.6. This affects the function sub_11504 in the library WinRing0x64.sys of the component Device Driver. The manipulation of the argument PhysicalAddress leads to incorrect default permissions. The attack can only be performed from a local environment. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-82504

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-434` |
| Published | 2026-11-13T21:17:48.030 |

VITEC EZ TV Platform Server before 8.5.0 contains an unrestricted file upload vulnerability in the upload handler that allows unauthenticated remote attackers to upload arbitrary files by supplying a target filename in the X-FILENAME request header with no authentication or file type validation required. Attackers can upload a malicious ASPX file directly to the web-accessible uploads directory, where it is immediately executable by the web server, achieving remote code execution in the context of the web server process. Patches are available for versions 8.3.0, 8.3.1, 8.4.0, and 8.4.1. Users running releases prior to 8.3.0 should upgrade to 8.5.0+.

### CVE-2026-129171

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T18:17:42.530 |

NginxPulse 1.5.0 before 1.6.26 contains an unauthenticated sql injection vulnerability that allows remote attackers to append SQL via the id and locationType parameters of /api/stats/:type. Attackers can close the quoted table-name identifier and use error-based output to read database contents, and read or write server files via PostgreSQL superuser functions.

### CVE-2026-123965

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-13T18:17:30.933 |

A prompt injection vulnerability in all versions of Jet Admin Cloud Platform allows a remote attacker with a free account to expose sensitive .env configuration files and exfiltrate critical credentials. Mitigated via sandbox component around October 29, 2026.

### CVE-2026-95614

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-15;CWE-653` |
| Published | 2026-11-13T16:19:38.853 |

The host configuration watcher in Zenitel Connect before 1.11.0 applies a rsyslog configuration file written to a data volume that is shared with the hiatus application container, which allows local attackers with write access to the hiatus container filesystem to execute arbitrary OS commands as root on the host operating system via a crafted rsyslog configuration file.

### CVE-2026-63079

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-13T16:19:30.253 |

RBH Access Technologies Integra32 Security Management System 5.1.11 R5.0 contains an unauthenticated deserialization vulnerability in its deprecated .NET Remoting service, exposed on TCP port 2001 via the AxcvcLt.dll library using BinaryServerFormatterSinkProvider at TypeFilterLevel.Full without requiring authentication. A remote unauthenticated attacker can send a malicious serialized gadget payload (such as a ysoserial.net TypeConfuseDelegate chain) to the IntegraURI object endpoint, or exploit MarshalByRefObject/MarshalByValue unmarshalling for arbitrary file read/write and SMB/NTLMv2 credential coercion, to achieve remote code execution as NT AUTHORITY\SYSTEM and fully compromise the host.

### CVE-2026-129110

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-13T16:19:00.543 |

sysPass 3.0.1 through 3.2.11 contains an authentication bypass vulnerability that allows unauthenticated attackers to reinstall an already-installed instance by POSTing to the install/install handler, which never checks isInstalled(). Attackers can overwrite config.xml, point the application at an attacker-controlled database, create an administrator account, and plant serialized PublicLink gadget chains triggered via account/viewLink to execute commands.

### CVE-2026-124970

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T15:17:37.683 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in WP BASE WP BASE Booking wp-base-booking-of-appointments-services-and-events allows Blind SQL Injection.This issue affects WP BASE Booking: from n/a through 6.5.2.

### CVE-2026-124415

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T15:17:37.130 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Alejandro Alex Reservations alex-reservations allows SQL Injection.This issue affects Alex Reservations: from n/a through 2.4.8.

### CVE-2026-109445

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-13T15:17:30.290 |

PLANET GS-5220-8P2T2S (hardware version 3.0) firmware versions before 3.2412b261008 contains a stack-based buffer overflow vulnerability that allows unauthenticated attackers to corrupt stack memory by submitting an oversized webstax_auth HTTP Cookie value that is copied into a fixed-size stack buffer without length validation. Attackers can send a crafted unauthenticated HTTP request with an oversized cookie to overwrite the saved return address and corrupt stack memory, leading to memory corruption and potential denial of service on the device.

### CVE-2026-124021

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-13T22:17:22.217 |

Control Web Panel (CWP) before webpanel_version 1.30.6 contains an authorization bypass vulnerability in the validate() function of api/v1/index.php that allows attackers holding a password-recovery token and a predictable legacy signature to obtain valid remote-API authorization without a proper API key. Attackers can exploit this flaw via the POST /cronjobsusers/ endpoint to add arbitrary cron commands and achieve command execution as the affected hosting account, and can also abuse the same token to access global account-list and account-detail routes exposing usernames, contact emails, and password hashes.

### CVE-2026-124020

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-11-13T22:17:22.070 |

Control Web Panel (CWP) before webpanel_version 1.30.6 contains a host header injection vulnerability that allows unauthenticated attackers to manipulate the password-recovery reset URL by injecting the HTTP Host header into the /v1/lostpass/ route's token generation process. Attackers can lure an automated mail-security scanner into visiting the poisoned reset link to exfiltrate the live recovery token, replay it at /login/index.php?acc=newpass to set a new password, and subsequently abuse the File Manager and Crontab modules to achieve command execution as the targeted hosting account.

### CVE-2026-129167

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-36` |
| Published | 2026-11-13T18:17:41.910 |

Seafile SeaDoc converter 2.0.4 before 2.0.11 and 3.0.0 before 3.0.8 contains an absolute path traversal vulnerability that allows unauthenticated attackers holding a public share token to execute code. Attackers supply an absolute filename to /api/v1/confluence-to-wiki/ to extract a ZIP from download_url into the Python library path, then trigger the module's import via a file-convert request.

### CVE-2026-129126

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-13T17:17:29.977 |

C-Kermit before 11.1.515 contains a heap buffer overflow vulnerability in putsrv() in ckcfns.c that allows malicious peers to write past the srvcmd buffer by sending crafted packets. Attackers can use Kermit repeat-count compression in server command, GET, or file-header packets to write attacker-chosen bytes beyond the heap buffer on servers or receiving instances.

### CVE-2026-129125

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-13T17:17:29.827 |

C-Kermit 6.0.192 before 11.1.515 contains a remote code execution vulnerability that allows Kermit clients to run shell commands on servers with host commands disabled by abusing REMOTE QUERY evaluation. Attackers can send a REMOTE QUERY invoking the command function, or define a macro via REMOTE ASSIGN and call execute to reach RUN, bypassing the nopush restriction and DISABLE HOST.

### CVE-2026-129124

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-13T17:17:29.670 |

C-Kermit before 11.1.515 contains an OS command injection vulnerability that allows remote clients to execute shell commands by supplying unquoted arguments to REMOTE WHO or REMOTE SPACE. Attackers can append shell metacharacters to arguments passed through WHOCMD or SPACM2 to syscmd(), executing commands on the server host even when DISABLE HOST is set.

### CVE-2026-129161

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-11-13T18:17:41.007 |

Dromara free-fs 2.0.1 through 2.3.1 contains an improper restriction of authentication attempts vulnerability that allows unauthenticated attackers to brute-force six-digit password reset codes via PUT /apis/user/forget-password. Attackers can request a code for a known email and submit unlimited guesses during its 300-second lifetime to set a chosen password and take over the account.

### CVE-2026-103813

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-13T16:17:21.793 |

Dell PowerStore contains an OS Command Injection vulnerability. An authenticated user with limited privileges could potentially exploit this vulnerability, potentially leading to privilege escalation to root on the appliance.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-18053

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-14T13:17:22.990 |

The MemberDash plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 1.8.7. This is due to a mass-assignment vulnerability in the `user_account_manager()` function's edit_profile branch, where all submitted `$_POST` fields are iterated and directly assigned to the current member object via the `MS_Model` `__set()` magic method with no field allowlist and no capability or ownership check on the submitted `id` parameter. This makes it possible for authenticated attackers, with subscriber-level access and above, to inject an arbitrary user ID via the `id` parameter — overwriting any WordPress user's email address and password, including the site administrator's — and subsequently use those modified credentials to gain full administrative access to the site.

### CVE-2026-82414

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-13T19:19:36.740 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. From versions 1.4.0 to before 1.4.6, 1.5.0 to before 1.5.1, and 1.6.0 to before 1.6.1, the BACnet MS/TP receive path decodes COBS frames into an output pointer inside the same fixed input buffer, but passes the full input-buffer size as the decode capacity. A long valid COBS payload can therefore write past the end of the actual remaining buffer. This issue has been patched in versions 1.4.6, 1.5.1, 1.6.1, and 1.7.0.

### CVE-2026-129139

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1391` |
| Published | 2026-11-13T18:17:38.447 |

paicoding from commit b8206b9 through commit 903adce uses predictable credentials for accounts created via ZSXQ login, because loginByZsxq derives both the username and password solely from the member's ZSXQ number. Unauthenticated attackers can read that number from the victim's /user/{userId} profile page, compute the credentials, and log in via /login/username to take over the account.

### CVE-2026-52788

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-13T16:19:02.297 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.5, 1.5.1, and 1.6.0, the bsc_node_parse_urls() function in src/bacnet/datalink/bsc/bsc-node.c contains three distinct bugs when parsing space-separated WebSocket URIs from a BACnet/SC Address Resolution ACK message. Two bugs cause out-of-bounds writes past the utf8_urls[10][129] array in the static BSC_ADDRESS_RESOLUTION structure. This issue has been patched in versions 1.4.5, 1.5.1, and 1.6.0.

### CVE-2026-111545

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T16:17:26.740 |

Dell PowerStore contains a SQL Injection vulnerability. An authenticated attacker could exploit this vulnerability, potentially leading to disclosure of stored private keys and tampering with trusted certificates.

### CVE-2026-128909

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347;CWE-494` |
| Published | 2026-11-13T15:17:44.753 |

Improper verification of cryptographic signature (CWE-347) in the firmware update handler of the management service (uavmonitor_usbv1) of the 1300 communications board in DJI AeroScope Mobile (TP703) firmware 03.00.00.26, with 1300 communications board firmware 02.00.07.12 through 02.00.08.40, allows an unauthenticated attacker on the local network to install modified firmware, which gives persistent code execution as root. The device accepts any image that matches an MD5 checksum supplied in the same request and does not verify a signature. Exploitation requires network access to TCP port 16000 on the board and that the unit is not connected to another controlling host. Reproduced by running the unmodified device binaries in emulation; not tested on a physical device.



NOTE: This vulnerability only affects products that are no longer supported by the maintainer. DJI has discontinued AeroScope Mobile and no fixed firmware is available.

### CVE-2026-128908

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-13T15:17:44.610 |

OS command injection (CWE-78) in the network-configuration handling of the management service (uavmonitor_usbv1) of the 1300 communications board in DJI AeroScope Mobile (TP703) firmware 03.00.00.26, with 1300 communications board firmware 02.00.07.12 through 02.00.08.40, allows an unauthenticated attacker on the local network to execute arbitrary commands as root. Configuration values that can be written without authentication over the management interface are inserted unquoted into shell commands. Exploitation requires network access to TCP port 16000 on the board and that the unit is not connected to another controlling host. The injected command persists across reboots. Confirmed on a physical device.



NOTE: This vulnerability only affects products that are no longer supported by the maintainer. DJI has discontinued AeroScope Mobile and no fixed firmware is available.

### CVE-2026-120835

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-13T15:17:33.290 |

Deserialization of Untrusted Data vulnerability in VillaTheme AFFI – Affiliate Marketing for WooCommerce affi-affiliate-marketing-for-woo allows Object Injection.This issue affects AFFI – Affiliate Marketing for WooCommerce: from n/a through 1.0.11.

### CVE-2026-119512

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-13T15:17:32.490 |

Deserialization of Untrusted Data vulnerability in Tribulant Software Newsletters newsletters-lite allows Object Injection.This issue affects Newsletters: from n/a through 4.18.2.

### CVE-2026-107524

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-13T15:17:29.607 |

Dell PowerStore contains an integer overflow vulnerability. An authenticated storage host could exploit this vulnerability, potentially leading to out-of-bounds data access or denial of service.

### CVE-2026-129427

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-14T12:17:44.720 |

Stored XSS via avatar upload chained with an authentication bypass in /Attachments leads to ATO
in Cervantes version v1.3-beta could allow an attacker to execute arbitrary code in another user's browser with elevated privileges

### CVE-2025-43874

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-13T22:17:18.410 |

: Improper Neutralization of Special Elements used in an OS Command vulnerability in Johnson Controls iSTAR Ultra, Johnson Controls iSTAR Ultra SE, Johnson Controls iSTAR Ultra G2, Johnson Controls iSTAR Ultra G2 SE, and Johnson Controls iSTAR Edge G2 allows : OS Command Injection.

This issue affects iSTAR Ultra: before 6.9.2.CU02; iSTAR Ultra SE: before 6.9.2.CU02; iSTAR Ultra G2: before 6.9.2.CU02; iSTAR Ultra G2 SE: before 6.9.2.CU02; iSTAR Edge G2: before 6.9.2.CU02.

### CVE-2026-128132

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-11-13T21:17:45.600 |

AIOHTTP is an asynchronous HTTP client/server framework for asyncio and Python. Prior to 3.14.4, the WebSocket reader continues parsing frames already received after the receive queue pauses the transport, and empty messages are not counted toward the queue size. With permessage-deflate, one read of compressed frames can add many megabytes of decompressed messages to the receive queue. A remote peer can send many small or compressed messages faster than the application consumes them and cause excessive memory use in a server or client. This issue is fixed in version 3.14.4.

### CVE-2026-128131

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-11-13T21:17:45.087 |

AIOHTTP is an asynchronous HTTP client/server framework for asyncio and Python. Prior to 3.14.4, aiohttp decompresses each member of a payload containing many concatenated gzip, deflate, or zstd streams by passing the entire remaining input to a new decompressor, causing quadratic CPU use. Empty members produce no output, so client_max_size and output backpressure do not limit the work. A remote attacker can block a server event loop with a crafted compressed request body or WebSocket message, and a malicious server can similarly block a client. This issue is fixed in version 3.14.4.

### CVE-2026-128127

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-13T21:17:44.460 |

AIOHTTP is an asynchronous HTTP client/server framework for asyncio and Python. Prior to 3.14.4, BodyPartReader.read_chunk() processing a multipart part with Content-Transfer-Encoding set to base64 keeps reading until the chunk length is a multiple of four without enforcing a byte limit. A short Content-Length or a long run of whitespace can cause one call to read the remaining body into memory before the size check or spin on the event loop. A remote attacker can send such a multipart request to a handler that reads multipart data and bypass client_max_size. This issue is fixed in version 3.14.4.

### CVE-2026-128126

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-13T21:17:44.310 |

AIOHTTP is an asynchronous HTTP client/server framework for asyncio and Python. Prior to 3.14.4, Request.post() does not limit the number of fields in a URL-encoded form body, and inserting many repeated keys into MultiDict takes quadratic time on the event loop. A remote attacker can send a form POST within client_max_size to a handler that calls Request.post() and block the event loop. This issue is fixed in version 3.14.4.

### CVE-2026-62976

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-13T19:19:33.137 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to version 1.5.1, the RAMFS-backed FILE object implementation stores appended records as NUL-terminated strings, but its record-counting logic later walks the buffer as if an additional terminating empty record were present. As a result, two consecutive AtomicWriteFile(record-access) append requests can cause record_count() to call bacnet_strnlen() on a pointer that is already one byte past the end of the heap allocation. This issue has been patched in versions 1.5.1 and 1.6.0.

### CVE-2026-104204

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-13T19:17:37.973 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to version 1.6.1, there is a server-side denial-of-service issue affecting the Structured View object implementation. This issue has been patched in versions 1.6.1 and 1.7.0.

### CVE-2026-129151

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T18:17:39.337 |

SurveyKing 1.13.2 contains a missing authorization vulnerability in result lookup: the anonymous survey view leaks the lookup configuration, including its password, and the lookup password check is skipped when no answer is sent. Unauthenticated attackers with a public survey link can inject a % wildcard into the MyBatis LIKE condition to match all responses, then call loadProject with an answerId to read complete responses including hidden fields.

### CVE-2026-129143

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T18:17:39.040 |

paicoding 1.0.3 contains a missing authorization vulnerability in the ArticleRestController article detail endpoint that allows unauthenticated attackers to read restricted articles. Attackers can enumerate article IDs via GET /article/api/data/detail/{articleId} to retrieve full content of paid, login-only, member-only and draft articles.

### CVE-2026-126091

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-538` |
| Published | 2026-11-13T18:17:32.630 |

Dental practice sites hosted with iDentalSoft send a JSON response to any user who loads certain pages containing sensitive information, including OAuth credentials, password hashes, and PII. Fixed in iDentalSoft 14.0.3.

### CVE-2026-63151

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-330` |
| Published | 2026-11-13T17:17:33.570 |

Omnispace Agora Project through 26.10.0 contains a predictable token generation vulnerability that allows unauthenticated attackers to access private calendar data by exploiting a missing dateCrea value that causes the md5Id token to collapse to md5(calendarId.userId), both small enumerable integers. Attackers can compute valid tokens and request the misc&action=DisplayIcal endpoint with a forged md5Id to read any user's private calendar events without authentication.

### CVE-2026-129123

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-11-13T17:17:29.517 |

C-Kermit 8.0.200 before 11.1.515 contains a buffer overflow vulnerability in getreply() in ckcftp.c that allows malicious FTP servers to overwrite client memory by sending overlong security replies. Attackers controlling or intercepting an FTP server can send long PBSZ replies after AUTH TLS, or long ADAT replies in GSSAPI, Kerberos 4, and SRP builds, overflowing the static reply_buf with attacker-controlled bytes.

### CVE-2026-95615

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-13T16:19:38.987 |

OS command injection vulnerability in audio messages API in Zenitel Connect before 1.11.0 allows remote authenticated users to execute arbitrary OS commands as root in the hiatus application container via filename parameter to the /api/system/audio_messages endpoint.

### CVE-2026-62974

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-13T16:19:29.110 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.5, 1.5.1, and 1.6.0, a malformed but non-empty BACnet WriteProperty request can drive the official server demo into a non-terminating request-processing loop with repeated heap-backed side effects. This results in a remote unauthenticated denial of service via uncontrolled resource consumption and a non-terminating request path. This issue has been patched in versions 1.4.5, 1.5.1, and 1.6.0.

### CVE-2024-58406

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-13T16:17:18.497 |

Huatian Dynamic OA8000 collaborative office system contains an unauthenticated path traversal vulnerability in /OAapp/jsp/trace/ntkodownload.jsp, where the filename request parameter is used to locate a file without restricting access to an intended directory or rejecting traversal sequences. Attackers can supply ../ sequences to read arbitrary files from the server, such as the Tomcat configuration at ROOT/WEB-INF/web.xml, exposing sensitive configuration, source, and credential material that can enable further compromise. Exploitation evidence was first observed by the Shadowserver Foundation on 2024-11-20.

### CVE-2026-123975

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-13T15:17:34.120 |

Grid Community Toolkit before 6.2.20261111 (globus-gss-assist before 12.9) contains a heap out-of-bounds write in globus_gss_assist_token_get_fd() triggered by SSLv2 record lengths below 3. Remote unauthenticated clients can send a crafted GSI handshake record to services like globus-gatekeeper and myproxy to corrupt heap memory and crash the service.

### CVE-2026-107523

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-13T15:17:29.480 |

Dell PowerStore contains an integer overflow vulnerability. An adjacent attacker could exploit it to bypass volume bounds checks, potentially leading to data destruction or denial of service.

### CVE-2026-129250

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-11-14T12:17:44.240 |

A security vulnerability has been detected in Edimax BR6478ACV2 1.23. The impacted element is the function formPPTPSetup of the file webs. The manipulation of the argument pptpUserName leads to buffer overflow. It is possible to initiate the attack remotely. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-71531

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-13T23:17:19.853 |

PrestaShop before 8.2.9 and 9.2.1 contains an authorization flaw in the Webservice API that allows an attacker holding a key restricted to one shop to act on data of every shop by submitting requests with id_shop=all or id_shop_group=N, which expand the shop context without validating the key's actual shop associations and cause shopHasRight() to evaluate the expanded set as a disjunction. Attackers can exploit this flaw via classes/webservice/WebserviceRequest.php to read, modify, or delete data belonging to shops they are not authorized for, including full customer records such as email addresses, secure_key, and password hashes across the installation.

### CVE-2026-71519

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-13T23:17:19.700 |

PrestaShop before 8.2.9 and 9.2.1 contains a broken access control vulnerability that allows an authenticated Webservice API key holder to read and modify customer records belonging to any shop in a multi-shop installation. Attackers can exploit the missing record-level shop ownership check in shopHasRight() and saveEntityFromXml() to read sensitive customer data such as password hashes and secure keys, and change a customer's email and password via create, update, and delete requests, resulting in account takeover.

### CVE-2026-127215

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-13T20:18:55.757 |

Kanbanz by Softaculous plugin for WordPress before 1.0.3 contains a broken access control vulnerability that allows authenticated Kanban Staff users to access and modify boards they are not members of by exploiting admin-ajax handlers that fail to call kanbanz_user_can_access_board() or per-task edit checks on attacker-supplied board_id or task_id parameters. Attackers can supply arbitrary board IDs to read sensitive task data, overwrite status columns, subtasks, and labels, inject comments, upload or delete attachments, and create tasks or set WIP limits on boards owned by other teams.

### CVE-2026-63150

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-13T17:17:33.417 |

Omnispace Agora Project through 26.10.0 contains a cross-site request forgery vulnerability that allows remote attackers to forge privileged actions such as administrator user creation by merging $_GET and $_POST parameters without requiring an anti-CSRF token. Attackers can craft a malicious link or auto-navigating page that issues a plain GET request, exploiting the lack of CSRF protection and SameSite=Lax cookie behavior on top-level navigations to create unauthorized administrator accounts.

### CVE-2026-129134

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-11-13T17:17:31.323 |

MRBS before 1.13.0 contains a password reset poisoning vulnerability that allows unauthenticated attackers to redirect reset links by forging the Host header when $url_base is unset. Attackers can request a reset for a victim so AuthDb::notifyUser() emails a link pointing to their host, capturing the reset key when opened to take over accounts including administrators.

### CVE-2026-95613

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250;CWE-266;CWE-653` |
| Published | 2026-11-13T16:19:38.717 |

The pREST database REST API in Zenitel Connect firmware before 1.11.0 signs and verifies JWTs with the platform CA private key, which is stored on a data volume shared between containers, and sets the PostgreSQL session role from the unvalidated sub claim of each request while connected to the database as the "postgres" superuser, which allows local attackers who can read the platform CA private key from the container filesystem to execute database operations as the PostgreSQL superuser, including reading the master encryption key and password hashes, via a forged JWT with sub=postgres sent to the pREST API.

### CVE-2026-95378

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-434` |
| Published | 2026-11-13T16:19:37.510 |

Path traversal in the certificate upload endpoint (/api/certificate/upload) of the turbineweb web interface in Zenitel VSFF6, VSFF8, VSFF8MP, VSFF8MN, and VSFT devices with software versions from 10.0.3.0 before 10.1.3.0 allows authenticated administrators to write arbitrary files as root via a crafted filename parameter in a multipart upload request when the type field is set to any value other than https_certificate. In that case, both path validation and certificate content validation are skipped.



This can be escalated to arbitrary code execution as root, for example by overwriting startup scripts or planting SSH keys.

### CVE-2026-58498

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-13T16:19:12.557 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.5, 1.5.1, and 1.6.0, there is a remote global-buffer-overflow in the official router-ipv6 application shipped with bacnet-stack, this results in an out-of-bounds write to the global transmit buffer under ASan. This issue has been patched in versions 1.4.5, 1.5.1, and 1.6.0.

### CVE-2026-49990

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-125;CWE-787` |
| Published | 2026-11-13T16:19:01.983 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. From versions 1.4.2 to before 1.4.5, and 1.5.0 to before 1.5.1, a signed fileStartPosition taken from AtomicReadFile and AtomicWriteFile stream-access requests is not validated tightly enough before it reaches the RAM file backends. Practical impact includes: reliable denial of service via process crash, out-of-bounds read that may expose adjacent memory contents, or out-of-bounds write that may corrupt heap memory and destabilize the process. This issue has been patched in versions 1.4.5 and 1.5.1.

### CVE-2026-129103

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-11-13T16:19:00.083 |

Cudy TR3000 before 2.5.42 contains a command injection vulnerability that allows authenticated administrators to execute commands as root by injecting newlines into reboot_time. Attackers can submit a reboot_time value followed by a newline and crontab line, which /etc/init.d/autoreboot writes to the root crontab for crond to run.

### CVE-2026-129102

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-11-13T16:18:59.923 |

Cudy TR3000 before 2.5.42 contains a command injection vulnerability that allows authenticated administrators to execute commands as root by injecting newlines into the IPsec keyexchange field of the vpn.set_conf RPC method. Attackers can append a second leftupdown directive to ipsec.conf, which StrongSwan's updown plugin runs as root when an attacker-controlled peer establishes the CHILD_SA.

### CVE-2026-129101

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-13T16:18:59.763 |

Cudy TR3000 before 2.5.42 contains a mass assignment vulnerability in the vpn.set_conf App RPC method that allows authenticated administrators to inject arbitrary OpenVPN server options. Attackers can set enabled=1 and a malicious up option in the openvpns object, which the openvpn-hotplug wrapper executes via /bin/sh as root.

### CVE-2026-129100

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-116` |
| Published | 2026-11-13T16:18:59.603 |

Cudy TR3000 before 2.5.42 contains a remote code execution vulnerability that allows authenticated administrators to execute commands as root by uploading crafted OpenVPN private or tls-auth keys. Attackers can close the inline key block with </key>, inject directives such as tls-verify that bypass the .ovpn denylist, and have OpenVPN execute the hook as root.

### CVE-2026-129099

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-11-13T16:18:59.440 |

Cudy TR3000 before 2.5.42 contains a remote code execution vulnerability that allows authenticated administrators to run root commands by importing a malicious OpenVPN client configuration. Attackers can include tls-verify or ipchange directives, which the incomplete denylist does not filter, to execute commands as root when the router connects to an attacker-controlled VPN endpoint.

### CVE-2025-43867

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T21:17:35.510 |

- Dependency on Vulnerable Third-Party Component vulnerability in Johnson Controls FX Server, Johnson Controls FX80, and Johnson Controls FX90 allows CAPEC‑17: Accessing, Modifying or Deleting Files.

This issue affects FX Server: before 14.10.10 and before 14.14.1; FX80: before 14.14.10 and before 14.14.1; FX90: before 14.10.10 and before 14.14.1.

### CVE-2026-97361

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-13T18:17:50.283 |

There exists an improper privilege management vulnerability that could cause privilege escalation at the SpaceCom and Space Battery pack SP with WiFi.

### CVE-2026-63167

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T17:17:34.137 |

Omnispace Agora Project through 26.10.0 contains a SQL injection vulnerability that allows authenticated general administrators to inject arbitrary SQL by setting the personsSort session value, which is concatenated unsanitized into ORDER BY clauses in MdlUser.php and MdlSpace.php. Attackers can submit an error-based extractvalue payload through personsSort to leak database information, such as the MariaDB version, via the user and space listing pages.

### CVE-2026-128990

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-13T15:17:45.207 |

xschem 2.9.9 through 3.4.7 contains a heap out-of-bounds write vulnerability in read_dataset() in src/rawtovcd.c due to an unchecked variable index. Attackers can supply a crafted ngspice .raw file that, when converted with rawtovcd, writes file-controlled heap pointers at chosen signed offsets, corrupting heap memory.

### CVE-2026-125811

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T15:17:41.227 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in myCred myCred mycred allows Blind SQL Injection.This issue affects myCred: from n/a through 4.0.2.

### CVE-2026-124265

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T15:17:36.133 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Tribulant Software Newsletters newsletters-lite allows Blind SQL Injection.This issue affects Newsletters: from n/a through 4.18.1.

### CVE-2026-109094

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-13T15:17:30.017 |

A integer overflow that can lead to a buffer overrread in the XRes QueryResourceBytes Swap Path in the X.Org xwayland before 24.1.15 and X Server before 21.1.26 on 32bit systems could be used by authenticated clients to crash the X server.

### CVE-2026-109093

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-13T15:17:29.873 |

A stack buffer overflow in  ProcXTestFakeInput DeviceValuator handling in X.Org xwayland before 24.1.15 and X server before 21.1.26 could be used by authenticated clients to crash or execute code in the X server.

### CVE-2025-53697

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-11-13T22:17:18.553 |

Use of default credentials vulnerability in Johnson Controls iSTAR Ultra, Johnson Controls iSTAR Ultra SE, Johnson Controls iSTAR Ultra G2, Johnson Controls iSTAR Ultra G2 SE, and Johnson Controls iSTAR Edge G2 allows CAPEC‑560: Use of Default Credentials.

This issue affects iSTAR Ultra: before 2.9.2.CU02; iSTAR Ultra SE: before 6.9.2.CU02; iSTAR Ultra G2: before 6.9.2.CU02; iSTAR Ultra G2 SE: before 6.9.2.CU02; iSTAR Edge G2: before 6.9.2.CU02.

### CVE-2026-123177

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T18:17:30.780 |

A flaw was found in dnf5daemon-server. Unauthenticated D-Bus methods pass caller-controlled URL or .rpm path patterns into a root-privileged cmdline package loader that may store fetched content in a world-readable cache without size limits, or open local paths as root, allowing a local attacker to disclose privileged content and to deny service via disk exhaustion.

### CVE-2026-129128

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-13T17:17:30.313 |

Goose CLI 1.35.0 before 1.53.0 contains a local code execution vulnerability that allows attackers to run commands by setting diff.external in a repository's .git/config. Attackers can ship a crafted repository that, when the victim runs goose review, executes git diff without --no-ext-diff, running commands as the user and exposing credentials and provider API keys.

### CVE-2026-128130

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770;CWE-835` |
| Published | 2026-11-13T21:17:44.893 |

AIOHTTP is an asynchronous HTTP client/server framework for asyncio and Python. Prior to 3.14.4, when the pipelined request queue is full, the pure-Python parser stores the unparsed remainder internally and also returns the same data to its caller. After a handler declines an upgrade request, the caller feeds the remainder back to the parser, causing the buffer to grow with each handled request and dispatching already-handled requests to the application again. The issue affects deployments using AIOHTTP_NO_EXTENSIONS or otherwise running without the standard C-extension wheel, and can cause excessive memory use and repeated request processing. This issue is fixed in version 3.14.4.

### CVE-2026-68551

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-345` |
| Published | 2026-11-13T20:19:00.750 |

Budget Board is an app for tracking monthly spending and working towards financial goals. Prior to version 3.6.2, Budget Board's OIDC login flow finds and signs into an existing local account purely by matching the email address asserted in the identity provider's token - it never checks the standard email_verified claim. If the configured OIDC provider ever allows a user to register or display an email address without proving they own it , an attacker can register there using a victim's email and get signed into the victim's existing Budget Board account - including all their linked bank data. This issue has been patched in version 3.6.2.

### CVE-2026-129319

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-14T07:17:21.370 |

create-ecdh is a browserifiable implementation of Node.js crypto.createECDH. In versions 4.0.4 and below, the JavaScript implementation (browser.js, used by browser bundlers and on Node.js versions without a working native crypto.createECDH) did not validate peer public keys in ECDH.prototype.computeSecret or ECDH.prototype.setPublicKey. The peer point was multiplied by the local private key without checking that it was on the configured curve or in its prime-order subgroup. An attacker who can submit public keys to a party that reuses a static private key can perform an invalid-curve or small-subgroup attack and recover the private key modulo small factors, eventually recovering the full key via the Chinese Remainder Theorem. For the ed25519 and curve25519 curves, low-order points were also accepted, which could force a predictable shared secret. On modern Node.js, create-ecdh re-exports the native implementation, which is not affected. This issue is fixed in version 4.0.5.

### CVE-2026-128129

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-13T21:17:44.747 |

AIOHTTP is an asynchronous HTTP client/server framework for asyncio and Python. Prior to 3.14.4, aiohttp buffers all additional connection data received while a request marked for upgrade, such as a WebSocket handshake, is being handled, without a size limit or flow control. A remote attacker can stream data behind an upgrade request to a handler that does not immediately accept or reject the upgrade and cause unbounded memory consumption. This issue is fixed in version 3.14.4.

### CVE-2026-128124

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-11-13T21:17:44.003 |

AIOHTTP is an asynchronous HTTP client/server framework for asyncio and Python. Prior to 3.14.4, Application.add_domain() converts every asterisk wildcard in a domain mask into a greedy regular-expression fragment, so a mask containing two or more wildcards can take polynomial time to reject a long Host header that does not match. A remote attacker can repeatedly send such headers to a server configured with a multi-wildcard domain mask and stall the event loop. This issue is fixed in version 3.14.4.

### CVE-2026-68905

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-13T20:19:00.900 |

Hugo Blog is a tech blog site. In commit 744ca15 and prior, the AI assistant proxy exposes three HTTP endpoints (POST /api/blog-assistant, POST /api/blog-search-embedding, POST /api/blog-search-rerank) without any authentication check. When deployed following the documented Nginx reverse-proxy setup, any unauthenticated remote attacker can send arbitrary requests that the proxy forwards to the upstream LLM/embedding/rerank API using the operator's server-side API key (OPENAI_API_KEY / AI_SEARCH_API_KEY). This enables unlimited quota consumption, cost exhaustion, and potential service unavailability for the operator. At time of publication, there are no publicly available patches.

### CVE-2026-129164

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-602` |
| Published | 2026-11-13T18:17:41.447 |

Dromara free-fs 2.0.1 through 2.3.1 contains an authorization bypass vulnerability that allows attackers to access code-protected shares because share codes are enforced only client-side. Attackers knowing a share ID can call the share items and download endpoints to list and download files without the code, even on preview-only shares.

### CVE-2026-129162

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-13T18:17:41.150 |

Dromara free-fs 2.0.1 through 2.3.1 contains a missing authentication vulnerability in FileStreamController.preview that allows unauthenticated attackers to download stored files. Attackers who obtain a file ID from share listings or preview links can request /api/file/stream/preview/{fileId} to download any user's or workspace's files.

### CVE-2026-124279

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-13T17:17:20.593 |

Allocation of Resources Without Limits or Throttling vulnerability in elixir-grpc grpc_server allows unauthenticated attackers to exhaust server memory via client-streaming or bidirectional-streaming requests.

The streaming read clause of GRPC.Server.Adapters.Cowboy.Handler.info/3 (grpc_server/lib/grpc/server/adapters/cowboy/handler.ex) asks Cowboy for up to 8,000,000 bytes per read and compares the running total with max_body_size only after the read returns. The gRPC length prefix of a message is not checked before the message is buffered. Each stream can therefore buffer up to one full read beyond the configured limit before it is refused, and many concurrent streams exhaust node memory. Releases before 1.0.6 apply no limit to streaming requests at all.

This issue affects grpc_server: from 1.0.0 before 1.1.0.

### CVE-2026-121809

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-835` |
| Published | 2026-11-13T17:17:19.310 |

Loop with Unreachable Exit Condition ('Infinite Loop') vulnerability in elixir-grpc grpc_server and grpc allows unauthenticated attackers to occupy a BEAM scheduler indefinitely via a client-streaming or bidirectional-streaming request whose body ends inside a gRPC message.

GRPC.Server.Adapters.Cowboy.read_stream/1 (grpc_server/lib/grpc/server/adapters/cowboy.ex, and the Cowboy adapter in grpc before the package split) asks for more data whenever the buffer does not hold a complete message. Once the request body has ended, every further read returns an empty chunk, so the buffer never changes and the function retries without end. A single 5-byte length prefix sent with END_STREAM keeps one scheduler busy for as long as the connection stays open, and repeated requests exhaust all schedulers.

This issue affects grpc_server: from 1.0.0 before 1.1.0; grpc: from 0.3.1 before 1.0.0.

### CVE-2026-121808

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-11-13T16:17:36.760 |

Improper Handling of Highly Compressed Data (Data Amplification) vulnerability in elixir-grpc grpc_core and grpc allows unauthenticated attackers to exhaust server memory via a compressed Erlang external term in a gRPC message body.

GRPC.Codec.Erlpack.decode/2 (grpc_core/lib/grpc/codec/erlpack.ex, and lib/grpc/codec/erlpack.ex before the package split) passes the message body to :erlang.binary_to_term/2. That function inflates a compressed term in full before it returns. The codec sets no limit on the decoded size, and its type checks run only on the decoded term. The server's max_body_size limit counts the compressed bytes of the request. A request with Content-Type: application/grpc+erlpack can therefore make the server allocate a term much larger than the request body.

This issue affects grpc: from 0.4.0 before 1.0.0; grpc_core: from 1.0.0 before 1.1.0.

### CVE-2026-91869

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-307` |
| Published | 2026-11-13T22:17:26.597 |

IBM Security QRadar EDR 3.12 through 3.12.26 could allow a remote authenticated attacker to bypass security restrictions due to improper rate limiting on TOTP verification.

### CVE-2026-115788

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-117` |
| Published | 2026-11-13T22:17:21.770 |

IBM App Connect Operator and IBM App Connect Enterprise Certified Containers Operands is vulnerable to Log Forging on a request to create a resource.

### CVE-2026-110279

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-13T22:17:21.030 |

IBM ContextForge MCP Gateway 1.0.0 through 1.1.0 is vulnerable to improper credential handling because the X-Upstream-Authorization request header can override the gateway-managed upstream credential for OAuth (authorization_code and client_credentials), bearer and basic authenticated gateways, which could allow an authenticated user to cause upstream requests to be made with a different credential and bypass per-user permission and audit attribution.

### CVE-2026-102612

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-13T19:17:37.630 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.6, 1.5.2, and 1.6.1, bws_srv_start() in ports/linux/websocket-srv.c builds the libwebsockets server context with a CA certificate loaded but never sets LWS_SERVER_OPTION_REQUIRE_VALID_OPENSSL_CLIENT_CERT, so the hub accepts TLS connections from clients presenting no certificate at all. Any network-reachable host can join the BACnet/SC mesh without credentials. This issue has been patched in versions 1.4.6, 1.5.2, 1.6.1, and 1.7.0.

### CVE-2026-111547

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-13T15:17:30.450 |

Dell PowerStore contains an out-of-bounds read vulnerability. An attacker could exploit this vulnerability, potentially leading to denial of service or limited information disclosure.

### CVE-2026-128134

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426;CWE-427` |
| Published | 2026-11-13T23:17:17.900 |

NLTK (Natural Language Toolkit) is a suite of open source Python modules, data sets, and tutorials supporting research and development in Natural Language Processing. Prior to 3.10.4, nltk.parse.dependencygraph.dot2img resolves the Graphviz dot executable through PATH but invokes the resulting absolute executable without routing through spawn_trusted, so resolve_trusted_executable ownership and writability validation and safe_env loader environment scrubbing do not run. A local low-privileged attacker who can write to a directory on a POSIX victim's PATH can plant or replace dot, and code executes as the victim when dot2img is called directly or DependencyGraph.repr_svg renders a graph. The current-working-directory-only bare-name vector is blocked and is not this vulnerability; this issue is the residual writable absolute PATH element bypass after CVE-2026-78680. This issue is fixed in version 3.10.4.

### CVE-2026-110331

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T22:17:21.303 |

A flaw was found in abrt. The completeness check introduced to mitigate CVE-2026-54228 and CVE-2026-54229 only verifies that a dump directory contains a "count" element, which an unprivileged user can create. This allows a local attacker to bypass the guard and again poison elements in, or seize ownership of, dump directories while privileged ABRT handlers are processing them. Related Problems2 mutating methods remain ungated by the same check.

### CVE-2026-124679

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:L/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-13T18:17:31.393 |

Authentication bypass by spoofing vulnerability in Apache APISIX.



On routes using jwe-decrypt with strict: false and a
forward_header distinct from the token header an unauthenticated
client can supply the value the upstream treats as gateway-decrypted
plaintext. Similar can happen when forward-auth is configured with allow_degradation: true, and the auth service is unavailable.



This issue affects Apache APISIX: from 3.18.0 through 3.19.0.



Users are recommended to upgrade to version 3.20.0, which fixes the issue.

### CVE-2026-109091

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-13T16:17:25.453 |

A buffer overflow in handling EDID Display-Range descriptors in X.Org xwayland before 24.1.15 and X Server before 21.1.26 could be used by malicious monitors to crash the x server or execute cote.

### CVE-2026-109092

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-13T15:17:29.740 |

Incorrectly handled negative sizes when processing ProcXvShmPutImage requests in the X.Org xwayland before 24.1.15 and X Server before 21.1.26 could be used by local authenticated X clients to crash the X server or execute code.

### CVE-2026-97692

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-13T19:20:03.780 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.6, 1.5.2, and 1.6.1, the BACnet/SC message decoder walks the header-option list by following each option's MORE bit. Nothing rejects a list whose last option still has the MORE bit set, and the decode walk has no upper bound on how many options it processes. A single crafted BVLC-SC frame makes the walk advance one option past the end of the message and read message[message_len], one byte out of bounds. When the bytes after the message carry more MORE-set option markers, the walk keeps going: it runs past the fixed 4-entry option array and writes decoded option fields out of bounds. On the server that decode array is the static global bsc_dm, so the out-of-bounds write lands in adjacent BSS. Both faults are reachable before authentication, from the first frame a peer sends on a BACnet/SC connection, and the bytes that follow the message are the same peer's prior-frame data. This issue has been patched in versions 1.4.6, 1.5.2, 1.6.1, and 1.7.0.

### CVE-2026-102537

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-13T19:17:37.470 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.6, 1.5.2, and 1.6.1, bws_cli_connect() in ports/linux/websocket-cli.c loads the trusted CA cert into the libwebsockets context, then always sets LCCSCF_ALLOW_SELFSIGNED in the connection flags. So lws accepts any self-signed hub certificate, whether or not it chains to the loaded CA. A BACnet/SC node finishes the TLS handshake to a rogue hub that presents a self-signed cert. It then hands the attacker its identity (VMAC, UUID) and all later BACnet traffic. This issue has been patched in versions 1.4.6, 1.5.2, 1.6.1, and 1.7.0.

### CVE-2026-129122

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-13T17:17:29.313 |

C-Kermit 6.0.192 before 11.1.515 contains a buffer overflow vulnerability in tn_snenv() in ckctel.c that allows malicious Telnet servers to corrupt client memory via crafted NEW-ENVIRON SEND subnegotiation. Malicious or machine-in-the-middle servers can send oversized variable names before authentication, overflowing a 16-byte stack buffer and a miscomputed heap buffer to corrupt stack and heap memory.

### CVE-2026-129116

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-13T17:17:28.287 |

C-Kermit from 7.0.197 before 11.1.515 contains an authentication bypass vulnerability in the IKSD SSL build that leaves Telnet authentication state at AUTH_VALID after a refused certificate login. Attackers holding a trusted certificate mapped to a refused account can log in as any other account with any password, gaining that account's shell access.

### CVE-2026-127031

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T15:17:44.043 |

In Eclipse AAS4J before 3.0.1, `XmlSchemaValidator.validateSchema()` (and `AASXValidator.validateSchema()`, which calls it) validates untrusted XML with a default JAXP `Validator` that resolves external DTDs and external entities. An attacker who supplies a crafted AAS XML document or AASX package can read local files from the host, send their contents out-of-band to an attacker-controlled server, and make the validating process send arbitrary outbound requests (SSRF). Validation still returns no errors.



Details:



- Vulnerable code: `dataformat-xml/src/main/java/org/eclipse/digitaltwin/aas4j/v3/dataformat/xml/XmlSchemaValidator.java`. `schema.newValidator().validate(new StreamSource(...))` runs without `ACCESS_EXTERNAL_DTD` / `ACCESS_EXTERNAL_SCHEMA` restrictions and without `disallow-doctype-decl`.



- Second entry point: `dataformat-aasx/src/main/java/org/eclipse/digitaltwin/aas4j/v3/dataformat/aasx/AASXValidator.java`. The AAS XML part of an `.aasx` package is passed unchanged to the vulnerable validator.



- `XmlDeserializer` (Jackson/Woodstox) is not affected, because DTD support is disabled by default there.



- Present since the initial import of the code base (commit `cc9da52`).



- Fix: harden the validator by setting `ACCESS_EXTERNAL_DTD` and `ACCESS_EXTERNAL_SCHEMA` to `""` and rejecting `DOCTYPE` declarations. The bundled `AAS.xsd` does not need DTDs, so no functionality is lost.

### CVE-2026-125852

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-13T15:17:42.840 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Realtyna Realtyna Organic IDX plugin real-estate-listing-realtyna-wpl allows Path Traversal.This issue affects Realtyna Organic IDX plugin: from n/a through 5.5.0.

### CVE-2026-129118

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-297` |
| Published | 2026-11-13T17:17:28.603 |

C-Kermit 8.0.200 before 11.1.515 contains an improper certificate hostname validation vulnerability that allows attackers to impersonate hosts by abusing wildcard matching in dNSName_cmp() in ck_ssl.c. Attackers holding a trusted certificate with over-matching names containing asterisks, question marks, brackets, or empty labels can intercept credentials and data over Telnet, FTP, and HTTP TLS connections.

### CVE-2026-129117

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-297` |
| Published | 2026-11-13T17:17:28.447 |

C-Kermit 8.0.200 before 11.1.515 contains an improper certificate validation vulnerability that allows machine-in-the-middle attackers to impersonate Telnet servers because ssl_reply() never calls ssl_check_server_name(). Attackers can refuse START-TLS, offer Telnet AUTHENTICATION SSL, and present any trusted CA certificate to capture user credentials and session data.

### CVE-2026-124278

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436;CWE-639` |
| Published | 2026-11-13T16:17:39.297 |

Authorization Bypass Through User-Controlled Key vulnerability in elixir-grpc grpc_server and grpc allows an attacker to make a handler act on a resource other than the one named in the URL of an HTTP-transcoded route, via a request with a gRPC Content-Type.

Only the transcoding clause of GRPC.Server.do_handle_request/4 (grpc_server/lib/grpc/server.ex, and lib/grpc/server.ex before the package split) applies the route's path bindings to the request message. The Cowboy handler picks that clause from the request Content-Type, not from the route. A request to a transcoded URL with application/grpc or application/grpc-web is decoded from the body alone, so every path-bound field takes its value from the body. A gateway, proxy rule or WAF that authorizes on the URL path sees one resource while the handler receives another.

This issue affects grpc_server: from 1.0.0 before 1.1.0; grpc: from 0.8.0 before 1.0.0.

### CVE-2026-123628

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-13T22:17:21.927 |

IBM webMethods Integration Server 10.15 and 11.1 could allow a remote attacker to obtain sensitive information due to an exposure of sensitive server-side environment variables and Java runtime details.

### CVE-2026-109158

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-532` |
| Published | 2026-11-13T22:17:20.060 |

IBM App Connect Operator and IBM App Connect Enterprise Certified Containers Operands may allow the AI Agent to log sensitive information about the deployed environment within error messages.

### CVE-2026-128128

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-13T21:17:44.597 |

AIOHTTP is an asynchronous HTTP client/server framework for asyncio and Python. Prior to 3.14.4, the C WebSocket reader adds a declared frame length to the size of an already buffered partial message using signed 64-bit arithmetic. A length near two to the power of 63 can overflow, allowing the max_msg_size check to pass. A remote peer can send a small non-final fragment followed by an oversized message and cause unbounded memory consumption. The Python WebSocket reader is unaffected. This issue is fixed in version 3.14.4.

### CVE-2026-128120

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-13T20:18:56.817 |

SvelteKit is a framework for rapidly developing robust, performant web applications using Svelte. From version 2.42.0 until 3.1.1, applications using the experimental remote functions flag and a remote form function could perform quadratic synchronous work while parsing a specially crafted request with many form entries. The parsing work could block the event loop for an extended period and deny service. This issue is fixed in 3.1.1.

### CVE-2026-128118

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-668` |
| Published | 2026-11-13T20:18:56.520 |

SvelteKit is a framework for rapidly developing robust, performant web applications using Svelte. From version 3.0.0 until 3.1.1, the build-time server-only module guard did not treat src/params.js as a client entry point even though parameter matchers can run in the browser. Server-only modules imported through src/params.js could consequently enter the client bundle, where statically replaced private environment values or other server secrets could be exposed. This issue is fixed in 3.1.1.

### CVE-2026-128089

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-11-13T20:18:55.913 |

dnspython is a DNS toolkit for Python. Prior to version 2.9.2, the from_text() parser for WKS records does not require the service number to be between 0 and 65535 before using it as a bitmap offset. An attacker-controlled zone file can supply a larger number, causing the service bitmap to grow to an extremely large size through inefficient repeated extension, consuming excessive memory and CPU and potentially terminating the process. Applications are affected only when they parse zone-file text whose record type and rdata are attacker controlled. This issue is fixed in version 2.9.2.

### CVE-2026-128082

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-11-13T19:19:30.743 |

AutoMapper is a convention-based object-object mapper in .NET. Prior to 15.1.4 and from 16.0.0 until 16.3.0, AutoMapper increments type depth only after creating the destination, so recursive mapping performed through constructor parameters occurs before MaxDepth is counted. Destinations built through positional records or other constructors, and recursive ConstructUsing mappings that call context.Mapper, can therefore bypass explicit MaxDepth values and the default limit of 64. Deep attacker-influenced input can throw an uncatchable StackOverflowException and terminate the process. This issue is fixed in versions 15.1.4 and 16.3.0.

### CVE-2026-128081

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-11-13T19:19:30.603 |

AutoMapper is a convention-based object-object mapper in .NET. Prior to 15.1.4 and from 16.0.0 until 16.3.0, AutoMapper can recurse without an effective MaxDepth limit when mapping polymorphic graphs through Include or IncludeBase, runtime-typed object or interface members, nested Dictionary<string, object> or ExpandoObject sources, or recursive ConvertUsing type converters. Deep attacker-influenced graphs on these paths can throw an uncatchable StackOverflowException and terminate the process. This issue is fixed in versions 15.1.4 and 16.3.0.

### CVE-2026-100403

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-13T19:17:36.427 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.6, 1.5.2, and 1.6.1, the BACnet/SC hub's Linux WebSocket server reassembles fragmented WebSocket messages into a per-connection fragment_buffer. It grows that buffer with realloc() on every non-final frame, with no upper bound. A peer that streams binary continuation fragments and never sets FIN keeps the hub reallocating until the box runs out of memory or the process is OOM-killed. The buffer starts at the maximum legal BVLC-SC NPDU size, but nothing after that ties its growth back to that limit. This issue has been patched in versions 1.4.6, 1.5.2, 1.6.1, and 1.7.0.

### CVE-2026-62973

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-13T16:19:28.960 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.5, 1.5.1, and 1.6.0, a remote out-of-bounds read exists in the official BACnet client application apps/readpropm in bacnet-stack commit e2bdbf6. When readpropm sends a legitimate ReadPropertyMultiple request to a malicious BACnet/IP peer, the peer can reply with a malformed but structurally valid ReadPropertyMultiple-ACK that drives the client into a global-buffer-overflow read on the global receive buffer Rx_Buf. This issue has been patched in versions 1.4.5, 1.5.1, and 1.6.0.

### CVE-2026-52790

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-416;CWE-562` |
| Published | 2026-11-13T16:19:02.587 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.5, 1.5.1, and 1.6.0, there is a library-level memory safety issue that is reachable from an unmodified official sample server (apps/server-basic/main.c) over BACnet/IP resulting in a stack-use-after-return in writable Device string properties. This issue has been patched in versions 1.4.5, 1.5.1, and 1.6.0.

### CVE-2026-52789

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-13T16:19:02.440 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.5, 1.5.1, and 1.6.0, a Denial of Service (DoS) vulnerability exists in the BACnet stack's ReadPropertyMultiple (RPM) handler. When processing a malformed RPM request packet that lacks the expected closing tags, the function handler_read_property_multiple enters an infinite loop. This issue has been patched in versions 1.4.5, 1.5.1, and 1.6.0.

### CVE-2026-52787

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-131;CWE-787` |
| Published | 2026-11-13T16:19:02.137 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.5, 1.5.1, and 1.6.0-rc2, a reachable out-of-bounds write exists when encoding the device.address-binding property. This issue has been patched in versions 1.4.5, 1.5.1, and 1.6.0-rc2.

### CVE-2026-49341

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-674` |
| Published | 2026-11-13T16:19:01.817 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to version 1.5.1, there is a remotely reachable denial-of-service vulnerability in bacnet-stack affecting the default demo server built from the unmodified apps/server/main.c. This issue has been patched in version 1.5.1.

### CVE-2026-124267

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T15:17:36.270 |

Missing Authorization vulnerability in Noor Alam Gmail SMTP gmail-smtp allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Gmail SMTP: from n/a through 1.2.3.23.

### CVE-2026-118976

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-13T15:17:32.237 |

In Progress® Telerik® UI for Blazor versions v11.1.0 through v14.0.0, the demo application's Chat AI Integration example contains a relative path traversal vulnerability that could allow an attacker to read files outside of the chat attachments folder that are within the server's filesystem scope.

### CVE-2026-110278

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-294` |
| Published | 2026-11-13T22:17:20.900 |

IBM ContextForge MCP Gateway 1.0.0 through 1.1.0 could allow an attacker to replay identity propagation claims signatures or expose sensitive user identity information to third-party MCP servers due to static signature payloads and missing per-gateway configuration checks during tool invocation.

### CVE-2026-9661

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-13T22:17:27.467 |

Poste Italiane Postecert FIRMAOK! 1.6.29 on Windows contains a local privilege escalation vulnerability caused by an uncontrolled OpenSSL search path, where launcher.exe and dependent executables such as updater.exe and tslupdater.exe load OpenSSL configuration and library files from a hardcoded, user-writable directory that does not exist by default. A low-privileged local attacker can create this missing directory and place malicious OpenSSL configuration or library files inside it, causing the application to load and execute attacker-controlled code with the privileges of the user running it, enabling horizontal or, when a higher-privileged user runs the application, vertical privilege escalation up to full system compromise.

### CVE-2026-107522

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-13T15:17:29.357 |

Dell PowerStore contains an Improper Authorization vulnerability. An authenticated user could exploit this vulnerability, potentially leading to privilege escalation to administrator.

### CVE-2026-103769

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-13T15:17:28.850 |

Deserialization of Untrusted Data vulnerability in Acowebs PDF Invoices and Packing Slips For WooCommerce pdf-invoices-and-packing-slips-for-woocommerce allows Object Injection.This issue affects PDF Invoices and Packing Slips For WooCommerce: from n/a through 1.4.10.

### CVE-2026-129432

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-14T13:17:22.680 |

Ettercap through 0.8.5.1 contains a heap out-of-bounds read vulnerability in dissector_mountd() in src/dissectors/ec_mountd.c that validates RPC credential and directory lengths independently rather than against the packet end. Network-adjacent attackers can send a crafted MOUNT MNT call to read up to 100 bytes past the heap buffer, leaking memory to the console and logs.

### CVE-2026-129431

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-14T13:17:22.533 |

Ettercap through 0.8.5.1 contains a heap out-of-bounds read vulnerability in dissector_socks() in src/dissectors/ec_socks.c that allows network-adjacent attackers to read heap memory via unchecked SOCKS5 username/password lengths. Attackers can send a crafted SOCKS5 authentication packet observed by Ettercap to read up to 255 bytes past the heap buffer, disclosing memory printed and logged as captured credentials.

### CVE-2026-129429

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-14T13:17:22.243 |

Frappe india-payroll before 16.0.4 contains a missing authorization vulnerability in the get_employee_details, compute_tax_comparison and set_tax_regime methods of tax_regime_selector.py that allows authenticated low-privileged users to access other employees' payroll data. Attackers can supply another employee identifier to read base pay and earning and deduction components, or change the tax regime on draft Salary Structure Assignments to affect tax withholding.

### CVE-2026-124969

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-14T05:18:32.480 |

The Optimole – Optimize Images | Convert WebP & AVIF | CDN & Lazy Load | Image Optimization plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the replace_urls_in_value function in all versions up to, and including, 4.2.19. This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). Successful exploitation requires PEAR's Archive_Tar library to be present and loadable on the host (common in official WordPress Docker images and many PHP distributions), and an administrator must subsequently use the plugin's Rename control on any attachment after the attacker has staged a malicious payload in a comment. Successful exploitation additionally requires an action by an administrator — the attacker cannot trigger the vulnerability on their own.

### CVE-2026-89037

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-13T21:17:48.173 |

Dolibarr before 24.0.2 contains an insecure direct object reference vulnerability in the REST Documents API for the ticket module that allows authenticated API users to access ticket attachments belonging to other companies by omitting a company-scope check that is only applied via a session variable set during public ticket authentication, which REST API authentication never sets. Attackers with ticket read permission can enumerate predictable ticket identifiers and supply them to the documents endpoint or download path to retrieve sensitive attachments such as invoices and contracts belonging to other third parties.

### CVE-2026-127216

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-13T21:17:43.483 |

Injection Guard plugin for WordPress before 1.4.0 contains a cross-site request forgery vulnerability that allows unauthenticated attackers to trigger password hash export by tricking a logged-in administrator into loading a crafted link, since the ig_settings admin page in templates/dashboard.php processes GET parameters without nonce verification. Attackers can exploit this to cause the plugin to write WooCommerce customer email hashes and password hashes to an unprotected file at wp-content/plugins/injection-guard/ab-hash.dat, which can then be downloaded without authentication to obtain customer password hashes for offline cracking.

### CVE-2026-67444

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-434` |
| Published | 2026-11-13T19:19:34.503 |

Hubleys is a dashboard for self-hosted services. Prior to version 0.5.2, any authenticated (non-admin) Hubleys user can upload a file with an arbitrary extension as their dashboard "background image," and the server will later serve that file back with a Content-Type derived straight from the attacker's chosen extension - so uploading an .html file gets it served as text/html. Because the endpoint that serves it returns a manually-constructed response rather than going through SvelteKit's normal page-rendering pipeline, the app's configured Content-Security-Policy never gets attached to it either, so a script embedded in the upload runs unrestricted. This issue has been patched in version 0.5.2.

### CVE-2026-129166

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T18:17:41.753 |

Keep 0.34.10 through 0.55.0 contains a blind SQL injection vulnerability in its CEL-to-SQL converter, which inserts bracket-indexed JSON keys from CEL filters unescaped into JSON path expressions for SQLite, PostgreSQL, and MySQL. Authenticated users with read:alert permission can submit crafted CEL expressions to /alerts/query or the cel parameter of /incidents, using result counts as a boolean oracle to extract other tenants' alerts and password hashes.

### CVE-2026-129160

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T18:17:40.853 |

free-fs 2.0.1 through 2.3.1 contains an SQL injection vulnerability in FileShareServiceImpl.getPages, which passes the orderBy parameter of the /apis/share/pages endpoint verbatim into the ORDER BY clause via MyBatis-Flex without a column whitelist. Authenticated users can supply CASE WHEN subquery expressions that use share ordering as a boolean oracle to read arbitrary database contents, such as share codes.

### CVE-2026-129153

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-13T18:17:39.683 |

SurveyKing 1.12.0 through 1.13.2 contains an authorization bypass in the linked survey feature that fails to verify the referenced linkSurveyId belongs to the caller's own project. Authenticated attackers can point a linked option at another user's survey so that loadLinkResult and updateLinkSurveyAnswer read, rewrite, or create responses in that survey.

### CVE-2026-107398

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-13T18:17:26.153 |

Indico is a feature-rich event management system. Prior to version 3.3.14, due to a path traversal vulnerability when building an "offline copy" of an event, a malicious event manager has the ability to retrieve the content of any local file that's readable by the user running Indico on the server. This issue has been patched in version 3.3.14.

### CVE-2026-63164

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-13T17:17:33.850 |

Omnispace Agora Project through 26.10.0 contains an insecure direct object reference vulnerability that allows authenticated attackers to access another user's private mail by supplying a crafted reloadMailTypeId parameter to Ctrl::getCurObj() without a readRight() ownership check in CtrlMail.php. Attackers can manipulate the mail identifier value, such as reloadMailTypeId=mail-1, to retrieve the title and body of private messages belonging to other users, resulting in unauthorized disclosure of sensitive communications.

### CVE-2026-129130

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-13T17:17:30.660 |

agent-device from 0.21.36 before 0.21.37 contains a local file disclosure vulnerability that allows authenticated remote callers to read daemon-host files by opening file:// URLs. Attackers can send an open command with a file:// target through /rpc, then issue snapshot to read any plaintext file readable by the daemon account.

### CVE-2026-129119

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-13T17:17:28.753 |

C-Kermit from 6.0.192 before 11.1.515 contains a file collision protection bypass that allows malicious senders to append data to existing files by marking transfers as RESEND. The gattr() function in ckcfn3.c clears the REJECT discard flag and switches to APPEND without a RECEIVE CONFIRM prompt, letting attackers modify files such as shell startup files.

### CVE-2026-126818

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-311` |
| Published | 2026-11-13T16:18:46.463 |

A Ruby object-document mapper does not apply its automatic field-level encryption configuration to certain fields when the data model uses class inheritance. Values the application designated for encryption are written to the database in readable form without any error or warning. A database account holding only read access to the application's collections, and no access to the encryption key store, may obtain those values.

### CVE-2026-127102

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-863` |
| Published | 2026-11-13T15:17:44.177 |

In Eclipse BaSyx Go Components versions up to and including 1.1.2, ABAC-enabled deployments of the Submodel Repository and the AAS Environment return Submodel Elements that the caller is not authorized to read from `GET /submodels/{submodelIdentifier}/submodel-elements`.



If an access rule grants READ on a single Submodel Element through a `$sme` `REFERABLE` object, the list route returns every element of that Submodel, including its value, as soon as one element matches the caller's rules. The single-element route and the full Submodel read enforce the same rule and deny access to the other elements. An authenticated caller with a READ grant for one element of a Submodel can therefore read all other elements of that Submodel.



The issue is fixed in Eclipse BaSyx Go Components v1.1.3.

### CVE-2026-125856

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T15:17:43.403 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Sarah Giles Dynamic User Directory dynamic-user-directory allows Reflected XSS.This issue affects Dynamic User Directory: from n/a through 2.4.

### CVE-2026-125854

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T15:17:43.120 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Unbounce Unbounce Landing Pages unbounce allows Stored XSS.This issue affects Unbounce Landing Pages: from n/a through 1.1.6.

### CVE-2026-125837

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T15:17:42.553 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in thethemefoundry Make make allows Reflected XSS.This issue affects Make: from n/a through 1.10.10.

### CVE-2026-125783

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T15:17:40.070 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in madalin.ungureanu Custom Post Types and Custom Fields creator – WCK wck-custom-fields-and-custom-post-types-creator allows Reflected XSS.This issue affects Custom Post Types and Custom Fields creator – WCK: from n/a through 2.4.0.

### CVE-2026-125452

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T15:17:39.700 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Denishua WPJAM Basic wpjam-basic allows Reflected XSS.This issue affects WPJAM Basic: from n/a through 7.1.2.

### CVE-2026-124420

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T15:17:37.403 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Themeisle Woody ad snippets insert-php allows Reflected XSS.This issue affects Woody ad snippets: from n/a through 2.7.10.

### CVE-2026-124410

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T15:17:36.683 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in wpLingua Translation Service Translate and boost SEO &#8211; Automatic AI translation &#8211; wpLingua wplingua allows Stored XSS.This issue affects Translate and boost SEO &#8211; Automatic AI translation &#8211; wpLingua: from n/a through 3.1.1.

### CVE-2026-124272

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T15:17:36.410 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Dimitri Grassi Salon booking system salon-booking-system allows Reflected XSS.This issue affects Salon booking system: from n/a through 10.31.14.

### CVE-2026-124260

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T15:17:35.997 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Jacob N. Breetvelt WP Photo Album Plus wp-photo-album-plus allows Reflected XSS.This issue affects WP Photo Album Plus: from n/a through 9.3.06.001.

### CVE-2026-119517

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T15:17:32.630 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in VillaTheme Catna – Woo Name Your Price and Offers catna-woo-name-your-price-and-offers allows Reflected XSS.This issue affects Catna – Woo Name Your Price and Offers: from n/a through 2.0.3.

### CVE-2025-53699

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1299` |
| Published | 2026-11-13T22:17:18.830 |

Missing protection mechanism for alternate hardware interface vulnerability in Johnson Controls iSTAR Ultra, Johnson Controls iSTAR Ultra SE, Johnson Controls iSTAR Ultra G2, Johnson Controls iSTAR Ultra G2 SE, and Johnson Controls iSTAR Edge G2 allows CAPEC‑554: Functionality Bypass.

This issue affects iSTAR Ultra: before 6.9.2.CU02; iSTAR Ultra SE: before 6.9.2.CU02; iSTAR Ultra G2: before 6.9.2.CU02; iSTAR Ultra G2 SE: before 6.9.2.CU02; iSTAR Edge G2: before 6.9.2.CU02.

### CVE-2025-53698

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1299` |
| Published | 2026-11-13T22:17:18.693 |

Missing protection mechanism for alternate hardware interface vulnerability in Johnson Controls iSTAR Ultra and Johnson Controls iSTAR Ultra SE allows CAPEC‑554: Functionality Bypass.

This issue affects iSTAR Ultra: before 6.9.2.CU02; iSTAR Ultra SE: before 6.9.2.CU02.

### CVE-2026-97358

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:L/SC:L/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-830` |
| Published | 2026-11-13T18:17:50.140 |

An inclusion of web functionality from an untrusted source could allow remote code execution on SpaceCom

### CVE-2026-124680

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-11-13T18:17:31.533 |

Interpretation Conflict, resulting in (Incorrect Authorization) vulnerability in Apache APISIX.



An unauthenticated client can reach upstream paths protected
by a route-level auth plugin when a route without auth exists on the
same upstream and the upstream does not collapse encoded dot segments.



This issue affects Apache APISIX: from 0.9 through 3.19.0.



Users are recommended to upgrade to version 3.20.0, which fixes the issue.

### CVE-2026-95379

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-13T16:19:38.563 |

Path traversal in the certificate.deleteCertificate JSON-RPC method (POST /api/rpc) of the turbineweb web interface in Zenitel VSFF6, VSFF8, VSFF8MP, VSFF8MN, and VSFT devices with software versions from 10.0.3.0 before 10.1.3.0 allows authenticated administrators to delete arbitrary files as root via a relative path (../) in the file_name parameter.



This can be used to cause denial of service or render the device inoperable by removing critical system files, and to weaken device security by removing files such as firewall rules or certificate trust stores.

### CVE-2026-129105

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-11-13T16:19:00.397 |

Cudy TR3000 before 2.5.42 contains an option injection vulnerability that allows authenticated administrators to inject arbitrary pppd options by embedding quotes and newlines in L2TP credentials. Attackers can submit crafted usernames or passwords to the net.set_wan RPC method, which l2tp.sh writes into a pppd options file, adding options like logfile to the root pppd process.

### CVE-2026-129104

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-11-13T16:19:00.240 |

Cudy TR3000 before 2.5.42 contains a dnsmasq configuration injection vulnerability that allows authenticated administrators to inject directives by embedding a newline in the net.set_dhcp leasetime field. Attackers can append address= entries via /etc/init.d/dnsmasq to alter DNS answers for LAN clients, or insert invalid lines that stop dnsmasq.

### CVE-2026-129092

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-13T15:17:45.513 |

CCC Attestation SIG attested-tls-poc through commit 731ca82 contains a time-of-check time-of-use vulnerability because Evidence is appraised only once during the TLS handshake, without post-handshake re-attestation. Attackers with local access to the attesting endpoint can alter workload code, data, configuration, or attached devices like GPUs while peers keep trusting the original Evidence.
