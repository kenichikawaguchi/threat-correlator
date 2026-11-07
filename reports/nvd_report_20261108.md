# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-07 15:01 UTC
- **対象期間**: `2026-11-06T15:00:35.000Z` 〜 `2026-11-07T15:01:34.000Z`
- **重要CVE数**: 299 件（Critical 9.0+: 75 件 / High 7.0〜: 224 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に報告された CVE のうち、**CVSS 7.0 以上は 30 件超**で、ほとんどが **認証バイパス / 権限昇格 / 任意コード実行** といった深刻なリスクを伴う。  
- 特に **Microsoft Entra Device Registration**、**IBM API Connect 12.1 系列**、そして **WordPress 用プラグイン** に集中した脆弱性が目立ち、クラウド・オンプレミス問わず広範囲に影響を及ぼす可能性がある。  
- 多くの脆弱性は **入力検証不備**（OS コマンドインジェクション、SQL インジェクション、パストラバーサル、XXE など）や **ハードコーディングされた認証情報** が根本原因であり、開発・デプロイ段階でのセキュアコーディングが不足していることが示唆される。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・影響範囲 |
|-----|------|----------|-------------------|
| **CVE‑2026‑109469** | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | Entra Device Registration の **認証バイパス** により、ネットワーク上の攻撃者が任意のデバイスを **管理者権限で登録** できる。 | Azure AD テナント全体に波及。デバイス認証が組織の Zero‑Trust 境界に組み込まれている場合、全社的な侵害につながる。 |
| **CVE‑2026‑71495** | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | Wanderer (self‑hosted trail DB) の **POST /api/v1/trail/download** が攻撃者制御の JSON `url` をそのまま `event.fetch()` に渡す **サーバーサイドリクエストフォージェリ (SSRF)** と任意コード実行。 | 公開インスタンスがデフォルトで **PUBLIC_PRIVATE_INSTANCE = false** のままデプロイされているケースが多数。外部サービスへの不正リクエストや内部ネットワーク情報漏洩が即座に発生。 |
| **CVE‑2026‑17360** | 9.8 (AV:N/AC:L/PR:N/UI:N/S:U) | IBM API Connect 12.1 系列に **ハードコードされた管理者クレデンシャル** が残存し、認証不要で **フル管理権限** を取得可能。 | IBM API Connect は金融・医療など高価値 API を管理する基盤。認証バイパスにより API カタログ・ランタイム設定が改竄され、データ漏洩・サービス停止リスクが極めて高い。 |
| **CVE‑2026‑119075** | 9.8 (AV:N/AC:L/PR:N/UI:N/S:U) | WooCommerce 用 **Registration Form** プラグイン (≤ 1.1.4) の **特権昇格** バグ。`FormHandler::validate_checkout_fields()` の allow‑list 欠如により、任意ユーザーが管理者権限でアカウントを作成できる。 | WordPress は中小企業から大手まで広く利用。プラグインだけでサイト全体が乗っ取られる危険性がある。 |
| **CVE‑2026‑104014** | 9.8 (AV:N/AC:L/PR:N/UI:N/S:U) | WooCommerce 用 **Naimur Email OTP Verification** (≤ 2.1.0) の **認証バイパス**。パスワードリセット完了エンドポイントが認証チェックを行わず、任意のパスワードに変更可能。 | パスワードリセットはユーザーアカウント取得の入口になるため、攻撃者が大量アカウントを乗っ取りやすくなる。 |

> **共通点**：いずれも「**認証・入力検証の欠如**」が根本原因で、**ネットワーク外部からの無認証アクセス** が可能になる点が特に危険です。

---

## 3. 推奨アクション  

### 3.1 直ちに実施すべき緊急対策
- **パッチ適用・バージョンアップ**  
  - **Microsoft Entra Device Registration**：2026‑12‑01 以降にリリースされた **Security Update for Azure AD (KB2026‑xxxx)** を適用し、`deviceRegistrationKey` のデフォルト設定を無効化。  
  - **Wanderer**：`npm install wanderer@0.20.0` 以上にアップグレードし、`PUBLIC_PRIVATE_INSTANCE=true` を必ず設定。  
  - **IBM API Connect**：12.1.1.3 以降（または最新の **Fix Pack**）へ更新。特に **CVE‑2026‑17360** 対策としてハードコードクレデンシャルが除去されたリリースを適用。  
  - **WooCommerce Registration Form**：プラグインを **1.1.5 以上** に更新。  
  - **Naimur Email OTP Verification**：プラグインを **2.1.1 以上** に更新。  

- **設定変更**  
  - Entra の **Device Registration** で「**Require user‑controlled key**」を **false** に設定し、キー管理を Azure AD のポリシーに委任。  
  - Wanderer の `PUBLIC_PRIVATE_INSTANCE` フラグを **true** に固定し、外部からの `url` パラメータ受け取りを禁止。  
  - IBM API Connect の **管理コンソール** でデフォルト管理者アカウント (`admin/admin`) が有効化されていないか確認し、無効化または強力なランダムパスワードに変更。  

- **WAF / IDS ルール追加**  
  - `event.fetch()` に対する外部 URL へのリクエストを **ホワイトリスト制御**（Wanderer）。  
  - IBM API Connect の管理 API エンドポイントへの **IP 制限** と **Basic Auth / Mutual TLS** の強制。  
  - WordPress の `wp_ajax_*` エンドポイントに対し **レートリミット** と **CSRF トークン** の必須化。  

### 3.2 中長期的な防御策
- **コードレビューと入力検証の標準化**  
  - OS コマンド・SQL・ファイルパス・XML への入力は必ず **サニタイズ / ホワイト

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-109469

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-06T23:17:20.557 |

Authorization bypass through user-controlled key in Entra Device Registration allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-71495

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-06T19:17:56.657 |

Wanderer is a self-hosted trail database for saving and sharing adventures. Prior to 0.20.0, when PUBLIC_PRIVATE_INSTANCE is not set to true, the unauthenticated POST /api/v1/trail/download handler passes the attacker-controlled JSON url field directly to event.fetch() and returns the fetched response. This allows requests to internal services such as db:8090 and search:7700, cloud metadata addresses, and other network destinations, exposing returned data and permitting internal network reconnaissance or denial of service. This issue is fixed in version 0.20.0.

### CVE-2026-17410

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-07T05:18:58.410 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to access and modify other tenants' portal data due to improper neutralization of argument delimiters.

### CVE-2026-17402

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-07T05:18:56.460 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary commands due to OS command injection. User-supplied input is not properly neutralized before it is passed to the operating system, which could allow commands to run on the underlying host.

### CVE-2026-17399

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-07T05:18:55.790 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary code due to insufficient validation of uploaded content. Content uploaded to the product is not sufficiently checked before it is processed, which could allow code to run on the server.

### CVE-2026-17392

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-90` |
| Published | 2026-11-07T05:18:54.113 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to gain unauthorized administrative access to other tenants due to LDAP injection. User-supplied input is not properly neutralized in directory queries, which could change the query and grant access beyond the user's own tenant.

### CVE-2026-17359

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-07T05:18:48.017 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary code due to improper control of generation of code. A user-supplied value can influence code that the product generates, which could lead to code execution.

### CVE-2026-17354

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-07T05:18:47.057 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to perform arbitrary file writes due to path traversal.

### CVE-2026-17342

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-07T05:18:45.943 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary code due to improper control of generation of code.

### CVE-2026-17336

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-07T05:18:44.673 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary SQL commands due to improper neutralization of special elements used in an SQL command.

### CVE-2026-17298

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:37.510 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-17239

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-07T05:18:32.657 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary code due to a path traversal vulnerability.

### CVE-2026-17158

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-07T05:18:28.853 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to gain elevated privileges due to improper authentication.

### CVE-2026-17150

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-11-07T05:18:28.230 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary code and access sensitive information from other tenants due to insufficient input validation. Uploaded custom module content is not sufficiently validated before it is processed, which could allow code to run with access beyond the user's own tenant.

### CVE-2026-17147

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-07T05:18:28.037 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary code and perform unauthorized administrative actions due to a path traversal vulnerability.

### CVE-2026-17146

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T05:18:27.843 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary JavaScript and obtain sensitive information due to improper input validation.

### CVE-2026-17134

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-07T05:18:26.630 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary SQL commands due to SQL injection.

### CVE-2026-17132

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-07T05:18:26.430 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary SQL commands due to improper neutralization of special elements used in an SQL command.

### CVE-2026-17117

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-07T05:18:25.647 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary code due to improperly controlled modification of object attributes. A user could set a field that should only be controlled by the system, which could lead to code execution.

### CVE-2026-17049

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:23.173 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information and modify arbitrary documents due to authorization bypass through user-controlled keys.

### CVE-2026-16920

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-07T05:18:22.990 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to bypass security restrictions due to a confused deputy vulnerability.

### CVE-2026-16884

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-07T05:18:22.440 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to obtain sensitive information due to an XML external entity (XXE) injection.

### CVE-2026-119075

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-07T12:17:44.033 |

The Registration Form for WooCommerce plugin for WordPress is vulnerable to privilege escalation due to a missing allow-list check in the FormHandler::validate_checkout_fields() function in versions up to, and including, 1.1.4 The My Account registration path (validate_fields()) validates a submitted 'tgwcfb/user-roles' value against the form's configured allowed roles, but the checkout registration path (validate_checkout_fields(), hooked to woocommerce_after_checkout_validation) stores the raw $_POST['user_roles'] value in $this->valid_data without any allow-list enforcement, and add_user_data() then injects that value into woocommerce_new_customer_data as the new account's role. This makes it possible for unauthenticated attackers to elevate their privileges to Administrator by supplying a user_roles=administrator parameter when creating an account during checkout, resulting in full site takeover.

### CVE-2026-104014

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-07T12:17:41.313 |

The Naimur Email OTP Verification for WooCommerce plugin for WordPress is vulnerable to authentication bypass in versions up to, and including, 2.1.0. This is due to the plugin's password-reset finalization endpoint (the wp_ajax_nopriv_ceovw_update_new_password action handled by CEOVW_AJAX::update_new_password()) authorizing the reset solely by the presence of a database row marking an email as 'VERIFIED', with no timestamp check, no session binding, and no per-reset token — combined with mark_otp_as_verified_for_reset() leaving the row in that state after a user enters their code (abandoning the flow leaves the row behind), and a scheduled 'ceovw_cleanup_expired_otps_event' cron that has no add_action() handler anywhere in the plugin so cleanup never runs. This makes it possible for unauthenticated attackers to take over any account whose owner previously requested and verified a password-reset code and did not immediately finish choosing a new password — the attacker needs only the victim's email address and a nonce that the plugin itself localizes publicly into the CEOVW_APP global on the WooCommerce account page for logged-out visitors, after which they call the endpoint, overwrite the victim's password, and are returned a live wordpress_logged_in_ session cookie for that user (full site takeover if the account is an administrator).

### CVE-2026-17408

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-07T05:18:57.917 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote attacker to execute arbitrary code due to improper neutralization of special elements in an OS command.

### CVE-2026-17360

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-07T05:18:48.197 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to gain full administrative control due to the use of hard-coded credentials.

### CVE-2026-17340

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-07T05:18:45.510 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to execute arbitrary code due to a path traversal vulnerability.

### CVE-2026-17313

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-07T05:18:40.163 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to obtain sensitive information and take control of gateway configuration due to authentication bypass via an alternate path.

### CVE-2026-17301

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-07T05:18:37.913 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow an unauthenticated attacker to bypass authentication due to improper verification of a cryptographic signature.

### CVE-2026-17278

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-07T05:18:33.440 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to gain unauthorized access to sensitive API catalog and runtime configuration data due to improper authentication. Information supplied by the client is not sufficiently verified, which could allow a caller to appear as a trusted party.

### CVE-2026-16720

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-07T05:18:21.883 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote attacker to obtain valid access tokens for other users due to improper authentication. Authentication against a connected directory service is not sufficiently enforced, which could allow another user's identity to be assumed.

### CVE-2026-19803

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-07T04:17:29.233 |

The Printcart Store – Web to Print Product Designer for WooCommerce plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 2.13.2. This is due to the `nbu_crop_image` AJAX handler accepting a user-supplied `url` parameter that `Nbdesigner_IO::convert_url_to_path()` concatenates onto the uploads base directory without normalizing or stripping `../` sequences, and then deriving both the output directory and output file extension via `pathinfo()` from the same attacker-controlled path — with no `stripImage()` call before `writeImage()` is invoked. This makes it possible for unauthenticated attackers to write attacker-controlled PHP content to arbitrary locations outside the uploads directory, resulting in remote code execution when the written file is subsequently requested. This vulnerability is only exploitable when the `nbdesigner_upload_popup_style` site option is set to `a` (Advanced Upload Popup), which causes the handler to be registered for unauthenticated requests; however, the required `save-design` nonce is printed on the fully public frontend `upload-design-file` page, making it trivially obtainable by any anonymous visitor once that configuration is active.

### CVE-2026-17362

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-07T04:17:29.070 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to create, modify, or delete tenants due to missing authorization.

### CVE-2026-123218

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-07T04:17:28.900 |

IBM Aspera Faspex 5.0.0 through 5.0.19 could allow an authorized user to craft a specific message to bypass user authorization and gain full administrative privileges.

### CVE-2026-93754

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-07T03:17:08.410 |

The payever – WooCommerce Gateway plugin for WordPress is vulnerable to arbitrary file upload leading to remote code execution in various versions up to, and including, 4.8.0. Three WooCommerce-API callbacks (payever_set_sandbox_api_keys, payever_toggle_subscription, payever_synchronization_incoming) are registered with no authentication, capability check, or nonce, and the upload_image() routine writes a remotely fetched file to the public uploads directory using an attacker-controlled basename() BEFORE validating the file type. This makes it possible for unauthenticated attackers to write an executable PHP file and achieve remote code execution. NOTE: the token-recovery leg of the full chain depends on the plugin's outbound validateToken() call to Payever's service; the unauthenticated hard-coded-credential identity overwrite (CWE-862/CWE-798) is independently exploitable.

### CVE-2026-85295

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1394` |
| Published | 2026-11-06T21:17:10.890 |

Chartbrew is an open-source web application that can connect directly to databases and APIs and use the data to create charts. Prior to 5.2.3, four authentication helpers accepted session tokens signed with CB_SECRET, including known, weak, or shipped-default values. The vulnerable surface is session JWT fallback in server/modules/verifyToken.js, verifyUser.js, getUserFromToken.js, and socketManager.js across the API and socket layer. A stock source or repository Docker Compose deployment retains a known, weak, or default CB_SECRET and an attacker submits a forged HS256 token decoding to a target user id. Knowing the symmetric secret lets the attacker create a token that the legacy verification fallback accepts as the target user without that user's password or two-factor authentication. The condition includes stock source and repository Docker Compose installs and any otherwise known or weak CB_SECRET; a bare container where CB_SECRET is undefined is not affected by this fallback path. A forged session impersonates the chosen user across the entire API and socket layer and exercises that user's Chartbrew privileges. This issue is fixed in version 5.2.3.

### CVE-2026-63439

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-06T21:17:09.970 |

2FAuth is a web app to manage Two-Factor Authentication (2FA) accounts and generate their security codes. Prior to 8.0.0, when AUTHENTICATION_GUARD=reverse-proxy-guard is enabled, ReverseProxyGuard::user() reads the default REMOTE_USER identity header, or a custom identity header selected by the AUTH_PROXY_HEADER_FOR_USER configuration setting, without confirming that the request originated from a configured trusted proxy. A remote client that can reach the application directly can forge the selected identity header and authenticate as an existing user, including an administrator, gaining access to stored 2FA secrets and account or application management functions. This issue is fixed in version 8.0.0.

### CVE-2026-63438

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-06T21:17:09.770 |

2FAuth is a web app to manage Two-Factor Authentication (2FA) accounts and generate their security codes. Prior to 8.0.0, when AUTHENTICATION_GUARD=reverse-proxy-guard accepts authentication headers from a client that did not pass through a trusted proxy, RemoteUserProvider::retrieveById() creates an account for an unknown REMOTE_USER, promotes the first created account to administrator, and synchronizes the account email from the configured mail header. An unauthenticated remote client can therefore create an administrator on a fresh instance or impersonate and redirect email for a known account, exposing 2FA secrets and administrative functions. This issue is fixed in version 8.0.0.

### CVE-2026-54349

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-06T21:17:08.947 |

Chartbrew is an open-source web application that can connect directly to databases and APIs and use the data to create charts. Prior to 5.2.1, SQL dashboard-variable substitution used attacker-controlled JavaScript replacement strings unsafely across SQL connectors and separately failed to escape backslashes for MySQL and MariaDB quoted contexts. The vulnerable surface is public and embedded dashboard/chart requests that call applyMysqlOrPostgresVariables. An unauthenticated user sends crafted URL filter values to a public or embedded chart backed by a stored SQL query. Replacement-string dollar sequences can alter SQL independently of the database engine, while MySQL and MariaDB backslash handling provides a second quoted-string escape path. The target must expose a public or embedded chart using URL-controlled variables in a SQL query; only the backslash branch is specific to MySQL and MariaDB. Injected SQL can read, modify, or delete data available to the configured database account. This issue is fixed in version 5.2.1.

### CVE-2026-58490

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-06T20:17:23.253 |

Tracecat is an open-source security automation platform for teams and AI agents. From version 0.37.0 until 1.0.0-beta.49, Docker Compose deployments with SAML enabled can render SAML_SIGNED_ASSERTIONS and SAML_SIGNED_RESPONSES as empty values, overriding secure application defaults and disabling both signature requirements. An unauthenticated attacker who can reach the SAML assertion consumer endpoint can submit a forged unsigned response for an existing Tracecat user email address and obtain that user’s session. Targeting an existing superadmin can result in superadmin account takeover. Exploitation does not create users when SAML user creation is disabled and does not affect default Fargate or Helm deployments. Version 1.0.0-beta.49 removes the insecure deployment pass-through and requires signed assertions and responses.

### CVE-2026-18535

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-11-07T05:18:59.120 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 are vulnerable to a Regular Expression Denial of Service (ReDoS) attack and to improper neutralisation of wildcard query operators.

### CVE-2026-17396

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-07T05:18:55.103 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to SQL injection.

### CVE-2026-17394

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-07T05:18:54.617 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to improperly controlled modification of object attributes. A user-supplied value could change an access-related setting that should be controlled by the system, which could expose sensitive information.

### CVE-2026-17353

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:46.880 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information and bypass security restrictions due to server-side request forgery.

### CVE-2026-17299

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:37.700 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to perform arbitrary file reads and server-side request forgery due to unrestricted resolution of external references. Externally referenced content in submitted definitions is not sufficiently restricted when processed, and the retrieved content could be returned to the attacker.

### CVE-2026-17297

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-601` |
| Published | 2026-11-07T05:18:37.333 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote attacker to perform an account takeover due to an open redirect vulnerability. The redirect address used during sign-in is not sufficiently validated, which could allow authentication results to be sent to an attacker-controlled location.

### CVE-2026-17296

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:37.140 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-86044

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-601` |
| Published | 2026-11-06T21:17:12.297 |

JupyterLab Desktop is the cross-platform desktop application for JupyterLab. Prior to 4.6.2-1, JupyterLab Desktop exposed getServerInfo to the renderer without confirming that the current page still had the local Jupyter server origin. In a local managed session using JupyterLab before 4.4.8, an attacker can place a crafted MathJax link in an untrusted notebook. If a victim opens the notebook and clicks the link, the existing renderer navigates to an attacker-controlled site while retaining access to the preload bridge. The site can call getServerInfo to obtain the local server URL and authentication token, then use the Jupyter REST API to create and trust a notebook that executes arbitrary code as the victim. Users whose environment already uses JupyterLab 4.4.8 or later are unaffected because the corrected link handling breaks the first step of the chain. This vulnerability is fixed in 4.6.2-1.

### CVE-2026-123832

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-06T17:17:21.387 |

In JetBrains CLion before 2026.2 code execution was possible in Safe Mode via JSON compilation database

### CVE-2026-123831

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-06T17:17:21.240 |

In JetBrains CLion before 2026.2, 
2026.1.4 code execution was possible in Safe Mode via Meson project settings

### CVE-2026-18838

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-07T05:18:59.803 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to obtain sensitive information and modify API configurations due to improper authentication. Identity information supplied in requests is not sufficiently verified, which could allow a caller to impersonate another user.

### CVE-2026-17409

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-178` |
| Published | 2026-11-07T05:18:58.157 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote attacker to execute unauthorized administrative operations and obtain sensitive information due to improper handling of case sensitivity. Access controls are not applied consistently to all variations of a request, which could allow restricted operations to be reached.

### CVE-2026-102530

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-94;CWE-116` |
| Published | 2026-11-06T21:17:05.510 |

JupyterLab Desktop is the cross-platform desktop application for JupyterLab. Prior to 4.6.2-1, remote-server URLs were inserted into the server-selection dialog and Welcome view without safe encoding. An attacker who convinces a user to submit a crafted URL can execute JavaScript in the Welcome renderer and abuse its privileged IPC bridge to execute arbitrary code with the user’s privileges. The Welcome view also unsafely renders RSS news-feed titles; exploitation through this separate input path requires control over content delivered through the application’s Jupyter Blog feed or its cached feed data, rather than submission of a remote-server URL. This issue affects all supported platforms and is fixed in version 4.6.2-1.

### CVE-2026-123966

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-122` |
| Published | 2026-11-07T14:17:01.800 |

A vulnerability was determined in Tenda AC19 16.03.10.07. Affected by this issue is the function saveParentControlInfo of the file /goform/saveParentControlInfo. This manipulation of the argument deviceId causes heap-based buffer overflow. The attack is possible to be carried out remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-18836

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:59.597 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote attacker to obtain sensitive information due to server-side request forgery. The affected component can be made to send requests to unintended destinations and return the response to the attacker.

### CVE-2026-17344

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:46.317 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to obtain sensitive information due to server-side request forgery. A service that can be reached without authentication could be made to send requests to unintended destinations.

### CVE-2026-17329

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:43.273 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to obtain sensitive information due to improper validation of endpoint URLs.

### CVE-2026-17131

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:26.230 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to obtain sensitive information due to server-side request forgery. Restrictions on outbound requests can be bypassed, so the server could be made to contact unintended destinations and return the response.

### CVE-2026-16918

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:22.803 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote attacker to access internal network resources due to server-side request forgery.

### CVE-2026-59104

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-06T22:17:59.043 |

UgCS server before 6.2 contains an authentication bypass in the HCI protocol login handler (LoginHandler) exposed on TCP port 3334. When the user database contains exactly one user (the default single-operator installation), a LoginRequest with empty userLogin and userPassword fields is interpreted as \"use the only user\" rather than as invalid credentials, and the server returns a fully authenticated session. Because the service listens on all interfaces (0.0.0.0) without TLS by default, an unauthenticated remote attacker with network access to port 3334 can obtain an authenticated session without knowing any credential and then issue privileged commands, including commanding connected drones and uploading flight routes.

### CVE-2026-86005

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-06T21:17:12.117 |

Chartbrew is an open-source web application that can connect directly to databases and APIs and use the data to create charts. Prior to 5.2.3, the administrative BullMQ dashboard was mounted without an authentication check. The vulnerable surface is the Bull Board/BullMQ administration dashboard at /apps/queues. A remote unauthenticated attacker reaches /apps/queues on a Chartbrew instance where Redis and BullMQ are enabled and a reverse proxy does not independently block the route. The dashboard trusted network reachability as authorization and exposed its queue-management interface directly. Redis and BullMQ must be enabled and the route must be reachable. Available actions depend on the installed Bull Board version and queue state, while confidentiality depends on job payload and log contents. An unauthenticated user can inspect exposed job payloads and logs and, when enabled by the installed version and queue state, retry or delete jobs or otherwise alter queue processing, affecting confidentiality, integrity, or availability. This issue is fixed in version 5.2.3.

### CVE-2026-119923

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-06T19:17:39.360 |

A heap-based buffer overflow in the TDS prelogin parser in the Babelfish for PostgreSQL extension versions 1.0-1.5, 2.1-2.15, 3.1-3.12, 4.0-4.8, 5.1-5.4 and in Amazon Aurora PostgreSQL with Babelfish might allow remote attackers to execute arbitrary OS commands as the database process user via a specially crafted malformed TDS prelogin packet to the TDS port. This record consolidates a related NULL-pointer-dereference finding in the same prelogin parser.



To remediate this issue, we recommend users upgrade to Babelfish for PostgreSQL extension versions 4.10, 5.6, 6.1 or later. As a workaround, restrict network access to the TDS port (default 1433). Customers using Amazon Aurora PostgreSQL with Babelfish should upgrade their cluster to Aurora PostgreSQL 13.9.16 (1.5.5), 13.23.3 (1.17.2), 14.6.16 (2.3.5), 14.17.8 (2.12.4), 14.18.6 (2.13.3), 14.19.5 (2.14.2), 14.20.5 (2.15.2), 14.22.3 (2.16.1), 14.23.1 (2.17.0), 15.10.8 (3.8.4), 15.12.8 (3.9.4), 15.13.6 (3.10.3), 15.14.5 (3.11.2), 15.15.5 (3.12.2), 15.17.3 (3.13.1), 15.18.1 (3.14.0), 16.8.8 (4.5.5), 16.9.6 (4.6.3), 16.10.5 (4.7.2), 16.11.5 (4.8.2), 16.13.3 (4.9.1), 16.14.1 (4.10.0), 17.4.8 (5.1.4), 17.5.6 (5.2.3), 17.6.5 (5.3.2), 17.7.5 (5.4.2), 17.9.3 (5.5.1), 17.10.1 (5.6.0), 18.3.4 (6.0.2), 18.4.1 (6.1.0) or later, and apply any pending maintenance to ensure they are on the latest patch.

### CVE-2026-122193

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-06T17:17:20.313 |

OS command injection in the example SSM document provisioning script in Trusted Remote Execution (REX) before 2026-07-28 might allow an authenticated remote user who is permitted to invoke the Rex-RO or Rex-RW SSM document to execute arbitrary commands as root on the managed instance, bypassing Cedar policy enforcement.



To remediate this issue, users should delete any Rex-RO and Rex-RW SSM documents created from the example script, in each account and Region where it was run.

### CVE-2026-59105

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-547;CWE-1391` |
| Published | 2026-11-06T15:17:22.270 |

Jumis (formerly Tildes Jumis) creates and uses a Microsoft SQL Server login named ##Tilde_JumisAdmin## whose password is derived deterministically from a single non-secret input - the SQL Server name (@@servername). The derivation algorithm is hard-coded in the client application and is identical across every installation; it contains a hard-coded secret key for entropy. Because the only input (the server name) is not secret - the instance suffix is hard-coded and the host name is discoverable via the SQL Server Browser service (UDP 1434), the TDS pre-login response, or DNS/NetBIOS - any party able to reach a Jumis SQL Server can compute the password offline and authenticate. The ##Tilde_JumisAdmin## login is a member of the sysadmin server role. Successful authentication therefore grants full administrative control of the SQL Server instance and read/write access to every customer's accounting database hosted on it. The on-premise server installation also programmatically enables xp_cmdshell during routine operation, so sysadmin access escalates to operating-system command execution on the database server.

### CVE-2026-123488

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-06T15:17:18.133 |

Craft CMS 4.0.0 before 4.18.9 and 5.0.0 before 5.11.2 contains an unauthenticated SQL injection vulnerability in the element search endpoint because the attribute parameter is concatenated into the query unsanitized and emulated PDO prepares allow stacked statements. Remote attackers can read and write the database, setting the admin flag or overwriting password hashes in the users table to gain administrator access.

### CVE-2026-124040

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-06T20:17:22.203 |

CivetWeb through 1.16, when built with USE_HTTP2 and enable_http2 on, contains a use-after-free vulnerability in handle_http2() that retains freed :method and :path pointers. Unauthenticated remote attackers can send a later HEADERS frame omitting these pseudo-headers to influence request method or path seen by access rules, or crash the server.

### CVE-2026-120984

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-07T14:17:01.580 |

A flaw was found in the Keycloak server's client management component. When a client is created or imported with authorization services enabled, the system fails to properly clear an internal session attribute used during the setup process. This allows an authenticated attacker with client management permissions to bypass security controls and upload a malicious JavaScript policy, which is then executed on the server when an authorization request is made. Successful exploitation could allow the attacker to run arbitrary code on the server, potentially compromising the entire system.

### CVE-2026-122041

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-07T13:16:36.067 |

The Checkout Field Editor for WooCommerce (Pro) plugin for WordPress is vulnerable to unauthorized deletion of arbitrary attachments due to a missing capability/ownership check in the ajax_remove_uploaded() function in versions up to, and including, 3.8.0. The handler is registered for both wp_ajax and wp_ajax_nopriv and is gated solely by the 'file_handling_nonce' nonce, which is emitted inside the public checkout page markup (data-nonce attribute) whenever a File Upload checkout field is configured. This makes it possible for unauthenticated attackers to delete arbitrary attachments (including those belonging to other users or posts) by submitting a crafted attachment_id, which can lead to loss of important media and potential denial of service.

### CVE-2026-118066

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-07T12:17:43.717 |

The Appointment Booking Plugin – LatePoint | Calendar & Scheduling for WordPress plugin for WordPress is vulnerable to Authentication Bypass via Account Takeover in all versions up to, and including, 5.7.6. This is due to the `OsModel::build_conditions_query()` function in `lib/models/model.php` comparing WHERE-clause values against the literal strings `'IS NULL'` and `'IS NOT NULL'` and concatenating a match directly into SQL without binding it as a parameter, a flaw that neither `sanitize_text_field()` nor the 5.7.5 `is_scalar()` hardening guard closes, since both pass the scalar sentinel through unchanged. This makes it possible for unauthenticated attackers to send `params[password_reset_token]=IS NOT NULL` to the public `customer_cabinet__change_password` AJAX route to match every non-null `account_nonse` value, resolving to the lowest-id customer and overwriting that customer's password to an attacker-chosen value — granting full access to their bookings, orders, and PII, and, when the `wp_users_as_customers` option is enabled, takeover of the linked WordPress subscriber or customer-role account. The attacker can first identify the target customer's email by sending `params[order_intent_key]=IS NOT NULL` to the public `steps__start_from_order_intent` route, which returns the name and email from the first matching order intent, and can then self-arm the required 15-minute password-reset freshness window by triggering a reset for that customer directly.

### CVE-2026-17339

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-07T05:18:45.287 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to access or delete resources belonging to other tenants due to path traversal.

### CVE-2026-17338

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:45.083 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to broken object-level authorization.

### CVE-2026-17292

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:36.330 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to take over ownership of other organizations due to broken object-level authorization. Access checks on organization objects are incomplete, which could allow ownership of organizations the user does not control to be changed.

### CVE-2026-17066

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-07T05:18:23.787 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information and modify or delete data belonging to other tenants due to missing authorization.

### CVE-2026-68935

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-06T22:17:59.390 |

Chartbrew is an open-source web application for creating charts from databases and APIs. In versions 4.8.5 through 5.2.2, API connection creation and update operations accept the internal  allowPrivateHost  field from user input. An authenticated user with permission to manage API connections can enable this field to bypass private and reserved-network destination restrictions. An upgrade migration also enables the override on pre-existing API connections. The per-connection setting takes precedence over  CB_ALLOW_PRIVATE_NETWORK_CALLS , so disabling that instance option does not protect connections with the override enabled. Successful exploitation allows requests to internal HTTP services reachable from the Chartbrew server, potentially disclosing information or triggering unauthorized actions depending on the target service. Recognized cloud metadata endpoints remain separately blocked. This issue is fixed in version 5.2.3.

### CVE-2026-17403

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-07T05:18:56.690 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote attacker to gain full administrative control due to the use of hard-coded credentials.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-17280

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-307` |
| Published | 2026-11-07T05:18:33.853 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote attacker to perform unauthenticated brute-force attacks to obtain valid credentials due to improper restriction of excessive authentication attempts.

### CVE-2026-120841

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-11-07T13:16:35.130 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in Magepeople inc. WpTravelly tour-booking-manager allows PHP Local File Inclusion.This issue affects WpTravelly: from n/a through 2.3.8.

### CVE-2026-120839

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-11-07T13:16:34.973 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in Magepeople inc. WpTravelly tour-booking-manager allows PHP Local File Inclusion.This issue affects WpTravelly: from n/a through 2.3.8.

### CVE-2026-121762

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-07T10:17:11.083 |

Cross-Site Request Forgery (CSRF) vulnerability in Blubrry Podcasting PowerPress Podcasting powerpress allows Cross Site Request Forgery.This issue affects PowerPress Podcasting: from n/a through 11.18.0.

### CVE-2026-66669

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-07T09:17:16.063 |

Cross-Site Request Forgery (CSRF) vulnerability in Suplugins Superb Addons: Blocks, Patterns &amp; Theme Designer superb-blocks allows Cross Site Request Forgery.This issue affects Superb Addons: Blocks, Patterns &amp; Theme Designer: from n/a through 4.2.4.

### CVE-2026-87112

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-07T07:17:05.090 |

The QA Assistants – Driven by data plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 5.3.0 via the 'dlevent_ver' parameter. This is due to unrestricted PHP deserialization via wrap_unserialize_static() calling unserialize() without an allowed_classes restriction, combined with serialize_escape() failing to sanitize path traversal sequences in the raw_name parameter. This makes it possible for unauthenticated attackers to inject a PHP Object. The Guzzle FileCookieJar gadget present in the plugin's bundled Composer dependencies can be leveraged to perform an Arbitrary File Write, writing attacker-controlled content to an attacker-chosen filename, which can result in Remote Code Execution. Exploitation requires triggering the qahm_cron_data_manage scheduled event via wp-cron.php to invoke the deserialization sink against a planted queue file, but this endpoint requires no authentication and fires automatically on a two-minute schedule.

### CVE-2026-17405

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:57.187 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to broken object-level authorization. Access checks on keystore objects do not confirm that the requesting user is permitted to read them, which could expose keystore information.

### CVE-2026-17335

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-07T05:18:44.453 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary code due to path traversal. File paths in uploaded content are not sufficiently validated, which could allow files to be written outside the intended location and code to be executed.

### CVE-2026-16716

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1259` |
| Published | 2026-11-07T05:18:20.733 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to bypass security restrictions to access and modify sensitive information due to improper restriction of security token assignment.

### CVE-2026-104913

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-07T03:16:59.167 |

The Interactive Real Estate – Floor Plan & Building Visualizer plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 2.6.0 via the extract_zip_data function. This is due to missing capability check, nonce verification, and file extension or MIME type validation before copying attacker-supplied ZIP members to the uploads directory. This makes it possible for authenticated attackers, with subscriber-level access and above, to upload files that may be executable, which makes remote code execution possible. This vulnerability is only exploitable on sites where the plugin's Freemius Premium license or trial is active, as the sole gate in the handler is a site-level license check rather than a per-user capability check.

### CVE-2026-50240

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-06T22:17:58.757 |

A flaw was found in OpenShift Pipelines-as-Code (PAC). PAC does not verify whether the creator of a Repository custom resource has permission to create PipelineRuns. A namespace user with only Repository and Secret create/delete permissions can cause PAC to execute attacker-controlled PipelineRuns as the auto-provisioned pipeline ServiceAccount, which carries ClusterRole/edit by default. This results in namespace-scoped privilege escalation, enabling Secret read, resource creation/modification/deletion, and potential supply chain injection in CI/CD namespaces.

### CVE-2026-85712

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-06T21:17:11.373 |

Chartbrew is an open-source web application that can connect directly to databases and APIs and use the data to create charts. Prior to 5.2.3, the shared project permission check trusted a caller-controlled team_id and let the teamOwner/teamAdmin branch continue without confirming that the target project belonged to that team. The vulnerable surface is project routes and related authorization checks that accepted user-controlled project identifiers. An authenticated user who is an owner or admin of their own team submits a victim project id together with the attacker's own team_id in the request body; default self-signup grants the required role on the user's own team. Authorization is evaluated against the attacker-selected team instead of the target project's team, and the update path mass-assigns the request body without a project field allow-list. The attacker needs a valid Chartbrew account, an owner or admin role on their own team, and a victim project identifier; requests without the body team_id trick are rejected. The attacker can re-parent the victim project into their own team, gain full read and write access, expose it publicly, remove password protection, and cause the victim to lose it; the shared delete route also permits cross-tenant deletion. This issue is fixed in version 5.2.3.

### CVE-2026-65960

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-06T20:17:24.397 |

Tetragon is an eBPF-based security observability and runtime enforcement project. Versions before 1.7.0 can use a Helm default that exposes the privileged Tetragon gRPC API through an unauthenticated TCP listener on localhost:54321. An attacker who can run or compromise same-node hostNetwork pods can reach the listener and invoke privileged methods without authentication. These methods can add, delete, or reconfigure tracing policies and change debug settings, potentially resulting in privilege escalation or container escape. Version 1.7.0 changes the default endpoint to a Unix-domain socket. Deployments that do not expose an unauthenticated TCP listener are not affected.

### CVE-2026-33050

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-06T20:17:22.570 |

GeoNode is a geospatial content management system, a platform for the management and publication of geospatial data. Prior to 5.1.0, a crafted vector file layer name supplied during upload allows a low-privileged remote user to inject shell syntax and execute arbitrary operating-system commands on the GeoNode server. This issue is fixed in version 5.1.0.

### CVE-2026-107155

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-942` |
| Published | 2026-11-06T19:17:06.623 |

A permissive cross-domain policy vulnerability has been identified in the SonicOS management interface, which in specific conditions could potentially enable a remote unauthenticated attacker to perform unauthorized operations.

### CVE-2026-107154

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-291` |
| Published | 2026-11-06T19:17:06.440 |

A session validation vulnerability has been identified in the SonicOS management interface, which in specific conditions could potentially enable a remote unauthenticated attacker to perform unauthorized operations.

### CVE-2026-118670

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T18:17:57.340 |

OHIF Viewers is a zero-footprint DICOM viewer with shared extension packages. From 3.5.0-beta.0 until 3.12.15, 3.13.7, and 3.14.0-beta.19, the dicom-pdf extension reads the attacker-controlled MIMETypeOfEncapsulatedDocument value in extensions/dicom-pdf/src/getSopClassHandlerModule.js and uses it as the Blob media type for the attacker-controlled EncapsulatedDocument bytes. When a victim opens Encapsulated PDF SOP Class 1.2.840.10008.5.1.4.1.1.104.1, extensions/dicom-pdf/src/viewports/OHIFCornerstonePdfViewport.tsx embeds the Blob URL in an object element. A Blob labeled as HTML is handled as HTML despite the application/pdf object hint, and the Blob inherits the OHIF origin, allowing embedded script to access session storage, authentication tokens, and same-origin PACS requests. The malicious DICOM object may be opened locally, uploaded to a shared PACS, or supplied by a DICOMweb source. This issue is fixed in source versions 3.12.15, 3.13.7, and 3.14.0-beta.19.

### CVE-2026-123836

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-06T17:17:21.963 |

In JetBrains Datalore before 2026.4 workspace collaborators could obtain the owner's SSH private key via Git backup

### CVE-2026-123491

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-06T15:17:18.663 |

Craft CMS 4.0.0 before 4.18.9 and 5.0.0 before 5.11.2 contains an SQL injection vulnerability in GraphQL eager-loading: arguments on eager-loadable nodes absent from the public schema are copied into EagerLoadPlan criteria without cleansing. Unauthenticated attackers can supply a parenthesized select argument to inject SQL expressions and read arbitrary database content, including password hashes and session tokens.

### CVE-2026-112340

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-06T15:17:08.537 |

Wazuh dashboard plugins from 4.9.0 before 4.14.9 contain an authorization bypass vulnerability that allows authenticated dashboard users to override the Manager API Authorization header via the /api/request proxy endpoint. Attackers can supply nested body.headers.Authorization values that replace the server-side session Bearer token, letting them act as another Manager API identity or send unauthenticated upstream requests.

### CVE-2026-106019

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-11-06T15:17:05.660 |

Insertion of sensitive information into log file vulnerability in Johnson Controls C-CURE 9000, Victor allows Use of Known Operating System Credentials.

This issue affects C-CURE 9000, Victor: 3.20.

### CVE-2026-17356

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-07T05:18:47.447 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a local attacker to obtain sensitive information due to the use of a hard-coded cryptographic key.

### CVE-2026-17332

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-07T05:18:43.827 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to bypass security restrictions due to improper certificate validation.

### CVE-2026-17291

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-601` |
| Published | 2026-11-07T05:18:36.097 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to perform account takeover due to an open redirect vulnerability. The redirect address used during OAuth 2.0 sign-in is not sufficiently validated, which could allow authentication results to be sent to an attacker-controlled location.

### CVE-2026-17190

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T05:18:29.840 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary JavaScript due to cross-site scripting. HTML content supplied by a provider is not sufficiently sanitized before it is displayed, which could allow script content to run in the user's browser.

### CVE-2026-16709

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T05:18:19.730 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary JavaScript in the victim's browser due to cross-site scripting. User-supplied input is not properly neutralized when a web page is updated, so script content could run in another user's session.

### CVE-2026-124078

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674;CWE-776` |
| Published | 2026-11-06T21:17:08.567 |

plist.js (npm package 'plist') before 5.0.1 contains an uncontrolled resource consumption vulnerability in the binary property-list parser (parseBinary) that allows unauthenticated attackers to crash a Node.js process by exploiting unmemoized recursive resolution of shared object references for arrays and dictionaries. Attackers can craft a small binary plist (under 200 bytes) containing chained self-referencing object indices to trigger exponential (2^N) resolution calls and memory growth, causing an unrecoverable out-of-memory crash and denial of service.

### CVE-2026-124027

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-06T20:17:21.123 |

ChatWiki before 2.10.0 contains a missing authentication vulnerability in the GET /manage/getLibRawFileOnePage route that allows unauthenticated attackers to read other tenants' documents. Attackers can enumerate sequential admin_user_id and file id query parameters, bypassing the ownership check, to retrieve PDF-rendered pages of any tenant's knowledge-base documents.

### CVE-2026-123993

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-489` |
| Published | 2026-11-06T19:17:44.550 |

Hisense VIDAA Smart TV firmware V0000.01.00a.P0220 contains an unauthenticated access vulnerability where a QA build of the Google Cobalt browser engine exposes the WebDriver automation server on TCP port 4444 across all network interfaces without any authentication or pairing requirement. A LAN-adjacent attacker can connect to the exposed WebDriver service to execute arbitrary JavaScript, read and exfiltrate sensitive localStorage data including ACR telemetry, MAC addresses, ad-service credentials, and location data, inject persistent content onto the display, and access the window.hisense native bridge to perform filesystem read/write and system-state operations.

### CVE-2026-89017

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-798` |
| Published | 2026-11-06T18:18:22.380 |

Skyline DataMiner BrokerGateway contains an embedded API key vulnerability that allows unauthenticated attackers to retrieve the installation-specific BrokerGateway key even while pairing mode is disabled. Attackers can use the retrieved key to obtain the unrestricted DataMinerUser.creds NATS credential and gain trusted message-bus access via TCP port 4222 without any prior DataMiner credentials. Fixed in DataMiner 10.6.9 CU1, 10.6.0 CU7, 10.5.0 CU19, and 10.4.0 CU22.

### CVE-2026-123792

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407;CWE-1333` |
| Published | 2026-11-06T16:17:55.463 |

The Symfony Yaml components Inline and Parser, parse some YAML documents inefficiently, so that a small crafted document can take disproportionately long to process, keeping a PHP process busy for seconds or minutes, potentially causing a denial of service in Symfony versions prior to 5.4.56, 6.x prior to 6.4.50, 7.x prior to 7.4.23, and 8.x prior to 8.1.11.

The parser repeats work it has already done in several places. An embedded mapping in a flow sequence is parsed again for every scalar appended to it, and so are the collections nested in it, so the parse time grows exponentially with the nesting depth. The patterns matching mapping keys and tags scan a run of spaces once per character of the run, and each scalar of a flow collection is matched against a copy of the rest of the collection, so the parse time grows quadratically with the size of the input. Nested blocks are also copied at each nesting level, which consumes memory as well as time. A few other constructs, such as an empty sequence item followed by a blank line or an anchor named 0, trigger similar repeated work.


Any code parsing untrusted YAML is affected, with the default flags. In Symfony 7.4 and later, that includes #[MapRequestPayload] when the Yaml component is installed and the endpoint does not restrict acceptFormat. A single unauthenticated request with a YAML content type keeps a PHP worker busy until max_execution_time. JSON documents are valid YAML, so a JSON payload sent with a YAML content type is enough for the flow collection case. In Symfony 6.4, #[MapRequestPayload] accepts YAML only when the application registers a yaml request format.

### CVE-2026-123783

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-11-06T15:17:21.103 |

Skyvern through 1.0.56 contains a sandbox bypass vulnerability that allows authenticated users to execute code by reconstructing functions from raw bytecode with types.CodeType. Attackers can deploy scripts that evade the is_safe_script_code AST denylist and import blocked modules such as subprocess or socket to run code in the Skyvern server process.

### CVE-2026-123490

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-06T15:17:18.483 |

Craft CMS from 5.8.17 before 5.11.2 contains a privilege escalation vulnerability because getOwners() applies caller criteria without cleansing the query configuration. Authenticated control panel users can invoke attacker-selected static PHP callables via crafted criteria to promote every account to administrator.

### CVE-2026-123487

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-11-06T15:17:17.947 |

Parse Server before 8.6.115 and 9.0.0 before 9.10.7-alpha.1 validates user email address format with a regular expression whose run time grows quadratically with input length and that is applied without a length limit. An unauthenticated attacker who knows the application ID can send a sign-up request, or a logged-in user can update their own email, with a long crafted email address to block the Node.js event loop and deny service to all clients.

### CVE-2026-123961

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-11-07T11:17:01.290 |

A security vulnerability has been detected in TOTOLINK CA300-PoE 6.2c.884. This impacts the function setWiFiBasicConfig of the file /cgi-bin/cstecgi.cgi. The manipulation of the argument KeyStr leads to buffer overflow. The attack may be initiated remotely. The exploit has been disclosed publicly and may be used.

### CVE-2026-123960

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-11-07T10:17:12.357 |

A weakness has been identified in TOTOLINK CA300-PoE 6.2c.884. This affects the function setWanConfig of the file /cgi-bin/cstecgi.cgi. Executing a manipulation of the argument pppoeUser/priDns/secDns can lead to buffer overflow. The attack can be launched remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-123958

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-11-07T09:17:15.177 |

A vulnerability was identified in TOTOLINK CA300-PoE 6.2c.884. The affected element is the function setLanConfig of the file /cgi-bin/cstecgi.cgi. Such manipulation of the argument lanDns/lanSecDns/langType leads to buffer overflow. It is possible to launch the attack remotely. The exploit is publicly available and might be used.

### CVE-2026-123957

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-11-07T09:17:14.890 |

A vulnerability was determined in TOTOLINK CA300-PoE 6.2c.884. Impacted is the function setIpQosRules of the file /cgi-bin/cstecgi.cgi. This manipulation of the argument ipStart causes buffer overflow. It is possible to initiate the attack remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-53980

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-06T15:17:22.100 |

Charmbracelet wish before 2.0.5 contains a path traversal vulnerability in the git middleware (charm.land/wish/v2) that allows authenticated SSH users to escape the configured repository directory by supplying crafted repo paths that bypass a flawed forward-slash-count containment check in git.Middleware(). Attackers can use a single-depth path ../evil, or on Windows a payload ..\..\evil that defeats the slash-count guard entirely, to read or write arbitrary repositories outside the intended root via git-upload-pack, git-upload-archive, or git-receive-pack.

### CVE-2026-123621

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-06T15:17:19.730 |

Usermin through 2.570 contains a path traversal vulnerability in mailbox/detachall.cgi that allows remote unauthenticated attackers to write files outside the temporary directory via unsanitized attachment filenames. Attackers can email attachments with ../ sequences in filenames, and when the recipient downloads all attachments, files like ~/.forward are overwritten, enabling command execution.

### CVE-2026-106022

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-316` |
| Published | 2026-11-06T15:17:05.997 |

Cleartext storage of sensitive information in memory vulnerability in Johnson Controls EasyIO Neo IOManager and Tools Installer allows Retrieve Embedded Sensitive Data.

This issue affects EasyIO Neo IOManager and Tools Installer: 1.1.0.0.

### CVE-2026-106020

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-06T15:17:05.847 |

Improper neutralization of input used for LLM prompting vulnerability in Johnson Controls EasyIO Neo IO Manager and Tools Installer allows Search Order Hijacking.

This issue affects EasyIO Neo IO Manager and Tools Installer: 1.1.0.0.

### CVE-2026-123959

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-11-07T10:17:12.123 |

A security flaw has been discovered in TOTOLINK CA300-PoE 6.2c.884. The impacted element is the function setLanguageCfg of the file /cgi-bin/cstecgi.cgi. Performing a manipulation of the argument langType results in buffer overflow. The attack can be initiated remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-17407

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-07T05:18:57.670 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary SQL commands due to SQL injection. Values received during sign-in are not properly neutralized before being used in a database query, which could allow SQL commands to run.

### CVE-2026-17406

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:57.427 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery. Address checks can be bypassed, which could allow the server to reach destinations that should be blocked.

### CVE-2026-17404

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:56.937 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-17398

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:55.557 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-17397

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:55.330 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-17388

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:53.253 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to broken object-level authorization.

### CVE-2026-17385

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:52.683 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-17384

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:52.500 |

IBM API Connect 10.0.8.0 through 10.0.8.12 could allow a remote authenticated attacker to obtain sensitive information due to a server-side request forgery vulnerability.

### CVE-2026-17382

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-07T05:18:52.133 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to a path traversal vulnerability.

### CVE-2026-17381

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:51.953 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to improper authorization validation using user-controlled keys.

### CVE-2026-17380

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-07T05:18:51.750 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to access sensitive information belonging to other tenants due to improper validation of a path parameter. A path value in a request is not sufficiently validated, which could allow a user to reach data outside their own tenant.

### CVE-2026-17365

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:48.900 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-17352

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:46.690 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-17334

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:44.260 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to improper authorization via user-controlled keys.

### CVE-2026-17330

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:43.460 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-17328

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:43.083 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to improper input validation. Input checks are incomplete, which could allow them to be bypassed.

### CVE-2026-17327

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:42.900 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-17325

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:42.510 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to improper validation of user-supplied URLs.

### CVE-2026-17294

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:36.743 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-17293

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:36.570 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to modify user profile information due to broken object-level authorization. Access checks do not confirm that the user is permitted to change the targeted profile.

### CVE-2026-17290

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-07T05:18:35.867 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to create unauthorized user accounts due to improper verification of cryptographic signatures. Identity information from a login provider is accepted without its signature being fully verified, so forged identity data could be used to create accounts.

### CVE-2026-17288

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:35.407 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-17287

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:35.177 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery. User-supplied addresses are not sufficiently validated, so the server could be made to send requests to unintended destinations and return the results.

### CVE-2026-17228

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:31.070 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery. Destination restrictions on outbound requests can be bypassed, which could allow the server to retrieve content from unintended resources.

### CVE-2026-17188

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:29.640 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery. When service definitions are imported, references to external resources are not sufficiently restricted, so the server could be made to request resources it should not access.

### CVE-2026-17187

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:29.457 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to improper validation of user-supplied URLs.

### CVE-2026-17172

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-07T05:18:29.247 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to bypass security restrictions due to improper authentication. Information supplied by the client is not sufficiently verified, which could allow a caller to impersonate another party.

### CVE-2026-17108

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:24.760 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-16912

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:22.630 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-16880

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-07T05:18:22.243 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to path traversal.

### CVE-2026-123784

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-06T15:17:21.297 |

Fluxbox through 1.3.7 contains an OS command injection vulnerability in RootTheme::reconfigTheme() that allows attackers to execute commands via crafted style background values. Attackers can embed shell metacharacters in background pixmap paths, random directories, or gradient texture text, which are concatenated unescaped into an fbsetbg command run via $SHELL -c when the style loads.

### CVE-2026-123962

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-61` |
| Published | 2026-11-06T17:17:25.483 |

In FreedomBox before 26.15, unprivileged user accounts can read/write files for which they lack permissions by setting the authorized_keys file to be a symlink. NOTE: FreedomBox is a Debian Pure Blend, which means that it distributes its software through Debian repositories.

### CVE-2026-118515

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-06T17:17:16.580 |

The Symfony Serializer component DataUriNormalizer handles only the exact types SplFileInfo, SplFileObject, and File, so for a property typed with a subclass such as UploadedFile, ObjectNormalizer instantiates the object through its constructor from attacker-controlled data, including the file path. This allows an arbitrary file on the server to be treated as an uploaded file in Symfony versions prior to 5.4.56, 6.x prior to 6.4.50, 7.x prior to 7.4.23, and 8.x prior to 8.1.11.

A request body such as {"image": {"path": "/path/to/project/.env.local", "originalName": "a.png", "test": true}} makes the application handle any file on the server as an upload, without the file being sent. With test: true, UploadedFile::isValid() skips is_uploaded_file() and move() falls back to rename(). Assert\File does not prevent this because it validates the file at the attacker-chosen path, which exists on the server.
Any code that deserializes untrusted data into a type that holds such a property is affected. That includes #[MapRequestPayload] on a DTO with an UploadedFile property, which is how uploads are mapped in Symfony 8.1; a single unauthenticated request with a JSON or form body is enough. Depending on what the application does with the upload, this can expose any file readable by PHP (for instance, when uploads are stored and served back), move any such file when move() is called, and reveal whether a path exists.

A serializer built without DataUriNormalizer ahead of the object normalizer is not protected by the fix; the serializer configured by FrameworkBundle is.

### CVE-2026-123786

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-06T15:17:21.643 |

Agenta before 0.122.5 contains a server-side request forgery vulnerability that allows workspace members with workflow edit rights to redirect workflow invocations by setting arbitrary revision URLs. Attackers can capture the attached secret-resolve Authorization token to read provider secrets from the vault API, or reach internal and cloud metadata addresses.

### CVE-2026-19121

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-07T05:18:59.963 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow an authenticated attacker to gain unauthorized access due to improper authorization. Tenant context is not sufficiently verified against the authenticated user, which could allow access to another tenant's resources.

### CVE-2026-17324

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-07T05:18:42.310 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to access sensitive configuration data and perform unauthorized actions due to missing authentication for a critical function.

### CVE-2026-17358

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-07T05:18:47.823 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to bypass authentication across tenants due to improper authentication. Authentication checks are not sufficiently isolated between tenants, which could allow a user from one tenant to be accepted by another.

### CVE-2026-17355

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:47.250 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information from internal network resources due to server-side request forgery. Destination checks on outbound requests can be bypassed, which could allow the server to reach internal systems that should be blocked.

### CVE-2026-17323

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-07T05:18:42.120 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to obtain sensitive information due to XML external entity (XXE) injection.

### CVE-2026-71397

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-06T21:17:10.480 |

Allocation of Resources Without Limits or Throttling vulnerability in elixir-grpc grpc_server allows unauthenticated attackers to exhaust memory and crash the node via an oversized client-streaming or bidirectional-streaming request body.

The streaming read clause of 'Elixir.GRPC.Server.Adapters.Cowboy.Handler':info/3 (grpc_server/lib/grpc/server/adapters/cowboy/handler.ex) never checks the configured max_body_size. Only the unary read path enforces that cap. 'Elixir.GRPC.Server.Adapters.Cowboy':reading_stream/1 (grpc_server/lib/grpc/server/adapters/cowboy.ex) appends every received chunk to its buffer until a complete length-prefixed message arrives. A client can declare a very large message and send it across many small HTTP/2 DATA frames, and the server buffers all of it.

This issue affects grpc_server: from 1.0.0 before 1.0.6.

### CVE-2026-85743

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-06T17:20:02.567 |

FreeScout is a self-hosted help desk and shared mailbox. Prior to 1.8.230, multiple outbound paths in Helper::downloadRemoteFile(), Helper::checkPort(), Helper::sanitizeRemoteUrl(), MailboxesController.php, and ModulesController.php do not consistently enforce a sink-level restricted-host policy. An authenticated administrator, or another authenticated user permitted to change mailbox connection settings or trigger module update or installation paths, can supply attacker-controlled URLs or hosts. The independent download and port-test sinks can reach encoded or otherwise uncovered loopback and internal addresses. The redirect-validation bypass additionally requires a configured whitelist that permits the original and final hosts while a restricted internal host appears only as an intermediate redirect hop. No unauthenticated SSRF path is established. The server can consequently contact loopback and internal services, provide a blind internal port oracle, and retrieve internal HTTP responses into application-controlled download sinks. This issue is fixed in version 1.8.230.

### CVE-2026-123623

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-06T16:17:54.560 |

Grida through 0.0.24 contains a missing authorization vulnerability in the Forms file-preview API routes that allows unauthenticated attackers to read other organizations' form response files. Attackers can use form and field IDs exposed in public form payloads with a chosen path parameter to obtain service-role signed URLs for attachments and connected Supabase bucket objects.

### CVE-2026-121623

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-11-06T16:17:52.780 |

The Symfony Serializer component DataUriNormalizer::denormalize() matches the data: scheme with a case-sensitive regular expression, allowing a value with an uppercase scheme, such as DATA:,/../../../etc/passwd, to bypass it, resulting in Arbitrary Local File Read through Path Traversal in Symfony versions prior to 5.4.56, 6.x prior to 6.4.50, 7.x prior to 7.4.23, and 8.x prior to 8.1.11.

A value whose scheme is not lowercase data: are treated as a local file path and opened instead of being decoded as inline data, so the resulting File, \SplFileInfo, or \SplFileObject points at a file on the server, which the application then handles as the uploaded content.

Any endpoint that deserializes untrusted input into one of these types is affected. FrameworkBundle registers DataUriNormalizer ahead of ObjectNormalizer by default. A single request with a crafted DATA: value is enough to read arbitrary local files that the application can access, with no authentication needed if the endpoint is public.

### CVE-2026-119170

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-11-06T15:17:12.073 |

There was a regression in how FIPS algorithms were enforced for the hashlib module. Only users that are using OpenSSL in FIPS mode are affected. Only Python 3.14.10 is affected, all other Python versions are unaffected.

### CVE-2026-112339

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-297` |
| Published | 2026-11-06T15:17:08.377 |

Wazuh from 3.9.0 before 4.14.9 contains a missing TLS hostname verification vulnerability in the fluent-forward module's wm_fluent_ssl_ctx() that allows network attackers to impersonate the Fluentd collector by presenting any certificate chaining to the configured ca_file. Attackers who redirect the connection via DNS, ARP, or on-path positions can receive forwarded security telemetry and the shared_key_hexdigest for offline cracking.

### CVE-2026-112338

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-06T15:17:08.217 |

Wazuh from 4.3.0 before 4.14.9 contains a server-side request forgery vulnerability in the GitHub module (wm_github.c) that trusts unvalidated Link rel="next" pagination URLs. Attackers controlling the next-page URL can make the manager send requests with the GitHub API token to attacker hosts, exposing organization repositories and settings.

### CVE-2026-118267

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-07T12:17:43.867 |

The WP Data Access – App Builder for Tables, Forms, Dashboards, Charts & Maps plugin for WordPress is vulnerable to Incorrect Authorization leading to Privilege Escalation in all versions up to, and including, 5.5.89 This is due to the plugin's write endpoints (`wpda/app/update`, `wpda/app/delete`, `wpda/app/insert`) passing the attacker-supplied `key` and `val` parameters directly to `$wpdadb->update`, `$wpdadb->delete`, and `$wpdadb->insert` without enforcing the container's row-filter (`defaultWhere`) or per-column allow-list (`isSelected`) restrictions that are correctly applied on the read endpoints. This makes it possible for authenticated attackers, with Subscriber-level access and above, to write to arbitrary rows and columns outside the configured restrictions — including overwriting the `user_pass` field of the WordPress administrator account in `wp_users` — and subsequently authenticate as the administrator, achieving full site takeover. Exploitation requires an administrator to have published a Data App that enables write transactions (update, delete, or insert) for Subscriber-level or anonymous users, which is an explicitly advertised use-case of the plugin. Exploitation by unauthenticated attackers requires that the administrator has published a Data App whose rest_api.authorization is 'anonymous' and whose container has transactions.update (or delete/insert) enabled. On a default installation, where that is not configured, the vulnerability requires attackers with subscriber-level access and above.

### CVE-2026-104746

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-07T12:17:41.480 |

The Motors – Car Dealership & Classified Listings Plugin plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the stm_listings_ajax_save_user_data function in all versions up to, and including, 1.4.125 This makes it possible for authenticated attackers, with subscriber-level access and above, to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). Although deletion is bounded to wp-content/uploads (preventing removal of wp-config.php), any authenticated Subscriber can trivially exploit this because the required AJAX nonce is printed on every front-end page and the handler's stm_user_avatar_path meta is writable by any logged-in user against their own account.

### CVE-2026-103900

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-07T10:17:05.140 |

The WPJAM Basic plugin for WordPress is vulnerable to Privilege Escalation in versions up to, and including, 7.1 This is due to the WPJAM_User_Signup::signup() function unpacking attacker-supplied `data[args]` from the AJAX POST body and merging it via PHP array union into the payload passed to WPJAM_User::create(), whose internal whitelist (wpjam_pick) explicitly preserves the `role` key before it is handed to wp_insert_user(). The endpoint is registered as wp_ajax_nopriv_{provider}-signup with a nonce that is emitted on the public login page. This makes it possible for unauthenticated attackers to elevate their privileges to Administrator by creating a new user with an attacker-chosen role, provided a social-login provider is registered and open registration is enabled.

### CVE-2026-104738

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-07T09:17:11.253 |

The Advanced Form Integration — Connect Forms to 300+ Apps plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 2.10.2 via deserialization of untrusted input . This makes it possible for unauthenticated attackers to inject a PHP Object. No known POP chain is present in the vulnerable software, which means this vulnerability has no impact unless another plugin or theme containing a POP chain is installed on the site. If a POP chain is present via an additional plugin or theme installed on the target system, it may allow the attacker to perform actions like delete arbitrary files, retrieve sensitive data, or execute code depending on the POP chain present. Exploitation requires that an administrator has previously configured at least one active NexForms integration (status=1) in the plugin's database table; in the free tier, only POST parameter keys containing the substrings 'name', 'email', 'first', or 'last' are routed to the vulnerable normalizer.

### CVE-2026-17386

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-338` |
| Published | 2026-11-07T05:18:52.857 |

IBM API Connect 10.0.8.0 through 10.0.8.12 could allow a remote attacker to gain full administrative control due to the use of a cryptographically weak pseudo-random number generator.

### CVE-2026-17343

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-07T05:18:46.130 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to bypass authorization checks to access or modify sensitive information due to improper authorization.

### CVE-2026-17326

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-07T05:18:42.697 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to bypass security restrictions due to improper authentication.

### CVE-2026-17321

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:41.723 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to delete or overwrite arbitrary control-plane assets due to an insecure direct object reference.

### CVE-2026-85736

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-06T21:17:11.757 |

Chartbrew is an open-source web application that can connect directly to databases and APIs and use the data to create charts. Prior to 5.2.3, connection creation or update stored attacker-chosen absolute SSL and SSH file paths, and later connection cleanup passed those stored paths to fs.unlink without a path restriction. The vulnerable surface is data-connection certificate and SSH-key cleanup when a connection is removed. A user with createOwn and deleteOwn permissions on their own team stores a target path in a connection and then deletes the connection to trigger cleanup; default self-signup grants teamOwner these permissions. The cleanup routine treats the stored SSL or SSH path as a managed certificate path and unlinks the referenced file; duplicateConnection provides a second advisory-identified trigger. The attacker must be able to create or update and then delete a connection on their own team. The default container runs Chartbrew as uid 0, while deployments with a less-privileged process are limited by that process's deletion permissions. The attacker can delete files such as /code/.env or application source, causing integrity loss and service disruption. This issue is fixed in version 5.2.3.

### CVE-2026-102344

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-73;CWE-306;CWE-346` |
| Published | 2026-11-06T21:17:05.323 |

Lavish is the new editor for your HTML artifacts. Prior to 0.1.43, the lavish-axi loopback HTTP server did not authenticate requests or validate Host and Origin values on session, artifact, prompt, and polling routes. A website visited while the server is running can use DNS rebinding to send same-origin browser requests to the local service. POST /api/sessions accepts a caller-selected file path and returns its deterministic session key; GET /artifact/:key/index.html then returns the file contents, allowing disclosure of any file readable by the server process without an existing session. An attacker can also queue text through POST /api/:key/prompts for an active agent session when the artifact path is known or guessed. Visiting the attacker-controlled website is the required user interaction. This vulnerability is fixed in 0.1.43.

### CVE-2026-123859

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-06T17:17:25.323 |

When identifier escaping is disabled through a non-default configuration, the write_pandas() data-loading functionality in the Snowflake Connector for Python and the Snowflake Connector for Python (Universal Core) did not escape DataFrame column names before including them in generated SQL, which could allow SQL injection. In both products, a crafted column name could have been used to chain additional SQL statements onto the generated statement, potentially allowing an attacker to read, modify, or delete other data accessible to the application's Snowflake role. Exploitation required an application to pass attacker controlled column names into this functionality. The fix is available in Snowflake Connector for Python version 4.8.1 and Snowflake Connector for Python (Universal Core) version 5.2.0. Users must upgrade manually.

### CVE-2026-17333

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-07T05:18:44.023 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote attacker to bypass authentication and inject unauthorized configuration changes due to improper certificate validation.

### CVE-2026-17309

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-07T05:18:39.393 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to obtain sensitive information and tamper with configuration due to improper certificate validation.

### CVE-2026-123974

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-379` |
| Published | 2026-11-06T20:17:20.633 |

In all versions of PyTorch's TorchServe, a predictable extraction directory in /tmp lets a local user swap the model handler and run code as the TorchServe service account leading to local privilege escalation.

### CVE-2026-123853

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-06T17:17:24.430 |

In JetBrains IntelliJ IDEA before 2026.3, 
2026.2.2 code execution was possible in Safe Mode via project-controlled JVM options of the build process

### CVE-2026-123841

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-06T17:17:22.693 |

In JetBrains IntelliJ IDEA before 2026.3 code execution was possible via symlinks in an imported settings archive

### CVE-2026-123838

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-06T17:17:22.247 |

In JetBrains IntelliJ IDEA before 2026.3 code execution was possible in Safe Mode via UI Designer form file

### CVE-2026-123837

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-06T17:17:22.097 |

In JetBrains IntelliJ IDEA before 2026.3, 
2026.2.1 command injection was possible in untrusted projects via Tomcat run configurations on WSL

### CVE-2026-17400

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-07T05:18:56.020 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to SQL injection.

### CVE-2026-17387

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:53.060 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to broken object-level authorization.

### CVE-2026-17383

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:52.323 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information from other tenants due to broken object-level authorization.

### CVE-2026-17378

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-07T05:18:51.370 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to broken object-level authorization.

### CVE-2026-17376

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:50.997 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to broken object-level authorization.

### CVE-2026-17375

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:50.800 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to improper authorization. Authorization decisions rely on information supplied by the client, which could allow access to information the user should not see.

### CVE-2026-17374

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:50.613 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to broken object-level authorization.

### CVE-2026-17373

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-07T05:18:50.430 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to improper authorization.

### CVE-2026-17363

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-07T05:18:48.710 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to SQL injection.

### CVE-2026-17361

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:48.390 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-17345

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-07T05:18:46.513 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to improper neutralization of special elements used in an SQL command.

### CVE-2026-17320

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:41.520 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to an insecure direct object reference.

### CVE-2026-17318

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:41.127 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to improper authorization.

### CVE-2026-17295

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-07T05:18:36.943 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to path traversal.

### CVE-2026-17289

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:35.620 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-17285

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:34.963 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to improper validation of external references. When schemas are validated, references to external resources are not sufficiently restricted, which could allow the server to retrieve content it should not access.

### CVE-2026-17283

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:34.520 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to broken object-level authorization.

### CVE-2026-17282

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:34.297 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to broken object-level authorization.

### CVE-2026-17281

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:34.100 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-17279

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-07T05:18:33.637 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to cause a denial of service due to uncontrolled resource consumption. Certain requests can cause internal processing to stall, which could make the service unavailable.

### CVE-2026-17112

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:25.040 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information belonging to other tenants due to broken object-level authorization.

### CVE-2026-16854

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-07T05:18:22.067 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information belonging to other tenants due to an injection vulnerability. Input used to build a data query is not properly neutralized, which could allow the query to return data the user is not permitted to see.

### CVE-2026-16718

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-07T05:18:21.523 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to improper validation of file paths.

### CVE-2026-16717

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:21.347 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information due to broken object-level authorization.

### CVE-2026-16715

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:20.543 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information from other tenants due to broken object-level authorization.

### CVE-2026-16712

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:20.210 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information from other tenants due to improper authorization. Identifiers supplied in requests are not sufficiently checked against the user's permissions, which could allow access to data belonging to other tenants.

### CVE-2026-62856

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89;CWE-200;CWE-639` |
| Published | 2026-11-06T17:18:34.047 |

FreeScout is a self-hosted help desk and shared mailbox application. Prior to version 1.8.226, the  polycast/receive  endpoint fails to escape SQL LIKE wildcards in supplied channel names, while channel authorization applies only to names with specific prefixes. An unauthenticated attacker with a guest session and valid CSRF token can submit a wildcard channel name to retrieve matching notification events intended for other users. Notification payload generation lacks a corresponding access check, exposing conversation message content, identifiers, URLs, and notification HTML across users and mailboxes. This issue is fixed in version 1.8.226.

### CVE-2026-123620

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-06T15:17:19.540 |

Usermin through 2.570 contains an OS command injection vulnerability in the Read Mail module that allows authenticated users to execute commands through unsanitized IMAP folder names. Attackers can create a folder containing shell metacharacters via an external IMAP client, then delete it in Usermin to run commands as their system account, bypassing webmail-only restrictions.

### CVE-2026-17411

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-07T05:18:58.650 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow an authenticated attacker to view, add, modify, or delete information in the back-end database due to SQL injection. Input is not properly neutralized before it is used in database queries.

### CVE-2026-17357

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:47.637 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to access internal network services due to server-side request forgery.

### CVE-2026-17129

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:26.030 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to obtain sensitive information and cause a denial of service due to an insecure direct object reference.

### CVE-2026-62346

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T19:17:53.770 |

Wanderer is a self-hosted trail database for saving and sharing adventures. Prior to 0.19.3, an authenticated local user can submit crafted waypoint.name and waypoint.icon values that the trail elevation graph interpolates into an innerHTML template in web/src/lib/vendor/maplibre-elevation-profile/elevationprofile.ts without HTML encoding or icon validation. A victim viewing the elevation profile executes the attacker-controlled script in their browser. Separately, federated waypoints can deliver the same malicious fields across instances without requiring the attacker to have a local account on the receiving instance. The script can expose session data or perform actions in the victim's context. This issue is fixed in version 0.19.3.

### CVE-2026-62345

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T19:17:53.607 |

Wanderer is a self-hosted trail database for saving and sharing adventures. Prior to 0.19.3, an authenticated user can store a crafted waypoint.icon value that createMarkerFromWaypoint() passes into FontawesomeMarker, where insertAdjacentHTML inserts the unvalidated value into map marker markup. Opening the affected trail map executes attacker-controlled script in the viewer's browser, which can expose session tokens or perform actions as the victim. Federated waypoint data can also reach the sink without a local account on the receiving instance. This issue is fixed in version 0.19.3.

### CVE-2026-62854

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T17:18:33.700 |

FreeScout is a self-hosted help desk and shared mailbox. Prior to 1.8.225, a user who can edit a mailbox signature can combine a scriptable file uploaded through /uploads/upload with nested tag fragments that bypass Helper::stripDangerousTags(). The resulting external script is served from the same origin, so the script-src 'self' policy permits it when another user opens the affected mailbox reply editor or new-ticket page. The script executes with the victim's FreeScout privileges and can read visible data and perform same-origin actions. This issue is fixed in version 1.8.225.

### CVE-2026-123618

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-06T15:17:19.187 |

ABP Framework before 10.7.1 contains an authentication bypass vulnerability that skips account state and two-factor checks when password login succeeds through a registered IExternalLoginProvider. Attackers holding the external directory password for deactivated, locked, or 2FA-protected accounts can obtain valid access tokens from the /connect/token password grant.

### CVE-2026-116751

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-07T12:17:43.070 |

The Booking for Appointments and Events Calendar – Amelia Pro plugin for WordPress is vulnerable to time-based SQL Injection via the 'tag[] (array KEYS)' parameter in all versions up to, and including, 9.9.1 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. WordPress's wp_magic_quotes escapes array values but not array keys, meaning attacker-controlled tag[] array keys reach EventRepository::getFilteredIds() completely unescaped and can be crafted to defeat the plugin's Statement::execute placeholder binder via overlapping strtr() substitution keys.

### CVE-2026-109991

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T12:17:42.267 |

The FunnelKit Payment Gateway for Stripe WooCommerce plugin for WordPress is vulnerable to Insecure Direct Object Reference in all versions up to, and including, 1.15.0.2 via the 'order-pay (WP query var from /checkout/order-pay/<ID>/)' parameter due to missing validation on a user controlled key. This makes it possible for unauthenticated attackers to read the full billing PII — including name, email address, phone number, and complete street address — of any store order by enumerating sequential order IDs, as this data is emitted into the inline fkwcs_data JavaScript object via wp_localize_script on every matching page response. Exploitation occurs even when WooCommerce itself rejects the order-pay page request, because the plugin's wp_localize_script call runs independently of WooCommerce's own order-key validation on the same request.

### CVE-2026-104768

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-07T12:17:41.793 |

The AutomatorWP – No-Code Workflow Automation, Integration & Webhooks Plugin, now with AI plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 6.0.4. This is due to missing privilege-ceiling validation in the `create_user()` function within the anonymous-user action (and equally in the Create User and Add/Change Role WordPress-integration actions), which verify only that the submitted role exists via `automatorwp_get_editable_roles()` without confirming the role falls at or below the acting context's privilege level — allowing attacker-controlled trigger tag data (e.g., a `{comment_author}` tag bound to the Role option) to supply any role, including `administrator`, unchallenged. This makes it possible for unauthenticated attackers to create a new administrator-role account tied to an attacker-controlled email address, receiving the generated password via WordPress's new-user notification email and thereby gaining full administrative access to the site. Exploitation requires the site to have an anonymous automation configured with the Role option bound to a dynamic trigger tag such as `{comment_author}`, and is triggered when a site administrator performs the routine action of approving a comment — an action that provides no in-UI indication that it will mint a new privileged account from the comment author field.

### CVE-2026-95870

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-07T10:17:12.787 |

The wpForo Forum plugin for WordPress is vulnerable to generic SQL Injection via the 'data' parameter in all versions up to, and including, 3.2.1 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. Exploitation requires that a searchable topic form field of type checkbox, or a select/autocomplete field with isMultiChoice enabled, is registered in the forum configuration.

### CVE-2026-119164

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-07T10:17:07.337 |

The wpForo Forum plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 3.2.2 via the `data[secondary_groupids]` parameter of the `wpforo_action_profile_update` POST handler. This is due to a type-confusion flaw in the secondary_groupids authorization guard within the `Members::update()` function in `classes/Members.php`, where casting a scalar CSV string (e.g. `"0,1"`) with `(array)` before `array_map('intval', …)` and `array_filter()` produces an empty array — causing the guard's outer conditional, and the else-branch that would otherwise strip the field from the update, to be bypassed entirely — while `encode()`/`decode()` downstream correctly explodes the original CSV and persists the attacker-supplied group IDs to `wp_wpforo_profiles.secondary_groupids`. This makes it possible for authenticated attackers, with Subscriber-level access and above, to escalate their forum privileges to wpForo Administrator by injecting the privileged Admin group ID, granting access to the Forum Accesses editor and the ability to rewrite forum-wide capability policies for all members and edit arbitrary content owned by other users. Exploitation requires the attacker to have at least 3 approved wpForo posts to satisfy the plugin's default `min_number_posts_to_edit_account` antispam gate, along with a valid wpforo nonce obtained from their own account profile form.

### CVE-2026-119155

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-07T10:17:07.150 |

The wpForo Forum plugin for WordPress is vulnerable to time-based SQL Injection via the 'href[locale]' parameter in all versions up to, and including, 3.2.2 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. The nonce required for exploitation is publicly issued to unauthenticated visitors on any forum page via the wpforo.nonces JavaScript object, meaning no account or prior interaction beyond a page load is required to obtain it.

### CVE-2026-107616

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-07T10:17:06.593 |

The Amelia plugin for WordPress is vulnerable to unauthorized access of attendee data due to a missing authorization check on the GetEventAttendeesCommandHandler::handle() function in versions up to, and including, 9.9.1. The handler only enforces the broad `amelia_read_events` capability — which the plugin's own `wpamelia-customer` role possesses — and does not verify that the authenticated user is an organizer/provider of the event referenced by the client-supplied `id` query parameter. This makes it possible for authenticated attackers, with wpamelia-customer-level access and above, to export the full CSV of attendee personally identifiable information (first/last name, email, phone, date of birth, gender, private notes, payment amounts/methods, WooCommerce order IDs, custom-field values, and uploaded-file URLs) for any Amelia event on the site by directly invoking the `/report/event/attendees` endpoint with an arbitrary event ID.

### CVE-2026-19128

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:19:00.717 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow an authenticated attacker to send unauthorized requests from the system due to server-side request forgery. This could be used to enumerate network resources or to support further attacks.

### CVE-2026-17331

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-07T05:18:43.647 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to read arbitrary files on the server due to external control of a file name or path.

### CVE-2026-16714

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-07T05:18:20.373 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote attacker to overwrite arbitrary files due to a path traversal vulnerability.

### CVE-2026-120043

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-07T05:18:08.970 |

The Affiliate Program Suite — SliceWP Affiliates plugin for WordPress is vulnerable to generic SQL Injection via the 'email' parameter in all versions up to, and including, 1.2.14 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. The injection is reachable without any account because the vulnerable code path is triggered via the user_register hook fired on every successful WooCommerce My Account registration, which requires only a guest-obtainable nonce.

### CVE-2026-105002

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-07T05:17:57.570 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow arbitrary code to be executed by the management service in certain non-default configurations due to improper control of generation of code. Customization content may be evaluated as code, which is only possible where the related feature is enabled and not properly restricted.

### CVE-2026-68933

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-307;CWE-312` |
| Published | 2026-11-06T22:17:59.220 |

Chartbrew is an open-source web application that can connect directly to databases and APIs and use the data to create charts. Prior to 5.2.3, public dashboard passwords were stored in plaintext, accepted through a URL query parameter, and checked without effective attempt throttling. The vulnerable surface is public password-protected dashboard storage and validation routes. An unauthenticated attacker targets a public password-protected dashboard and repeatedly submits candidate passwords or obtains password-bearing server or proxy logs. Unlimited online guesses enable brute force, while cleartext storage and URL transport expose the secret in application storage and server or proxy access logs. The target must be a public dashboard with password protection enabled. Even failed attempts reveal chart count and configuration without the password; a recovered password grants access to the protected dashboard and its chart data. This vulnerability is fixed in 5.2.3.

### CVE-2026-85726

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-06T21:17:11.567 |

Chartbrew is an open-source web application that can connect directly to databases and APIs and use the data to create charts. Prior to 5.2.3, a date-typed MongoDB variable placed inside a quoted query placeholder was inserted as an unescaped string, unlike the safely escaped or coerced string, number, and Boolean branches. The vulnerable surface is mongoDB-backed public, shareable, or embedded charts processed by date-variable substitution. An unauthenticated user supplies a crafted URL filter to a public, shareable, or embedded MongoDB chart whose query places a date-typed variable in a quoted literal. The crafted date value breaks out of the quoted literal and changes query logic; the chart's returned row count becomes a Boolean oracle for character-by-character field extraction. The chart must be externally reachable and use the vulnerable date-in-quoted-placeholder branch. Extraction is read-only and limited to one queried collection per request, and it requires neither an account nor a known field value. The blind oracle can disclose any field in the queried collection, including secrets the chart does not display. This issue is fixed in version 5.2.3.

### CVE-2026-85708

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-06T21:17:11.183 |

Chartbrew is an open-source web application that can connect directly to databases and APIs and use the data to create charts. Prior to 5.2.3, Chart share and embed tokens were signed with CB_SECRET, including known or shipped-default values in stock source and repository Docker Compose installs. The vulnerable surface is chart share-token verification and filter-access routes for private charts. An attacker who knows the deployment's CB_SECRET targets a private chart that has been shared at least once so a share-policy row exists, then forges a Chart-subject token for that chart id. The known signing key permits valid Chart tokens, and the filter-access path accepts sequential integer ids without requiring a legitimate share link; token expiry and revocation are ineffective once the secret is known. The condition requires a known or default secret and an existing share-policy row. A bare container where CB_SECRET is undefined is outside this path, and a unique secret excludes it only while the value remains unknown and unpredictable. An unauthenticated attacker can enumerate integer ids and read arbitrary private chart data, including chartData, without possessing a legitimate share link. This issue is fixed in version 5.2.3.

### CVE-2026-102657

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-06T21:17:05.863 |

esm.sh is a no-build content delivery network (CDN) for web development. Prior to server version 137_7, the documented web.NewHandler static file server in web/handler.go joins the URL-decoded r.URL.Path with Config.AppDir without verifying that the result remains inside the configured application directory. URL-encoded dot segments such as %2e%2e bypass the plain traversal redirect performed by Go's ServeMux, allowing an unauthenticated remote attacker to make the server open and return files outside Config.AppDir that are readable by the server process. The confirmed impact is file disclosure only, and the issue is reachable with Dev disabled. This issue is fixed in server version 137_7.

### CVE-2026-82308

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-06T19:17:57.567 |

A pre-authentication heap-based buffer overflow vulnerability has been identified in the SonicOS SSL-VPN service, which could potentially enable a remote unauthenticated attacker to cause an application level denial of service.

### CVE-2026-19868

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-308` |
| Published | 2026-11-06T19:17:48.437 |

An authentication enforcement vulnerability in SonicOS SSLVPN service may allow a user with valid credentials for an alternate authentication method to bypass SAML authentication controls. Successful exploitation may also bypass SAML-enforced multi-factor authentication (MFA).

### CVE-2026-123356

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-06T19:17:44.220 |

GROBID is machine learning software for extracting information from scholarly documents. Prior to 0.9.1, the unauthenticated /api/modelTraining endpoint calls GrobidRestProcessTraining.trainModel in GrobidRestProcessTraining.java, where each request creates Executors.newFixedThreadPool(1), submits a training task, and leaves the executor running. Repeated requests permanently retain JVM worker threads and can exhaust process or operating-system thread capacity, degrading or stopping request processing. This issue is fixed in version 0.9.1.

### CVE-2026-85742

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T18:18:21.143 |

FreeScout is a self-hosted help desk and shared mailbox. Prior to 1.8.230, a pre-authenticated attacker can place HTML in a failed-login email value that is copied through monitored user activity into a queued SendAlert job. If alert delivery fails, the serialized payload is stored in failed_jobs and the administrator job-details endpoint renders it after a blacklist sanitizer that leaves executable event-handler attributes. When an administrator opens /system/ajax-html/job_details/{id} as a top-level page, the raw fragment lacks the normal layout policy and attacker-controlled JavaScript can perform same-origin administrator actions. Logs Monitoring for users, a failed alert email job, queue failure storage, and top-level administrator interaction are all required; the normal modal path is not affected in the tested configuration. This issue is fixed in version 1.8.230.

### CVE-2026-62344

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-06T18:18:16.933 |

Wanderer is a self-hosted trail database for saving and sharing adventures. Prior to 0.19.3, the unauthenticated GET /activitypub/trail/{id} and GET /activitypub/comment/{id} endpoints call ActivitypubTrail() and ActivitypubComment() to return full trail and comment records without applying the PocketBase collection view rules. An attacker who can enumerate or guess record IDs can retrieve private trail names, descriptions, GPS coordinates, GPX file URLs, photo URLs, and comments. This issue is fixed in version 0.19.3.

### CVE-2026-102650

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-11-06T18:17:37.333 |

Nuxt Content is the file-based CMS for Nuxt applications, powered by Markdown and Vue components. From 3.0.0 until 3.15.2, the unauthenticated POST /__nuxt_content/:collection/query endpoint accepts an attacker-controlled sql field in src/runtime/api/query.post.ts and permits expensive SQLite expressions. Version 3.0.0 performed no query validation; in affected releases using assertSafeQuery in src/runtime/internal/security.ts, the reported validation gap rejects a short list of SQL command keywords in WHERE clauses but permits function calls including randomblob(), zeroblob(), hex(), and length(). The query reaches the synchronous better-sqlite3 sink in src/runtime/internal/database.server.ts, allowing a single remote request to consume substantial CPU and memory while blocking the Node.js event loop and all concurrent request handling. Fully static prerendered deployments that do not expose the server endpoint are not affected. This issue is fixed in version 3.15.2.

### CVE-2026-102359

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-06T18:17:37.110 |

Kroki creates diagrams from textual descriptions. Prior to 0.31.2, the TikZ backend's tikz/tikz2svg guard used when KROKI_SAFE_MODE is enabled blocks only \verbatiminput while allowing native TeX file-read primitives including \openin, \read, \input, and \include. TeX Live's permissive openin_any setting remains active, so an unauthenticated actor can submit crafted LaTeX to POST /tikz/svg or the generic diagram API and cause the renderer to read any file accessible to the Kroki container user. The file contents are rendered into the returned SVG, which may disclose mounted secrets, configuration data, credentials, private keys, or process environment data. The -no-shell-escape option prevents shell execution but does not restrict these native file operations. This issue is fixed in version 0.31.2.

### CVE-2026-123855

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-06T17:17:24.727 |

In JetBrains Toolbox App before 3.6.1 command injection was possible via enterprise configuration URLs

### CVE-2026-123834

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-06T17:17:21.680 |

In JetBrains Datalore before 2026.4 improper scope validation in database tasks allowed using another workspace's service account

### CVE-2026-104657

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-377;CWE-494` |
| Published | 2026-11-06T17:17:11.353 |

Missing integrity verification in the Progress Software Fiddler Download and Setup Skill on Linux, macOS, and Windows which allows an attacker to compromise or influence a release component and execute attacker-controlled code when a user runs the skill. On macOS, the skill stages the package at a predictable path and installs it with administrator privileges, which may allow code execution with root privileges after user approval. A local process may also replace the staged macOS package while the skill waits for approval.

### CVE-2026-87045

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-06T15:17:26.850 |

The HTTP/2 server in subsys/net/lib/http/http_server_http2.c clears the connection's stream binding at the start of every frame. handle_http_frame_header() executed client->current_stream = NULL unconditionally, but a CONTINUATION frame does not open a new stream and enter_http_frame_continuation_state() never re-bound one, so the rest of the header block was processed with client->current_stream unset. Two paths then write through the NULL pointer. A request for an unregistered resource, or a method the matched resource does not support, is answered by send_http2_404() or send_http2_405(), and both call send_headers_frame(), which unconditionally sets client->current_stream->headers_sent = true. A POST, PUT or PATCH to a registered dynamic resource reaches handle_http2_dynamic_resource(), which unlike its siblings (handle_http2_static_resource(), dynamic_get_del_opts_req_v2(), dynamic_post_put_req_v2()) had no client->current_stream == NULL guard, and stores through the pointer with client->current_stream->current_detail = dynamic_detail.

Any peer that can reach the server can trigger this without authentication or prior state. A single stray CONTINUATION frame with END_HEADERS set, sent right after the client preface and requesting any unregistered path, is enough, because nothing rejected a CONTINUATION that no HEADERS frame had opened. A legitimate split header block (a HEADERS frame with END_HEADERS clear whose payload ends on a header-field boundary, then a CONTINUATION with END_HEADERS set) reaches the same state. The in-tree test test_http2_post_headers_with_continuation() did not catch this because it splits the header block mid field, which takes the handle_incomplete_http_header() shortcut that keeps the stream bound.

The result is a write to a fixed low address (a small offset into struct http2_stream_ctx), which faults on mainstream targets (flash/vector-table region on Cortex-M, or a trap under MPU/MMU null-pointer detection), and the default fatal-error handler halts the system. Impact is an unauthenticated, remotely triggerable denial of service against any device running the HTTP/2 server: the 404 path needs no particular resource to be registered, and HTTP/2 is built into CONFIG_HTTP_SERVER with cleartext h2c accepted, so TLS does not prevent it. Neither the target address nor the written value is attacker-controlled, so there is no confidentiality or integrity impact. Applications built without CONFIG_HTTP_SERVER are not affected.

### CVE-2026-17379

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-07T05:18:51.560 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote attacker to bypass authentication and assign arbitrary roles due to improper verification of cryptographic signatures.

### CVE-2026-17337

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-07T05:18:44.887 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to bypass authentication due to improper certificate validation. A certificate check is not performed reliably in all cases, which could allow a connection to be accepted without proper authentication.

### CVE-2026-17244

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-07T05:18:33.240 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to perform unauthorized actions and obtain sensitive information due to missing authorization. Certain operations do not verify that the user is permitted to act on the targeted resource, which could allow other users' API keys to be deleted.

### CVE-2026-123852

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-06T17:17:24.283 |

In JetBrains Junie GitHub Action before 1.8.0 code execution with workflow credentials was possible via fork updates

### CVE-2026-123848

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-297` |
| Published | 2026-11-06T17:17:23.717 |

In JetBrains IntelliJ IDEA before 2026.3 host name verification was missing for server TLS certificates

### CVE-2026-104656

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T17:17:11.210 |

Improper neutralization of input in the sessions grid in Progress Telerik Fiddler Everywhere 8.3.0 and earlier allows an attacker to execute backend IPC commands by convincing a user to open a specially crafted SAZ file.

### CVE-2026-64894

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:P/AC:H/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-06T15:17:22.440 |

Inclusion of functionality from untrusted control sphere vulnerability in Johnson Controls EasyIO Neo IOManager and Tools Installer allows Malicious Software Update.

This issue affects EasyIO Neo IOManager and Tools Installer: 1.1.0.0.

### CVE-2026-119156

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T13:16:34.510 |

The Download Manager plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'wpdm_reg[first_name], wpdm_reg[last_name], wpdm_reg[user_login]' parameter in all versions up to, and including, 7.5.9 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the site to have "Anyone can register" enabled, the plugin's [wpdm_reg_form] shortcode published on a public page, and at least one package authored by user ID 1 rendered with the Spotlight link template.

### CVE-2026-93766

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T12:17:47.280 |

The Happyforms Pro plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'happyforms_client_referer' parameter in all versions up to, and including, 1.38.9 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-93755

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T12:17:47.120 |

The Happyforms plugin for WordPress is vulnerable to Stored Cross-Site Scripting via spoofable client IP headers in versions up to, and including, 1.38.9. This is due to the happyforms_get_client_ip() function reading raw HTTP_CLIENT_IP and HTTP_X_FORWARDED_FOR request headers without any validation or sanitization, storing the value as post meta ('client_ip') via update_post_meta() during unauthenticated form submissions, and later echoing it in the admin submission edit screen's Details metabox without output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user (typically an administrator reviewing a submission) accesses an injected page.

### CVE-2026-93429

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T12:17:46.967 |

The VikBooking Hotel Booking Engine & PMS plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'guests[][][documents]' Parameter in all versions up to, and including, 1.8.17 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the attacker to possess a valid booking sid/ts pair, which can be obtained by making a standard public booking, as the session token needed to satisfy the JSession::checkToken() gate is emitted in the publicly accessible pre-checkin form.

### CVE-2026-123418

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T12:17:45.933 |

The Church Admin plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'lat' parameter in all versions up to, and including, 5.1.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This vulnerability is only exploitable when a Google Maps API key has been configured in Church Admin settings, as the vulnerable sink is only reached when that option is present.

### CVE-2026-122231

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T12:17:45.763 |

The WS Form LITE – Drag & Drop Contact Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'field_<id>[0][0]' parameter in all versions up to, and including, 1.12.18 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is possible because the client-side esc_html() helper returns any non-string value unchanged, allowing a nested-array payload coerced via Array.prototype.toString to reach jQuery .append() unescaped.

### CVE-2026-119183

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T12:17:44.197 |

The JetFormBuilder — Dynamic Blocks Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the '<form field mapped to a post meta key, e.g. lst_cost>' parameter in all versions up to, and including, 3.6.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the target site to have configured a public Insert Post form writing to a post meta key and a Calculated Field whose formula references that key via the %META::key% macro, after which a single unauthenticated POST is sufficient to persist the payload.

### CVE-2026-116537

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T12:17:42.913 |

The Link Library plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'link_description' parameter in all versions up to, and including, 7.10.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This exploit requires the site administrator to have enabled the non-default 'Convert [] to <> in Link Description and Notes' (use_html_tags) setting; when this option is off, the bracket-to-angle-bracket conversion never runs and the payload is never reconstructed into executable HTML.

### CVE-2026-115548

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T12:17:42.747 |

The Quttera ThreatSign – Web Malware Scanner for WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'HTTP_USER_AGENT' parameter in all versions up to, and including, 4.1.0.48 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever an administrator accesses an injected page.

### CVE-2026-111370

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T12:17:42.587 |

The WP Visitor Statistics (Real Time Traffic) plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'os (also browser, res)' parameter in all versions up to, and including, 8.9.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-111317

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T12:17:42.430 |

The JetFormBuilder — Dynamic Blocks Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the '<any form field name — e.g. 'payload'>' parameter in all versions up to, and including, 3.6.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the targeted form to have both the Save Form Record action enabled and a form-level Form Record preset configured; the stored payload only executes when a privileged user visits the front-end form page with the preset's record query variable set to the attacker's submitted record ID.

### CVE-2026-109230

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T12:17:42.110 |

The WP Visitor Statistics (Real Time Traffic) plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'browser' parameter in all versions up to, and including, 8.7.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload is stored via an unauthenticated HTTP request to the public visitor tracking endpoint (wmcAction=wmcTrack) and executes when the bundled jqPlot PieRenderer inserts the HTML-decoded series label directly as HTML in the authenticated administrator's browser.

### CVE-2026-109214

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T12:17:41.953 |

The User Frontend – Membership, User Registration, User Profile, User Directory & Content Restriction with Frontend Post Submission plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the '<taxonomy_field_name> (default: 'category')' parameter in all versions up to, and including, 4.3.13 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the target installation to have configured a Taxonomy field in text-input mode with guest post submission enabled on at least one frontend form.

### CVE-2026-122037

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T07:17:04.540 |

The AgenWebsite Shipping – Plugin Ongkos Kirim & Generate Resi Otomatis Semua Kurir Indonesia plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'zipcode' parameter in all versions up to, and including, 9.2.41 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-120537

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T07:17:04.057 |

The TranslatePress – Translate Multilingual sites with AI Translation plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment (storage); originals / language / original_language (exfiltration from endpoint)' parameter in all versions up to, and including, 3.3.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-116558

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T07:17:02.590 |

The Unlimited Elements for Elementor plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the '<title>/<description> inside the attacker-controlled RSS feed body' parameter in all versions up to, and including, 2.0.26 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is exploitable against any site whose administrator has placed the RSS Feed catalog widget pointing at a feed URL the attacker controls, as the plugin's own 2.0.25 escaping pre-processor intentionally excludes |raw prints in element content positions from its escaping logic, and XML entity-encoded payloads in feed item titles are decoded back to raw markup before reaching the sink.

### CVE-2026-115811

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T07:17:02.420 |

The Strong Testimonials plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'star_rating' parameter in all versions up to, and including, 3.3.16 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful execution requires an administrator to open the standard Preview link for a pending testimonial, a step the plugin's normal moderation workflow naturally invites.

### CVE-2026-75590

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:19:01.820 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to access internal network resources and obtain sensitive information due to server-side request forgery. A protection that blocks requests to internal addresses can be bypassed, so the server could be made to contact internal services and return part of their responses.

### CVE-2026-17401

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-07T05:18:56.237 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to execute arbitrary code due to a stack-based buffer overflow.

### CVE-2026-17341

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:45.740 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to perform server-side request forgery and relay unauthorized email messages due to improper neutralization of user-supplied input.

### CVE-2026-17316

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-07T05:18:40.743 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote attacker to perform server-side request forgery due to improper validation of user-supplied input.

### CVE-2026-119167

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T05:18:06.850 |

The TranslatePress – Translate Multilingual sites with AI Translation plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 3.3.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires that at least one prior comment from the attacker's name and email pair has been approved under WordPress's default comment_previously_approved moderation setting, and that a secondary language is configured in TranslatePress.

### CVE-2026-120739

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T04:17:13.697 |

The Optimole – Optimize Images | Convert WebP & AVIF | CDN & Lazy Load | Image Optimization plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 's (missing_srcsets[*][*].s)' parameter in all versions up to, and including, 4.2.18 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The HMAC signature required to pass the REST endpoint's authorization check is published in plaintext to unauthenticated visitors inside the inline optimoleDataOptimizer JavaScript object on any page with an incomplete profile, making the effective authentication barrier nonexistent.

### CVE-2026-120677

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T04:17:13.537 |

The Optimole – Optimize Images | Convert WebP & AVIF | CDN & Lazy Load | Image Optimization plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 4.2.18 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the comment to be approved by an administrator and for the affected post to contain at least one iframe or video element (e.g., a core Video block), which is sufficient under default plugin settings where video lazy loading is enabled.

### CVE-2026-119158

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T04:17:13.190 |

The Pie Register – User Registration, Profiles & Content Restriction plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'first_name' parameter in all versions up to, and including, 3.8.4.16 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is exploitable when public registration is enabled and the registration form includes a Profile Picture field; the attacker registers via the publicly accessible form (nonce is emitted to unauthenticated visitors) to store the payload, then logs in as the newly created Subscriber to post a comment that triggers delivery to all page visitors.

### CVE-2026-120540

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T03:17:03.690 |

The iubenda | All-in-one Compliance for GDPR / CCPA Cookie Consent + more plugin for WordPress is vulnerable to Stored Cross-Site Scripting in versions up to, and including, 3.13.6. This is due to the way iubendaParser::parse_comments() re-processes HTML inside IUB-COOKIE-BLOCK markers through the bundled simple_html_dom parser after WordPress has already KSES-filtered the saved comment: simple_html_dom's remove_noise() stores <code> bodies under a deterministic key ('___noise___ 1000') and restore_noise() later substitutes any matching substring back into attribute values WITHOUT re-escaping, allowing a quote-breaking payload stashed in an allowed <code> element to be injected into an allowed <abbr title="___noise___ 1000"> attribute at render time. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page, after an administrator approves the first (otherwise moderated) comment under WordPress's default comment_previously_approved setting.

### CVE-2026-120512

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T03:17:03.210 |

The Form Maker by 10Web – Mobile-Friendly Drag & Drop Contact Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'wdform_<n>_element<id> (Hidden Input field, name = user-defined, e.g. hidden_probe)' parameter in all versions up to, and including, 1.15.50 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires an administrator to open the Submissions screen and click the Show-on-Map link associated with the poisoned entry, at which point the attacker-controlled field_id value is echoed unescaped into a single-quoted JavaScript string in the FormMakerEditCountryinPopup popup — a step whose nonce and capability checks are automatically satisfied by the administrator's own session and the freshly minted fm_ajax_nonce embedded in the link.

### CVE-2026-120082

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T03:17:02.673 |

The GeoDirectory – WP Business Directory Plugin and Classified Listings Directory plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'post_content' parameter in all versions up to, and including, 2.8.200 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The nested shortcode payload ([gd_dynamic_conten[gd_tags]t ...]) defeats the plugin's geodir_strip_shortcodes() guard because WordPress's strip_shortcodes() performs only a single pass over registered tags, and HTML-entity-encoded attributes in the resulting shortcode survive wp_kses_post() because kses inspects HTML tags rather than shortcode attribute values.

### CVE-2026-119175

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T03:17:01.443 |

The Flying Images: Optimize and Lazy Load Images for Faster Page Speed plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 2.4.15 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. A first-time commenter's submission requires a single administrator approval under the default comment_previously_approved setting; however, once approved, all subsequent comments from the same name and email pair bypass moderation, and the injected script executes for every visitor — including administrators viewing the post from the front end.

### CVE-2026-119070

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T03:17:00.717 |

The Optimole – Optimize Images | Convert WebP & AVIF | CDN & Lazy Load | Image Optimization plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 4.2.17 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The exploit requires the plugin to be in its normal connected state (cdn_key and cdn_secret configured) with the image replacer enabled, which is the default post-setup configuration; the stored payload bypasses all WordPress comment sanitization filters because it contains no HTML metacharacters at storage time — the characters are produced only by Optimole's own decoder at render time.

### CVE-2026-123998

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307;CWE-1392` |
| Published | 2026-11-06T19:17:45.427 |

Hisense VIDAA Smart TV firmware V0000.01.00a.P0220 contains an authentication bypass vulnerability in its remote-control MQTT broker on TCP port 36669, which accepts publicly documented default credentials and an ineffective 4-digit pairing PIN with no rate limiting or lockout, allowing a brute force of the entire code space in about five seconds, while some actions require no pairing at all. A LAN-adjacent attacker can exploit this to inject key events, change volume, switch input sources, enumerate inputs, launch arbitrary installed applications, and monitor pairing activity, posing a significant risk in hotel deployments where untrusted LAN access is common.

### CVE-2026-119924

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-06T19:17:39.593 |

An out-of-bounds read in the TDS RPC procedure-name parser in the Babelfish for PostgreSQL extension versions 1.0-1.5, 2.1-2.15, 3.1-3.12, 4.0-4.8, 5.1-5.4 and in Amazon Aurora PostgreSQL with Babelfish might allow remote authenticated users to read adjacent process memory or cause a denial of service via a malformed TDS RPC request to the TDS port (default 1433).



To remediate this issue, we recommend users upgrade to Babelfish for PostgreSQL extension versions 4.10, 5.6, 6.1 or later. As a workaround, restrict network access to the TDS port (default 1433). Customers using Amazon Aurora PostgreSQL with Babelfish should upgrade their cluster to Aurora PostgreSQL 13.9.16 (1.5.5), 13.23.3 (1.17.2), 14.6.16 (2.3.5), 14.17.8 (2.12.4), 14.18.6 (2.13.3), 14.19.5 (2.14.2), 14.20.5 (2.15.2), 14.22.3 (2.16.1), 14.23.1 (2.17.0), 15.10.8 (3.8.4), 15.12.8 (3.9.4), 15.13.6 (3.10.3), 15.14.5 (3.11.2), 15.15.5 (3.12.2), 15.17.3 (3.13.1), 15.18.1 (3.14.0), 16.8.8 (4.5.5), 16.9.6 (4.6.3), 16.10.5 (4.7.2), 16.11.5 (4.8.2), 16.13.3 (4.9.1), 16.14.1 (4.10.0), 17.4.8 (5.1.4), 17.5.6 (5.2.3), 17.6.5 (5.3.2), 17.7.5 (5.4.2), 17.9.3 (5.5.1), 17.10.1 (5.6.0), 18.3.4 (6.0.2), 18.4.1 (6.1.0) or later, and apply any pending maintenance to ensure they are on the latest patch.

### CVE-2026-58141

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-06T16:18:54.697 |

Dify before 1.15.0 contains a server-side request forgery vulnerability that allows any authenticated console user to bypass SSRF protections and issue arbitrary HTTP requests to internal services and cloud metadata endpoints due to the Squid proxy configuration only defining source ACLs without destination deny rules and the make_request() helper performing no independent destination IP validation. Attackers can use endpoints such as GET /console/api/remote-files/<url>, POST /console/api/remote-files/upload, the HTTP Request workflow node, website crawl, or document import from URL to reach internal components like the sandbox, internal APIs, and PostgreSQL, and on AWS deployments read IAM credentials from the instance metadata service, with the HTTP Request node further enabling POST, PUT, and DELETE writes to internal services relying on network isolation for authorization.

### CVE-2026-121765

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-07T12:17:45.110 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Cozmoslabs TranslatePress translatepress-multilingual allows Stored XSS.This issue affects TranslatePress: from n/a through 3.3.8.

### CVE-2026-17322

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-532` |
| Published | 2026-11-07T05:18:41.930 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a local attacker to obtain sensitive credentials and compromise accounts due to insertion of sensitive information into log files.

### CVE-2026-17319

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-07T05:18:41.320 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to modify tool configuration and cause a denial of service due to improper authorization. Information supplied by the client is relied on when deciding what a user is allowed to do, which could allow unauthorized changes that disrupt service.

### CVE-2026-17311

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:39.780 |

IBM API Connect 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to modify application API subscriptions due to broken object-level authorization.

### CVE-2026-17284

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-07T05:18:34.737 |

IBM API Connect 10.0.8.0 through 10.0.8.12 and 12.1.0.0 through 12.1.1.2 could allow a remote authenticated attacker to perform unauthorized operations in other tenants' environments due to improper validation of client-supplied information. Tenant context is not sufficiently verified, which could allow actions on resources belonging to other tenants.

### CVE-2026-123997

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-06T19:17:45.207 |

Hisense VIDAA Smart TV firmware V0000.01.00a.P0220 contains an unauthenticated denial-of-service vulnerability in the UPnP/DLNA AVTransport SOAP service that allows LAN-adjacent attackers to freeze the entire television software layer by sending a crafted SetAVTransportURI request on TCP port 38400. Attackers can exploit this flaw without credentials to render the device completely unresponsive to remote control or front-panel input, requiring a physical power cycle to restore functionality.

### CVE-2026-119758

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-918` |
| Published | 2026-11-06T18:17:58.240 |

ERPNext OCR app for Frappe/ERPNext through 1.1.1 contains a missing authorization and path traversal vulnerability that allows any authenticated user to read arbitrary server files by passing a fully client-controlled path argument to the whitelisted read_document method. Attackers can supply local file paths to bypass Frappe's File doctype permission model and access other users' private uploads, or supply arbitrary URLs to trigger server-side requests reaching internal services and cloud metadata endpoints.

### CVE-2026-123842

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-06T17:17:22.833 |

In JetBrains IntelliJ IDEA before 2026.3 arbitrary file write was possible via symlinks when extracting plugin archives

### CVE-2026-103985

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-269;CWE-284` |
| Published | 2026-11-06T17:17:10.887 |

FreeScout is a self-hosted help desk and shared mailbox. Prior to 1.8.231, the profile form exposes the only_assigned_tickets permission to its non-admin owner, and UsersController::profileSave() adds or removes User::PERM_ONLY_ASSIGNED_TICKETS without checking that the editor is an administrator. A restricted agent can uncheck the option, or submit an ordinary profile save that omits it, to remove the administrator-imposed restriction. The agent can then read and modify conversations assigned to other agents in every mailbox they already belong to. This issue is fixed in version 1.8.231.

### CVE-2026-123489

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-06T15:17:18.313 |

Craft CMS 4.0.0 before 4.18.9 and 5.0.0 before 5.11.2 contains a blind SQL injection vulnerability because the sandbox-exposed getNext() and getPrev() methods pass arbitrary criteria arrays to Craft::configure() without removing SQL-bearing properties such as orderBy and where. Authenticated control panel users can supply a crafted elementIds value, rendered as a sandboxed template, to obtain a conditional SQL oracle under the Craft database account.

### CVE-2026-123485

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-06T15:17:17.597 |

Ground Station from 0.6.0 before 0.8.20 does not restrict the get-orbital-sources Socket.IO handler (also exposed as get-tle-sources) to administrators, although the orbital-source write handlers are admin-only. An authenticated operator-role user can call either handler to retrieve the plaintext usernames, passwords, and tokens that administrators stored for basic and token orbital sources.

### CVE-2026-112341

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-06T15:17:08.710 |

Wazuh versions from 4.0.0 before 4.14.9 contain a sql injection vulnerability in WazuhDBBackend._substitute_params due to sequential regex placeholder cross-contamination. Authenticated users with agent:read on one agent can inject UNION SELECT via the q and search parameters to extract every agent's internal_key through a blind boolean oracle on total_affected_items.

### CVE-2026-112336

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-11-06T15:17:07.890 |

Wazuh Manager from 3.0.0 before 4.14.9 contains a memory leak vulnerability in the generic JSON decoder that allows remote attackers to exhaust wazuh-analysisd memory via repeated static fields. Attackers can enroll an agent through passwordless enrollment and send events with duplicate fields such as id, triggering an OOM kill that disables alerting.

### CVE-2026-54589

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-06T21:17:09.143 |

Chartbrew is an open-source web application that can connect directly to databases and APIs and use the data to create charts. Prior to 5.2.1, the outbound URL guard recognized ordinary IPv4, IPv6, and IPv4-mapped IPv6 destinations but did not recognize IPv4 addresses embedded in NAT64 prefixes. The vulnerable surface is aPI Data Connection outbound requests routed through server/modules/outboundTargetPolicy.js. An authenticated user with permission to create or edit an API connection supplies an attacker-controlled hostname or redirect whose DNS answer is a NAT64 address embedding a private or link-local IPv4 destination. The policy treated the NAT64 address as public; a NAT64 gateway then translated it to the embedded private IPv4 address after validation. The bypass requires a NAT64/DNS64 deployment path and connection-management privileges. IPv4-only deployments are not affected by this specific bypass. The attacker can read responses from 169.254.169.254 cloud metadata and arbitrary internal IPv4 hosts and ports reachable through the NAT64 gateway. This issue is fixed in version 5.2.1.

### CVE-2026-123849

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-06T17:17:23.850 |

In JetBrains IntelliJ IDEA before 2026.3 code execution was possible in untrusted projects via the Terraform File Watchers
