# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-31 15:01 UTC
- **対象期間**: `2026-10-30T15:00:45.000Z` 〜 `2026-10-31T15:01:21.000Z`
- **重要CVE数**: 217 件（Critical 9.0+: 41 件 / High 7.0〜: 176 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVSS 7.0 以上の脆弱性は、**認証バイパス／認証なしでのリモートコード実行** が集中しています。特に、コンテナ/仮想化基盤（LXD）、IoT/AI プラットフォーム、そして WordPress 系プラグインに対する攻撃面が拡大。  
多くは **デフォルト設定のまま** で利用されることが前提となっており、**パッケージのバージョン管理が甘い環境** での被害が顕著になると予想されます。  

---

## 2. 特に注目すべき CVE  

| CVE ID | CVSS | 主な問題点 | 影響範囲・利用シーン | 注目理由 |
|--------|------|------------|----------------------|----------|
| **CVE‑2026‑112816** | 10.0 | LXD HTTPS リスナーの証明書検証不備 | LXD 4.0‑5.0 系クラスター全体（Ubuntu・Canonical が提供） | **クラウド/オンプレミスの仮想化基盤全体が乗っ取られる** 可能性。クラスター管理者権限が取得できるため、他の VM すべてが危険に晒される。 |
| **CVE‑2026‑61826** | 10.0 | Bazarr API の認証抜け | Bazarr (Sonarr / Radarr 連携ツール) の `api_ns_plex` エンドポイント | **認証なしで任意の API 呼び出しが可能**。メディア管理サーバが外部に公開されているケースで、情報漏洩・改ざんリスクが高い。 |
| **CVE‑2026‑61738** | 10.0 | SOCFortress CoPilot の GCP レポート生成エンドポイントで任意コード実行 | SOCFortress CoPilot (SOC SaaS) の `/api/scoutsuite/generate-gcp-report` | **管理者・アナリスト権限が不要**で GCP 環境に対するコード実行が可能。SaaS 型のセキュリティ運用ツールが逆に攻撃側に回る危険性。 |
| **CVE‑2026‑62853** | 9.9 | ThingLinks の Groovy スクリプト無サンドボックス実行 | ThingLinks IoT プラットフォームの `/groovyScriptTest/registerScript` | **認証ユーザーが任意のサーバ側コードを実行**でき、IoT デバイス制御や内部ネットワークへの踏み台化が容易。 |
| **CVE‑2026‑119096** | 9.8 | WordPress 「Uncanny Toolkit for LearnDash」認証バイパス | LearnDash 学習管理プラグイン全インスタンス | **`email` パラメータの不正処理により認証が回避**。教育系サイトで多数のユーザー情報が流出・改ざんされるリスク。 |

> **注:** 上記は **CVSS が 9.8 以上** かつ **広範囲にデプロイされている可能性が高い**（コンテナ基盤・メディアサーバ・SaaS・IoT・WordPress）点を重視して選出しました。

---

## 3. 推奨アクション  

### 3.1 共通対策
- **脆弱バージョンの即時排除**：対象パッケージ・プラグインのバージョンを確認し、ベンダーが提供する **修正版** へアップデート。  
- **デフォルト認証情報・シークレットの廃止**：`default JWT secret`、`hard‑coded session_key` などは必ず **環境変数やシークレット管理ツール** に置き換える。  
- **外部公開エンドポイントのアクセス制御**：API がインターネットに露出している場合は **IP フィルタリング、WAF ルール、Zero‑Trust ネットワーク** で保護。  
- **証明書・TLS 設定の見直し**：LXD などは **CA 署名証明書の検証を強制**（`client.verify_certificates = true`）し、自己署名証明書は使用しない。  
- **監査ログの有効化**：認証失敗・管理者権限取得イベントを **SIEM** に集約し、異常検知ルールを追加。

### 3.2 個別対策

| CVE | 修正バージョン / パッケージ | 具体的な作業 |
|-----|----------------------------|--------------|
| **CVE‑2026‑112816** | LXD **4.0.15**, **5.0.11**, **5.21.9**, **6.10.1** 以降 | `apt-get update && apt-get install lxd=4.0.15-...`（Ubuntu）<br>設定ファイル `/etc/lxd/lxd.conf` で `client.verify_certificates = true` を明示的に設定。 |
| **CVE‑2026‑61826** | Bazarr **1.5.7‑beta.14** 以上 | `pip install --upgrade bazarr==1.5.7-beta.14` または Docker イメージを最新版に差し替え。<br>`api_ns_plex` エンドポイントを **認証必須** にするカスタムミドルウェアを導入。 |
| **CVE‑2026‑61738** | SOCFortress CoPilot **0.1.77** 以上 | `docker pull socfortress/copilot:0.1.77` → デプロイ更新。<br>GCP レポート生成 API の **ロールベースアクセス制御** を再確認し、不要な `admin`/`analyst` ロールを削除。 |
| **CVE‑2026‑62853** | ThingLinks **1.4.0** 以上 | `npm install thinglinks@1.4.0`（または公式 Docker イメージ）。<br>Groovy スクリプト受け取り API に **サンドボックス (e.g., GroovySandbox)** を導入し、`Content‑Security‑Policy` で実行権限を制限。 |
| **CVE‑2026‑119096** | Uncanny Toolkit for LearnDash **3.8.3** 以上 | WordPress 管理画面 → プラグイン更新で **3.8.3** へアップデート。<br>`email` パラメータのバリデーションを **正規表現** で厳格化し、プラグイン開発者にパッチ適用を要請。 |

### 3.3 追加の防御策
- **コンテナイメージのスキャン**：Trivy、Anchore などで LXD、Bazarr、SOCFortress のイメージを定期的にスキャンし、脆弱性が検出されたら自動的に再ビルド。  
- **CI/CD パイプラインでの依存関係ロック**：`requirements.txt`、`package.json`、`composer.json` などは **SHA‑256 ハッシュ** で固定し、脆弱バージョンが混入しないようにする。  
- **ペネトレーションテスト**：特に API エンドポイント（`/api_ns_plex`, `/api/scoutsuite/generate-gcp-report`, `/groovyScriptTest/registerScript`）に対して **認証・入力検証テスト** を実施

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-61826

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-352;CWE-862` |
| Published | 2026-10-30T17:17:27.497 |

Bazarr is a companion application to Sonarr and Radarr. Prior to 1.5.7-beta.14, the `api_ns_plex` namespace in `bazarr/api/plex/oauth.py` omits `@authenticate` on its Resource handlers, while normal APIs require an API key and no global authentication hook compensates. Anonymous callers can invoke `POST /api/plex/oauth/logout` to clear credentials and disable the integration, or `POST /api/plex/apikey` to persist an attacker-selected key, without a PIN, account or state precondition. `POST /api/plex/oauth/pin` and `GET /api/plex/oauth/pin/<pin_id>/check` additionally allow an attacker who completes a PIN with an attacker-controlled Plex account to bind that account's token to the instance. `PlexPinCheck` skips state validation when `state_param` is absent and merely logs a mismatch without stopping execution. `POST /api/plex/select-server`, `POST /api/plex/oauth/servers`, `POST /api/plex/webhook/create`, `POST /api/plex/webhook/delete` and `POST /api/plex/encrypt-apikey` expose further `write_config()` operations. Attacker-controlled server URLs feed later outbound requests carrying the configured API key in `X-Plex-Token`, enabling server-side request forgery and credential exposure in addition to persistent configuration tampering and integration denial of service. Version 1.5.7-beta.14 closes the anonymous API-mutation path by adding authentication; complete OAuth state validation is not established and remains a separate residual for curator review.

### CVE-2026-112816

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-30T17:17:14.293 |

Improper certificate validation in the HTTPS listener in Canonical LXD 4.0.14, 5.0.10, 5.21.8, 6.9 before 4.0.15, 5.0.11, 5.21.9, 6.10.1 allows an unauthenticated attacker to authenticate as any trusted client and gain full access to the cluster and managed virtual machines via a crafted certificate chain.

### CVE-2026-61738

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73;CWE-434` |
| Published | 2026-10-30T15:16:53.507 |

SOCFortress CoPilot focuses on providing a single pane of glass for all your security operations needs. Prior to 0.1.77, `POST /api/scoutsuite/generate-gcp-report` in `backend/app/integrations/scoutsuite/routes/scoutsuite.py` admits admin and analyst users and validates the uploaded content as `GCPScoutSuiteJSON`, but passes raw `file.filename` from the multipart header to `save_file_to_directory` in `backend/app/integrations/scoutsuite/services/scoutsuite.py`. The writer combines this filename with `scoutsuite-report` using `os.path.join` without sanitization or a resolved-path containment check. A traversal filename therefore writes the supplied JSON outside the intended report directory. In the reported root-running backend, the researcher demonstrated root-owned writes outside that directory and into the application source directory. This permits host-file overwrite subject to the accepted JSON-content constraint and can disrupt application operation; the demonstrated primitive does not establish unrestricted executable contents or unconditional cross-tenant confidentiality loss. Version 0.1.77 removes caller-controlled filenames from the affected route; unrestricted-content and direct-code-execution claims require separate curator reconciliation.

### CVE-2026-62853

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-94` |
| Published | 2026-10-30T21:17:14.267 |

ThingLinks is an enterprise IoT platform. Prior to 1.4.0, the `/groovyScriptTest/registerScript` endpoint accepts user-supplied Groovy script content and passes it to an unsandboxed `Groovy compilation and loading` flow. An authenticated attacker can provide code that is compiled and instantiated on the server, resulting in arbitrary server-side code execution. The issue affects the `rule engine`'s Groovy script test/register flow. This issue is fixed in version 1.4.0.

### CVE-2026-61728

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79;CWE-922` |
| Published | 2026-10-30T15:16:52.937 |

SOCFortress CoPilot focuses on providing a single pane of glass for all your security operations needs. In affected snapshots preceding the respective 0.1.70 and 0.1.76 sink repairs, portal users, including `customer_user`, can submit stored markup through `POST /api/incidents/db_operations/alert/comment`. In `customer-portal/src/components/alerts/AlertDetails/AlertComment.vue`, `commentHtml` replaces newlines in `comment.comment` but passes the result to `v-html` without escaping or sanitizing HTML. When another user views the poisoned alert, stored script executes on the application origin; the same unsanitized rendering pattern affects server-stored SOC case, asset and health-check fields in `SocCaseNote.vue`, `SocCaseItem.vue`, `SocCaseAssetsItem.vue`, `SocAlertAssetsItem.vue` and `HealthcheckItem.vue`. The authentication store in `customer-portal/src/stores/auth.ts` persists both access and refresh tokens in JavaScript-readable storage, and `customer-portal/src/api/httpClient.ts` uses bearer headers rather than HttpOnly cookies. An injected script can steal both tokens, impersonate the viewer and obtain fresh tokens through `/auth/refresh`. If an analyst or administrator views the poisoned alert or case, this enables persistent privileged account takeover, cross-tenant data access, incident modification or deletion, and detection/response subversion. The health-check sink repair is first contained in version 0.1.70, while the comment and other SOC sink repairs are first contained in version 0.1.76. Version 0.1.76 is the provisional first release containing all observed repairs; grouped versus split CVE scope requires curator adjudication.

### CVE-2026-118235

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-31T09:16:33.620 |

The SimpleForm – Form Maker to Chat Apps with Quiz, Poll and Multi Lead Notifications plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 3.10.2 via the handle_upload function. This is due to missing server-side file key allowlist and pre-sanitization extension derivation that allows a trailing-dot filename to bypass all extension and MIME validation in handle_upload. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible. The only access control is a nonce that is printed into every public form's data-nonce attribute, making it trivially obtainable by any unauthenticated visitor on a page embedding the form shortcode.

### CVE-2026-119096

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-31T08:16:49.043 |

The Uncanny Toolkit for LearnDash plugin for WordPress is vulnerable to Authentication Bypass in versions up to, and including, 3.8.2 via the `email` parameter of the `uo_login_action()` function. This is due to a parser-differential flaw in which the plugin's account-verification gate resolves the submitted `email` value using the raw, unsanitized string passed to `get_user_by()`, while the subsequent `wp_signon()` call relies on WordPress core's internal `sanitize_user()` to strip appended junk characters — causing the gate lookup to fail and be skipped entirely while the real account is still resolved and authenticated. This makes it possible for unauthenticated attackers to log in to unverified or administrator-suspended accounts whose credentials they already possess, obtaining a valid `wordpress_logged_in` session cookie and defeating the plugin's account-approval and account-suspension controls. The nonce required to reach the handler is freely obtainable in the same request from the unauthenticated `ult-refresh-nonce` endpoint, making exploitation trivial for any attacker with network access to the site and knowledge of a target account's credentials.

### CVE-2026-116512

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-31T08:16:48.603 |

The Project Manager – AI Powered Project Management, Task Management, Kanban Board & Time Tracker plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 4.1.1 via the 'id' parameter parameter. This is due to unsanitized 'id' parameter value concatenated directly into the pipe-delimited validation rule string, which is then split and each token invoked as a dynamic PHP function with no allowlist check. This makes it possible for unauthenticated attackers to execute code on the server. This is exploitable by unauthenticated attackers because WordPress core executes the route argument's validate_callback inside WP_REST_Server::dispatch() before the route's permission_callback is invoked, meaning the Project_Manage_Capability authorization gate is never reached on the vulnerable code path.

### CVE-2026-109220

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-31T07:16:34.367 |

The PDF Invoice for WooCommerce + Drag and Drop Template Builder plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 7.1.1 via the 'customer_note' parameter parameter. This is due to insufficient sanitization of the customer_note checkout field, which is inlined verbatim into invoice HTML, entity-decoded back into a live tag by simplehtmldom, reassembled into raw bytes by mPDF, and passed to unserialize() in _getObjAttr without validation. This makes it possible for unauthenticated attackers to execute code on the server. An unauthenticated attacker can trigger the vulnerable code path on a default install by placing an anonymous WooCommerce checkout via the public Store API (POST /wc/store/v1/checkout) using a Direct Bank Transfer or cheque payment method, which automatically transitions the order to 'on-hold' status and fires the plugin's invoice-generation hook.

### CVE-2026-63377

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-30T23:17:14.267 |

TAKO AI Agent for Okta is a local-first AI agent that helps Okta administrators query tenant data using natural language. Prior to 3.0.1-beta, `POST /api/auth/setup` in `src/api/routers/auth.py` allows an unauthenticated network attacker to create the first administrator account before the legitimate owner completes initial setup. The `initial_setup` function checks only the `is_setup` completion flag and requires no authentication, one-time bootstrap token, or network restriction. The default `docker-compose.yml` publishes port 8001 on all interfaces, the `Dockerfile` starts the listener on 0.0.0.0, and `src/api/main.py` mounts the authentication router without a global authentication guard. The endpoint invokes `create_auth_user` with `UserRole.ADMIN` and `set_auth_cookie`, issuing a valid `fctr_session` JWT cookie. Localhost-only CORS rules do not restrict non-browser HTTP clients, and the setup operation does not require access to a real Okta tenant. The attacker becomes the sole administrator and prevents legitimate first-run setup, can read Okta-synced user data, API tokens, chat history, and application configuration, modify users and Okta integration credentials, and lock out administrators or disable the service. Already completed setup is rejected. This issue is fixed in version 3.0.1-beta.

### CVE-2026-61620

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-30T20:17:10.967 |

HoneySQL turns Clojure data structures into SQL. From 2.0.0 until 2.7.1392, applications that pass user input or other arbitrary data into the HoneySQL `DSL` by calling `keyword` or `symbol` on that input can produce SQL strings that facilitate SQL injection when executed unchanged by a `JDBC` driver. Some formatters do not apply the existing suspicious-character check to the resulting entity names. The impact depends on the privileges of the database connection executing the generated statement. Input validation before constructing `keyword` or `symbol` entities is a workaround. The maintainer-designated fixed version is 2.7.1392.

### CVE-2026-90888

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-30T19:20:18.680 |

Unauthenticated PHP Object Injection in LeadSnap <= 1.25 versions.

### CVE-2026-39738

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-30T19:18:24.427 |

Unauthenticated PHP Object Injection in FunnelKit Automations <= 3.8.6.1 versions.

### CVE-2026-119526

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-30T19:18:20.673 |

Deserialization of Untrusted Data vulnerability in ThemeREX Royal Event allows Object Injection.

This issue affects Royal Event: from n/a through 2.0.

### CVE-2026-116386

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-30T19:18:13.640 |

Unauthenticated Privilege Escalation in SMS Alert Order Notifications <= 4.0.2 versions.

### CVE-2026-61737

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-30T15:16:53.363 |

ng-antd-admin is an Angular and NestJS administration system template. Prior to 22.0, a hardcoded default `JWT` secret permits token forgery when a deployment has not replaced the default secret, without a startup warning. An attacker can bypass authentication and authorization, impersonate any user including administrators, and access protected API endpoints, leading to account takeover, data leakage and unauthorized operations. Version 22.0 rejects the shipped secret in production but permits it with a warning in non-production environments.

### CVE-2026-110799

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-30T15:16:44.787 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. Prior to version 1.0.8.7, the password reset functionality is vulnerable to an Authentication Bypass due to insufficient validation of the user and token GET parameters. This issue has been patched in version 1.0.8.7.

### CVE-2026-62863

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-306;CWE-942` |
| Published | 2026-10-30T21:17:14.547 |

MoLing is a computer-use and browser-use based MCP server. Prior to 0.5.0, when MoLing runs in SSE mode using `-l`, its `/sse` and `/message` HTTP endpoints do not authenticate requests and the `mcp-go` dependency sets `Access-Control-Allow-Origin: *`. A malicious web page can open a cross-origin `EventSource` to `/sse`, including a loopback listener, and read the `endpoint` event to obtain `sessionId`. After a victim running SSE mode visits that page, the attacker can use the disclosed `sessionId` against `/message` to send unauthorized MCP tool calls. Depending on the configured tools, those calls can read or write local files, execute commands or perform other actions. Binding only to loopback does not prevent this browser-mediated attack. This issue is fixed in version 0.5.0.

### CVE-2026-116241

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-115` |
| Published | 2026-10-30T20:17:03.813 |

pgAdmin 4's Import/Export Data tool wraps a user's query export in a psql \copy (...) TO command and checks that the query's parentheses are balanced so that nothing can escape the wrapper. The check rejected a backslash inside a single-quoted string, but not inside a double-quoted identifier, where it treated the next double quote as closing the identifier. psql's \copy parser applies the connection's escape character to whichever quote opened a token, so with standard_conforming_strings off a backslash-escaped double quote does not close the identifier. pgAdmin's and psql's view of the quoting then diverged, a closing parenthesis hidden from the check ended the \copy (...) wrapper, and a following TO PROGRAM clause was executed by psql on the pgAdmin host, as the operating-system account running pgAdmin, before the server rejected the statement. An ordinary database role can turn standard_conforming_strings off for itself, and the Import/Export Data permission is granted to non-administrators by default.

This is a bypass of the fix for CVE-2026-17566. The fix rejects any backslash inside a double-quoted identifier, as was already done for single-quoted strings, since its meaning depends on a server setting that cannot be known reliably when the query is validated.

This issue affects pgAdmin 4: before 9.19.

### CVE-2026-93327

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-30T15:16:56.867 |

A Deserialization of Untrusted Data vulnerability in the SubWorkflow task in Google Cloud Application Integration versions prior to 2026-09-11 on Google Cloud Platform allows an authenticated attacker to execute arbitrary code using a maliciously crafted serialized object.


This vulnerability was patched on 11 September 2026, and no customer action is needed.

### CVE-2026-61729

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-798` |
| Published | 2026-10-30T15:16:53.083 |

SOCFortress CoPilot focuses on providing a single pane of glass for all your security operations needs. Prior to 0.1.76, `verify_graylog_header` in `backend/app/active_response/routes/graylog.py` and `verify_velociraptor_header` in `backend/app/incidents/routes/incident_alert.py` authenticate webhooks against `GRAYLOG_API_HEADER_VALUE` and `VELOCIRAPTOR_API_HEADER_VALUE` with the same publicly hardcoded fallback. The same default is shipped in `.env.example`. Deployments that leave either setting unset or unchanged permit an anonymous caller with the known header value to bypass the JWT authentication required by normal APIs. `POST /api/graylog/invoke` forwards attacker-selected `COMMAND`, `ACTION`, `VALUE` and `AGENT_ID` to the configured Wazuh manager without the command-enum validation of the authenticated invocation route, allowing active-response scripts to disrupt endpoints and manipulate defensive controls. `POST /api/incidents/alerts/create/threshold` and `POST /api/incidents/alerts/create/velo-sigma` accept forged alerts for arbitrary `customer_code` values and drive attacker-controlled OpenSearch queries. Active-response delivery requires a configured reachable Wazuh manager. Deployments with independently changed header secrets are not subject to this default-secret bypass. This issue is fixed in version 0.1.76.

### CVE-2026-117656

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290;CWE-349` |
| Published | 2026-10-31T00:16:51.340 |

Acceptance of Extraneous Untrusted Data With Trusted Data vulnerability in the Sign in with Apple strategy in pow-auth Assent allows an unauthenticated remote attacker to impersonate another user via the user parameter of the authorization callback.

Apple posts the user's name to the callback endpoint in a user form parameter that the browser submits and the client controls. Assent.Strategy.Apple.callback/2 in lib/assent/strategies/apple.ex decodes that parameter, and fetch_user/2 merges it over the claims of the verified ID token, so the unverified map wins. An attacker who completes a Sign in with Apple login with their own Apple ID and edits the user parameter can replace sub, email, and any other claim. Applications that look up, link, or authorize accounts by the returned subject or email then act on the attacker's values.

This issue affects assent: from 0.1.25 before 0.3.2.

### CVE-2026-78403

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-862` |
| Published | 2026-10-30T20:17:17.843 |

Stack-based buffer overflow and missing
authorization vulnerability in Thales Sentinel Keys Server on Windows allows
Overflow Buffers. Sentinel Keys Server does not check the length of the first
field in the HTTP request. An attacker may craft an HTTP request and send it to
Sentinel Keys Server. It may lead to remote code execution as NT
AUTHORITY\SYSTEM.





This issue affects Sentinel Keys Server:
versions lower than 1.3.8.0.

### CVE-2026-61850

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-30T20:17:11.380 |

Kargo manages and automates the promotion of software artifacts. From 0.6.0 until 1.8.14, 1.9.9, and 1.10.8, two authorization flaws in the `project-scoped RBAC API` let an authenticated user with delegated permission to manage a Project's `Roles` or `ServiceAccounts` confer permissions exceeding the user's own. A user authorized to edit `Roles` can create, replace, or add rules granting permissions not held by the user; a user authorized to edit a Role's ServiceAccount can bind an identity, including the user's own, to a more powerful Role. A Kargo Role comprises a `ServiceAccount, Role, and RoleBinding` in the Project namespace. Changes are written using the API server's broadly privileged credentials after only a coarse resource-kind edit check, rather than checking each permission being conferred. This permits escalation to Project-administrator access, disclosure of `Project Secrets` and credentials, and modification or deletion of Project resources. Stolen Git, container-registry, or Helm-registry credentials can extend confidentiality and integrity impacts to those external systems. Escalation remains limited to Projects where the attacker already has RBAC-management delegation and does not itself grant cluster-wide or cross-Project access. Default non-administrator roles do not permit these operations; exploitation requires an `administrator-created custom role` granting the relevant permissions and control of an account assigned that role. This issue is fixed in versions 1.8.14, 1.9.9, and 1.10.8.

### CVE-2026-39732

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-30T19:18:24.137 |

Unauthenticated SQL Injection in Transliterator <= 2.5.13 versions.

### CVE-2026-119706

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-30T16:17:51.673 |

InternLM LMDeploy 0.9.0 through 0.18.0 contains an unauthenticated remote code execution vulnerability that allows remote attackers to run OS commands by sending pickled data to the /update_weights endpoint. Attackers can submit a base64-encoded crafted pickle in serialized_named_tensors, which ForkingPickler.loads deserializes without validation, executing commands as the api_server process.

### CVE-2026-61730

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-200;CWE-306;CWE-522;CWE-552` |
| Published | 2026-10-30T15:16:53.223 |

SOCFortress CoPilot focuses on providing a single pane of glass for all your security operations needs. In affected deployments, the unauthenticated `/scoutsuite-report` `StaticFiles` mount in `backend/copilot.py` exposes the `scoutsuite-report` directory even though normal /api routes require JWT authentication. Generated HTML reports and `scoutsuite-results/scoutsuite_results_<name>.js` files disclose AWS, Azure and GCP IAM principals, resource inventories, misconfigurations and findings. Report names derive from caller-selected names with predictable defaults. During an admin- or analyst-initiated GCP scan, `backend/app/integrations/scoutsuite/routes/scoutsuite.py` saves the uploaded Google service-account JSON key into that same web-served directory. In `backend/app/integrations/scoutsuite/services/scoutsuite.py`, `generate_gcp_report_background` removes the key only after the scan finishes. Any anonymous client that can reach the host and request the file path can therefore retrieve the private key during the scan and use the service account's cloud permissions, as well as read retained cloud-security reports. Credential isolation is released in version 0.1.77; a release fully remediating the report-disclosure component has not been established.

### CVE-2026-119660

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1394` |
| Published | 2026-10-30T15:16:50.197 |

MuseBot before 2.0.0 contains an authentication bypass vulnerability that allows unauthenticated attackers to forge admin sessions by using the hard-coded default session_key 'muse_bot_session_key'. Attackers can sign a MuseBot-session cookie carrying a user_id to gain full administrative access, reading password hashes, chat records, and bot configuration, and stopping bots.

### CVE-2026-116238

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307;CWE-863` |
| Published | 2026-10-30T20:17:02.433 |

In server mode pgAdmin 4 locks an internal account after MAX_LOGIN_ATTEMPTS failed logins (3 by default). The limit could be bypassed, giving an unauthenticated attacker an unlimited number of password guesses against any internal account, including the administrator's, in the default configuration:

- Flask-Security registers its own views next to pgAdmin's. A login submitted to its /login view was checked and logged in without pgAdmin's failed login count or lock. Its /verify view checked a signed-in user's password without limit, its /change view changed a password without pgAdmin's change password permission or re-encrypting the user's saved server passwords, and its /reset views sent and applied password resets for accounts that are not internal or are locked.
- The internal account was looked up by its exact username, while the login form matches the email ignoring case, so a login with the username typed in another case was neither counted nor checked for the lock.
- With LDAP or webserver authentication also configured, a wrong internal password was never counted, and with Kerberos or webserver authentication configured a guess could be answered without being counted.

In addition, where accounts from different authentication sources share an email address, a password reset could be sent for, or applied to, an account from another source, and the About box showed the server configuration to a user whose email was that of an administrator's account.

The fix refuses submissions to Flask-Security's own views, counts every failed internal login however the username is typed and whatever other sources are configured, no longer lets a login that posts a password fall back to an authentication source that does not check it, and locks only internal authentication. Password resets and the About box act only on the user's own internal account. Desktop mode is not affected.

This issue affects pgAdmin 4: before 9.19.

### CVE-2026-119717

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-30T16:17:55.170 |

pybars4 through 0.9.13 contains a code injection vulnerability in pybars/_compiler.py that allows attackers to execute Python code via unescaped bracketed path segments in Handlebars templates. Attackers can supply a template with a crafted segment in a helper or block argument to break out of the generated resolve() string literal and execute code in the application process.

### CVE-2026-119716

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-30T16:17:55.013 |

pybars3 through 0.9.7 contains a code injection vulnerability in pybars/_compiler.py that allows template authors to execute Python code via unescaped bracketed path segments. Attackers can supply Handlebars templates with crafted segments in helper or block arguments to break out of string literals and execute Python in the application process.

### CVE-2026-103882

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-31T09:16:32.510 |

The Acadlix LMS – AI Quiz Maker, Online Exam & Course Plugin for WordPress plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the post_delete_assessment_file_by_id function in all versions up to, and including, 1.1.9. This makes it possible for authenticated attackers, with subscriber-level access and above, to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). The route's permission callback only verifies a generic wp_rest nonce that the plugin itself emits inside the public acadlixOptions JavaScript object on every frontend page, effectively reducing the authentication requirement to unauthenticated.

### CVE-2026-89270

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-31T07:16:37.707 |

The Popup Builder – Create highly converting, mobile friendly marketing popups. plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 4.4.5 This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to trash all published popups on the site with a single unauthenticated GET request. The attack is amplified by a second flaw in SGPopup::find(), which returns false for every normally published popup when the sg_popup_preview_id parameter is present, causing the trash branch to fire against every popup on the site simultaneously.

### CVE-2026-116557

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-31T07:16:35.857 |

The WP Booking System - Booking Calendar plugin for WordPress is vulnerable to unauthorized modification of data due to a missing capability check on the wpbs_action_ajax_calendar_remove_note() function in versions up to, and including, 2.1.0.5 This makes it possible for authenticated attackers, with Subscriber-level access and above, to delete arbitrary calendar notes belonging to any calendar.

### CVE-2026-62849

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-30T21:17:14.120 |

ThingLinks is an enterprise IoT platform. Prior to 1.4.0, an unauthenticated SQL injection vulnerability in the `TDengine TDS APIs` allows request-controlled JSON field values submitted to `/anyUser/tds/insertTableData` to reach unsafe SQL construction in the `TDS mapper`. A remote unauthenticated attacker can tamper with TDengine time-series data, including inserting unintended rows or overwriting existing readings. The affected surface is the TDS module's insert-table-data flow and TDengine mapper SQL generation. This issue is fixed in version 1.4.0.

### CVE-2026-117666

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-297` |
| Published | 2026-10-30T21:16:51.447 |

Improper Validation of Certificate with Host Mismatch vulnerability in deadtrickster ssl_verify_fun allows an adversary in the middle to impersonate a TLS peer via a certificate that carries a partial-label wildcard. try_match_wildcard/4 in src/ssl_verify_hostname.erl anchors only the text before and after the * of an identifier such as f*.example.net, so the wildcard also consumes dots and the certificate is accepted for f.evil.example.net. RFC 6125 confines a wildcard to the left-most label. The same matcher lets *.168.1.1 match the IP literal 192.168.1.1. Whole-label wildcards are matched correctly.

Erlang/OTP 20.0 and later check the hostname in ssl before a user verify_fun sees valid_peer, so a client that keeps server_name_indication set rejects the mismatch regardless. Exposed are clients that disable SNI, servers that verify client certificate hostnames with this library, and direct callers of verify_cert_hostname/2.

This issue affects ssl_verify_fun: from 1.0.1 before 1.1.8.

### CVE-2026-55598

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-30T20:17:10.063 |

PinePods is a complete, self-hosted podcast management system written in Rust. Prior to 0.9.0, an authenticated user can subscribe to an attacker-controlled RSS feed through `POST /api/data/add_podcast` in `rust-api/src/handlers/podcasts.rs`. `get_podcast_values` and `add_episodes` in `rust-api/src/database.rs` parse the feed with `feed-rs` and store the `<enclosure url>` verbatim in `Episodes.episodeurl` without destination host/IP validation. `POST /api/data/download_podcast` invokes `spawn_download_podcast_episode` and `download_episode_and_wait()` in `rust-api/src/services/tasks.rs`, which sends a `reqwest` GET to the stored URL and saves and records the response in `DownloadedEpisodes` for later retrieval. The `estimate_duration_from_audio_url_async()` path in `rust-api/src/database.rs` also sends an unvalidated HEAD during feed add/refresh. Default redirect following permits an initially external enclosure URL to redirect to an internal target. A low-privilege user can make server-side GET/HEAD requests to reachable loopback, private-network and cloud metadata services and read downloaded internal responses, enabling internal-service enumeration, confidential-data disclosure and possible metadata credential theft. Episode downloading requires server downloads to be enabled, which is the default; self-service signup is supported. This issue is fixed in version 0.9.0.

### CVE-2026-116852

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-30T19:18:15.020 |

Author Remote Code Execution (RCE) in Widget Options <= 4.2.5 versions.

### CVE-2026-119978

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-749` |
| Published | 2026-10-30T18:17:27.577 |

Flowise through 3.1.4 contains a sandbox escape vulnerability that allows authenticated users to execute OS commands by abusing allowlisted langchain and mammoth modules when ALLOW_BUILTIN_DEP=true. Attackers can submit JavaScript to /api/v1/node-custom-function that writes a file into the mammoth package via LocalFileStore and requires it, escaping vm2 as the Flowise process user.

### CVE-2026-118697

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-30T18:17:24.687 |

In JetBrains Toolbox App before 3.9.1 and 3.8.2; IntelliJ IDEA before 2026.3 and 2026.2.4, the jetbrainsd daemon trusted compromised intermediate certificates

### CVE-2026-112905

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-285` |
| Published | 2026-10-30T15:16:45.177 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. Prior to version 1.0.8.7, authenticated IDOR on admin/auth-token endpoint allows any administrator to read and overwrite another administrator's API tokens. This issue has been patched in version 1.0.8.7.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-116239

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-639` |
| Published | 2026-10-30T20:17:03.017 |

In server mode pgAdmin 4 keeps an account per authentication source, so the same username can exist as, for example, an internal account and an LDAP account. After LDAP or Kerberos authenticated a user, pgAdmin chose the account to log in by username alone, or took the account Flask-Security's login form had looked up, without checking that it came from the source that authenticated the user. The session therefore belonged to another account, with its role, its servers and its saved database passwords:

- An LDAP or Kerberos user whose username matched an internal account was logged in as that internal account, including the administrator account created when pgAdmin is first set up.
- With internal authentication listed before LDAP or Kerberos in AUTHENTICATION_SOURCES, the login form's internal validation looks up the account whose email was typed and keeps it even though its password does not match. A Kerberos user could type another Kerberos user's principal and be logged in as that user, and an LDAP user could do the same with an LDAP account whose email is their username.

Exploitation requires valid credentials for an LDAP directory or Kerberos realm that pgAdmin is configured to use.

The fix looks the account up by the authenticated username and the source that authenticated it, and no longer uses the account the login form found for any source but internal authentication. Internal authentication logs in that account only if it is an internal account. Desktop mode is not affected.

This issue affects pgAdmin 4: before 9.19.

### CVE-2026-61845

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-10-30T19:18:28.197 |

Crass is a Ruby CSS parser that's fully compliant with the CSS Syntax Level 3 specification. Prior to 1.0.7, Crass converts `CSS scientific notation` number values with unbounded exponentiation before clamping the result to `Float::MAX`. Applications that use Crass to parse attacker-controlled CSS strings can be forced to spend disproportionate CPU and memory parsing a tiny input, potentially resulting in a crash. This issue is fixed in version 1.0.7.

### CVE-2026-45144

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T15:16:51.783 |

Chamilo LMS is an open-source learning management system. From 2.0.0 until 2.0.1, `GET /user/{username}` is anonymously reachable and renders six user-editable profile fields (`firstname`, `lastname`, `competences`, `openarea`, `teach`, and `diplomas`) inside `{% autoescape false %}`, without server-side sanitization on the write path. A ROLE_STUDENT attacker can plant HTML in their own profile; self-registration, when enabled, lets an otherwise anonymous attacker obtain that role. The stored content executes in the browser of any visitor, including administrators, who follows the public profile link, potentially allowing account takeover through session, JWT, or `localStorage` exfiltration. This issue is fixed in version 2.0.1.

### CVE-2026-76010

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-31T10:16:38.547 |

The Photo Gallery, Sliders, Proofing and Themes – NextGEN Gallery plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 4.4.1 via the render_image function. This is due to unrestricted mass assignment of caller-supplied meta_data keys onto the image model combined with missing realpath containment in path construction and a bypassable signature check on the public image delivery route. This makes it possible for authenticated attackers, with custom-level access and above, to execute code on the server. Exploitation requires the authenticated attacker to own at least one NextGEN gallery — a condition that can be satisfied by any Subscriber who was ever granted the 'NextGEN Manage gallery' capability, and that access is retained indefinitely due to the stored gallery-author equality fallback in _can_manage_gallery() even after the capability is revoked.

### CVE-2026-116086

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-31T09:16:33.223 |

A flaw was found in konflux-ci. An attacker with permission to trigger automated workflow runs can cause an information disclosure by providing crafted issue titles to workflow scripts. The affected script incorporates user-provided titles directly into data queries without adequate sanitization, allowing the attacker to inject malicious filter commands. As a result, sensitive information such as API credentials, deployment keys, and internal notes returned from repository queries may be exposed in workflow logs.

### CVE-2026-120070

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-31T08:16:49.183 |

The User Frontend – Membership, User Registration, User Profile, User Directory & Content Restriction with Frontend Post Submission plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 4.3.13 via the `post_content` parameter of the `submit_post()` function. The vulnerability exists because the protected-shortcode blocklist guard inspects the `sanitize_textarea_field()` copy of the submitted `post_content`, while the copy actually persisted to the database is processed through `wp_kses()`, whose `wp_kses_no_null()` step strips C0 control bytes — allowing an attacker to inject a single `\x01` byte inside the `[wpuf-registration]` tag name to defeat the `strpos()` blocklist check while the clean, functional shortcode is stored verbatim; `strip_shortcodes()` does not neutralize the stored shortcode either, because the Frontend container that registers it via `add_shortcode()` is only instantiated when `is_admin()` is false, and `admin-ajax` requests have `is_admin() === true`. This makes it possible for authenticated attackers, with Subscriber-level access and above, to inject a `[wpuf-registration role="editor"]` shortcode into a published post, causing a live Editor-role registration form to be rendered publicly on the frontend that any visitor — or the attacker themselves — can submit to mint a WordPress Editor account with an immediately active privileged session when the default `autologin_after_registration` setting is enabled.

### CVE-2026-104012

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-31T08:16:47.893 |

The Rox Appointment Booking – Appointment Booking Scheduling Solution plugin for WordPress is vulnerable to Privilege Escalation via Mass Assignment in all versions up to, and including, 1.3.1 This is due to the public `/rox-appointment-booking/v1/public/booking` REST endpoint performing mass-assignment of the raw request body into a new customer row while `CustomerModel::$fillable` includes the internal `wp_user_id` column, allowing an unauthenticated attacker to persist an arbitrary WordPress user ID alongside an attacker-controlled email address with no authorization check. When an administrator subsequently opens the poisoned customer record and clicks Update Customer, `SaveCustomer::handleRequest()` passes the stored `wp_user_id` and attacker-supplied email to `wp_update_user()` — succeeding because `LinkedAccount::canChange()` unconditionally returns true when the acting user holds the `edit_users` capability — thereby overwriting the targeted administrator's email address and enabling full account takeover via a standard WordPress password-reset request. Successful exploitation requires an administrator to open and save the poisoned record, and the attacker must know or guess a valid administrator user ID (such as the default user ID 1).

### CVE-2026-63378

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-30T23:17:14.410 |

TAKO AI Agent for Okta is a local-first AI agent that helps Okta administrators query tenant data using natural language. Prior to 3.0.1-beta, any authenticated user with a valid `fctr_session` cookie can submit arbitrary Python source in the `script_code` field of `POST /api/react/execute-script`, without administrator privilege. In `src/api/routers/react_stream.py`, the source is stored with `skip_discovery=True`, bypassing AI-based content filtering, and is passed to `validate_generated_code` in `src/utils/security_config.py`. `BLOCKED_PATTERNS` recognizes direct `__import__` calls but misses the import name passed as a string, `getattr` is in `ALLOWED_BUILTINS`, and the AST checker handles `ast.Name` and `ast.Attribute` targets but fails to handle `ast.Call` targets. Dynamic `getattr` call chains through `__builtins__` therefore evade validation. The `_write_temp_script` helper writes the accepted code to disk, and `asyncio.create_subprocess_exec()` executes it as the application process user, which is root in the default container. Command output is returned as Server-Sent Events through `GET /api/react/stream-react-updates?process_id=<id>`. The resulting container compromise can disclose environment secrets including Okta API tokens and the JWT key, expose the SQLite database, and permit backend-service pivoting and persistence. This issue is fixed in version 3.0.1-beta.

### CVE-2026-63339

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-269` |
| Published | 2026-10-30T23:17:13.537 |

IXP Manager is a full-stack web application for managing Internet Exchange Points. Prior to version 7.3.0, an authenticated, non-administrative user can elevate their privileges to administrator status. Restricting administrative functions reduces exposure but is not a complete fix. This issue is fixed in version 7.3.0.

### CVE-2026-16760

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502;CWE-693` |
| Published | 2026-10-30T22:16:54.193 |

In Trail of Bits fickling through 0.1.12, the _process_import() method in fickle.py adds an imported name to the likely_safe_imports set whenever the source module is present in sys.stdlib_module_names and the name is absent from the UNSAFE_IMPORTS denylist, without inspecting what the name resolves to or how it behaves. The OvertlyBadEvals analysis pass in analysis.py then unconditionally skips any call whose function name appears in likely_safe_imports, including calls that would otherwise be flagged as overtly dangerous. As a result, any callable reachable through a non-blocked standard library module inherits module-level trust regardless of its own behavior, and check_safety() returns LIKELY_SAFE with zero findings for pickle payloads that reach code execution or file write through such callables. Demonstrated primitives: dataclasses._create_fn, which passes an attacker-controlled function body to exec() and yields arbitrary code execution on Python 3.7 through 3.12 (the internal _create_fn function was removed in Python 3.13); mailcap.findmatch, which internally calls os.system() on a test command taken from an attacker-controlled caps dictionary, yielding arbitrary code execution on Python versions through 3.12 (the mailcap module was removed in Python 3.13); and readline.add_history() followed by readline.write_history_file(), which writes attacker-controlled content to an arbitrary filesystem path (POSIX platforms, where the readline module is available). fickling.load() chains check_safety() into pickle.loads() as an explicit security gate, so a LIKELY_SAFE verdict causes the payload to be deserialized and executed with the privileges of the victim process. The root cause is the inference of callable safety from module origin; it is independent of, and separately fixable from, the dotted __qualname__ resolution weakness tracked as CVE-2026-118938, which this advisory does not address. As of 2026-10-30 the three demonstrated modules were added to UNSAFE_IMPORTS on the vendor master branch (commit d011709) pending release; released versions through 0.1.12 remain affected, and the module-origin trust root cause persists, as demonstrated by the related CVE-2026-118938 remaining exploitable on that same build.

### CVE-2026-118938

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502;CWE-706` |
| Published | 2026-10-30T22:16:54.020 |

In Trail of Bits fickling through 0.1.12, a pickle STACK_GLOBAL operand carrying a dotted __qualname__ (for example "Values.read_file") is resolved by pickle's find_class through _getattribute to an arbitrary attribute path rather than to a module-level function. Fickling records only the leading component of the name in its import tracking and renders the operation as a plain import (for instance, 'python -m fickling' displays it as 'from optparse import Values.read_file'), so the trailing attribute reference is never analyzed as a call. The OvertlyBadEvals analysis pass does not flag it, and check_safety() returns LIKELY_SAFE with zero findings. This allows an attacker to reach a class method that performs code execution: optparse.Values.read_file executes exec(open(filename).read(), vars), achieving arbitrary code execution when the crafted pickle is loaded through fickling.load(), which chains check_safety() into pickle.loads() as an explicit security gate. optparse is present in all current CPython 3.x releases (deprecated as of Python 3.13, not removed). This weakness is in the resolution and analysis of dotted attribute-path names, and is distinct from and independently fixable from the module-origin trust weakness tracked as CVE-2026-16760: resolving or flagging dotted attribute-path imports closes this vector while leaving the module-level trust behavior unchanged. This bypass was verified to remain present on the vendor master branch at commit d011709 as of 2026-10-30, after the vendor's October blocklist additions and a new heuristic that flags private stdlib attributes; because the public class method Values.read_file is neither blocklisted nor flagged as a private attribute, it is not addressed by those remediations.

### CVE-2026-119332

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-30T20:17:07.600 |

Ladybird is a truly independent web browser. Prior to 209579c96473c75bd5eba9701fcadb841a045964, FinalizationRegistry::cleanup() in Libraries/LibJS/Runtime/FinalizationRegistry.cpp removed a dead record from m_records, retained an iterator to the next FinalizationRecord, and then invoked attacker-controlled JavaScript through the cleanup callback. If that callback called unregister() for the next record, remove_by_token() freed the node referenced by the retained iterator, and the next cleanup iteration read its target and held_value fields after free. This reliably crashes instrumented WebContent builds and creates a memory-corruption primitive in production builds. This vulnerability is fixed by commit 209579c96473c75bd5eba9701fcadb841a045964.

### CVE-2026-78527

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-30T19:19:12.177 |

Contributor PHP Object Injection in GS Testimonial Slider <= 3.3.10 versions.

### CVE-2026-73186

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-30T19:19:10.123 |

Subscriber PHP Object Injection in Enable Media Replace <= 4.2.2 versions.

### CVE-2026-118090

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-30T19:18:17.527 |

Subscriber PHP Object Injection in MasterStudy LMS <= 3.7.55 versions.

### CVE-2026-118086

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-30T19:18:17.257 |

Subscriber Privilege Escalation in WP BASE Booking <= 6.5.2 versions.

### CVE-2026-105894

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-30T18:17:16.483 |

The Ak Framework plugin for WordPress, included in the Newsy - Viral News & Magazine WordPress Theme, is vulnerable to Privilege Escalation in all versions up to, and including, 2.9.8. This is due to missing capability checks in the ajax_refresh_nonce and ak_admin_ajax handlers before passing attacker-controlled option names and values to update_option(). This makes it possible for unauthenticated attackers to update arbitrary WordPress options including users_can_register and default_role to escalate privileges to administrator by enabling user registration with administrator as the default role.

### CVE-2026-65566

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-30T17:17:27.793 |

Cross-Site Request Forgery (CSRF) vulnerability in Meow Apps AI Engine ai-engine allows Cross Site Request Forgery.This issue affects AI Engine: from n/a through 3.8.8.

### CVE-2026-110176

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-31T01:17:05.153 |

The File Force Download module for Drupal 7 implements hook_file_download() to add a Content-Disposition header when a file URL carries the download query parameter. In Drupal 7, returning a non-empty header array from that hook is itself a grant of access to the file.



In versions 7.1.0 through 7.1.2, the module only delegated to other modules' hook_file_download() implementations when the file was in the private scheme. For every other scheme it returned its headers without any check. An unauthenticated visitor who appended download=1 to the URL of a file in the temporary:// scheme, or in a stream wrapper supplied by another module, could retrieve the file, overriding the access checks that would otherwise have applied. Files in the public and private schemes are not affected.

### CVE-2026-63396

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-30T23:17:14.710 |

Coop is an open source review and moderation tool from ROOST. Prior to 1.0.0, an unauthenticated actor can query `Query.allOrgs` through `/api/v1/graphql` on a publicly accessible deployment and obtain data for all organizations, including organization IDs, names, email addresses, website URLs and on-call alert email addresses. The `usersWhoCanReviewEveryQueue` field also exposes reviewing users' IDs, email addresses, first and last names, roles, permissions and creation dates. Running the service on an authenticated private network prevents outside actors from directly querying the GraphQL API. This issue is fixed in version 1.0.0.

### CVE-2026-63393

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-30T23:17:14.557 |

OpenSearch SQL supports querying OpenSearch data using SQL and Piped Processing Language. In the 2.x line from 2.8.0.0 until 2.19.6.0, and the 3.x line prior to 3.7.0.0, a remote authenticated user with basic read/search permissions can provide a crafted `cursor` parameter to the `plugins/sql` endpoint and trigger unsafe deserialization of untrusted data, resulting in arbitrary code execution on the server. This issue is fixed in repository releases 2.19.6.0 and 3.7.0.0.

### CVE-2026-62990

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-269` |
| Published | 2026-10-30T21:17:16.030 |

Shopper is a Headless e-commerce Admin Panel. In versions from 2.0.0 prior to 2.10.1 and in the 3.0.0 prereleases beta.1 and beta.2, authenticated back-office staff with a content-upload permission can store executable media on the administrator's own origin. In the 2.x implementation, relevant upload permissions include `edit_products` or `add_brands`, and `packages/admin/config/media.php` allows `image/svg+xml` in every media collection, including image fields whose image/* validation also accepts SVG. The product files collection in `packages/admin/src/Livewire/Components/Products/Form/Files.php` has no MIME restriction and accepts `text/html` as well. Media is served inline from the `public` disk under `/storage/` with its own content type, without `Content-Disposition: attachment` or a `Content-Security-Policy`. When an administrator opens an uploaded HTML or SVG file, stored script executes in that administrator's session. In 2.x, the script can invoke `packages/admin/src/Livewire/SlideOvers/CreateTeamMember.php`, whose `store()` checks `access_setting` held by the viewing administrator but trusts client-supplied `role_id`, to create a new attacker-controlled administrator with a chosen password. This account persists after the uploaded file is deleted and gives access to customer data, orders, settings, and user/role management; the same script can exfiltrate data or grant permissions to the attacker's account. Direct account creation by the low-privileged uploader is blocked, so exploitation requires the administrator to open the file. The 3.x prerelease line already excludes SVG but still allows executable product files. This issue is fixed in versions 2.10.1 and 3.0.0-beta.3.

### CVE-2026-62968

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-30T21:17:15.433 |

Dream Displays provides in-game screens for streaming videos in Minecraft. From 1.5.0 until 1.8.2, user-controlled input can influence arguments passed to `yt-dlp` under specific conditions. Unintended command-line options may be interpreted by `yt-dlp`, potentially altering its behavior. This issue is fixed in version 1.8.2.

### CVE-2026-62334

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-10-30T20:17:12.493 |

OpenVM is a performant and modular zkVM framework built for customization and extensibility. Before 1.7.0 in the 1.x line and in affected 2.0 and 2.1 prereleases, `OpenVmHalo2Verifier.verify` constructs raw proof calldata from user-controlled `proofData`, performs a `staticcall` to `address(this)`, and treats a successful call as proof acceptance. If the first four proof bytes match another external selector exposed by the wrapper, dispatch can invoke a successful non-verifier function instead of the generated Halo2 fallback verifier. Applications using the generated Solidity wrapper can consequently accept arbitrary app commitments and public values without checking the proof suffix, accumulator, app commitments or public values. This issue is fixed in versions 1.7.0, 2.0.0-rc.3 and 2.1.0-preview.

### CVE-2026-62333

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-30T20:17:12.330 |

OpenVM is a performant and modular zkVM framework built for customization and extensibility. Before 1.7.0 in the 1.x line and in affected 2.0 and 2.1 prereleases, `MemoryMerkleAir` does not forbid Merkle expansion rows at `parent_height` = 0 or below while `expand_direction` != 0. A malicious prover can fabricate a subtree below a memory leaf and swap digests inside that subtree to change the committed memory root without a corresponding memory operation. The fraudulent rows still balance against the Merkle and compression buses and require no memory-bus operation for the changed leaf. Because the memory Merkle root binds VM memory state across continuation segment boundaries, this affects the soundness of OpenVM proofs using persistent memory. This issue is fixed in versions 1.7.0, 2.0.0-rc.3 and 2.1.0-preview.

### CVE-2026-62302

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-30T20:17:12.063 |

MyTube is a self-hosted downloader and player for several video websites. Prior to version 1.10.3, `server.ts` calls `registerStaticRoutes` and `registerCloudRoutes` before `registerApiRoutes`, where `authMiddleware` and `roleBasedAuthMiddleware` are mounted. Because Express processes middleware in registration order, `staticRoutes.ts` and `cloudRoutes.ts` remain outside the authentication stack even when `loginEnabled=true`. Unauthenticated clients can access local videos through `/videos/*`, thumbnails through `/images/*` and `/images-small/*`, avatars through `/avatars/*`, subtitles through `/subtitles/*`, cloud thumbnail caches through `/api/cloud/thumbnail-cache/*`, and cloud signed URLs or redirects through `/cloud/videos/:filename` and `/cloud/images/:filename`. The frontend login wall does not protect direct media requests. Cloud routes return 404 when cloud storage is unconfigured, but that is not an authentication rejection; protected API routes correctly return 401. Combined with hidden-video path leaks, the flaw permits unauthenticated downloads of hidden media. Default loginEnabled=false single-user deployments have no authentication boundary to bypass. This issue is fixed in version 1.10.3.

### CVE-2026-115830

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-30T20:17:02.240 |

In Secret Server versions earlier than 12.3.1, a user under certain conditions could submit an unsigned JWT and receive cloudadmin permissions in response.

### CVE-2026-115829

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-30T20:17:02.107 |

In Secret Server versions earlier than 12.3.1, a user could bypass the initial login step and authenticate by successfully negotiating the second factor login step only.

### CVE-2026-62160

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-10-30T19:18:32.473 |

Daptin is a GraphQL/JSON-API headless CMS. Prior to 0.12.26, the global `LanguageMiddleware` in `server/language.go` passes the raw `Accept-Language` header from `LanguageMiddlewareFunc` through `GetLanguagePreference` to `golang.org/x/text/language.ParseAcceptLanguage` without a size or shape filter. The guard for CVE-2022-32149 counts hyphens but not underscores, even though the internal parser normalizes underscores to hyphens. Long lists of underscore-separated language subtags longer than eight characters bypass the guard. These subtags fail the `len <= 8` length check in `golang.org/x/text/internal/language/parse.go`, causing repeated `gobble` operations to move the entire remaining buffer through `runtime.memmove`. With many invalid subtags, this repeated buffer movement takes quadratic work. Unauthenticated requests to the public landing page or `/api` can consume disproportionate CPU, with a 256 KiB header already causing seconds of processing and larger input permitted by the default 1 MiB header ceiling. `resource.CheckErr` also logs the entire invalid header, amplifying cost, while normal successful HTTP responses can conceal the denial-of-service traffic. Repeated requests can saturate server CPU. This issue is fixed in version 0.12.26.

### CVE-2026-119979

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-30T18:17:27.760 |

LM Studio before 0.4.22+1 contains a path traversal vulnerability in the model downloader's resolveDownloadRequest that allows attackers to write files outside the models directory using backslash-separated traversal filenames. Attackers can trick users into downloading a crafted model repository that plants a plugin manifest.json, install-state.json and mcp-bridge-config.json, running an attacker-supplied Python payload on every launch.

### CVE-2026-119762

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-30T18:17:26.957 |

Axigen Mail Server before 10.5.69, 10.6.x before 10.6.40, and 10.7.x before 10.7.2 contains an unauthenticated denial of service vulnerability caused by unbounded nesting depth when parsing SOAP/XML and JSON request bodies before authentication. Attackers can send a single deeply nested request to WebMail, WebAdmin, or WebMail Proxy listeners to exhaust the stack and crash SMTP, IMAP, POP3, and web services repeatedly.

### CVE-2026-119760

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-30T18:17:26.650 |

sniproxy through 0.7.0 contains a NULL pointer dereference vulnerability in resolv_cancel() that allows remote unauthenticated attackers to crash the daemon by sending overlong hostnames. Attackers can send a 254 or 255 character TLS SNI name or HTTP Host header matching a wildcard backend, then close the connection to terminate the proxy.

### CVE-2025-8574

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-30T18:17:13.960 |

The Database Cleaner plugin for WordPress is vulnerable to arbitrary table deletion in all versions up to, and including, 1.4.7. This is due to a lack of restriction on database tables that can be deleted. This makes it possible for authenticated attackers, with Administrator-level access and above, to delete core WordPress tables.

### CVE-2026-119116

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415;CWE-416` |
| Published | 2026-10-30T17:17:16.343 |

A use-after-free and double-free issue in the SetClient command handler of the kmstool-enclave sample application of AWS aws-nitro-enclaves-sdk-c before 0.4.6 may allow an application that runs on the parent EC2 instance to corrupt heap memory inside a Nitro Enclave which may lead to arbitrary code execution within the enclave.



To remediate this issue, users should rebuild any enclave image that includes kmstool-enclave, or code derived from it, against aws-nitro-enclaves-sdk-c 0.4.6.

### CVE-2026-119713

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-30T16:17:54.567 |

Paperclip 2026.403.0 before 2026.416.0 contains a remote code execution vulnerability that allows agent API key holders to set cleanupCommand and teardownCommand via PATCH /api/execution-workspaces/:id. When the workspace is archived, cleanupExecutionWorkspaceArtifacts runs these commands through a shell as the Paperclip server process, executing attacker-chosen OS commands on the server host.

### CVE-2026-119662

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-30T15:16:50.540 |

Songloft 2.9.0 before 2.13.6 contains a hardcoded credentials vulnerability that allows adjacent network attackers to authenticate as administrator using the fixed admin/admin pair. Attackers on the same network can log in via the /api/v1/auth/login endpoint to modify library and configuration settings and install JavaScript plugins running in QuickJS.

### CVE-2026-119656

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-30T15:16:49.477 |

CoreShop by CoreUnion through 1.5.5 contains an unauthenticated sql injection vulnerability in the api/Agent/GetGoodsPageList endpoint via the order parameter appended to an ORDER BY clause. Anonymous attackers can inject subqueries that bypass SqlSugar's field check to extract member accounts and orders through boolean-based or time-based blind techniques.

### CVE-2026-119655

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-30T15:16:49.300 |

CoreShop through 1.5.5 contains an unauthenticated sql injection vulnerability in the api/Good/GetGoodsPageList endpoint via the unvalidated order parameter appended to ORDER BY. Attackers can inject subqueries that bypass SqlSugar's field check and use boolean-based or time-based blind techniques to extract member accounts and orders.

### CVE-2026-119654

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-30T15:16:49.120 |

DataCap through 2025.1.1 contains a missing authorization vulnerability that allows any authenticated user to escalate privileges by calling administrative role and menu management APIs. Attackers, including self-registered accounts, can send PUT requests to /api/v1/user/allocationRole to assign themselves the administrator role and gain full control of the instance.

### CVE-2010-20125

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-30T15:16:43.023 |

DedeCMS before 5.7 contains a file inclusion vulnerability in plus/carbuyaction.php that allows remote unauthenticated attackers to control the include path by manipulating the uninitialized code parameter passed to require_once. Attackers can supply path traversal sequences ../../ to include arbitrary local files outside the intended payment directory, potentially achieving local file disclosure. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-18.

### CVE-2026-114217

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-312` |
| Published | 2026-10-31T09:16:33.077 |

A flaw was found in konflux-ci. Continuous Integration (CI) automation scripts store sensitive GitHub access tokens in plaintext on the runner without cleaning them up after execution. A local attacker with access to the CI environment can read these stored credentials to gain unauthorized repository access, potentially allowing them to modify source code or release artifacts.

### CVE-2026-63346

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-116` |
| Published | 2026-10-30T23:17:14.130 |

Refitter is a tool for generating a C# REST API client using the Refit library. Prior to 2.1.2, the header parameter name in `parameters[].name` with `in: header` is emitted verbatim into a Refit `[Header("<name>")]` attribute string without escaping quotation marks. An attacker-influenced OpenAPI description can pass default validation without `--skip-validation` and break out from the parameter-list position by closing the parameter and method syntax, attribute, interface, and namespace. The generated file can remain valid C# while containing a top-level file class with a `[ModuleInitializer]` method, which executes attacker code when the compiled assembly is loaded at application startup, even if the client is never called. Query `AliasAs` and enum/default value sinks are escaped; this flaw is in header-name attribute-string emission. The behavior was verified with Refitter 2.0.0 and .NET 8. This issue is fixed in version 2.1.2.

### CVE-2026-63345

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-1116` |
| Published | 2026-10-30T23:17:13.987 |

Refitter is a tool for generating a C# REST API client using the Refit library. Prior to 2.1.2, OpenAPI `paths`-object keys are emitted verbatim into Refit route attributes such as `[Get("<path>")]` without escaping quotation marks or restricting characters. An attacker-influenced single-line, slash-prefixed path survives default validation without `--skip-validation` and can close the attribute string, interface, and namespace while introducing a top-level file class and reopening the generated structure to keep valid C#. A `[ModuleInitializer]` method executes attacker code when an application compiles and loads the generated assembly at startup, even without calling the generated client. The enum and default value sinks are escaped and are not the vulnerable path-emission sink. The behavior was verified on Refitter 2.0.0 with .NET 8. This issue is fixed in version 2.1.2.

### CVE-2026-63344

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-116` |
| Published | 2026-10-30T23:17:13.840 |

Refitter is a tool for generating a C# REST API client using the Refit library. Prior to 2.1.2, content-type keys in the content maps of `requestBody/responses` are emitted verbatim into a Refit `[Headers("Accept: <ct>", "Content-Type: <ct>")]` attribute string without escaping quotation marks. A crafted content-type key in an attacker-influenced OpenAPI description survives default validation without `--skip-validation`, breaks out of the attribute string and enclosing interface and namespace, and can introduce a top-level file class while leaving valid generated C#. A `[ModuleInitializer]` method in that class executes attacker code when the generated assembly is loaded at application startup, without requiring a call to the client. The behavior was verified with Refitter 2.0.0 and .NET 8. This issue is fixed in version 2.1.2.

### CVE-2026-40573

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-10-30T21:16:53.670 |

NovumOS is a custom 32-bit operating system written in Zig and x86 Assembly. Prior to version 0.25-beta.1, the `Nova` interpreter runs in Ring 0 with unrestricted kernel-memory access. Loading a malicious `.nv` script through the shell permits a local user to execute code with kernel privileges without security checks. The advisory identifies VM initialization in `zig/nova/vm.zig` as the affected component; script execution is not isolated in a restricted Ring 3 privilege domain. This issue is fixed in version 0.25-beta.1.

### CVE-2026-62284

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-918` |
| Published | 2026-10-30T20:17:11.727 |

OSAC operator is a Kubernetes operator. In the affected revision identified as 8220502, the `console-proxy` `RemoteConfigResolver` parses Kubernetes Secret kubeconfig data with `clientcmd.RESTConfigFromKubeConfig` without sanitizing the resulting `rest.Config`. An attacker who can create or modify a Secret labeled `osac.openshift.io/remote-cluster-kubeconfig`: "true" in a namespace where the proxy's RoleBinding grants Secret read access can supply `users[].user.exec`. When `rest.TransportFor` builds the HTTP transport for an upstream WebSocket connection, client-go invokes that exec credential plugin, spawning an arbitrary process as the osac-`console-proxy` service account inside the pod. Attacker-controlled `clusters[].server` also enables server-side request forgery from the proxy pod. Remote and auto VM cluster modes are affected, with auto the default; exclusively `local` mode does not read kubeconfig Secrets and is unaffected. The credential-plugin execution path is patched in commit 7e4222b; that patch does not address the described server-address SSRF path.

### CVE-2026-119722

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-30T16:17:55.907 |

Blender before 4.5.15 and 5.x before 5.2.3 contains a heap out-of-bounds access vulnerability in read_struct() that skips size validation when a .blend file's SDNA struct layout compares equal. Attackers can supply a crafted .blend file with short blocks so field reads, writes, and pointer dereferences overrun heap memory, causing crashes or code execution.

### CVE-2026-119719

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-30T16:17:55.473 |

Blender before 4.5.15 and 5.x before 5.2.3 contains a heap buffer overflow vulnerability in the blend file thumbnail extractor caused by 32-bit integer overflow in thumb_data_vertical_flip(). Attackers can craft a .blend file with malicious TEST block dimensions that trigger an out-of-bounds write when blender-thumbnailer or the Windows shell extension previews it, causing crashes or code execution.

### CVE-2026-119718

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-30T16:17:55.310 |

Blender before 4.5.15 and 5.x before 5.2.3 contains a heap buffer overflow vulnerability caused by integer overflow in ptcache_data_alloc() when reading point cache files. Attackers can supply a crafted point cache file with a large totpoint value alongside a .blend file to crash Blender or execute code as the user.

### CVE-2026-104067

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-30T16:17:36.500 |

Scribus before 1.6.7 contains an out-of-bounds memory access vulnerability in the importsvm plugin that fails to verify bitmap and transparency mask dimensions match. Attackers can supply a crafted SVM file with mismatched mask dimensions to trigger heap reads and writes, causing crashes or code execution as the user.

### CVE-2026-104066

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-30T16:17:36.340 |

Scribus before 1.6.7 contains a heap buffer overflow vulnerability in the Mac PICT image loader and import plugin when unpacking 4-bit indexed pixel data. Attackers can supply a crafted PICT file with inconsistent width and row data that, when placed or imported, writes out of bounds, causing crashes or code execution.

### CVE-2026-104065

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-30T16:17:36.180 |

Scribus before 1.6.7 contains an out-of-bounds write vulnerability in the importdrw Micrografx Draw plugin that uses an unvalidated y offset to select image scanlines. Attackers can craft a DRW file that, when imported by a user, writes decoded bitmap data outside the heap image buffer, causing crashes or code execution.

### CVE-2026-104064

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-30T16:17:36.027 |

Scribus before 1.6.7 contains an integer overflow vulnerability in the scimgdataloader_tiff TIFF loader that allows attackers to trigger a heap overflow via crafted tile dimensions. Attackers can supply a tiled TIFF with large tile width, height and sample values for a user to import, corrupting heap memory to crash Scribus or execute code.

### CVE-2026-104062

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-30T16:17:35.677 |

Scribus before 1.6.7 contains a heap buffer overflow vulnerability in the PICT image loader and import plugin that allows attackers to corrupt heap memory by supplying an unchecked bytesPerLine value. Attackers can craft a PICT file whose bytesPerLine exceeds the QImage scanline size, so placing or importing it crashes Scribus and may execute code as the user.

### CVE-2026-104061

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-30T16:17:35.250 |

Scribus before 1.6.7 contains a heap out-of-bounds write vulnerability in the scimgdataloader_psd loader that uses unchecked PSD file values as lookup array indexes. Attackers can convince users to place or import a crafted PSD file to corrupt heap memory, causing crashes and potentially code execution as the user.

### CVE-2026-61708

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-284;CWE-639;CWE-862` |
| Published | 2026-10-30T15:16:52.793 |

SOCFortress CoPilot focuses on providing a single pane of glass for all your security operations needs. Prior to 0.1.76, `POST /api/agent_data_store/upload` in `backend/app/data_store/data_store_routes.py` permits `customer_user` callers to choose `bucket_name` and `object_name` without an allowlist, tenant prefix, ownership check or content restriction. The only file check requires a nonempty filename. The operations in `backend/app/data_store/data_store_operations.py` create missing buckets and upsert objects, allowing existing objects belonging to any tenant to be overwritten. Targets include `sysmon-configs/<customer_code>/sysmon_config.xml` distributed to managed Windows endpoints, `copilot-case-report-templates/<name>` rendered server-side, and case evidence or forensic artifacts under `copilot-cases/<case_id>/<file>` and `velociraptor-artifacts/<agent_id>/<flow_id>/<file>`. A lowest-privilege user can tamper with cross-tenant evidence, blind endpoint telemetry, poison report templates for later code execution, plant data or exhaust storage. Sibling list, download and delete routes remain restricted to admin/analyst; the exposed operation is the upload write path. This issue is fixed in version 0.1.76.

### CVE-2026-119680

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:L/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T15:16:51.187 |

A stored cross-site scripting (XSS) vulnerability exists in the chart feature of SharePoint Manager Plus (SPMP) due to improper sanitization and HTML encoding of user-controlled data. An attacker can inject malicious HTML or JavaScript into attributes used to generate charts, including users' full names, site names, or group names. The injected content is stored and subsequently executed in the context of other users' browsers when the affected charts are rendered. This vulnerability was fixed in client application build 4508.

### CVE-2026-116964

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-31T09:16:33.357 |

A flaw was found in konflux-ci. An attacker with repository write access can achieve arbitrary code execution within the Continuous Integration and Continuous Delivery (CI/CD) workflow environment. By injecting shell commands into environment export scripts, the attacker causes manifest synchronization scripts to dynamically evaluate unvalidated script output. Successful exploitation allows the attacker to compromise CI/CD pipelines, steal sensitive authentication tokens and deployment credentials, and gain unauthorized access to production systems.

### CVE-2026-62979

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-209` |
| Published | 2026-10-30T21:17:15.593 |

jack lets users share media libraries through their Radarr/Sonarr stack, peer-to-peer. Prior to 0.1.0, `middleware/handle-error.ts` serializes raw `FetchError` objects into HTTP responses. `lib/servers/base.ts` attaches outbound request headers on upstream non-success responses and schema-validation failures; the public `extras` field in `lib/errors/FetchError.ts` remains enumerable and is emitted by JSON serialization. These headers include the internal Radarr/Sonarr `X-Api-Key` and custom connector headers such as `CF-Access-Client-Secret`. `lib/redact.ts` redacts logs and spans but not this response path. Any client with the shared peer API key, plus Cloudflare Access credentials if required by the deployment, can force an error without a race or user interaction. `GET /peer/items/:id` and `GET /servers/health` can expose the internal media-server key, while `GET /torznab/download/:id` can expose another peer's key and Cloudflare Access secrets. The /peer/search and /items routes catch these errors and are not affected. Disclosed internal keys grant full administrative control of the corresponding Radarr/Sonarr instance, crossing the intended boundary between friends' shared peer access and private backend credentials. This issue is fixed in version 0.1.0.

### CVE-2026-63338

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-863` |
| Published | 2026-10-30T23:17:13.377 |

IXP Manager is a full-stack web application for managing Internet Exchange Points. Prior to version 7.3.0, an authenticated user can view and edit a resource belonging to another user without authorization. The API-key edit/update path in `ApiKeyController` selects records by identifier without checking that `user_id` matches the caller, allowing access to another user's API-key record. This issue is fixed in version 7.3.0.

### CVE-2026-115642

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-30T17:17:15.053 |

In OpenStack keystonemiddleware before 13.0.2, by supplying a custom X-Service-Token header in a request, anyone in possession of an access-restricted application credential may bypass those restrictions resulting in elevation of privileges.

### CVE-2026-62847

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-377;CWE-427` |
| Published | 2026-10-30T21:17:13.807 |

Metalama is a Roslyn-based open-source patterns and architecture toolkit for C#. Prior to 2025.1.18, 2026.0.25 and 2026.1.19, Metalama.Framework and Metalama.Tool load and execute compile-time assemblies, auxiliary executable tools and embedded helper assemblies from predictable temporary directories. On `Linux` and `macOS`, the default `Path.GetTempPath()` location is world-writable, and existing artifacts are trusted based on sentinel or `.completed` marker files rather than integrity verification. A local unprivileged user on a shared machine or CI/build agent can pre-create the deterministic directory structure and plant a malicious DLL with the matching sentinel. When a higher-privileged developer or build account subsequently builds, Metalama skips regeneration and executes the planted artifact in the compiler, IDE or MSBuild process as the building user. This permits cross-user privilege escalation, reading source and secrets, supply-chain tampering with build output, or disrupting builds. Default Windows per-user temporary directories are protected by ACLs and are not affected. Deployer-selected insecure cache locations are outside the vulnerability's scope. This issue is fixed in versions 2025.1.18, 2026.0.25 and 2026.1.19.

### CVE-2026-58412

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-30T21:17:12.910 |

Filecoin Pin is an IPFS Pinning Service API implementation that pins to Filecoin's PDP service. Prior to 1.1.0, the upload GitHub Action's fork detection in `upload-action/src/build.js` checks only `event.pull_request`. In the documented two-workflow pattern, an untrusted fork pull-request workflow produces an artifact and a privileged `workflow_run` workflow downloads and uploads it. Because `workflow_run` has no `event.pull_request`, `isForkPR` becomes false and `uploadStatus` becomes `pending-upload`. The action later resolves `workflow_run.pull_requests` without repeating the fork check before initializing the wallet with `walletPrivateKey` and uploading the artifact. An external contributor can therefore cause attacker-controlled artifacts to be stored using the repository owner's Filecoin wallet, incurring unauthorized storage expenditure, dataset pollution and consumption of configured wallet funds. Disclosure of the wallet private key is not required. The 0.x action line is not receiving a backport and must be migrated to a fixed 1.x release. This issue is fixed in version 1.1.0.

### CVE-2026-62331

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-30T19:18:33.450 |

praktor is a multi-agent Claude Code orchestrator with Telegram input and output, Docker isolation, and a Mission Control UI. Prior to 0.9.1, both Telegram upload sites in `internal/telegram/bot.go` concatenate the attacker-controlled document filename into a destination path without sanitization, and `path.Join` collapses parent-directory traversal. A remote Telegram user who can message the bot can therefore write outside `uploads/` within the persistent agent workspace mounted at `/workspace/agent`. Because `allow_from: []` permits all senders by default, no prior authentication or privilege is required in that configuration. The attacker can plant or overwrite `CLAUDE.md`, instruction, skill, hook, or configuration files that the Claude agent reads and operates on across later runs, turning a document upload into stored instruction injection. The demonstrated arbitrary-write scope is the persistent agent workspace volume, not an unrestricted host-filesystem write. This issue is fixed in version 0.9.1.

### CVE-2026-62162

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-30T19:18:32.630 |

Hydra is a layer-two scalability solution for Cardano. Prior to 2.1.0, the `Claim` branch in `hydra-plutus/validators/deposit.ak` checks only that `datum.head_id` matches the attacker-controlled `redeemer.currencySymbol` and that the transaction is valid before the deposit deadline. It neither requires spending the Head state-token UTxO in the same transaction nor constrains outputs. After a deposit made through `POST /commit` is confirmed, any third party able to build a Cardano transaction can observe and consume the pending deposit UTxO before its deadline and redirect the assets to an arbitrary address. A standalone deposit spend invokes no Head validator, bypassing its safety checks; historical head-ID binding and the Aiken rewrite retained this missing invariant. The default deadline is three times depositPeriod, so the described attack applies to pending deposits before that deadline. This issue is fixed in version 2.1.0.

### CVE-2026-61854

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-362;CWE-400;CWE-667` |
| Published | 2026-10-30T19:18:28.887 |

VoiceSentinel is a real-time voice moderation system for Minecraft servers. From 2.2.1 until 3.3.1, the optional report buffer feature has a race between retention cleanup and normal transcript writes. In `report_buffer.py`, `_maybe_cleanup()` uses an unlocked dictionary for once-per-hour cleanup throttling, allowing simultaneous `_cleanup_tenant()` operations for one tenant. Cleanup reads `transcripts.jsonl` and rewrites it in place without file locking or atomic replacement, while `report_buffer_append_async` uses `asyncio.to_thread` to append without synchronization. In `main.py`, concurrent `_processing_worker` tasks make this reachable in normal operation; `processing.worker_count` of two or more and public-pool servers sharing a `server_key` increase collisions. With `report_buffer.enabled` set to true, racing writes can lose, duplicate or corrupt transcript data and defeat `report_buffer.retention_seconds` pruning, allowing unbounded disk growth that can exhaust storage and crash the host or other services sharing it. The feature is opt-in and disabled by default. This issue is fixed in version 3.3.1.

### CVE-2026-61586

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-30T19:18:27.840 |

Copernik XML Factory provides secure-by-default JAXP factory creation for Java. Prior to 0.1.2, Copernik XML Factory does not block XInclude resource resolution on the stock JDK provider after an application enables XInclude on a factory returned by `XmlFactories.newDocumentBuilderFactory()` or `XmlFactories.newSAXParserFactory()`, or on an `XMLReader` passed through `XmlFactories.harden()`. An application parsing untrusted XML can resolve attacker-controlled `xi:include` references to disclose local files or, through `http` references, reach internal network endpoints by server-side request forgery. Exploitation requires use of one of those factory/hardening APIs, the stock JDK provider with Apache Xerces absent from the classpath, explicit `setXIncludeAware(true)` or the equivalent reader feature, and XML from an untrusted source. The Xerces provider selected when Xerces is present and the Android provider are unaffected. This issue is fixed in version 0.1.2.

### CVE-2026-119117

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-214;CWE-532` |
| Published | 2026-10-30T19:18:20.007 |

Insertion of sensitive information into a log file in Amazon Kinesis Producer Library for Java before 1.0.8, when the library's logger is configured at DEBUG log level, might allow local users to obtain the AWS credentials that the library resolved for the application. Separately, affected versions of the library pass these credentials to the native child process as command-line arguments, where a local user can read them from the process argument list.



To remediate this issue, users should upgrade to version 1.0.8 or later, rotate any long-term IAM user keys, revoke active role sessions where needed, and restrict or redact log data written by an affected version. 0.x users should migrate to software.amazon.kinesis:amazon-kinesis-producer 1.0.8 or later.

### CVE-2026-119086

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-843` |
| Published | 2026-10-30T18:17:25.050 |

Missing queue-set type validation in the queue-set selection system call in FreeRTOS-Kernel before V11.3.3 on MPU-enabled ports with queue sets enabled allows a local unprivileged task to write actor-controlled data beyond a pointer-sized object on the privileged kernel stack, affecting privileged memory across the MPU isolation boundary.



To remediate this issue, users should upgrade to FreeRTOS-Kernel V11.3.3, rebuild, and reflash affected firmware. Builds that do not enable queue sets are not affected.

### CVE-2026-119148

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-807` |
| Published | 2026-10-30T17:17:16.493 |

Incomplete string validation in AWS aws-nitro-enclaves-sdk-c before 0.4.6 may allow a third party to impersonate the AWS KMS endpoint.



To remediate this issue, users should rebuild any custom enclave image against aws-nitro-enclaves-sdk-c 0.4.6.

### CVE-2026-103898

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-31T08:16:47.460 |

The Wp Social Login and Register Social Counter plugin for WordPress is vulnerable to Authentication Bypass in all versions up to, and including, 3.2.2. This is due to the social login REST callback registered at `/wp-json/wslu-social-login/type/{provider}/` with `permission_callback => __return_true` locating an existing WordPress account solely by the email string returned from the OAuth provider and calling `wp_set_auth_cookie()` without a password check, while the only verification guard — `!empty($getProfile->emailVerified)` in `inc/admin-create-user.php` — is a no-op for the bundled Hybridauth Facebook and Twitter adapters, both of which assign the raw email string rather than a boolean verified flag to `emailVerified`. This makes it possible for unauthenticated attackers to obtain a fully authenticated session as any existing WordPress user, including Administrators, whose registered email address can be presented through a configured Facebook or Twitter login on the target site. Exploitation requires only that the attacker control an OAuth account whose provider-returned email matches the target account's registered WordPress email address; no local credentials, nonce, or prior foothold is needed.

### CVE-2026-119977

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-31T06:16:34.550 |

WordPress Core is vulnerable to Remote Code Execution in versions 4.7 through 7.1.3. This is due to predictable, web-accessible staging paths used during full-package core upgrades. This makes it possible for unauthenticated attackers to execute code on the server during the upgrade window.

### CVE-2026-63182

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-30T22:16:58.280 |

LightSAML implements SAML 2.0 data model classes, XML serialization and deserialization, XML security, certificate support, and message bindings. Prior to 4.7.1 and 5.0.1, LightSAML and xmlseclibs disagree about which assertion an inbound SAML signature covers. `Response::deserialize` uses `manyElementsFromXml` to collect only direct-child `saml:Assertion` elements of `samlp:Response`, and `AssertionSignatureValidatorAction` validates their `ds:Signature` using an out-of-band trusted IdP credential resolved by Issuer, not a key from the document. `XMLSecurityDSig::validateReference()` removes the enveloped signature from the shared DOM, but `processRefNode()` resolves `Reference URI="#id"` document-wide through an XPath of the form `//*[@Id]` and takes `item(0)`, which need not be the assertion whose claims LightSAML consumes. An attacker who has captured one genuinely signed assertion, such as an earlier login response, can place its signature-stripped bytes earlier in `samlp:Extensions` and present a forged direct-child assertion with the same ID and copied genuine signature. Validation then covers the hidden genuine bytes while LightSAML surfaces unsigned attacker-controlled `Subject/NameID`, `Conditions`, and `Attributes`, enabling authentication bypass or privilege escalation even when signature validation is required. The behavior was confirmed in versions 5.0.0 and 4.6.1. This issue is fixed in versions 4.7.1 and 5.0.1.

### CVE-2026-62989

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-285;CWE-862` |
| Published | 2026-10-30T21:17:15.873 |

Shopper is a Headless e-commerce Admin Panel. Prior to 2.10.0, the Variants Livewire component in `packages/admin/src/Livewire/Components/Products/Form/Variants.php` exposes `DeleteAction` and `DeleteBulkAction` without server-side authorization. An authenticated staff user with `edit_products` can access `/shopper/products/{id}/edit` and obtain the signed component state even without `delete_product_variants`. The `callTableAction` and `callTableBulkAction` paths then permanently delete individual or multiple variants without checking that dedicated permission. For variant products, this can destroy the sellable catalogue and disrupt storefront product pages, cart, and checkout. This issue is fixed in version 2.10.0.

### CVE-2026-62967

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-30T21:17:15.290 |

ZTNET is a ZeroTier web UI for private controllers with multiuser and organization support. Prior to 0.8.0, any authenticated low-privilege user can permanently deactivate another account, including an administrator, through `POST /api/auth/user/invalidateUser`. In `src/pages/api/auth/user/invalidateUser.ts`, `getServerSession` checks only that a session exists and does not compare `session.user.id` with the client-supplied `userId`. Supplying a victim's `userId` and a `deviceId` for which no matching pair exists in `UserDevice` makes the handler set the target account's `isActive` to false. Login is then refused by `src/server/auth.ts` with `account-expired`. An attacker needs only a normal authenticated account and the victim's user ID, which may be obtainable from member lists, UI responses, logs, or other application metadata. This can lock administrators out, disrupt organization management, and deny access to any targeted user. This issue is fixed in version 0.8.0.

### CVE-2026-115346

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-30T18:17:22.220 |

The Avada | Website Builder For WordPress & WooCommerce theme for WordPress is vulnerable to Arbitrary File Upload in versions up to, and including, 7.16.2 via the convert_palette_images_to_truecolor() function. This is due to insufficient file type validation before processing uploaded files. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible.

### CVE-2026-61804

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T17:17:27.073 |

myTinyWMS is a free, open-source warehouse management system. Prior to version 1.6.4, `Product (Artikel)` and `Category` management store the `name` parameter without adequate backend sanitization and render raw database strings through unescaped Blade output in dynamic table cells, including `article/index.blade.php` and `category/index.blade.php`. An authenticated attacker can save malicious input through product creation or category forms. When another user, including a worker or administrator, opens the corresponding product sheet, category listing or dashboard, the stored JavaScript executes in that user's browser context. This can enable cross-user script execution, session theft and administrative takeover. This issue is fixed in version 1.6.4.

### CVE-2026-117681

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-31T09:16:33.487 |

A flaw was found in konflux-ci. This vulnerability allows privilege escalation when the user interface proxy automatically disables Transport Layer Security (TLS) certificate verification for connections to internal backend services in environments lacking a default service certificate authority. Because the proxy attaches a cluster-scoped authentication token with user impersonation rights to these requests, an adjacent network attacker capable of intercepting traffic can capture the credentials to gain full administrative control of the cluster.

### CVE-2026-118696

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-299` |
| Published | 2026-10-30T18:17:24.530 |

In JetBrains IntelliJ IDEA, PyCharm, PhpStorm, RubyMine and WebStorm before 2026.3, 2026.2.4, 2026.1.5.1, and 2025.3.6.2; GoLand before 2026.3, 2026.2.4, 2026.1.5.1, and 2025.3.5.2; Rider before 2026.3, 2026.2.4, 2026.1.5.3, and 2025.3.5.3; CLion before 2026.3, 2026.2.4.1, 2026.1.5.2, and 2025.3.6.3; DataGrip before 2026.3, 2026.2.6.1, 2026.1.4.1, and 2025.3.6.1; RustRover before 2026.3, 2026.2.5, 2026.1.4.1, and 2025.3.7.1; DataSpell before 2026.1.3.1 and 2025.3.3.1, the embedded browser trusted revoked intermediate certificates

### CVE-2026-119287

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-30T16:17:42.723 |

Zuke is a code-first, strongly typed build automation system for Deno. Prior to 1.51.0, the @zuke/core MCP registry mode accepts command-form registry descriptors without applying the ZUKE_REGISTRY_LAUNCH_HOSTS authorization enforced for remote module descriptors. When zuke mcp --registry --allow-run reads a registry writable by another party and a run-capable caller invokes the affected tool, the registry writer can choose the program and arguments executed with the operator's environment and workspace access. The --allow-run and --protect name globs do not contain the issue because the descriptor supplies those names, and the optional destructive confirmation displays a description controlled by the same writer. The local default registry populated only through zuke register is not affected because that command writes module-form descriptors. This issue is fixed in version 1.51.0.

### CVE-2026-62958

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-125` |
| Published | 2026-10-30T21:17:14.840 |

libriscv is a RISC-V sandbox and emulator. Prior to 1.18, a crafted ELF binary can cause out-of-bounds reads in the host emulator. `Memory<W>::binary_loader` checks `PT_LOAD` program-header bounds, but `Memory<W>::serialize_execute_segment` trusts section-header `sh_offset` and `sh_size` when locating `.text` without verifying the file range against `m_binary.size()`; `Memory<W>::lookup()` has a similar section-table problem. Malformed `.text` or `.symtab` offsets can therefore bypass the program-header checks and point outside the binary buffer, crashing rvlinux. With suitable memory layout or integer overflow, out-of-buffer host heap memory may instead be mapped into the guest by `create_execute_segment()`, potentially exposing host memory. The reported reproducer demonstrates a host SIGSEGV, while memory disclosure through grooming is described as possible rather than demonstrated. This issue is fixed in version 1.18.

### CVE-2026-104615

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:L/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-30T16:17:36.687 |

A security vulnerability was discovered in SUSE Rancher Fleet's cluster registration flow, in Fleet versions before 0.12, 0.13.0 up to 0.13.17, 0.14.0 up to 0.14.12, 0.15.0 up t o 0.15.17 and 0.16.0 up to 0.16.3. The cluster identity claimed by a registration request was accepted without being bound to the registration token that the request was made with. As a result, a registration request could be associated with a managed cluster that was originally registered with a different registration token.

### CVE-2026-119682

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-30T15:16:51.327 |

An improper access control vulnerability exists in the multi-factor authentication (MFA) functionality of ManageEngine SharePoint Manager Plus (SPMP). A low-privileged authenticated user can bypass authorization checks to read and modify MFA configuration settings, enable or disable MFA for the application, enumerate MFA-enrolled users, and delete MFA-enrolled accounts. Successful exploitation could allow an attacker to weaken authentication protections or cause a denial of service by configuring invalid MFA settings, potentially locking legitimate users out of the application. This vulnerability was fixed in build 4507. The reproduction explicitly uses build 4506.

### CVE-2026-119336

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59;CWE-61` |
| Published | 2026-10-30T20:17:08.297 |

Pi-hole is a DNS sinkhole that protects devices from unwanted content without installing any client-side software. From 6.4.2 until 6.5, the root-run advanced/Scripts/updatecheck.sh cron job applies truncate -s 0 and chmod 644 to /etc/pihole/versions while following symbolic links in a directory owned by the pihole user. An attacker executing as pihole can replace that path with a symlink so the scheduled root operations truncate or create an arbitrary root-owned file, or race the operations so chmod makes a sensitive target world-readable without truncating it. This issue is fixed in version 6.5.

### CVE-2026-119335

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-30T20:17:08.137 |

Pi-hole is a DNS sinkhole that protects devices from unwanted content without installing any client-side software. Prior to 6.5, advanced/Scripts/utils.sh getFTLPID() attempts to validate the pihole-owned /run/pihole-FTL.pid file with expr "${FTL_PID}" : "[^[:digit:]]", but this rejects only values whose first character is not a digit. An attacker with code execution as the pihole user can write a digit-prefixed arithmetic expression to the pihole-owned PID file. Root-run pihole subcommands then evaluate [[ "$pid" -eq "-1" ]], causing Bash to recursively evaluate array subscripts and execute command substitution as root. This bypasses the content-validation portion of the CVE-2026-41489 remediation while leaving its hardcoded PID-file path protection intact. This issue is fixed in version 6.5.

### CVE-2026-119333

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-10-30T20:17:07.780 |

draw.io Desktop is the official Electron build of draw.io. Prior to 31.5.2, the Windows application launched powershell and attrib by bare executable name from src/main/electron.js. When draw.io Desktop was not already running, opening a diagram from File Explorer made the diagram directory the current working directory, allowing a colocated attacker-controlled powershell.bat or attrib.exe to be resolved before the intended system executable. A victim who extracted an attacker-supplied archive and cold-opened its legitimate .drawio file could therefore execute attacker-controlled code when Local Fonts were enabled or when draft or backup attributes were updated. This issue is fixed in version 31.5.2.

### CVE-2026-119777

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-30T18:17:27.427 |

A flaw was found in GStreamer's gst-plugins-bad H.266/VVC parser. When processing a malformed H.266 media file or stream, an integer overflow while parsing profile, tier, and level fields can lead to a stack-based buffer overflow. An attacker could cause an application to crash and may be able to execute code in the context of the affected application.

### CVE-2026-116243

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426;CWE-427` |
| Published | 2026-10-30T20:17:04.160 |

pgAdmin 4 runs pg_dump, pg_restore, pg_dumpall and psql from the binary path a user sets in their preferences. In server mode the binary path was refused only when it lay under the per-user storage directory (STORAGE_DIR), not under a SHARED_STORAGE directory, which ordinary users can upload files to. A user could therefore upload an executable to shared storage, point their binary path at it, and have pgAdmin run it as the operating-system account running pgAdmin. On POSIX, files created through pgAdmin are not executable, so this is exploitable where any file with an executable name can run, such as Windows server mode.

The fix checks the binary path against every SHARED_STORAGE directory as well, after expanding $DIR, collapsing ".." and resolving symbolic links, compares directories in a way a different spelling on a case-insensitive filesystem cannot bypass, refuses a path containing a NUL, and enforces the check wherever binary paths are resolved, including for the PSQL tool.

This issue affects pgAdmin 4: before 9.19.

### CVE-2026-63414

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-30T23:17:15.707 |

Shopify App is a Rails engine for building Shopify applications. From 22.1.0 until 23.0.3, `token-exchange` authenticated controllers can expose a request-derived `shop` context instead of the identity from a verified Shopify ID token or active Shopify session. `current_shopify_domain` can resolve to the sanitized `shop` query parameter, so a request authenticated for one `shop` can cause application code to treat a different requested `shop` as current. Affected applications use `shopify_app` `token-exchange` authentication, accept authenticated requests with a `shop` query parameter, and rely on `current_shopify_domain` or `params[:shop]` for authorization, tenant lookup, stored access-token selection or `shop`-scoped data access. An attacker with a valid Shopify session token for one `shop` can supply another `shop` in that parameter and potentially obtain unauthorized application data or perform `shop`-scoped actions, depending on the application's authorization model. This issue is fixed in version 23.0.3.

### CVE-2026-120194

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-31T10:16:38.310 |

A flaw was found in json-glib. The JSONPath slice evaluator used by json_path_query() can enter an infinite loop when given a slice expression with a negative step. An application that evaluates attacker-controlled JSONPath expressions can be forced into a hang, leading to a denial of service.

### CVE-2026-109197

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-31T10:16:37.507 |

The WP Directory Kit plugin for WordPress is vulnerable to generic SQL Injection via the 'idfield' parameter in all versions up to, and including, 1.6.0 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-120040

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-31T07:16:37.370 |

The Mail logging & Catcher plugin for WordPress is vulnerable to Sensitive Information Exposure in all versions up to, and including, 2.2.0 via the 'message' parameter. This makes it possible for authenticated attackers, with subscriber-level access and above, to extract valid administrator password-reset keys from stored email logs and complete the WordPress password-reset flow to escalate privileges to administrator. Exploitation requires an administrator to have previously configured the plugin's default_view_role setting to a capability held by low-privileged users such as 'read'; on an untouched install the default of 'manage_options' restricts log access to administrators only.

### CVE-2026-119163

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-31T07:16:36.600 |

The FunnelKit Automations – Email Marketing Automation and CRM for WordPress & WooCommerce plugin for WordPress is vulnerable to time-based SQL Injection via the 'bwfan_cart_id' parameter in all versions up to, and including, 3.8.5.2 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. Exploitation is a two-step persisted attack: an unauthenticated attacker submits a crafted bwfan_cart_id value during a guest Store API checkout (requiring only a publicly obtainable WooCommerce cart nonce), and the injection fires when a scheduled Action Scheduler job later reloads the stored meta upon order status transition out of pending, failed, or cancelled.

### CVE-2026-63341

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248;CWE-400` |
| Published | 2026-10-30T23:17:13.690 |

Aedes is an MQTT broker that can run on any stream server. Prior to 1.1.1, the MQTT broker does not bound topic depth or structural complexity before passing topics through `mqemitter` into `qlobber`. A `PUBLISH`, `SUBSCRIBE`, or registered `Will` message containing an excessively deep topic can reach `qlobber._split_words` in `lib/qlobber.js` and trigger an uncaught `too many words` exception. Calls from `handlers/subscribe.js` and the publishing logic are not protected against that exception, so it escapes to the `Node.js event loop` and terminates the entire broker. The `Will` path is independently reachable when a client disconnects ungracefully: it calls `broker.publish` directly and bypasses the `PUBLISH` handler. An attacker must be able to establish an `MQTT session`, authenticated or unauthenticated according to broker configuration. A successful attack disconnects all legitimate clients and prevents reconnection until the broker process restarts. This issue is fixed in version 1.1.1.

### CVE-2026-111578

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T22:16:53.880 |

The PDF Invoices & Packing Slips for WooCommerce WordPress plugin from 5.16.2 before 5.16.5 does not properly escape several customer-supplied order fields — including the billing and shipping address values and the customer order note — before they are output in generated invoice and packing-slip documents, allowing unauthenticated users placing guest orders to store a malicious script that executes when a shop administrator views the document, leading to Stored Cross-Site Scripting.

### CVE-2026-62966

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476;CWE-672` |
| Published | 2026-10-30T21:17:15.137 |

ESPAsyncWebServer is an asynchronous HTTP and WebSocket server library for ESP32, ESP8266, RP2040 and RP2350. Prior to version 3.11.2, the multipart parser in `src/WebRequest.cpp` frees `_itemBuffer` and sets it to NULL when `BOUNDARY_OR_DATA` matches the closing boundary of a file part, before confirming the following terminator, while leaving `_itemIsFile` true. If the next byte is neither the final closing dashes nor a clean CRLF, the `DASH3_OR_RETURN2` or `EXPECT_FEED2` rewind branch re-injects provisionally consumed bytes through `itemWriteByte`. Because `_itemIsFile` remains true, `_itemBuffer`[`_itemBufferIndex`++] writes through a null pointer. On ESP32 this causes a `StoreProhibited` exception, panic and device reboot, producing remote denial of service. A route with a non-trivial body/upload handler, such as a file-upload or web-OTA endpoint, must be present. This issue is fixed in version 3.11.2.

### CVE-2026-62864

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-30T21:17:14.693 |

Ring is a Clojure web applications library inspired by Python's WSGI and Ruby's Rack. Prior to 1.15.5, `wrap-nested-params` in the `ring.middleware.nested-params` namespace uses a backtracking regular expression to match parameter names from URL query strings and HTTP request bodies. An attacker can craft a parameter name that drives quadratic O(n^2) matching work, causing regular-expression denial of service in applications using the middleware. `Ring-Defaults` users are also exposed because nested-params is enabled by default. Applications omitting the middleware do not expose this parsing path. This issue is fixed in version 1.15.5.

### CVE-2026-62297

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-10-30T21:17:13.520 |

ag-psd is a JavaScript library for reading and writing Photoshop Document files. Before the allocation-limit remediation attempt in version 31.0.0, `readPsd()` commits image and layer buffers from attacker-declared PSD geometry before validating the declarations against the actual available data or sane allocation limits. The `psdReader.js` implementation sizes off-heap typed arrays using `width`, `height`, `channels`, `depth` and `per-layer rectangles`, so a tiny PSD declaring enormous geometry can force multi-gigabyte memory allocation before a later bounds error. The reported 52-byte input on Node 24 produced approximately 3.17 GB peak RSS before a RangeError; under memory pressure the process can be terminated before the error can be caught, and concurrent inputs can exhaust memory. Services reading untrusted PSDs are exposed to denial of service. This differs from genuinely large PSD files whose memory demand is proportional to real input content. Version 31.0.0 adds a composite-image allocation limit, but complete coverage of the separately described layer-rectangle allocation path is not established and requires curator residual/scope review.

### CVE-2026-62264

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-287;CWE-306` |
| Published | 2026-10-30T19:18:32.827 |

PDF Reader MCP is a Model Context Protocol server for reading PDF documents. In versions 2.2.0 and later prior to 3.0.1, when `MCP_TRANSPORT=http` enables the opt-in HTTP server, `@sylphx/pdf-reader-mcp` reads `MCP_API_KEY` and logs that `X-API-Key` authentication is enabled but never validates the `X-API-Key` header on incoming requests. The `/mcp` endpoint consequently accepts unauthenticated clients. With the default bind address of `0.0.0.0`, any client able to reach the port can invoke every PDF tool and read any PDF the server process can open on the host, despite the misleading authentication-enabled startup log. URL-based sources additionally permit limited server-side request forgery; private and loopback destinations are blocked by default unless `--allow-private-ips` is set. The default `stdio` transport is unaffected. This issue is fixed in version 3.0.1.

### CVE-2026-59978

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-30T19:18:27.480 |

AdminNeo is a full-featured database management tool written in PHP. From 4.6.2 until 5.5.0, the unauthenticated `?script=version` endpoint accepts POST data without origin, CSRF or parameter-type validation. A `version[]` parameter becomes a PHP array that `bootstrap.inc.php` serializes into the shared `adminneo.version` cache. On later page loads, `design.inc.php` passes that cached value to `cookie()` and `rawurlencode()`, causing a `TypeError` rather than encoding a version string. A remote attacker can make the instance return HTTP 500 to all users for the cache's twenty-four-hour lifetime or until the poisoned cache is removed. Exploitation requires the web server to be able to write that shared cache; making it unwritable is an interim workaround. The issue retains the underlying type-validation defect reported previously in Adminer despite changes to AdminNeo's version-checking flow. This issue is fixed in version 5.5.0.

### CVE-2026-46560

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-30T19:18:25.203 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.1, the `RADIUS` authentication module opens an unconnected datagram socket and trusts the first UDP datagram received on the client source port. The receive path does not verify the source IP and port, match the response identifier to the outstanding request, or verify the RFC 2865 `Response Authenticator`; the RFC 2869 `Message-Authenticator` is neither sent nor required. Any non-Reject/non-Challenge packet is treated as success. On a deployment with a `RADIUS` module instance enabled on a login chain, an unauthenticated network attacker can race the real server on-path or spray forged `Access-Accept` packets off-path and obtain a session for any `RADIUS`-mapped username without knowing the shared secret. Unlike CVE-2024-3596, exploitation requires no MD5 chosen-prefix forgery because no response authenticator is checked. The resulting session carries the impersonated principal's privileges. This issue is fixed in version 16.1.1.

### CVE-2026-39734

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-35` |
| Published | 2026-10-30T19:18:24.280 |

Unauthenticated Path Traversal in WP EasyPay <= 4.5.4 versions.

### CVE-2026-116862

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-30T19:18:15.570 |

Unauthenticated Broken Access Control in WP REST Cache <= 2026.3.1 versions.

### CVE-2026-116861

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-30T19:18:15.427 |

Unauthenticated Sensitive Data Exposure in Flexible Chat <= 1.1.0 versions.

### CVE-2026-116401

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-30T19:18:13.903 |

Unauthenticated Broken Access Control in HUSKY <= 1.4.6 versions.

### CVE-2026-97638

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-30T18:18:21.470 |

The Forminator Forms – Contact Form, Payment Form & Custom Form Builder plugin for WordPress is vulnerable to Insecure Direct Object Reference in all versions up to, and including, 1.57.3.1 via the 'previous_draft_id' parameter due to missing validation on a user controlled key. This makes it possible for unauthenticated attackers to delete arbitrary saved drafts belonging to other users and take over those draft identifiers by overwriting them with attacker-controlled form submissions. This requires the attacker to have obtained a victim's draft_id, which may be harvested from a shared "continue later" link; the nominally present nonce check is effectively bypassed because the nonce is publicly obtainable by any unauthenticated visitor loading a form page.

### CVE-2026-76012

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-30T18:18:12.937 |

The Photo Gallery, Sliders, Proofing and Themes – NextGEN Gallery plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 4.4.1 via the legacy_render function. This is due to broken authorization on the Lightroom gallery_edit endpoint combined with mass assignment of gallery path and unrestricted file upload into a registered template directory, whose extension check uses a substring match that accepts sanitized .php_ filenames as valid templates. This makes it possible for authenticated attackers, with custom-level access and above, to execute code on the server. Exploitation requires the authenticated attacker to be the stored author of at least one existing NextGEN gallery, as ownership of that gallery is the sole authorization check gating the mass-assignment and upload steps.

### CVE-2026-110305

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-30T18:17:20.060 |

The Advanced Custom Fields: Extended plugin for WordPress is vulnerable to Sensitive Information Exposure in all versions up to, and including, 0.9.2.7 via the process. This makes it possible for unauthenticated attackers to extract sensitive data including the WordPress password hash of any user by injecting a {get_user} template tag that is resolved and written as a publicly readable term name. Exploitation requires that an administrator has configured a public [acfe_form] shortcode page with a Term action using a save.name field mapping — a supported and documented configuration.

### CVE-2026-107630

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-30T18:17:19.237 |

The Email Templates Customizer and Designer for WordPress and WooCommerce plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 1.5.14 This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to enumerate WooCommerce order IDs via the preview_order parameter and exfiltrate every customer's billing name, address, phone number, and email address. The exploit requires two unauthenticated requests: the first harvests a reusable nonce from the 302 Location header returned by the unguarded admin_init handler, and the second supplies that nonce alongside an arbitrary order ID to the preview endpoint, making full customer PII disclosure trivially achievable without any account or credentials.

### CVE-2026-119290

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-532` |
| Published | 2026-10-30T16:17:43.160 |

Zuke is a code-first, strongly typed build automation system for Deno. Prior to 1.51.0, @zuke/core writes rendered reportSummary(...) notes to GITHUB_STEP_SUMMARY through writeJobSummary without applying the redactor that protects resolved secret() values in console and persisted run output. A GitHub Actions build that places secret-derived text in a summary note can publish credentials in cleartext to everyone able to view the workflow run, including unauthenticated viewers of a public repository, and the durable summary remains exposed until the run is deleted. GitHub Actions masking directives do not protect the summary file, while runs outside GitHub Actions and builds that do not summarize secret-derived text are not affected. This issue is fixed in version 1.51.0.

### CVE-2026-61739

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-862` |
| Published | 2026-10-30T15:16:53.650 |

SOCFortress CoPilot focuses on providing a single pane of glass for all your security operations needs. Prior to 0.1.77, the Velociraptor Sigma exclusion-management endpoints in `backend/app/incidents/routes/incident_alert.py` omit role and tenant authorization, and `POST /api/incidents/alerts/create/velo-sigma/exclusion` does not validate credentials. Its `return_username_for_logging` dependency in `backend/app/auth/utils.py` calls `decode_token`, which returns ordinary Invalid token or Expired signature strings on failure, and the dependency passes these strings through instead of rejecting the request. A Bearer header is required, but an arbitrary invalid, expired or forged value can create a suppression rule without a valid account. The collection GET at /create/velo-sigma/exclusion lists exclusions; the read, update and delete routes under `/create/velo-sigma/exclusion/{exclusion_id}`, and the `/velo-sigma/exclusion/{exclusion_id}/toggle` route, use `get_current_user` without role checks, permitting any authenticated `customer_user` to manage every exclusion. In `backend/app/incidents/services/velo_sigma.py`, `process_sigma_alert` calls `check_exclusions` and drops matching enabled alerts before incident creation. A null `customer_code` applies a rule across all tenants. Attackers can suppress detections platform-wide through channel, title or field matching, while low-privilege accounts can enumerate detection-tuning data and modify, disable or delete legitimate exclusions. This issue is fixed in version 0.1.77.

### CVE-2026-45145

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-30T15:16:51.923 |

Chamilo LMS is an open-source learning management system. Prior to 2.0.1, `public/main/inc/lib/career.lib.php` and `public/main/cron/import_csv.php` call PHP's native `unserialize()` on `user_career.extra_data` retrieved from the database without the `allowed_classes: false` safety option. An attacker able to write crafted serialized PHP objects to that column, for example through a separate SQL injection, a compromised admin CSV import, or a lower-privilege admin panel, can instantiate arbitrary PHP objects and trigger POP gadget chains in autoloaded `Symfony`, `Doctrine`, or `Monolog` components. This permits arbitrary OS commands as the web server user, compromising server confidentiality, integrity, and availability. This issue is fixed in version 2.0.1.

### CVE-2026-116755

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-31T02:17:33.957 |

Improper Neutralization of Special Elements used in a Command ('Command Injection') in the Orchestrator component of SoftIron HyperCloud allows an authenticated user with access to the management plane to execute arbitrary operating system commands on hypervisor hosts as the privileged orchestration user. Attacker-controlled virtual machine template content (for example, the VM DESCRIPTION field) is delivered to hosts through a shell here-document whose terminator is not quoted, so shell expansion and here-document terminator injection are performed on that content during virtual machine lifecycle operations such as deploy, migrate, and network setup. Exploitation requires valid credentials, access to the management plane (owning a virtual machine alone is not sufficient), and a lifecycle operation that reaches the affected host. This issue affects the Orchestrator component of SoftIron HyperCloud from 1.0 through 2.6.17 and is fixed in 2.6.18.

### CVE-2026-63398

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-30T23:17:14.850 |

Coop is an open source review and moderation tool from ROOST. Prior to 1.0.2, the SAML strategy's verify callback resolved the authenticated user by email alone using `kyselyUserFindByEmail`, without binding the lookup to the organization in `/saml/login/:orgId/callback`. An attacker who administers an organization and controls its SAML IdP signing key can submit an assertion for a victim email to another organization's callback when that target organization has registered the same signing certificate. The assertion verifies against the target certificate, and the email resolves to the target user, creating a session as that user and allowing full cross-tenant account takeover without privileges in the target organization. Exploitation requires the unusual configuration in which the target certificate matches a signing key controlled by the attacker. This issue is fixed in version 1.0.2.

### CVE-2026-119764

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T18:17:27.273 |

Mythic 3.2.16 through 3.4.0.61 contains a stored cross-site scripting vulnerability that allows attackers controlling target endpoint files to run JavaScript in the Mythic UI origin by planting HTML in .pdf-named files. When an operator downloads the file and clicks Preview Media, content-sniffed HTML from /direct/view renders same-origin, stealing localStorage JWTs for full GraphQL and REST access.

### CVE-2026-118205

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-30T18:17:24.253 |

The Essential Addons for Elementor – Popular Elementor Templates & Widgets plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 6.8.7 via the `page_id` parameter of the `register_user()` function. The vulnerability exists because the handler's post status deny-list rejects `future`, `draft`, and `pending` but admits `inherit` — the status carried by every WordPress revision — allowing an attacker to substitute a revision ID for a live page ID, while a flawed "last saved by administrator" check reads `post_author` on revisions (which reflects the editing administrator) rather than the `_edit_last` meta that is never copied to revisions, and the nonce gate is rendered ineffective because any unauthenticated visitor can freely obtain a valid nonce via the `wp_ajax_nopriv_eael_get_token` endpoint. This makes it possible for unauthenticated attackers to register an account with a role as high as Editor — gaining capabilities including `edit_others_posts`, `publish_pages`, `upload_files`, and `unfiltered_html` — by naming a revision whose `_elementor_data` contains an elevated role an administrator previously saved and later reverted on a page bearing the Login/Register widget. Successful exploitation requires that the site has "Anyone can register" enabled and that an administrator has at some point saved and then reverted a non-default "New User Role" on an affected page.

### CVE-2026-62848

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502;CWE-913` |
| Published | 2026-10-30T21:17:13.957 |

Metalama is a Roslyn-based open-source patterns and architecture toolkit for C#. From 2023.0.101-rc until 2025.1.18, 2026.0.25 and 2026.1.19, the Windows Visual Studio integration deserializes local named-pipe messages without restricting which CLR types can be instantiated. The pipe connects `devenv`, the out-of-process Roslyn code-analysis process and the `CodeLens` process, and has the predictable name `Metalama_{role}_{processId}_{hash(PackageVersion)}`. Releases from the first public 2023.0 line through 2026.0.x use Newtonsoft.Json with `TypeNameHandling.All`; the later `SerializationBinder` only remaps assembly names, and `BindToType` resolves arbitrary wire-supplied types without an allow-list. Releases 2026.1.0 through 2026.1.18 use typeless MessagePack with `TypelessObjectResolver` and likewise instantiate arbitrary types. A same-user local process able to write to the pipe can send crafted messages that lead to arbitrary code execution with confidentiality, integrity and availability impacts inside the affected Visual Studio process. Default Windows pipe ACLs limit writers to the same logged-in user, so this does not escalate privileges or cross a security boundary; command-line and MSBuild-only builds do not use the channel. The maintained Metalama + PostSharp extension is affected from 2024.1 through 2026.1.4, while earlier Metalama-free PostSharp versions are unaffected. The retired Metalama and Caravela extensions remain affected and require removal or migration. The framework issue is fixed in versions 2025.1.18, 2026.0.25 and 2026.1.19; the maintained Metalama + PostSharp Visual Studio extension is fixed in version 2026.1.5. The retired Metalama and Caravela extensions require removal or migration.

### CVE-2026-78402

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-787` |
| Published | 2026-10-30T20:17:17.653 |

Stack-based buffer overflow and out-of-bounds
write vulnerability in Thales Sentinel Keys Server on Windows allows Overflow
Buffers. 



Sentinel Keys Server does not check the length of the first field in
the input message. A local attacker may craft an input and send it to Sentinel
Keys Server. It may lead to code execution as NT AUTHORITY\SYSTEM enabling
local privilege escalation.





This issue affects Sentinel Keys Server: versions
lower than 1.3.8.0.

### CVE-2026-116250

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59;CWE-367` |
| Published | 2026-10-30T20:17:05.170 |

In server mode pgAdmin 4 validates a path a user gives for a file in their storage directory with check_access_permission() and then opened it by name. Several places opened it with a plain open() or handed the path to a utility that opened it later: the servers.json export and import and the import file listing, and the files given to pg_dump, pg_dumpall, pg_restore and psql by Backup, Restore and Import/Export Data. A symbolic link swapped in at the file or at any parent directory between the check and the open redirected the operation outside the storage directory, so a file could be written, overwritten or read, or loaded into a table, as the operating-system account running pgAdmin. A hard link to an outside file, which O_NOFOLLOW does not detect, and a FIFO, which could hang a request, had the same effect. CVE-2026-86861 fixed this for the File Manager's save_file; these were the remaining paths.

Exploitation requires creating such a link or FIFO inside the user's storage directory. pgAdmin offers no way to do so, and the per-user storage directories belong to the pgAdmin account, so this requires write access to the storage backend as a different operating-system user, for example a shared or network-mounted storage directory, and winning the race.

The fix opens each file by walking down from the storage directory one component at a time with O_NOFOLLOW, accepting only a regular file with one link, and passes the utilities the open descriptor (/dev/fd/N) on Linux. Error messages no longer include the server path.

This issue affects pgAdmin 4: before 9.19.

### CVE-2026-61627

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-787` |
| Published | 2026-10-30T15:16:52.650 |

libass is a portable subtitle renderer for the `ASS`/SSA (Advanced Substation Alpha/Substation Alpha) subtitle format. Prior to 0.17.5, libass can overread and overwrite the glyph array in `wrap_lines_measure` while rendering malicious `ASS` content. In `wrap modes other than two`, a final line ending with a literal backslash-n sequence and otherwise consisting only of such sequences or spaces can remain after early trimming and make the line-measurement loops overshoot by one glyph. When the total text size exactly matches the allocated glyph-array capacity, the first loop reads an uninitialized 32-bit fixed-point `pos.x` value, although that value is not subsequently used. The second loop writes `pos.x` and `pos.y` beyond the array, zeroing the first and adding an attacker-controllable offset to the second. No actual exploitation beyond possible denial of service is known; broader exploitation is theoretical and constrained by the addresses, limited writes, and ASLR. This issue is fixed in version 0.17.5.

### CVE-2026-61626

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-30T15:16:52.500 |

libass is a portable subtitle renderer for the ASS/SSA (Advanced Substation Alpha/Substation Alpha) subtitle format. From 0.17.4 until 0.17.5, libass event pruning does not guard negative Matroska `ReadOrder` values, allowing an attacker to clear arbitrarily many bits to zero at attacker-controlled positions near the NULL pointer. Exploitation requires a malicious Matroska stream loaded through `ass_process_chunk`, enabled read-order checking, and later pruning of the malicious events. Read-order checking is enabled by default unless `ass_set_check_readorder` is called with zero; pruning must occur explicitly through `ass_prune_events` or through automatic pruning previously enabled with `ass_configure_prune`. On common systems with arithmetic right shift, 32-bit int values, the upper address region reserved to the kernel, and matching binary/kernel architecture, the expected consequence is denial of service. More extensive exploitation on uncommon systems is theoretical and strongly constrained by the target addresses, bit-clearing-only mutation, and ASLR. This issue is fixed in version 0.17.5.

### CVE-2026-120114

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T10:16:38.183 |

The Debug Log Manager – Conveniently Monitor and Inspect Errors plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'message (and pageUrl)' parameter in all versions up to, and including, 2.5.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires that the site administrator has debug logging enabled with JS error logging active, and that the attacker can obtain the publicly emitted dlmVars.jsErrorLogging nonce — which is broadcast on every frontend page — to pass the nonce check on the unauthenticated endpoint.

### CVE-2026-120075

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T09:16:33.897 |

The WP Activity Log plugin for WordPress is vulnerable to Stored Cross-Site Scripting in all versions up to, and including, 5.6.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-110530

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T09:16:32.933 |

The FeedWordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting in versions up to, and including, 2026.0517 via syndicated RSS/Atom feed content. The plugin's SyndicatedPost::sanitize_content() function only strips the 'target' attribute (the lines that would strip 'style' and 'on[a-z]+' event-handler attributes are commented out), and SyndicatedPost::insert_post() deliberately removes WordPress's wp_filter_kses and wp_filter_post_kses filters from content_save_pre before persisting imported feed items via wp_insert_post(). This makes it possible for unauthenticated attackers who control an external feed that a site has already subscribed to to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-118057

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T08:16:48.903 |

The Shield Security – Smart Bot Blocking, Brute-Force Login Protection & File Scanning plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'REQUEST_URI' parameter in all versions up to, and including, 22.3.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The hidden 'path' column in ForTraffic.php lacks a client-side render function, so DataTables builds its cell via innerHTML, causing stored HTML in the path value to be parsed into live DOM nodes; a prior partial fix in version 18.5.8 added esc_html() only to the visible 'page' column, leaving the hidden 'path' field unescaped and exploitable through version 22.2.6.

### CVE-2026-107759

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T08:16:48.033 |

The WPO365 | MICROSOFT 365 GRAPH MAILER plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'Subject (via wp_mail/PHPMailer, e.g. CF7 your-subject)' parameter in all versions up to, and including, 6.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload is stored without authentication via any mail-sending feature that forwards a submitter-controlled subject (e.g. a Contact Form 7 form) when the Graph Mailer is enabled but OAuth authorization has not been completed, a default state immediately after plugin activation.

### CVE-2026-119162

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T07:16:36.457 |

The User Submitted Posts – Enable Users to Submit Posts from the Front End plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via the 'user-submitted-content' parameter in all versions up to, and including, 20260916 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. On a default installation the submitted post is held as Pending and requires admin approval before the payload is reachable by other visitors; however, if the plugin's "publish immediately" option is enabled, no approval step exists and the stored payload becomes live without any moderator interaction.

### CVE-2026-119089

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T07:16:36.313 |

The ThirstyAffiliates – Affiliate Links, Link Branding, Link Tracking & Marketing Plugin plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 3.12.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This vulnerability is only exploitable on block themes (such as Twenty Twenty-Five) where the Comment Content block causes comment HTML to flow through render_block, triggering the plugin's transformer. Additionally, a successful attack requires the attacker to have had one prior comment approved, after which subsequent crafted comments are auto-approved and rendered publicly.

### CVE-2026-119065

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T07:16:36.163 |

The Shipping Zones by Drawing for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'szbd-picked' checkout parameter in versions up to, and including, 3.3.0 The szbd_checkout_field_update_order_meta() handler stores stripslashes(sanitize_text_field($_POST['szbd-picked'])) in order meta without validating the JSON structure or restricting dangerous characters, and the szbd_show_checkout_field_admin_order_meta() handler later concatenates the decoded lat and lng values directly into a double-quoted href attribute without esc_url() or esc_attr(). This makes it possible for unauthenticated attackers, by submitting an ordinary guest-checkout order with a crafted szbd-picked JSON payload, to inject arbitrary attributes (such as onmouseover) onto the Google Maps link in the WooCommerce admin order view that will execute whenever an administrator accesses an injected order.

### CVE-2026-118070

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T07:16:36.007 |

The Welcart e-Commerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'gid' parameter in all versions up to, and including, 2.12.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload is staged by an unauthenticated visitor who forges the ROBOT PAYMENT browser-return request, storing the malicious gid value in order metadata; the script then fires when an administrator opens that order in the WordPress admin panel.

### CVE-2026-116548

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T07:16:35.717 |

The VikRentCar Car Rental Management System plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'optionals' parameter in all versions up to, and including, 1.4.10 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-116522

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T07:16:35.410 |

The Relevanssi – A Better Search plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 4.28.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the site to have both the comment indexing and comment highlighting options enabled, and the payload only fires when a visitor reaches a singular page via a Relevanssi search-result permalink carrying the highlight query parameter.

### CVE-2026-115840

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T07:16:35.140 |

The VikRentCar Car Rental Management System plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'poplink' parameter in all versions up to, and including, 1.4.9 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The handler requires only a WordPress nonce (vikwp_nonce), which the plugin itself emits to unauthenticated visitors on the public booking-confirmation page, allowing an attacker to obtain a valid token without any account.

### CVE-2026-111254

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T07:16:34.987 |

The W3 Total Cache plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 2.10.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires that a Pro license was previously active with REST caching enabled and has since become inactive while Disk Enhanced page caching remains configured, and that the attacker holds a previously approved commenter identity.

### CVE-2026-107750

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T07:16:33.920 |

The PDF Invoices & Packing Slips for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'billing_address.first_name / last_name / company, customer_note' parameter in all versions up to, and including, 5.16.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is an incomplete fix for CVE-2026-92244: the wp_kses() allow-list introduced in 5.16.2 correctly blocks raw-tag payloads but is bypassed by entity-encoded payloads (e.g., &lt;img onerror=…&gt;) that contain no literal angle-bracket characters and are therefore passed through unmodified before the trailing decode rematerializes them.

### CVE-2026-107653

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T07:16:32.940 |

The SureCart – Ecommerce Made Easy For Selling Physical Products, Digital Downloads, Subscriptions, Donations, & Payments plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 4.9.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful execution requires the injected comment to be visible on a page that loads SureCart's web-component bundle (e.g. a page containing a SureCart Buy Button block), and the comment must be auto-approved or approved by a moderator.

### CVE-2026-116520

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T06:16:32.630 |

The PPWP – Password Protect Pages plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment / shortcode attribute desc_below_form (and placeholder as the marker-smuggling helper)' parameter in all versions up to, and including, 1.9.26 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is exploitable by unauthenticated attackers because WordPress's comment_content filter leaves bare shortcode text (containing no HTML tags) untouched, and the comment_whitelist setting auto-approves subsequent comments from a previously approved name and email without administrator intervention.

### CVE-2026-109997

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T06:16:31.853 |

The Ninja Forms – Contact Form Builder with Calculators, Quizzes, Signatures & AI Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'formData.extra' parameter in all versions up to, and including, 3.15.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The nf_ajax_submit endpoint issues a valid nonce to any requester on failure, effectively neutralizing the nonce check and making exploitation trivially achievable in a single unauthenticated request.

### CVE-2026-109234

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T06:16:31.510 |

The Meow Lightbox plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'post_content (bbPress reply body)' parameter in all versions up to, and including, 5.6.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the administrator to have enabled Output Buffering, the HtmlDomParser engine, and Aggressive Resolve, as well as a stored-HTML submission surface (such as bbPress anonymous replies) whose kses allow-list preserves img attributes; given these preconditions, a one-shot unauthenticated submission can execute arbitrary JavaScript in the context of any user who views the affected page.

### CVE-2026-63224

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-30T22:16:58.837 |

OpenRemote is an open-source internet-of-things platform. Prior to 1.26.0, the `datapoint export` API constructs `CSV crosstab` SQL by concatenating an `asset name` and `attribute name` into a `COPY` query that uses `crosstab` and streams `TO STDOUT`. The `asset name` enters both a double-quoted column identifier and a category query enclosed by the fixed `$cat$` delimiter. Escaping single quotes in one string context does not escape embedded double quotes in identifiers or protect that dollar-quote boundary. An authenticated user permitted to create or rename an asset and read/export datapoints for one of its attributes can store SQL metacharacters in the name and request a `crosstab` export, causing injected SELECT output to be returned in the normal ZIP/CSV response. This enables database exfiltration without direct database or filesystem access or token forgery. In a multi-tenant deployment it can expose other tenants' data if the manager's database role can read shared tables; integrity and availability effects are not established by the demonstrated read primitive. This issue is fixed in version 1.26.0.

### CVE-2026-116249

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:L/VA:L/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-10-30T20:17:05.027 |

In server mode pgAdmin 4 resolves a server's password file, SSL certificate, key, CRL and SSH tunnel identity file relative to the user's storage directory, but get_complete_file_path() only stripped leading slashes before joining the two. A path such as "../<another user>/.pgpass", set through the server dialog, the REST API or a servers.json import, therefore named another user's file, and connecting used that user's saved passwords, client certificate or SSH key. The sslkeylogfile connection parameter was passed to libpq unchanged, so a path outside storage let libpq create or append a file as the account running pgAdmin.

make_conninfo() also quoted connection parameter values but not their names, so a crafted parameter name could smuggle additional keyword=value pairs past these checks.

The fix requires the resolved path, with symbolic links followed, to stay inside the user's storage directory or the named shared storage directory, confines sslkeylogfile the same way, and accepts only exact libpq keywords as connection parameter names. A refused path or keyword is reported instead of letting libpq fall back to a default.

This issue affects pgAdmin 4: before 9.19.

### CVE-2026-118089

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-30T19:18:17.383 |

Shop manager PHP Object Injection in Product Feed Manager <= 7.14.1 versions.

### CVE-2026-96894

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T18:18:21.320 |

The ERP: Complete HR, Accounting & CRM Suite Built for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Inbound Email Body in all versions up to, and including, 1.17.10 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The inbound email router's only gate is a regex match on the References header for a reply token whose hash is never cryptographically validated, meaning any external party who received or can mimic a CRM outbound email can satisfy the check without a WordPress account.

### CVE-2026-112365

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T18:17:20.993 |

The easy.jobs – AI powered Job Listing, Job Board, Career Page, Recruitment & Hiring Solution plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'cover_letter' parameter in all versions up to, and including, 2.8.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful execution requires an administrator to open the affected candidate's Application tab and click the attacker-crafted link, at which point WHATWG URL parsing collapses the encoded scheme back to javascript: and executes the payload.

### CVE-2026-104744

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T18:17:15.690 |

The Independent Analytics Pro plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'utm_campaign' parameter in all versions up to, and including, 2.15.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the Independent Analytics Pro build to be active, as the free build nulls campaign parameters; additionally, the attacker must first visit a frontend page to obtain a server-signed payload that can be replayed with a crafted utm_campaign value against the unauthenticated /iawp/search REST endpoint, since the signature check does not cover utm_* fields.

### CVE-2026-118238

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-30T16:17:41.993 |

The Tenda W18E web management server is vulnerable to OS command injection via the "diagnose" packet-capture feature due to improper validation of JSON fields. An authenticated user can inject shell metacharacters into the protocol or targetDevice fields, which are later concatenated into a tcpdump command and executed with root privileges. This vulnerability can be exploited without authentication if the device is in a factory-reset state.

### CVE-2026-63201

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-134` |
| Published | 2026-10-30T22:16:58.637 |

Netopeer2 is a server for implementing network configuration management based on the `NETCONF` Protocol. In affected versions, a low-privileged authenticated `NETCONF` user can remotely crash `netopeer2-server` by sending a `get RPC` with an invalid `subtree filter` whose text contains format specifiers. In `src/netconf.c`, `np2srv_rpc_get_cb()` sends the invalid value through `ERR()` to `np2log_printf()`, where `vsnprintf()` first formats the message safely. In `src/log.c`, that already formatted buffer is subsequently passed to `np2log()` as the format string itself, causing `vsyslog()` to interpret attacker-controlled percent sequences and read invalid pointer arguments. The reported denial of service was confirmed on version 2.8.7 using `NETCONF`-over-SSH and AddressSanitizer; reliable remote code execution was not confirmed. `The advisory identifies 2.8.8 as patched`; repository comparisons verify the fix in public release 2.8.21. The affected/fixed boundary remains unresolved because no public 2.8.8 tag was located, which does not establish the status of an untagged 2.8.8 build.

### CVE-2026-63184

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-829;CWE-918` |
| Published | 2026-10-30T22:16:58.447 |

Refitter is a tool for generating a C# REST API client using the Refit library. Prior to 2.1.1, the `refitter` dotnet tool invokes `NJsonSchema` with unsafe defaults for `$ref` resolution when generating Refit interfaces and contracts from attacker-controlled or attacker-influenced OpenAPI descriptions. Remote `http(s)` references cause requests from the developer or CI host and inline untrusted remote schema content into generated output. Absolute local file paths and relative `../` traversal outside the input directory also resolve and inline local content, permitting arbitrary local-file disclosure. The demonstrated chain stops at server-side request forgery, remote file inclusion, and local file inclusion, not code execution: Refit sets the base URL at runtime, enum values use verbatim-string doubling, and string defaults are escaped. This issue is fixed in version 2.1.1.

### CVE-2026-62301

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-30T20:17:11.910 |

MyTube is a self-hosted downloader and player for several video websites. Prior to version 1.10.3, backend video access does not enforce the visitor role's intended public-only restriction when `loginEnabled=true` and a visitor password is configured. The frontend filter in `VideoContext.tsx` is only client-side, `roleBasedAuthMiddleware.ts` allows all visitor GET requests, and `storageService/videos.ts` performs `getVideos()` and `getVideoById(id)` queries without checking the caller's role or `visibility`. A visitor can enumerate `/api/videos` or request `/api/videos/:id` to retrieve hidden `visibility`=0 records, exposing titles, `sourceUrl` values, `videoPath` values, subtitle paths and `thumbnailPath` values. The `serveMountVideo()` path also serves mounted video files without `visibility` checks. Leaked paths work against unauthenticated `/videos/*` and `/subtitles/*` routes, allowing media downloads without credentials. The RSS visitor feed already filters `visibility`=1 content and is not the affected query path. Default loginEnabled=false single-user deployments are unaffected by this role-boundary issue because all callers are owner-equivalent. This issue is fixed in version 1.10.3.

### CVE-2026-119337

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-30T20:17:08.447 |

RAGFlow is an open-source RAG (Retrieval-Augmented Generation) engine. From 0.25.2 until 0.27.3, POST /api/v1/agents/chat/completions invokes completion_openai and returns through the openai-compatible branch before UserCanvasService.accessible() checks whether the caller may access the requested agent. An authenticated user who knows another user's private agent UUID can execute that Only me workflow and read its output across the user or tenant boundary; configured tools may also cause side effects, but stronger impacts were not demonstrated. This issue is fixed in version 0.27.3.

### CVE-2026-119331

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-200;CWE-346` |
| Published | 2026-10-30T20:17:07.133 |

Ladybird is a truly independent web browser. Prior to the c0d68bddf3e3616e5173835f0f4c155ee9700d91 commit, CSSStyleSheet.cssRules, insertRule(), and deleteRule() in Libraries/LibWeb/CSS/CSSStyleSheet.cpp did not enforce the stylesheet origin-clean flag with the required SecurityError, even though cross-origin imported stylesheets were correctly marked non-origin-clean. A malicious page could read parsed rules from a stylesheet loaded without CORS and could insert or delete rules in the victim stylesheet, bypassing the Same-Origin Policy. Reading could expose selectors, generated content, feature markers, or other sensitive rule text, while mutation could alter page visibility or layout. The issue does not provide memory corruption, code execution, or persistence after the attacker page closes. This vulnerability is fixed by commit c0d68bddf3e3616e5173835f0f4c155ee9700d91.

### CVE-2026-116252

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88;CWE-522;CWE-918` |
| Published | 2026-10-30T20:17:05.473 |

pgAdmin 4's materialized view refresh passed the target database's name to psql's --dbname argument unchanged. libpq treats a --dbname value containing "=" (or a postgresql:// URI) as a full connection string, whose keywords override the host, port and other settings pgAdmin had supplied. A database whose name is such a string, which any role with CREATEDB can create, therefore redirected the psql process pgAdmin starts for the refresh to a host and port of the creator's choosing, and the connecting user's saved server password was presented to that endpoint. It also let the pgAdmin host be made to open connections to arbitrary addresses.

The same weakness was fixed for Backup, Restore, Maintenance and Import/Export Data in earlier releases (CVE-2026-86862); the materialized view refresh was the remaining caller. The fix routes the name through the same database_conninfo() helper, so libpq treats it strictly as a database name.

This issue affects pgAdmin 4: before 9.19.

### CVE-2026-116247

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522;CWE-1188` |
| Published | 2026-10-30T20:17:04.750 |

When a server in pgAdmin 4 had no password file, client certificate or client key configured, or the configured one could not be found, pgAdmin left the parameter out of the connection and libpq fell back to the defaults of the operating-system account running pgAdmin: ~/.pgpass, ~/.postgresql/postgresql.crt and postgresql.key, or PGPASSFILE, PGSSLCERT and PGSSLKEY. In server mode any user could therefore connect to a server with the service account's saved passwords or client certificate, and supplying only a copy of its public certificate was enough for libpq to pair it with the service account's private key. A pg_service.conf entry, or a maintenance database name read as a connection string by pg_dumpall, could bring the same files back for the utilities.

The fix gives each of these parameters a value in server mode, the user's own file or otherwise a path that can never be opened, in the connection string, in the environment of the utilities and in the --dbname connection string that ranks above a service entry. Desktop mode is unchanged.

This issue affects pgAdmin 4: before 9.19.

### CVE-2026-116245

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522;CWE-862` |
| Published | 2026-10-30T20:17:04.467 |

libpq looks a connection service up in the service file of the operating-system account running pgAdmin 4, and an entry there can hold a password or name a password file or client certificate. In server mode any user could set a server's Service, or a "service" connection parameter, to one of those entries and connect with its credentials. A PGPASSWORD or PGSERVICE variable set for that account was likewise used by libpq for every connection without a value of its own and passed on to the utilities, and pg_dumpall read a maintenance database name such as "service=..." as a connection string.

The fix adds the SERVER_MODE_ALLOWED_SERVICES setting, empty by default: in server mode only a listed service can be used, the servicefile parameter is refused, and PGPASSWORD and PGSERVICE are removed from pgAdmin's environment at startup. The allowlist is checked again on the final connection string, and the pg_dumpall database name is wrapped as a connection string.

This issue affects pgAdmin 4: before 9.19.

### CVE-2026-116244

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522;CWE-1188` |
| Published | 2026-10-30T20:17:04.327 |

When a pgAdmin 4 connection was not meant to use a Kerberos user's delegated credentials, pgAdmin removed KRB5CCNAME from its environment, so the Kerberos library fell back to the default credential cache, or a client keytab, of the operating-system account running pgAdmin. libpq then answered any server that asked for GSSAPI authentication with that account's ticket, whatever user name the pgAdmin user gave, so in server mode any user could connect as the service account's Kerberos principal; gssencmode=disable did not prevent it. On Windows, SSPI used the service account's logon in the same way. psql was also started with pgAdmin's environment, which could hold another user's credential cache while that user was connecting.

The fix points KRB5CCNAME and KRB5_CLIENT_KTNAME at a file that cannot exist except while a Kerberos-authenticated user connects with Kerberos, and gives every other connection, psql and the utilities require_auth=!gss,!sspi and gssencmode=disable, checked on the final connection string. require_auth needs libpq 16 or later.

This issue affects pgAdmin 4: before 9.19.

### CVE-2026-116242

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522;CWE-1188` |
| Published | 2026-10-30T20:17:03.983 |

pgAdmin 4 opens SSH tunnels with the sshtunnel library but gave it neither host_pkey_directories nor ssh_config_file, so it always loaded the unencrypted private keys in ~/.ssh of the operating-system account running pgAdmin, read that account's ~/.ssh/config (IdentityFile, User, HostName, ProxyCommand) for the tunnel host, and could use its ssh-agent. In server mode any user could therefore configure a tunnel to a host that accepts the service account's key, with no credentials of their own or with an identity file that did not exist in their storage, and reach it as that account.

The fix makes tunnels in server mode use only the identity file or password the user configured: the service account's keys, configuration and agent are no longer used, and an identity file that cannot be found in the user's storage is reported instead of falling back to ~/.ssh. Desktop mode is unchanged.

This issue affects pgAdmin 4: before 9.19.

### CVE-2026-116240

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-367` |
| Published | 2026-10-30T20:17:03.383 |

In server mode pgAdmin 4 validates a path into the user's storage directory with check_access_permission(), which builds the absolute path with get_abs_path(). Several callers then acted on a path they built differently, so the path checked and the path used could name different files:

- Opening a file in the Query Tool, the Google client secret and, on Windows, Import/Export Data, Backup, Restore and saving a file joined the path to the storage directory after stripping leading slashes and backslashes. On POSIX a path checked as a name inside storage could become an absolute path once stripped, so any file the pgAdmin account can read could be opened; on Windows a path naming a drive discarded the storage directory, so these could read, or write, outside it.
- Listing a folder decoded the path a second time after the check, so a folder named like an encoded "..", which a user can create, listed any directory on the host.
- Download, delete, rename and the file-exists check appended the path to the storage directory without a separator, so in a deployment where one user's storage directory name is a prefix of another's, another user's files could be read, deleted or moved; download also checked the path appended to itself.
- Creating a folder could create one in another user's directory.

The fix makes check_access_permission() return the path it checked and every caller act on that path, decodes folder paths once, and opens, deletes and renames files relative to directories opened from the storage directory without following symbolic links. Desktop mode is not affected.

This issue affects pgAdmin 4: before 9.19.

### CVE-2026-94175

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T19:20:19.250 |

Unauthenticated Cross Site Scripting (XSS) in All In One Login <= 2.4.1 versions.

### CVE-2026-54855

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T19:18:26.240 |

Unauthenticated Cross Site Scripting (XSS) in Profile Builder <= 4.0.5 versions.

### CVE-2026-48201

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T19:18:25.347 |

Unauthenticated Cross Site Scripting (XSS) in Fast Velocity Minify <= 3.5.7 versions.

### CVE-2026-39786

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T19:18:24.730 |

Unauthenticated Cross Site Scripting (XSS) in BA Book Everything <= 1.8.33 versions.

### CVE-2026-28160

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T19:18:23.873 |

Unauthenticated Cross Site Scripting (XSS) in VikRentCar <= 1.4.10 versions.

### CVE-2026-116851

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T19:18:14.877 |

Unauthenticated Cross Site Scripting (XSS) in eCommerce Product Catalog <= 3.6.5 versions.

### CVE-2026-116847

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T19:18:14.613 |

Unauthenticated Cross Site Scripting (XSS) in Mang Board WP <= 2.4.6 versions.

### CVE-2026-116405

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T19:18:14.053 |

Unauthenticated Cross Site Scripting (XSS) in VikRentCar <= 1.4.9 versions.

### CVE-2026-105077

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T19:17:58.637 |

Unauthenticated Cross Site Scripting (XSS) in Ad Inserter <= 2.8.19 versions.

### CVE-2026-119710

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-30T16:17:54.063 |

PipesHub 0.3.0 before 0.10.0 contains an event type injection vulnerability that allows authenticated users with only the crawl:write scope to delete connectors by injecting into the :connector path segment. Attackers can send a :connector value like web.delete to the schedule route, bypassing connector:delete and lock checks to remove connector instances and purge record embeddings.

### CVE-2026-119708

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-30T16:17:53.737 |

abp-next-admin 10.4.0 through 10.7.0 contains a cross-tenant authorization bypass in the BlobManagement download-by-name endpoint, letting authenticated users read other tenants' files. Attackers supply a victim tenantId in the request path, causing DownloadByNameAsync to switch tenant context and return blobs stored by that tenant.

### CVE-2026-119707

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-30T16:17:51.970 |

SonicJS through 3.0.0 contains a missing authorization vulnerability in the /api/:collection and /api/content write routes that only check coarse role labels. Authenticated authors or editors can use a bearer JWT or API key to create, modify, publish, or soft-delete other users' documents, bypassing document ACLs and administrator deny overrides.

### CVE-2026-119289

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-30T16:17:43.013 |

Zuke is a code-first, strongly typed build automation system for Deno. Prior to 1.10.0, the @zuke/gh githubWorkflow(...) gate correlates a dispatched workflow run using only a display-title marker that is visible in the workflow run list and can be copied by another dispatcher. In configurations where the external workflow repository grants workflow_dispatch permission to a party not equally trusted by the releasing repository, an attacker can dispatch a run with the marker and cause the gate to adopt its conclusion without verifying the event, ref, or creation window. A passing substituted run can authorize an unvalidated release, while a failed or cancelled run can block a valid release, and the persisted adopted run ID preserves the substitution across build resume. This issue is fixed in version 1.10.0.

### CVE-2026-119649

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-30T15:16:48.347 |

Orchard CMS 1.10.3 through 1.11 contains an improper authorization vulnerability in MediaLibraryService.CheckMediaFolderPermission() that allows authenticated Authors and Contributors to access other users' media. Attackers can display, clone, and delete other users' media items by content id and delete arbitrary media folders via FolderController.Delete().

### CVE-2026-119645

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-30T15:16:47.710 |

ZenTao PMS through 22.6 contains a missing authorization vulnerability in doc::ajaxGetDoc() that allows authenticated users to read documents without checkPrivDoc() access checks. Low-privilege attackers can enumerate sequential document ids to retrieve body and draft content of private documents and restricted library, product, project, or team documents.

### CVE-2026-62965

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-30T21:17:14.993 |

SABnzbd is an open source automated Usenet download tool. Prior to 5.1.0Beta3, orphan-job management in `sabnzbd/api.py` accepts the user-controlled `value` parameter without path confinement before `os.path.join()` with `download_dir`. An absolute path discards that base directory. An attacker with a valid API key can invoke `mode=status` with `name=delete_orphan` to reach `_api_delete_orphan` and `remove_all()` in `sabnzbd/filesystem.py`, which uses `shutil.rmtree()` for recursive deletion. The advisory also identifies `_api_add_orphan` and `_api_delete_all_orphan` as affected by the path-validation issue, while its concrete arbitrary-deletion trace is through `_api_delete_orphan`. The API key is stored in plaintext in `sabnzbd.ini`. The attacker can delete files or directories writable by the SABnzbd process, including configuration, queue data, and downloads, but system files outside the regular user's ownership are not affected. This issue is fixed in version 5.1.0Beta3.

### CVE-2026-116246

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:P/VC:H/VI:N/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-214;CWE-526` |
| Published | 2026-10-30T20:17:04.603 |

To pass a server's password to psql and to the utilities pgAdmin 4 runs as background processes, the server manager wrote it into pgAdmin's own process environment: as PGPASSWORD for the PSQL tool, and under a per-process variable for a utility. Nothing removed it afterwards. pgAdmin's environment is shared by every user's requests and copied into every process it starts, so in server mode another user's later PSQL session or utility inherited the password, and libpq used PGPASSWORD for any connection made without a password of its own, letting one user connect with another user's saved password.

The fix puts the password only into the environment built for the process that needs it and starts psql with a copy of pgAdmin's environment instead of the environment itself.

This issue affects pgAdmin 4: before 9.19.

### CVE-2026-84243

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-30T18:18:13.650 |

The gettext family of functions in the GNU C Library version 2.0 and later accept LANGUAGE environment variable entries that contain '/' or that are equal to "..", unless the program is setuid or setgid (AT_SECURE).  An attacker who can set LANGUAGE in the environment of a program that uses gettext can make it load a message catalog (.mo file) from an arbitrary location in the file system.  A crafted .mo file can crash the program through out-of-range offsets, or supply translations whose format directives do not match the arguments passed by the program.  That causes undefined behaviour in the printf family of functions and may allow arbitrary code execution with the privileges of the program.  The safety of message catalogs relies on them being installed in trusted, read-only locations, and the directory traversal bypasses this.

The fix for CVE-2014-0475 rejects ".." path components in locale names passed to setlocale or taken from the LC_ALL, LC_* and LANG environment variables.  gettext reads LANGUAGE directly and appends each colon-separated entry to the message catalog directory, so that fix did not cover LANGUAGE.

LANGUAGE is only used when the LC_MESSAGES locale is not "C", "C.<encoding>" or "POSIX", so the attacker must also be able to select another installed locale, for example through LANG or LC_ALL.  Exploitation also requires that the attacker can place the crafted file in a location readable by the target program, and that the environment crosses a trust boundary without the program running as AT_SECURE.  An example is an SSH server that accepts LANGUAGE and LANG from clients through the AcceptEnv directive and restricts an account to a forced command; the attacker may use this to escape the restriction.

### CVE-2026-119288

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-30T16:17:42.873 |

Zuke is a code-first, strongly typed build automation system for Deno. Prior to 1.51.0, @zuke/core launches resolved Windows .cmd and .bat shims by prepending cmd /c, causing cmd.exe to reparse a command line assembled with C-runtime quoting rules. A build running on Windows that resolves a tool from node_modules/.bin and passes attacker-influenced text containing an unquoted &, |, or ^ metacharacter can execute an additional attacker-chosen command in the build's context with access to its credentials. POSIX platforms are not affected. This issue is fixed in version 1.51.0.
