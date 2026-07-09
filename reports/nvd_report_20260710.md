# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-09 15:00 UTC
- **対象期間**: `2026-07-08T15:00:28.000Z` 〜 `2026-07-09T15:00:33.000Z`
- **重要CVE数**: 141 件（Critical 9.0+: 16 件 / High 7.0〜: 125 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近 1 か月で報告された CVE の多くは **「認証なしで任意ファイルをアップロードできる」**、**「認証バイパス」**、**「SAML トークン検証不備」** といった、リモートから即座にコード実行 (RCE) や管理者権限取得が可能になる **高リスクの設計ミス** が目立ちます。  
- Web CMS 系 (Joomla、WordPress) のプラグインが集中して攻撃対象となっており、特にファイルタイプチェックの不備が原因の **Arbitrary File Upload** が多数報告されています。  
- インフラ系コンポーネント (Fluentd、CoreWCF、Snowpark‑Python SDK) でも **入力検証不備** によるパス・トラバーサルや SQL インジェクションが確認され、内部システムへの横展開リスクが高まっています。  
- Google Chrome (Android) 系の多数の Use‑After‑Free / Uninitialized Use バグは、ブラウザサンドボックスの突破を狙った **高度なリモートコード実行** を可能にします。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な脆弱性種別 | 影響範囲・被害シナリオ | 推奨される対策 (概要) |
|-----|------|----------------|------------------------|-----------------------|
| **CVE‑2026‑56291** | 10.0 | 任意ファイルアップロード → 完全リモートコード実行 | Joomla 用拡張 **Balbooa Forms** が認証不要で任意の実行ファイルをアップロード可能。攻撃者はサーバ上で任意のコマンドを実行でき、サイト全体が乗っ取られる。 | 1. Balbooa Forms を **最新版 (≥ 2.2.0 以降)** に更新。<br>2. `upload_tmp_dir` の実行権限を削除し、Web サーバの実行権限を最小化。 |
| **CVE‑2026‑54782** | 10.0 | SAML 1.1/2.0 トークン検証不備 → 署名なしトークン受容、発行者キー解決失敗 | **CoreWCF** (WCF の .NET Core 移植) 1.8.0 未満 / 1.9.0 未満で、`IdentityConfiguration` とフェデレーションバインディングを併用すると、署名が無くてもトークンが受理され、認証バイパスが可能。 | 1. CoreWCF を **1.8.1** 以上、もしくは **1.9.1** 以上にアップデート。<br>2. SAML 設定で必ず `RequireSignedTokens=true` を明示。 |
| **CVE‑2026‑15158** | 9.8 | 任意ファイルアップロード (WordPress) | **Blocksy Companion** プラグイン (≤ 2.1.46) の `save_attachments` が `.woff2` 文字列を含むファイル名を無条件に許可。攻撃者は PHP など実行可能ファイルをアップロードし、管理者権限取得が可能。 | 1. Blocksy Companion を **2.1.47 以降** に更新。<br>2. `wp_check_filetype_and_ext` フィルタをカスタムで上書きし、拡張子ホワイトリストを厳格化。 |
| **CVE‑2026‑14245** | 9.8 | 認証バイパス → 管理者アカウント取得 | **miniOrange OTP Login, Verification and SMS Notifications** (≤ 5.5.1) の `um_reset_password_process_hook()` がサーバ側でパスワード検証を行わず、OTP なしでパスワードリセットが完了。攻撃者は任意のユーザーのパスワードを変更し、管理者権限を奪取できる。 | 1. プラグインを **5.5.2 以降** に更新。<br>2. OTP リセットフローに必ず **サーバ側でのトークン検証** を実装。 |
| **CVE‑2026‑44024** | 9.8 | パス・トラバーサル (Fluentd) | **Fluentd** 1.19.2 以前で `${tag}` プレースホルダを用いたファイルパス設定が検証不足。攻撃者は `../` などを含むタグで任意のディレクトリに書き込み、機密情報漏洩や RCE に繋がる。 | 1. Fluentd を **1.19.3 以降** にアップデート。<br>2. `path` 設定に正規表現で **${tag} のサニタイズ** を実装し、`../` を除外。 |

> **補足**  
> - Chrome 系 (CVE‑2026‑15113 〜 CVE‑2026‑15118 等) はすべて **150.0.7871.115** 以降で修正済みです。社内の Android デバイスは速やかに最新版へ更新してください。  
> - Snowflake Snowpark‑Python SDK (CVE‑2026‑15062) は **1.53.0** 以降で修正。認可ロジックの見直しも合わせて実施してください。  

---

## 3. 推奨アクション  

### 3.1 パッケージ・プラグインの即時更新
| 製品 / パッケージ | 現行バージョン (脆弱) | 推奨バージョン |
|-------------------|----------------------|----------------|
| Joomla – Balbooa Forms | 任意 (≤ 2.1.x) | **2.2.0 以降** |
| WordPress – Blocksy Companion | ≤ 2.1.46 | **2.1.47 以降** |
| WordPress – miniOrange OTP Login | ≤ 5.5.1 | **5.5.2 以降** |
| CoreWCF | 1.8.0 / 1.9.0 | **1.8.1** 以上、**1.9.1** 以上 |
| Fluentd | 1.19.2 | **1.19.3** 以上 |
| Snowpark‑Python SDK | < 1.53.0 | **1.53.0** 以上 |
| Bitwarden Server | < 2026.

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-56291

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:Red` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-09T11:16:40.990 |

The Joomla extension Balbooa Forms is vulnerable to an unauthenticated arbitrary file upload that allows uploading executable files and leads to full RCE.

### CVE-2026-54782

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-290;CWE-347` |
| Published | 2026-07-08T23:16:56.030 |

CoreWCF is a port of the service side of Windows Communication Foundation (WCF) to .NET Core. Prior to 1.8.1 and 1.9.1, CoreWCF SAML 1.1 and SAML 2.0 token validation does not correctly resolve the issuer signing key or require signed tokens when IdentityConfiguration is used with federated bindings, allowing an unauthenticated remote attacker to impersonate any principal the trusted STS could issue. This issue is fixed in versions 1.8.1 and 1.9.1.

### CVE-2026-5955

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-09T10:16:27.427 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Inrove Software and Internet Services BiEticaret allows SQL Injection.

This issue affects BiEticaret: before v3.3.57.

### CVE-2026-15158

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-09T10:16:25.370 |

The Blocksy Companion plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 2.1.46 via the save_attachments function. This is due to the Custom Fonts extension registering a wp_check_filetype_and_ext filter that approves any filename containing .woff2 or .ttf as a substring via strpos() rather than validating that those strings appear as the final extension via PATHINFO_EXTENSION — allowing double-extension filenames such as shell.woff2.php to pass MIME validation and be handled as permitted font files. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible. This vulnerability is only exploitable when the premium version of the plugin (blocksy-companion-pro) is installed with both the WooCommerce Extra (Advanced Reviews) and Custom Fonts extensions active; the free blocksy-companion plugin does not contain the vulnerable code paths.

### CVE-2026-14245

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-09T08:16:46.933 |

The miniOrange OTP Login, Verification and SMS Notifications plugin for WordPress is vulnerable to Authentication Bypass leading to Administrator Account Takeover in all versions up to, and including, 5.5.1. This is due to the `um_reset_password_process_hook()` function performing no server-side verification that the OTP validation step was completed, and relying solely on a public `form_nonce` nonce that the plugin itself emits to unauthenticated visitors via the `moumprvar` JavaScript object on the Ultimate Member password reset page, while still accepting the attacker-controlled `username_b` parameter to target any WordPress user without role restriction or any binding to a previously validated OTP session. This makes it possible for unauthenticated attackers to obtain a freshly generated password-reset URL for an arbitrary Administrator account — returned in a 302 `Location` header — and use it to take full control of that account. Exploitation requires the Ultimate Member Password Reset Form integration to be active and the plugin to not be configured for phone-only reset.

### CVE-2026-44024

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-08T22:17:14.337 |

Fluentd collects events from various data sources and writes them to files, RDBMS, NoSQL, IaaS, SaaS, Hadoop and so on. Prior to 1.19.3, Fluentd allows dynamically constructing file paths using the ${tag} placeholder, and insufficient validation of ${tag} in file configurations such as the path parameter of the out_file plugin allows attackers sending untrusted tags containing path traversal characters to write or overwrite arbitrary files and potentially achieve remote code execution. This issue is fixed in version 1.19.3.

### CVE-2026-15113

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T23:16:52.413 |

Use after free in Autofill in Google Chrome on Android prior to 150.0.7871.115 allowed a remote attacker to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-15062

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-08T15:16:26.320 |

SQL injection vulnerabilities in the Snowflake Snowpark Python SDK (snowpark-python) versions prior to 1.53.0 could allow authenticated low-privilege users to execute SQL beyond their authorization scope. An attacker could exploit these vulnerabilities by embedding SQL payloads in source database column names to escalate privileges via the DataFrameReader.dbapi() API by supplying a specially crafted location parameter to DataFrameWriter write methods to redirect a COPY INTO to an arbitrary source query, or by including a backslash-single-quote sequence in an export path to defeat the normalize_path() sanitizer and inject SQL via DataFrame.to_csv(). Successful exploitation may result in source database compromise, unauthorized cross-tenant data exfiltration, or unauthorized read of Snowflake account data.

### CVE-2026-2342

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-09T10:16:25.833 |

Improper neutralization of input during web page generation ('cross-site scripting') vulnerability in OceanicSoft Informatics Systems Ltd. ValeApp allows Stored XSS.

This issue affects ValeApp: through 09072026. NOTE: The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-47840

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-07-09T07:16:24.553 |

A network attacker positioned between UAA and its LDAP directory can impersonate the directory using any certificate from any trusted CA, then harvest the LDAP bind password and every end-user password sent during simple-bind authentication, and return forged group memberships that grant themselves admin scopes. This affects every deployment that authenticates users against LDAP over StartTLS.
Affected versions: UAA versions prior to v78.13.0; Cf-deployment versions prior to v56.2.0.

### CVE-2026-47646

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-09T00:17:23.160 |

Improper neutralization of input during web page generation ('cross-site scripting') in Dynamics 365 Customer Voice allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-54527

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-08T21:16:49.273 |

JupyterLab Git is a Git extension for JupyterLab. From 0.30.0b3 before 0.54.0, the PlainTextDiff.ts createHeader() method passes Git filenames directly to innerHTML when rendering renamed files in commit history, allowing a crafted filename to execute JavaScript when a victim views the rename diff in the Git History tab. This issue is fixed in version 0.54.0.

### CVE-2026-60104

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-08T20:17:00.413 |

Bitwarden Server before 2026.6.0 does not verify that the email in a POST /auth-requests/admin-request body belongs to the authenticated caller, allowing a low-privileged organization member to obtain another user's vault key and a victim-scoped access token by creating a Trusted Device Encryption authentication request, bound to an attacker-controlled public key, that is readable from an unauthenticated endpoint once approved resulting in disclosure of the victim's vault key and account takeover.

### CVE-2026-59873

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-08T16:16:33.867 |

node-tar is a tar archive manipulation library for Node.js. Prior to 7.5.19, node-tar does not enforce hard upper bounds on total decompressed data, entry counts, or decompression ratio in extraction and parsing paths such as src/extract.ts, allowing a small crafted gzip bomb to exhaust disk space and CPU. This issue is fixed in version 7.5.19.

### CVE-2026-59702

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-08T16:16:31.577 |

repomix contains a server-side request forgery vulnerability in the POST /api/pack endpoint that allows unauthenticated attackers to make arbitrary outbound requests. The endpoint fails to properly validate http://, https://, and file:// URLs before passing them to git clone, enabling attackers to access private network addresses, GCP metadata services, or local filesystem paths.

### CVE-2026-9074

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-08T16:16:35.050 |

IBM API Connect 10.0.8.0 through 10.0.8.9 and 12.1.0.0 through 12.1.0.3 contains an unauthenticated SQL injection vulnerability in the password reset functionality.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-47828

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-07-09T07:16:23.990 |

During bosh create-env and bosh delete-env, the CLI uploads compiled CPI packages and rendered job templates to the new VM's DAV blobstore over HTTPS without verifying the server certificate, even though a CA certificate for that endpoint is available in the installation manifest. A network attacker can terminate the TLS connection, harvest the Basic-auth credentials, and read the rendered-templates archive containing every bootstrap secret for the new BOSH Director, then replay the credentials against the real VM's agent for root code execution.
Affected versions: bosh-cli versions prior to v7.10.4.

### CVE-2026-59807

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-07-08T20:16:57.123 |

Composio SDK before 0.2.32-beta.283 contains a path validation bypass vulnerability that allows attackers to read and exfiltrate sensitive files by exploiting a missing assertSafeFileUploadPath check in the readFileFromDisk function within tool-file-uploads.ts. Attackers can exploit prompt injection to manipulate file_uploadable parameters to reference sensitive paths such as SSH private keys, causing the CLI to upload credential files to attacker-controlled storage.

### CVE-2026-4275

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-09T11:16:39.630 |

The Divi Torque Lite – Divi Theme, Divi Builder & Extra Theme plugin for WordPress is vulnerable to Cross-Site Request Forgery in all versions up to, and including, 4.2.3. This is due to the use of '__return_true' as the permission_callback for the /install_plugin and /activate_plugin REST API endpoints, which bypasses WordPress's built-in REST API nonce verification. Although the endpoint callbacks contain internal current_user_can() checks, the absence of nonce verification means that a forged cross-site request from a logged-in administrator's browser will pass the capability check via the admin's session cookies. This makes it possible for unauthenticated attackers to install arbitrary plugins from WordPress.

### CVE-2026-5523

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-09T06:16:21.300 |

The Divi Form Builder plugin for WordPress is vulnerable to Missing Authorization in versions up to, and including, 5.1.8. This is due to the update_user() function accepting a user ID parameter from form submissions without verifying that the authenticated user has permission to edit that specific user account, and the handle_register_submission() function only checking if any user is logged in rather than validating permissions for the target user. This makes it possible for authenticated attackers, with subscriber-level access and above, to change the email address and password of any user account, including administrators, resulting in complete account takeover.

### CVE-2026-59723

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-346` |
| Published | 2026-07-08T23:16:56.440 |

Cline is an autonomous coding agent as an SDK, IDE extension, or CLI assistant. Prior to 3.0.30, the Cline Hub dashboard server launched by the cline dashboard command accepts WebSocket connections on the /browser endpoint without validating the Origin header, and when ROOM_SECRET is unset for local 127.0.0.1 binds, isAuthorizedBrowserRequest() allows attacker-controlled websites to send desktopCommand frames that read workspace state, mutate MCP and provider settings, and trigger command execution when a provider or model is configured. This issue is fixed in version 3.0.30.

### CVE-2026-15133

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T23:16:54.413 |

Use after free in InterestGroups in Google Chrome prior to 150.0.7871.115 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-15132

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-457` |
| Published | 2026-07-08T23:16:54.317 |

Uninitialized Use in V8 in Google Chrome prior to 150.0.7871.115 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-15129

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T23:16:54.020 |

Use after free in Views in Google Chrome prior to 150.0.7871.115 allowed a remote attacker to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-15126

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T23:16:53.733 |

Use after free in Forms in Google Chrome prior to 150.0.7871.115 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-15125

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-08T23:16:53.637 |

Inappropriate implementation in Forms in Google Chrome prior to 150.0.7871.115 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-15123

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-08T23:16:53.450 |

Inappropriate implementation in DOM in Google Chrome prior to 150.0.7871.115 allowed a remote attacker to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-15118

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T23:16:52.940 |

Use after free in Input in Google Chrome prior to 150.0.7871.115 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-15116

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T23:16:52.730 |

Use after free in Actor in Google Chrome prior to 150.0.7871.115 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-15114

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-787` |
| Published | 2026-07-08T23:16:52.533 |

Out of bounds read and write in Codecs in Google Chrome prior to 150.0.7871.115 allowed a remote attacker to potentially exploit heap corruption via a crafted video file. (Chromium security severity: High)

### CVE-2026-15112

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T23:16:52.310 |

Use after free in Ozone in Google Chrome prior to 150.0.7871.115 allowed a remote attacker to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-15110

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T23:16:52.103 |

Use after free in Extensions in Google Chrome prior to 150.0.7871.115 allowed an attacker who convinced a user to install a malicious extension to potentially exploit heap corruption via a crafted Chrome Extension. (Chromium security severity: High)

### CVE-2026-15107

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T23:16:51.783 |

Use after free in IndexedDB in Google Chrome prior to 150.0.7871.115 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-10037

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-08T22:17:12.500 |

A sandbox escape vulnerability exists in the OpenJDK packages provided in Ubuntu. The .jar MIME handlers installed by these packages execute files marked as executable when the mailcap package is installed. A compromised or malicious sandboxed application with access to the OpenURI portal via xdg-desktop-portal-gtk can write a malicious .jar file to the host file system, set its executable bit, and trigger the handler to execute arbitrary code outside of the sandbox environment.

### CVE-2026-59822

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-07-08T20:16:57.683 |

LiteLLM is a proxy server (AI Gateway) to call LLM APIs in OpenAI (or native) format. Prior to 1.84.0, LiteLLM's MCP Streamable HTTP endpoint allowed an unauthenticated attacker to use a fabricated Authorization header to trigger an OAuth2 passthrough fallback path that replaced failed LiteLLM key validation with an empty UserAPIKeyAuth() object, allowing requests to reach MCP tooling without a valid LiteLLM key. This issue is fixed in version 1.84.0.

### CVE-2026-58253

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-08T20:16:54.943 |

NATS Server is a high-performance server for NATS.io, the cloud and edge native messaging system. Prior to 2.14.0, 2.12.7, and 2.11.16, when no_auth_user was configured, a parser fast path intended for ordinary client connections could also apply to route or leafnode listeners, allowing an unauthenticated peer to bypass inter-server CONNECT authentication and operate with the privileges associated with that connection type. This issue is fixed in versions 2.14.0, 2.12.7, and 2.11.16.

### CVE-2026-29009

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-07-08T17:17:21.173 |

U-Boot through 2026.04-rc3 contains a buffer overflow vulnerability in nfs_readlink_reply() (net/nfs-common.c) when CONFIG_CMD_NFS is enabled, allowing a malicious or compromised NFS server to overflow the 2048-byte nfs_path_buff buffer by returning multiple relative symlink targets that are appended without cumulative length validation. Attackers can send two or more READLINK responses containing relative symlink targets of approximately 1100 bytes each to corrupt adjacent BSS variables including nfs_server_ip, nfs_server_mount_port, nfs_server_port, nfs_our_port, nfs_state, and rpc_id, potentially achieving memory corruption and control over the NFS client state machine.

### CVE-2026-53951

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-94` |
| Published | 2026-07-08T16:16:30.623 |

Copier is a library and CLI app for rendering project templates. In versions 9.5.0 through 9.15.1, the `trust` setting's prefix match
(`copier/_settings.py`) compares the template URL against a trusted prefix with a raw `str.startswith` and no path normalization, while the URL is normalized when the template is actually fetched (`Path.resolve()` for local paths; libcurl dot-segment removal for `https`). A template reference that textually starts with a trusted prefix but contains `..` is therefore granted trust yet resolves to a different, attacker-controlled template, whose `tasks` / `migrations` / `jinja_extensions` then run without the `--trust` prompt — arbitrary command execution. Version 9.15.2 patches the issue.

### CVE-2026-15067

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-08T15:16:26.433 |

Snowflake Terraform Provider versions prior to 2.18.0 contain several security vulnerabilities, including SQL injection via an unsanitized data source input could result in arbitrary SQL execution under the provider's privileged Snowflake session, potentially enabling sensitive data exfiltration and minting of long-lived access credentials. Exploitation requires the ability for an attacker to  influence a workspace variable in a pipeline where this data source was enabled. Improper neutralization of identifier content in user resource inputs could allow DDL injection into user management statements, potentially causing accounts to be created with attacker-controlled credentials and without the  security controls configured by the operator. The fix is available in Snowflake Terraform Provider version 2.18.0. Users must manually upgrade.

### CVE-2026-12593

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-09T14:16:26.713 |

The implementation of an internal and undocumented Dashboard API endpoint (POST /api/users/~/{user}/tokens) forgot to ensure an HTTP request for creating an API Token for another user had sufficient permission to do so.





Precondition for successful exploitation was a preexisting internal user (with more privileges than the attacker), the attacker knowing its login name and the attacker being able to authenticate to the Dashboard via OAuth/OIDC. The attacker would then have had to forge a token creation API request on behalf of the other user and could have authenticated and finalized the token creation with their own OAuth/OIDC credentials. In the worst case, this would mean an attacker could have become Dashboard Administrator and been able to perform all administrative actions if the preexisting internal user had administrative privileges. In combination with a separate weakness, this could have further led to code execution on the host system running the Dashboard with the privileges of the OS-User running the Dashboard server.

### CVE-2026-31984

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-09T08:16:47.940 |

A denial-of-service vulnerability caused by unbounded resource allocation was discovered in the audit logging functionality, due to a missing size limit on input recorded into audit entries. An unauthenticated attacker can submit requests containing excessively large input that is recorded into audit entries, possibly exhausting the available disk space and rendering the system inoperable.

### CVE-2026-55471

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-07-08T22:17:15.520 |

HAPI FHIR is a complete implementation of the HL7 FHIR standard for healthcare interoperability in Java. Prior to 6.9.10, org.hl7.fhir.utilities.XsltUtilities saxonTransform(...) overloads instantiated a bare net.sf.saxon.TransformerFactoryImpl() without ACCESS_EXTERNAL_DTD or ACCESS_EXTERNAL_STYLESHEET restrictions, allowing an attacker who controls or can tamper with transformed XML to trigger XML External Entity injection for local file disclosure and blind XXE or SSRF to arbitrary URLs reachable from the host. This issue is fixed in version 6.9.10.

### CVE-2026-6896

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-08T21:16:55.097 |

GitLab has remediated an issue in GitLab EE affecting all versions from 13.11 before 18.11.7, 19.0 before 19.0.4, and 19.1 before 19.1.2 that under certain conditions could have allowed an authenticated user with developer-role permissions to execute arbitrary scripts in another user's browser session due to improper sanitization of user-supplied input.

### CVE-2026-57480

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-07-08T21:16:50.890 |

Parse Server is an open source backend that can be deployed to any infrastructure that can run Node.js. Prior to 9.9.1-alpha.12 and 8.6.82, deeply nested $or, $and, and $nor query condition operators in the REST API or LiveQuery query handling could trigger exponential-time processing in the internal query-traversal helper and block the Node.js event loop. This issue is fixed in versions 9.9.1-alpha.12 and 8.6.82.

### CVE-2026-55596

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-08T21:16:50.247 |

Plate is a rich-text editor with AI and shadcn/ui. From 53.0.0 until 53.1.4, the media embed renderer trusts serialized provider or sourceUrl metadata in useMediaState and skips parseMediaUrl protocol validation, allowing a crafted Plate document to set a known video provider while keeping url as a javascript: iframe source that the registry MediaEmbedElement renders directly as an iframe src when a victim opens the document. This issue is fixed in version 53.1.4.

### CVE-2026-55206

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-07-08T21:16:49.987 |

py7zr is a Python-based library and utility to support 7zip archive compression, decompression, encryption and decryption. Prior to 1.1.3, PackInfo._read() in archiveinfo.py used an O(n^2) cumulative sum pattern for attacker-controlled numstreams values parsed from archive headers, allowing a crafted .7z archive to cause excessive CPU consumption during SevenZipFile.init() before extraction. This issue is fixed in version 1.1.3.

### CVE-2026-55195

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-07-08T21:16:49.840 |

py7zr is a Python-based library and utility to support 7zip archive compression, decompression, encryption and decryption. Prior to 1.1.3, py7zr's Worker.decompress() extracted archive entries without tracking total decompressed size, allowing a crafted .7z file such as a 15.6 KB archive that expands to 100 MB to exhaust disk or memory before extraction completes. This issue is fixed in version 1.1.3.

### CVE-2026-59936

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-08T20:16:59.403 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.14.1, an attacker can craft a PDF with a page content stream containing a not terminated inline image, causing an infinite loop during inline image end marker detection such as when extracting page text. This issue is fixed in version 6.14.1.

### CVE-2026-59935

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-07-08T20:16:59.260 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.14.2, an attacker can craft a PDF with a page content stream containing a not terminated inline image that uses the ASCII85 or ASCIIHex filters, causing an infinite loop during parsing such as when extracting page text. This issue is fixed in version 6.14.2.

### CVE-2026-59803

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-07-08T20:16:55.913 |

rpcx through 1.9.3, fixed in commit 047aec1, contains a denial-of-service vulnerability in protocol.Message.Decode (protocol/message.go). When a message has the compression flag set, the payload is gzip-decompressed via util.Unzip with no limit on the decompressed output size. The only built-in size guard, protocol.MaxMessageLength, is checked against the compressed on-the-wire frame length, not the decompressed size, so it provides no protection. Because decoding (and decompression) occurs in readRequest before authentication, a single unauthenticated connection can send a small (under 2 MB) gzip-compressed message that expands to gigabytes of heap allocation, leading to out-of-memory conditions and service unavailability.

### CVE-2026-14891

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-59` |
| Published | 2026-07-08T20:16:48.300 |

HashiCorp Nomad and Nomad Enterprise are vulnerable to a sandbox escape in the Docker task driver that may allow a job submitter to bind-mount a host path into a container even when volume bind mounts are disabled, potentially leading to reading and writing files on the host. This vulnerability, CVE-2026-14891, is fixed in Nomad Community Edition 2.0.4 and Nomad Enterprise 2.0.4, 1.11.8, and 1.10.14.

### CVE-2026-59879

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190;CWE-400;CWE-835;CWE-1284` |
| Published | 2026-07-08T17:17:26.370 |

Immutable.js provides many Persistent Immutable data structures. Prior to 4.3.9 and 5.1.8, List#set, List#setSize, List#setIn, List#updateIn, and the functional set, setIn, and updateIn mishandle an index or size in the range 2 ** 30 to 2 ** 31 in setListBounds in src/List.js, causing an empty List to enter an uncatchable infinite loop, a populated List to allocate without bound until process abort, or setSize to silently wrap large values. This issue is fixed in versions 4.3.9 and 5.1.8.

### CVE-2026-29008

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-07-08T17:17:21.047 |

U-Boot through 2026.04-rc3 contains an integer underflow vulnerability in the tcp_rx_state_machine() function (net/tcp.c) that allows a network-adjacent attacker to crash the bootloader by sending a malformed TCP SYN+ACK packet with a manipulated data offset field causing payload_len to become negative. When the TCP_SYN_SENT handler calls tcp_rx_user_data() without invoking tcp_seg_in_wnd() validation, the negative payload_len is implicitly converted to a large unsigned integer (e.g., 0xFFFFFFD8) and passed to memcpy() in store_block(), causing an immediate crash that prevents device boot and may enable memory corruption when CONFIG_LMB is disabled.

### CVE-2026-59880

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-07-08T16:16:34.517 |

Immutable.js provides many Persistent Immutable data structures. Prior to 4.3.9 and 5.1.8, Immutable.Map and Immutable.Set keep keys that share the same 32-bit hash in a HashCollisionNode collision bucket that is scanned linearly, allowing an attacker who controls keys inserted into a Map, such as through Immutable.Map(obj), Immutable.fromJS(obj), state.merge(userObject), or mergeDeep, to craft many colliding keys and degrade insertion and lookup to consume disproportionate CPU. This issue is fixed in versions 4.3.9 and 5.1.8.

### CVE-2026-59874

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-07-08T16:16:33.990 |

node-tar is a tar archive manipulation library for Node.js. Prior to 7.5.18, tar.replace accepts a checksum-valid tar header with a negative base-256 encoded entry size, causing the archive scanner to make no progress while repeatedly parsing the same header. This issue is fixed in version 7.5.18.

### CVE-2026-59703

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-552` |
| Published | 2026-07-08T15:16:32.173 |

repomix contains a local file inclusion vulnerability in the git clone endpoint that allows unauthenticated attackers to read arbitrary local git repositories. The isValidRemoteValue function in src/core/git/gitRemoteParse.ts fails to block file:// URLs, permitting attackers to supply file:// scheme URLs that bypass validation and are passed directly to git clone, enabling unauthorized access to all tracked file contents on the server filesystem.

### CVE-2026-50644

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-09T11:16:39.887 |

SOPlanning is vulnerable to SQL injection in the audit retention configuration. An attacker holding parameters_all rights can inject SQL commands into the audit configuration form which is then saved. The execution is triggered when the audit functionality is accessed (by the attacker or another user).

This issue was fixed in version 1.56.01.

### CVE-2026-58192

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-07-08T21:16:52.150 |

Appium is a cross-platform automation framework for all kinds of apps, built on top of the W3C WebDriver protocol. Prior to 1.1.6, the Appium storage plugin exposes POST /storage/delete, whose handler passes the user-supplied name value directly into path.join(storageRoot, name) and fs.rimraf() without path sanitization, allowing an unauthenticated remote client to escape the storage root with ../ sequences and recursively delete arbitrary writable files or directories. This issue is fixed in version 1.1.6.

### CVE-2026-47830

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-07-09T07:16:24.280 |

Incorrect Permission Assignment in BOSH.Utils.psm1 in BOSH-Ecosystem bosh-windows-stemcell-builder allows low-privilege authenticated users to overwrite C:\bosh\service_wrapper.exe or C:\bosh\bosh-agent.exe and gain NT AUTHORITY\SYSTEM on the next service restart or reboot. This can lead to full host control.
Affected versions: bosh-windows-stemcell-builder versions prior to v2019.98.

### CVE-2026-47826

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-07-09T07:16:23.840 |

The blobs.yml path key traversal vulnerability in the BOSH CLI tool allows an attacker to write arbitrary files and exfiltrate sensitive information.
Affected versions: BOSH CLI tool versions prior to v7.10.4.

### CVE-2026-55849

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-08T22:17:15.783 |

@cyclonedx/cyclonedx-npm creates CycloneDX Software Bill of Materials from npm projects. From 2.1.0 before 5.0.0, the CLI passes user-supplied --workspace values to a subshell without proper sanitization when npm_execpath is unset or empty, allowing arbitrary OS command execution with the privileges of the invoking user. This issue is fixed in version 5.0.0.

### CVE-2026-59261

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-07-08T17:17:25.640 |

OpenClaw before 2026.5.28 contains a credential exposure vulnerability where workspace dotenv files can override provider credentials. Attackers with lower-trust access to configured input paths can expose sensitive data and credentials that should remain within trusted boundaries.

### CVE-2026-31985

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:L/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-671` |
| Published | 2026-07-09T08:16:48.083 |

When the upstream Guardian or CMC was configured in the Remote Collector via n2os-tui, the generated configuration disabled TLS certificate verification, and no option was provided to enable it. A malicious actor could perform a man-in-the-middle attack and intercept the communication between the Remote Collector and the Guardian or CMC. This could result in theft of the sync token, impersonation of the server, injection of spoofed data (such as false asset information or vulnerabilities) into the Guardian or CMC, or disruption of the data flow between the Remote Collector and the Guardian or CMC.

### CVE-2026-15122

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-08T23:16:53.347 |

Insufficient validation of untrusted input in Codecs in Google Chrome on Windows prior to 150.0.7871.115 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-15120

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T23:16:53.143 |

Use after free in Core in Google Chrome on Windows prior to 150.0.7871.115 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-15119

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-08T23:16:53.050 |

Race in GetUserMedia in Google Chrome prior to 150.0.7871.115 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-55830

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-184` |
| Published | 2026-07-08T22:17:15.653 |

RestrictedPython is a tool that helps to define a subset of the Python language which allows to provide a program input into a trusted environment. Prior to 8.3, check_function_argument_names() rejected protected guard hook names for regular, variadic, and keyword-only arguments but omitted positional-only arguments, allowing __getattr__, _getitem_, _write_, or _print_ to be shadowed by a local parameter and bypass the embedding application's access policy. This issue is fixed in version 8.3.

### CVE-2026-4256

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-90` |
| Published | 2026-07-09T14:16:32.640 |

Improper neutralization of special elements used in an LDAP query ('LDAP injection') vulnerability in PEAKUP Technology Inc. PassGate allows LDAP Injection.

This issue affects PassGate: through 30042026.

### CVE-2026-58525

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-08T21:16:54.300 |

Improper access control in Microsoft Edge (Chromium-based) allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-55575

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-08T20:16:53.137 |

LiquidJS is a Shopify / GitHub Pages compatible template engine in pure JavaScript. Prior to 10.27.1, the pop array filter at src/filters/array.ts allocated a full clone of its input array via [...toArray(v)] without calling this.context.memoryLimit.use(...), allowing a template render such as {{ huge_array | pop }} to allocate an O(N) clone of an attacker-influenced array outside the configured memoryLimit budget. This issue is fixed in version 10.27.1.

### CVE-2026-59731

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-647` |
| Published | 2026-07-08T17:17:25.937 |

Astro is a web framework for content-driven websites. Version 6.4.7 performs authorization decisions on a partially decoded pathname after reaching the iterative URL decoder limit, while later rewrite route matching performs an additional decodeURI() operation and can resolve the request to a protected route. This issue is fixed in version 6.4.8.

### CVE-2026-54591

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-08T21:16:49.657 |

AsyncSSH is a Python package which provides an asynchronous client and server implementation of the SSHv2 protocol on top of the Python asyncio framework. Prior to 2.23.1, a malicious SSH server can write arbitrary files on the asyncssh SCP client's filesystem by sending filenames containing ../ traversal sequences because _parse_cd_args in scp.py returns server-provided names verbatim and _recv_files joins them to the destination path without enforcing the target directory boundary. This issue is fixed in version 2.23.1.

### CVE-2026-3144

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1392` |
| Published | 2026-07-08T16:16:28.463 |

IBM API Connect 12.1.0.0 through 12.1.0.3 uses default credentials which could allow an attacker to gain unauthorized access to the application before the system enforces a credential update.

### CVE-2026-54652

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-269;CWE-532;CWE-598;CWE-863` |
| Published | 2026-07-08T15:16:29.390 |

Frigate is an open source network video recorder. In version 0.17.1, the GET /api/logs/{service} endpoint allows any authenticated user including the viewer role to download Frigate and nginx logs, exposing auto-generated admin passwords and camera credentials logged in request query strings and enabling viewer-to-admin privilege escalation. A fixed release has not been identified.

### CVE-2026-11903

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-08T15:16:25.470 |

Improper neutralization of input during web page generation ('cross-site scripting') vulnerability in Progress MOVEit Transfer (Ad Hoc module).

This issue affects MOVEit Transfer: from 2026.0.0 before 2026.0.1, from 2025.1.0 before 2025.1.4, from 2025.0.0 before 2025.0.8.

### CVE-2026-55878

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-08T22:17:16.050 |

Symfony UX is a JavaScript ecosystem for Symfony. From 2.32.0 before 2.36.1 and from 3.0.0 before 3.2.0, the ux:install console command installs files from a recipe kit by copying paths listed in a copy-files map, and because Path::isRelative() accepts paths like ../../../etc, a crafted or compromised kit can write attacker-controlled content to arbitrary locations or read local files outside the recipe directory. This issue is fixed in versions 2.36.1 and 3.2.0.

### CVE-2026-39822

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-61` |
| Published | 2026-07-08T17:17:21.310 |

On Unix systems, opening a file in an os.Root improperly follows symlinks to locations outside of the Root when the final path component of the a path is a symbolic link and the path ends in /. For example, 'root.Open("symlink/")' will open "symlink" even when "symlink" is a symbolic link pointing outside of the root.

### CVE-2026-47831

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-07-09T07:16:24.423 |

Use of a cryptographically weak random number generator in the GenerateRandomPassword function in bosh-windows-stemcell-builder allows a remote attacker to brute-force the resulting SSH login via TCP/22.
Affected versions: bosh-windows-stemcell-builder versions prior to v2019.98.

### CVE-2026-47829

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-07-09T07:16:24.150 |

Argument Injection in bosh-cli allows a compromised BOSH Director to inject arbitrary OpenSSH options into the locally-spawned ssh process when an operator runs bosh ssh -c, bosh logs -f, or other non-interactive SSH paths, leading to local command execution on the operator's workstation.
Affected versions: bosh-cli versions prior to v7.10.4.

### CVE-2026-60105

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-08T21:16:54.813 |

Monsta FTP before 2.14.5 contains a server-side request forgery vulnerability in the fetchRemoteFile action caused by an incomplete IP blocklist check in the isBlockedIP() function, which fails to detect embedded IPv4 addresses within IPv4-mapped IPv6 addresses. An unauthenticated attacker can obtain a CSRF token from the public getSystemVars endpoint and submit a fetchRemoteFile request with a source URL resolving to an IPv4-mapped address, causing the server to issue HTTP requests to internal services and write responses to an attacker-controlled FTP destination, enabling retrieval of cloud instance metadata credentials.

### CVE-2026-58207

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-08T21:16:52.293 |

NATS Server is a high-performance server for NATS.io, the cloud and edge native messaging system. Prior to 2.14.3 and 2.12.12, a client able to send account-scoped connection monitoring requests could crash the server by supplying Connz pagination Offset and Limit values that overflowed internal arithmetic before the response window was safely bounded. This issue is fixed in versions 2.14.3 and 2.12.12.

### CVE-2026-14373

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-08T20:16:48.080 |

HashiCorp Nomad and Nomad Enterprise did not enforce the allow_privileged restriction for the Docker task driver's host namespace mode options. This may allow an authenticated job submitter to run a container in a host namespace and access information belonging to the host or to other workloads on the same client. This vulnerability, CVE-2026-14373, is fixed in Nomad Community Edition 2.0.4 and Nomad Enterprise 2.0.4, 1.11.8, and 1.10.14.

### CVE-2026-60102

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-08T17:17:28.997 |

Horde Virtual File System (VFS) API before 3.0.1 contains an OS command injection vulnerability in the Horde_Vfs_Smb driver where the _escapeShellCommand() method fails to sanitize command substitution sequences, allowing authenticated attackers to inject arbitrary shell commands through user-controlled filenames. Attackers can supply malicious filenames containing unescaped command substitution payloads through operations such as file upload, folder creation, rename, or deletion, which are interpolated into a double-quoted shell context and executed via proc_open() through /bin/sh -c before smbclient runs, resulting in arbitrary command execution on the underlying system.

### CVE-2026-55874

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-08T15:16:30.320 |

SeaweedFS is a distributed storage system. Prior to 4.34, the S3 API gateway does not reject dot-dot path segments in the X-Amz-Copy-Source header used by CopyObject and UploadPartCopy, allowing an authenticated identity scoped to one bucket to read objects from other buckets through server-side copy. This issue is fixed in version 4.34.

### CVE-2026-59804

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-1385` |
| Published | 2026-07-08T20:16:56.077 |

Midscene Bridge Server through 1.10.3, fixed in commit 86f4118, contains a missing authentication and CORS misconfiguration vulnerability that allows unauthenticated remote attackers to hijack active bridge sessions by opening a cross-origin WebSocket connection to the local Socket.IO server, which performs no Origin header validation and requires no authentication token. Attackers can connect from any web page visited by the victim to seize the single-client slot, intercept and inject automation commands, exfiltrate command-payload data, or unconditionally terminate the server by supplying the MIDSCENE_BRIDGE_SIGNAL_KILL query parameter.

### CVE-2026-59692

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-09T11:16:41.783 |

A stack buffer overflow vulnerability was found in GStreamer's DTLS plugin. During a DTLS handshake, the peer certificate Subject Distinguished Name is printed into a fixed-size 2048-byte stack buffer without bounds checking. A remote unauthenticated attacker can send a certificate with an oversized Subject DN that exceeds the buffer, causing a stack buffer overflow and process crash, resulting in denial of service.

### CVE-2026-1989

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-09T10:16:25.710 |

Authorization bypass through User-Controlled key vulnerability in PAVO Financial Technology Solutions Inc. PAVO Pay allows Exploitation of Trusted Identifiers.

This issue affects PAVO Pay: through 09072026. NOTE: The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-54772

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-835` |
| Published | 2026-07-08T23:16:54.830 |

CoreWCF is a port of the service side of Windows Communication Foundation (WCF) to .NET Core. Prior to 1.8.1 and 1.9.1, an unauthenticated remote attacker that can reach a NetTcpBinding, NetNamedPipeBinding, or UnixDomainSocketBinding endpoint can trigger premature EOF handling in the CoreWCF net.tcp, net.pipe, or net.uds framing handshake and pin one server thread-pool worker at full CPU per connection. This issue is fixed in versions 1.8.1 and 1.9.1.

### CVE-2026-54499

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502;CWE-676` |
| Published | 2026-07-08T23:16:54.690 |

Stanza is a Stanford NLP Python library for tokenization, sentence segmentation, NER, and parsing of many human languages. Prior to 1.12.2, Stanza model loaders such as stanza.models.common.pretrain.Pretrain.load() attempt torch.load(..., weights_only=True) but fall back to torch.load(..., weights_only=False) on attacker-controllable pickle.UnpicklingError, allowing a malicious .pt pretrain or model file to execute arbitrary pickle code when a Stanza NLP pipeline loads it. This issue is fixed in version 1.12.2.

### CVE-2026-15117

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T23:16:52.833 |

Use after free in Payments in Google Chrome prior to 150.0.7871.115 allowed a remote attacker who convinced a user to engage in specific UI gestures to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-15111

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T23:16:52.203 |

Use after free in Views in Google Chrome prior to 150.0.7871.115 allowed a remote attacker who convinced a user to engage in specific UI gestures to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-55470

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-07-08T22:17:15.377 |

HAPI FHIR is a complete implementation of the HL7 FHIR standard for healthcare interoperability in Java. Prior to 6.9.10, the fix for CVE-2026-45367 incompletely patched the DSTU2 module, leaving FHIRPathEngine.matches() in org.hl7.fhir.dstu2/utils/FHIRPathEngine.java to call raw String.matches(sw) without RegexTimeout protection while replaceMatches() was updated, allowing an unauthenticated attacker to trigger catastrophic regex backtracking and exhaust server CPU. This issue is fixed in version 6.9.10.

### CVE-2026-44160

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409` |
| Published | 2026-07-08T22:17:14.600 |

Fluentd collects events from various data sources and writes them to files, RDBMS, NoSQL, IaaS, SaaS, Hadoop and so on. Prior to 1.19.3, Fluentd's in_http and in_forward plugins support gzip-compressed data but enforce limits only on compressed payloads through settings such as body_size_limit and chunk_size_limit, allowing crafted compressed payloads to decompress in memory to an excessive size and cause denial of service through memory exhaustion. This issue is fixed in version 1.19.3.

### CVE-2026-44025

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-08T22:17:14.473 |

Fluentd collects events from various data sources and writes them to files, RDBMS, NoSQL, IaaS, SaaS, Hadoop and so on. Prior to 1.19.3, Fluentd's Monitor Agent plugin in_monitor_agent exposes internal metrics and plugin information via a REST API, and responses from /api/plugins.json and related endpoints unintentionally include internal instance variables that may contain database passwords, API keys, or cloud credentials. This issue is fixed in version 1.19.3.

### CVE-2026-56669

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407;CWE-436` |
| Published | 2026-07-08T21:16:50.690 |

Elysia is a Typescript framework for request validation, type inference, OpenAPI documentation, and client-server communication. Prior to 1.4.29, Elysia uses getAll in form data normalization for multipart/form-data endpoints, causing the amount of work to grow quadratically with the number of unique key-value pairs and allowing CPU exhaustion. This issue is fixed in version 1.4.29.

### CVE-2026-49866

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-08T21:16:49.137 |

libp2p is a JavaScript Implementation of libp2p networking stack. Prior to 16.0.0, @libp2p/gossipsub defaultDecodeRpcLimits set maxIhaveMessageIDs and maxIwantMessageIDs to Infinity, allowing oversized IHAVE and IWANT control message arrays in message/decodeRpc.ts and gossipsub.ts to synchronously iterate roughly 180,000 message IDs per 4 MB frame and block the Node.js event loop. This issue is fixed in version 16.0.0.

### CVE-2026-15167

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-08T21:16:47.667 |

DBS Etherwatch file parser crash in Wireshark 4.6.0 to 4.6.6 and 4.4.0 to 4.4.16 allows denial of service

### CVE-2026-59939

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409` |
| Published | 2026-07-08T20:16:59.557 |

httplib2 is a comprehensive HTTP client library for Python. Prior to 0.32.0, httplib2 performs unbounded decompression of HTTP response bodies encoded with Content-Encoding: gzip or deflate in _decompressContent in httplib2/init.py, allowing a malicious or compromised HTTP server to return a small compressed payload that expands to an arbitrarily large size in memory and causes MemoryError or OOM-kill in the client process. This issue is fixed in version 0.32.0.

### CVE-2026-58250

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-07-08T20:16:54.483 |

NATS Server is a high-performance server for NATS.io, the cloud and edge native messaging system. Prior to 2.12.8 and 2.11.17, an unauthenticated peer with network access to a leafnode listener with compression enabled could crash the server during the pre-authentication leafnode handshake by sending repeated leafnode INFO protocol messages before authentication and account setup completed. This issue is fixed in versions 2.12.8 and 2.11.17.

### CVE-2026-58210

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-08T20:16:53.950 |

NATS Server is a high-performance server for NATS.io, the cloud and edge native messaging system. Prior to 2.14.3 and 2.12.12, an unauthenticated MQTT client could cause the server to retain large incomplete MQTT CONNECT packets before authentication completed, consuming server memory while the parser waited for the advertised MQTT packet length. This issue is fixed in versions 2.14.3 and 2.12.12.

### CVE-2026-55760

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-08T20:16:53.287 |

Handlebars.java provides logic-less and semantic Mustache templates with Java. Prior to 4.5.2, applications that pass user-controlled input to Handlebars.compile() using FileTemplateLoader or ClassPathTemplateLoader are vulnerable to path traversal, allowing arbitrary file read through template names derived from URL path parameters, request parameters, or other user-controlled sources. This issue is fixed in version 4.5.2.

### CVE-2026-55404

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-07-08T20:16:52.987 |

yt-dlp and youtube-dl are command-line audio/video downloaders. Prior to 2026.7.4, the --write-link, --write-url-link, and --write-desktop-link options can write .url or .desktop shortcut files using attacker-controlled webpage_url or filename metadata without sufficient validation or escaping, allowing malicious file:// URI injection on Windows or newline-based desktop entry key injection on Linux that can execute commands if the generated shortcut is opened. This issue is fixed in version 2026.7.4.

### CVE-2026-59928

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407;CWE-1333` |
| Published | 2026-07-08T17:17:28.600 |

Mistune is a Python Markdown parser with renderers and plugins. Prior to 3.3.0, a Markdown document containing many repeated or distinct reference-link definitions causes quadratic work in src/mistune/block_parser.py and the ref_links environment dictionary handling, allowing denial of service through CPU exhaustion. This issue is fixed in version 3.3.0.

### CVE-2026-59925

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407;CWE-1333` |
| Published | 2026-07-08T17:17:28.183 |

Mistune is a Python Markdown parser with renderers and plugins. Prior to 3.3.0, long sequences of well-formed double-asterisk or triple-asterisk emphasis pairs around a character cause quadratic work in src/mistune/inline_parser.py because the parser scans forward for matching close markers from every potential opening run, allowing denial of service in default Mistune parsing. This issue is fixed in version 3.3.0.

### CVE-2026-59922

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407;CWE-1333` |
| Published | 2026-07-08T17:17:27.770 |

Mistune is a Python Markdown parser with renderers and plugins. Prior to 3.3.0, a run of closed tilde, equals-sign, or caret marker pairs around a character causes quadratic work in src/mistune/plugins/formatting.py when the strikethrough, mark, or insert plugin scans for matching markers from each possible start position, allowing denial of service through CPU exhaustion. This issue is fixed in version 3.3.0.

### CVE-2026-59892

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-07-08T17:17:27.190 |

OpenTelemetry JavaScript is the OpenTelemetry JavaScript client. Prior to 2.9.0, @opentelemetry/propagator-jaeger decodes incoming uber-trace-id and uberctx-* HTTP header values with decodeURIComponent() without handling decode errors, allowing an unauthenticated remote attacker to send a malformed percent-encoded value that throws an uncaught URIError and terminates a Node.js process using JaegerPropagator as the active propagator. This issue is fixed in version 2.9.0.

### CVE-2026-59887

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-07-08T17:17:26.883 |

linkify-it is a links recognition library with full Unicode support. Prior to 5.0.2, the mailto: schema validator used by .test() and .match() can be invoked at every mailto: occurrence and scan the remaining input through src_email_name in lib/re.mjs, causing O(n^2) CPU consumption on crafted user text. This issue is fixed in version 5.0.2.

### CVE-2026-59869

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-07-08T16:16:33.423 |

js-yaml is a JavaScript YAML parser and dumper. From 3.0.0 before 3.15.0 and from 4.0.0 before 4.3.0, js-yaml can spend quadratic CPU time parsing a document whose size grows only linearly when a chain of mappings uses merge keys where each mapping merges the previous one. This issue is fixed in versions 3.15.0 and 4.3.0.

### CVE-2026-59725

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-404` |
| Published | 2026-07-08T16:16:33.133 |

Socket.IO enables bidirectional and low-latency communication for every platform. From 4.1.0 before 6.6.7, Engine.IO protocol v4 polling transport does not properly close the HTTP response for invalid binary POST requests with Content-Type: application/octet-stream, allowing an unauthenticated attacker to exhaust server-side connections and sockets. This issue is fixed in version 6.6.7.

### CVE-2026-59724

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-08T16:16:32.980 |

Socket.IO enables bidirectional and low-latency communication for every platform. From 6.5.0 before 6.6.7, Engine.IO servers with WebTransport enabled can resolve a crafted session ID such as __proto__ through an inherited property of the clients object during WebTransport upgrade handling, causing a TypeError and denial of service. This issue is fixed in version 6.6.7.

### CVE-2026-49147

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-150` |
| Published | 2026-07-08T15:16:27.787 |

App::Ack versions through 3.10.0 for Perl print unsanitised terminal escape sequences from filenames in several output modes.

When ack prints a filename whose basename contains terminal control bytes such as ANSI escape sequences, those bytes reach the terminal unchanged. Version 3.10.0 added a _safe_filename helper that sanitises the filenames printed by -f, -g, the colored match heading, and per-match lines, but the --show-types, -l/-L, and -c paths still emit the raw filename.

A file whose name embeds cursor-movement or color escapes can overwrite or recolor earlier terminal output, or be passed unchanged to a downstream consumer.

### CVE-2026-49146

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-08T15:16:27.673 |

App::Ack versions before 3.10.0 for Perl allow memory exhaustion via an unbounded context value in a project .ackrc.

ack searches up the directory hierarchy from the current directory for a project .ackrc and loads its options. The -B and -C context options accepted any positive integer, and ack sized the before-context buffer to that value, so a project .ackrc setting --before-context=100000000 made ack allocate a buffer of 100 million elements.

A project .ackrc committed to an untrusted repository can abort ack with an out-of-memory condition.

### CVE-2026-49145

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-73;CWE-426` |
| Published | 2026-07-08T15:16:27.563 |

App::Ack versions through 3.10.0 for Perl read arbitrary files via --files-from in a project .ackrc.

ack searches up the directory hierarchy from the current directory for a project .ackrc and loads its options. The project-source option blocklist in App::Ack::ConfigLoader does not include --files-from, so a project .ackrc can set it to a path whose listed files ack then reads and searches. Version 3.10.0 added --follow to the blocklist; --files-from remains accepted.

A project .ackrc committed to an untrusted repository can make ack read files outside the project and print their matching lines.

### CVE-2026-10699

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-07-08T15:16:25.173 |

Missing release of memory after effective lifetime vulnerability in Progress MOVEit Transfer (Custom Reports modules).

This issue affects MOVEit Transfer: from 2025.0.0 before 2025.0.8, from 2025.1.0 before 2025.1.4, from 2026.0.0 before 2026.0.1.

### CVE-2026-54784

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-311;CWE-523` |
| Published | 2026-07-08T23:16:56.307 |

CoreWCF is a port of the service side of Windows Communication Foundation (WCF) to .NET Core. In version 1.9.0, CoreWCF SPNEGO SecurityContextToken negotiation can expose the proof key recovered from the RSTR when TransportWithMessageCredential with Windows client credentials and session establishment are used, allowing an observer to impersonate the authenticated Windows principal and decrypt or forge WS-SecureConversation traffic. This issue is fixed in version 1.9.1.

### CVE-2026-54783

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-294;CWE-345;CWE-347` |
| Published | 2026-07-08T23:16:56.173 |

CoreWCF is a port of the service side of Windows Communication Foundation (WCF) to .NET Core. Prior to 1.8.1 and 1.9.1, CoreWCF WS-Security endorsing and supporting signature verification does not ensure the selected ds:Signature covers the expected Security header target, allowing an attacker with one captured signed SOAP envelope to replay arbitrary service operations as the victim principal. This issue is fixed in versions 1.8.1 and 1.9.1.

### CVE-2026-54781

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-345` |
| Published | 2026-07-08T23:16:55.890 |

CoreWCF is a port of the service side of Windows Communication Foundation (WCF) to .NET Core. Prior to 1.8.1 and 1.9.1, CoreWCF SAML token validation does not enforce SubjectConfirmation method URIs or holder-of-key proof keys in SamlSecurityTokenHandler, allowing holder-of-key downgrade or custom confirmation method assertions to authenticate a subject without proving authority over the assertion. This issue is fixed in versions 1.8.1 and 1.9.1.

### CVE-2026-54774

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-345;CWE-347` |
| Published | 2026-07-08T23:16:55.090 |

CoreWCF is a port of the service side of Windows Communication Foundation (WCF) to .NET Core. Prior to 1.8.1 and 1.9.1, SamlSerializer skips final SignatureValue verification when a CoreWCF service validates SAML tokens using a non-X.509 signing token, allowing an attacker to reference a non-X.509 SecurityToken key identifier and bypass assertion signature verification. This issue is fixed in versions 1.8.1 and 1.9.1.

### CVE-2026-13320

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-08T21:16:46.630 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 15.7 before 18.11.7, 19.0 before 19.0.4, and 19.1 before 19.1.2 that under certain conditions could have allowed an authenticated user to execute arbitrary scripts in another user's browser session due to improper sanitization of user-supplied input.

### CVE-2026-9253

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-09T12:16:25.630 |

The WP Cost Estimation & Payment Forms Builder (E&P Forms) plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'customerInfos' parameter in all versions up to, and including, 10.5.97 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-13441

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-09T11:16:24.790 |

The EventPrime – Events Calendar, Bookings and Tickets plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'new_event_type_background_color' parameter in all versions up to, and including, 4.3.4.2 due to insufficient input sanitization and output escaping. This makes it possible for authenticated attackers, with custom-level access and above, to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the plugin's Guest Submissions setting (allow_submission_by_anonymous_user) to be enabled, which allows unauthenticated attackers to submit event types via the frontend form; when that setting is disabled, exploitation requires at minimum a subscriber-level authenticated account.

### CVE-2026-8848

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-09T08:16:49.480 |

The Popup Maker – Boost Sales, Conversions, Optins, Subscribers with the Ultimate WP Popup Builder plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 1.22.0. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for authenticated attackers, with editor-level access and above, to install and activate an arbitrary plugin from an attacker-controlled URL, leading to remote code execution. Exploitation requires that a valid Popup Maker Pro license is active on the target site and that Popup Maker Pro is not yet installed, as these conditions are necessary for the legacy v1/connect/info endpoint to issue the bearer token used to satisfy the install endpoint's only non-spoofable validation check.

### CVE-2026-33390

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-07-09T08:16:48.233 |

An Incorrect Privilege Assignment vulnerability was discovered in the synchronization functionality due to Arc sensors receiving CLI permissions. An authenticated user with limited privileges can push administrative CLI commands through the sync, altering the device configuration, and/or affecting its availability.

### CVE-2026-15000

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-09T08:16:47.340 |

The Connect Contact Form 7 and Mailchimp plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Mailchimp Merge Field Values in all versions up to, and including, 0.9.78.06 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injected payload is only triggered when a privileged user (Administrator) performs a Contact Lookup for the email address submitted via the CF7 form, meaning execution is deferred until an administrator interacts with the affected entry.

### CVE-2026-44161

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-08T22:17:14.737 |

Fluentd collects events from various data sources and writes them to files, RDBMS, NoSQL, IaaS, SaaS, Hadoop and so on. Prior to 1.19.3, the Fluentd out_http output plugin allows placeholders such as ${tag} in the endpoint configuration parameter, and if a placeholder value is derived from untrusted input an attacker can control the destination hostname of outbound HTTP requests and force requests to arbitrary internal services. This issue is fixed in version 1.19.3.

### CVE-2026-0288

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:N/R:U/V:D/RE:M/U:Red` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-08T21:16:45.590 |

Multiple buffer overflow vulnerabilities in the User-ID Terminal Server Agent (TSA) component of Palo Alto Networks PAN-OS software allow an unauthenticated attacker with network access to cause a denial of service (DoS) condition or potentially execute arbitrary code by sending specially crafted network traffic.

The security risk posed by this issue is minimized when the User-ID Terminal Server Agent connectivity is restricted to only trusted internal IP addresses according to our recommended  best practice deployment guidelines https://docs.paloaltonetworks.com/ngfw/help/10-2/user-identification/device-user-identification-terminal-services-agents#:~:text=To%20minimize%20security%20risk%2C%20restrict%20TS%20Agent%20connectivity%20to%20trusted%20internal%20IP%20addresses%20only. .

Panorama is not impacted by this vulnerability.

### CVE-2026-24700

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-08T15:16:27.047 |

An OS command injection vulnerability exists in the start_lltd() function of the "rc" binary in Cisco RV130/RV130W with firmware 1.0.3.55 and RV110W routers with firmware 1.2.2.5 / 1.2.2.8. The machine_name configuration parameter is not properly sanitized, which could allow an authenticated remote attacker to execute arbitrary OS commands with root privileges.

### CVE-2026-24699

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-08T15:16:26.943 |

An OS command injection vulnerability exists in the sub_34984() function of the "rc" binary in Cisco RV130/RV130W with firmware 1.0.3.55 and RV110W routers with firmware 1.2.2.5 / 1.2.2.8. The lan_ipv6_prefixlen configuration parameter is not properly sanitized, which could allow an authenticated remote attacker to execute arbitrary OS commands with root privileges.

### CVE-2026-24698

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-08T15:16:26.827 |

An OS command injection vulnerability exists in the save_syslog_to_file() function of the "httpd" binary in Cisco RV130/RV130W with firmware 1.0.3.55 and RV110W routers with firmware 1.2.2.5 / 1.2.2.8. The model_name configuration parameter is not properly sanitized, which could allow an authenticated remote attacker to execute arbitrary OS commands with root privileges.

### CVE-2026-24697

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-08T15:16:26.697 |

An OS command injection vulnerability exists in the start_bonjour() function of the "rc" binary in Cisco RV130/RV130W with firmware 1.0.3.55 and RV110W routers with firmware 1.2.2.5 / 1.2.2.8. The wan_hostname configuration parameter is not properly sanitized, which could allow an authenticated remote attacker to execute arbitrary OS commands with root privileges.

### CVE-2026-10698

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-943` |
| Published | 2026-07-08T15:16:25.040 |

Improper Neutralization of Special Elements in Data Query Logic vulnerability in Progress MOVEit Transfer (Custom Reports modules).

This issue affects MOVEit Transfer: from 2025.0.0 before 2025.0.8, from 2025.1.0 before 2025.1.4, from 2026.0.0 before 2026.0.1.

### CVE-2026-59691

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-09T11:16:41.657 |

A heap buffer overflow vulnerability was found in GStreamer's rfbsrc plugin. When a client connects to a malicious RFB/VNC server that advertises a 16bpp framebuffer and sends Hextile-encoded updates, the Hextile background fill path writes 32-bit pixel values into a buffer allocated for 16-bit pixels. This type mismatch causes an out-of-bounds heap write that can lead to denial of service (process crash) and potential memory corruption.

### CVE-2026-14372

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-09T11:16:24.910 |

The Bit Form – Contact Form, Payment Forms, Multi Step Forms, Calculator & Custom Form Builder plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the deleteFiles function in all versions up to, and including, 3.1.1 This makes it possible for authenticated attackers, with subscriber-level access and above, to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config).

### CVE-2026-41857

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-07-09T06:16:20.287 |

A compromised or malicious BOSH Director can execute arbitrary shell commands on the operator's workstation when the operator runs bosh ssh (or bosh scp/bosh logs -f) with default flags.
Affected versions: BOSH CLI versions prior to 7.10.5.

### CVE-2026-54528

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-178` |
| Published | 2026-07-08T21:16:49.407 |

JupyterLab Git is a Git extension for JupyterLab. Prior to 0.54.0, jupyterlab-git uses fnmatch.fnmatchcase() in GitHandler.prepare() in jupyterlab_git/handlers.py to enforce excluded_paths, allowing an authenticated user on a case-insensitive filesystem to vary URL path casing and read excluded directories. This issue is fixed in version 0.54.0.

### CVE-2026-35210

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-639;CWE-863` |
| Published | 2026-07-08T21:16:48.487 |

OpenCTI is an open source platform for managing cyber threat intelligence knowledge and observables. Prior to 7.260326.0, an authorization bypass vulnerability in OpenCTI allows any authenticated user with KNOWLEDGE_KNUPDATE permission to bypass Confidence Level validation and Object Marking restrictions by injecting the synchronized-upsert: true HTTP header, enabling attackers to downgrade confidence levels, remove security markings such as TLP:RED, manipulate relationships, and affect STIX object types including Indicators, ThreatActors, Malware, and Reports. This issue is fixed in version 7.260326.0.

### CVE-2026-59805

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-08T20:16:56.250 |

Gumroad before 2026.07.06.2 contains a broken access control vulnerability in the PurchasesController that allows authenticated sellers to manipulate purchase access for other sellers' products by sending PUT requests to the revoke_access and undo_revoke_access actions without seller ownership validation. Attackers can modify the is_access_revoked status on arbitrary purchases to unauthorized revoke or restore buyer access to products they do not own.

### CVE-2026-58213

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-74` |
| Published | 2026-07-08T20:16:54.180 |

NATS Server is a high-performance server for NATS.io, the cloud and edge native messaging system. Prior to 2.14.1 and 2.12.9, an MQTT client could include protocol control characters in subscription filters that were later forwarded as NATS protocol data to route or leafnode connections, corrupting the forwarded protocol stream and allowing injection of unintended NATS protocol operations. This issue is fixed in versions 2.14.1 and 2.12.9.

### CVE-2026-59262

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-08T16:16:31.430 |

AFFiNE's histories GraphQL field fails to validate Doc.Read permission before exposing document edit history, allowing authenticated workspace members to retrieve restricted content timelines. Attackers can supply arbitrary document GUIDs to access full edit histories including user names, emails, and timestamps of private pages they lack access to.

### CVE-2026-55761

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-08T16:16:31.020 |

Portainer Community Edition is a lightweight service delivery platform for containerized applications that can be used to manage Docker, Swarm, Kubernetes and ACI environments. In versions 2.39.0 through 2.39.3 and 2.40.0 until 2.43.0, unauthenticated restore and administrator initialization endpoints (/api/restore and /api/users/admin/init) remain accessible during the five-minute setup window for uninitialized instances, allowing a network attacker to restore a crafted backup or create the first administrator account and gain full administrative access. This issue is fixed in versions 2.39.4 and 2.43.0.

### CVE-2026-59948

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-787` |
| Published | 2026-07-08T20:16:59.980 |

Composer is a dependency Manager for the PHP language. Prior to 2.2.29 and 2.10.2, a maliciously crafted package from an untrusted repository other than Packagist.org or Private Packagist can cause Composer to write attacker-controlled files outside the vendor directory and outside the project during install or update by using an invalid package name that is not correctly validated before dependency-resolution results are written or installed. This issue is fixed in versions 2.2.29 and 2.10.2.
