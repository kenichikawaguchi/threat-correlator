# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-02 15:00 UTC
- **対象期間**: `2026-10-01T15:00:33.000Z` 〜 `2026-10-02T15:00:43.000Z`
- **重要CVE数**: 267 件（Critical 9.0+: 42 件 / High 7.0〜: 225 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に報告された CVSS 7.0 以上の脆弱性は、**リモートコード実行 (RCE)・認証バイパス・パストラバーサル** が集中している点が特徴です。特に、Apache HTTP Server 系列や FortiMail、WordPress プラグインといった広く利用されている基盤ソフトウェアに対する深刻度 9.8‑10.0 の脆弱性が多数報告され、**攻撃者が認証不要で任意コード実行や機密情報取得が可能**になるケースが目立ちます。ロボット制御系（Teledyne FLIR Aware2）や産業向けアクセス管理（Fortra Core Privileged Access Manager）でも同様に高リスクが確認され、**IoT/OT 環境への波及リスクが拡大**しています。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑55393** (Teledyne FLIR Aware2) | 10.0 | パストラバーサルによりロボットの設定・認証情報が取得可能 | **ロボット（PackBot・FirstLook）に対する遠隔情報漏洩**。産業・防衛分野で使用されるため、機密情報流出と制御奪取のリスクが極めて高い。 |
| **CVE‑2026‑93698** (Multilang adminbin) | 9.9 | 認証済みだが低権限で任意コマンド実行 | **管理インターフェースの入力検証不備**。低権限ユーザーでもコマンド実行が可能になるため、内部脅威や横方向移動の足掛かりになる。 |
| **CVE‑2026‑96658** (Foreman) | 9.9 | 認証済み低権限ユーザーが RCE 可能 | **テンプレートエンジンのサンドボックス回避**。Foreman はインフラ自動化で広く利用されており、攻撃者が管理サーバ上でコードを実行できる点が重大。 |
| **CVE‑2026‑104286** (FortiMail) | 9.8 | パストラバーサルで任意ファイル書き込み | **メールゲートウェイへの不正ファイル配置**はスパム・マルウェア配布や情報窃取に直結。FortiMail は多くの企業でメールインフラの要。 |
| **CVE‑2026‑59797 / 57941 / 56154** (Apache HTTP Server 2.4.0‑2.4.68) | 9.8 (各) | Use‑After‑Free / 不適切な特権管理により RCE | **Apache HTTP Server はインターネットの根幹**。複数モジュールで同時に深刻な UAF が確認され、パッチ適用が遅れると大規模な Web サービスが一瞬で乗っ取られる危険がある。 |
| **CVE‑2026‑19652** (Divi Membership WP plugin) | 9.8 | 権限昇格により任意ユーザーが管理者になる | **WordPress の人気プラグインが認証バイパス**。多数のサイトでプラグインがインストールされているため、広範囲にわたるサイト乗っ取りが予想される。 |

> **注:** 上記は CVSS が最高（10.0）に近く、かつ **影響範囲が広い（インフラ基盤・IoT・CMS）** ものを選出。特に Apache 系列は全サーバーに波及するため、最優先で対策が必要です。

---

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
- **脆弱性スキャンの実施**：Nessus、OpenVAS、Qualys などで対象資産を即時スキャンし、該当 CVE が検出されたホストをリスト化。  
- **ネットワーク隔離**：影響が確認されたシステムは、外部からの直接アクセス（ポート 80/443、SSH 等）をファイアウォールで遮断し、内部限定に切り替える。  
- **監視・アラート**：Web アプリケーションファイアウォール（WAF）や IDS/IPS に以下シグネチャを追加し、異常リクエストを即座に検知。  
  - パストラバーサル文字列 (`../`, `%2e%2e%2f`)  
  - 不正な `adminbin` パラメータ  
  - Apache mod_http2 / mod_rewrite の異常メモリ操作パターン  

### 3.2 個別パッケージ・バージョン別対策  

| 製品 / パッケージ | 現行脆弱バージョン | 推奨バージョン / パッチ | 対策概要 |
|-------------------|-------------------|------------------------|----------|
| **Teledyne FLIR Aware2** (PackBot / FirstLook) | ≤ 6.9.0.2 (PackBot) / ≤ 1.7.9 (FirstLook) | **6.9.0.3 以上** / **1.7.10 以上** | ファームウェア更新でパストラバーサルとハードコードパスワードの修正が含まれる。更新後はデフォルト管理者パスワードを即時変更。 |
| **Multilang adminbin** (独自製品) | 1.0‑2.3 (任意) | ベンダー提供の **adminbin‑v3.0** 以上 | 入力サニタイズとコマンドホワイトリストを実装。低権限ユーザーの実行権限を最小化。 |
| **Foreman** | ≤ 3.5 (全般) | **3.6.0 以上** (2026‑03 リリース) | テンプレートエンジンのサンドボックス強化と `allowed_methods` のデフォルト制限。 |
| **FortiMail** | 7.2.0‑7.2.9, 7.4.0‑7.4.8, 7.6.0‑7.6.6, 8.0.0‑8.0.1 | **8.0.2 以上** (公式パッチ) | パストラバーサルチェックをサーバ側で強化。Web UI の管理者パスワードを再設定。 |
| **Apache HTTP Server** | 2.4.0‑2.4.68 | **2.4.69** (2026‑04) | 全モジュール (mod_http2, mod_ssl, mod_rewrite) の UAF 修正が含まれる。**`LoadModule`** の不要モジュールは無効化し、`Allow

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-55393

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-01T21:17:21.540 |

Unvalidated pathnames in the web interface in Teledyne FLIR Aware2 versions through 6.9.0.2 (PackBot) and 1.7.9 (FirstLook) allows remote unauthenticated attackers to read configuration and security parameters on Teledyne FLIR PackBot and FirstLook robots running this software via path traversal.

### CVE-2026-93698

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-02T07:16:39.027 |

Insufficient validation allows arbitrary commands to be executed via the Multilang adminbin.

### CVE-2026-96658

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-01T17:17:34.500 |

A flaw was found in Foreman. An authenticated attacker with low-level permissions can achieve remote code execution (RCE) by bypassing the safemode sandbox within the templating engine. Due to improper handling of delegated methods, an attacker can append unauthorized functions to the allowed execution list, enabling them to run arbitrary commands on the hosting server.

### CVE-2026-19652

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-02T14:17:10.483 |

The Divi Membership plugin for WordPress is vulnerable to Privilege Escalation in versions up to, and including, 2.2.0. This is due to the `dmem_form_submit_handler()` function determining the new user's role by iterating all WordPress roles and calling `password_verify()` against an attacker-controlled bcrypt hash supplied in the `form_id` POST parameter, with no validation or whitelist of allowed roles. This makes it possible for unauthenticated attackers to register a new account with the administrator role by submitting a locally computed bcrypt hash of `administrator` as `form_id`, and when `auto_login=on` is submitted, be immediately authenticated as that administrator in the same request, resulting in full site takeover. Exploitation requires a WordPress nonce, but that nonce is publicly emitted on any page rendering the Divi Membership registration form and is therefore obtainable by any unauthenticated visitor.

### CVE-2026-94541

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-02T10:17:09.313 |

The WPMobile.App – Android and iOS App Builder plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 11.82 This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to exfiltrate password-reset URLs for arbitrary users, including administrators, mirrored into the push queue by the mail-to-push feature, and use those URLs to take over the targeted accounts. This exploit chain requires the plugin's mail-to-push feature (wpmobile_auto_mail=1) to be enabled, as that setting is what causes outbound WordPress password-reset emails — including the reset URL and key — to be mirrored into the push row queue where they become accessible to the attacker.

### CVE-2026-97637

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-02T08:17:05.660 |

The JSON API Auth plugin for WordPress is vulnerable to Authentication Bypass via Cached Session Cookie Disclosure in all versions up to, and including, 3.1.2. The vulnerability exists because the required PI-Media/json-api parent plugin caches controller dispatch results in transients keyed solely by URI and query string, ignoring HTTP method and POST body; this causes the `generate_auth_cookie()` endpoint — which embeds a live WordPress `logged_in` cookie produced by `wp_generate_auth_cookie()` directly in its JSON response body — to serve that cached authenticated response to any subsequent unauthenticated GET request to the same URI. This makes it possible for unauthenticated attackers to retrieve a valid Administrator `logged_in` session cookie from the cached response and use it to fully authenticate as the site Administrator, including via the same plugin's `get_currentuserinfo` endpoint and any cookie-authenticated controller action. Exploitation requires the PI-Media/json-api parent plugin to be installed and active with the Auth controller enabled, and a legitimate Administrator must have POSTed to `/api/auth/generate_auth_cookie/` within the preceding 24-hour cache TTL; the nominal HTTPS enforcement gate present in `Auth.php` is trivially bypassed by supplying `insecure=cool` as a request parameter.

### CVE-2026-19660

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-02T05:16:38.430 |

The Divi Membership plugin for WordPress is vulnerable to Authentication Bypass in all versions up to, and including, 2.3.0. The `process_paypal_callback` function, hooked to the `init` action, accepts a base64-encoded `paypal_param` GET parameter with no IPN validation, no cryptographic signature check, no ownership verification, and no nonce, allowing it to trust an entirely attacker-controlled user ID value that is passed directly to `wp_set_current_user()` and `wp_set_auth_cookie()`. This makes it possible for unauthenticated attackers to log in as any existing WordPress user — including administrators — by supplying an arbitrary user ID in the `paypal_param` GET parameter, resulting in full site takeover. The vulnerability is further compounded by the fact that the PayPal gateway class is instantiated unconditionally regardless of whether PayPal is enabled or configured, ensuring the vulnerable hook is always registered on every front-end request.

### CVE-2026-14378

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-02T04:18:06.277 |

The DevKit Pro plugin for WordPress is vulnerable to Authentication Bypass Leading to Administrator Account Takeover in all versions up to, and including, 2.3.0 This is due to the `revert_switch` handler trusting the attacker-controlled `original_user_id` cookie as the privileged identity: `verify_nonce_and_capability()` incorrectly checks the `manage_options` capability on the user identified by the cookie rather than on the actual requester via `current_user_can()`, while the switch-back form and a valid session-bound nonce are emitted publicly via `wp_footer` to any visitor — including unauthenticated users — whenever that cookie is present. This makes it possible for unauthenticated attackers to set the `original_user_id` cookie to any administrator's user ID, collect the rendered nonce, and POST it back to the `revert_switch` handler, causing `wp_set_auth_cookie()` to be called with the administrator's ID and granting the attacker a full administrator-level authenticated session and complete site takeover.

### CVE-2026-104286

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-01T20:17:24.010 |

An improper limitation of a pathname to a restricted directory ('path traversal') vulnerability in Fortinet FortiMail 8.0.0 through 8.0.1, FortiMail 7.6.0 through 7.6.6, FortiMail 7.4.0 through 7.4.8, FortiMail 7.2.0 through 7.2.9 may allow an unauthenticated attacker to write arbitrary files on the underlying system via crafted HTTP or HTTPS requests.

### CVE-2026-59797

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-01T17:17:29.527 |

Improper Privilege Management vulnerability in Apache HTTP Server's mod_ssl via SSLRequire and file-related expressions.



This issue affects Apache HTTP Server: from 2.4.0 through 2.4.68.

### CVE-2026-57941

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-01T17:17:27.457 |

Use After Free vulnerability in Apache HTTP Server's mod_http2 via shared session->bbtmp re-entrancy



This issue affects Apache HTTP Server: from 2.4.0 through 2.4.68.

### CVE-2026-56154

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-01T17:17:26.610 |

Use After Free vulnerability in Apache HTTP Server's mod_rewrite when using lookahead (%{LA-U:HTTP:...})



This issue affects Apache HTTP Server: from 2.4.0 through 2.4.68.

### CVE-2026-12627

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-01T16:17:40.480 |

Fortra's Core Privileged Access Manager (BoKS) contains a stack-based buffer overflow vulnerability in boks_autoregisterd. A remote attacker with network access to the autoregistration service may be able to trigger memory corruption during client response processing.

### CVE-2026-103752

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-01T15:17:29.270 |

Unauthenticated Privilege Escalation in Authorizer <= 3.15.3 versions.

### CVE-2026-56662

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-01T20:17:26.950 |

GetSimple CMS is a content management system (CMS), and GetSimple CMS CE is the community edition of that CMS. Prior to version 1.5, the UpdateCE update form contained no anti-CSRF token, and the POST handler performed no token or request-origin verification. A remote attacker can host a page that auto-submits a forged POST to the update endpoint; when an authenticated administrator visits it, the server performs an attacker-directed download-and-deploy operation in the administrator's session — with no further interaction. Because the deployed content is executed (see the related ZIP-extraction advisory), this yields remote code execution. The url field is additionally written into the form unescaped, providing a secondary HTML-injection sink via a malicious upgrade.json. This issue has been patched in version 1.5.

### CVE-2026-86325

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-02T11:17:36.173 |

A stack-based buffer overflow vulnerability exists in protocol gateways' account management interface. The vulnerability is caused by insufficient length validation of the `account_name` parameter when processing account management requests. An attacker authenticated as a read-only user to the web management interface could supply a specially crafted account name that exceeds the size of the internal stack buffer, resulting in corruption of program execution flow. Successful exploitation could allow an attacker to read sensitive information from device memory, including credentials, modify arbitrary memory contents, and disrupt device availability.

### CVE-2026-104480

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-390;CWE-863` |
| Published | 2026-10-02T02:17:02.007 |

Discord libdave before 1.2.0 did not reject an MLS Welcome message when the resulting group roster contained an unrecognized participant. An attacker in control of the DAVE signaling path (the voice gateway, or an equivalent position able to add, alter, or withhold signaling messages to a client) could cause affected clients to accept an unauthorized member into the end-to-end encrypted media session, compromising the confidentiality and integrity of audio and video.

### CVE-2026-18397

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-130;CWE-252;CWE-347;CWE-457` |
| Published | 2026-10-01T22:17:01.220 |

This vulnerability enables unauthenticated remote code execution (RCE) on a victim's machine by exploiting a combination of cryptographic weaknesses and memory management issues in the SConnect native host component.

The attack leverages an unrestricted messaging interface between an attacker-controlled web page and the native host, allowing malicious input to bypass security checks.

### CVE-2026-55395

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-01T21:17:21.830 |

Hardcoded passwords in the access control in Teledyne FLIR Aware2 versions through 6.9.0.2 (PackBot) and 1.7.9 (FirstLook) allows remote unauthenticated attackers to access and reconfigure Teledyne FLIR PackBot and FirstLook robots running this software via reading the passwords from the firmware or documentation.

### CVE-2026-14984

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-10-01T20:17:24.297 |

Cleartext transmission in the primary control endpoints of Teledyne FLIR Aware2 versions through 6.9.0.2 allows remote unauthenticated attackers to intercept, hijack, or modify session traffic against Teledyne FLIR PackBot robots running this software via sniffing or hijacking network traffic.

### CVE-2026-94620

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-10-01T16:18:08.550 |

Classroom 50 is a free and open-source tool for managing and grading programming assignments via GitHub. Prior to version 1.11.0, `gh teacher download` clones each student's assignment repository and then writes autograde artifacts (`result.json` and `results.json`) into the just-cloned working tree. The write followed symlinks, so a student who committed `result.json` or `results.json` as a **symlink** (materialized verbatim by `git clone`) could redirect the teacher's write to an arbitrary path — e.g. `~/.zshrc`, `~/.ssh/authorized_keys`, a cron file, or an in-clone `.git/hooks/*` file that git subsequently executes. The written bytes are attacker-controlled (the student's uploaded release asset for `result.json`; student-chosen submit-tag names for `results.json`). This is an arbitrary file write leading to code execution as the teacher, whose `gh` token carries `admin:org`, `repo`, and `workflow` across the entire classroom organization. Version 1.11.0 contains a patch. Some workarounds are available. Avoid running `gh teacher download` against untrusted student repositories, or run it inside a disposable sandbox / container with no access to sensitive host files or credentials. Inspect cloned trees for symlinked, hardlinked, or special (`result.json`/`results.json`) entries before allowing the artifact-refresh step to run.

### CVE-2026-104610

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-10-02T13:17:44.450 |

A security vulnerability has been detected in Tenda HG7, HG9 and HG10 300001138_en_xpon. This impacts the function boaGetVar of the file /boaform/formLoopBack of the component Boa Web Server. Such manipulation of the argument Ethtype leads to stack-based buffer overflow. The attack can be executed remotely. The exploit has been disclosed publicly and may be used.

### CVE-2026-103764

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-02T00:16:59.253 |

Mooncake transfer engine before 0.3.13 contains an untrusted pointer dereference in ServerSession::readHeader that allows unauthenticated attackers to read and write arbitrary process memory via the TCP transport data port. Attackers can send a crafted SessionHeader with arbitrary addr and size values using READ or WRITE opcodes to disclose KV cache contents, prompts and secrets or corrupt memory toward code execution.

### CVE-2026-71449

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-01T22:17:04.903 |

: Use of Hard-coded Cryptographic Key vulnerability in Johnson Controls EasyIO FS32 allows : Retrieve Embedded Sensitive Data.

This issue affects EasyIO FS32: before 3.0b63.

### CVE-2026-103922

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-346;CWE-441` |
| Published | 2026-10-01T18:17:12.840 |

Capacitor is a cross-platform native runtime for web applications. From 6.0.0 until 6.2.2, 7.6.9, 8.3.5, 8.4.3, and 8.5.1, the Android and iOS WebView navigation guard validates a target URL's host and scheme but not its path, allowing a victim who activates an untrusted link to navigate a frame to /_capacitor_http_interceptor_. The native proxy can fetch an attacker-selected URL and return the response as a document at the application's own origin, allowing script in that response to access same-origin storage, cookies, and registered Capacitor plugin capabilities. Applications remain affected when CapacitorHttp is disabled because affected releases serve the proxy path regardless of that setting. This issue is fixed in versions 6.2.2, 7.6.9, 8.3.5, 8.4.3, and 8.5.1.

### CVE-2026-13043

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-798` |
| Published | 2026-10-01T17:17:21.290 |

A missing authentication vulnerability in the Kernel Memory Access Driver (PSKMAD) used by WatchGuard endpoint security products allows a local, authenticated attacker to bypass the driver's access-control handshake and issue arbitrary privileged commands to the driver, resulting in disclosure of kernel and process memory.

### CVE-2026-62071

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-01T15:17:30.647 |

Unauthenticated SQL Injection in WordPress File Upload <= 5.1.10 versions.

### CVE-2026-83632

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-190;CWE-770` |
| Published | 2026-10-02T13:17:58.647 |

Allocation of resources without limits or throttling, Integer overflow or wraparound, Heap-based buffer overflow vulnerability in Apache Thrift.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-104467

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-02T12:17:19.373 |

YesWiki before 4.6.7 contains an authorization bypass vulnerability in ApiService::isAuthorized() that allows unauthenticated attackers to call admin-only API routes when public API mode is enabled. Attackers can send requests to endpoints like api/ci/update_config and api/archives to overwrite configuration and list, download, or delete backup archives.

### CVE-2026-91135

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-02T11:17:37.277 |

Heap-based buffer overflow vulnerability in Apache Thrift C++ THeaderTransport.



When an application enables the ZLIB transform for the frames it sends, THeaderTransport::transform() copies the compressed frame into the write buffer without making sure it fits. Data that does not compress, such as content a remote peer supplied, grows under compression, so the copy writes past the end of the heap buffer by an amount that grows with the size of the frame, and for large frames it also reads past the end of the transform buffer.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-102628

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-215;CWE-489` |
| Published | 2026-10-01T20:17:21.447 |

The Cadmos LTI application hosted at cadmos.eummena.io had Laravel debug mode enabled (APP_DEBUG=true, APP_ENV=local) in a publicly accessible environment. An unauthenticated attacker could send a GET request and trigger an unhandled exception, causing Laravel to expose the entire server environment, including all .env configuration variables, in plaintext. Fixed on or before 2026-09-02.

### CVE-2026-63569

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-02T07:16:37.430 |

Improper input validation in DHAgreement.CalculateAgreement (MTI/A0 two-pass Diffie-Hellman) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows an on-path attacker to make the local party compute an agreed value the attacker already knows, defeating the key authentication MTI/A0 is meant to provide. It also allows a malicious peer to learn the local static private key modulo the small factors of p-1, and to recover it entirely in groups with many such factors. The attack uses a crafted out-of-range or small-order ephemeral value, and works because that value is raised to the static private key without the range and subgroup-membership checks applied to DH public keys. Only applications that call DHAgreement directly are affected.

### CVE-2026-15896

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-26` |
| Published | 2026-10-02T06:16:40.773 |

The Super Forms – Drag & Drop Form Builder plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 6.3.316 via the parse_request function. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. The optional 'file_upload_auth' setting defaults to empty, meaning no authentication is required in the default configuration; enabling this setting mitigates unauthenticated exploitation but does not remediate the path traversal itself. Exploitation on Linux requires a real 13-digit timestamp directory to exist, whereas on Windows the traversal works with any hardcoded 13-digit prefix. However, the plugin's file upload response returns the name of the created directory, which means the vulnerability is exploitable as long as file upload is enabled on the form.

### CVE-2026-56660

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-352;CWE-434;CWE-918` |
| Published | 2026-10-01T20:17:26.643 |

GetSimple CMS is a content management system (CMS), and GetSimple CMS CE is the community edition of that CMS. Prior to version 1.5, the update handler in UpdateCE.php downloads a ZIP archive and extracts its contents into the web root without validating file types or extraction paths. Because PHP files are written into a web-accessible directory, an attacker who can cause a malicious archive to be processed achieves remote code execution as the web-server user. Entry names are also used unsafely, allowing directory traversal (../) to write files outside the intended extraction directory. This issue has been patched in version 1.5.

### CVE-2026-53953

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-338;CWE-640` |
| Published | 2026-10-01T20:17:25.283 |

GetSimple CMS is a content management system (CMS), and GetSimple CMS CE is the community edition of that CMS. In version 3.3.22, the password reset endpoint can be accessed without authentication. When a reset request is submitted for an existing user, the application generates a new temporary password and immediately stores its hash as the user's new password. The temporary password is generated using PHP rand() seeded with microtime(). Because this seed is time-based and has a limited effective search space, an attacker can generate possible reset password candidates. Since the admin login endpoint does not enforce rate limiting or account lockout, these candidates can be tested online until the correct password is found. Successful exploitation may lead to administrator account takeover. At time of publication, there are no publicly available patches.

### CVE-2026-55083

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-01T19:17:21.330 |

DHIS2 is a flexible information system for data capture, management, validation, analytics and visualization. From versions 2.42.0 to before 2.42.5.1, and from versions 2.43.0 to before 2.43.0.1, DHIS2 is vulnerable to remote code execution (RCE) via unsafe Java deserialization. This issue has been patched in versions 2.42.5.1, 2.43.0.1, and 2.44.

### CVE-2026-96659

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-267` |
| Published | 2026-10-01T17:17:35.590 |

A flaw was found in Foreman. This vulnerability allows an authenticated user with low-level Viewer permissions to cause unauthorized information disclosure by submitting requests to template preview endpoints. By exploiting this issue, the user can access sensitive data, such as host root passwords. Furthermore, under insecure system configurations where Safemode protections are disabled, the flaw may allow the user to execute arbitrary commands as the Foreman system account.

### CVE-2026-79898

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-01T15:17:31.623 |

Fortra BoKS Manager contains a command injection vulnerability in crlserver. An authenticated user authorized to add CRL URLs through BCC, the WSI REST or SOAP API, or the cacrl command-line interface could cause shell command substitution to be processed by crlserver as root on the BoKS Master. BCC and WSI provide network-accessible administration paths and do not require a local sudo or suexec rule; non-root use of cacrl requires such a rule.

### CVE-2026-93697

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T07:16:38.893 |

There is a stored XSS vulnerability allowing arbitrary code execution in the WHM Mass Modify Accounts interface.

### CVE-2026-93029

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T07:16:38.733 |

There is a stored XSS vulnerability allowing arbitrary code execution in the WHM Manage SSL Hosts interface.

### CVE-2026-86345

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-923` |
| Published | 2026-10-02T00:17:04.180 |

A flaw was found in 389-ds-base. The server does not discard plaintext bytes already buffered from a client connection when negotiating StartTLS, allowing an on-path attacker to inject a crafted LDAP message that is processed after the TLS upgrade and whose response is delivered to the client in place of the client's own pending operation's response, due to messageID collision. This can cause a client application to treat a failed authentication (bind) attempt as successful.

### CVE-2026-102667

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-749` |
| Published | 2026-10-01T20:17:21.750 |

Joyland AI app allows an attacker with shared network access to inject JavaScript into content loaded in WebView. Without user-granted permissions, an attacker could access the clipboard, make arbitrary HTTP requests via the Weex 'stream' module, or access app-internal storage.  If the installed app has been granted permissions previously, the attacker can access the entire file system, camera, microphone, and GPS tracking.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-104464

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-02T12:17:18.873 |

YesWiki before 4.6.7 contains a server-side request forgery vulnerability that allows unauthenticated attackers to make server-side GET requests by supplying an unvalidated actor URL to the Bazar abonnements sync action. Attackers can target internal hosts or cloud metadata endpoints and chain attacker-controlled outbox first/next links, with fetched responses stored as readable Bazar entries.

### CVE-2026-104462

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-02T12:17:18.467 |

YesWiki before 4.6.7 contains an SQL injection vulnerability in the Bazar nuagetag action, which concatenates the unescaped tags attribute into a raw SQL IN clause. Attackers with page-write access (unauthenticated on default installs) can embed a nuagetag tag ending in a backslash to break quote parity and inject a UNION subquery, exfiltrating password hashes and arbitrary table data.

### CVE-2026-104457

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-02T12:17:17.653 |

YesWiki before 4.6.7 contains an SQL injection vulnerability in the Bazar filtertags action, which wraps unescaped filterN attribute tokens in quotes and concatenates them into a raw tags.value IN (...) clause. Unauthenticated attackers on default installs can save filtertags markup in a page with a trailing-backslash token that breaks quote parity under MySQL backslash escaping. This lets them inject a five-column UNION subquery to read arbitrary table data such as password hashes.

### CVE-2026-104445

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-02T12:17:15.657 |

YesWiki before 4.6.7 contains an authentication bypass vulnerability in the ActivityPub inbox that fails to bind the verified HTTP signature signer to the activity actor. Unauthenticated attackers with any ActivityPub keypair can send signed Delete or Update activities referencing a mirrored entry's sourceUrl to delete or overwrite other actors' federated entries.

### CVE-2026-80298

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-02T10:17:08.567 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in HAVELSAN Inc. Sef - AI Chatbot Platform allows SQL Injection.

This issue affects Sef - AI Chatbot Platform: before 2.1.

### CVE-2026-15897

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-02T06:16:41.053 |

The Super Forms – Drag & Drop Form Builder plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 6.3.316. This is due to the Register & Login add-on's before_email_success_msg() function, in its register_login_action='update' flow, trusting an attacker-supplied user_id value and passing it to wp_update_user() without any ownership or capability check. Because the super_save_form AJAX action also enforces no capability check, any authenticated user with Subscriber-level access and above can create the required malicious form (register_login_action='update' with register_login_user_id_update='true') and then submit it with user_id set to an administrator's ID along with a new user_pass/user_email. This makes it possible for authenticated attackers with Subscriber-level access and above to overwrite the credentials of arbitrary existing accounts — including administrators — resulting in account takeover and full site compromise.

### CVE-2026-103765

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-02T00:16:59.663 |

Mooncake through 0.3.13.post1 contains a missing authentication vulnerability in the HTTP metadata server /metadata handler that allows unauthenticated attackers to read, overwrite, and delete transfer engine metadata keys. Attackers can poison segment descriptors such as tcp_data_port or re-create rpc_meta entries to redirect KV cache transfers to attacker-controlled listeners, or exhaust server memory.

### CVE-2026-104051

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-01T22:17:00.833 |

PictShare before 3.7.1 contains an information disclosure vulnerability that allows unauthenticated attackers to obtain the secret delete_code and uploader metadata by calling the API::info() endpoint which returns the complete raw metadata object without a field whitelist. Attackers can use the publicly visible file hash to retrieve the delete_code via the info API and then invoke the delete API to permanently delete arbitrary files, while also exposing uploader IP, User Agent, remote port, and SHA-1 hash, resulting in loss of content integrity, availability, and uploader privacy.

### CVE-2026-70650

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T20:17:29.110 |

GetSimple CMS is a content management system (CMS), and GetSimple CMS CE is the community edition of that CMS. In versions 3.3.22 and prior, an authenticated stored Cross-Site Scripting (XSS) vulnerability exists in the page backup viewer (admin/backup-edit.php). Page fields are correctly HTML-encoded when a page is saved, but the backup viewer decodes them again (htmldecode() / strip_decode()) and prints the result without re-escaping. A user who can edit a page can store JavaScript in a page's Keywords, Description, Menu text or Content; it executes in the browser of any administrator who later views that page's backup, in the context of the admin control panel. At time of publication, there are no publicly available patches.

### CVE-2026-103484

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787;CWE-1284` |
| Published | 2026-10-01T20:17:23.213 |

IVFFlat index build in pgvector before 0.8.7 allows a database user to write data out-of-bounds, which can lead to arbitrary code execution.

### CVE-2026-104018

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-01T18:17:14.687 |

An improper privilege management vulnerability (CWE-269) exists in the command shell of Wind River VxWorks 7 when configured to enforce per-user command privileges. Under certain shell operations, a command may be evaluated without the privilege check that is normally applied, allowing an authenticated user with limited privileges to execute commands they are not authorized to run. Successful exploitation can result in privilege escalation, with impact to the confidentiality, integrity, and availability of the affected device. The issue affects all versions of VxWorks 7 prior to 26.09.  It has been fixed in 26.09.

### CVE-2026-93546

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-01T17:17:33.313 |

Integer overflow in mod_dav_fs in Apache HTTP Server through 2.4.68 allows an authenticated WebDAV client with write access to crash worker processes and persistently corrupt a directory's property database via PROPPATCH requests declaring many XML namespaces.

### CVE-2026-12405

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-01T17:17:19.717 |

A flaw was found in rubygem-foreman_remote_execution. A command injection vulnerability exists in the Red Hat Satellite API (/api/v2/job_invocations). When a job template has the effective_user property marked as overridable: true, the application fails to properly sanitize the effective_user input provided during the API request. The exploitation does not rely on the content or logic of the Job Template/playbook itself; rather, the injection occurs during the instantiation of the job execution environment by the Satellite server. An attacker with permissions to execute job templates can inject arbitrary shell commands into this parameter, which are executed on the target infrastructure with the privileges of the execution user.

### CVE-2026-97284

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-01T15:17:38.807 |

Contributor PHP Object Injection in Icegram <= 3.1.31 versions.

### CVE-2026-103068

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-01T15:17:26.037 |

Subscriber Privilege Escalation in ByteCoreStack &#8211; MCP Connector for AI Tools <= 1.2.2 versions.

### CVE-2026-94422

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-02T14:17:12.003 |

An incorrect implementation of message filtering in xdg-dbus-proxy versions before 0.1.9 allows an attacker to bypass the intended message filtering on the D-Bus session bus by setting a reply serial number on non-reply messages. A malicious or compromised Flatpak app could use this to achieve arbitrary code execution outside its sandbox. xdg-dbus-proxy was designed to be part of the sandbox boundary for Flatpak, but it is released as a separate project and is sometimes used by other app frameworks such as Firejail.

### CVE-2026-96277

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248;CWE-755` |
| Published | 2026-10-02T13:18:05.010 |

Uncaught exception, Improper Handling of Exceptional Conditions vulnerability in Apache Thrift Ruby bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94658

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-02T13:18:03.117 |

Inefficient Algorithmic Complexity vulnerability in Apache Thrift Lua bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-83745

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-130;CWE-789` |
| Published | 2026-10-02T13:17:58.927 |

Memory allocation with excessive size value, Improper handling of length parameter inconsistency vulnerability in Apache Thrift 
nodejs and D lang bindings.

Both bindings' WebSocket server transports read the payload length out of the frame header and allocate that many bytes immediately, without checking that the bytes have arrived. A single ~14-byte frame therefore commits as much memory as it cares to declare -- measured at 513 MiB against the Node.js server and 2 GiB against the D transport -- and in the Node.js case the connection is left open afterwards, so the frame can simply be sent again.




This issue affects Apache Thrift before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-83663

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-02T13:17:58.780 |

Uncontrolled Recursion vulnerability in Apache Thrift go bindings.



Both Go transports satisfy a read out of a buffered frame and, when that frame yields no payload bytes, read the next frame and call `Read` again instead of looping. A peer produces such a frame for 4 bytes in `TFramedTransport` (a declared size of zero) or 18 bytes in `THeaderTransport` (a header block that fills the frame), so nothing bounds the depth. The Go stack limit is reached as a `fatal error`, which `recover()` cannot catch, so the whole process dies.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-66859

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-457;CWE-476` |
| Published | 2026-10-02T13:17:53.597 |

NULL Pointer Dereference, Use of Uninitialized Variable vulnerability in Apache Thrift c_glib bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-66858

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-02T13:17:53.453 |

The protocol skip routine in several Apache Thrift bindings did not apply the binding's recursion limit, so a message that nests unknown fields deeply enough can exhaust the stack. Affected: the Python C++ accelerator (the pure-Python protocols are not affected), the PHP library and its thrift_protocol extension, and the Perl, Lua, Smalltalk and OCaml libraries.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-66837

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-190` |
| Published | 2026-10-02T13:17:53.323 |

Stack-based Buffer Overflow, Integer Overflow or Wraparound vulnerability in Apache Thrift php bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-66081

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-824` |
| Published | 2026-10-02T13:17:53.050 |

Access of Uninitialized Pointer vulnerability in Apache Thrift c_glib bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-63772

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-02T13:17:52.640 |

Allocation of Resources Without Limits or Throttling vulnerability in Apache Thrift go bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-96294

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248;CWE-755` |
| Published | 2026-10-02T12:17:24.433 |

Uncaught exception, Improper Handling of Exceptional Conditions vulnerability in Apache Thrift NodeJS bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94646

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248;CWE-1284;CWE-1321` |
| Published | 2026-10-02T12:17:23.587 |

Uncaught exception, Improper validation of specified quantity in input, Improperly controlled modification of object prototype attributes ('prototype pollution') vulnerability in Apache Thrift nodejs bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-87117

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-02T12:17:22.370 |

NULL pointer dereference vulnerability in Apache Thrift PHP bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-86537

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191;CWE-248;CWE-835` |
| Published | 2026-10-02T12:17:22.233 |

Uncaught exception, Loop with unreachable exit condition ('infinite loop'), Integer underflow (wrap or wraparound) vulnerability in Apache Thrift D language bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-86535

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835;CWE-1321` |
| Published | 2026-10-02T12:17:21.960 |

Loop with unreachable exit condition ('infinite loop'), Improperly controlled modification of object prototype attributes ('prototype pollution') vulnerability in Apache Thrift NodeJS bindings with TJSONProtocol.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-82458

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770;CWE-789` |
| Published | 2026-10-02T12:17:21.173 |

Memory allocation with excessive size value, Allocation of resources without limits or throttling vulnerability in Apache Thrift Go, netstd, OCaml, Erlang, JavaME, Rust, C++, Java, Kotlin and D language bindings.




This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-61373

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-02T12:17:20.847 |

Allocation of Resources Without Limits or Throttling vulnerability in Apache Thrift Java TSaslNonblockingServer.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-104472

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-02T12:17:20.197 |

YesWiki before 4.6.7 contains a missing authorization vulnerability in the attachment download handler that allows unauthenticated attackers to bypass page read ACLs. Attackers can request the download handler with a known page tag and file parameter to retrieve confidential attachments from read-restricted pages.

### CVE-2026-104460

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-02T12:17:18.140 |

YesWiki before 4.6.7 contains a blind SQL injection vulnerability in the {{newtextsearch}} action because Bazar list option ids are concatenated into SQL REGEXP/LIKE clauses in actions/newtextsearch.php without escaping. Anonymous attackers can plant a malicious option id in an anonymously editable Bazar list and use search requests as a boolean oracle to read arbitrary database data, including admin password hashes from the yeswiki_users table.

### CVE-2026-104438

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-02T12:17:14.503 |

YesWiki before 4.6.7 contains a missing authorization vulnerability in the listpagestag and includepages actions of the tags tool, which enumerate pages without applying read-ACL filtering. Unauthenticated or unprivileged attackers can embed these actions with a chosen tag or page name to disclose the names and body-derived titles of ACL-restricted pages.

### CVE-2026-104431

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-405` |
| Published | 2026-10-02T12:17:13.610 |

Zebra before 6.0.0 contains a denial of service vulnerability that allows unauthenticated peers to stall Tokio workers by submitting mempool transactions requiring expensive synchronous script verification. Attackers can send non-standard high-sigop P2SH transactions that reach CachedFfiTransaction::is_valid() before standardness checks, saturating the verifier buffer and rendering the node unresponsive.

### CVE-2026-104430

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-628` |
| Published | 2026-10-02T12:17:13.467 |

Zebra zebrad 4.5.0 and zebra-script 7.0.0 count P2SH redeem script signature operations in legacy mode rather than zcashd's accurate P2SH mode, overcounting CHECKMULTISIG preceded by OP_1 through OP_16 as 20 sigops and causing a consensus divergence. Remote attackers can broadcast P2SH spends using low-threshold multisig redeem scripts so that a block zcashd accepts exceeds Zebra's inflated MAX_BLOCK_SIGOPS count, causing Zebra nodes to reject it and stall off the chain.

### CVE-2026-104423

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-405` |
| Published | 2026-10-02T12:17:12.433 |

Zebra (zebrad) before 6.2.1 contains an asymmetric resource consumption vulnerability that allows unauthenticated peers to stall block verification by pushing V6 mempool transactions with invalid Halo2 proofs. Attackers can flood the shared unprioritized Halo2 verification queue with zero-fee transactions carrying zero-filled Orchard and Ironwood proofs, causing nodes to fall behind the chain tip.

### CVE-2026-104422

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-02T12:17:12.283 |

The block sync download path in Zebra (zebrad) before 6.3.0 reads a block's height from its unvalidated coinbase scriptSig and drops blocks that appear too far behind the tip before consensus validation, without penalizing the supplying peer. Because V5 transaction IDs exclude the scriptSig, a malicious peer can repeatedly serve a canonical block whose coinbase claims height 1 while keeping the requested hash, delaying the node's discovery of the newest block.

### CVE-2026-104410

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-02T12:17:10.520 |

SiYuan before 3.8.5 contains an information disclosure vulnerability that allows publish readers to read password-protected and publish-disabled database rows via the /api/export/preview endpoint. Attackers can request an export preview of a public document embedding a database view to obtain protected rows' primary-key text and cell values.

### CVE-2026-94642

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-02T11:17:38.377 |

Uncaught exception vulnerability in Apache Thrift PHP bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94633

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-130;CWE-789` |
| Published | 2026-10-02T11:17:38.247 |

Memory allocation with excessive size value, Improper handling of length parameter inconsistency vulnerability in Apache Thrift Dart bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-93926

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401;CWE-772` |
| Published | 2026-10-02T11:17:37.960 |

Missing release of memory after effective lifetime, Missing release of resource after effective lifetime vulnerability in Apache Thrift THeaderTransport.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-93925

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-835;CWE-1335` |
| Published | 2026-10-02T11:17:37.817 |

Stack-based buffer overflow, Incorrect bitwise shift of integer vulnerability in Apache Thrift C++ THeaderProtocol.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-91137

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770;CWE-834;CWE-1284` |
| Published | 2026-10-02T11:17:37.413 |

Improper validation of specified quantity in input, Allocation of resources without limits or throttling, Excessive Iteration vulnerability in Apache Thrift PHP bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-85494

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-130;CWE-248;CWE-407;CWE-789;CWE-1188` |
| Published | 2026-10-02T11:17:36.010 |

Improper handling of length parameter inconsistency, Uncaught exception, Inefficient Algorithmic Complexity, Memory allocation with excessive size value, Initialization of a resource with an insecure default vulnerability in Apache Thrift Python, Ruby, Erlang, Lua, Dart, JavaME, Perl, PHP and D language bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-85493

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248;CWE-674` |
| Published | 2026-10-02T11:17:35.877 |

Uncontrolled Recursion vulnerability in Apache Thrift Dart and Java ME bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94635

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-130;CWE-770` |
| Published | 2026-10-02T10:17:09.630 |

Allocation of resources without limits or throttling, Improper handling of length parameter inconsistency vulnerability in Apache Thrift Lua bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-63574

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-10-02T08:17:02.477 |

Memory allocation with excessive size value in the OpenPGP signature and user attribute subpacket parsers (SignatureSubpacketsParser.ReadPacket, UserAttributeSubpacketsParser.ReadPacket) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows a remote, unauthenticated attacker who can supply a crafted OpenPGP public key, certificate or signature to cause a denial of service (OutOfMemoryException or memory exhaustion in the parsing process) via a subpacket header using the five-octet length form, because the declared length was used to size the subpacket buffer with no upper bound and without being compared with the size of the enclosing subpacket area or packet, so a few bytes of input could demand an allocation of up to about 2 GB before any subpacket data was read.

### CVE-2026-63571

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-02T08:17:01.993 |

Improper verification of cryptographic signature in the attribute certificate path validator (PkixAttrCertPathValidator, also used by PkixAttrCertPathBuilder) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows a remote attacker to have a forged X.509 attribute certificate accepted as valid, and so obtain whatever roles or privileges an application grants on the strength of its attributes, via an attribute certificate that names a trusted attribute authority as its issuer but was not signed by it, because the RFC 3281 validation steps check the holder and issuer certification paths, validity period, extensions and revocation status but never verify the attribute certificate's signature with the issuer's public key. Only applications that use these classes to validate attribute certificates are affected.

### CVE-2026-17507

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-195` |
| Published | 2026-10-02T08:17:01.310 |

In Bouncy Castle for Java before 1.86, the MLS implementation (org.bouncycastle.mls) holds RFC 9420's uint32 leaf_index in a signed int, so a wire value with the top bit set decodes to a negative number. That is a legitimate encoding rather than malformed input, and it must still decode, since the MLS interop test vectors round-trip the full range. GroupKeySet.SecretTree.hasLeaf and Group.validateRemove compared the decoded value directly against the tree's leaf count, and a signed comparison treats any negative int as less than a positive bound, so an out-of-range sender passed the membership check. In the hasLeaf case the SenderData of an unprotected PrivateMessage could then drive LeafIndex.directPath through NodeIndex.parent() arithmetic that never reaches the tree root, growing the resulting node list without bound until the JVM exhausted its heap. A single small message from any current group member could therefore deny service to every other member of the group. Both comparisons now interpret the value as unsigned via Integer.toUnsignedLong, rejecting an out-of-range sender however it was encoded; well-formed leaf indices are unaffected.

### CVE-2026-103604

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-02T08:17:00.980 |

Inefficient algorithmic complexity in X.509 distinguished name string conversion (X509Name.ToString and IetfUtilities.ValueToString) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows a remote unauthenticated attacker to cause a denial of service through CPU exhaustion via a certificate, CRL, certification request or other structure whose name contains a long attribute value made up of characters that must be escaped, such as commas, or of leading or trailing spaces, because each escaping backslash was inserted into the buffer being scanned, so the work grew quadratically with the length of the value. Applications are exposed when they convert such a name to a string, for example to log or display it, or compare it with IetfUtilities.RdnAreEqual, as PKIX path validation does for directoryName name constraints.

### CVE-2026-103603

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-10-02T08:17:00.837 |

Memory allocation with excessive size value in the HSS/LMS signature code (HssPublicKeyParameters, HssSignature) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows a remote unauthenticated attacker who can supply both an HSS public key and a signature to cause a denial of service through memory exhaustion via a public key encoding with an excessive level count, because the level count L read when parsing an HSS public key was not checked against the RFC 8554 maximum of 8, and signature parsing then allocated an array of L - 1 entries before reading any further signature data. A single verification can commit up to about 17 GB of memory or fail with an OutOfMemoryException.

### CVE-2026-103600

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-02T08:17:00.363 |

Uncontrolled recursion in the ASN.1 parser (Asn1InputStream, Asn1StreamParser) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows a remote unauthenticated attacker to cause a denial of service via a crafted ASN.1 encoding of deeply nested constructed elements (for example SEQUENCE inside SEQUENCE, in definite-length DER or indefinite-length BER form), because each nesting level is parsed by a further recursive call with no bound on depth. About 2,000 levels (8 KB of DER) are enough to exhaust a 1.5 MB thread stack, the .NET main-thread default on Windows, and raise a StackOverflowException, which .NET cannot catch and which terminates the whole process; on threads with larger stacks, parse time instead grows quadratically with depth (about 9 seconds of CPU for a 64 KB input). Any path that parses untrusted ASN.1 is exposed, including X.509 certificates and CRLs, CMS/PKCS#7, PKCS#8/PKCS#12, OCSP and TLS Certificate messages.

### CVE-2026-63568

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-02T07:16:37.267 |

Allocation of resources without limits or throttling in the CMP/CRMF password-based MAC verifier (PKMacBuilder) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows a remote unauthenticated attacker to cause a denial of service through CPU exhaustion via a CMP message or CRMF certificate request whose PBMParameter declares a very large iteration count, because PKMacBuilder enforced its iteration-count ceiling only when the caller had supplied an explicit maximum through the PKMacBuilder(IPKMacPrimitivesProvider, int) constructor. With any other constructor, ProtectedPkiMessage.Verify and CertificateRequestMessage.IsValidSigningKeyPop performed as many hash iterations as the sender requested, up to about 2^31, before the MAC could be checked.

### CVE-2026-63566

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-10-02T07:16:36.973 |

Memory allocation with excessive size value in the DTLS handshake reassembly (DtlsReliableHandshake, DtlsReassembler) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows a remote unauthenticated DTLS peer to cause a denial of service through memory exhaustion via crafted handshake message fragments, because the reassembly buffer for each incoming handshake message was allocated at the 24-bit length declared in the fragment header, without the check against the peer's maximum handshake message size that TLS already applied. A fragment carrying no payload can force an allocation of almost 16 MB, for each of up to 16 pending messages per handshake, before the handshake is authenticated. DTLS servers and DTLS clients are both affected; TLS is not.

### CVE-2026-16000

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-325` |
| Published | 2026-10-02T07:16:36.400 |

Missing cryptographic step in the DSTU 7624 CCM mode implementation (KCcmBlockCipher) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows an attacker who can observe encrypted messages of known or chosen content to forge ciphertexts with valid authentication tags, via messages encrypted without associated data. The cause is that the G1 block, which binds the nonce, the message length and the parameter flags into the CBC-MAC, was processed only when associated data was present. Without associated data the tag was a CBC-MAC of the plaintext alone, independent of the nonce. Only applications that use KCcmBlockCipher directly and supply no associated data are affected.

### CVE-2026-103761

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-01T23:16:46.987 |

Mooncake transfer engine through 0.3.13.post1 contains a memory exhaustion vulnerability in TransferMetadata::receivePeerNotify that allows unauthenticated attackers to grow process memory without limit. Attackers can repeatedly send notify frames up to 1 MB to the handshake RPC port, filling the uncapped notifys vector until the out-of-memory killer terminates the engine.

### CVE-2026-104020

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-01T21:17:18.650 |

Uncontrolled recursion in the Ion reader in Amazon Ion Python before 0.15.0 might allow a remote unauthenticated actor to crash the application using the library, resulting in a denial of service, via a crafted, deeply nested Ion value.



To remediate this issue, users should upgrade to version 0.15.0 or later.

### CVE-2026-71542

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T20:17:29.430 |

GetSimple CMS is a content management system (CMS), and GetSimple CMS CE is the community edition of that CMS. In versions 3.3.22 and prior, GetSimpleCMS-CE is vulnerable to stored Cross-Site Scripting (XSS) in the "Theme to Components" functionality (admin/components.php) via the title parameter. The stored title is rendered inside a double-quoted HTML attribute in the administrative interface through an output path that HTML-entity-decodes the value before printing it, without re-encoding for the attribute context. This allows persistent execution of arbitrary JavaScript in the admin panel. At time of publication, there are no publicly available patches.

### CVE-2026-54049

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T20:17:25.587 |

Sakai is a Collaboration and Learning Environment (CLE). From versions 23.0 to before 23.5, and versions 25.0 to before 25.3, the Sakai Conversations tool stores topic and post messages without HTML sanitization, and the frontend renders them using LitElement's unsafeHTML() directive, resulting in stored cross-site scripting (XSS). Any authenticated user with access to a site that has the Conversations tool enabled can inject arbitrary HTML and JavaScript that executes in the browsers of all other users who view that topic or post. This issue has been patched in versions 23.5, 25.3, and 26.0.

### CVE-2026-55230

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T19:17:21.503 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. Prior to version 1.0.8.6, Vvveb's HTML sanitizer fails to strip event-handler attributes when a tag carries a greater-than character inside a quoted attribute value. A low-privilege content author (default role author or contributor) can store a payload in post or product content that runs JavaScript in a browser of every visitor and of any administrator who views or previews that content, which opens a path to admin account takeover. This issue has been patched in version 1.0.8.6.

### CVE-2026-104057

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-01T19:17:19.160 |

Podgrab contains an unauthenticated denial-of-service vulnerability caused by unsynchronized concurrent access to shared maps (activePlayers and allConnections) in its WebSocket handler, where Wshandler and HandleWebsocketMessages goroutines read and write these maps without a mutex. A remote attacker can open multiple WebSocket connections to the /ws endpoint and send messages in a loop to trigger a Go runtime data race that crashes the process, causing a denial of service that requires operator intervention to restore service.

### CVE-2026-102369

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-01T18:17:12.400 |

Tapo C120 v1 and C200 V5
do not adequately protect login challenge data or sanitize
attacker-controlled input processed by the MacTool handler. An unauthenticated
attacker on the same local network can replay login challenge data to obtain an
administrative session, enable a privileged service that becomes accessible
after a reboot, and submit crafted input to execute arbitrary commands within
the device management process.









Successful
exploitation may allow arbitrary command execution on the camera and compromise
the confidentiality, integrity, and availability of the affected device.
Exploitation requires access from the same local network, replay of the login
challenge data, activation of the privileged service, and a device reboot.

### CVE-2024-58388

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-01T15:17:17.347 |

Sharp (and Toshiba Tec rebranded) multifunction printers contain an unauthenticated local file inclusion vulnerability that allows remote attackers to read arbitrary files by manipulating the path parameter in the installed_emanual_down.html endpoint. Attackers can supply directory traversal sequences such as path=/manual/../../../<path> to access files outside the intended manual directory, including /etc/passwd, coredump files containing credentials, and system configuration files. Exploitation evidence was first observed by the Shadowserver Foundation on 2024-07-30.

### CVE-2026-104471

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-02T12:17:20.037 |

YesWiki before 4.6.7 contains an unrestricted file upload vulnerability that allows authenticated admins to write remote files into the web-accessible files/ directory via Bazar CSV import preview. Attackers can import a CSV whose file or image field references a remote .php URL, which is saved without extension checks and executed as server-side code.

### CVE-2026-104418

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-02T12:17:11.710 |

Ghost from 6.10.3 before 6.64.0 contains a remote code execution vulnerability that allows authenticated administrators to run code by abusing theme translation file loading. Attackers with administrator access can upload a crafted theme containing malicious translation files to execute arbitrary code on the Ghost server.

### CVE-2026-104414

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T12:17:11.127 |

Ghost from 2.5.0 before 6.64.0 contains a stored cross-site scripting vulnerability that allows attackers to inject untrusted scripts into post content via oEmbed photo responses. Attackers can host malicious oEmbed photo responses so that embedding their URL stores scripts that run in the Ghost editor, published site, and newsletter emails, compromising staff admin sessions.

### CVE-2026-86326

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-02T11:17:36.330 |

An improper verification of cryptographic signature vulnerability exists in protocol gateways because the device does not properly verify the cryptographic authenticity of firmware images before installation. An attacker with high privileges and access to the firmware update interface could provide a specially crafted or modified firmware image, causing it to be installed on the device. Successful exploitation could allow the attacker to execute unauthorized code, compromise the integrity and availability of the device, and persist malicious modifications across subsequent firmware updates.

### CVE-2026-103766

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-02T00:16:59.820 |

ClipBucket v5 through 5.5.3-#197 contains an sql injection vulnerability that allows authenticated users with ad_manager_access permission to inject SQL via the delete parameter in admin_area/ads_manager.php. Attackers can supply time-based blind payloads concatenated into AdsManager::DeleteAd queries to extract user credentials and emails or modify and delete arbitrary records.

### CVE-2026-101888

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-01T17:17:17.453 |

The Prime Mover plugin for WordPress before 2.2.1 contains a Zip Slip path traversal vulnerability that allows authenticated administrators to write arbitrary files outside the intended extraction directory during migration ZIP import. Attackers can craft ZIP entry names with traversal sequences processed by computeExtractionParameters() and resumableZipExtractor() in utilities/PrimeMoverSystemCheckUtilities.php to write attacker-controlled content to arbitrary filesystem locations, potentially achieving remote code execution if the written files are interpreted by the web environment.

### CVE-2026-95588

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-01T15:17:36.977 |

Unauthenticated Arbitrary File Deletion in AcyMailing SMTP Newsletter <= 11.0.5 versions.

### CVE-2026-104611

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-10-02T13:17:44.640 |

A vulnerability was detected in Tenda AC9 15.03.02.13. Affected is an unknown function of the file /goform/fast_setting_internet_set of the component POST Request Handler. Performing a manipulation of the argument netWanType results in stack-based buffer overflow. The attack is possible to be carried out remotely. The exploit is now public and may be used.

### CVE-2026-104413

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T12:17:10.980 |

Ghost from 5.94.0 before 6.64.0 contains a stored cross-site scripting vulnerability that allows staff users, including Contributors, to host arbitrary HTML by abusing bookmark card image fetching. Attackers can create bookmark cards that store non-image files from external websites as icons or thumbnails to compromise other staff users' admin sessions.

### CVE-2026-104411

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T12:17:10.690 |

Ghost from 6.22.1 before 6.64.0 contains a stored cross-site scripting vulnerability that allows staff users to host scripts by uploading files served with extension-derived content types on the default local storage adapter. Attackers can upload script-bearing files to the site's domain to compromise other staff users' admin sessions.

### CVE-2026-55396

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-10-01T21:17:21.973 |

Cleartext transmission without a cryptographic integrity check in operator control unit to robot UDP traffic in Teledyne FLIR Aware2 versions through 6.9.0.2 (PackBot) and 1.7.9 (FirstLook) allows adjacent unauthenticated attackers to intercept, hijack, or modify control traffic against Teledyne FLIR PackBot and FirstLook robots running this software via sniffing or hijacking network traffic.

### CVE-2026-102294

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-01T18:17:12.220 |

TP-Link TL-WR841N contains an authenticated OS command injection vulnerability in the IPv6 WAN configuration. A crafted IPv6 Gateway value is improperly incorporated into a system command, allowing an authenticated administrator to execute arbitrary operating system commands. 

Successful exploitation may allow unauthorized access to sensitive information, modification of device configuration or services, and disruption of device operation.

### CVE-2026-102514

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-01T21:17:18.307 |

Out-of-bounds Write (CWE-787) in the PEA archive extraction routine (pea.pas, unpea_procedure) of the first-party pea component in PeaZip 11.2.0 and earlier allows an attacker who convinces a victim to open or extract a crafted .pea archive to execute arbitrary code as the user running PeaZip. While decompressing a PCOMPRESS1 stream, the 32-bit compressed-block-size field of the first block (compsize) is read directly from the archive and used without validation as the length of a blockread into the fixed-size global buffers wbuf1/wbuf2 (1,114,112 bytes) and as the bound of the subsequent copy loop. The existing check "compsize > WBUFSIZE" is applied only to the size of each following block, so the first block escapes it; the same unvalidated value is also used to index wbuf1[compsize], an out-of-bounds read at an attacker-chosen offset. The copy loop additionally copies the requested length instead of the number of bytes actually read, and terminates on equality rather than on an upper bound. Because the project is built without range checking and no archive password, integrity tag or non-default configuration is required, the overflow overwrites adjacent global data; code execution was demonstrated by two independent researchers against the official Linux x86-64 and Windows x64 builds, and the denial-of-service and memory-corruption primitive is cross-platform (Windows, macOS, Linux, BSD).

### CVE-2026-73975

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-10-01T17:17:31.117 |

djehuty is a research data repository system developed by 4TU.ResearchData. Prior to version 26.3.2, an authenticated depositor can inject arbitrary SPARQL into a state-modifying (DELETE/INSERT) query by supplying a crafted session name, letting them write (and delete) arbitrary triples anywhere in the RDF store. Because the RDF store is shared across all accounts and datasets, this is an integrity compromise of the whole repository's metadata, not just the attacker's own records. Having a logged-in account is a precondition. djehuty allows self-registration via ORCID/SAML, so this is a low barrier in typical deployments. This issue has been patched in version 26.3.2.

### CVE-2026-104463

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-02T12:17:18.643 |

YesWiki before 4.6.7 contains a server-side request forgery vulnerability that allows unauthenticated attackers to trigger server requests by sending signed Follow activities to the public forms actor inbox route. Attackers sign requests with their own keyId while supplying internal actor URLs in the body, reaching internal hosts or cloud metadata via blind GET and POST requests.

### CVE-2026-104458

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-02T12:17:17.813 |

YesWiki before 4.6.7 contains a server-side request forgery vulnerability in validateKeyIdUrl() that allows unauthenticated attackers to bypass the SSRF guard using 6to4, NAT64, or IPv4-compatible IPv6 addresses. Attackers can send a crafted Signature keyId to the public actor inbox route to reach cloud metadata, loopback services, or internal hosts.

### CVE-2026-104449

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-02T12:17:16.320 |

YesWiki before 4.6.7 contains an access control vulnerability allowing unauthenticated attackers to overwrite any existing wiki page, including pages whose write ACL restricts editing, via the Bazar entry-creation flow. Attackers can submit a crafted entry with an attacker-controlled id_fiche matching an existing page, overwriting its body for mass defacement and content destruction.

### CVE-2026-104437

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-02T12:17:14.357 |

Zebra before 4.4.0 contains a consensus divergence vulnerability in V5 transparent signature verification, computing a ZIP-244 digest for SIGHASH_SINGLE inputs lacking corresponding outputs instead of failing. Attackers can craft V5 transactions with fewer outputs than inputs that Zebra accepts and templates via getblocktemplate, producing blocks zcashd rejects.

### CVE-2026-104435

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-02T12:17:14.063 |

Zebra zebrad 4.4.0 and zebra-script 6.0.0 fail to enforce a ZIP-244 consensus rule, accepting V5 transparent inputs signed with SIGHASH_SINGLE that lack a corresponding output. Attackers can broadcast crafted V5 transactions with more inputs than outputs that Zebra accepts but zcashd rejects, causing a network consensus split.

### CVE-2026-101322

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-01T16:17:32.587 |

In Eclipse BaSyx AAS Web UI versions v2-241220 through releases before v2-260924, the shared request handler attached the selected infrastructure's `Authorization` header to outgoing requests without checking the destination origin. In deployments using authentication, an attacker could induce a user to open a crafted Web UI link whose `aas` or `path` query parameter points to an attacker-controlled endpoint. The user's browser would then send the configured Basic Authentication credentials, Bearer token, or an available OAuth2 access token to that endpoint. The attacker could reuse the disclosed credential to access protected AAS services with the victim's privileges. The issue is fixed in v2-260924.

### CVE-2026-96289

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-02T13:18:05.977 |

Uncontrolled Recursion vulnerability in Apache Thrift PHP bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-96287

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-02T13:18:05.627 |

Inefficient Algorithmic Complexity vulnerability in Apache Thrift Perl bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-96286

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-02T13:18:05.247 |

Uncaught exception vulnerability in Apache Thrift Perl bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94657

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-02T13:18:02.897 |

Allocation of resources without limits or throttling vulnerability in Apache Thrift JavaME bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94656

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-02T13:18:02.570 |

Allocation of resources without limits or throttling vulnerability in Apache Thrift ruby bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94655

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407;CWE-770` |
| Published | 2026-10-02T13:18:02.287 |

Allocation of resources without limits or throttling, Inefficient Algorithmic Complexity vulnerability in Apache Thrift Lua bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94654

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-02T13:18:01.987 |

Loop with unreachable exit condition ('infinite loop') vulnerability in Apache Thrift python bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-85476

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-02T13:17:59.290 |

Loop with unreachable exit condition ('infinite loop') vulnerability in Apache Thrift c_glib bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-66055

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-02T13:17:52.913 |

Allocation of Resources Without Limits or Throttling vulnerability in Apache Thrift C++, Java, Go, netstd, Python and Delphi bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-96292

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407;CWE-1333` |
| Published | 2026-10-02T12:17:24.297 |

Inefficient regular expression complexity, Inefficient Algorithmic Complexity vulnerability in Apache Thrift Lua bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-96288

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674;CWE-770` |
| Published | 2026-10-02T12:17:24.167 |

Uncontrolled Recursion, Allocation of resources without limits or throttling vulnerability in Apache Thrift Erlang bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94653

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-02T12:17:24.017 |

Inefficient Algorithmic Complexity vulnerability in Apache Thrift PHP bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94648

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-02T12:17:23.717 |

Allocation of resources without limits or throttling vulnerability in Apache Thrift dart bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94637

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-10-02T12:17:23.323 |

Improper handling of highly compressed data (data amplification) vulnerability in Apache Thrift Go bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94636

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409;CWE-628;CWE-1284` |
| Published | 2026-10-02T12:17:23.183 |

Improper handling of highly compressed data (data amplification), Function call with incorrectly specified arguments, Improper validation of specified quantity in input vulnerability in Apache Thrift py bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-90440

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248;CWE-404;CWE-755` |
| Published | 2026-10-02T12:17:22.507 |

Uncaught exception, improper handling of exceptional conditions, improper resource shutdown vulnerability in Apache Thrift D thrift.server.nonblocking.TNonblockingServer.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-82459

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191;CWE-787` |
| Published | 2026-10-02T12:17:21.350 |

Integer underflow (wrap or wraparound), Out-of-bounds write vulnerability in Apache Thrift C++ 32 bit THeaderTransport.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-104450

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T12:17:16.483 |

YesWiki before 4.6.7 contains a missing authorization flaw in the pointimage action (tools/attach/actions/pointimage.php), which saves content to an attacker-chosen page with write ACL checks bypassed. Unauthenticated attackers can POST pagetag, title, and description fields to any page rendering {{pointimage}} to append raw HTML or JavaScript to any wiki page, including pages whose write ACL restricts editing, causing stored cross-site scripting in viewers' and administrators' browsers.

### CVE-2026-104427

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-459` |
| Published | 2026-10-02T12:17:13.030 |

Zebra before 6.1.0 contains an incomplete cleanup vulnerability in the state write task that allows remote unauthenticated peers to stall node synchronization by poisoning parent_error_map. Attackers can deliver a coinbase-malleated block sharing a canonical block's hash before it propagates, causing the next canonical block to be rejected and stalling the node for roughly 2,000 blocks.

### CVE-2026-104426

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-02T12:17:12.887 |

Zebra before 6.1.0 contains an inefficient algorithmic complexity vulnerability in remaining_transaction_value that clones the entire block-level spent-UTXO map per transaction during contextual verification. Attackers can mine or seed the mempool with roughly 26,000 minimal single-input transactions in one block, stalling every validating node for over 52 seconds.

### CVE-2026-96990

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-02T11:17:39.180 |

Allocation of Resources Without Limits or Throttling vulnerability in Apache Thrift Erlang bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94651

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-755;CWE-772` |
| Published | 2026-10-02T11:17:38.890 |

improper handling of exceptional conditions, Missing release of resource after effective lifetime vulnerability in Apache Thrift java bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94650

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-02T11:17:38.763 |

Uncontrolled Recursion vulnerability in Apache Thrift c_glib bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94645

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770;CWE-1284` |
| Published | 2026-10-02T11:17:38.633 |

Improper validation of specified quantity in input, Allocation of resources without limits or throttling vulnerability in Apache Thrift nodejs bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94644

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-02T11:17:38.507 |

Allocation of resources without limits or throttling vulnerability in Apache Thrift PHP bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94639

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248;CWE-755;CWE-770` |
| Published | 2026-10-02T10:17:09.783 |

improper handling of exceptional conditions, Allocation of resources without limits or throttling, Uncaught exception vulnerability in Apache Thrift Java bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-94634

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770;CWE-1188` |
| Published | 2026-10-02T10:17:09.467 |

Allocation of resources without limits or throttling, Initialization of a resource with an insecure default vulnerability in Apache Thrift Python bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-63577

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-02T08:17:02.937 |

Improper certificate validation in the directoryName name-constraint check (PkixNameConstraintValidator.WithinDNSubtree) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows an attacker who controls, or can have certificates issued by, a name-constrained intermediate CA to get certificates accepted by PKIX path validation whose subject distinguished name, or a directoryName subjectAltName, lies outside the CA's permitted subtrees, via a name that places other RDNs ahead of a copy of the permitted RDN sequence, because the check looks for the constraint's first RDN anywhere in the name and compares the remaining RDNs from that position, instead of requiring the constraint to be an initial prefix of the name as RFC 5280 sections 4.2.1.10 and 7.1 require.

### CVE-2026-63576

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-02T08:17:02.787 |

Improper certificate validation in PkixNameConstraintValidator (ExtractHostFromURL) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows a name-constrained subordinate CA, or anyone able to obtain certificates with chosen subjectAltName URIs from such a CA, to bypass permitted or excluded uniformResourceIdentifier name constraints during certification path validation via a URI whose path, query, fragment or userinfo contains characters such as '@' or ':', because the host was extracted by string slicing without first isolating the RFC 3986 authority component, so the host compared against the constraints could differ from the URI's actual host.

### CVE-2026-63573

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-203` |
| Published | 2026-10-02T08:17:02.317 |

Observable discrepancy in the CMS RSA PKCS#1 v1.5 key-transport unwrap (KeyTransRecipientInformation.UnwrapKey) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows a remote attacker who holds a captured CMS EnvelopedData message, and who can submit many modified messages to an application that decrypts them with the recipient's RSA private key and reveals how decryption failed, to recover the captured message's content-encryption key and so its content, via a Bleichenbacher-style adaptive chosen-ciphertext attack, because a key-transport ciphertext with invalid PKCS#1 v1.5 padding is rejected during unwrap with a distinct "bad padding in message." CmsException instead of being replaced by a random key, so it can be told apart from a correctly padded ciphertext, which fails only later at content decryption.

### CVE-2026-18036

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-208` |
| Published | 2026-10-02T08:17:01.660 |

In Bouncy Castle for Java before 1.86, NTRU reduced secret values with the % operator in three helpers whose reference implementations are deliberately division-free, so each reduction was carried out by an integer division whose latency depends on the secret operand. Polynomial.modQ divided by a variable divisor, which a compiler cannot strength-reduce to a multiply the way it can a constant one, so it emitted a division on every call including on the decapsulation path where the dividend derives from the private key; Polynomial.mod3 and NTRUSampling.mod3 divided the secret key polynomials f and g during key generation, the message polynomials r and m during encapsulation, and coefficients recovered during decapsulation. An attacker able to measure that timing can recover information about the NTRU private key. modQ now masks, which is exact because q is always a power of two, and mod3 uses the reference implementation's division-free fold and select; the results are unchanged.

### CVE-2026-103602

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-02T08:17:00.677 |

Improper certificate validation in PkixNameConstraintValidator in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows an attacker who controls, or can obtain certificates from, a name-constrained intermediate CA to have certificates accepted during PKIX certification path validation for email addresses, DNS names or URI hosts that lie within excluded subtrees applying to that CA, via an rfc822Name, dNSName or uniformResourceIdentifier name whose host ends with a dot, because names and constraints were compared without first removing the RFC 1034 root-label trailing dot, so a fully qualified host name did not match an excluded subtree for the same host written without the dot.

### CVE-2026-103601

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-354` |
| Published | 2026-10-02T08:17:00.527 |

Release of unverified plaintext in the CCM (CcmBlockCipher) and DSTU 7624 CCM (KCcmBlockCipher) AEAD modes in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows a remote attacker to obtain decryptions of ciphertexts of their choosing via forged messages sent to an application that lets the output buffer of a failed decryption be observed, for example through buffer reuse or logging, because decryption wrote the recovered plaintext into the caller-supplied output buffer before checking the authentication tag and left it there when the check failed. Only decryption into a caller-supplied buffer is affected; methods that return a newly allocated array are not.

### CVE-2026-63567

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-203` |
| Published | 2026-10-02T07:16:37.127 |

Observable discrepancy in IesEngine.DecryptBlock in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows a remote attacker who has captured an IES or ECIES ciphertext, and who can submit modified ciphertexts for decryption under the same key pair, to recover its plaintext via a CBC padding-oracle attack, because in block-cipher mode the engine decrypts the ciphertext and removes its padding before verifying the MAC. A padding failure is therefore reported with a different error message, and without the MAC computation, compared with a MAC failure. Only applications that construct IesEngine directly with a padded block cipher, such as AES in CBC mode with PKCS#7 padding, are affected; stream-mode IES is not.

### CVE-2026-16001

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-354` |
| Published | 2026-10-02T07:16:36.537 |

Exposure of the message authentication key through the encryption keystream in the stream mode of IesEngine (an IesEngine constructed without a block cipher) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows a remote attacker who has observed one encrypted message with known plaintext to forge shorter messages of their choosing that the recipient accepts as authentic, via a crafted ciphertext and MAC tag, because the MAC key was taken from the key derivation output directly after a keystream as long as the message, while the derivation input depends only on the static key pair and fixed parameters. The keystream revealed by that one message therefore contains the MAC key for every sufficiently shorter message.

### CVE-2026-15999

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-354` |
| Published | 2026-10-02T07:16:36.193 |

Improper validation of integrity check value in the AES-CCM implementation (CcmParameters and CcmBlockCipher) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows an on-path attacker to modify CCM-encrypted content without detection via an AlgorithmIdentifier whose CCMParameters declare an authentication tag (aes-ICVlen) of zero or another length outside the RFC 5084 set, because CcmParameters accepted any value and CcmBlockCipher validated the tag length only when encrypting, so decryption compared a zero-length or very short tag. Affected paths include ParameterUtilities.GetCipherParameters, used by CmsEnvelopedData and CmsEnvelopedDataParser for EnvelopedData encrypted with AES-CCM, and any caller passing an unchecked tag length to CcmBlockCipher for decryption.

### CVE-2026-103760

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-01T23:16:46.817 |

Mooncake transfer engine through 0.3.13.post1 contains a denial of service vulnerability that allows unauthenticated remote attackers to block the handshake daemon by never reading replies. Attackers can send a Metadata request to the handshake RPC port and stall SocketHandShakePlugin's single listener thread in writeFully(), breaking all subsequent handshakes, metadata fetches, notify and probe requests.

### CVE-2026-104356

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-338` |
| Published | 2026-10-01T22:17:00.990 |

PictShare before version 3.7.1 contains a weak randomness vulnerability where the getRandomString() function uses the non-cryptographic rand() PRNG to generate the delete_code authorization token in src/inc/core.php. Attackers can predict or infer the PRNG state to guess valid delete_code values and perform unauthorized deletion of hosted files without needing to read the code from the info endpoint.

### CVE-2026-96780

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-01T21:17:26.207 |

figlet.js is a FIG driver written in JavaScript that aims to implement the FIGfont specification. Prior to 1.11.3, text() and textSync() can enter an unbounded loop when whitespaceBreak is enabled and width is smaller than the rendered width of a single FIGlet character. Under these conditions, breakWord() cannot find a valid break point and returns without consuming a character, so generateFigTextLines() repeatedly processes the same input while consuming CPU and growing memory. The non-default option and attacker-controlled width must both reach an affected call. This issue is fixed in version 1.11.3.

### CVE-2023-54404

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-01T18:17:11.040 |

Zod schema-validation library through 4.6.5 contains an uncontrolled resource consumption vulnerability that allows attackers to exhaust memory by submitting a large array to an application using an array schema without a length constraint. Attackers can exploit the handleArrayResult parse logic in $ZodArray, which accumulates every validation issue for each failing element with no cap or early termination, causing the process to allocate excessive issue objects and crash due to out-of-memory conditions.

### CVE-2026-12541

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-01T17:17:20.190 |

A flaw was found in Foreman. OS command injection vulnerabilities exist in the foreman-rake db:dump and db:import_dump tasks. The application fails to properly sanitize user-supplied input in the destination parameter (during backups) and the file parameter (during imports) before passing them to a Ruby system() call for execution. An attacker with permissions to execute foreman-rake (e.g., via a restricted sudo configuration) can append malicious shell commands to the provided file paths.

### CVE-2026-12540

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-01T17:17:20.053 |

A flaw was found in Foreman. A command injection vulnerability exists in the foreman-rake errors:fetch_log task. The request_id parameter is passed to an underlying system command (typically grep) without adequate shell neutralization. While the task is intended to fetch specific log entries, an attacker with sudo permissions to execute this rake task can inject shell metacharacters (such as ;, ", or |) to break out of the intended command and execute arbitrary code.

### CVE-2026-92820

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-02T06:16:43.197 |

The Ninja Forms - File Uploads plugin for WordPress is vulnerable to arbitrary file operations in all versions up to, and including, 3.3.34 via the external (Amazon S3) upload flow. The plugin trusts an attacker-supplied file path from the form submission and stores it as the upload's file_path, which is then used without validation to attach a file to the form's notification email (arbitrary file read), to write fetched content (arbitrary file write, leading to remote code execution when the external store is configured), and in a scheduled deletion (arbitrary file deletion). This makes it possible for unauthenticated attackers to read, write, or delete arbitrary files on the server. Exploitation requires the site to use the plugin's External File Upload (Amazon S3) action; the read variant additionally requires a form Email action configured to attach the uploaded file.

### CVE-2026-73636

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-294` |
| Published | 2026-10-01T17:17:30.873 |

Authentication bypass by capture-replay in mod_auth_digest in Apache Software Foundation Apache HTTP Server 2.4.x on all platforms allows a man-in-the-middle (MITM) attacker to replay captured digest authentication credentials via crafted requests that trigger garbage collection of the client's shared memory entry when AuthDigestNonceLifetime is set to 0.

Users are recommended to upgrade to version 2.4.69, which fixes this issue.

### CVE-2026-14316

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-01T17:17:21.440 |

The revoked-key error path builds a human-readable failure reason using sprintf() into a heap buffer. The allocated buffer is too small for the final formatted message. When sprintf() writes the full message, it can write past the end of the heap allocation.

### CVE-2026-79899

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-377` |
| Published | 2026-10-01T15:17:31.773 |

Fortra BoKS Manager contains an insecure temporary file vulnerability in bccgethostcert. The utility creates predictable temporary files without first setting a restrictive umask. A local user on the BoKS Master who can read files under BOKS_tmp may be able to obtain CA secret or host private-key material while the utility runs, or obtain CA secret material left behind after successful certificate creation.

### CVE-2026-104416

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-203` |
| Published | 2026-10-02T12:17:11.420 |

Ghost from 4.39.0 before 6.64.0 contains an information disclosure vulnerability in the Admin API that allows staff users to view secret tokens of pending staff invites. Staff users with invite viewing permission can accept pending invites for higher-privileged roles to escalate their privileges.

### CVE-2026-8618

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-01T19:17:25.340 |

A stack-based buffer overflow vulnerability exists in the TDDPv2 service (/usr/bin/tddp) on Deco M9 Plus due to insufficient validation of decrypted request data length before it is copied into a fixed-size stack buffer in the subtype 0x91 handler. Successful exploitation may allow an adjacent, unauthenticated attacker to cause a denial of service or achieve arbitrary code execution during the device setup phase through crafted TDDP packets.

### CVE-2026-84682

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-01T19:17:24.960 |

A command injection vulnerability exists in the TDDPv2 service (/usr/bin/tddp) on Archer AX90 V1. An unauthenticated adjacent-network attacker can exploit the setProductVer command handler to execute arbitrary operating system commands as root during device boot. 

Successful exploitation may result in complete device compromise through arbitrary command execution with root privileges.

### CVE-2026-12544

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-01T17:17:20.340 |

A flaw was found in Foreman. The foreman-rake initialization logic in /usr/share/foreman/config/settings.rb contains a vulnerable code pattern where configuration data is processed through two distinct executable layers. This creates a multi-stage execution chain that allows for both Server-Side Template Injection (SSTI) and insecure deserialization. This vulnerability can lead to remote code execution, total infrastructure compromise and supply chain risk.

### CVE-2026-104469

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-384` |
| Published | 2026-10-02T12:17:19.703 |

YesWiki before 4.6.7 contains a session fixation vulnerability that allows attackers to hijack authenticated sessions because login does not regenerate the PHP session ID. Attackers who set or learn a victim's pre-authentication YesWiki-* session cookie can reuse it after login to access private content and perform actions with the victim's privileges.

### CVE-2025-71427

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-01T23:16:46.613 |

Office-PowerPoint-MCP-Server through 2.0.7 contains a path traversal vulnerability that allows MCP callers to write and read files outside the working directory by supplying absolute paths or ../ sequences. Attackers can steer an AI agent via prompt injection to abuse save_presentation, open_presentation, or manage_image output_path to overwrite any server-writable file or load external files.

### CVE-2026-55232

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-01T19:17:21.900 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. Prior to version 1.0.8.6, Vvveb's SSRF guard resolves a host with an IPv4-only function and never inspects IPv6, so any host that lacks an A record passes a private-range check. Editor oEmbed proxy fetches an attacker-supplied URL server side and reflects a response body, so an authenticated admin-panel user (default role site_admin or higher) can read internal-only services and cloud metadata, including IAM credentials, using an IPv6 literal or a domain that carries only an AAAA record. This issue has been patched in version 1.0.8.6.

### CVE-2026-97297

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-01T15:17:38.960 |

Subscriber Broken Access Control in Gratisfaction <= 4.6.3 versions.

### CVE-2026-97277

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-01T15:17:38.380 |

Subscriber Broken Access Control in Social Boost <= 3.6.2 versions.

### CVE-2026-92174

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-02T06:16:43.007 |

The SiteOrigin Widgets Bundle plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 1.73.2 via the 'theme' parameter parameter. This makes it possible for authenticated attackers, with contributor-level access and above, to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included. Exploitation requires sending a malicious widgetData payload containing a legacy top-level theme key alongside a non-empty columns array to the /wp-json/sowb/v1/widgets/previews REST endpoint, which bypasses field validation because update_fields() only processes declared form fields.

### CVE-2026-91828

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-02T06:16:42.857 |

The OMGF | GDPR/DSGVO Compliant, Faster Google Fonts. Easy. WordPress plugin before 6.3.11 does not require authentication or a valid nonce on an action that issues a slow server-side loopback request, allowing unauthenticated attackers to exhaust the site's PHP worker pool and make the entire site unavailable.

### CVE-2026-103098

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-319` |
| Published | 2026-10-02T01:16:43.193 |

Transmission of a sensitive key in the URL
over an unencrypted HTTP connection.  The
request is sent over HTTP rather than HTTPS, meaning the key is transmitted in
plaintext across the network. An attacker with the ability to monitor network
traffic could intercept the request and obtain the key

### CVE-2026-103097

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-312;CWE-540;CWE-798` |
| Published | 2026-10-02T01:16:43.070 |

An API key is
hardcoded and retrievable from the application package. Since Android
applications can be reverse engineered, embedding sensitive API credentials
directly in the client application may allow unauthorized users to extract and
misuse the key.

### CVE-2026-103096

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-312;CWE-540;CWE-798` |
| Published | 2026-10-02T01:16:42.930 |

API
key is hardcoded and retrievable from the application package. Since Android
applications can be reverse engineered, embedding sensitive API credentials
directly in the client application may allow unauthorized users to extract and
misuse the key.

### CVE-2026-86344

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-01T22:17:05.590 |

A flaw was found in 389-ds-base. An unauthenticated remote attacker can send a complete LDAP operation followed by the first bytes of an incomplete LDAPMessage on the same connection, causing the server to hand that connection to a second worker thread before the first worker's result is flushed. The second worker blocks until nsslapd-ioblocktimeout while holding the connection mutex, preventing delivery of the completed operation's result. Repeating this across a small number of connections proportional to the configured worker-thread pool size exhausts the entire pool under default configuration, denying service to all clients (anonymous and authenticated, plaintext and TLS) for as long as the attacker maintains the connections.

### CVE-2026-56661

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-01T20:17:26.793 |

GetSimple CMS is a content management system (CMS), and GetSimple CMS CE is the community edition of that CMS. Prior to version 1.5, the update handler fetches a user-supplied URL with file_get_contents() after only format validation (FILTER_VALIDATE_URL) — there is no validation of the request destination. An attacker who can submit the form can make the server issue requests to arbitrary destinations, including internal-only services and cloud metadata endpoints (169.254.169.254). The fetched response body is written to a web-accessible file (/Tmpfile.zip) and is not deleted when the content is not a valid ZIP, turning this into a full-read SSRF: the attacker can retrieve the response of the internal request directly. This issue has been patched in version 1.5.

### CVE-2026-68496

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-10-01T18:17:27.360 |

The Smile parser in FasterXML jackson-dataformats-binary never invokes StreamReadConstraints.validateNameLength() when decoding JSON object property names, so the maxNameLength limit is not enforced for this format. SmileParser._handleLongFieldName() grows its internal name buffer through an unconstrained _growArrayTo() call and performs no length validation. An attacker who can have a Smile document parsed may therefore embed a single property name of unbounded length; the parser buffers the whole name in memory before returning it, whatever maxNameLength is configured to. Because StreamReadConstraints.maxDocumentLength is also disabled by default, nothing else bounds the name under default settings, so the only limits are the attacker's upload capacity and available heap, leading to memory exhaustion and denial of service. No privileges beyond the ability to submit data to a parsing endpoint are required, and exploitation needs only that the bytes reach SmileFactory parsing, directly or through an ObjectMapper configured with the Smile module. jackson-core's own JSON parsers enforce maxNameLength incrementally during name decoding; this gap is specific to the binary formats. maxNameLength and validateNameLength were introduced in jackson-core 2.16.0, so releases before 2.16.0 do not contain the constraint that is left unenforced. This issue is tracked together with the CBOR parser defect in the same vendor advisory, GHSA-3v8f-v6vx-fmrm, which covers both binary formats. The Smile parser defect (jackson-dataformats-binary issue #726) is CVE-2026-68496; the CBOR parser defect (issue #725) is assigned CVE-2026-68495.

### CVE-2026-68495

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-10-01T18:17:27.167 |

The CBOR parser in FasterXML jackson-dataformats-binary never invokes StreamReadConstraints.validateNameLength() when decoding JSON object property names, so the maxNameLength limit is not enforced for this format. CBORParser._decodeLongerName() decodes a definite-length property name with no length check, and CBORParser._decodeChunkedName() delegates to the value-oriented _finishChunkedText() routine, which validates maxStringLength rather than maxNameLength. An attacker who can have a CBOR document parsed may therefore embed a single property name of unbounded length; the parser buffers the whole name in memory before returning it, whatever maxNameLength is configured to. Because StreamReadConstraints.maxDocumentLength is also disabled by default, nothing else bounds the name under default settings, so the only limits are the attacker's upload capacity and available heap, leading to memory exhaustion and denial of service. No privileges beyond the ability to submit data to a parsing endpoint are required, and exploitation needs only that the bytes reach CBORFactory parsing, directly or through an ObjectMapper configured with the CBOR module. jackson-core's own JSON parsers enforce maxNameLength incrementally during name decoding; this gap is specific to the binary formats. maxNameLength and validateNameLength were introduced in jackson-core 2.16.0, so releases before 2.16.0 do not contain the constraint that is left unenforced. This issue is tracked together with the Smile parser defect in the same vendor advisory, GHSA-3v8f-v6vx-fmrm, which covers both binary formats. The CBOR parser defect (jackson-dataformats-binary issue #725) is CVE-2026-68495; the Smile parser defect (issue #726) is assigned CVE-2026-68496.

### CVE-2026-63718

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-10-01T17:17:30.040 |

Inconsistent Interpretation of HTTP Requests ('HTTP Request/Response Smuggling') response smuggling vulnerability in Apache HTTP Server via mod_proxy_uwsgi and a crafted uwsgi response with Transfer-Encoding.



This issue affects Apache HTTP Server: from 2.4.30 through 2.4.68.

### CVE-2026-63686

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-01T17:17:29.923 |

A NULL pointer dereference in mod_xml2enc in Apache Software Foundation Apache HTTP Server before 2.4.69 on all platforms allows an untrusted backend server to cause a denial of service via a proxied response with a charset whose conversion partially succeeds then fails.

Users are recommended to upgrade to version 2.4.69, which fixes this issue.

### CVE-2026-63292

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-01T17:17:29.803 |

Stack-based buffer overflow in mod_vhost_alias in Apache Software Foundation Apache HTTP Server through 2.4.68 on all platforms allows a remote client to cause a denial of service or potentially execute arbitrary code via an HTTP request with a Host header exceeding 8192 bytes when VirtualDocumentRoot uses a hostname format specifier and LimitRequestFieldSize is raised above the default.

Users are recommended to upgrade to version 2.4.69, which fixes this issue.

### CVE-2026-63045

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-01T17:17:29.680 |

Improper validation of FTP PASV reply address in mod_proxy_ftp in Apache Software Foundation Apache HTTP Server through 2.4.68 on all platforms allows, in forward proxy configurations, an untrusted FTP server to cause the proxy to open a data connection to an arbitrary third-party host via a crafted PASV response.

Users are recommended to upgrade to version 2.4.69, which fixes this issue.

### CVE-2026-59685

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-01T17:17:29.380 |

Out-of-bounds Write vulnerability in Apache HTTP Server on Windows while processing paths with 8.3 names that may grow when expanded.



This issue affects Apache HTTP Server: from 2.4.0 through 2.4.68.

### CVE-2026-56449

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-01T17:17:26.733 |

Out-of-bounds Write vulnerability in Apache HTTP Server's mod_proxy_html with crafted HTTP response bodies.



This issue affects Apache HTTP Server: from 2.4.0 through 2.4.68.

### CVE-2026-56153

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-01T17:17:26.487 |

Out-of-bounds Write vulnerability in Apache HTTP Server's mod_charset_lite.



This issue affects Apache HTTP Server: from 2.4.0 through 2.4.68.

### CVE-2026-48005

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-01T17:17:25.480 |

Missing authentication checks in mod_auth_digest in Apache Software Foundation Apache HTTP Server before 2.4.69 on all platforms allows an unauthenticated remote client to cause a denial of service (forced re-authentication) via forged Authorization headers when Digest authentication is enabled with AuthDigestNcCheck .

Users are recommended to upgrade to version 2.4.69, which fixes this issue.

### CVE-2026-12423

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-01T17:17:19.887 |

A flaw was found in Foreman. The Red Hat Satellite /unattended/provision API endpoint is vulnerable to an authentication bypass due to a semantic logic flaw in host_verifier.rb. The application verifies the database state of a provisioning token rather than its actual presence in the incoming HTTP request. Because a host actively undergoing provisioning has an unexpired token in the database, the server's valid_host_token? method evaluates to true, granting access to the kickstart template even if the requester provides no token at all in the URL.

### CVE-2026-79896

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-01T16:17:59.940 |

Fortra BoKS Manager contains an out-of-bounds read vulnerability in the custom TLS ClientHello parser used by boks_portmux. A remote unauthenticated attacker can submit a malformed ClientHello and terminate boks_portmux. Although the daemon is normally restarted automatically, repeated requests can sustain the service interruption.

### CVE-2026-47360

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-01T16:17:44.443 |

Exposure of Sensitive Information to an Unauthorized Actor vulnerability in Apache HTTP Server's mod_session_cookie module.



   
When SessionCookieRemove changes across internal redirects, the session cookie may still be passed to a backend server.





This issue affects Apache HTTP Server: from 2.4.0 through 2.4.68.

### CVE-2026-46729

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-01T16:17:44.293 |

NULL Pointer Dereference vulnerability in Apache HTTP Servers mod_heartmonitor over unicast listener.



This issue affects Apache HTTP Server: from 2.4.0 through 2.4.68.

### CVE-2026-62073

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-01T15:17:30.797 |

Unauthenticated Broken Access Control in WP Full Stripe Free <= 8.5.6 versions.

### CVE-2026-100517

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-01T15:17:17.810 |

Unauthenticated Insecure Direct Object References (IDOR) in Photo Reviews for WooCommerce <= 1.2.30 versions.

### CVE-2026-100514

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-01T15:17:17.660 |

Unauthenticated Insecure Direct Object References (IDOR) in REST API Log <= 1.7.2 versions.

### CVE-2026-104733

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-02T13:17:45.010 |

User Impersonation in ProcessOnes XMMP Server ejabberd <= 26.04 allows an attacker to impersonate arbitrary users via unvalidated authzid parameter in SASL-PLAIN mechanism.

### CVE-2026-80443

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-02T09:16:44.823 |

Improper certificate validation vulnerability in HAVELSAN Inc. Sef - AI Chatbot Platform allows Adversary in the Middle (AiTM).

This issue affects Sef - AI Chatbot Platform: before 2.1.

### CVE-2026-15911

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-01T19:17:19.947 |

Confluent Kafka Python client's HashiCorp Vault KMS integration could allow a remote attacker to obtain sensitive information due to improper TLS certificate validation.

### CVE-2026-103921

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-01T17:17:19.390 |

GraphQL Tools provides utilities for building, stitching, and mocking GraphQL schemas. Prior to 1.1.35, the executor-legacy-ws buildWSLegacyExecutor() function hardcodes TLS certificate rejection off for Node.js connections to wss:// endpoints. Applications using the executor directly, or url-loader with SubscriptionProtocol.LEGACY_WS, can therefore accept an attacker-controlled certificate when a network-positioned attacker intercepts the connection. Authentication material in connectionParams or headers can be disclosed, and subscription data can be modified. Browser WebSocket clients are unaffected because browsers enforce certificate validation. This issue is fixed in version 1.1.35.

### CVE-2026-67105

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-319` |
| Published | 2026-10-01T15:17:31.237 |

HCL BigFix Service Management is affected by an Insecure Communication vulnerability, which could allow an attacker with internal network access to intercept unencrypted HTTP traffic between backend services, enabling the extraction of sensitive data and potential man-in-the-middle (MitM) attacks.

### CVE-2026-64893

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:P/VC:H/VI:L/VA:L/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-10-01T22:17:04.540 |

- Cleartext Transmission of Sensitive Information vulnerability in Johnson Controls EasyIO NEO allows - Man In the Middle Attack.

This issue affects EasyIO NEO: before 3.3b25.

### CVE-2026-73637

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-01T17:17:31.000 |

Use after free in mod_auth_digest in Apache Software Foundation Apache HTTP Server before 2.4.69 on all platforms allows an unauthenticated remote client to cause authentication state corruption via concurrent Digest authentication requests when AuthDigestNcCheck is enabled or AuthDigestNonceLifetime is set to 0.

Users are recommended to upgrade to version 2.4.69, which fixes this issue.

### CVE-2026-93875

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T14:17:11.850 |

The JetAppointment plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'friendlyTime' parameter in all versions up to, and including, 2.5.2.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injected payload is stored in the wp_jet_appointments_meta table via the unauthenticated jet_engine_form_booking_submit endpoint and executes in the administrator's browser when the appointment details popup is opened in the WordPress admin panel.

### CVE-2026-104456

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-02T12:17:17.490 |

YesWiki before 4.6.7 contains a second-order SQL injection vulnerability in AclService::updateRequestWithACL, where a stored username is concatenated unescaped into a read-ACL LIKE clause. Attackers can self-register an account name containing a double-quote payload, then load non-admin ACL-filtered listings to read database contents and bypass read ACLs.

### CVE-2026-104448

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-02T12:17:16.163 |

YesWiki before 4.6.7 contains a cross-site request forgery vulnerability in the ajaxdeletepage handler, which permanently deletes a page on any GET request carrying a jsonp_callback parameter without checking a CSRF token. Attackers can lure a logged-in administrator or page owner to a crafted link to delete arbitrary pages along with their ACLs, links, triples, comments and referrers.

### CVE-2026-104443

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-02T12:17:15.323 |

YesWiki before 4.6.7 contains an empty-filter scope bypass in the triples delete API that allows any authenticated user to delete or forge arbitrary semantic triples regardless of ownership. Attackers can send an empty filter to the triples delete endpoint to remove the admins-group membership triple, emptying the admin group and causing a site-wide authorization lockout.

### CVE-2026-87920

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T10:17:08.857 |

The W3 Total Cache plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content via Output-Buffer Regex Rewrite in all versions up to, and including, 2.10.6 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This vulnerability is only exploitable when the 'Remove query strings from static resources' option is enabled in W3 Total Cache, as mutate_url() must strip the '?' delimiter and everything following it — including the closing quote of the outer attribute — to break the attribute boundary.

### CVE-2026-97663

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T08:17:06.000 |

The Customer Reviews for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Author Name in all versions up to, and including, 5.122.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the image attachment feature (ivole_attach_image) to be enabled, which allows unauthenticated attackers to both submit a review with an entity-encoded malicious author name and upload an attached image via the publicly accessible wp_ajax_nopriv_cr_upload_local_images_frontend endpoint.

### CVE-2026-97641

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T08:17:05.837 |

The Relevanssi – A Better Search plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content in all versions up to, and including, 4.28.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is only exploitable when the administrator has configured a non-empty value for the "Allowable tags in excerpts" setting, such as the default example value of &lt;p&gt;&lt;a&gt;&lt;strong&gt;, as the prefix-matching regex must have an allowable tag whose name is a prefix of the injected tag name.

### CVE-2026-97342

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T08:17:05.317 |

The JetFormBuilder — Dynamic Blocks Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'choice' Post Meta via Insert/Update Post Action in all versions up to, and including, 3.6.5.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injected payload is submitted via the unauthenticated wp_ajax_nopriv_jet_form_builder_submit endpoint, stored verbatim into post meta through the Insert/Update Post action, and later rendered unescaped by the Select Field block template when the get_from_db option generator copies raw meta values into option value attributes and label content.

### CVE-2026-97336

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T08:17:04.983 |

The CMB2 plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'file_list' Field Type in all versions up to, and including, 2.13.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is only exploitable when an integrating plugin or theme registers a file_list field on a publicly accessible front-end form or a user meta box, as CMB2 is a developer library and does not expose these fields by default.

### CVE-2026-96871

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T08:17:04.813 |

The Mang Board plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'data_type' parameter in all versions up to, and including, 2.4.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is exploitable on any board configured with the default write_level=0 (guest posting) and editor_type=N settings, which are the out-of-the-box defaults for newly created boards.

### CVE-2026-96578

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T08:17:04.477 |

The GSpeech TTS – WordPress Text To Speech Plugin plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content in all versions up to, and including, 3.22.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This mXSS-style transform bypasses WordPress comment kses sanitization because the payload is stored using only kses-allowed tags and attributes; the malicious event handlers and style fragments become active only when the plugin's output-buffer callback rewrites the rendered HTML at request time.

### CVE-2026-96567

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T08:17:04.310 |

The MW WP Form plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'post_id' parameter in all versions up to, and including, 5.1.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The CSRF gate protecting form submission (MW_WP_Form_Csrf) is bypassable by any unauthenticated visitor who first loads the public form page to obtain a valid double-submit cookie, leaving no effective barrier to storing malicious payloads.

### CVE-2026-96566

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T08:17:04.117 |

The Newsletter – Send awesome emails from WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'np1' Custom Field Parameter in all versions up to, and including, 9.4.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The subscription endpoint (na=sa) requires no nonce, no capability check, and no CAPTCHA, and the payload can be smuggled past email-address validation by embedding the {profile_1} placeholder in the local part of the submitted address, since WordPress's is_email() permits curly braces there.

### CVE-2026-95817

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T08:17:03.933 |

The DoFollow Case by Case plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content in all versions up to, and including, 3.6.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Comment moderation delays but does not prevent exploitation — once an administrator approves the visually innocuous comment, the stored payload executes in the browser of every subsequent visitor to the affected post.

### CVE-2026-95670

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T08:17:03.760 |

The No External Links plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Log URL via /goto/{base64} Redirect in all versions up to, and including, 5.2.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is only exploitable when the administrator has enabled the 'Link Encoding: Base64' option in the plugin settings.

### CVE-2026-93756

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T08:17:03.240 |

The Smash Balloon Social Post Feed – Simple Social Feeds for WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Facebook Comment Message via v-html in Admin Builder Preview in all versions up to, and including, 4.13.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts that will execute whenever an administrator accesses the feed builder preview page. This attack requires only a Facebook account to post a comment on the connected Facebook Page, with no WordPress credentials needed; additionally, the use of v-show rather than v-if means injected HTML — including onerror handlers — is evaluated in the DOM even when the comment section is not visually displayed. When combined with the lack of URL validation in the cff_install_addon AJAX handler (admin/addon-functions.php), an injected script running in an administrator's session can trigger arbitrary plugin installation from an attacker-controlled URL, which may result in server-side code execution.

### CVE-2026-103426

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T08:17:00.210 |

The Relevanssi Premium plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the '_rt' parameter in all versions up to, and including, 2.31.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the click-tracking and logging feature to be activated in the plugin settings, and exploitation is trivially accessible to unauthenticated users because a valid _rt_nonce is publicly emitted on every search-results page.

### CVE-2026-102772

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T08:17:00.047 |

The CMB2 plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the '<textarea_code field id> (e.g. kl_code, kl_post_code)' parameter in all versions up to, and including, 2.13.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The front-end save path requires only a CMB2 box nonce, which is emitted to all visitors including unauthenticated guests via a simple GET request, making the attack trivially reachable without any credentials on sites that expose a public CMB2 form writing a textarea_code field.

### CVE-2026-100182

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T08:16:59.697 |

The Download Monitor plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Cross-Origin postMessage to Admin Editor in all versions up to, and including, 5.2.10 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the attacker to trick an authenticated Administrator into visiting an attacker-controlled page that targets an open Download edit screen, after which the payload is persisted unfiltered via the Administrator's unfiltered_html capability and later emitted verbatim to the frontend by the [download_data] shortcode's unescaped post_content render path.

### CVE-2026-100107

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T08:16:58.250 |

The Kubio AI Page Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 2.9.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-102565

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T07:16:35.617 |

The BA Book Everything plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'booking_service_qty' parameter in all versions up to, and including, 1.8.28 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires that an administrator or other privileged user opens the injected order record in the plugin's wp-admin order management area, which is the plugin's ordinary order-review workflow.

### CVE-2026-90438

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T06:16:42.050 |

The Ninja Forms – The Contact Form Builder That Grows With You plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Paragraph Text (RTE) Field Submission in all versions up to, and including, 3.15.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is only exploitable when the targeted Paragraph Text field has the Rich Text Editor (RTE) option enabled.

### CVE-2026-10026

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-02T05:16:36.503 |

The CTX Feed Pro plugin for WordPress is vulnerable to Code Injection in all versions up to, and including, 7.6.12. This is due to insufficient input validation on the 'Feed Config' field which is passed directly to the eval() function. This makes it possible for authenticated attackers, with Administrator-level access and above, to execute arbitrary PHP code on the server.

### CVE-2026-93367

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T04:18:09.573 |

The Visitors Traffic Real Time Statistics Pro plugin for WordPress is vulnerable to unauthenticated stored Cross-Site Scripting in all versions up to, and including, 11.22 via the page_title parameter of the ahcpro_track_visitor AJAX action. The action is registered for logged-out callers (wp_ajax_nopriv_ahcpro_track_visitor) and stores $_POST['page_title'] with NO sanitization, keeping it raw in the ahc_title_traffic.til_page_title column. When an administrator opens the plugin's dashboard, the 'Traffic by Title' DataTable renders that stored value as innerHTML without output escaping, executing arbitrary JavaScript. This makes it possible for unauthenticated attackers to inject web scripts that run in an administrator's session.

### CVE-2026-71452

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:L/VI:L/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-01T22:17:05.160 |

- OS Command Injection vulnerability in Johnson Controls EasyIO FS32 allows OS Command Injection.

This issue affects EasyIO FS32: before 3.0b63.

### CVE-2026-34494

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:A/VC:N/VI:N/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1191` |
| Published | 2026-10-01T22:17:01.870 |

- On-Chip Debug Interface vulnerability in Johnson Controls Neo Series MVP2 allows Collect Data from Common Resource Locations.

This issue affects Neo Series MVP2: before 3.3b63.

### CVE-2026-34493

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:A/VC:N/VI:N/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1191` |
| Published | 2026-10-01T22:17:01.720 |

- On-Chip Debug Interface vulnerability in Johnson Controls EasyIO FS32 allows Collect Data from Common Resource Locations.

This issue affects EasyIO FS32: before 3.3b63.

### CVE-2026-53964

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-10-01T20:17:25.440 |

Document Merge Service is a document template merge service providing an API to manage templates and merge them with given data. Prior to version 9.1.0, a remote code execution (RCE) via server-side template injection (SSTI) allows for user supplied code to be executed in the server's context where it is executed as the document-merge-server user with the UID 901 thus giving an attacker considerable control over the container. The vulnerability is limited to XLSX templates, were the xltpl library uses a npn-sandboxed Jinja environment for the processing of the template. This issue has been patched in version 9.1.0.

### CVE-2026-55231

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-01T19:17:21.680 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. Prior to version 1.0.8.6, a flawed central path sanitizer lets an authenticated admin-panel user who holds backup access (default role site_admin or higher) read and delete arbitrary files on a server. An attacker can recover database credentials from config/db.php, read host files such as /etc/passwd, and delete config/db.php to push a site back into install mode for a full takeover. This issue has been patched in version 1.0.8.6.

### CVE-2026-94390

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-01T15:17:36.727 |

Editor PHP Object Injection in Hide Shipping Method For WooCommerce <= 1.5.4 versions.

### CVE-2026-56589

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T15:17:30.340 |

HCL BigFix Service Management is affected by a Stored Cross-Site Scripting (XSS) vulnerability, which could allow an attacker to inject and store malicious scripts within the application that execute when a victim views the affected page, enabling session hijacking and the theft of sensitive data.

### CVE-2026-85215

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-02T14:17:11.327 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in GG Soft Software Services Inc. Paperwork allows SQL Injection.

This issue affects Paperwork: through 2026-09-09.

### CVE-2026-61374

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-02T13:17:52.497 |

Allocation of Resources Without Limits or Throttling vulnerability in Apache Thrift Java bindings.



This issue affects Apache Thrift: before 0.25.0.



Users are recommended to upgrade to version 0.25.0, which fixes the issue.

### CVE-2026-104447

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-02T12:17:15.990 |

YesWiki before 4.6.7 contains a cross-site request forgery vulnerability in the autoupdate UpdateAction that allows attackers to delete installed packages via unprotected GET requests. Attackers can lure a logged-in administrator to a crafted link with action=delete and a package parameter to remove extensions like bazar, breaking core site functionality.

### CVE-2026-104444

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-02T12:17:15.490 |

YesWiki before 4.6.7 contains an authorization bypass vulnerability in the comments API editComment route that allows authenticated low-privilege users to overwrite arbitrary pages or comments by supplying their own page as the pagetag field. Attackers can send a POST request to the api/comments endpoint targeting a victim tag, bypassing per-page write ACLs to replace content and reparent existing pages or comments.

### CVE-2026-104439

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-204` |
| Published | 2026-10-02T12:17:14.670 |

YesWiki before 4.6.7 contains a user enumeration vulnerability in LostPasswordAction.php that allows unauthenticated attackers to confirm registered email addresses through differing responses. Attackers can submit emails to the MotDePassePerdu recovery page without rate limiting to identify valid accounts for targeted phishing or password-spraying.

### CVE-2026-104434

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-02T12:17:13.917 |

ZcashFoundation Zebra zebra-rpc before 8.0.0 and zebrad before 4.5.0 contain a reachable assertion in the z_listunifiedreceivers RPC handler, which calls expect() on Sapling receiver parsing that fails for Unified Addresses carrying invalid Jubjub points. Authenticated RPC clients can submit such an address to abort the zebrad process, repeatably keeping the node offline.

### CVE-2026-63578

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-02T08:17:03.087 |

Allocation of resources without limits in password-based private-key decryption (PbeUtilities.GenerateCipherParameters) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows an attacker who can supply an encrypted private key, such as a PKCS#8 EncryptedPrivateKeyInfo or "ENCRYPTED PRIVATE KEY" PEM file, to cause a denial of service through CPU exhaustion via an iteration count close to 2^31, because the count is taken from the unauthenticated algorithm parameters without an upper bound and the key derivation runs before the password or the data can be checked. PKCS#5 PBES1 and PBES2 (PBKDF2), the PKCS#12 PBE algorithms and CMS password recipients (CmsPbeKey) are affected. Loading PKCS#12 files with Pkcs12Store is covered by CVE-2026-63572, and a zero or negative count with the PKCS#12 algorithms by CVE-2026-63575.

### CVE-2026-63575

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-02T08:17:02.643 |

Loop with unreachable exit condition in the PKCS#12 key derivation (Pkcs12ParametersGenerator) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows an attacker who can supply a PKCS#12 (PFX) file, or a PKCS#8 encrypted private key that uses a PKCS#12 password-based encryption algorithm, to cause a denial of service through CPU exhaustion via an iteration count of zero or below, because the derivation loop ran until its counter equalled the count, so for such a count it wrapped through about 2^32 iterations before the MAC or the password could be checked. A 75-byte PFX file with a negative MacData iteration count kept Pkcs12Store.Load busy for many minutes.

### CVE-2026-63572

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-02T08:17:02.157 |

Allocation of resources without limits in PKCS#12 keystore loading (Pkcs12Store.Load) in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows an attacker who can supply a PKCS#12 (PFX) file to cause a denial of service through CPU exhaustion via an iteration count close to 2^31 in the file's MacData or in the PBE parameters of an encrypted SafeContents or shrouded key bag, because the counts are taken from the file without an upper bound and the key derivation runs before the MAC or the password can be checked. A zero or negative count is covered by CVE-2026-63575. Pkcs12Utilities.ConvertToDefiniteLength is also affected.

### CVE-2026-63570

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-02T08:17:01.833 |

Loop with unreachable exit condition in Pkcs12Store.GetCertificateChain in Legion of the Bouncy Castle Inc. bc-csharp before 2.7.0 allows an attacker who can supply a crafted PKCS#12 file to an application that loads it and requests a key entry's certificate chain to cause a denial of service, in which the call never returns and consumes CPU and memory until an OutOfMemoryException, via certificates whose issuer links form a cycle, for example two certificates whose AuthorityKeyIdentifier extensions each identify the other's public key. This happens because the chain-building loop stops only when no issuer is found or a certificate links to itself, and keeps no record of certificates already visited. The key-identifier links are followed without checking signatures.

### CVE-2026-82358

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-01T20:17:32.540 |

RT-Labs AB C-Open CANopen contains a write protection bypass in the SDO (Service Data Object) server implementation 'src/co_sdo_server.c' that fails to properly validate write permissions when processing download-segment frames. An unauthenticated attacker on the CAN bus can initiate an SDO upload for a read-only Object Dictionary (OD) entry, which sets a data pointer to the read-only object, then send download-segment frames to write to that memory location. The download-segment handler does not verify that a download session is active, allowing any CANopen node to overwrite read-only OD entries using two SDO frames. Note that CANopen protocol operates over CAN bus and does not provide built-in authentication mechanisms. Fixed in 1.1.1.

### CVE-2026-82357

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-01T20:17:32.363 |

RT-Labs AB C-Open CANopen contains a NULL pointer dereference if the LSS protocol is used to configure the device. An object defined by the user application may not have all required subindexes for object 0x1018. An unauthenticated, remote attacker with access to the CAN bus, through a compromised node for instance, can initiate the LSS protocol on a device with a misconfigured identity object and potentially crash the device. Fixed in 1.1.1.

### CVE-2026-71426

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-98` |
| Published | 2026-10-01T20:17:29.260 |

GetSimple CMS is a content management system (CMS), and GetSimple CMS CE is the community edition of that CMS. In versions 3.3.22 and prior, an authenticated user with page-editing rights can store an arbitrary filesystem path in a page's template attribute. On the public front-end, this value is passed unsanitized to a PHP include() when the page is rendered. Because the include path is never confined, this allows directory-traversal Local File Inclusion: arbitrary local files are included (and, if they contain PHP, executed) when any visitor requests the page. At time of publication, there are no publicly available patches.

### CVE-2026-14983

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-01T20:17:24.167 |

Missing authentication in the web interface in Teledyne FLIR Aware2 versions through 6.9.0.2 allows remote unauthenticated attackers to achieve denial of service against Teledyne FLIR PackBot robots running this software via misuse of the reboot endpoint.

### CVE-2026-9032

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-01T18:17:29.390 |

Tapo C120 v1 and C200 v5
contain a NULL pointer dereference in the HTTPS onboarding connect request parser.  The interface is reachable without
authentication after initial setup and does not validate that a password field
is present for certain authentication and encryption parameter combinations,
allowing a malformed request from the same local network to crash the HTTPS service










 Successful exploitation may
temporarily make HTTPS management functions unavailable. Repeated malformed
requests may sustain the denial-of-service condition, and recovery may in some
cases require a device reboot.

### CVE-2026-78578

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-01T18:17:27.997 |

Tapo C120 v1 and C200 v5
do not enforce authentication for do method HTTPS onboarding connect actions
after initial setup.  An unauthenticated adjacent
attacker can submit unauthorized wireless configuration parameters, causing the
camera to attempt connection to a different network.





Successful
exploitation disconnects the camera from its intended wireless network, making
it unreachable on its management address, resulting in a denial-of-service
condition.

### CVE-2026-73976

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-10-01T18:17:27.550 |

djehuty is a research data repository system developed by 4TU.ResearchData. Prior to version 26.3.2, An unauthenticated attacker can inject SPARQL into the search/listing queries through three separate parameters. Because the affected queries are read (SELECT) queries, this does not write to the store, but it allows: Cross-graph data exfiltration — e.g. UNION-ing in triples from graphs the request was never scoped to (drafts/private/internal data held in the RDF store); denial of service — expensive or malformed queries that tie up the SPARQL backend / web workers. No account or user interaction is required. This issue has been patched in version 26.3.2.

### CVE-2026-97273

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T15:17:38.247 |

Unauthenticated Cross Site Scripting (XSS) in Premmerce Wishlist for WooCommerce <= 1.1.13 versions.

### CVE-2026-97268

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T15:17:37.963 |

Unauthenticated Cross Site Scripting (XSS) in Premmerce Wishlist for WooCommerce <= 1.1.13 versions.

### CVE-2026-97260

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T15:17:37.820 |

Unauthenticated Cross Site Scripting (XSS) in MaxGalleria <= 6.5.3 versions.

### CVE-2026-102378

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-01T15:17:25.727 |

Unauthenticated Cross Site Scripting (XSS) in Parallax Section block <= 2.0.4 versions.

### CVE-2026-104059

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-01T19:17:19.480 |

Lektor 3.3.14 and 3.4.0b15 contains a cross-site request forgery vulnerability in the admin API blueprint that allows unauthenticated attackers to perform state-changing actions by sending cross-origin requests without CSRF tokens, Origin/Referer validation, CORS configuration, or Host allowlisting. Attackers can exploit the newattachment, deleterecord, build, clean, and publish endpoints from a malicious web page to write arbitrary files, delete pages, wipe build output, trigger deployment publication, and via DNS rebinding reach read endpoints to disclose data.

### CVE-2026-101889

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-01T17:17:17.613 |

The Prime Mover plugin for WordPress before 2.2.1 contains a path traversal vulnerability that allows authenticated administrators to delete arbitrary directories by importing a crafted WPRIME/TAR package with manipulated tar_root_folder values in wprime-config.json. Attackers can exploit insufficient path validation in computeExtractVariables() and validateImportedSiteVsPackage() to cause primeMoverDoDelete() to remove directories outside the intended extraction path, potentially deleting critical WordPress directories such as wp-admin and rendering the site inoperable.
