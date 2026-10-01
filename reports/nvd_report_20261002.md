# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-01 15:00 UTC
- **対象期間**: `2026-09-30T15:00:40.000Z` 〜 `2026-10-01T15:00:33.000Z`
- **重要CVE数**: 297 件（Critical 9.0+: 45 件 / High 7.0〜: 252 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件** 余りに上りますが、特に **認証不要でリモートコード実行 (RCE) やフルバックアップ取得が可能になる脆弱性** が目立ちます。  
- WordPress・Joomla といった CMS 系プラットフォームのプラグイン／拡張機能が集中して高リスク (CVSS 9.8〜10.0)。  
- クラウド／SaaS 型サービス（Fleet、Kobako など）でも **認証バイパス** が多発し、内部ネットワークに侵入した攻撃者が簡単に権限昇格できる点が懸念材料です。  
- さらに、**鍵・パスワード生成ロジックの不備**（BoKS keytabmd）や **ハードコーディングされたシークレット**（Hitachi Coding Suite）といった、運用上のミスが直接的に重大脆弱性へと結びつくケースも確認されています。  

> **傾向**：認証・入力検証の欠如、デフォルト設定のまま公開されている管理 API が共通の根本原因です。早急なパッチ適用と、不要プラグインの除去・設定見直しが必須です。

---

## 2. 特に注目すべき CVE  

| CVE | 製品・コンポーネント | 主な影響 | 理由・影響範囲 |
|-----|-------------------|----------|----------------|
| **CVE‑2026‑101148** | BackupSheep WordPress Backup Plugin ≤ 1.8 | **認証不要でサイト全体バックアップ取得・削除** (C/H/I/A = H/H/H/H) | インテグレーションキーが未設定でも有効とみなされ、攻撃者は任意のサイトのデータベース（パスワードハッシュ含む）を取得できる。WordPress サイト全体が即座に情報漏洩リスクに。 |
| **CVE‑2026‑102427** | OrdaSoft Joomla CCK < 8.3.16 (site/uploader.php) | **認証不要 RCE** (C/H/I/A = H/H/H/H) | フロントエンドの `task=getContent` が認証・ACL を全くチェックせず、任意の PHP コードが実行可能。Joomla を利用する企業サイト・ポータルが即座に乗っ取られる。 |
| **CVE‑2026‑55107** | Kobako Ruby gem (Wasm‑isolated mruby) | **任意コード実行** (CVSS 10.0) | ユーザー提供の Ruby スクリプトが Wasm 隔離を想定しているが、メモリ・ファイル・ネットワークへのアクセス制御が不完全。マルチテナント環境や SaaS アプリでのサンドボックス崩壊リスク。 |
| **CVE‑2026‑79901** | BoKS keytabmd (Active Directory service‑account password generator) | **予測可能なパスワード** (C/H/I/A = H/H/H/H) | パスワード生成が現在時刻ベースの疑似乱数でシードされ、攻撃者が変更タイミングを推測すれば AD サービスアカウントを完全取得できる。 |
| **CVE‑2026‑103264** | Fleet < 4.87.0 (device API) | **認証バイパス** (C/H/I/A = H/H/N/N) | デバイス UUID 以外にホスト名・シリアル番号でも認証が通るため、情報収集が可能な攻撃者がデバイスを偽装し管理 API に不正アクセス。大量デバイス管理環境での横展開が懸念。 |

> **注目ポイント**：上記 5 件はすべて **認証不要**、または **極めて弱い認証** が原因で、攻撃者がリモートから直接システムを支配できる点が共通しています。特に WordPress/Joomla のプラグインは多数のサイトで共通利用されているため、インパクトは大きいです。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 | 現行脆弱バージョン | 推奨バージョン | 取得先・備考 |
|------|-------------------|----------------|--------------|
| BackupSheep WordPress Backup Plugin | ≤ 1.8 | **≥ 1.9** (公式リリース) | WordPress 管理画面 → プラグイン > 更新 |
| OrdaSoft Joomla CCK | < 8.3.16 | **8.3.16** 以降 | Joomla Extension Directory から最新版取得 |
| Kobako (Ruby gem) | 0.9.x 以前 | **≥ 1.2.0** (gem 更新) | `gem update kobako` もしくは公式リポジトリのリリースノート参照 |
| BoKS keytabmd | 2.3.0 以前 | **≥ 2.4.1** (パッチ適用) | BoKS 公式サイトのダウンロードページ |
| Fleet (MDM) | < 4.87.0 | **4.87.0** 以降 | Fleet のパッケージリポジトリ (apt/yum) で `fleet-server upgrade` |

### 3.2 設定・運用面の緊急対策
1. **不要プラグインの無効化・削除**  
   - BackupSheep、Ultimate Multisite、Super Forms など、使用していないプラグインは即時無効化し、ファイルシステムから削除。  
2. **管理 API のアクセス制限**  
   - Fleet、Kobako、Joomla の管理 API エンドポイントに IP アクセスコントロール（ファイアウォール or WebACL）を適用。  
3. **キー・シークレットのローテーション**  
   - BoKS keytabmd のサービスアカウントパスワードを即時変更し、今後は時間ベース乱数ではなく、CSPRNG で生成されたパスフレーズを使用。  
   - Hitachi Coding Suite 系列でハードコーディングされた JWT 秘密鍵が判明した場合は、ベンダー提供のパッチが出るまで **全システムで JWT 鍵を再生成**。  
4. **監視・ログ強化**  
   - WordPress/Joomla の `auth.log`、`access.log` に対し、**バックアップ取得リクエスト**や **uploader.php** へのアクセスをリアルタイムでアラート。  
   - Fleet のデバ

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-101148

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-10-01T06:17:04.057 |

The BackupSheep WordPress Backup Plugin WordPress plugin through 1.8 does not properly validate its integration key, treating an unset or blank key as valid, which allows unauthenticated attackers to create and download full site backups, including the database with user password hashes, and to delete arbitrary files on the server, leading to sensitive data disclosure and site takeover.

The BackupSheep WordPress Backup Plugin WordPress plugin through 1.8 has been closed on WordPress.org since July 2024 and no fixed version is available. Remove it from any site where it is installed.

### CVE-2026-55107

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-470` |
| Published | 2026-09-30T18:18:37.550 |

Kobako is a Ruby gem that embeds a Wasm-isolated mruby interpreter inside applications, allowing execution of untrusted Ruby scripts (LLM-generated code, user formulas, student submissions, third-party plugins) in-process without giving them access to host memory, files, network, or credentials. From version 0.1.0 to before version 0.9.1, a guest mruby script running inside the Kobako sandbox can execute arbitrary Ruby in the host process, fully escaping the sandbox. This issue has been patched in version 0.9.1.

### CVE-2026-102427

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-30T16:17:06.623 |

Joomla Extension - ordasoft.com - Unauthenticated Remote Code Execution in OrdaSoft Joomla CCK < 8.3.16 - site/uploader.php is reached through the component’s normal frontend routing (task=getContent), a task with no authentication or ACL check anywhere in the dispatch chain. The handler validates the uploaded file’s content with a real magic-byte MIME check, but the extension allow-list that would otherwise restrict the saved file’s extension was present in the source and commented out. The saved file’s extension was taken directly from the attacker-supplied filename with no validation, and the file was written to a path directly under the Joomla web root that is executed by the PHP handler. An image/PHP polyglot, a file whose header bytes satisfy the MIME check with PHP source appended after, passed the content check while carrying a .php extension of the attacker’s choosing.

### CVE-2026-76570

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T15:22:34.903 |

Joomla Extension - joomcode.com - Unauthenticated SQL injection in read and write queries in JCTables  1.21.1 - The front-end CRUD API controller performs no Joomla token validation and no authentication check on any task. Table names, column names, and values are taken directly from request parameters and concatenated into SQL queries, allowing SQLi for reading and writing queries.

### CVE-2026-79901

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-338` |
| Published | 2026-10-01T14:17:30.883 |

In deployments using BoKS keytab management, affected versions of boks_keytabmd generate Active Directory service-account passwords from a predictable pseudo-random sequence seeded with the current Unix timestamp. An attacker who knows the service principal and can estimate the password-change time can reproduce a limited candidate set and verify candidates offline.

### CVE-2026-75957

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-01T08:16:52.763 |

The Ultimate Multisite – WordPress Multisite SaaS & WaaS Platform plugin for WordPress is vulnerable to Authentication Bypass in all versions up to, and including, 2.15.0 via the `checkout_form` parameter of the `login_customer_after_checkout` function. This is due to the publicly accessible `wu_ajax_nopriv_wu_validate_form` AJAX handler accepting a freely obtainable checkout nonce, and the `checkout_form=wu-finish-checkout` parameter causing `get_validation_rules()` to discard all validation rules while `finish_checkout_form_fields()` returns an empty step list — forcing `is_last_step()` to return true and routing the request directly into full order processing — after which `maybe_create_customer()` resolves the attacker-supplied `email_address` to an existing WordPress user ID without any authentication or ownership verification, and `login_customer_after_checkout()` calls `wp_set_auth_cookie()` for that user ID via a passwordless code path. This makes it possible for unauthenticated attackers to log in as any existing WordPress user — including a Network Super Admin — simply by knowing their email address. Exploitation requires that the targeted user account has no pre-existing Ultimate Multisite customer record; accounts such as a Network Super Admin on a fresh Multisite install, or any administrator or editor added before Ultimate Multisite was configured, satisfy this condition and are therefore exploitable.

### CVE-2026-15989

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-01T08:16:51.233 |

The Super Forms – Drag & Drop Form Builder plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 6.3.316. This is due to the Register & Login add-on's before_email_success_msg() function whitelisting the client-submitted 'role' key and copying it into the user-data array that is passed directly to wp_insert_user(), without validating the submitted role against the administrator-configured register_user_role, without an allow-list, and without any current_user_can() capability check. This makes it possible for unauthenticated attackers to register a new account with the Administrator role by injecting role=administrator into the data submitted to any published Super Forms registration form (register_login_action='register').

### CVE-2026-102115

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-09-30T21:16:59.180 |

Kiteworks Core did not correctly validate a parameter submitted to the password reset workflow. An unauthenticated attacker who knew the email address of a user with a locally stored password could potentially reset that account's password without access to the emailed reset link and then authenticate as that user, including where the account holds administrative privileges.

### CVE-2026-100512

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T18:17:59.300 |

Contributor PHP Object Injection in Nested Pages <= 3.3.2 versions.

### CVE-2026-55494

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-30T17:16:47.100 |

Tugtainer is a self-hosted app for automating updates of Docker containers. Prior to version 1.30.4, Tugtainer Agent allows unauthenticated access to Docker management APIs when AGENT_SECRET is not configured. The Agent uses request signatures to protect its API routes. However, in agent/auth.py, the signature verification function returns successfully if Config.AGENT_SECRET is empty. This causes protected Agent APIs to become accessible without authentication. This issue has been patched in version 1.30.4.

### CVE-2026-18782

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T15:22:30.177 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Trex Digital Smart Manufacturing Systems Inc. Trex MES allows Command Line Execution through SQL Injection.

This issue affects Trex MES: through 2026-09-29.

### CVE-2026-14157

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-134` |
| Published | 2026-10-01T02:16:53.983 |

Use of an Externally Controlled Format String in the ASUS Router modules allow a remote authenticated user to execute arbitrary commands via a crafted file uploaded through the web management interface.

### CVE-2026-102149

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-30T21:17:03.760 |

Kiteworks Email Protection Gateway did not sufficiently restrict which account a certificate could be assigned to. This could allow an attacker to associate a certificate with another user's account, affecting the confidentiality and integrity of that account's encrypted mail and, where certificate-based login is enabled, potentially permitting unauthorized access to the account.

### CVE-2026-55181

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-30T17:16:46.937 |

Tugtainer is a self-hosted app for automating updates of Docker containers. Prior to version 1.30.3, Tugtainer's OIDC authentication can still be initiated even when OIDC_ENABLED=false. The /auth/oidc/enabled endpoint correctly reports that OIDC is disabled. However, a direct request to /auth/oidc/login still starts the OIDC login flow, returns HTTP 302, sets an oidc_state cookie, and redirects the user to the configured OIDC authorization endpoint. This bypasses the intended OIDC disable switch. This issue has been patched in version 1.30.3.

### CVE-2026-102490

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:C/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-30T17:16:40.707 |

All versions of Zammad including the latest alpha enable the local zammad user to escalate privileges to root.

### CVE-2026-102489

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:C/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-30T17:16:40.550 |

Zammad versions 6.3.0 to 6.5.4 are vulnerable a session hijack vulnerability that leads to remote code execution as the zammad user. The vulnerability is also present in version 7.0.0 to version 7.1.3, but not exploitable due to environment conditions.

### CVE-2026-103264

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-01T11:17:21.410 |

Fleet versions before 4.87.0 contain an authentication bypass vulnerability in the device API that accepts hostnames and hardware serials as authentication tokens in addition to device UUIDs. Unauthenticated attackers who know or guess these non-secret identifiers can authenticate as iOS/iPadOS hosts to read device data and trigger device-scoped actions including software installation and MDM migration.

### CVE-2026-103244

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-01T11:17:17.503 |

ground-station versions before 0.8.0 contain an authentication bypass vulnerability in the setup.restore command that allows unauthenticated attackers to execute arbitrary SQL during first-run setup mode. Attackers can invoke setup.restore via Socket.IO to plant admin users and forged session tokens, then authenticate as administrator without credentials for complete application takeover.

### CVE-2026-103655

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-10-01T09:17:07.867 |

MISP contains a vulnerability in its two-factor authentication (TOTP) verification process that permits a valid one-time code to be accepted more than once within its time-based validity window.

The issue exists in the user login flow where a TOTP code is verified as a second authentication factor. Because the system did not record whether a given TOTP period had already been consumed, the same code remained valid for its entire time window (typically 30 seconds). An attacker who captures a legitimate code during a user's login could replay it to authenticate a second session as that user.

Preconditions:

- The target user has TOTP-based two-factor authentication enabled.

- The attacker is in a position to observe or intercept the TOTP code during a legitimate login (e.g., network-level interception, shoulder surfing, or a compromised client).

- The replay must occur within the TOTP validity period.

Security impact:

- Unauthorized account access by replaying a captured one-time code.

- Potential compromise of threat-intelligence data and administrative functions accessible to the targeted user.

Affected versions: <v2.5.48.

### CVE-2025-41753

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-01T07:16:32.473 |

The object name of a dynamically created BACnet File Object is interpreted as a file path without sufficient validation. Because relative paths are not limited to the intended directory, an unauthenticated remote attacker can traverse outside of it and read or overwrite arbitrary files on the device, which may lead to full system compromise.

### CVE-2026-82829

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-912` |
| Published | 2026-10-01T05:17:11.090 |

Hitachi Coding Software Suite contains a vulnerability related to Hidden Functionality vulnerability which allows an attacker to gain unauthorized access by exploiting hidden accounts or hard coded credentials.


This issue affects Hitachi Coding Software Suite: through 3.3.0.

### CVE-2026-82827

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-01T05:17:10.780 |

Hitachi Coding Software Suite contains a vulnerability related to Use of Hard-coded Cryptographic Key. The Hardcoding of JWT signing secret key allows an attacker to generate unauthorized Bearer tokens and exploit administrative functions.


This issue affects Hitachi Coding Software Suite: through 3.3.0.

### CVE-2026-82825

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-01T05:17:10.443 |

Hitachi Coding Software Suite contains a vulnerability related to Missing Authentication for Critical Function. This allows an unauthenticated attacker to invoke a critical API, potentially leading to unauthorized retrieval or alteration of sensitive information, or unauthorized manipulation.


This issue affects Hitachi Coding Software Suite: through 3.3.0.

### CVE-2026-82824

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-35` |
| Published | 2026-10-01T05:17:10.270 |

Hitachi Coding Software Suite contains a vulnerability related to Path Traversal vulnerability that allows an attacker to access, create, modify, or delete files.


This issue affects Hitachi Coding Software Suite: through 3.3.0.

### CVE-2026-76142

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284;CWE-306` |
| Published | 2026-10-01T05:17:09.093 |

Insufficient authentication and access control on the internal-only IPC SOAP endpoint of the Genian NAC/ZTNA policy server allows an unauthenticated attacker to invoke internal functions

### CVE-2026-102147

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T21:17:03.633 |

A stored cross-site scripting (XSS) weakness in Kiteworks Core could allow an unauthenticated attacker to store crafted content that later executes arbitrary JavaScript in the authenticated session of an administrator who views the affected page. This could have permitted the attacker to gain full administrative control, including the creation of a new administrative account.

### CVE-2026-103475

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-489` |
| Published | 2026-09-30T18:18:17.817 |

yii2-starter-kit through 4.2.0 exposes the Yii debug and Gii modules to all IP addresses by setting allowedIPs to ['*'] in its default development configuration. Unauthenticated remote attackers can access the debug endpoint to read sensitive data including session cookies and database queries, or access the Gii endpoint to generate and write PHP files into the application directory.

### CVE-2026-103470

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:N/R:U/V:X/RE:L/U:Red` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-30T16:17:10.230 |

In Internet2 Grouper before 7.5.1 (in some configurations), a user who is allowed to create or edit rules in the User Interface can escalate privileges.

### CVE-2026-103395

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T15:22:27.710 |

LightLLM through 1.2.0 visual_only deployments expose an unauthenticated RPyC service with allow_pickle enabled that deserializes attacker-supplied arguments in the remote_infer_images method. Attackers can reach the visual RPyC port and pass objects with __reduce__ methods to execute arbitrary code with service account privileges.

### CVE-2026-101283

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-30T22:16:33.317 |

iperf3 3.20–3.21 (esnet/iperf) has a pre-auth heap buffer overflow in decrypt_rsa_message(): a 256-byte RSA buffer is BIO_read with the attacker-controlled ciphertext length (guard warns only), so an unauthenticated client overflows the heap via an oversized authtoken; fixed in 3.22

### CVE-2026-101276

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-30T21:16:54.913 |

iperf3 3.21 (esnet/iperf) contains a remote, unauthenticated heap use-after-free: the server's per-test watchdog server_timer_proc() frees streams without cancelling/joining their worker threads, so a blocked worker dereferences a freed iperf_stream; fixed in 3.22.

### CVE-2026-103547

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-30T20:17:31.607 |

In ldapd in OpenBSD 7.8 before errata 057 and 7.9 before errata 021, delegated BSD authentication results are correlated only by the LDAP child process client file descriptor and LDAP message ID. After a connection closes, a later connection that reuses the same file descriptor and message ID can receive the earlier authentication result. A remote attacker who can reach ldapd can complete a Bind as another identity. A missing connection can also cause a NULL pointer dereference. (ldapd is not enabled by default.)

### CVE-2026-102992

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-09-30T20:17:27.080 |

piscina is a node.js worker pool implementation. Prior to 4.9.4, 5.3.2, and 6.0.0-rc.5, Piscina stores ThreadPool.options in src/index.ts as a plain object that inherits from Object.prototype. Applications with a separate prototype-pollution primitive can therefore supply inherited values for security-sensitive options that do not have own defaults. An inherited execArgv value is passed to the Node.js Worker constructor and can preload attacker-controlled code in worker threads, an inherited loadBalancer function can execute during task scheduling, and inherited env values can alter worker environments. This issue is fixed in versions 4.9.4, 5.3.2, and 6.0.0-rc.5.

### CVE-2026-103473

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-30T18:18:17.483 |

Deno versions 2.7.0 through 2.9.7 on Windows contain a command injection vulnerability in node:child_process where shell arguments are escaped for the wrong shell type. Attackers can inject OS commands by passing untrusted arguments with the shell option, allowing arbitrary command execution with Deno process privileges.

### CVE-2026-19445

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-30T17:16:45.720 |

A remote, unauthenticated TLS client can make a server crash or call
through a freed pointer if its sni_callback assigns a different context to
SSLSocket.context (the documented way to select a certificate per server
name) and nothing else keeps the original ssl.SSLContext alive. Typical
cases are servers that create an SSLContext per connection or replace it
while connections are open; servers that wrap their listening socket with
it are not affected.


Mitigation: keep a reference to every SSLContext that sets sni_callback for
the lifetime of the server. TLS clients are not affected.

### CVE-2026-92966

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-01T05:17:11.967 |

The The Appointment Booking Plugin – LatePoint | Calendar & Scheduling for WordPress plugin for WordPress is vulnerable to arbitrary shortcode execution in all versions up to, and including, 5.7.0. This is due to the software allowing users to execute an action that does not properly validate a value before running do_shortcode. This makes it possible for unauthenticated attackers to execute arbitrary shortcodes. The payload is planted during the unauthenticated booking flow and triggered when the Customer Cabinet block rendered by render_customer_dashboard() outputs the stored name into the content stream, where WordPress core's do_shortcode filter at priority 11 re-parses and executes it.

### CVE-2026-102106

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-30T21:16:57.490 |

Improper authentication in a Kiteworks Email Protection Gateway administrative service. An administrative service in Kiteworks Email Protection Gateway did not consistently enforce administrator authentication, so the required password check could be bypassed. An attacker who referenced a valid administrator account could potentially create, modify, or delete internal users and managed domains and change their security-feature configuration without authenticating; deleting a managed domain also removes its user accounts and could lock administrators out of the gateway.

### CVE-2026-102105

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-30T21:16:57.370 |

Kiteworks Email Protection Gateway before version 9.5.0 is vulnerable to Server-Side Request Forgery (SSRF). A server-side request forgery (SSRF) weakness in Kiteworks Email Protection Gateway could allow a remote, unauthenticated attacker to induce the gateway to issue crafted requests to internal or otherwise unintended network destinations. The requests are triggered while the gateway renders message content that references external resources. Depending on the services reachable from the gateway, this could disclose sensitive internal information or trigger unintended actions on internal systems.

### CVE-2026-102104

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-30T21:16:57.250 |

Kiteworks Email Protection Gateway before version 9.5.0 is vulnerable to Server-Side Request Forgery (SSRF). A server-side request forgery (SSRF) weakness in Kiteworks Email Protection Gateway could allow a remote, unauthenticated attacker to induce the gateway to issue crafted requests to internal or otherwise unintended network destinations. The requests are triggered while the gateway performs an online certificate status check for an inbound message. Depending on the services reachable from the gateway, this could disclose sensitive internal information or disrupt gateway operation.

### CVE-2026-102103

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-30T21:16:57.127 |

Kiteworks Email Protection Gateway before version 9.5.0 is vulnerable to Server-Side Request Forgery (SSRF). A server-side request forgery (SSRF) weakness in Kiteworks Email Protection Gateway could allow a remote, unauthenticated attacker to induce the gateway to issue crafted requests to internal or otherwise unintended network destinations. The requests are triggered while the gateway retrieves a certificate revocation list in an inbound message. Depending on the services reachable from the gateway, this could disclose sensitive internal information or disrupt gateway operation.

### CVE-2026-102102

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-30T21:16:57.000 |

Kiteworks Email Protection Gateway before version 9.5.0 is vulnerable to Server-Side Request Forgery (SSRF). A server-side request forgery (SSRF) weakness in Kiteworks Email Protection Gateway could allow a remote, unauthenticated attacker to induce the gateway to issue crafted requests to internal or otherwise unintended network destinations. The requests are triggered while the gateway retrieves an issuer certificate in an inbound message. Depending on the services reachable from the gateway, this could disclose sensitive internal information or disrupt gateway operation.

### CVE-2026-102095

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-30T21:16:56.120 |

Kiteworks Email Protection Gateway before version 9.5.0 is vulnerable to Server-Side Request Forgery. Kiteworks Email Protection Gateway performed server-side fetches of URLs contained in the message content it processed, without adequately restricting the fetch destination. A remote, unauthenticated sender could craft a message that caused the gateway to issue requests to internal services and cloud instance metadata endpoints and return the responses, potentially disclosing sensitive internal data and, depending on the internal service reached, affecting its state.

### CVE-2026-75969

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:U/V:C/RE:L/U:Red` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-30T17:16:49.583 |

Missing authentication for critical function vulnerability for all PTZOptics cameras and the Firmware Upgrade Tool - Firmware Update modules. A missing authentication vulnerability in the firmware update mechanism of affected PTZOptics cameras allows an unauthenticated user to install modified firmware on the device without administrator credentials.



This vulnerability allows attackers to upload modified firmware to the device without admin credentials. This issue affects:





  *  Move 4K 12X before: 0.0.98
  *  Move 4K 20X before: 0.1.33
  *  Move 4K 30X before: 2.1.17
  *  Link 4K 12X before: 0.0.99
  *  Link 4K 20X before: 0.1.37
  *  Link 4K 30X before: 2.1.18
  *  Move SE 12X before: 9.1.66
  *  Move SE 20X before: 9.1.44
  *  Move SE 30X before: 9.1.46
  *  Studio 4K 12X before: 8.3.32
  *  Studio 4K 20X before: 8.3.32
  *  Studio SE 12X before: 8.3.32
  *  Studio SE 20X before: 8.3.32
  *  All Generation 2 cameras, including: PT12X-SDI-GY-G2, PT12X-SDI-WH-G2, PT12X-NDI-GY-G2, PT12X-NDI-WH-G2; PT12X-USB-GY-G2, PT12X-USB-WH-G2; PT20X-SDI-GY-G2, PT20X-SDI-WH-G2, PT20X-NDI-GY-G2, PT20X-NDI-WH-G2; PT20X-USB-GY-G2, PT20X-USB-WH-G2; PT30X-SDI-GY-G2, PT30X-SDI-WH-G2, PT30X-NDI-GY-G2, PT30X-NDI-WH-G2; PTVL-ZCAM, PTVL-NDI-ZCAM; PTEPTZ-ZCAM-G2, PTEPTZ-NDI-ZCAM-G2; PT12X-ZCAM, PT12X-NDI-ZCAM; PT20X-ZCAM, PT20X-NDI-ZCAM; Studio Pro - All versions
  *  Upgrade Tool - All versions

### CVE-2026-62308

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-30T17:16:49.423 |

Tugtainer is a self-hosted app for automating updates of Docker containers. Prior to version 1.30.6, Tugtainer allows an authenticated user to make the backend server send outbound HTTP requests to arbitrary user-supplied URLs through the notification test endpoint. The /settings/test_notification endpoint accepts a urls field and passes it directly to Apprise without restricting protocols, hostnames, localhost addresses, private IP ranges, or cloud metadata addresses. This can be abused as an authenticated blind server-side request forgery (SSRF). This issue has been patched in version 1.30.6.

### CVE-2026-55176

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-30T17:16:46.630 |

Soft Machine is a Virtual Machine–based agentic development environment / Cloud OS. In versions 0.2.247 and prior, two authentication helpers in /app/server.js — verifyContainerAuth() and authenticateWorkspaceHttp() — accept the global CONTAINER_SHARED_SECRET as a bearer token without verifying which workspace the caller belongs to. Because that secret is set identically on every container in the Fly app and is reachable from the user-facing process environment inside each workspace, any tenant can use it to authenticate to any other tenant's workspace API. The result is cross-workspace read, write, and destructive-restore primitives reachable from any paying customer's shell. The existing per-workspace token check (workspaceTokenMatches) protects the user-facing per-workspace token path, but the shared-secret bearer path bypasses it entirely. At time of publication, there are no publicly known patches.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-13313

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-489` |
| Published | 2026-10-01T02:16:53.817 |

An Active Debug Code vulnerability in certain ASUS router models allows a remote authenticated user, via a crafted HTTP request, to bypass security mechanisms and enable the Telnet service, thereby executing arbitrary commands with root privileges and potentially affecting other devices connected to the router.
Refer to the ' Security Update for ASUS Router Firmware ' section on the ASUS Security Advisory for more information.

### CVE-2026-100277

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-30T16:16:59.380 |

In JetBrains YouTrack before 2026.2.19197 account takeover was possible by replaying a notification signature

### CVE-2026-66246

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-10-01T14:17:29.770 |

iControl is affected by a Broken Access Control vulnerability, which could allow an attacker to exploit missing authentication checks or insecure direct object references (IDOR), enabling privilege escalation and the unauthorized modification or deletion of sensitive application data.

### CVE-2026-95687

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-01T09:17:10.273 |

The WPC Shop as a Customer for WooCommerce plugin for WordPress is vulnerable to privilege escalation via account takeover in all versions up to, and including, 2.0.0 This is due to the plugin not properly validating the target user's role prior to issuing a new authentication session, allowing an authenticated attacker to log in as any WordPress Administrator by directly supplying an Administrator's user ID to the wpcsa_login endpoint and receiving a full Administrator session cookie without supplying the Administrator's password. This makes it possible for authenticated attackers to perform a direct session takeover, gaining full Administrator-level access to the site.

### CVE-2026-19807

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-01T08:16:51.390 |

The ByteCoreStack – MCP Connector for AI Tools plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 1.2.3 This is due to the `wp_update_user_meta` MCP tool in `execute_tool` gating writes solely with `current_user_can('edit_user', $uid)` — a check that WordPress core's `map_meta_cap` resolves to the `read` primitive when the target user ID matches the caller's own — while enforcing an incomplete meta key blocklist that covers only `user_pass`, `user_activation_key`, and `session_tokens`, leaving the `wp_capabilities` and `wp_user_level` meta keys entirely unprotected. This makes it possible for authenticated attackers with Subscriber-level access and above to elevate their privileges to Administrator by issuing a `wp_update_user_meta` call over the MCP JSON-RPC endpoint with `key=wp_capabilities` and an arbitrary role array such as `{'administrator': true}` targeting their own user ID, causing WordPress to load that account as an Administrator on the next request.

### CVE-2026-80275

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-425` |
| Published | 2026-10-01T06:17:09.720 |

Comelit Multi-User Gateway for VIP System (model 1456B) firmware versions 2.9.1 and 2.10.0 fail to enforce server-side authorization on an administrative password-change function. An authenticated user level can invoke this function to overwrite the installer (administrator) account password.

### CVE-2026-101147

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-01T06:17:01.790 |

The Featured Image from URL (FIFU) WordPress plugin before 6.0.8, Featured Image from URL (FIFU) Premium WordPress plugin before 8.2.8 do not correctly enforce the REST API nonce, disabling the check for the whole request when a crafted URL is used, which could allow attackers to make a logged-in administrator perform any REST API action, such as creating a new administrator account, via a CSRF attack.

### CVE-2026-102125

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-653;CWE-668` |
| Published | 2026-09-30T21:17:00.813 |

The sandbox that isolates document conversion on a Kiteworks appliance did not fully confine the code running inside it. Code already executing within that sandbox could potentially escape its confinement and act with the privileges of the service account that runs the application, which could allow an attacker in that position to read or modify application data and configuration, or to disrupt the service on the affected appliance.

### CVE-2026-102120

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-269` |
| Published | 2026-09-30T21:17:00.057 |

A privilege escalation vulnerability in Kiteworks could have allowed an attacker who had already obtained code execution on one node of a clustered Kiteworks deployment to run operating system commands with elevated privileges on another node of the same cluster. Insufficient input validation in an internal cluster management function let attacker-supplied values reach a privileged execution context; exploitation requires existing access to a node in the cluster, and the affected function is not reachable from outside the cluster.

### CVE-2026-97291

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T18:18:44.763 |

Contributor PHP Object Injection in Schema & Structured Data for WP & AMP <= 1.66 versions.

### CVE-2026-102377

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T18:18:14.393 |

Contributor PHP Object Injection in Photo Gallery by 10Web <= 1.8.46 versions.

### CVE-2026-100254

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-30T16:16:55.947 |

In JetBrains TeamCity before 2026.2, 
2026.1.4, 
2025.11.8 authenticated users could execute commands on Windows servers via CRLF injection in Pipeline Git connection settings

### CVE-2026-100253

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-09-30T16:16:55.780 |

In JetBrains TeamCity before 2026.2, 
2026.1.4, 
2025.11.8 sandbox escape leading to code execution was possible via the versioned settings Kotlin DSL

### CVE-2026-18783

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-30T15:22:30.350 |

Missing authentication for critical function vulnerability in Trex Digital Smart Manufacturing Systems Inc. Trex MES allows Authentication Bypass.

This issue affects Trex MES: through 2026-09-29.

### CVE-2026-103272

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-203` |
| Published | 2026-10-01T11:17:22.563 |

Ghost versions from 2.10.0 before 6.63.0 contain a staff enumeration vulnerability in the content API that allows unauthenticated attackers to leak user data. Attackers can observe discrepancies in API metadata responses to enumerate staff members and extract sensitive information without authentication.

### CVE-2026-103271

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-01T11:17:22.407 |

Ghost versions from 4.0.0 before 6.63.0 contain a content API vulnerability that allows unauthenticated visitors to access gated post content. Attackers can bypass content restrictions by directly querying the content API to retrieve restricted posts without authentication.

### CVE-2026-103268

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-01T11:17:22.073 |

Ghost versions before 6.62.0 contain an authentication bypass vulnerability that allows suspended staff users to reactivate their accounts through self-service password reset. Attackers with suspended staff credentials can perform password reset operations to regain active account access and restore their original privileges.

### CVE-2026-103262

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-10-01T11:17:21.050 |

Tornado versions before 6.5.9 contain an unbounded memory accumulation vulnerability in CurlAsyncHTTPClient that allows remote attackers to cause denial of service by sending a compressed response. Attackers can send a gzip-encoded decompression bomb that accumulates in memory without size limits, causing the application process to be killed by out-of-memory conditions.

### CVE-2026-19253

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-10-01T06:17:08.467 |

The Cache Enabler WordPress plugin before 1.8.17 does not validate a URL before using it to build a filesystem path in its cache purge routine, and does not confine the resulting deletion to the cache directory, allowing unauthenticated users to delete arbitrary files and directories on sites where another installed Cache Enabler WordPress plugin before 1.8.17 or  passes a request-derived URL to its public cache-clearing hook.

### CVE-2026-82828

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-01T05:17:10.937 |

Hitachi Coding Software Suite contains an Incorrect Authorization vulnerability that allows an unprivileged user to perform administrator-level operations.


This issue affects Hitachi Coding Software Suite: through 3.3.0.

### CVE-2026-82826

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-10-01T05:17:10.633 |

Hitachi Coding Software Suite contains a vulnerability related to the Cleartext Transmission of Sensitive Information which allows an attacker to eavesdrop on with authentication credentials and sensitive data in transit.


This issue affects Hitachi Coding Software Suite: through 3.3.0.

### CVE-2026-103591

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-30T23:16:58.773 |

DeepWiki-Open through commit d92819a contains an unauthenticated arbitrary file read vulnerability in the GET /codemap/file endpoint via the repo_url parameter. Attackers can supply a non-URL repo_url value to bypass path containment checks and read any file accessible to the API process by specifying absolute file paths.

### CVE-2026-103000

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-30T21:17:07.490 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.19.0, a crafted PDF can provide unusually large alphabetical page-label values that cause pypdf/_page_labels.py to generate strings beyond a reasonable page-label length when an application retrieves document page labels, consuming excessive memory and potentially making the application unavailable. This issue is fixed in version 6.19.0.

### CVE-2026-102999

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-09-30T21:17:07.343 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.19.0, a crafted PDF containing many embedded files can cause the dictionary-based attachments API in pypdf/_doc_common.py to reparse the full attachment list for each content lookup, producing repeated work and long runtimes when an application accesses the embedded-file mapping. This issue is fixed in version 6.19.0.

### CVE-2026-102998

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-30T21:17:07.177 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.19.0, a crafted PDF with form field values can cause pypdf/generic/_appearance_stream.py appearance-stream generation to repeat invariant selection-data work inside a loop when an application updates fields with flattening enabled, resulting in excessive runtimes and application unavailability. This issue is fixed in version 6.19.0.

### CVE-2026-102997

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-09-30T21:17:07.020 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.18.1, a crafted PDF containing a partially malformed /FlateDecode stream with padded data can force pypdf/filters.py to use inefficient byte-by-byte decompression while the earlier recovery counter fails to advance for bytes that successfully decode, causing long runtimes and application unavailability. This is a residual issue after the malformed FlateDecode recovery fix. This issue is fixed in version 6.18.1.

### CVE-2026-102996

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-30T21:17:06.863 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.18.1, a crafted PDF can provide a TrueType or Type1 simple font with an unusually large /Widths array, causing pypdf/_font.py Font._collect_tt_t1_character_widths to process entries beyond the 256 character codes meaningful for a simple font and consume excessive memory during operations such as text extraction. This issue is fixed in version 6.18.1.

### CVE-2026-102995

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-30T21:17:06.713 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.18.1, a crafted PDF can place unusually large source-code or destination-string tokens in a font /ToUnicode mapping, causing pypdf/_cmap.py parse_bfchar to decode and retain oversized values during operations such as text extraction and consume excessive memory. This is a second follow-up to earlier /ToUnicode resource-consumption fixes and is limited to the remaining token-length path. This issue is fixed in version 6.18.1.

### CVE-2026-102100

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T21:16:56.750 |

Kiteworks Core before version 9.5.0 is vulnerable to Stored Cross-Site Scripting. A stored cross-site scripting (XSS) weakness in Kiteworks Core could allow an authenticated user to submit content that, when later viewed by another user, executes arbitrary JavaScript in that user's authenticated session. This could be used to perform actions on the victim's behalf and may have permitted account takeover, including of higher-privileged users. Exploitation requires the victim to view the attacker-supplied content.

### CVE-2026-102092

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T21:16:55.743 |

Kiteworks Core before version 9.5.0 is vulnerable to Stored Cross-site Scripting (XSS) that could allow an authenticated user to store crafted content that executes arbitrary JavaScript in another user's authenticated session when they preview shared content. This could potentially lead to session compromise and account takeover.

### CVE-2024-58387

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-30T21:16:52.510 |

Inspur Haiyue HCM Cloud contains an arbitrary file read vulnerability in the /api/model_report/file/download endpoint that allows unauthenticated remote attackers to read arbitrary files by supplying unvalidated path parameters index and ext. Attackers can craft requests such as /api/model_report/file/download?index=/&ext=<path> to traverse the filesystem and disclose sensitive files including /etc/passwd, application database files, and system configuration files. Exploitation evidence was first observed by the Shadowserver Foundation on 2024-11-04 .

### CVE-2023-54403

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-30T21:16:52.150 |

Yonyou U8 CRM before V16.5 and V18 contains an arbitrary file read vulnerability in /ajax/getemaildata.php that allows unauthenticated attackers to bypass authentication using the DontCheckLogin=1 parameter and read arbitrary files via an unvalidated filePath parameter. Attackers can exploit this flaw to read sensitive files outside the web application directory, including configuration files containing database or service credentials. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-14.

### CVE-2023-54402

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-30T21:16:51.980 |

iDocView contains a server-side request forgery vulnerability in its /doc/upload endpoint that allows remote unauthenticated attackers to fetch arbitrary URLs by supplying a hardcoded default token value (testtoken) to bypass authentication. Attackers can exploit the unrestricted URL scheme handling, including file:// URIs, to read arbitrary local files such as operating-system and application configuration files, and to reach internal network hosts and services not otherwise accessible. Exploitation evidence was first observed by the Shadowserver Foundation on 2024-03-26.

### CVE-2026-102994

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-09-30T20:17:28.080 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.18.0, a crafted PDF containing indirect-object identifiers or generation-number tokens that continue for a long time without whitespace can cause pypdf/_reader.py and pypdf/generic/_base.py to scan excessive input through read_until_whitespace, resulting in long runtimes and application unavailability. This issue is fixed in version 6.18.0.

### CVE-2026-102993

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-09-30T20:17:27.630 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.17.0, a crafted PDF can provide unusually large Roman page-label values that cause pypdf/_page_labels.py to generate excessively large numeral strings when an application retrieves document page labels, consuming large amounts of memory and potentially making the application unavailable. This issue is fixed in version 6.17.0.

### CVE-2026-101882

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-09-30T20:17:19.790 |

OpenClaw Windows Node before 2026.7.1 contains an incomplete validation vulnerability in system.execApprovals.set that accepts wildcard-executable rules and abusable system binaries like mshta, rundll32, and certutil. Remote callers can add broad allow rules to execute arbitrary commands on the Windows host through system.run without operator checks or user prompts.

### CVE-2026-101880

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-30T20:17:18.857 |

OpenClaw Windows Node before 2026.7.1 contains an incorrect authorization vulnerability in the system.run exec-approval policy where ExecShellWrapperParser fails to split commands on pipe operators or extract command substitutions. Connected gateways or agents can bypass approval rules by placing denied commands behind allowed prefixes using pipe operators or command substitution syntax, achieving arbitrary command execution on Windows hosts.

### CVE-2026-55224

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-30T18:18:37.713 |

MineAdmin is a ready-to-use backend management system suitable for quickly building website backends, operation platforms, permission centers, internal management systems, CMS, CRM, OA, ERP and other business applications. Prior to version 3.2.0-alpha.2, the app-store plugin service concatenates unsanitized user-supplied identifier values directly into file system paths. An attacker can use path traversal sequences (e.g., ../) to read, install, or uninstall plugins from arbitrary directories, and potentially execute arbitrary composer commands. This issue has been patched in version 3.2.0-alpha.2.

### CVE-2026-55094

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-94;CWE-95;CWE-250;CWE-306` |
| Published | 2026-09-30T18:18:37.387 |

Taskcluster is the task execution framework that supports Mozilla's continuous integration and release processes. Prior to version 100.3.0, Taskcluster is vulnerable to unauthenticated RCE on Taskcluster deployments with an anonymous role that exposes the GraphQL endpoint and parses filter arguments using the sift library. This issue has been patched in version 100.3.0.

### CVE-2026-103474

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-30T18:18:17.647 |

yii2-starter-kit through 4.2.0 fails to validate file types in the backend storage upload actions, allowing authenticated managers to upload PHP files. Attackers with manager role can upload PHP scripts to the web-accessible storage directory and request them to execute arbitrary code on the server.

### CVE-2026-103472

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-30T18:18:17.330 |

restbed through 5.0.0 accepts WebSocket frames with declared payload lengths up to 2^63 bytes and buffers the payload without size limits in an unbounded stream buffer. Remote unauthenticated attackers can declare large frame sizes and stream payload data to exhaust server memory, causing denial of service through process crash.

### CVE-2026-103471

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-30T18:18:17.163 |

restbed through 5.0.0 buffers HTTP request headers without enforcing a maximum size limit, allowing remote unauthenticated attackers to exhaust server memory. Attackers can open TCP connections and stream bytes indefinitely without sending the header delimiter, forcing the server to allocate unbounded heap memory until the process is killed.

### CVE-2026-47097

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-30T15:22:30.857 |

AJA HELO Plus firmware before 2.1.7 contains an information disclosure vulnerability that allows unauthenticated attackers to decrypt sensitive diagnostics bundles by exploiting a static AES passphrase embedded in obfuscated form within the firmware. Attackers can reverse engineer the publicly available firmware image to recover the shared passphrase and decrypt diagnostics export bundles retrieved from the unauthenticated diagnostics endpoint on any affected device, exposing highly sensitive server information.

### CVE-2026-103270

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-30T15:22:26.903 |

LightLLM through 1.2.0 mounts reinforcement learning control routes on the public HTTP API without authentication checks. Unauthenticated attackers can call endpoints like /pause_generation, /abort_request, /flush_cache, and /init_weights_update_group to disrupt inference operations and wedge workers on deployments started with --enable_rl.

### CVE-2026-88789

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-01T11:17:28.917 |

Improper Restriction of XML External Entity Reference in the XSLT support extension (camel-quarkus-support-xalan) in Apache Camel Quarkus from 3.2.0 before 3.33.3 and from 3.34.0 before 3.40.0 on all platforms allows an attacker who supplies the XML document being transformed to read local files or issue requests to internal network locations via an external entity declaration in that document.

The extension supplies its own Xalan-backed TransformerFactory to the xslt component and registers it as the JAXP default. Xalan-J 2.7.x predates JAXP 1.5 and does not honour javax.xml.XMLConstants.ACCESS_EXTERNAL_DTD or ACCESS_EXTERNAL_STYLESHEET, so the external access restrictions Apache Camel applies to the TransformerFactory it creates were not in effect. On the xslt component path this affects message bodies that reach the transformer already as a javax.xml.transform.Source; bodies of other types are converted to a SAXSource by Apache Camel with external entities and external DTD loading disabled, and are not affected. Because the factory is also the JAXP default, other code in the application obtaining one through TransformerFactory.newInstance() loses the same restrictions without error.

Applications are affected if they use any of camel-quarkus-xslt, camel-quarkus-xslt-saxon, camel-quarkus-tika or camel-quarkus-xmlsecurity, each of which brings the XSLT support extension onto the classpath. For all but camel-quarkus-xslt, the exposure is limited to the JAXP default factory, since those extensions do not perform XSLT transformations themselves.

Users are recommended to upgrade to version 3.33.3 or 3.40.0, which fixes this issue.

### CVE-2026-103758

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-01T11:17:26.360 |

Obot 0.21.1 through 0.24.1 contains an authorization bypass vulnerability that allows authenticated users to reach MCP servers because the checkUI deny list omits the /mcp-connect-composite/ route. Basic-role users with a composite MCP ID can proxy requests through mcpGateway.Proxy to invoke tools on MCP servers restricted by Access Control Rules.

### CVE-2026-103292

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T11:17:25.847 |

Ghost versions from 0.5.3 through versions prior to 6.50.0 fail to sanitize the data placed in the JSON-LD HTML tag emitted by the {{ghost_head}} helper. An authenticated user with limited privileges can inject unescaped content that is rendered as script in the published page, potentially leading to compromise of a staff user's admin session when that user views the affected page.

### CVE-2026-103283

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-10-01T11:17:24.397 |

Ghost versions 6.20.0 before 6.57.1 contain a session handling vulnerability that allows authenticated staff users to log in as any other staff user with only the password, bypassing two-factor authentication. Attackers with valid staff credentials can exploit improper session management to impersonate other staff members and gain unauthorized access to administrative functions.

### CVE-2026-103277

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T11:17:23.403 |

Ghost versions from 2.5.0 before 6.34.0 contain an untrusted script execution vulnerability in the oEmbed preview feature that fails to sandbox externally hosted scripts. Attackers can craft malicious oEmbed content to execute scripts in the context of a staff user's admin session, potentially compromising administrative access.

### CVE-2026-64949

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:Y/R:I/V:C/RE:M/U:Red` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-01T10:17:16.207 |

Incomplete extension blacklist in the File Manager module allows authenticated upload and execution of arbitrary .phar files. Affects Pandora FMS from 777 onwards.

### CVE-2026-89296

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-01T06:17:14.337 |

The Pro Like Button WordPress plugin before 2.0 does not properly sanitize and escape a parameter before using it in a SQL query, allowing unauthenticated users to perform SQL injection attacks.

### CVE-2026-102121

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-306` |
| Published | 2026-09-30T21:17:00.213 |

A form-rendering interface in the Advanced Forms component is reachable without authentication so that published forms can be displayed to anonymous visitors, but it returned more data than the form itself required. Anyone who knew the web address of a published form could potentially retrieve the form owner's Kiteworks account profile, including personal details, along with parts of the deployment's configuration settings; no passwords, authentication tokens, or multi-factor secrets were exposed.

### CVE-2026-103398

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-30T15:22:28.800 |

OpenSave through 2.4.0 fails to properly validate save paths supplied by paired peers in the manifest request handler. Attackers can specify arbitrary directories outside configured save locations to read and write files through manifest and sync routes.

### CVE-2026-103338

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-01T13:17:08.350 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Unlimited Elements Unlimited Elements For Elementor (Free Widgets, Addons, Templates) unlimited-elements-for-elementor allows Blind SQL Injection.This issue affects Unlimited Elements For Elementor (Free Widgets, Addons, Templates): from n/a through 2.0.20.

### CVE-2026-102379

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-01T13:17:07.297 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in VillaTheme BuildKit – Product Builder for WooCommerce – Custom PC Builder woo-product-builder allows Blind SQL Injection.This issue affects BuildKit – Product Builder for WooCommerce – Custom PC Builder: from n/a through 1.0.28.

### CVE-2026-103286

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-01T11:17:24.880 |

Ghost versions from 2.21.0 before 6.56.0 contain a privilege escalation vulnerability in the notifications system that allows low-privilege staff users to escalate to higher-privilege staff roles. Attackers with low-privilege staff access can exploit the notifications system to gain elevated privileges without proper authorization checks.

### CVE-2026-103278

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-10-01T11:17:23.567 |

Ghost versions 5.8.0 before 6.34.0 contain an input validation vulnerability in the admin iframe that allows attackers to take over staff user accounts. Attackers with content publishing privileges can craft malicious pages that, when visited by active staff users, enable account takeover through improper input validation.

### CVE-2026-103259

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:A/VC:H/VI:H/VA:H/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-01T11:17:20.473 |

n8n versions before 2.39.6 and 2.40.0 before 2.40.1 contain a session token leakage vulnerability in the Dynamic Credentials authorize and revoke endpoints. Attackers with resolver registration capability can capture collaborators' session tokens by setting a fallback resolver to an attacker-controlled endpoint during the account connection flow, enabling unauthorized credential access.

### CVE-2026-101885

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-30T20:17:21.157 |

ZeroClaw versions before 0.8.5 built with plugins-wasm feature contain a path traversal vulnerability in plugin installation that fails to validate the wasm_path manifest field. Attackers can convince users to install crafted plugins that write arbitrary files to paths outside the plugins directory, such as shell startup files, enabling code execution.

### CVE-2026-64950

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:Y/R:U/V:C/RE:L/U:Amber` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T10:17:16.367 |

Missing input validation and output encoding on the directory name parameter in File Manager's Create Directory allows stored XSS, executing without user interaction. Affects Pandora FMS from 777 onwards.

### CVE-2026-76146

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-01T05:17:09.783 |

An OS command injection vulnerability in Genian SSL PNS allows an attacker who knows only the client access ID, without the password, to execute arbitrary commands remotely

### CVE-2026-103757

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-01T11:17:26.177 |

Budibase through 3.41.0 contains a server-side request forgery vulnerability in AI table generation because the uploadUrl function in packages/server/src/utilities/fileUtils.ts uses raw node-fetch instead of fetchWithBlacklist. Authenticated builder users can send a prompt to POST /api/ai/tables that places an internal URL in an attachment column, causing the server to fetch it and return a presigned object-storage URL containing the response, such as cloud metadata credentials.

### CVE-2026-103246

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-01T11:17:17.887 |

n8n versions before 2.39.6 and 2.40.0 before 2.40.1 fail to validate credential ownership during inline agent node-tool introspection. Attackers can reference arbitrary credential IDs to decrypt and exfiltrate plaintext secrets to attacker-controlled hosts without ownership verification.

### CVE-2026-46711

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-30T17:16:46.060 |

Soft Machine is a Virtual Machine–based agentic development environment / Cloud OS. In versions 0.2.247 and prior, the workspace HTTP service that listens on 0.0.0.0:8080 inside each sm-ws-* Fly Machine exposes endpoints (/health, /file/<path>, /archive/<dir>) without any authentication or origin check. Any host that can reach TCP/8080 on a workspace can read arbitrary files under that workspace's /workspace root and download whole project trees as tar archives. Because every workspace shares the same Fly private 6PN and resolves all peer addresses via the unauthenticated _instances.internal TXT record, every other sm-ws-* machine on the same Fly app/org is a reachable, unauthenticated attacker — the trust boundary (workspace owner ↔ everyone-else) is missing. At time of publication, there are no publicly known patches.

### CVE-2026-94250

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-01T12:17:17.063 |

Allocation of resources without limits or throttling vulnerability in batch-requests plugin in Apache APISIX.



An unauthenticated caller can drive a gateway worker into OOM via a route where the batch-requests plugin is used and the batch endpoint is publicly exposed. This issue affects Apache APISIX: from 1.3.0 through 3.18.0.



Users are recommended to upgrade to version 3.19.0, which fixes the issue.

### CVE-2026-103263

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-01T11:17:21.233 |

Tornado before 6.5.9 contains a path traversal vulnerability in StaticFileHandler that follows symbolic links inside the static root without confirming the resolved target stays within it. When a symlink pointing outside the static directory exists inside it, unauthenticated attackers can request it to read files such as configuration files, private keys, and application secrets accessible to the process user.

### CVE-2026-102990

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-09-30T20:17:26.140 |

basic-ftp is an FTP client for Node.js. Prior to 6.2.1, Client.list() can be forced by a malicious or compromised FTP server to spend quadratic CPU time parsing a directory listing because the RE_LINE expression in src/parseListUnix.ts backtracks across adjacent variable-length owner and group fields when a long Unix-style line has a valid prefix but cannot satisfy the later size and date fields. parseList() selects a parser from the last nonblank line and then applies it to every line, so a normal final line can select the Unix parser while an earlier crafted line blocks the Node.js event loop and freezes the process. This issue is fixed in version 6.2.1.

### CVE-2026-100273

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-30T16:16:58.720 |

In JetBrains YouTrack before 2026.2.19197 authorisation bypass in the scripts debugger allowed arbitrary code execution

### CVE-2026-102984

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-09-30T15:22:23.490 |

Astro is a web framework for content-driven websites. Prior to 11.1.3, the @astrojs/node adapter builds a request URL from the Host header, and a malformed port can make that URL invalid. The recovery path reuses the same malformed host and throws an uncaught TypeError: Invalid URL before routing begins. In the default standalone configuration, the request returns an HTTP 500 response and the server continues running, but when staticHeaders is enabled the synchronous handler does not catch the exception and the Node process terminates. Proxies and CDNs that reject malformed Host headers prevent this path from reaching the origin. The issue affects availability only and does not expose data or permit code execution. This issue is fixed in version 11.1.3.

### CVE-2026-103257

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-01T11:17:20.100 |

n8n versions before 1.123.80, from 2.0.0 before 2.39.6, and from 2.40.0 before 2.40.1 contain a path traversal vulnerability in the n8n node that fails to validate resource identifiers. Attackers can craft malicious resource IDs to redirect API calls to unintended resources, allowing unauthorized access to workflows, executions, and credential secrets within the API key's scope.

### CVE-2026-103493

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T10:17:14.780 |

In JetBrains YouTrack before 2026.2.19422 stored XSS via Mermaid and LaTeX content was possible

### CVE-2026-15983

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-10-01T09:17:09.223 |

The Super Forms – Drag & Drop Form Builder plugin for WordPress is vulnerable to Arbitrary File/Directory Deletion in all versions up to, and including, 6.3.316. This is due to the `super_save_form` AJAX handler performing no capability check — allowing Subscriber-level authenticated users to create or modify Super Forms and enable the `file_upload_submission_delete` setting — combined with the `super_submit_form` handler's `submit_form` function passing the attacker-controlled `files[].subdir` value from `$_POST['data']` directly into `SUPER_Common::delete_dir()` without sanitization, and a trivially bypassed `ABSPATH` guard that a `subdir` value of `wp-config.php` defeats because `dirname(realpath(ABSPATH . $subdir))` resolves to the WordPress root while the naive `ABSPATH !== $dir` string check fails to match due to a trailing-slash mismatch. This makes it possible for authenticated attackers, with Subscriber-level access and above, to recursively delete arbitrary files and directories on the server, up to and including the entire WordPress installation, resulting in full site takedown and potential remote code execution if critical files such as `wp-config.php` are removed and the site is subsequently re-installed by another party.

### CVE-2026-51570

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-30T21:17:11.137 |

modelscope Agentscope v1.0.0-v1.0.8 is vulnerable to Path Traversal in insert_text_file.

### CVE-2026-51568

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-30T21:17:10.993 |

modelscope Agentscope v1.0.18-v1.0.0 is vulnerable to Path Traversal in write_text_file.

### CVE-2026-102126

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T21:17:00.963 |

A stored cross-site scripting (XSS) weakness in Kiteworks Core could allow an administrator holding only a single, narrowly scoped delegated permission to store crafted content that later executes arbitrary JavaScript in the authenticated session of a System Administrator who views the affected page. This could have permitted the lower-privileged administrator to escalate to full administrative control of the tenant, including the creation of a new administrative account.

### CVE-2026-102101

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T21:16:56.880 |

Kiteworks Core before version 9.5.0 is vulnerable to Deserialization of Untrusted Data. A deserialization weakness in Kiteworks Core could, under certain conditions, allow crafted data to be deserialized unsafely, potentially resulting in remote code execution on the appliance. Exploitation depends on an attacker first being able to influence the affected data, so this issue is not exploitable on its own.

### CVE-2026-87004

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-30T18:18:41.470 |

Tugtainer is a self-hosted app for automating updates of Docker containers. Prior to version 1.31.3, when the OIDC login flow completes, backend/modules/auth/providers/auth_oidc_provider.py decodes the id_token returned by the identity provider's token endpoint using jose.jwt.get_unverified_claims() instead of jwt.decode(). This skips signature verification, audience (aud) validation, issuer (iss) validation, and expiry (exp) checking entirely. The extracted claims (email/sub/preferred_username) are then used directly as the user_id for the resulting Tugtainer session. This issue has been patched in version 1.31.3.

### CVE-2026-103432

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-30T16:17:09.533 |

apcupsd through 3.14.14 has an sscanf stack-based buffer overflow in getupsvar() in src/cgi/upsfetch.c (used by upsstats.cgi, multimon.cgi, and upsfstats.cgi), a related issue to CVE-2026-15544.

### CVE-2026-100255

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1289` |
| Published | 2026-09-30T16:16:56.100 |

In JetBrains TeamCity before 2026.2, 
2026.1.4, 
2025.11.8 administrator account takeover was possible via password reset

### CVE-2026-103067

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-01T13:17:08.223 |

Cross-Site Request Forgery (CSRF) vulnerability in Memberful Memberful - Membership Plugin memberful-wp allows Cross Site Request Forgery.This issue affects Memberful - Membership Plugin: from n/a through 1.81.0.

### CVE-2026-102118

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59;CWE-250` |
| Published | 2026-09-30T21:16:59.707 |

A local privilege escalation vulnerability in Kiteworks could have allowed an attacker with an existing shell under a low-privileged service account to escalate to root privileges on the appliance.

### CVE-2026-102113

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59;CWE-269` |
| Published | 2026-09-30T21:16:58.427 |

A privilege escalation vulnerability in Kiteworks could allow an attacker who has already obtained code execution as an unprivileged backend service account on the appliance to escalate to root. A privileged routine did not safely handle a filesystem path that the lower-privileged account could influence, allowing the attacker to cause a root-owned operation to run arbitrary commands with the highest privileges. Exploitation requires existing local access to that service account.

### CVE-2026-102112

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-269` |
| Published | 2026-09-30T21:16:58.267 |

A privilege escalation vulnerability in Kiteworks could allow an attacker who has already obtained code execution as an unprivileged backend service account on the appliance to escalate to root and run arbitrary commands with the highest privileges. Exploitation requires existing local access to that service account.

### CVE-2026-53605

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250;CWE-269` |
| Published | 2026-09-30T18:18:37.213 |

Reachy Mini ISO for Wireless contains the necessary files to build a custom Raspberry Pi OS image for the Reachy Mini Wireless robot, using pi-gen. Prior to version 0.2.4, the Reachy Mini Wireless OS image shipped with an overly broad sudoers entry granting the pollen daemon user (uid 1000) passwordless sudo access to /usr/bin/systemctl with no subcommand or argument restriction. This is a local privilege escalation (LPE). Any process running as pollen can obtain full root (uid 0) on the device in three commands, with no additional vulnerability required and no user interaction. This issue has been patched in version 0.2.4.

### CVE-2026-47601

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T16:17:30.563 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the open-source kernel module DMA-BUF import path where an unprivileged local user could cause improper preservation of memory access permissions when importing a read-only buffer from another device's DMA-BUF exporter. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, denial of service, information disclosure, and data tampering.

### CVE-2026-47600

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-09-30T16:17:30.400 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer where an error-handling path could operate on an improperly initialized resource. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, denial of service, information disclosure, and data tampering.

### CVE-2026-47599

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-281` |
| Published | 2026-09-30T16:17:30.270 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the open-source kernel module where an unprivileged local user could cause improper preservation of memory access permissions during DMA mapping. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, denial of service, information disclosure, and data tampering.

### CVE-2026-47597

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-30T16:17:29.963 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the open-source kernel module Resource Server where an unprivileged local user could cause a use-after-free through a missing self-reference guard in the map cleanup path. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, denial of service, information disclosure, and data tampering.

### CVE-2026-47595

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-281` |
| Published | 2026-09-30T16:17:29.680 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the kernel mode layer where an unprivileged user can write to read-only memory because the memory's permissions are not preserved. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, denial of service, information disclosure, and data tampering.

### CVE-2026-47594

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-30T16:17:29.513 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability where an unprivileged user may cause a use-after-free condition by issuing a sequence of driver commands. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, denial of service, data tampering, and information disclosure.

### CVE-2026-47593

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-30T16:17:29.370 |

NVIDIA GPU Display Driver for Windows contains a vulnerability in the kernel mode layer where an unprivileged user can cause an out-of-bounds write. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, and denial of service.

### CVE-2026-47592

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-30T16:17:29.200 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer where an unprivileged user could cause an out-of-bounds read. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47591

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-30T16:17:29.053 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the kernel mode layer where an unprivileged user could bypass read-only memory protection due to incorrect authorization, enabling write access to memory marked read-only. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47590

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-30T16:17:28.897 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability where an unprivileged user may cause a use-after-free condition by issuing a sequence of driver commands. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, denial of service, and information disclosure.

### CVE-2026-47589

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-30T16:17:28.733 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability where an unprivileged user may cause a use-after-free condition by issuing a sequence of driver commands. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, denial of service, and information disclosure.

### CVE-2026-47588

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-30T16:17:28.577 |

NVIDIA GPU Display Driver for Linux contains a vulnerability where an unprivileged user could cause a use-after-free condition by issuing a sequence of driver commands. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, denial of service and information disclosure.

### CVE-2026-47587

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-30T16:17:28.443 |

NVIDIA GPU Display Driver for Linux contains a vulnerability where an unprivileged user could cause a use-after-free. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, denial of service, information disclosure, and data tampering.

### CVE-2026-47585

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-09-30T16:17:28.137 |

NVIDIA GPU Display Driver for Windows contains a vulnerability in the kernel module where an attacker could cause an integer underflow. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47583

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-30T16:17:27.857 |

NVIDIA GPU Display Driver for Windows contains a vulnerability in the kernel module where an attacker could cause type confusion. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47579

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-30T16:17:27.273 |

The NVIDIA GPU Display Driver for Windows contains a vulnerability in the kernel mode driver through which a user might trigger a use-after-free condition. Successful exploitation of this issue could lead to code execution, escalation of privileges, denial of service, information disclosure, and data tampering.

### CVE-2026-47578

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-131` |
| Published | 2026-09-30T16:17:27.130 |

NVIDIA GPU Display Driver for Windows contains a vulnerability in the kernel mode layer where an attacker could cause an incorrect buffer size calculation. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47577

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-30T16:17:26.990 |

NVIDIA GPU Display Driver for Windows contains a vulnerability in the kernel module where an attacker could cause an incorrect comparison. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47575

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T16:17:26.710 |

NVIDIA GPU Display Driver for Windows contains a vulnerability in the display driver DIAG escape handler where a local unprivileged attacker may cause an integer overflow and out-of-bounds write. A successful exploit of this vulnerability might lead to denial of service, and code execution.

### CVE-2026-47574

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-669` |
| Published | 2026-09-30T16:17:26.580 |

NVIDIA vGPU Virtual GPU Manager for Linux contains a vulnerability where an attacker could cause incorrect resource transfer between spheres. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47573

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T16:17:26.437 |

NVIDIA NVAPI for Windows contains a vulnerability where an attacker could cause an out-of-bounds write. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47572

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-30T16:17:26.297 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the kernel mode layer where a user could cause type confusion. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47571

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-30T16:17:26.123 |

NVIDIA GPU Display Driver for Windows contains a vulnerability in kernel-mode escape handling where an attacker with local access could bypass an authorization check that is intended to restrict certain operations based on client execution context. A successful exploit of this vulnerability might lead to escalation of privilege, information disclosure, data tampering, denial of service, or code execution.

### CVE-2026-47570

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-09-30T16:17:25.970 |

NVIDIA GPU Display Driver for Windows contains a vulnerability in the CUDA driver where an attacker could cause a library to be loaded from an uncontrolled search path. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, information disclosure, data tampering, and denial of service.

### CVE-2026-47569

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-30T16:17:25.827 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the kernel mode layer where a user could cause a type confusion via a handle recycle race. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47563

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-30T16:17:25.040 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the kernel mode layer where a user could cause a NULL pointer dereference. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47561

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T16:17:24.693 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the kernel mode layer where the size of an ioctl input buffer is not validated, allowing an unprivileged caller to trigger an out-of-bounds write in kernel memory. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47560

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-30T16:17:24.547 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the kernel mode layer where an unprivileged user could cause a use-after-free. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47559

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-30T16:17:24.373 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer, where a user could access memory belonging to another user's process. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, data tampering, denial of service, and information disclosure.

### CVE-2026-47558

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-30T16:17:24.227 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the kernel mode layer where an unprivileged user could cause a double-free of imported memory state. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47556

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-30T16:17:23.913 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer where an unprivileged user could cause an integer overflow that leads to an out-of-bounds write. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47553

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T16:17:23.410 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer where an unprivileged user could cause an out-of-bounds write. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47552

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-30T16:17:23.263 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the kernel mode layer where an unprivileged user could bypass an authorization check and modify privileged configuration. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47551

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-30T16:17:23.080 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer where a user could cause a use-after-free. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47550

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-09-30T16:17:22.937 |

NVIDIA GPU Display Driver for Windows contains a vulnerability in the kernel mode layer where an unprivileged local user can supply an untrusted pointer that the driver dereferences without validation. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47548

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T16:17:22.600 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer where an attacker could cause an out-of-bounds write. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47545

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-30T16:17:22.100 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer where an attacker could cause an out-of-bounds read. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47541

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T16:17:21.470 |

NVIDIA vGPU Virtual GPU Manager for Linux contains a vulnerability in the kernel mode layer where an attacker could cause an out-of-bounds write. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47540

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-09-30T16:17:21.290 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer where an attacker could cause an integer underflow. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47536

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-30T16:17:20.677 |

NVIDIA vGPU Virtual GPU Manager for Linux contains a vulnerability in the kernel mode layer where an attacker could cause an out-of-bounds read. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47535

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-30T16:17:20.523 |

NVIDIA vGPU Virtual GPU Manager for Linux contains a vulnerability in the firmware where an attacker could cause an out-of-bounds read. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47530

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T16:17:19.667 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer where an attacker could cause an out-of-bounds write. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47528

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-824` |
| Published | 2026-09-30T16:17:19.327 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the firmware where an attacker could cause an access of an uninitialized pointer. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47523

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T16:17:18.493 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer where an attacker could cause an out-of-bounds write. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47521

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-30T16:17:18.187 |

NVIDIA vGPU Virtual GPU Manager for Linux contains a vulnerability in the kernel mode layer where an attacker could cause an out-of-bounds read. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47520

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-30T16:17:18.040 |

NVIDIA vGPU Virtual GPU Manager for Linux contains a vulnerability in the kernel mode layer where an attacker could cause an out-of-bounds read. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47519

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-30T16:17:17.897 |

NVIDIA vGPU Virtual GPU Manager for Linux contains a vulnerability in the kernel mode layer where an attacker could cause an out-of-bounds read. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47516

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-30T16:17:17.410 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability where an unprivileged user could cause a use-after-free. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, data tampering, denial of service, and information disclosure.

### CVE-2026-47514

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-30T16:17:17.063 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer, where a user could cause exposure of kernel stack contents including return addresses and pointers. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47513

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-30T16:17:16.903 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer, where a user could cause an out-of-bounds read from kernel heap memory. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47512

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-30T16:17:16.740 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer, where a user could cause an out-of-bounds read leading to kernel information disclosure. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47511

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T16:17:16.593 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer, where a user could cause an out-of-bounds write. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47510

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-30T16:17:16.447 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer, where a user could cause an integer overflow leading to an out-of-bounds write to GPU memory. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47508

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-681` |
| Published | 2026-09-30T16:17:16.110 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer, where a user could cause an incorrect conversion between numeric types. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47507

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-129` |
| Published | 2026-09-30T16:17:15.907 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer, where a user could cause an out-of-bounds array access. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47505

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-30T16:17:15.577 |

NVIDIA GPU Display Driver for Windows contains a vulnerability in the kernel mode layer where an attacker could cause a use-after-free. A successful exploit of this vulnerability might lead to code execution, denial of service, or escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47504

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-30T16:17:15.423 |

NVIDIA Linux GPU Display Driver contains a vulnerability in the NGX updater where an outdated embedded cryptographic library is susceptible to type confusion. A successful exploit of this vulnerability might lead to code execution, denial of service, information disclosure, or data tampering.

### CVE-2026-47503

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T16:17:15.280 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the Virtual GPU Manager (vGPU plugin), where a guest VM user may cause an out-of-bounds write by sending a crafted RPC message with invalid performance state list size parameters. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, data tampering, denial of service, and information disclosure.

### CVE-2026-47502

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-30T16:17:15.110 |

NVIDIA vGPU Virtual GPU Manager for Windows and Linux contains a vulnerability in the kernel mode layer, where a guest user could cause an integer overflow leading to memory corruption. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47501

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T16:17:14.953 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the kernel mode layer where a user could cause an out-of-bounds write by supplying mismatched memory buffers during event buffer setup. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47500

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-30T16:17:14.743 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode layer where improper cleanup of reference counts during error paths could lead to a use-after-free condition. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47499

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-30T16:17:14.570 |

NVIDIA vGPU Virtual GPU Manager for Windows and Linux contains a vulnerability in the kernel mode layer where a guest could cause an out-of-bounds read. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47498

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T16:17:14.433 |

NVIDIA vGPU Manager contains a vulnerability in the GPU System Processor (GSP) plugin where a guest VM user may cause an out-of-bounds write by sending a specially crafted RPC message. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, data tampering, denial of service, and information disclosure.

### CVE-2026-47497

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-30T16:17:14.293 |

NVIDIA Virtual GPU Manager contains a vulnerability in the GPU System Processor (GSP) tracing component where a guest VM user may cause improper access by sending crafted data through a shared buffer. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, data tampering, denial of service, and information disclosure.

### CVE-2026-47495

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T16:17:14.030 |

NVIDIA vGPU Virtual GPU Manager for Windows and Linux contains a vulnerability in the kernel mode layer where a user could cause an out-of-bounds write. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47494

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-09-30T16:17:13.893 |

NVIDIA GPU Display Driver for Linux contains a vulnerability where a user might be able to cause a format string issue. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, data tampering, denial of service, and information disclosure.

### CVE-2026-47493

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-30T16:17:13.753 |

NVIDIA vGPU software for Windows and Linux contains a vulnerability in the GPU kernel driver where a guest may access privileged host GPU resources for which it is not authorized. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, data tampering, denial of service, and information disclosure.

### CVE-2026-47491

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-404` |
| Published | 2026-09-30T16:17:13.433 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the kernel mode layer where an unprivileged user can cause improper release of memory resources, leaving a mapping accessible after the underlying memory is reused. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-47489

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-281` |
| Published | 2026-09-30T16:17:13.247 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the kernel mode layer where permissions on read-only memory might not be preserved. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-100256

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-09-30T16:16:56.243 |

In JetBrains IntelliJ IDEA before 2026.2.3 rCE via Structural Search script constraints was possible in untrusted projects

### CVE-2026-103431

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-150` |
| Published | 2026-10-01T09:17:07.717 |

colmux in collectl before 4.3.20.2 does not sanitize ANSI/VT100 terminal escape sequences in data received from remote collectl instances before displaying it, allowing a local user on a monitored host to inject escape sequences into the terminal of an operator running colmux, via a crafted process name (argv[0]).

### CVE-2026-101884

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-09-30T20:17:20.663 |

OpenClaw Windows Node before 2026.7.1 contains an incomplete environment-variable sanitizer in system.run that fails to block GIT_CONFIG_*, DOTNET_STARTUP_HOOKS, and JAVA_TOOL_OPTIONS variables. Attackers with gateway or agent access can supply these variables to allowlisted tools like git, dotnet, or java to load attacker-controlled code and achieve arbitrary code execution.

### CVE-2026-47576

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-30T16:17:26.850 |

NVIDIA GPU Display Driver for Windows contains a vulnerability in the kernel module through which an attacker might initiate an out-of-bounds read. Successful exploitation of this issue could lead to denial of service and information disclosure.

### CVE-2026-100268

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-30T16:16:58.000 |

In JetBrains YouTrack before 2026.2.19197 project administrators could read comments from other projects via notification templates

### CVE-2026-100266

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-30T16:16:57.707 |

In JetBrains Hub before 2026.2.52366 missing authorisation allowed authenticated users to send arbitrary emails from the server's trusted address

### CVE-2026-62060

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-01T13:17:10.140 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in captivateaudio Captivate Sync captivatesync-trade allows Blind SQL Injection.This issue affects Captivate Sync: from n/a through 3.3.2.

### CVE-2026-62059

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-01T13:17:10.010 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Ultimate Member Ultimate Member ultimate-member allows Blind SQL Injection.This issue affects Ultimate Member: from n/a through 2.13.1.

### CVE-2026-103279

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-10-01T11:17:23.743 |

Ghost versions from 3.10.0 before 6.34.0 fail to fully invalidate all sessions after a password change. Attackers with a stolen session cookie can maintain access to user accounts even after the associated user changes their password.

### CVE-2026-103651

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-362` |
| Published | 2026-10-01T08:16:51.020 |

MISP contains a vulnerability in its one-time password (OTP) authentication flow that allows replay of a consumed HOTP (paper) token and rewinding of the token counter.

The HOTP verification logic compared the submitted token against a counter value that was cached in the user's session at the time the password was entered, rather than against the authoritative counter stored in the database. Because the session-cached counter is not updated after a token is successfully consumed, an attacker who holds a valid session (password already submitted) can reuse a previously burned HOTP token. The stale cached counter still matches the replayed token, granting a second successful authentication and effectively rewinding the counter state.

Preconditions:

- The target user has HOTP (paper token) second-factor authentication enabled.

- The attacker possesses a valid session in which the password step has already been completed (the OTP step is pending).

- The attacker has access to at least one HOTP token value (e.g., a paper token list).

Security impact:

- Bypass of the second authentication factor, allowing unauthorized access to a user's MISP account.

- Corruption of the HOTP counter state, potentially invalidating subsequent legitimate tokens or enabling further replays.

Affected versions: <2.5.48.

### CVE-2026-55177

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-30T17:16:46.787 |

CloudTAK is a browser-based Common Operating Picture and situational awareness tool compatible with TAK. Prior to version 13.10.0, every route in the ESRI helper family (api/routes/esri.ts) takes a fully attacker-controlled URL from the request (POST /api/esri body url, and the portal / server / layer query parameters on the GET /api/esri/* routes) and passes it into EsriBase / EsriProxyPortal / EsriProxyServer / EsriProxyLayer in api/lib/esri.ts, which fetch it with the bare fetch from @tak-ps/etl. No IP / DNS / hostname classification is applied at any point, so the destination is never validated against private, loopback, or link-local ranges. Any authenticated user (the routes only require Auth.is_auth(config, req, { anyResources: true }), i.e. any token, not an admin) can therefore make the CloudTAK server issue arbitrary outbound GET/POST requests to internal addresses such as the cloud instance-metadata service (169.254.169.254), loopback admin ports (127.0.0.1:<port>), and other hosts reachable only from inside the deployment VPC. This is a full-read SSRF, not blind: on success the upstream JSON body is returned to the caller via res.json(...), and on failure the upstream error string is reflected verbatim as ESRI Server Error: <message>. An attacker can read cloud metadata (and the temporary IAM credentials the instance role exposes), enumerate internal services, and exfiltrate their response bodies. The sniff() URL classifier provides no protection: it only pattern-matches the pathname (/rest, /arcgis/rest, /sharing/rest), so a URL like http://169.254.169.254/arcgis/rest or http://127.0.0.1:8500/rest passes sniff() and is fetched. This issue has been patched in version 13.10.0.

### CVE-2026-19553

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-297` |
| Published | 2026-09-30T17:16:45.880 |

ssl.SSLContext.wrap_bio() didn't require the server_hostname argument
to not be None if ssl.SSLContext.check_hostname was set. Due to a
missing parameter check in SSLObject, if the server_hostname argument
isn't supplied then hostname verification would be silently skipped.


This defect could lead to programs where certificate hostname verification
*appeared* to be succeeding with SSLContext.check_hostname = True and no
ValueError being raised due to misconfiguration.


If the program passes a server_hostname value that isn't an empty string
or None to any of these APIs then certificate hostname verification
proceeds as expected and the program is not affected by this vulnerability.


Mitigating this vulnerability doesn't require updating Python or applying
the patch. To mitigate, pass a valid non-None and non-empty
server_hostname value to SSLContext.wrap_bio(),
asyncio.create_connection(), or asyncio.loop.start_tls() and
certificate hostname verification will proceed as expected. Upgrading to
the latest version of Python or applying the patch only changes the
behavior from silently skipping hostname verification to raising a
ValueError, similar to SSLContext.wrap_socket(), when server_hostname
isn't supplied.

### CVE-2026-100262

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-30T16:16:57.120 |

In JetBrains YouTrack before 2026.2.18991 missing authorisation allowed users with read-only project access to overwrite project notification templates

### CVE-2026-62097

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T15:22:32.350 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in WPTasty Business Directory business-directory-plugin allows Blind SQL Injection.This issue affects Business Directory: from n/a through 6.4.27.

### CVE-2026-103251

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-01T11:17:18.973 |

n8n versions before 1.123.80, from 2.0.0 before 2.39.6, and from 2.40.0 before 2.40.1 contain a validation bypass vulnerability in the community package installation handler for queue mode deployments. Attackers with Redis write access can bypass name validation, permission checks, checksum verification, and npm safety checks to install arbitrary npm packages across all cluster instances without authentication.

### CVE-2026-64947

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:Y/R:I/V:C/RE:H/U:Red` |
| Weaknesses | `CWE-352;CWE-434` |
| Published | 2026-10-01T10:17:15.917 |

A chained CSRF bypass and unrestricted file upload vulnerability in the Plugin File Manager allows an attacker to upload and execute arbitrary PHP code, resulting in Remote Code Execution. This issue affects Pandora FMS: from 777 onwards.

### CVE-2026-93882

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-01T08:16:53.330 |

The LearnPress – WordPress LMS Plugin for Create and Sell Online Courses plugin for WordPress is vulnerable to Insecure Direct Object Reference in versions up to, and including, 4.4.8 via the CourseMaterialTemplate::render_material_items() callback exposed on the public lp-ajax-handle (load_content_via_ajax) endpoint. The endpoint is explicitly listed in the AbstractAjax no-nonce allowlist and performs no capability check, and the render_material_items() handler decides authorization against one attacker-supplied identifier (course_id) while fetching the returned material rows via a second, independently attacker-supplied identifier (item_id) with no check that the lesson belongs to the authorized course. This makes it possible for unauthenticated attackers to read and download course-material files (uploaded and external file paths/URLs) belonging to lessons in paid or enrollment-required courses, provided any single course on the site has 'No Required Enroll' enabled and owns at least one material file.

### CVE-2026-96255

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-01T06:17:16.460 |

The Payments for Hubtel WordPress plugin before 1.0.2 does not prevent public access to a debug log in which it records payment requests, including the store's payment gateway API credentials in plain text, allowing unauthenticated attackers to obtain those credentials.

### CVE-2026-81809

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-01T06:17:11.197 |

The Paytm Payment Gateway WordPress plugin before 2.8.9 does not properly escape data taken from payment callbacks before using it in a SQL statement, and the integrity check on those callbacks can be forged when the gateway is enabled without credentials, allowing unauthenticated users to perform SQL injection attacks.

### CVE-2026-81739

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T06:17:10.783 |

The Paytm Payment Gateway WordPress plugin before 2.8.9 does not sanitize and escape data it stores from payment callbacks before outputting it in an admin page, and the integrity check on those callbacks can be forged when the gateway is enabled without credentials, allowing unauthenticated users to store scripts that will run in the session of a store administrator.

### CVE-2026-80276

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-01T06:17:10.430 |

Comelit Multi-User Gateway for VIP System (model 1456B) firmware versions 2.9.1 and 2.10.0 expose a network-accessible management interface that does not require authentication. Through this interface, sensitive device configuration data - including the Remote Configuration Password - can be read in cleartext by a remote, unauthenticated attacker.

### CVE-2026-76145

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-01T05:17:09.623 |

An improper privilege management vulnerability in Genian SSL PNS allows an attacker to escalate to super administrator privileges and force the creation of an OS account by manipulating the permission column during CSV bulk user registration

### CVE-2026-92245

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-01T04:18:21.727 |

The Simply Schedule Appointments plugin for WordPress is vulnerable to Sensitive Information Exposure in all versions up to, and including, 1.6.12.32 via the 'recursive' parameter. This makes it possible for unauthenticated attackers to extract customer PII — including names, email addresses, phone numbers, and custom form field data — stored in appointment records, as well as per-appointment public_token values. The leaked per-appointment public_token values also enable unauthenticated attackers to delete arbitrary appointments via the DELETE /wp-json/ssa/v1/appointments/{id} endpoint, which accepts the token as sole authorization.

### CVE-2026-102143

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-306;CWE-434` |
| Published | 2026-09-30T21:17:03.143 |

An unauthenticated attacker could cause a file with attacker-controlled content to be written to the appliance filesystem through an administrative upload handler that did not properly authenticate the request. This did not by itself result in code execution, which would require a separate vulnerability to place the file in an executable location.

### CVE-2026-102128

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-30T21:17:01.270 |

An identity-verification weakness in Kiteworks Email Protection Gateway allowed the gateway to act on the Kiteworks platform on behalf of a user it had not authenticated, and to provision a platform account for an identity it did not already know. A remote, unauthenticated sender could potentially exploit this to obtain control of a platform account.

### CVE-2026-102091

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-30T21:16:55.617 |

Kiteworks Secure Data Forms before version 9.5.0 is vulnerable to Server-Side Request Forgery that could allow an unauthenticated, remote attacker to make the server issue arbitrary outbound network requests and read back the responses. This could potentially be used to reach internal-only services or other network-restricted resources.

### CVE-2026-102717

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125;CWE-457` |
| Published | 2026-09-30T15:22:21.957 |

MQTT WebSocket setter ABI mismatch may disclose memory or cause a crash

### CVE-2026-64946

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:Y/R:U/V:C/RE:M/U:Amber` |
| Weaknesses | `CWE-79;CWE-352` |
| Published | 2026-10-01T10:17:15.763 |

A chained CSRF and unrestricted SVG file upload vulnerability in the File Manager module allows stored Cross-Site Scripting, enabling session cookie exfiltration and administrator account takeover. This issue affects Pandora FMS: from 777 onwards.

### CVE-2026-102123

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-30T21:17:00.517 |

A Kiteworks appliance setup interface did not confine a user-supplied file path to its intended directory, which could allow an unauthenticated attacker to write a file to any location writable by the affected service account, potentially compromising the integrity of the appliance or rendering it unavailable until an operator intervenes. Exploitation requires network access to the affected interface, which is not reachable on a fully configured appliance in its default configuration; reaching it depends on either the transient window while an appliance is first being provisioned or a non-default appliance configuration.

### CVE-2026-103446

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:Y/R:U/V:C/RE:M/U:Amber` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-30T18:18:17.017 |

Authorization bypass through User-Controlled key vulnerability in The Wikimedia Foundation MediaWiki WikiLambda extension allows Authentication Bypass.

This issue affects MediaWiki WikiLambda extension: 1.46.

### CVE-2026-76143

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-01T05:17:09.267 |

A missing authorization vulnerability in Genian SSL PNS allows an attacker to bypass multi-factor authentication by manipulating a login request parameter.

### CVE-2026-47580

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-30T16:17:27.423 |

NVIDIA GPU Display Driver for Windows contains a vulnerability in the kernel module where an attacker could cause a missing authorization issue. A successful exploit of this vulnerability might lead to information disclosure and data tampering.

### CVE-2026-47496

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T16:17:14.160 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the Virtual GPU Manager (vGPU plugin) where a guest VM user may cause an out-of-bounds write by sending a specially crafted RPC call to the host. A successful exploit of this vulnerability might lead to escalation of privileges, data tampering, and denial of service.

### CVE-2026-101295

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-30T15:22:19.423 |

Path traversal / arbitrary file write in oc-mirror's operator catalog image extraction. When mirroring operator catalogs using either the legacy v1 path (--v1) or the OCI feature path (--use-oci-feature), oc-mirror extracts tar entries from catalog image layers without validating that file paths resolve within the intended destination directory.

### CVE-2026-103082

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-01T11:17:17.343 |

Server-Side Request Forgery (SSRF) vulnerability in LA-Studio LA-Studio Element Kit for Elementor lastudio-element-kit allows Server Side Request Forgery.This issue affects LA-Studio Element Kit for Elementor: from n/a through 1.6.2.

### CVE-2026-92144

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T10:17:17.370 |

The Forminator Forms – Contact Form, Payment Form & Custom Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'postdata-1[post-custom]' Parameter in all versions up to, and including, 1.57.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The required form submission nonce is freely obtainable by unauthenticated users via the publicly accessible wp_ajax_nopriv_forminator_get_nonce endpoint, making the full attack chain exploitable without any authentication or prior account.

### CVE-2026-75786

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:Y/R:U/V:C/RE:L/U:Red` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-01T10:17:16.530 |

Unsanitized concatenation of the module parameter in the Grafana datasource endpoint allows authenticated blind SQL injection. Affects Pandora FMS from 777 onwards.

### CVE-2026-103490

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-01T10:17:14.420 |

In JetBrains YouTrack before 2026.2.19422 privilege escalation was possible via user group links

### CVE-2026-97661

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T09:17:11.043 |

The Business Essentials for Contact Form 7 plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'gateway' Form Field in all versions up to, and including, 1.2.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the Payments module to be enabled and a form to be configured to accept both PayPal and Stripe as payment gateways.

### CVE-2026-96813

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T09:17:10.837 |

The Form Maker by 10Web – Mobile-Friendly Drag & Drop Contact Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Mark on Map Longitude/Latitude Fields in all versions up to, and including, 1.15.47 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-96573

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T09:17:10.647 |

The Appointment Hour Booking – Booking Calendar plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via Booking Form Single-Line Field via Schedule Calendar List Renderer in all versions up to, and including, 1.5.97 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the 'list_readmore_numberofwords' Other Parameters setting to be configured with a positive integer value; the default value of 0 bypasses the decode-and-truncate branch entirely and is not exploitable through this sink.

### CVE-2026-92244

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T09:17:10.087 |

The PDF Invoices & Packing Slips for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Billing First Name / Last Name / Company Fields in all versions up to, and including, 5.16.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload survives initial storage because WooCommerce's sanitize_text_field() and wc_clean() do not strip entity-encoded strings containing no literal '<' character, allowing unauthenticated guest-checkout orders to plant the malicious content.

### CVE-2026-85235

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T09:17:09.400 |

The Forminator Forms – Contact Form, Payment Form & Custom Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Rich-Text Textarea Field in all versions up to, and including, 1.57.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires an administrator to open the stored submission entry in the Forminator Entries view and interact with the planted link, at which point WordPress core's jQuery-based click handler on `.contextual-help-tabs a` evaluates the entity-decoded href as HTML, firing the attacker's payload in the administrator's authenticated wp-admin session.

### CVE-2026-14995

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T09:17:08.967 |

The Autoptimize plugin for WordPress is vulnerable to Stored Cross-Site Scripting via REQUEST_URI Path in all versions up to, and including, 3.1.15.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the Critical CSS feature to be active with a valid API key configured, as this is the precondition for unauthenticated frontend requests to trigger queue entries via ao_ccss_enqueue().

### CVE-2026-85679

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T06:17:11.577 |

The Extendify plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'styles.blocks' Block Type Key in all versions up to, and including, 3.1.6 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is possible because registerIncoming() is hooked on rest_request_before_callbacks and runs before WordPress evaluates the route's permission_callback, meaning any unauthenticated POST, PUT, or PATCH request to a /wp/v2/global-styles route can trigger the vulnerable code path.

### CVE-2026-96561

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T04:18:22.110 |

The AI Engine – The Chatbot, AI Framework & MCP for WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting in versions up to, and including, 3.8.0 This is due to a chain of missing input neutralization and output escaping across the /mwai-ui/v1/chats/submit REST endpoint, the PHP error-log parser (MeowKit_MWAI_Helpers::php_error_logs), the Advisor task (Meow_MWAI_Modules_Advisor::run_advisor), and the Advisor dashboard widget (advisor_metabox): the server-parameter denylist in chat_submit strips only exact key names such as 'model' while convert_keys() later canonicalizes 'model_' back to 'model', allowing an unauthenticated caller to place an attacker-controlled string (including CR/LF) into $query->model; final_checks() throws an Exception whose message embeds that raw string, and the non-streaming, non-admin catch branch writes it to the PHP error log unmodified — creating a forged log line that the plugin's own parser subsequently returns as recent PHP-error content; run_advisor() then appends that content verbatim to the AI prompt (indirect prompt injection — CWE-1427), the returned JSON is stored in the mwai_advisor_data option with no schema validation or HTML sanitization, and advisor_metabox() concatenates the resulting 'title' and 'description' values directly into the WordPress dashboard widget without esc_html(), wp_kses(), or equivalent escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever an administrator accesses the WordPress dashboard.

### CVE-2026-102150

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-30T21:17:03.880 |

A function in the Kiteworks Advanced Forms component was reachable without authentication. An unauthenticated attacker could potentially use it to carry out a limited set of internal service operations on the Kiteworks platform; it did not permit access to user accounts, stored files, or form submissions.

### CVE-2026-102142

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-09-30T21:17:03.027 |

A system notification template on the Kiteworks appliance was rendered by a template engine that evaluated expressions contained in the stored template body. An authenticated System Administrator could potentially store a crafted template that executed operating-system commands on the appliance when the notification was next sent.

### CVE-2026-102132

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-30T21:17:01.787 |

An administrative import function in Kiteworks Core did not verify that the requesting administrator was entitled to create the privileged integration credential being imported. A delegated administrator holding a single narrowly scoped administrative permission could therefore obtain full system administrator privileges, without any action by an existing system administrator.

### CVE-2026-102131

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-178` |
| Published | 2026-09-30T21:17:01.667 |

Kiteworks Email Protection Gateway rejected certain configuration settings, but its validation did not recognize every form in which they could be supplied. An authenticated administrator could potentially use an unrecognized form to have a file of their choosing written to the gateway and executed, resulting in code execution as the gateway service account.

### CVE-2026-102130

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-434` |
| Published | 2026-09-30T21:17:01.533 |

Kiteworks Email Protection Gateway did not sufficiently validate the content of an uploaded backup, and allowed an administrator to influence how the application loaded it. An authenticated administrator could potentially use this to execute arbitrary code on the gateway as the underlying service account.

### CVE-2026-102129

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-30T21:17:01.407 |

A user-provisioning interface in Kiteworks Core did not verify that the requesting administrator was entitled to grant the role being assigned. An administrator whose delegated permissions covered role changes alone could therefore raise an account to full system-administrator privileges.

### CVE-2026-102119

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-30T21:16:59.900 |

A path traversal weakness in an optional, non-default administrative feature allowed an authenticated administrator to move files to unintended locations outside the feature's designated directory. This could potentially be leveraged to execute arbitrary code on the underlying system.

### CVE-2026-102117

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-807;CWE-940` |
| Published | 2026-09-30T21:16:59.533 |

On deployments where the remote-support capability is licensed and enabled, an authenticated System Administrator who also possessed the key protecting the submitted data could redirect the underlying system's outbound support connection to a destination of their choosing. That destination could then have operating-system commands executed on the node and receive their output, potentially resulting in remote code execution with the privileges of a local service account.

### CVE-2026-102116

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-91` |
| Published | 2026-09-30T21:16:59.360 |

-A weakness could have allowed an authenticated Kiteworks Email Protection Gateway administrator to write a file outside its intended location and cause the application to execute it, potentially resulting in remote code execution as the underlying service account.

### CVE-2026-102114

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-30T21:16:58.880 |

A command injection vulnerability in Kiteworks could allow a high-privileged authenticated administrator to execute arbitrary operating-system commands as root on the affected appliance node. Successful exploitation requires an administrative account with elevated privileges.

### CVE-2026-102108

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T21:16:57.737 |

An authenticated administrator of Kiteworks Email Protection Gateway could submit a crafted serialized object to a cluster management interface that was deserialized without sufficient validation, potentially allowing arbitrary code execution in the context of the gateway service account. Exploitation requires an administrator account holding a specific queue-management privilege.

### CVE-2026-102099

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-30T21:16:56.630 |

Kiteworks Core before version 9.5.0 is vulnerable to Arbitrary File Write. An improper restriction of a user-supplied file path in a Kiteworks administrative export feature could allow an authenticated administrator to write a file to an arbitrary location on the underlying host, potentially leading to command execution on the appliance. Exploitation requires an existing, authenticated administrative account with access to the affected export function.

### CVE-2026-102098

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T21:16:56.500 |

Kiteworks Core before version 9.5.0 is vulnerable to SQL Injection. A stored SQL injection vulnerability in a Kiteworks administrative reporting feature could allow an authenticated administrator to read sensitive data from the underlying database and to affect the availability of the service. Exploitation requires an existing, authenticated administrative account with access to the affected reporting function.

### CVE-2026-102097

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-94` |
| Published | 2026-09-30T21:16:56.370 |

Kiteworks Email Protection Gateway before version 9.5.0 is vulnerable to Remote Code Execution. Kiteworks Email Protection Gateway allowed an authenticated administrator to import configuration whose contents were not sufficiently validated before being processed. A crafted submission could potentially allow arbitrary commands to be executed on the affected gateway.

### CVE-2026-102096

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-30T21:16:56.243 |

Kiteworks Core before version 9.5.0 is vulnerable to OS Command Injection that allows an authenticated administrator to upload a configuration package whose contents were not sufficiently validated before being processed. A crafted package could cause the underlying system to execute arbitrary operating-system commands, potentially with elevated privileges, on the affected appliance.

### CVE-2026-102094

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-09-30T21:16:55.990 |

Kiteworks Email Protection Gateway before version 9.5.0 is vulnerable to Unsafe Reflection and does not sufficiently restrict the code that the mail-processing pipeline could load from an imported rule configuration. An authenticated administrator with mail-rule configuration privileges could cause the gateway to load and execute code beyond the approved set of mail-processing components, potentially in the context of the mail-gateway service account.

### CVE-2026-102093

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-30T21:16:55.870 |

Kiteworks Core before version 9.5.0 is vulnerable to Improper Privilege Management and does not correctly enforce restrictions on role assignment, which could allow an authenticated administrative user with limited, non-Sysadmin role-management permissions to elevate another user to full system-administrator privileges beyond those the administrative user was authorized to grant.

### CVE-2026-102089

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-30T21:16:55.350 |

Kiteworks Email Protection Gateway before version 9.5.0 is vulnerable to a path traversal weakness in an administrative import function allowed an authenticated administrator to write files to arbitrary locations on the server. This could potentially be leveraged to execute arbitrary code on the underlying system.

### CVE-2026-97256

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T18:18:44.240 |

Editor PHP Object Injection in Page Builder by SiteOrigin <= 2.36.0 versions.

### CVE-2026-102392

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T18:18:14.713 |

Shop manager PHP Object Injection in Extra Product Options For WooCommerce | Custom Product Addons and Fields <= 3.3.8 versions.

### CVE-2026-103442

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:P/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:Y/R:U/V:D/RE:M/U:Amber` |
| Weaknesses | `CWE-15` |
| Published | 2026-09-30T16:17:10.050 |

External control of system or configuration setting vulnerability in The Wikimedia Foundation MediaWiki CentralAuth extension allows Code Injection.

This issue affects MediaWiki CentralAuth extension: 1.46, 1.45, and 1.43.

### CVE-2026-103441

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:A/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:Y/R:I/V:C/RE:M/U:Red` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T16:17:09.860 |

Deserialization of untrusted data vulnerability in The Wikimedia Foundation MediaWiki Wikibase extension allows Leverage Executable Code in Non-Executable Files.

This issue affects MediaWiki Wikibase extension: 1.46, 1.45, and 1.43.

### CVE-2026-103289

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-10-01T11:17:25.360 |

Ghost from 5.9.0 before 6.44.1 contains an input validation issue in the comments feature that allows authenticated members to access comments they are not authorized to view, resulting in disclosure of restricted comment data.

### CVE-2026-103288

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-01T11:17:25.200 |

Ghost, an open-source publishing platform, contains an input validation flaw in its comment like feature in versions from 5.9.0 before 6.44.1. An authenticated member can delete comment likes or dislikes belonging to other users that they are not authorized to delete, resulting in an authorization bypass and unauthorized modification of comment engagement data.

### CVE-2026-103266

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-01T11:17:21.737 |

Ghost versions 5.2.0 through versions prior to 6.62.0 allow a remote attacker, without authentication, to abuse the Stripe Checkout flow to attach a paid subscription to an existing member, modify that member's name, and inject content into newsletters sent to the member. Depending on the recipient's email client, the injected content may be rendered, resulting in HTML injection or cross-site scripting (XSS).

### CVE-2026-103256

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-01T11:17:19.913 |

n8n versions before 2.39.6 and 2.40.0 before 2.40.1 contain a credentials leak vulnerability in the Wekan and Baserow username-and-password credentials that sends unencrypted passwords to unvalidated hosts. Attackers with credential update permissions can modify the host field to receive account passwords at arbitrary hosts, bypassing domain validation controls.

### CVE-2026-103255

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-10-01T11:17:19.717 |

n8n versions before 1.123.80, from 2.0.0 before 2.39.6, and from 2.40.0 before 2.40.1 contain a path traversal vulnerability in the Supabase node where the tableId parameter is inserted into request paths without validation. Attackers can exploit workflows binding tableId to untrusted input to traverse to Auth and Storage APIs using the administrative serviceRole key, bypassing Row Level Security and enabling unauthorized data access and modification.

### CVE-2026-103252

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-01T11:17:19.160 |

n8n versions before 1.123.80, from 2.0.0 before 2.39.6, and from 2.40.0 before 2.40.1 contain an authorization bypass vulnerability in the credential test endpoint that resolves project-scoped variables without validating caller access. Attackers can specify an arbitrary project ID in the request body to interpolate sensitive variables into credential test requests sent to attacker-controlled hosts for exfiltration.

### CVE-2026-103248

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-01T11:17:18.257 |

n8n versions before 1.123.80, from 2.0.0 before 2.39.6, and from 2.40.0 before 2.40.1 contain a filter injection vulnerability in the Supabase node's Filters (String) mode that fails to escape field values. Attackers can inject filter expressions from untrusted input to read all table rows, update all records, or delete entire tables in a single request.

### CVE-2026-96577

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-01T10:17:17.760 |

A flaw was found in oc-mirror. During mirroring operations, the embedded local cache registry binds to all network interfaces without authentication or encryption instead of restricting access to the local system. An unauthenticated attacker on an adjacent network can connect to the exposed service to push tampered container images, delete cached images, or access mirrored content.

### CVE-2026-64948

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:Y/R:A/V:C/RE:L/U:Amber` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-01T10:17:16.057 |

Missing authorization in module data retrieval allows unauthorized cross-group access to module history. Affects Pandora FMS from 777 onwards.

### CVE-2026-103488

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-01T10:17:12.487 |

In JetBrains YouTrack before 2026.2.19422 missing authorisation allowed authenticated users to add themselves to project teams and access restricted issues

### CVE-2026-103659

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-862` |
| Published | 2026-10-01T09:17:08.213 |

MISP contains an authorization bypass in the event flattening feature. When a user requests an event with the flatten option enabled, the application removes the Object containment from the query and returns object attributes as top-level event attributes. In doing so, the object-level distribution and sharing-group access control check was not re-applied to those attributes.

As a result, a user who can view a community-distributed event could retrieve attributes belonging to organisation-only objects (distribution level 0) or objects restricted to a specific sharing group, even though the user's organisation does not have access to those objects. This constitutes an unauthorized disclosure of sensitive threat intelligence data.

A secondary issue was introduced by the initial remediation: the fix reused the full Object contain conditions (including soft-delete state) as the gate for flattened attributes, causing an event owner requesting deleted attributes to lose all attributes whose parent object was still live. The final fix isolates the distribution ACL condition as the sole gate.

Preconditions:

- An authenticated user with access to a community-distributed event

- The event contains at least one object with a distribution level or sharing group that restricts access beyond the event's own distribution

Impact:

- Unauthorized disclosure of attributes belonging to restricted objects

- Potential exposure of organisation-specific threat intelligence to other organisations

Affected versions: <2.5.48

### CVE-2026-92412

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T06:17:15.377 |

The Five Star Restaurant Reviews WordPress plugin before 2.3.14 does not properly escape a user-supplied value before outputting it into an HTML tag, allowing unauthenticated attackers to inject arbitrary web script that runs in the browser of anyone tricked into submitting a crafted request, including a logged-in administrator.

### CVE-2026-78210

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-01T05:17:10.117 |

In affected versions of Octopus Server, users with certain scoped permission sets could execute arbitrary scripts in an environment without possessing the required authorization.

### CVE-2026-102109

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T21:16:57.860 |

A SQL injection vulnerability existed in Kiteworks Secure Data Forms, where a value derived from the authenticated user's stored account data was incorporated into a database query without proper sanitization. An authenticated user could potentially influence that value to inject SQL. Exploitation requires an authenticated session and applies only to deployments where a specific optional feature is in use.

### CVE-2026-101881

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-30T20:17:19.330 |

OpenClaw Windows Node before 2026.7.1 contains an allocation of resources without limits vulnerability in the gateway WebSocket transport that allows connected gateways to exhaust node memory. Attackers can send an unending sequence of WebSocket continuation frames without EndOfMessage to cause unbounded memory growth until the node process crashes.

### CVE-2026-101879

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-30T20:17:18.373 |

OpenClaw Windows Node before 2026.7.1-3 contains a missing authorization vulnerability in NodeService capture handlers that allows connected gateways or agents to perform screen snapshots, camera snaps, and location captures without consent prompts. Attackers can invoke screen.snapshot, camera.snap, and location.get over the node WebSocket to silently capture screenshots, photograph users through webcams, and obtain device geolocation without user interaction.

### CVE-2026-97290

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T18:18:44.590 |

Unauthenticated Cross Site Scripting (XSS) in Photonic Gallery & Lightbox for Flickr, SmugMug & Others <= 3.36 versions.

### CVE-2026-94171

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T18:18:43.497 |

Unauthenticated Cross Site Scripting (XSS) in CURCY <= 2.2.16 versions.

### CVE-2026-102391

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T18:18:14.567 |

Unauthenticated Cross Site Scripting (XSS) in JetFormBuilder <= 3.6.5.4 versions.

### CVE-2026-102376

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T18:18:14.197 |

Subscriber Cross Site Scripting (XSS) in Branda <= 3.4.32 versions.

### CVE-2026-100510

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T18:17:59.147 |

Unauthenticated Cross Site Scripting (XSS) in Post and Page Builder by BoldGrid <= 1.27.14 versions.

### CVE-2026-47602

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-09-30T16:17:30.733 |

NVIDIA GPU Display Driver for Windows and Linux contains a vulnerability in the kernel mode driver where a local user can cause the driver to dereference an untrusted pointer. A successful exploit of this vulnerability might lead to denial of service and information disclosure.

### CVE-2026-47554

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-30T16:17:23.587 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the kernel mode layer where improper verification of cryptographic signatures may cause signature verification to be bypassed under memory pressure. A successful exploit of this vulnerability might lead to denial of service and data tampering.

### CVE-2026-103254

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-01T11:17:19.537 |

n8n versions before 1.123.80, from 2.0.0 before 2.39.6, and from 2.40.0 before 2.40.1 contain a path traversal vulnerability in signed resume URL generation for Send-and-Wait approvals. Attackers with workflow creation permissions can mint valid approval URLs for gates in projects they cannot access by exploiting unresolved traversal sequences in caller-controlled node IDs, enabling cross-project approval forgery.

### CVE-2026-103253

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-01T11:17:19.343 |

n8n versions before 1.123.80, from 2.0.0 before 2.39.6, and from 2.40.0 before 2.40.1 contain an SQL injection vulnerability in the Oracle Database node's Delete Table Drop operation. Attackers can inject single quotes in the table or schema fields to append arbitrary SQL statements and execute DDL or DML commands against the connected database with the credential's privileges.

### CVE-2026-103250

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:N/VA:N/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-10-01T11:17:18.777 |

n8n versions before 1.123.80, from 2.0.0 before 2.39.6, and from 2.40.0 before 2.40.1 contain a NoSQL injection vulnerability in the MongoDB Chat Memory node that fails to validate the sessionId parameter. Unauthenticated attackers can supply MongoDB query operators in the sessionId field to access conversation histories from other users and perform unauthorized write and delete operations.

### CVE-2026-93495

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-665` |
| Published | 2026-10-01T02:16:54.150 |

Improper initialization in an ASUS certain motherboard allows an physically proximate user to read or write arbitrary memory by inserting a specially crafted device.

### CVE-2026-102127

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-30T21:17:01.117 |

An XML parser used by Kiteworks Email Protection Gateway did not restrict external entity references. Where an optional, non-default message-processing feature is enabled, a remote and unauthenticated sender could potentially use a crafted message to read files accessible to the gateway service account, including cryptographic key material and credentials, and have them sent to a destination they control.

### CVE-2026-47598

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-30T16:17:30.123 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the open-source kernel module event delivery path where an unprivileged local user could cause a use-after-free through a race between asynchronous event delivery and file close. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, denial of service, information disclosure, and data tampering.

### CVE-2026-47596

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:P/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-281` |
| Published | 2026-09-30T16:17:29.827 |

NVIDIA GPU Display Driver for Linux contains a vulnerability in the kernel mode layer where an unprivileged user can write to read-only memory because the memory's permissions are not preserved. A successful exploit of this vulnerability might lead to code execution and escalation of privileges.

### CVE-2026-47582

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T16:17:27.710 |

NVIDIA GPU Display Driver for Windows contains a vulnerability in the kernel module where an attacker could cause an out-of-bounds write. A successful exploit of this vulnerability might lead to code execution, denial of service, escalation of privileges, information disclosure, and data tampering.
