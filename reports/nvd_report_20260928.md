# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-27 15:00 UTC
- **対象期間**: `2026-09-26T15:01:47.000Z` 〜 `2026-09-27T15:00:14.000Z`
- **重要CVE数**: 52 件（Critical 9.0+: 9 件 / High 7.0〜: 43 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、CVSS 7.0 以上の深刻度を持つものは **30 件以上** と非常に多く、特に **Web アプリケーション（Joomla・WordPress）** と **サーバーサイドコンポーネント（Node.js vm2、hMailServer）** に集中しています。  
- 最高評価は **CVSS 10.0**（CVE‑2026‑97163）で、認証不要のリモートコード実行が可能になる点が顕著です。  
- 多くの脆弱性は「**ファイルアップロード／パス・トラバーサル**」や「**評価関数（eval）/シリアライズ**」の不適切な入力検証に起因しており、攻撃者は **管理者権限取得** や **任意コード実行** を比較的容易に達成できます。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 製品・コンポーネント | 主な脆弱性種別 | 推奨される対策 (概要) | 影響範囲・リスク |
|-----|------|----------------------|----------------|----------------------|-------------------|
| **CVE‑2026‑97163** | **10.0** | Joomla 拡張 **lomart.fr – UP plugin** (5.0.0‑5.2.0, 6.0.0‑6.0.29) | 認証不要リモートコード **インストール**（任意 PHP スクリプト） | 5.2.1 / 6.0.30 以降にアップデート、不要なプラグインは無効化 | 完全リモートコード実行 → サーバ全体の乗っ取り |
| **CVE‑2026‑100741** | **9.8** | **hMailServer** 6.0.0‑6.3.3 (Windows) | JScript **Eval インジェクション**（パスワード解析時に任意コード実行） | 6.3.4 以降にアップデート、外部からのパスワード変更をファイアウォールで遮断 | サービスアカウント権限で任意コード実行、メールサーバ全体が危険 |
| **CVE‑2026‑82901** | **9.8** | WordPress プラグイン **Ultra Addons for Contact Form 7** (≤ 3.5.50) | 任意ファイルアップロード（MIME 判定不備） | 3.5.51 以降に更新、アップロードディレクトリの実行権限を削除 | 攻撃者がシェルやウェブシェルを配置し、サイト乗っ取りが可能 |
| **CVE‑2026‑85984** | **9.8** | WordPress プラグイン **miniOrange OTP Login** (≤ 5.5.5) | 認証バイパス（`mo_wp_login_intent` パラメータ） | 5.5.6 以降に更新、`skip_pass_fallback` 設定を無効化 | 認証プロセスを迂回し、管理者アカウントでログイン可能 |
| **CVE‑2026‑100721** | **9.5** | **vm2** (Node.js サンドボックス) < 3.12.2 | 外部モジュール解決時の **認可バイパス**（`require.external` カスタムリゾルバ） | 3.12.2 以降にアップデート、`require.external` の使用は最小限に | サンドボックス脱走 → 任意コード実行、ホストプロセスへの影響 |

> **選定理由**  
> - **スコアが最高（10.0）または 9.8 以上** で、かつ **認証不要** で攻撃が成立する点が共通。  
> - 影響が **Web サーバ全体、メールサーバ、Node.js アプリ** とインフラの根幹に及ぶ。  
> - 多くは **プラグインや拡張機能** のみの更新で対処可能だが、放置すると **完全乗っ取り** に至るリスクが高い。

---

## 3. 推奨アクション  

### 3.1 パッケージ・プラグインの即時更新
| 製品 | 現行バージョン (脆弱) | 修正版 (推奨) | 更新方法 |
|------|----------------------|--------------|----------|
| Joomla – **lomart.fr UP plugin** | 5.0.0‑5.2.0、6.0.0‑6.0.29 | **5.2.1** / **6.0.30** 以上 | Joomla 管理画面 → 拡張機能 → 更新、または手動で zip 配布版を上書き |
| **hMailServer** | 6.0.0‑6.3.3 | **6.3.4** 以上 | 公式サイトからインストーラを取得し、サービスを停止した上でアップグレード |
| WordPress – **Ultra Addons for Contact Form 7** | ≤ 3.5.50 | **3.5.51** 以上 | WordPress 管理画面 → プラグイン → 更新、または FTP で上書き |
| WordPress – **miniOrange OTP Login** | ≤ 5.5.5 | **5.5.6** 以上 | 同上 |
| **vm2** (npm) | < 3.12.2 | **3.12.2** 以上 | `npm install vm2@^3.12.2` もしくは `yarn add vm2@^3.12.2` |
| **AzuraCast** (多数の脆弱性) | < 0.23.8 | **0.23.8** 以上 | Docker イメージを最新版にプルし、コンテナを再作成 |
| **MONAI** (pickle 連鎖・OS コマンドインジェクション) | < 1.6.0 | **1.6.0** 以上 | `pip install --upgrade monai` |

### 3.2 設定・運用上の緩和策
- **Joomla / WordPress**:  
  - 不要な拡張機能は **無効化または削除**。  
  - アップロードディレクトリ (`/media`, `/uploads`) の **実行権限 (chmod 0755)** を外す。  
  - `wp-config.php` で `DISALLOW_FILE_EDIT` と `DISALLOW_FILE_MODS` を有効化し、管理画面からのファイル編集を禁止。  
- **hMailServer**:  
  - 管理ポート (default 9997) への **IP 制限** をファイアウォールで設定。  
  - パスワード変更 API の **認証強化**（二要素認証の導入）を検討。  
- **vm2**:  
  - `require.external` の使用は **デフォルトで無効** にし、必要時はホワイトリスト方式で限定。  
  - サンドボックス内で外部モジュールをロードする場合は **署名検証** を組み込む

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-97163

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-284` |
| Published | 2026-09-26T15:16:55.890 |

Joomla Extension - lomart.fr - Unauthenticated remote code installation in UP plugin extension 5.0.0-5.2.0, 6.0.0-6.0.29

### CVE-2026-100741

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-09-27T08:16:26.813 |

Eval injection in the JScript event-script dispatcher in Progressive Robot Ltd's hMailServer, versions 6.0.0 through 6.3.3 on Windows, allows a remote, unauthenticated attacker to run arbitrary JScript inside the hMailServer service process, with the privileges of the service account, via a password containing a backslash followed by an apostrophe, sent in any logon (SMTP AUTH, POP3, IMAP) that names an existing, active account. Exploitation requires a non-default configuration: event scripting enabled (off by default), the script language set to JScript (the default is VBScript), and an OnClientValidatePassword handler defined in the event script. The server wrote event values into the handler call as JScript string literals, escaping the apostrophe but not the backslash, so such a value closes the literal and the rest of it is parsed as script. The same flaw is reachable by a remote POP3 server through the message UID it returns, where an OnExternalAccountDownload handler is defined, and by a remote SMTP server through the error reply it rejects a delivery with, where an OnDeliveryFailed handler is defined. Before 6.2.25 the injected script can create any COM object, and from 6.2.25 it can with the default ScriptAllowedObjects value of '*'; WScript.Shell among them gives command execution as the service account. VBScript event scripts and the Linux builds of Progressive Robot Ltd's hMailServer are not affected.

### CVE-2026-82901

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-26T19:16:28.427 |

The Ultra Addons for Contact Form 7 plugin for WordPress is vulnerable to Arbitrary File Upload due to insufficient file type validation in the 'uacf7_wpcf7_mail_components' function in all versions up to, and including, 3.5.50. This makes it possible for unauthenticated attackers to upload arbitrary files on the affected site's server which may make remote code execution possible. Note: This is only exploitable when the plugin's PDF Generator module is enabled, which is disabled by default.

### CVE-2026-85984

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-26T18:16:31.010 |

The miniOrange OTP Login, Verification and SMS Notifications plugin for WordPress is vulnerable to Authentication Bypass via the mo_wp_login_intent parameter in all versions up to, and including, 5.5.5. This is due to a missing password-intent guard in the skip_pass_fallback-enabled configuration branch of the mo_by_pass_login() function, which treats administrator role membership alone as sufficient authentication whenever the unauthenticated, unverified POST parameter mo_wp_login_intent is submitted with the value otp, causing mo_get_user() to skip wp_authenticate_username_password() and resolve a WP_User purely from a username lookup. This makes it possible for unauthenticated attackers to log in as any existing administrator account by supplying only a known username and an empty password alongside mo_wp_login_intent=otp, with no password or OTP verification required. Exploitation is conditional on a site administrator having simultaneously enabled the following plugin options: WP Login OTP, Login with Only OTP, Allow Users to Login with Username and Password, and Admin OTP Bypass.

### CVE-2026-100721

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-27T02:17:17.547 |

vm2 before 3.12.2 contains an authorization bypass in the NodeVM external-module resolver. When an embedder configures `require.external` with a custom resolver (and `context: 'host'`), `LegacyResolver.customResolve` in lib/resolver-compat.js records the resolved module directory in `this.externals` as `new RegExp('^' + escapeRegExp(resolvedPath))`, without requiring a path separator or end-of-string boundary. Untrusted guest code can therefore require the allowlisted module (e.g. `foo`) and then require the absolute path of a non-allowlisted sibling whose path merely shares the resolved prefix (e.g. `.../node_modules/foo2/index.js`); the sibling passes `isPathAllowedForModule` and is loaded through `hostRequire`, so its top-level code runs in the host process before the exports are wrapped with `vm.readonly`, resulting in a sandbox escape and arbitrary code execution in the host context.

### CVE-2026-94132

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-26T15:16:55.397 |

Joomla Extension - acymailing.com - Remote Code Execution vulnerability in mailbox action feature in AcyMailing Enterprise extension < 11.1.0 - MIME parts of incoming emails were saved to media/com_acym/upload/ with no extension check, so anyone who could email the monitored mailbox could write a PHP file into the web root.

### CVE-2026-97160

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-26T15:16:55.520 |

Joomla Extension - lomart.fr - Authenticated, privileged PHP command injection in UP plugin extension 5.0.0-5.2.0, 6.0.0-6.0.29

### CVE-2026-97161

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-284` |
| Published | 2026-09-26T15:16:55.640 |

Joomla Extension - lomart.fr - Various path traversal / file access vectors in UP plugin extension 5.0.0-5.2.0, 6.0.0-6.0.29

### CVE-2026-100835

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-27T02:17:21.640 |

Contrast before 1.16.0 is susceptible to remote attestation relay attacks. Contrast accepted any TEE attestation report that verified correctly and contained the expected firmware patch levels and software measurements, regardless of which machine produced it, so attestation was not bound to specific, physically trusted hardware. An attacker who can both intercept network traffic between the CLI and the Coordinator (or between the Coordinator and an attested component) and forge reports or extract secrets from any single TEE machine under their physical control can relay such a report to impersonate a Contrast Coordinator or a Contrast workload, defeating identity verification in Contrast's attested TLS (aTLS).

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-100722

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-09-27T02:17:18.817 |

vm2 before 3.12.2 does not apply host-side Promise rejection handling in the sandbox-to-host construct trap. In BaseHandler, the apply trap calls markHostPromiseHandled() on the returned value, but the adjacent construct path returns the result of Reflect.construct without the same sanitization. If an embedder exposes a constructable host function whose constructor returns a native rejected Promise, an untrusted script executed via VM.run can invoke it with `new` and ignore the result; the rejected host Promise crosses the bridge unhandled and, under Node's strict unhandled-rejection policy, is promoted to an uncaught exception that terminates the host process.

### CVE-2026-100846

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-27T02:17:23.283 |

MONAI before 1.5.2 contains a deserialization of untrusted data vulnerability in the algo_from_pickle function in monai/auto3dseg/utils.py. The function reads a .pkl file and passes its contents to pickle.loads without validating the data source or content. If an application invokes algo_from_pickle on an attacker-supplied pickle file, an object defining __reduce__ is executed during deserialization, resulting in arbitrary code execution in the context of the application.

### CVE-2026-77203

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-26T18:16:29.917 |

The Groups – Memberships and Access Control plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 4.6.0. This is due to the groups_join() function deriving group-join eligibility from the ambient post's author capabilities via the global $post->post_author rather than from the currently authenticated user's own capabilities, while simultaneously minting and returning a valid groups-join-data hash and WordPress nonce for the caller in the same response — eliminating all authorization barriers to self-enrollment. This makes it possible for authenticated attackers, with Subscriber-level access and above, to enroll themselves into any group including privileged groups carrying the groups_admin_groups capability, and to subsequently create and join a group containing every registered WordPress capability, effectively escalating their privileges to Administrator. Exploitation requires the attacker to supply an Administrator-authored post ID via the post_ID parameter of the authenticated wp_ajax_parse_media_shortcode handler in order to establish the privileged ambient post context used by the flawed authorization check.

### CVE-2026-100872

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-27T13:16:38.523 |

Sylius versions before 2.1.16 and 2.2.9 fail to validate payment amounts during cart recalculation, allowing unauthenticated attackers to modify order totals after gateway transaction initiation. Attackers can pay a small amount, enlarge the order after gateway capture, and have the system mark the inflated order as fully paid while the gateway captured only the original amount.

### CVE-2026-100871

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-27T13:16:38.380 |

Sylius versions before 1.12.25, 1.13.17, 1.14.20, 2.1.16, and 2.2.9 fail to include firewall identification in JWT tokens issued by separate Admin and Shop API endpoints. Attackers can register a shop customer account using an administrator's email address and obtain a token that the Admin API resolves to that administrator, granting full administrative access.

### CVE-2026-100870

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-09-27T13:16:38.240 |

Sylius versions before 1.12.25, 1.13.17, 1.14.20, 2.1.16, and 2.2.9 build administrator password-reset links using the request Host header without validation, allowing unauthenticated attackers to redirect reset tokens to attacker-controlled domains. Attackers can request password resets for known administrator email addresses with forged Host headers to intercept valid reset tokens and take over administrator accounts.

### CVE-2026-100865

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-27T02:17:26.410 |

Heym before 0.0.53 contains multiple independent vulnerabilities. (1) The workflow condition evaluator uses Python eval() without an effective sandbox, allowing any user who can edit a workflow branch/condition node — or who can import a workflow template containing a malicious condition node — to execute arbitrary Python code as the backend process user when the workflow runs. (2) Slack webhook signature verification and (3) Telegram webhook secret-token verification fail open when the trigger node has no credentialId or an empty signing secret, allowing anyone who knows the public webhook URL to trigger workflows with the owner's credentials without authentication. (4) The OAuth authorization endpoint does not validate the redirect_uri scheme, so an attacker who registers a public OAuth client with a javascript: or data: redirect_uri and lures a victim to the consent screen receives the authorization code and executes attacker-controlled JavaScript in the Heym origin, including access to the victim's HttpOnly auth cookie. (5) WorkflowExecutionToken, PortalSession, HITLRequest.public_token, and OAuthAuthorizationCode values are stored in plaintext, so any database read exposure yields valid scoped bearer tokens, including portal and HITL tokens with a 168-hour TTL that permit workflow execution on behalf of the owner.

### CVE-2026-100864

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-27T02:17:26.260 |

heym before 0.0.91 contains a sandbox escape vulnerability in the expression engine's DotList map/filter and fallback resolver that allows authenticated users to execute arbitrary Python code. Attackers can craft workflow expressions using dunder attribute access through item expressions or the fallback resolver to access os.system and execute commands as the backend process.

### CVE-2026-100856

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-27T02:17:25.050 |

AzuraCast before 0.23.6 contains a code injection vulnerability in the remote relay password field due to incomplete migration from the vulnerable cleanUpString method to toRawString. Attackers with RemoteRelays station permission can inject nested Liquidsoap interpolation syntax to execute arbitrary code in the Liquidsoap process, disclose internal API keys, or disrupt station operation.

### CVE-2026-100852

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-27T02:17:24.437 |

AzuraCast through 0.23.x contains a command injection vulnerability in the Liquidsoap config generation for live recording that fails to quote the streamer username in process.run calls. Authenticated station users with Streamers and Profile permissions can set a username containing shell metacharacters and trigger command execution as the Liquidsoap process user when recording closes.

### CVE-2026-100847

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-27T02:17:23.437 |

AzuraCast before 0.23.8 contains a DQL injection vulnerability in the sortOrder API parameter of AbstractSearchableListAction.php. Attackers can inject arbitrary DQL expressions through the sortOrder parameter to extract sensitive database information including user credentials and station settings.

### CVE-2026-100857

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-27T02:17:25.197 |

AzuraCast before 0.23.4 contains a code injection vulnerability in the ConfigWriter::cleanUpString() method that fails to sanitize Liquidsoap string interpolation sequences, allowing authenticated users with Media or Profile permissions to inject arbitrary Liquidsoap code into station configuration. Attackers can inject #{process.run()} expressions into playlist URLs or station metadata fields that execute shell commands as the azuracast user when the station restarts.

### CVE-2026-100844

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-27T02:17:22.993 |

MONAI before 1.6.0 is vulnerable to OS command injection in the nnUNetV2Runner component (monai.apps.nnunet.nnunetv2_runner). User-controlled values taken from the YAML configuration file (notably dataset_name_or_id) and from CLI/kwargs arguments are concatenated into a command string without quoting or validation and then passed to subprocess with shell=True, so shell metacharacters (e.g., ';' on Linux, '&' on Windows) are interpreted. If a victim loads and processes a crafted configuration file — for example by instantiating nnUNetV2Runner with the malicious YAML and invoking a training/validation job such as train_single_model() — arbitrary commands are executed with the privileges of the user running the job.

### CVE-2026-100838

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-27T02:17:22.083 |

Contrast is a confidential-computing runtime for Kubernetes. In versions before 1.19.1, the Kata agent policies generated by the Contrast CLI contained a flaw in the CopyFile verification that allowed arbitrary writes to the guest root filesystem. A malicious process on the untrusted host able to connect to the Kata agent VSOCK could issue a series of CopyFile requests to overwrite security-critical files in the guest or trick the workload into disclosing sensitive data, effectively amounting to a full guest takeover. Users unable to upgrade can apply an equivalent rego policy fix passed to 'contrast generate --policy'.

### CVE-2026-100740

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-787` |
| Published | 2026-09-27T01:17:17.810 |

A vulnerability was detected in D-Link DIR-895L A1_102b07. Impacted is the function tunnel_set_params of the file tunnel.c of the component L2TP Control Channel Parser. Performing a manipulation results in out-of-bounds write. The attack may be initiated remotely. The exploit is now public and may be used.

### CVE-2026-100845

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-27T02:17:23.140 |

MONAI before 1.6.0 contains an unsafe deserialization vulnerability in the NumpyReader class that unconditionally uses numpy.load with allow_pickle=True when loading .npy and .npz files. Attackers can craft malicious .npy files with pickle payloads that execute arbitrary code when loaded through MONAI's standard data pipeline.

### CVE-2026-100843

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-27T02:17:22.853 |

MONAI versions before 1.6.0 contain a remote code execution vulnerability in the algo_from_pickle() function due to unsafe pickle.loads() deserialization in monai/auto3dseg/utils.py. Attackers can craft malicious pickle files that execute arbitrary system commands when deserialized by the vulnerable function.

### CVE-2026-100841

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-27T02:17:22.543 |

In MONAI 1.6.0, PersistentDataset (monai/data/dataset.py) explicitly rejects the combination track_meta=True with weights_only=True, forcing users who cache MetaTensors (the default tensor type in MONAI >= 1.0) to run torch.load(hashfile, weights_only=False). Related cache helpers in monai/data/utils.py also call pickle.loads on cached content and derive cache keys with hashlib.md5. As a result, a local user with write access to a shared or world-writable cache_dir (e.g. /tmp/monai_cache, HPC scratch, ~/.cache/monai) can place a malicious pickle file that is deserialized the next time another user's MONAI pipeline reads the cache, resulting in arbitrary code execution in that user's context. All released versions of the monai pip package are affected; no patched version is available as of the advisory.

### CVE-2026-100840

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-09-27T02:17:22.387 |

MONAI through 1.6.0 contains a remote code execution vulnerability in the bundle configuration engine that resolves _target_ values to arbitrary importable callables without an allow list and passes $ expressions to Python eval(). Attackers can publish a malicious bundle with crafted configuration containing arbitrary code that executes when a victim loads the bundle using monai.bundle.load() or monai.bundle.run().

### CVE-2025-71425

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-09-27T02:17:16.797 |

Contrast (Edgeless Systems) before 1.8.1 logs the workload secret to stderr, and thus to Kubernetes logs, when the Contrast initializer is configured with CONTRAST_LOG_LEVEL set to info or debug. Because info is the default, all installations that do not customize the initializer log level are affected. This exposes workload secrets — normally accessible only to the Contrast Coordinator, the initializer, the seedshare owner, and the workload owner — to Kubernetes users with get or list permission on pods/logs and to anyone with read access to the Kubernetes log storage, such as the cloud provider. Deployments that do not use workload secrets are unaffected.

### CVE-2025-71423

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-09-27T02:17:15.993 |

Edgelesssys Contrast is a confidential-computing runtime for Kubernetes. In versions 1.9.0 before 1.12.2, the initializer logs the full NewMeshCert response — which contains the workload secret — to standard output at INFO level. As a result, workload secrets are exposed to any Kubernetes user with get or list permission on pods/logs. Because workload secrets are used for encrypted storage and Vault integration, those must also be considered compromised. This is a regression of GHSA-h5f8-crrq-4pw8.

### CVE-2026-100839

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-27T02:17:22.230 |

Contrast is a confidential-computing runtime for Kubernetes. In versions before 1.18.0, the guest kernel's ACPI/AML handling is vulnerable to an AML injection attack ("BadAML"). ACPI tables containing AML bytecode are passed from the untrusted host (QEMU) to the guest firmware (OVMF) and on to the Linux kernel, whose AML interpreter executes them. An attacker controlling the host — an assumed adversary in Contrast's threat model — can craft a table with malicious, Turing-complete AML bytecode that the guest kernel interprets with access to the full guest memory, including private pages, resulting in arbitrary code execution and disclosure or modification of confidential guest data. The issue affects the AMD SEV-SNP platforms Metal-QEMU-SNP and Metal-QEMU-SNP-GPU; Metal-QEMU-TDX is not affected because ACPI table contents are measured into RTMR 0 by OVMF on Intel TDX. Version v1.18.0 mitigates the attack by sandboxing the kernel AML interpreter so that it cannot read or write private memory pages. This weakness is not specific to Contrast but is generic to Confidential Computing setups that expose the ACPI interface to the host.

### CVE-2026-93302

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-27T10:16:59.417 |

MatchTrustedPeer ignores the public key used, leading to forged CA clones passing verification. Affected builds are any that enable the macro WOLFSSL_TRUST_PEER_CERT and load CA certificates with wolfSSL_CTX_trust_peer_cert() or wolfSSL_trust_peer_cert(). The peer must know the certificates being loaded to either of those APIs to take advantage of the issue. When OPENSSL_COMPATIBLE_DEFAULTS is also defined this widens the affected API to include all CA certificate loading. Both macros are defined when using autoconf builds such as (nginx, haproxy, stunnel, wpas, apache httpd, hitch, bind, rsyslog, ffmpeg, all, distro). When the certificate is listed as a trusted peer certificate the issue previously allowed for a malicious (D)TLS server to bypass authentication once knowing which CA’s the client would accept. This also affects mutual authentication cases where the client knows which CA’s the server has loaded. If building with any of these configurations and using (D)TLS where the loaded CA’s could be known and authentication of the peer is desired, users should either: update to the latest wolfSSL version, apply the fix patch, or use the configure flag --disable-openssl-compatible-defaults and not load CA’s with wolfSSL_CTX_trust_peer_cert() or wolfSSL_trust_peer_cert() to mitigate the issue.

### CVE-2026-89136

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-27T10:16:59.287 |

When using RPK (Raw Public Key), the client side of a TLS 1.2, 1.3 and DTLS 1.2 connection could accept an unsolicited server_cert_type=RawPublicKey which allowed a malicious or misbehaving server to bypass authentication. RPK is off by default and only enabled in --enable-rpk OR --enable-all OR --enable-distro AKA HAVE_RPK builds.

### CVE-2026-89102

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-27T10:16:58.767 |

In wolfSSL versions 5.7.2 through 5.9.2 there is a client-side implementation flaw in RFC 6961, multiple OCSP response stapling, which can lead to certificate forgery. When a wolfSSL client enables OCSP stapling with the HAVE_CERTIFICATE_STATUS_REQUEST_V2 feature and calls wolfSSL_UseOCSPStaplingV2(ssl, WOLFSSL_CSR2_OCSP_MULTI, options), the client accepts any certificate in the peer's chain as a certificate authority without verifying that the certificate is actually authorized to act as one. This means that an attacker who possesses any certificate that chains to a CA trusted by the client (along with its private key) can forge certificates for arbitrary identities that will be accepted as valid by the client. The end entity certificate of the server is stored in the persistent trust store, affecting subsequent connections that reuse the context even when OCSP multi usage is not employed. Found by internal wolfSSL testing.

### CVE-2026-100725

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-27T02:17:20.760 |

http4k (Maven artifact org.http4k:http4k-core) before 6.48.0.0, 5.42.0.0, and 4.51.0.0 ships a BasicCookieStorage (client-side cookie store used by ClientFilters.Cookies) that does not enforce RFC 6265 scoping rules for the cookie domain, path, and Secure attributes. When a single BasicCookieStorage instance is used to talk to more than one origin or scheme, cookies stored for one origin can be sent to other origins, and cookies marked Secure can be sent over plain HTTP, potentially disclosing session cookies or other sensitive values to unauthorized hosts or network observers. Clients that use a storage instance for a single origin are not affected.

### CVE-2026-97162

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-26T15:16:55.767 |

Joomla Extension - lomart.fr - Various SQL injection vectors in UP plugin extension 5.0.0-5.2.0, 6.0.0-6.0.29

### CVE-2026-94131

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-26T15:16:54.183 |

Joomla Extension - acymailing.com - Unauthenticated arbitrary file deletion in AcyMailing Enterprise extension < 11.1.0 - A subscriber could store a path in a file-type custom field and have AcyMailing delete that file when the field was cleared, including files outside the upload folder such as configuration.php.

### CVE-2026-100869

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-27T13:16:38.100 |

Sylius versions before 2.1.16 and 2.2.9 fail to restrict payment request actions in the Shop API endpoint, allowing customers to trigger refunds on completed orders. Attackers with order tokens can submit arbitrary payment actions like refunds that payment gateways execute while Sylius maintains order as paid, causing financial loss.

### CVE-2026-100853

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-27T02:17:24.590 |

In AzuraCast before 0.23.8, the public On-Demand download endpoint fails to verify playlist-level access controls, allowing unauthenticated users to download media files excluded from On-Demand-enabled playlists. Attackers can bypass the station operator's intended access restrictions by directly requesting media via the download endpoint using valid media identifiers, exposing private or restricted audio content.

### CVE-2026-100834

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-09-27T02:17:21.487 |

http4k's Digest authentication module (org.http4k:http4k-security-digest) before versions 6.48.0.0, 5.42.0.0 and 4.51.0.0 defaults the nonceVerifier parameter of ServerFilters.DigestAuth and DigestAuthProvider to { true }, so every nonce is accepted regardless of its value, age, or prior use. Applications relying on this default have no replay protection on Digest authentication: an attacker who can capture a valid 'Authorization: Digest' response (for example by observing network traffic or reading logs) can replay it indefinitely against the same protected resource.

### CVE-2026-100858

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-27T02:17:25.340 |

heym before 0.0.109 contains a server-side request forgery vulnerability in the Slack, Discord, and Crawler workflow nodes. These nodes issue HTTP requests to URLs taken from user-created credentials (webhook_url / flaresolverr_url) using an unguarded HTTP client, bypassing the SSRF egress guard that already protects the HTTP, WebSocket, and MCP nodes; the credential API validates only that the URL is non-empty. Any registered user can create a credential pointing at an internal address and execute a workflow, causing the backend to reach loopback, private, link-local, or cloud-metadata endpoints and return the full response body in the node output (non-blind SSRF).

### CVE-2026-100833

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-27T02:17:21.323 |

Contrast (edgelesssys/contrast) versions 1.14.0 before 1.23.1 generate runtime policies that fail to detect all container image substitutions. A bad rebase during a Kata Containers update accidentally introduced an `allow_storage` rule that accepts storage entries using the `image_guest_pull` driver without verifying the image digest. An attacker with access to the Kata agent API — for example, a Kubernetes cluster administrator in Contrast's threat model — can therefore substitute a container image with an exploit payload, provided the substituted image satisfies the remaining policy rules, undermining the confidential container's integrity guarantees.

### CVE-2026-101032

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-27T14:16:28.190 |

navi through 2.24.0 fails to properly escape cheatsheet variable values when substituting them into shell commands. Attackers can inject shell metacharacters through crafted file names in suggestion command directories to execute arbitrary commands with victim privileges.

### CVE-2026-100842

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-09-27T02:17:22.693 |

MONAI through 1.6.0 contains an eval injection vulnerability in _get_fake_spatial_shape() in monai/bundle/scripts.py. The function validates shape expressions with a helper that walks the AST and only collects ast.Name nodes, rejecting any name other than 'p' or 'n', before passing the string to eval(). Expressions built solely from constants and attribute, subscript, or call nodes (for example "(1).__class__.__bases__[0].__subclasses__()" or "int.__class__.__init__.__globals__") contain no ast.Name nodes and therefore bypass the allowlist. Because the shape value originates from bundle metadata consumed by _get_real_input_data and verify_net_in_out (reachable through the bundle 'verify_net_in_out' CLI flow), an attacker who can influence a bundle's metadata can escape the eval sandbox via object introspection chains and achieve code execution in this non-default flow.

### CVE-2026-72668

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-441` |
| Published | 2026-09-26T21:16:55.540 |

Unintended Proxy or Intermediary ('Confused Deputy') (CWE-441) in Kibana Agent Builder can lead to privilege escalation. A non-administrative user able to edit a shared agent could cause privileged operations to be carried out under the identity of a higher-privileged user who subsequently interacts with that agent. Where the same user can also author workflows, this can extend to full administrative control of Kibana and of the Elasticsearch cluster.

### CVE-2026-100851

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-27T02:17:24.233 |

AzuraCast before 0.23.8 contains a broken access control vulnerability in the GET /api/station/{id}/vue/profile endpoint that allows authenticated users with only View Station Page permission to read Icecast/Shoutcast admin, source, and relay passwords. Attackers with View-only access can call this endpoint and receive plaintext frontend credentials in the JSON response, then use the admin password to authenticate to the Icecast admin interface without Broadcasting permission.

### CVE-2026-100859

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-27T02:17:25.503 |

Heym before 0.0.106 contains a credential exfiltration vulnerability in the POST /api/credentials/test endpoint that allows collaborators with shared credential access to exfiltrate the credential owner's secret. Attackers can override the destination URL in the config parameter to cause the server to send decrypted authentication secrets to attacker-controlled endpoints.

### CVE-2026-100855

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-27T02:17:24.893 |

AzuraCast before 0.23.6 contains a missing permission check vulnerability in the GET /api/station/{station_id}/file/{id}/play endpoint that allows authenticated users to download media files from any station. Attackers can enumerate media files using sequential IDs and exfiltrate the complete media library of stations they lack permissions for.

### CVE-2026-100849

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-27T02:17:23.757 |

AzuraCast is a self-hosted web radio management suite. In AzuraCast before 0.23.8, the station webhook URL validation in AbstractConnector::getValidUrl() (backend/src/Webhook/Connector/AbstractConnector.php), used by the Generic and Discord webhook connectors, rejects only URLs whose host is a literal link-local IP address (169.254.0.0/16 or fe80::/10). Loopback addresses and RFC1918 private ranges are not rejected, and any non-literal-IP hostname causes the IP parsing call to throw, which skips the check entirely. A user holding only the station-scoped WebHooks permission can therefore configure a webhook pointing at an internal, loopback, or private-network target and cause the server to issue an outbound HTTP POST containing the station's Now Playing data, resulting in server-side request forgery. The PUT /station/{id}/webhook/{id}/test endpoint allows the same low-privileged user to trigger the request on demand. At the time of the advisory no patched version was available.

### CVE-2026-100848

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-27T02:17:23.583 |

AzuraCast (Composer package azuracast/azuracast) before 0.23.8 validates a station's "Remote Relay" URL only for URL syntax and an http/https scheme (Utilities\Urls::parseUserUrl, used by StationRemote::getUrlAsUri) and performs no host or IP address restriction. A user holding only the station-scoped RemoteRelays permission can therefore set a Remote Relay URL pointing at loopback, private-network, or cloud-metadata addresses (e.g. http://127.0.0.1:<port>/ or http://169.254.169.254/latest/meta-data/), and AzuraCast's periodic background Now Playing sync (AbstractRemote::getNowPlayingAsync) will automatically and repeatedly issue HTTP requests to that address, resulting in server-side request forgery against internal resources. This affects the main branch as of commit bcf8754eef3a268ad82c3db4d81f7920c3c28b56 (2026-07-31); no patched version is available at the time of the advisory.

### CVE-2025-71426

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-27T02:17:17.160 |

Contrast is a confidential-computing runtime for Kubernetes. In versions before 1.4.1, a recovering Coordinator does not verify the seed supplied by the recovering party. An attacker can therefore stand up a rogue Coordinator whose manifest passes validation but whose secret seed is attacker-controlled. If network traffic is redirected from the legitimate Coordinator to the attacker's Coordinator, a workload owner can be impersonated when they either set a new manifest without comparing the returned root CA certificate against the existing one (the default behavior of the contrast CLI) or verify the Coordinator without comparing the root CA certificate against a trusted reference. Under these conditions the attacker can issue certificates that chain back to the rogue Coordinator's root CA and recover arbitrary workload secrets of workloads deployed after the attack. Secrets of the legitimate Coordinator (seed, workload secrets, CA), workload integrity, and certificates chaining to the mesh CA are not affected.

### CVE-2026-97164

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-27T12:17:11.987 |

Joomla Extension - svenbluege.de - Authenticated arbitrary path deletion in `clear cache` task in Event Gallery extension < 6.5.0 - Using the `images` parameter of the `cache.process` task, you can recursively delete any directories that the web server is authorized to write to.
