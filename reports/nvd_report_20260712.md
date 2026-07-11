# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-11 15:00 UTC
- **対象期間**: `2026-07-10T15:00:37.000Z` 〜 `2026-07-11T15:00:14.000Z`
- **重要CVE数**: 130 件（Critical 9.0+: 22 件 / High 7.0〜: 108 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、**CVSS 7.0 以上が 30 件以上**と非常に多く、特に **AI/LLM 連携サービス** と **CMS 系プラグイン** に集中しています。  
- LLM の出力を直接実行する実装ミス（例：PraisonAI の `CodeAgent._execute_python()`）や、**ファイルアップロード・認証バイパス** が原因のリモートコード実行 (RCE) が多数報告され、攻撃者がネットワーク境界を越えて内部システムを完全制御できるリスクが顕在化しています。  
- 多くの脆弱性は **「デフォルトで認証が不要」**、**「入力検証が不十分」**、**「サンドボックスが無い」** といった設計上の欠陥に起因しており、**設定ミスやパッケージの古いバージョンが直ちに攻撃対象**になる点が共通しています。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 製品・コンポーネント | 主な問題点 | 影響範囲・攻撃シナリオ |
|-----|------|----------------------|------------|------------------------|
| **CVE‑2026‑61447** | 10.0 | PraisonAI < 1.6.78 (CodeAgent) | LLM が生成した Python コードを **AST 解析・サンドボックスなし**で実行。プロンプトインジェクションで任意コード実行可能。 | 攻撃者は任意の Python スクリプトを実行し、環境変数・シークレットの取得、さらに内部ネットワークへの横展開が可能。 |
| **CVE‑2026‑57827** | 10.0 | Joomla! 拡張 **RSFiles** | 認証不要の **任意ファイルアップロード**。アップロードされた PHP 等実行ファイルでフル RCE。 | 公開された Joomla サイト全体が乗っ取られ、データベース情報や管理者権限取得が容易になる。 |
| **CVE‑2026‑55500** | 9.9 | 9Router < 0.4.80 (API) | `/api/settings/database` が **認証なし**でデータベース全体のエクスポート/インポートを許可。 | 攻撃者は全 API キー・OAuth トークン・設定情報を取得し、さらにデータベースを書き換えてサービスを停止させられる。 |
| **CVE‑2026‑57807** | 9.8 | miniOrange **OAuth SSO (OAuth Client)** ≤ 38.5.8 | 認証バイパス（代替経路）により **パスワードリカバリ** が不正利用可能。 | 攻撃者は管理者アカウントのパスワードリセットを実行し、SSO 環境全体への不正ログインが可能になる。 |
| **CVE‑2026‑12761** | 9.8 | miniOrange **Social Login & Register** ≤ 7.7.0 (WordPress) | `email_` パラメータで任意メールアドレスを受け付け、認証フローを迂回。 | 攻撃者は任意ユーザーとしてログインでき、WordPress 管理画面や連携サービスへの不正アクセスが可能。 |

> **選定理由**  
> - **CVSS が 10.0 に近い**（最高リスク）こと。  
> - **広範囲に展開されているプラットフォーム**（Joomla、WordPress、AI SaaS）であり、**多数の組織が利用中**。  
> - **認証不要・デフォルト設定のまま**で攻撃が成立する点が、即時の緊急対策を要するため。

---

## 3. 推奨アクション  

### 3.1 共通の緊急対策
- **インターネットに公開されている全サービスのファイアウォール設定を見直し**、不要なポート・エンドポイントは外部から遮断。  
- **最小権限の原則 (Least Privilege)** を適用し、API キーや管理者トークンの権限を必要最小限に絞る。  
- **監査ログの有効化** と **SIEM へのリアルタイム転送** を実装し、異常なリクエスト（例：大量のファイルアップロード、未認証のエクスポート要求）を即座に検知。  
- **バックアップの定期取得とリストア手順の検証**（特にデータベース全体のエクスポート機能がある製品は必須）。  

### 3.2 製品別具体的対策  

| 製品 | 現行バージョン | 推奨バージョン | 具体的作業 |
|------|----------------|----------------|------------|
| **PraisonAI** | < 1.6.78 / < 4.6.78 | **≥ 1.6.78**（CodeAgent 修正）<br>**≥ 4.6.78**（AICoder・deploy/api.py 等全体修正） | - 公式リリースノートに従いアップデート。<br>- `api_key` 必須化、CORS を `origin` に限定。<br>- `CodeAgent._execute_python()` に **AST 検証** と **サンドボックス** を導入。 |
| **Joomla! RSFiles** | 任意（脆弱バージョン） | **公式パッチリリース**（2026‑Q2 以降）または **RSFiles 2.5.0 以降** | - アップロード許可ファイルタイプを **画像・PDF のみ** に制限。<br>- `upload_max_filesize` と `post_max_size` を適切に設定。<br>- `mod_security` で `file_upload` ルールを強化。 |
| **9Router** | < 0.4.80 | **≥ 0.4.80** | - `/api/settings/database` エンドポイントに **認証ミドルウェア** を追加。<br>- 環境変数・シークレットは **Vault** 等外部シークレット管理へ移行。 |
| **miniOrange OAuth SSO (OAuth Client)** | ≤ 38.5.8 | **≥ 38.5.9** | - パスワードリカバリフローに **CAPTCHA** と **IP レートリミット** を導入。<br>- `oauth_client

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-61447

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-11T14:16:23.377 |

PraisonAI before 1.6.78 contains a remote code execution vulnerability in CodeAgent._execute_python() that executes LLM-generated Python code without AST validation, import restrictions, or sandbox enforcement. Attackers can influence LLM output through prompt injection to exfiltrate all environment secrets and execute arbitrary code on the host system.

### CVE-2026-57827

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:Red` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-11T10:16:34.057 |

The Joomla extension RSFiles is vulnerable to an unauthenticated arbitrary file upload that allows uploading executable files and leads to full RCE.

### CVE-2026-55500

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-10T16:16:33.357 |

9Router is an AI router & token saver. Prior to 0.4.80, the /api/settings/database endpoint allows full database export (containing all credentials, API keys, OAuth tokens, and settings) and full database import (complete overwrite) without any authentication requirement beyond the ALWAYS_PROTECTED middleware check, which only validates JWT or CLI token. This issue is fixed in version 0.4.80.

### CVE-2026-57807

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-07-10T21:16:59.947 |

Authentication Bypass Using an Alternate Path or Channel vulnerability in miniOrange Security Software Pvt Ltd. OAuth Single Sign On - SSO (OAuth Client) allows Password Recovery Exploitation.

This issue affects OAuth Single Sign On - SSO (OAuth Client): from n/a through 38.5.8.

### CVE-2026-12761

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-10T21:16:53.160 |

The miniOrange Social Login and Register (Discord, Google, Twitter, LinkedIn) plugin for WordPress is vulnerable to authentication bypass leading to account takeover in versions up to and including 7.7.0. This is due to the Profile Completion flow accepting an arbitrary email address via the 'email_field' POST parameter without verifying that the email belongs to the identity returned by the OAuth provider, combined with send_otp_token() returning the SHA-512(customer_key || otp) transaction hash to the client where the OTP space is only 99,000 values (wp_rand(1000, 99999)) and the customer_key is a static option (empty on unregistered installs). This makes it possible for unauthenticated attackers to trigger an OTP email to an arbitrary admin's address, crack the OTP offline from the leaked hash in under a second, and submit the cracked OTP to mo_openid_social_login_validate_otp(), which logs the attacker in as the user whose email was supplied — granting full administrator access.

### CVE-2026-5801

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-10T19:17:27.323 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Semtek Informatics Software Consulting Trade Ltd. Co. SEM-PMP allows Command Line Execution through SQL Injection.

This issue affects SEM-PMP: through 23042026.

### CVE-2026-2397

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-10T18:16:20.613 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Adam Retail Automation Ltd. MobilMen 20T allows SQL Injection.

This issue affects MobilMen 20T: from v3 through 10072026. NOTE: The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-59151

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-10T19:17:26.780 |

Prowler is a cloud security platform. Prior to 5.30.3, Prowler's SAML authentication flow trusted the email domain asserted in a SAMLResponse when deciding which tenant should receive the final token, and the ACS finish logic in api/src/backend/api/v1/views.py recalculated the tenant from user.email instead of binding token issuance to the validated SAML configuration. An authenticated attacker with a controlled SAML IdP could complete a valid SAML flow for an attacker-controlled domain while asserting an email address from another configured domain, causing a SAMLToken and tenant-scoped JWT to be issued for the wrong tenant and enabling cross-tenant account takeover. This issue is fixed in version 5.30.3.

### CVE-2026-59792

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-23` |
| Published | 2026-07-10T15:16:48.240 |

In JetBrains IntelliJ IDEA before 2026.1.4, 
2026.2 code execution via path traversal in project workspace ID handling was possible

### CVE-2026-61445

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-11T14:16:23.240 |

PraisonAI before 4.6.78 contains arbitrary file write and command execution vulnerabilities in the AICoder component due to missing path validation and command sanitization in LLM tool calls. Attackers can inject malicious prompts through the chat interface to write files to arbitrary filesystem locations and execute arbitrary shell commands with root privileges.

### CVE-2026-61444

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-10T15:16:50.610 |

PraisonAI versions before 4.6.78 contain a code injection vulnerability in deploy/api.py where the agents_file parameter is directly interpolated into an f-string without sanitization. Attackers can inject arbitrary Python code that executes when the generated server code runs via subprocess.Popen().

### CVE-2026-60090

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-11T14:16:22.353 |

PraisonAI before 4.6.78 fails to validate the caller-controlled dimension argument in the PGVector and Cassandra knowledge-store create_collection() backends. Although schema, keyspace, and collection-name identifiers are validated, the dimension value (declared as int but not enforced at runtime) is interpolated directly into the vector column of the generated CREATE TABLE DDL. A caller able to influence collection-creation dimensions can pass a string such as '3); DROP TABLE tenant_secrets; --' to inject SQL/CQL tokens into the statement executed by the database driver.

### CVE-2026-20744

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-10T23:16:47.683 |

The charging station websocket endpoint accepts connections without 
proper authentication, which could lead to privilege escalation.

### CVE-2026-55879

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-10T21:16:57.367 |

OpenReplay is a self-hosted session replay suite. From 1.24.0 before 1.25.0, the OpenReplay tracking SDK accepts custom event names and captured page URLs from any visitor using a public project key, stores them in ClickHouse without output encoding, and later renders them in the authenticated dashboard through TextEllipsis and the event-details modal, allowing an unauthenticated attacker to store script that executes in the dashboard origin, reads the session JWT from localStorage, and takes over a dashboard account. This issue is fixed in version 1.25.0.

### CVE-2026-61459

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-07-10T19:17:27.450 |

MCP Server Kubernetes before 3.9.0 contains an argument injection vulnerability in structured tools (kubectl_get, kubectl_describe, kubectl_delete) that allows attackers to bypass the assertNoDangerousFlags security check by supplying resourceType and name parameters with leading dashes. Attackers can inject the --server flag to redirect kubectl commands to an attacker-controlled API server, causing the operator's bearer token to be transmitted externally and enabling full cluster compromise.

### CVE-2026-15143

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-10T16:16:25.680 |

A flaw was found in the file_type content detector of guardrails-detectors. This vulnerability allows a remote attacker to supply an arbitrary XML Schema Definition (XSD) string, which is processed without proper restrictions. This can lead to server-side requests to arbitrary URLs or local file reads, potentially resulting in sensitive information disclosure, such as cloud provider credentials or access to internal network services.

### CVE-2026-56765

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-10T15:16:43.727 |

Vikunja before 2.2.1 contains an authorization flaw where the LinkSharing.ReadAll endpoint exposes share hashes to users with read access, enabling permission escalation to admin-level shares. The GetTaskAttachment endpoint performs permission checks against user-supplied task IDs but fetches attachments by sequential ID without verifying ownership, allowing attackers to download and delete all file attachments across all projects instance-wide.

### CVE-2026-55884

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-10T22:16:44.423 |

Tilt defines dev environments as code for microservice apps on Kubernetes. From 0.20.8 through 0.37.3, the Tilt HUD HTTP server registers handlers on a gorilla/mux router with no authenticating middleware. When the HUD is bound to a non-loopback address, an unauthenticated network caller can trigger developer-defined resources, tamper with Tiltfile arguments, read full engine state including the session token, and invoke apiserver resources through the token-attaching /proxy handler. This issue is fixed in version 0.37.4.

### CVE-2026-58492

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-10T17:17:01.670 |

grav-plugin-database is the database plugin for Grav CMS. Prior to 1.2.0, the PDO::tableExists method interpolates its table argument directly into a raw SQL query string without sanitization, escaping, quoting, or whitelisting, allowing attacker-controlled table names passed by consuming plugin or developer code to execute arbitrary SQL against the configured database. This issue is fixed in version 1.2.0.

### CVE-2026-56261

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-10T15:16:42.017 |

Crawl4AI before 0.8.7 contains a server-side request forgery (SSRF) vulnerability in the Docker API server's /crawl/job and /llm/job endpoints, which accept webhook URLs without destination validation. An attacker can supply webhook URLs pointing to private or internal IP ranges, Docker networks, or cloud metadata endpoints (e.g. 169.254.169.254), causing the server to make requests to internal services and potentially expose cloud metadata.

### CVE-2026-51119

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-10T17:16:57.587 |

An issue in Invixium IXM WEB v.2.3.85.25 allows an attacker to escalate privileges via the /SystemUsers/CreateAppUser components

### CVE-2026-57828

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-11T10:16:35.710 |

The Joomla extension Phoca Downloads is vulnerable to an authenticated arbitrary file upload that allows registered users uploading executable files and leads to full RCE.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-61426

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-11T14:16:22.483 |

PraisonAI before 1.7.3 contains an insecure default configuration that binds to all interfaces with no API key requirement and wildcard CORS. Unauthenticated attackers can call GET /api/agents to read agent instructions and system prompts, or POST /api/chat to invoke agents without authentication.

### CVE-2026-1359

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-11T09:16:16.020 |

The Genolve – AI image AI video generation plugin for WordPress is vulnerable to unauthorized modification of data due to a missing capability check on the genolve_setOpt() function in all versions up to, and including, 5.0.5. This makes it possible for authenticated attackers, with Contributor-level access and above, to update arbitrary WordPress options, including enabling user registration and setting the default role to administrator, resulting in privilege escalation.

### CVE-2026-15155

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-07-11T07:16:46.170 |

The Essential Addons for Elementor – Popular Elementor Templates & Widgets plugin for WordPress is vulnerable to Authenticated Account Takeover via Email Header Injection in all versions up to, and including, 6.6.10 This is due to insufficient server-side validation of a Login/Register widget setting used to construct outgoing email headers — the allowed-values restriction is enforced only in the client-side editor UI and not on the server, and the applied sanitization does not strip or encode CR/LF characters, allowing CRLF sequences stored in that setting to survive into raw mail headers. This makes it possible for authenticated attackers, with Contributor-level access and above, to inject an additional Bcc header into the WordPress administrator's password-reset notification email, receive a copy of a valid administrator password-reset link, and achieve full administrator account takeover.

### CVE-2025-6784

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-07-11T07:16:44.637 |

The Code Engine plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 0.3.5 via the 'code-engine' shortcode. This is due to the plugin not restricting access to the code injecting functionality of the plugin. This makes it possible for authenticated attackers, with Contributor-level access and above, to execute code on the server.

### CVE-2026-2354

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-11T05:16:33.777 |

The Swiss Toolkit For WP plugin for WordPress is vulnerable to arbitrary file upload due to a flawed file type validation bypass in the `upload_extension_files()` function in all versions up to, and including, 1.4.6. The `upload_extension_files()` function hooks into WordPress's `wp_check_filetype_and_ext` filter and uses `strpos()` to check if a filename contains a configured extension string, rather than verifying the actual file extension. This makes it possible for authenticated attackers, with Author-level access and above, to upload arbitrary files (including PHP) on the affected site's server which may make remote code execution possible, granted the "Enhanced Multi-Format Image Support" feature is enabled with at least one extension (e.g., avif) in the allowed formats.

### CVE-2026-14262

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-11T05:16:32.367 |

The Simple JWT Login – Allows you to use JWT on REST endpoints. plugin for WordPress is vulnerable to Authentication Bypass to Privilege Escalation in all versions up to, and including, 3.6.6 via the `payload` parameter. The vulnerability exists because `AuthenticateService::generatePayload()` only overwrites JWT payload keys whose names appear in the admin-configured `jwt_payload` list — leaving any attacker-supplied identity claims such as `email`, `id`, or `username` intact and signed into the JWT with the site's HS256 secret. This makes it possible for authenticated attackers, with subscriber-level access and above, to escalate their privileges to that of an Administrator by injecting a target administrator's email address into the `payload` parameter at the `/wp-json/simple-jwt-login/v1/auth` endpoint, then redeeming the resulting JWT at the `/autologin` endpoint to obtain a fully authenticated session as that administrator.

### CVE-2026-13353

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-11T04:17:16.937 |

The WP Ultimate CSV Importer – WordPress Import & Export for CSV, XML & Excel plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 8.0.1 via the 'MappedFields' parameter. This is due to missing capability checks on the AJAX handlers for install_addon, saveMappedFields, and StartImport, combined with the plugin nonce being exposed to any authenticated user who can load an admin page, allowing a Subscriber to install the Import WooCommerce add-on, persist attacker-controlled PHP expressions in the MappedFields parameter, and trigger evaluation via eval() in ImportHelpers::get_meta_values(). This makes it possible for authenticated attackers, with subscriber-level access and above, to execute code on the server.

### CVE-2026-13756

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-11T02:16:17.457 |

The WP Grid Builder plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 2.3.3. This is due to missing authorization and meta key validation in the `update()` handler for the `/wp-json/wpgb/v2/metadata` REST endpoint. This makes it possible for authenticated attackers, with Subscriber-level access and above, to elevate their privileges to Administrator by updating their own `wp_capabilities` user meta with a crafted nested array payload.

### CVE-2026-44795

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-470;CWE-502` |
| Published | 2026-07-10T22:16:41.717 |

Spinnaker is an open source, multi-cloud continuous delivery platform. Prior to 2026.1.0, 2026.0.3, 2025.4.4, and 2025.3.3, unsafe YAML processing bypasses safe deserialization when using CloudFormation deployments or CloudFoundry baking. The use of a non-safe constructor allows arbitrary loading of Java classes, leading to remote code execution. This issue is fixed in versions 2026.1.0, 2026.0.3, 2025.4.4, and 2025.3.3.

### CVE-2026-6212

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-10T19:17:27.840 |

Authorization bypass through User-Controlled key vulnerability in Teracity Software Technologies Inc. TeraMIS allows Privilege Abuse.

This issue affects TeraMIS: from V03.26.01.14 through 30.04.2026.

### CVE-2026-2398

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-10T17:16:56.320 |

Authorization bypass through User-Controlled key vulnerability in Adam Retail Automation Ltd. MobilMen 20T allows Privilege Escalation.

This issue affects MobilMen 20T: from v3 through 10072026. NOTE: The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-54149

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-10T16:16:32.587 |

MaxKB is an open-source AI assistant for enterprise. Prior to 2.10.0-lts, MaxKB tool import functionality in apps/tools/serializers/tool.py and MCP referencing mode in apps/application/chat_pipeline/step/chat_step/impl/base_chat_step.py do not consistently validate MCP transport type, allowing an authenticated user to import a .tool file containing stdio transport with malicious commands and trigger the configuration through an AI Chat node so MultiServerMCPClient executes arbitrary system commands. This issue is fixed in version 2.10.0-lts.

### CVE-2026-59793

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-07-10T15:16:48.350 |

In JetBrains TeamCity before 2026.1.2 arbitrary file access was possible via the Perforce VCS integration

### CVE-2026-61454

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-11T14:16:23.630 |

The Grav Admin2 plugin (getgrav/grav-plugin-admin2) before 2.0.4 embeds a global JavaScript variable window.__GRAV_CONFIG__ in the Admin2 SPA bootstrap page at /grav/admin (and its subroutes). This object is returned in every unauthenticated response and discloses the server URL, API prefix, admin base path, runtime environment type, and exact Grav and Admin2 version numbers, allowing an unauthenticated attacker to fingerprint the deployment and select version-specific exploits without reconnaissance.

### CVE-2026-61439

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-07-11T14:16:22.870 |

PraisonAI versions before 4.6.78 contain a prompt injection defense misconfiguration where the block threshold defaults to CRITICAL severity, allowing HIGH-level threats to pass through unblocked. Attackers can submit single-vector prompt injection attacks such as instruction overrides or financial manipulation that trigger HIGH severity detection but are logged without blocking, enabling system prompt extraction and unauthorized tool invocations.

### CVE-2026-56303

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-11T14:16:21.820 |

Capgo before 12.128.2 contains an information disclosure vulnerability in the find_apikey_by_value PostgreSQL function marked SECURITY DEFINER and executable by the anon role. Unauthenticated attackers can call this function via the /rest/v1/rpc/find_apikey_by_value endpoint to retrieve sensitive API key metadata including user_id, mode, org scoping, and expiration details when supplied a valid key value.

### CVE-2026-44383

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-07-10T23:16:48.343 |

Multiple connections to the backend using the same charging station ID 
are allowed, which could allow an attacker to deploy multiple instances 
of malicious OCPP clients to overwhelm the backend.

### CVE-2026-42952

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-07-10T23:16:48.203 |

Previously, there was no throttling on repeated authentication attempts 
to the charging station backend, which could allow an attacker to 
execute a denial-of-service attack.

### CVE-2026-14480

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-07-10T23:16:47.110 |

OpenPLC Runtime v3 contains an authenticated arbitrary file write 
vulnerability in the legacy web UI program‑upload workflow. The 
application stores an attacker‑supplied filename (prog_file) directly 
into the Programs.File database field and later uses this value as the 
destination path for an uploaded file without validating or restricting 
the path. Because Python os.path.join() honors attacker‑controlled 
absolute paths, an authenticated user can write arbitrary files anywhere
 writable by the OpenPLC webserver process. In the default build 
pipeline, all C++ source files within the OpenPLC runtime core directory
 are automatically compiled into the executable runtime binary. By 
writing a malicious .cpp file into this directory, an authenticated 
attacker can escalate the arbitrary file write into arbitrary native 
code execution when the operator triggers a normal program compilation 
and runtime start.

### CVE-2026-57584

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-07-10T22:16:44.560 |

Phalcon is a high-performance, full-stack PHP framework. Prior to 5.15.0, every Phalcon MVC application built with a default router registers a built-in route whose compiled PCRE pattern contains the nested quantifier (/.), and the same construct is produced by the /:params placeholder and the CLI router. Phalcon\Mvc\Router::handle() matches this pattern against the attacker-controlled request URI on every request, so a crafted path such as one containing repeated slashes followed by decoded newlines can trigger catastrophic backtracking and cause CPU exhaustion or route-matching failure. This issue is fixed in version 5.15.0.

### CVE-2026-57219

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-10T21:16:59.060 |

RabbitMQ is a messaging and streaming broker. Prior to 3.13.15, 4.0.20, 4.1.11, and 4.2.6, the obsolete GET /api/auth endpoint can disclose the OAuth 2 client secret on RabbitMQ installations configured with management.oauth_client_secret, exposing credentials to unauthenticated callers when the management plugin and that OAuth configuration are enabled. This issue is fixed in versions 3.13.15, 4.0.20, 4.1.11, and 4.2.6.

### CVE-2026-57850

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-10T20:16:48.663 |

RustDesk before 1.4.9 does not enforce a session's authorized connection scope on the server side, so a peer granted a limited session type (FileTransfer, PortForward, ViewCamera, or Terminal) can send control messages and login options reserved for a full Remote session. An authenticated remote peer can exploit this missing scope check to act outside its granted scope, injecting out-of-scope control messages to observe and control the host beyond the permissions it was given.

### CVE-2026-61461

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-10T19:17:27.713 |

Dify before 1.16.0-rc1 contains a SQL injection vulnerability in the MyScale vector store backend that allows attackers to execute arbitrary SQL by supplying unsanitized search parameters to the search_by_full_text method without escaping or parameterization. Attackers can inject malicious SQL through the search parameters to read, modify, or delete data in the underlying ClickHouse database.

### CVE-2026-61460

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-10T19:17:27.587 |

Krayin CRM through 2.2.3 contains an insecure direct object reference vulnerability in LeadController, PersonController, OrganizationController, QuoteController, and ActivityController that allows authenticated users to edit, update, or delete records owned by other users. Attackers can modify CRM records and reassign ownership by exploiting missing record-level ownership validation in edit, update, and destroy methods.

### CVE-2025-30007

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-10T19:17:18.130 |

HestiaCP before 1.9.5 contains an authenticated OS command injection vulnerability that allows low-privilege authenticated users to execute arbitrary commands as root by injecting a single-quote character into unvalidated DNS record types. Attackers can exploit insufficient input validation in is_dns_record_format_valid() combined with unsafe eval-based parsing in update_domain_zone() to prematurely close a variable assignment string and achieve full root code execution on the underlying host in a single DNS record creation step.

### CVE-2026-59190

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-10T17:17:02.647 |

grav-plugin-admin is an HTML user interface that provides a way to configure Grav and create and modify pages. In 1.10.52 and earlier, an authenticated attacker with admin.users permission can change the password of any user account, including the super administrator, by sending a direct POST request to /admin/user/{username}?task=save with data[password] because saveUser authorizes the caller's user-management permission but does not verify whether the caller may edit the target user. This issue is expected to be fixed in version 1.10.53.

### CVE-2026-59161

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-07-10T17:17:02.250 |

Excelize is a Go language library for reading and writing Microsoft Excel spreadsheets. Prior to 2.11.0, the streaming worksheet reader used by Rows and GetRows does not enforce the TotalRows limit on the row r attribute, allowing a small XLSX file with a row number above 1048576 and no cell coordinate to make GetRows append empty rows up to the attacker-controlled index and consume excessive memory and CPU. This issue is fixed in version 2.11.0.

### CVE-2026-53653

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-10T17:16:57.857 |

Grav is a file-based Web platform. Prior to 1.7.53 and 2.0.0-rc.8, Grav allows an unauthenticated visitor to exhaust server memory and CPU by requesting image derivatives with oversized dimensions through URL query image actions such as forceResize in Grav::fallbackUrl, which passes request parameters to ImageMedium magic actions without a dimension or pixel ceiling. This issue is fixed in versions 1.7.53 and 2.0.0-rc.8.

### CVE-2026-61434

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-10T15:16:50.213 |

PraisonAI versions before 4.6.78 contain an allowlist bypass vulnerability in shell command execution that allows attackers to execute restricted commands via find's built-in -exec, -execdir, and -delete actions. Attackers can craft find commands with these built-in actions to read blocked files, delete files, or execute non-allowlisted binaries without triggering shell metacharacter filters.

### CVE-2026-56305

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-620` |
| Published | 2026-07-10T15:16:42.300 |

Capgo before 12.128.2 contains an authentication bypass vulnerability in the password change endpoint that allows attackers to change user passwords without requiring current password confirmation. Attackers with temporary session access can exploit this flaw to permanently lock out legitimate users and achieve full account takeover.

### CVE-2026-56279

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-10T15:16:42.157 |

Capgo before 12.128.2 contains an information disclosure vulnerability in the get_orgs_v7(userid) RPC function that remains publicly invokable despite intended private access controls. Unauthenticated attackers can supply arbitrary user UUIDs to retrieve foreign users' organization membership, roles, management emails, and billing metadata.

### CVE-2026-38059

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-10T15:16:39.563 |

The iDirect iQ200 exposes the /api/identity and /api/ REST API endpoints without authentication. An unauthenticated attacker with network access can retrieve sensitive device information including the serial number, Device ID (DID), Terminal Private Key identifier (TPK), MAC address, and exact firmware version. The DID and TPK are used for satellite network authentication in the iDirect platform, potentially enabling terminal impersonation and network reconnaissance.

### CVE-2026-55852

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-10T22:16:43.970 |

Frappe is a full-stack web application framework. Prior to 16.23.0 and 15.112.0, TarSlip RCE was possible in Package Import because tarfile members were not sufficiently checked before extraction. This issue is fixed in versions 16.23.0 and 15.112.0.

### CVE-2026-52747

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-180` |
| Published | 2026-07-10T22:16:42.697 |

ModSecurity is an open source, cross platform web application firewall (WAF) engine for Apache, IIS and Nginx. Prior to 3.0.16, the multipart/form-data request body parser in libmodsecurity silently removes embedded line breaks from non-file form-field values before exporting them to ARGS and ARGS_POST because src/request_body_processor/multipart.cc overwrites reserved bytes in m_reserve instead of appending the current buffer. This creates a parser differential between ModSecurity and backend applications that preserve line breaks in form fields, allowing rules that inspect ARGS or ARGS_POST to miss payloads whose dangerous syntax depends on a line break. This issue is fixed in version 3.0.16.

### CVE-2026-57156

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-07-10T20:16:48.257 |

FreeRDP is a free implementation of the Remote Desktop Protocol. Prior to 3.28.0 on 32-bit builds, FreeRDP clients contain an integer overflow in update_read_delta_points in libfreerdp/core/orders.c when multiplying an attacker-controlled point count by sizeof(DELTA_POINT), allowing a malicious RDP peer to allocate an undersized heap buffer and then write beyond it during initialization. This issue is fixed in version 3.28.0.

### CVE-2026-55638

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-862;CWE-863` |
| Published | 2026-07-10T17:16:59.183 |

9Router is an AI router & token saver. Prior to 0.5.2, 9router protects /v1, /v1beta, /api/v1, and /api/v1beta in src/dashboardGuard.js but omits /codex before next.config.mjs rewrites /codex/* to /api/v1/responses. A remote unauthenticated attacker can send requests to /codex/* to bypass the API-key gate and cause the server to make upstream provider calls using operator-stored LLM provider credentials. This issue is fixed in version 0.5.2.

### CVE-2026-55665

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-10T21:16:56.847 |

Grist is spreadsheet software using Python as its formula language. Prior to 1.7.15, Grist contained two cross-site scripting vulnerabilities where an attacker-controlled value reached a link's href without scheme validation, so a javascript URL could run in a victim's Grist origin on a single click. On the account-selection page, /welcome/select-account used its next query parameter as the account buttons' link target. In document tours, the GristDocTour table's Link_URL column became a clickable button, allowing an editor of a shared document to store a javascript URL there that ran when another user opened the document and clicked the tour link. Because the script runs in the victim's authenticated session, it can call Grist APIs as the victim, reading or modifying data and changing sharing settings and access rules. A document editor could therefore escalate to owner-level access. This issue is fixed in version 1.7.15.

### CVE-2026-55789

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-91` |
| Published | 2026-07-10T20:16:47.933 |

Logto is the modern, open-source auth infrastructure for SaaS and AI apps. Prior to 1.41.0, Logto's self-hosted SAML application IdP built the signed SAML response and assertion by string-substituting user-controlled profile attributes such as name, email, and custom attribute-mapping values into element-text placeholders of a SAML XML template using samlify 2.10.0, which left those placeholders unescaped. An authenticated low-privilege user could place XML markup in a profile attribute so Logto signed a forged SAML attribute, such as an arbitrary role, allowing privilege escalation at relying Service Providers that authorize on SAML attributes. This issue is fixed in version 1.41.0.

### CVE-2026-54329

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-10T19:17:24.440 |

Snipe-IT is an IT asset/license management system. Prior to 8.6.2, the Accessories API create path mass-assigns request parameters to the Accessory model while company_id is mass assignable, allowing a low-privileged authenticated user in one company to create accessory records under another company when Full Multiple Companies Support is enabled. This issue is fixed in version 8.6.2.

### CVE-2026-61437

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-07-10T15:16:50.350 |

PraisonAI (pip package praisonaiagents) before 1.6.78 contains an unsafe dynamic module loading vulnerability in AgentFlow._resolve_pydantic_class (src/praisonai-agents/praisonaiagents/workflows/workflows.py). When a workflow step uses a string output_pydantic reference, the framework locates and imports a sibling tools.py from the workflow file's directory via importlib exec_module without sandboxing, ignoring the PRAISONAI_ALLOW_*_TOOLS environment variables. An attacker who controls a workflow file and its sibling tools.py can execute arbitrary Python code with the workflow runner's privileges when the workflow is executed via WorkflowManager or after load_yaml.

### CVE-2026-61429

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-11T14:16:22.740 |

PraisonAI versions before 1.6.78 contain a server-side request forgery vulnerability in the Crawl4AI/Chromium backend that allows attackers to bypass SSRF validation by exploiting DNS rebinding and HTTP redirects. Attackers can craft URLs that resolve to internal services after the initial validation check, enabling the headless browser to follow redirects and read internal responses including sensitive canary values.

### CVE-2026-55883

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-07-10T22:16:44.287 |

Tilt defines dev environments as code for microservice apps on Kubernetes. From 0.24.0 through 0.37.3, the Tilt HUD WebSocket at /ws/view is gated by a CSRF token, but the token is served by the unauthenticated /api/websocket_token endpoint and the upgrader accepts clients that omit an Origin header. When the HUD is network-exposed, an attacker who can reach the listener can open the HUD WebSocket and receive the full view stream, including session state, Tiltfile contents, resource statuses, and continued updates. This issue is fixed in version 0.37.4.

### CVE-2026-55882

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-10T22:16:44.113 |

Tilt defines dev environments as code for microservice apps on Kubernetes. From 0.19.5 through 0.37.3, the Tilt HUD server mounts Go net/http/pprof handlers under /debug with no access control. When the HUD or apiserver listener is network-exposed, an unauthenticated caller can read process memory through /debug/pprof/heap and /debug/pprof/goroutine, including session and apiserver tokens, and degrade performance through /debug/pprof/profile or /debug/pprof/trace. This issue is fixed in version 0.37.4.

### CVE-2026-56675

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-287;CWE-290;CWE-306;CWE-441` |
| Published | 2026-07-10T17:17:01.070 |

9Router is an AI router & token saver. Prior to 0.5.2, 9router treats loopback requests as trusted and allows /v1/* access without an API key, so a same-host reverse proxy that forwards public traffic to the backend through 127.0.0.1 causes src/dashboardGuard.js to misclassify external requests as local. A remote unauthenticated attacker can access /v1 APIs such as /v1/models and may abuse configured upstream provider credentials through /v1 proxy endpoints depending on enabled providers. This issue is fixed in version 0.5.2.

### CVE-2026-56254

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-320` |
| Published | 2026-07-10T15:16:41.810 |

In @capgo/capacitor-updater (Cap-go/capgo) before 12.128.2, the end-to-end encryption scheme distributes the private key to each device that downloads the app. Because the public key can be derived from the private key, an attacker performing a man-in-the-middle attack or compromising the Capgo server can create a validly signed update bundle and cause devices to install an update not produced by the original app maker.

### CVE-2026-54736

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-208;CWE-347` |
| Published | 2026-07-10T22:16:42.970 |

Phalcon is a high-performance, full-stack PHP framework. Prior to 5.14.1, Phalcon\Encryption\Crypt::decrypt compares the attacker-supplied HMAC tag against the freshly computed HMAC using PHP/Zephir identity comparison, which lowers to a byte-wise comparison that returns early on the first differing byte. This observable timing discrepancy can allow an attacker to recover a valid tag byte-by-byte and attach it to a chosen IV and ciphertext so that decrypt() accepts tampered encrypted content as authentic. This issue is fixed in version 5.14.1.

### CVE-2026-58499

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-10T21:17:00.197 |

EverOS is a memory runtime for agents. Prior to 1.0.1, EverOS is vulnerable to path traversal in the POST /api/v1/memory/add ingestion endpoint because the per-message sender_id field was not validated as a path-safe identifier, unlike app_id and project_id. During user-memory extraction, sender_id is used as owner_id and joined into the filesystem path where the extracted episode is persisted as a Markdown file, so a sender_id containing ../ sequences could direct writes outside the configured memory root and allow an unauthenticated caller to create or overwrite .md files at locations writable by the server process with partially attacker-influenced content. This issue is fixed in version 1.0.1.

### CVE-2026-55641

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-290;CWE-348;CWE-918;CWE-1327` |
| Published | 2026-07-10T17:16:59.330 |

9Router is an AI router & token saver. Prior to 0.5.2, 9router determines whether a /v1 LLM proxy request is local by reading the client-controlled Host header, allowing a remote unauthenticated attacker to send Host: localhost and bypass API-key authentication. In the default configuration, this exposes the /v1 proxy to upstream provider calls using stored provider credentials and allows /v1/search with the searxng provider_options.baseUrl parameter to drive server-side requests to internal or cloud-metadata hosts. This issue is fixed in version 0.5.2.

### CVE-2026-53657

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-276;CWE-668` |
| Published | 2026-07-10T17:16:57.987 |

Lima launches Linux virtual machines, typically on macOS, for running containerd. Prior to 2.1.3, on an instance of Lima running with the qemu driver, an arbitrary user in the VM could access /run/lima-guestagent.sock when the guest agent is enabled, which could result in running arbitrary commands with root privileges in the VM because the guest agent socket provides tunneling for arbitrary addresses, including Unix socket addresses for privileged daemons like D-Bus. This issue is fixed in version 2.1.3.

### CVE-2026-7655

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-07-11T06:16:10.657 |

The SureCart plugin for WordPress is vulnerable to privilege escalation via account takeover in versions up to, and including, 4.2.3. This is due to the plugin not properly validating a user's identity prior to updating their details like email during customer profile synchronization from webhook events. This makes it possible for unauthenticated attackers to change linked user's email addresses, including administrators if the administrator account is linked to a SureCart customer record, and leverage that to reset the user's password and gain access to their account if the customer ID is known.

### CVE-2026-49213

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-10T22:16:42.270 |

TypeBot is a chatbot builder tool. Prior to 3.17.2, Typebot's shared SSRF validator in packages/lib/src/ssrf/validateHttpReqUrl.ts can be bypassed with the IPv6 unspecified address :: because validateIPAddress blocks local, metadata, and private ranges but does not block :: or its expanded form. A workspace editor or creator can configure a server-side HTTP Request block or guarded script fetch to make the Typebot server connect to local HTTP services through safeKy, including flows triggered by POST /v1/typebots/{publicId}/startChat or POST /v1/sessions/{sessionId}/continueChat. This issue is fixed in version 3.17.2.

### CVE-2026-55377

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-10T20:16:46.460 |

Logto is the modern, open-source auth infrastructure for SaaS and AI apps. Prior to 1.41.0, Logto's Account Center step-up check accepted any active verification record that belonged to the current user and had isVerified === true. A WebAuthn registration verification record for binding a new passkey could be created and verified with only an existing Account API bearer token, then sent in the logto-verification-id header and treated as identityVerified=true by Account Center routes, allowing MFA factor management without proving possession of an existing password, identifier, or MFA factor. This issue is fixed in version 1.41.0.

### CVE-2026-56668

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-10T18:16:24.413 |

ZITADEL is an open source identity management platform. Prior to 4.15.3, ZITADEL's OAuth2 Token Exchange endpoint for urn:ietf:params:oauth:grant-type:token-exchange does not verify that the subject token belongs to the requesting client or that requested scopes remain within the original token's scopes, allowing a low-privilege token to be exchanged for elevated permissions at another application. This issue is fixed in version 4.15.3.

### CVE-2026-59796

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-10T15:16:48.683 |

In JetBrains TeamCity before 2026.1.2 pipeline modification was possible due to improper permission checks

### CVE-2026-59795

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-10T15:16:48.573 |

In JetBrains TeamCity before 2026.1.2 stored XSS via unauthenticated agent registration was possible

### CVE-2026-55659

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-116` |
| Published | 2026-07-10T21:16:56.577 |

Grist is spreadsheet software using Python as its formula language. Prior to 1.7.15, several server-rendered Grist pages embedded user-controlled values into the page and into inline scripts without fully escaping them, allowing cross-site scripting. On the main application page, a document's name or description, set by a document editor, is rendered into the page that other users load when opening the document. On the OAuth2 end-of-flow page, the openerOrigin request parameter was reflected back into the served page. Injected script runs in the victim's Grist origin and can act through the authenticated session, reading or modifying data and changing sharing settings and access rules. A document editor could therefore escalate to owner-level access. This issue is fixed in version 1.7.15.

### CVE-2026-55516

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-10T19:17:25.710 |

Snipe-IT is an IT asset/license management system. Prior to 8.6.2, PATCH or PUT /api/v1/maintenances/{maintenance_id} checks access to the current maintenance record and asset but then fills attacker-controlled fields including asset_id without re-authorizing the newly supplied asset, allowing an authorized user to move a maintenance record onto an asset outside their company scope. This issue is fixed in version 8.6.2.

### CVE-2026-55405

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-10T21:16:55.977 |

LangChain4j is a Java library for building LLM-powered applications on the JVM. Prior to  1.2.1-beta8, 1.5.1-beta11, 1.11.8-beta19, and 1.16.3-beta26, the MariaDB and pgvector embedding stores build metadata-filter SQL by string-concatenating filter keys, and in MariaDB string values, directly into the query without adequate escaping. A crafted metadata key in EmbeddingSearchRequest.filter() can break out of its SQL context and inject arbitrary SQL into the statements executed by the stores' search and removeAll(Filter) operations, enabling blind data exfiltration, denial of service via sleep functions, and deletion of arbitrary rows through removeAll(Filter). This issue is fixed in langchain4j-mariadb and langchain4j-pgvector versions 1.2.1-beta8, 1.5.1-beta11, 1.11.8-beta19, and 1.16.3-beta26.

### CVE-2026-9282

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-11T07:16:47.070 |

The W3 Total Cache plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 2.9.4 via the setupSources function. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. Exploitation requires enabling manual minify mode and supplying a manual-format minify filename so that the hash is empty and the f_array[] entries are not overwritten before reaching setupSources().

### CVE-2026-4661

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-11T07:16:46.513 |

The WP CTA – Sticky CTA Builder, Generate Leads, Promote Sales plugin for WordPress is vulnerable to time-based blind SQL Injection via the 'fildname' parameter in all versions up to, and including, 2.2.2. This is due to insufficient escaping of user-supplied column names in the ajaxCheck() method and lack of preparation in the $wpdb->update() call. The vulnerability is compounded by the complete absence of authorization checks and the endpoint being registered for unauthenticated users via wp_ajax_nopriv_. This makes it possible for unauthenticated attackers to inject arbitrary SQL queries and extract sensitive information from the database via time-based blind SQL injection techniques, including administrator password hashes.

### CVE-2026-15335

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-11T05:16:32.923 |

The Booking Package plugin for WordPress is vulnerable to generic SQL Injection via 'email' Form Parameter (form<N>) in all versions up to, and including, 1.7.20 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. The vulnerable REST API endpoint /wp-json/booking-package/v1/request is registered with permission_callback: __return_true and wp_magic_quotes does not apply to REST-sourced $_POST values, meaning single quotes in the payload reach the SQL sink intact without any authentication requirement. The impact of this is severely limited as the vulnerable parameter goes through is_email.

### CVE-2026-15338

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-11T04:17:22.537 |

The LA-Studio Element Kit for Elementor plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 1.6.1 via the get_type_template function. This makes it possible for authenticated attackers, with contributor-level access and above, to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included. The wp_normalize_path function used in get_template only normalizes directory separators and does not resolve or reject path traversal sequences, while the extension check is trivially bypassed because the caller already appends the required extension to the traversal payload.

### CVE-2026-55175

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-10T23:16:48.487 |

Spinnaker is an open source, multi-cloud continuous delivery platform. Prior to versions 2026.1.1, 2026.0.3, 2025.4.4, and 2025.3.4 on their respective release lines, Kustomize bake operations allow unsafe YAML tag processing in rosco manifests. This can lead to remote code execution on rosco pods when performing Kustomize bakes. This issue is fixed in versions 2026.1.1, 2026.0.3, 2025.4.4, and 2025.3.4.

### CVE-2026-57220

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-10T21:16:59.180 |

RabbitMQ is a messaging and streaming broker. Prior to 4.2.6, the RabbitMQ stream listener does not enforce the configured stream frame-size limit while assembling frames during authentication and before Tune negotiation, allowing an unauthenticated remote client to declare oversized frame lengths and consume broker memory in rabbit_stream_core. This issue is fixed in version 4.2.6.

### CVE-2026-55233

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-10T21:16:55.760 |

OpenResty is a high performance web platform. From 1.29.2.1 to before 1.29.2.5, an out-of-bounds write vulnerability exists in the upstream PROXY protocol v2 implementation. When OpenResty is configured to send PROXY protocol version 2 headers to upstream servers, constructing the header in the stream proxy protocol v2 patch can write beyond the bounds of the allocated buffer, causing the worker process to crash and resulting in a denial of service. Only configurations that explicitly enable PROXY protocol v2 for upstream connections are impacted. This issue is fixed in version 1.29.2.5.

### CVE-2026-55229

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-10T21:16:55.630 |

Gotenberg is a Docker-powered stateless API for PDF files. Prior to 8.34.0, Gotenberg's /forms/libreoffice/convert endpoint allows a specially crafted document to cause LibreOffice to automatically retrieve external HTTP(S) resources and local file resources during document conversion, enabling blind SSRF and limited local file disclosure via linked image resource loading. This issue is fixed in version 8.34.0.

### CVE-2026-55213

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-07-10T21:16:55.497 |

h2o is an HTTP server with support for HTTP/1.x, HTTP/2 and HTTP/3. Prior to commit edd7a120bfc4af11ac0cbebce2a43cc1f93f9af1, when h2o processes a QPACK instruction sent from the peer over HTTP/3, lib/http3/qpack.c might allocate an on-stack buffer as large as approximately 800 KB by calling alloca, which exceeds the default pthread stack size used by musl libc and causes the h2o server to crash with a segmentation fault while touching the guard page. This issue is fixed in commit edd7a120bfc4af11ac0cbebce2a43cc1f93f9af1.

### CVE-2026-55827

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-131;CWE-787` |
| Published | 2026-07-10T20:16:48.060 |

FreeRDP is a free implementation of the Remote Desktop Protocol. Prior to 3.27.1, FreeRDP clients launched with the non-default /cache:codec:rfx option pass desktop stride and height to RemoteFX decoding for Cache Bitmap V3 data while allocating bitmap->data only for the smaller DstWidth and DstHeight in gdi_Bitmap_Decompress, allowing a malicious RDP server to trigger a heap out-of-bounds write with attacker-controlled offset and content. This issue is fixed in version 3.27.1.

### CVE-2026-55687

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121;CWE-787` |
| Published | 2026-07-10T17:16:59.590 |

ESF-IDF is the Espressif Internet of Things (IOT) Development Framework. Versions 6.0.1, 5.5.4, 5.4.4, 5.3.5, and possibly prior contain an out-of-bounds write in jpeg_parse_dqt_marker() in components/esp_driver_jpeg/jpeg_parse_marker.c because the attacker-controlled DQT marker Tq nibble is used as an index into the qt_tbl array without validating that it is in the range 0..3, allowing malformed JPEG input to corrupt stack memory and reliably trigger a denial of service. This issue is fixed in version 6.0.2 and is expected to be fixed in versions 5.5.5, 5.4.5, and 5.3.6.

### CVE-2026-54063

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-10T17:16:58.440 |

Excelize is a Go language library for reading and writing Microsoft Excel spreadsheets. Prior to 2.11.0, the checkSheet() function in github.com/xuri/excelize/v2 uses an attacker-controlled <row r="N"> XML attribute value directly as the length argument to make([]xlsxRow, row) without validating it against the Excel row limit (TotalRows = 1,048,576). A specially crafted XLSX file can trigger two denial-of-service variants: (A) an out-of-memory process kill when r=2147483647 forces a ~16 GB allocation attempt, and (B) a runtime panic via out-of-bounds slice indexing when r=-1. Any service that opens attacker-supplied XLSX files and calls GetCellValue is affected. No authentication is required. This issue is fixed in version 2.11.0.

### CVE-2026-39244

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-10T17:16:57.123 |

adm-zip before 0.5.18 is vulnerable to denial of service via a crafted ZIP file with a manipulated uncompressed size header field. In zipEntry.js line 103, Buffer.alloc(_centralHeader.size) allocates memory based on the declared uncompressed size from the ZIP central directory header without validating it against the actual compressed data size or imposing any upper bound. The size value is read directly from the binary header at entryHeader.js line 266 with no bounds check. An attacker can craft a ~120-byte ZIP file that declares ~4GB uncompressed size, causing a memory allocation amplification ratio of over 33 million to 1. The allocation occurs before CRC validation, so the malicious payload cannot be rejected early. All extraction and read methods are affected: readFile(), readAsText(), extractEntryTo(), extractAllTo(), extractAllToAsync(), test(), and entry.getData(). Any application accepting untrusted ZIP files via adm-zip is vulnerable to immediate process crash.

### CVE-2025-70796

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-10T17:16:52.767 |

An unauthenticated path traversal vulnerability exists in the web management interface of WTI (Wireless Technology, Inc.) version 3.5.0.r 2024/05/24 00:00:00. An unauthenticated attacker can craft malicious HTTP requests containing traversal sequences to access files outside of the intended web root directory. This may allow disclosure of sensitive system files and configuration data

### CVE-2026-33382

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-10T16:16:29.130 |

Several Grafana API endpoints, some of them unauthenticated, do not limit the size of the request body before processing it. An attacker can send very large payloads that force excessive memory allocation, potentially exhausting memory and causing a denial of service.

### CVE-2026-57574

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-07-10T21:16:59.683 |

Misskey is an open source, federated social media platform. Prior to 2026.6.0, Misskey contains a vulnerability in Time-based One-Time Password (TOTP) authentication in UserAuthService where insufficient validation of used tokens allows the reuse of a single-use code within its valid time step. If both credentials and a TOTP code are obtained concurrently, an attacker may reuse the code to perform unauthorized actions, potentially leading to account takeover. This issue is fixed in version 2026.6.0.

### CVE-2026-53450

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-10T19:17:24.193 |

Coturn is a free open source implementation of TURN and STUN Server. Prior to 4.13.0, coturn rejects loopback peers by default unless allow-loopback-peers is enabled, but the default loopback guard can be bypassed by using the IPv4-mapped IPv6 peer address ::ffff:127.0.0.1 in a TURN XOR-PEER-ADDRESS attribute. ioa_addr_is_loopback checks for the literal IPv6 loopback shape before IPv4-mapped IPv6 handling, so good_peer_addr does not apply the default loopback rejection and an authenticated TURN client can expose services bound only to localhost on the coturn host through TURN relay traffic. This issue is fixed in version 4.13.0.

### CVE-2026-55672

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-863` |
| Published | 2026-07-10T18:16:23.637 |

ZITADEL is an open source identity management platform. Prior to 3.4.12 and 4.15.2, ZITADEL's OAuth2 and OIDC CodeExchange, RefreshToken, and device token flows fail to verify that the requesting client matches the client that initiated the authorization flow, allowing intercepted grants or refresh tokens to be exchanged under a different client. This issue is fixed in versions 3.4.12 and 4.15.2.

### CVE-2026-54919

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-07-10T17:16:58.700 |

cpp-httplib is a C++11 single-file header-only cross platform HTTP/HTTPS library. In affected Mbed TLS backend versions from 0.31.0 through 0.46.1 and wolfSSL backend versions from 0.33.0 through 0.46.1, when cpp-httplib is built with CPPHTTPLIB_MBEDTLS_SUPPORT or CPPHTTPLIB_WOLFSSL_SUPPORT and a client connects to an IP-literal host with server certificate verification enabled, SSLClient and Client in HTTPS mode skip certificate chain validation and WebSocketClient on the Mbed TLS backend skips verification altogether, allowing a man-in-the-middle attacker positioned to intercept traffic to present a crafted certificate and read or modify the traffic. This issue is fixed in version 0.47.0.

### CVE-2026-56676

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-367;CWE-918` |
| Published | 2026-07-10T16:16:34.923 |

9Router is an AI router & token saver. Prior to 0.5.2, 9router validates image URLs by resolving the host before fetching, but open-sse/translator/concerns/image.js performs the later server-side image fetch with a separate DNS resolution. An authenticated attacker with access to the LLM proxy can use a vision-capable model and an attacker-controlled DNS name that first resolves to a public IP and then rebinds to an internal address, allowing server-side requests to internal-only HTTP services. This issue is fixed in version 0.5.2.

### CVE-2026-56667

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-10T18:16:24.283 |

ZITADEL is an open source identity management platform. Prior to 4.15.3, ZITADEL Login V2 OIDC and SAML FailedPrecondition error paths return loginSettings.defaultRedirectUri to router.push without applying the isSafeRedirectUri check, allowing an organization or instance administrator to store a javascript or data URI that can execute in a user's browser when an affected login error path is reached. This issue is fixed in version 4.15.3.

### CVE-2026-55501

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-307` |
| Published | 2026-07-10T16:16:33.493 |

9Router is an AI router & token saver. Prior to 0.4.80, the dashboard login rate limiter in src/lib/auth/loginLimiter.js derives the client identity from the attacker-controlled X-Forwarded-For HTTP header, and src/app/api/auth/login/route.js uses that spoofable value for checkLock and recordFail. A remote attacker can rotate the X-Forwarded-For value on each login attempt to receive a fresh rate-limit bucket, bypass the 5-attempt threshold and progressive lockout durations, and perform unlimited brute-force attempts against the dashboard password. This issue is fixed in version 0.4.80.

### CVE-2026-59794

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-10T15:16:48.463 |

In JetBrains TeamCity before 2026.1.2 stored XSS on the cloud profile page was possible via agent-reported data

### CVE-2026-6939

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-11T07:16:46.787 |

The CorvusPay WooCommerce Payment Gateway plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'approval_code' parameter in all versions up to, and including, 2.7.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The unauthenticated REST endpoint POST /wp-json/corvuspay/success/ is registered with permission_callback set to __return_true, and although a signature validation step exists it only logs the result without halting execution, meaning an attacker can supply a completely arbitrary signature and have a malicious approval_code stored in the database unchallenged.

### CVE-2026-13378

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-11T06:16:08.930 |

The Form Vibes – Database Manager for Forms plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Contact Form 7 Form Field in all versions up to, and including, 1.5.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-3576

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-11T05:16:34.013 |

The Planyo Online Reservation System plugin for WordPress is vulnerable to Server-Side Request Forgery leading to Local File Inclusion in all versions up to, and including, 3.0. The ulap.php file acts as an AJAX proxy and is directly accessible without WordPress bootstrapping or any authentication. The send_http_post() function validates the host of the provided URL against an allowlist that includes 'localhost', but critically fails to validate the URL scheme/protocol. This makes it possible for unauthenticated attackers to supply a file:// URL (e.g., file://localhost/etc/passwd) which bypasses the host allowlist check because parse_url() returns 'localhost' as the host. The URL is then passed to curl_init() or fopen(), both of which support the file:// protocol, allowing the attacker to read arbitrary local files on the server and have their contents returned in the HTTP response. This can lead to disclosure of sensitive files such as /etc/passwd, wp-config.php (containing database credentials and authentication keys), and other server-side files.

### CVE-2026-13114

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-11T04:17:16.650 |

The Motors – Car Dealership & Classified Listings Plugin plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content and User Biographical Info in all versions up to, and including, 1.4.112 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-53448

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-10T19:17:23.930 |

Coturn is a free open source implementation of TURN and STUN Server. Prior to 4.12.0, the coturn HTTPS admin panel passes HTTP query parameters directly into SQL queries via snprintf string interpolation without sanitization. The is_secure_string filter that protects the STUN protocol path is not applied to the admin panel's delete-user, delete-secret, and delete-IP operations, so an authenticated admin can inject arbitrary SQL through the du, ds, and dip parameters, gaining full database control and potentially OS-level access via PostgreSQL COPY TO PROGRAM. This issue is fixed in version 4.12.0.

### CVE-2026-1667

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-10T17:16:54.597 |

The SEO Plugin by Squirrly SEO plugin for WordPress is vulnerable to Arbitrary Post Creation and Stored Cross-Site Scripting in all versions up to, and including, 14.0.0 due to a leak of an API token and insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to create arbitrary posts, and, if the Advanced Custom Fields plugin is installed and activated, inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-61442

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-11T14:16:23.017 |

PraisonAI Platform (praisonai-platform) before 0.1.9 fails to enforce owner/admin authorization on the PATCH routes for projects, issues, and agents, which only require workspace-member role. A workspace member can modify owner-created records; for projects, a member can reassign lead_id to their own user id and then delete the owner-created project, bypassing the delete route's owner/admin permission check.

### CVE-2026-49394

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-10T22:16:42.410 |

Frappe is a full-stack web application framework. Prior to 16.19.0, authorization bypass was possible via the update_page endpoint in Workspace because public workspaces did not receive the required Workspace Manager edit check. This issue is fixed in version 16.19.0.

### CVE-2026-41482

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-10T22:16:41.337 |

Frappe is a full-stack web application framework. Prior to 16.18.3, possible path traversal and local file inclusion were possible through secure local resource access in the Chrome PDF Generator. This issue is fixed in version 16.18.3.

### CVE-2026-57214

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-10T21:16:58.423 |

RabbitMQ is a messaging and streaming broker. Prior to 4.2.5, the RabbitMQ management UI renders the x-internal-purpose queue or exchange argument into an HTML title attribute without proper escaping on the Queues and Exchanges pages, allowing a user with permission to declare a queue or exchange to execute JavaScript in another user's browser. This issue is fixed in version 4.2.5.

### CVE-2026-57212

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-10T21:16:58.150 |

RabbitMQ is a messaging and streaming broker. Prior to 3.13.14, 4.0.19, 4.1.10, and 4.2.5, the rabbitmq_management HTTP API accepts oversized valid JSON bodies on with_decode and direct_request paths because read_complete_body checks the accumulated size before the final chunk but not the final combined size. This issue is fixed in versions 3.13.14, 4.0.19, 4.1.10, and 4.2.5.

### CVE-2026-55881

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-10T21:16:57.653 |

OpenReplay is a self-hosted session replay suite. From 1.22.0 before 1.27.0, getFirstMob returned 15-second presigned S3 download URLs for a session's DOM-replay recording based solely on the session path parameter, while validateProjectAccess checked only that the project belonged to the requester's tenant and did not verify that the session belonged to that project, allowing any authenticated low-privilege user to read another tenant's first 15 seconds of session-replay recording data. This issue is fixed in version 1.27.0.

### CVE-2026-55880

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-10T21:16:57.493 |

OpenReplay is a self-hosted session replay suite. In 1.27.0 and earlier, three dashboard and note mutation functions ran their SQL without the ownership predicate that their sibling read and edit functions use: notes.delete filtered only on note id and project id, while dashboards.update_widget and dashboards.remove_widget filtered only on dashboard id and widget id, allowing any authenticated member to delete another user's private session notes and remove or rewrite widgets on another user's private dashboards.

### CVE-2026-11321

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-10T20:16:45.453 |

The DataInjection plugin for GLPI 2.15.6 (GLPI 11 builds) concatenates user-supplied CSV field values directly into SQL queries during CSV import, without parameterization or escaping, resulting in authenticated SQL injection. An authenticated user with access to the Data injection feature can embed SQL expressions such as SLEEP() in a mapped field (for example Serial Number) to manipulate the generated query and extract database information via time-based blind injection.

### CVE-2026-55474

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-07-10T19:17:25.080 |

Snipe-IT is an IT asset/license management system. Prior to 8.5.0, ActionlogController::displaySig concatenates the route filename parameter into a private upload-directory path without sanitization, allowing an authenticated attacker to traverse outside the intended directory and read arbitrary files accessible to the web server process. This issue is fixed in version 8.5.0.

### CVE-2026-55460

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-10T19:17:24.667 |

Snipe-IT is an IT asset/license management system. Prior to 8.6.2, an authenticated non-admin user with users.view and users.edit but without users.delete can directly POST to /users/bulksave with delete_user=1 because BulkUsersController::destroy() authorizes only update, allowing the user to soft-delete another non-admin user. This issue is fixed in version 8.6.2.

### CVE-2026-39903

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-10T17:16:57.230 |

Simple Machines Forum 2.1 prior to 2.1.8 and 3.0 prior to 3.0 Alpha 5 contains an authorization bypass vulnerability in Sources/Actions/AttachmentApprove.php where a single-character operator error causes the permission check to always pass regardless of user permissions. An authenticated low-privileged user can approve, reject, or delete any pending attachments on any board without holding the required approve_posts permission, bypass moderation queues for their own uploads, and enumerate and delete other users' pending attachments.

### CVE-2026-61455

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-07-10T15:16:50.877 |

Grav before 2.0.1 contains a decompression bomb vulnerability in ZipArchiver::extract() that lacks limits on uncompressed size, file count, and nesting depth. Attackers can supply a crafted ZIP archive that expands to fill available disk space, causing denial of service by exhausting storage resources.

### CVE-2026-61450

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-10T15:16:50.740 |

Grav before 2.0.2 contains a Twig sandbox bypass that allows a page author (any admin.pages user, or anyone able to write to user/pages) to exfiltrate configuration secrets. Although the sandbox replaces the 'config' variable with a redacted facade and strips Config::get/toArray from the method allowlist, the raw container remains accessible via the allow-listed grav.offsetGet('config'), which returns the real Config object. Allow-listed object-dumping filters (json_encode, print_r, yaml_encode) then serialize that object at the PHP level without invoking the sandbox method gate, exposing the full config tree including plugin secrets such as SMTP credentials, API keys, and plugin DB credentials. This is an incomplete fix for GHSA-j274-39qw-32c9.

### CVE-2026-61441

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-10T15:16:50.480 |

PraisonAI Platform (praisonai-platform) before 0.1.9 improperly authorizes deletion of issue dependencies. The DELETE dependency route accepts either endpoint of a dependency edge and checks delete permission only against the caller-selected URL issue. A workspace member who cannot delete a dependency through an owner-created issue endpoint (which returns 403) can delete the same dependency edge by targeting a related member-owned issue endpoint, because permission is validated against the member-owned issue's owner. This allows members to bypass owner/admin authorization and remove owner-created issue dependencies.

### CVE-2026-56335

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-10T15:16:42.880 |

Capgo before 12.128.2 contains an authorization bypass vulnerability where write-scoped API keys can directly mutate protected channel configuration fields through PostgREST by exploiting a null authentication check in the immutability trigger. Attackers with write API keys can modify sensitive channel attributes such as public, allow_emulator, and security-related flags outside intended application routes.

### CVE-2026-57217

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-10T21:16:58.810 |

RabbitMQ is a messaging and streaming broker. Prior to 3.13.15, 4.0.21, 4.1.11, and 4.2.6, RabbitMQ topic authorization can allow restricted topic writes and binds during metadata-store failures because topic-permission lookup errors from Khepri can collapse to undefined, which the internal backend treats as allow. This issue is fixed in versions 3.13.15, 4.0.21, 4.1.11, and 4.2.6.

### CVE-2026-57215

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-10T21:16:58.550 |

RabbitMQ is a messaging and streaming broker. Prior to 3.13.15, 4.0.20, 4.1.11, and 4.2.6, RabbitMQ allows foreign bindings to amq.rabbitmq.reply-to destinations because volatile direct-reply-to queues can be accepted at bind and route time but are missing from Khepri-backed deletion checks, leaving persistent route entries after unbind. This issue is fixed in versions 3.13.15, 4.0.20, 4.1.11, and 4.2.6.

### CVE-2026-55843

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-10T19:17:26.250 |

Snipe-IT is an IT asset/license management system. Prior to 8.6.0, UsersController::update() passes a missing permission request field through NormalizePermissionsPayloadAction and PreserveUnauthorizedPrivilegedPermissionsAction in a way that can overwrite a target user’s permissions with a sparse result, allowing an administrator updating another administrator, or a user with users.edit updating a regular account, to remove the target’s administrative or granular permissions. This issue is fixed in version 8.6.0.

### CVE-2026-54001

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-10T16:16:32.467 |

osquery is a SQL powered operating system instrumentation, monitoring, and analytics framework. Prior to 5.23.1, on Windows, a local unprivileged attacker can cause a heap buffer out-of-bounds write if there is a query of the authenticode table targeting a maliciously crafted binary, due to publisher information parsing in getOriginalProgramName. If exploited successfully, this could allow a potential local privilege escalation from standard user to SYSTEM. This issue is fixed in version 5.23.1.

### CVE-2026-54000

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-10T16:16:32.340 |

osquery is a SQL powered operating system instrumentation, monitoring, and analytics framework. Prior to 5.23.1, on Windows, a local unprivileged attacker can cause a heap buffer out-of-bounds write if there is a query of the processes table targeting a maliciously crafted process, due to unchecked PEB string lengths in process command-line and current-directory reads. If exploited successfully, this could allow a potential local privilege escalation from standard user to SYSTEM. This issue is fixed in version 5.23.1.

### CVE-2026-38057

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-10T15:16:39.397 |

The iDirect iQ200 does not validate CSRF tokens on state-changing API endpoints after authentication. The /api/reboot endpoint accepts POST requests authenticated solely by a session cookie that lacks the SameSite attribute. A remote attacker can host a malicious web page that, when visited by an authenticated administrator, automatically submits a cross-site POST request causing an immediate device reboot and satellite link loss. Repeated attacks can sustain a denial-of-service condition.
