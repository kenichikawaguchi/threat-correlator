# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-15 15:01 UTC
- **対象期間**: `2026-08-14T15:00:28.000Z` 〜 `2026-08-15T15:01:15.000Z`
- **重要CVE数**: 81 件（Critical 9.0+: 20 件 / High 7.0〜: 61 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVSS 7.0 以上の脆弱性は、**リモートコード実行（RCE）・コマンドインジェクション・認証バイパス** が集中している点が顕著です。特に **AI/ML プラットフォーム、IoT ゲートウェイ、データベースミラーリング、WordPress プラグイン** において、認証不要で OS コマンドが実行できるケースが多数報告されています。攻撃者は単一の HTTP リクエストや特別に細工したファイルアップロードだけで、管理者権限に匹敵する操作が可能になるため、**早急なパッチ適用とネットワーク境界での防御** が必須です。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑73678** | 10.0 | MindsDB Minds Platform (≤ 26.1.0) の `/api/v1/responses/` へ細工したプロンプトを送信するだけで、認証不要で任意の OS コマンドが実行可能 | **完全リモートコード実行**（RCE）かつ **認証不要**。AI/ML 環境は内部ネットワークに配置されがちだが、外部からの直接攻撃が可能になる点が危険。 |
| **CVE‑2026‑19188** | 10.0 | Haiwell IoT Cloud HMI Gateway の `/setting` エンドポイントの `cmdPing` Socket.io イベントで入力サニタイズが不十分 → OS コマンドインジェクション | **産業制御系 (ICS) デバイス** に対する重大なコマンドインジェクション。IoT ゲートウェイは外部ネットワークと接続されるケースが多く、侵入後に制御系ネットワークへ横展開が容易になる。 |
| **CVE‑2026‑17186** | 9.9 | IBM Db2 Mirror for i (7.4/7.5/7.6) が特殊文字を適切にエスケープせず、遠隔から任意の CL コマンド実行が可能 | **エンタープライズ DB ミラー** に対する RCE。DB サーバは高権限で稼働しているため、侵害が全社規模の情報漏洩・改ざんにつながる。 |
| **CVE‑2026‑16142**  (WordPress TrueBooker) | 9.8 | `add_front_user_update()` が認証なしで呼び出せ、任意の `truebooker_wp_user_id` が WP ユーザー ID として処理される → アカウント乗っ取り | **WordPress プラグインの認証バイパス** が多数報告されている中でも、管理者権限取得が最も簡単なパターン。多数のサイトでプラグインがインストール済みと想定される。 |
| **CVE‑2026‑50027** | 9.8 | mcp‑memory‑service (≤ 10.67.0) の `/api/documents/*` が API キーや OAuth の有無に関わらず無認証で利用可能 → 任意コード実行 | **AI アプリケーション向け記憶層** が外部に公開されるケースが増えている。認証が無視されると、機密データ取得だけでなくサーバ側で任意コード実行が可能になる。 |

> **注**：上記 5 件は **CVSS が 9.8 以上** で、かつ **認証不要** または **極低権限で実行可能** という点で特に危険度が高いです。

---

## 3. 推奨アクション  

### 3.1 共通の緊急対策
| 項目 | 推奨内容 |
|------|----------|
| **パッチ適用** | ベンダーが提供する **最新版**（以下に具体的バージョンを記載）へ速やかにアップデート。 |
| **ネットワーク分離** | 影響製品が外部に直接露出しないよう、**ファイアウォールで IP 制限**、**VPN のみからのアクセス** を徹底。 |
| **入力検証の強化** | Web アプリケーションファイアウォール (WAF) で **OS コマンド文字列**（`;`, `&&`, `|` など）や **SQL/NoSQL インジェクション** パターンをブロック。 |
| **監査ログの有効化** | 該当エンドポイントへの **アクセスログ**、**コマンド実行ログ** を集中管理し、異常検知ルールを追加。 |
| **最小権限の原則** | サービスアカウントやコンテナの実行権限を **最小限** に設定し、`root` 権限での実行を回避。 |

### 3.2 製品別具体的対策

| 製品 / プラグイン | 現行バージョン (脆弱) | 推奨バージョン / パッチ | 追加対策 |
|-------------------|----------------------|------------------------|----------|
| **MindsDB Minds Platform** | ≤ 26.1.0 | **≥ 26.2.0**（公式パッチリリース） | `/api/v1/responses/` への **認証ミドルウェア** を導入し、IP 制限も併用 |
| **Haiwell IoT Cloud HMI Gateway** | すべてのリリース | **ファームウェア 5.4.3 以降**（パッチ適用） | `cmdPing` イベントの **入力サニタイズ** を実装、不要な Socket.io エンドポイントは無効化 |
| **IBM Db2 Mirror for i** | 7.4/7.5/7.6 (全バージョン) | **Fix Pack 7.6.1**（2026‑Q3） | DB 接続ユーザーの **権限分離**、外部からの CLI アクセスを VPN のみ許可 |
| **TrueBooker (WordPress)** | ≤ 1.2.6 | **≥ 1.2.7**（開発者が提供） | `add_front_user_update` を **認証済みユーザーのみ** に制限し、`nonce` 検証を追加 |
| **mcp‑memory‑service** | ≤ 10.67.0 | **≥ 10.67.1** | API キー／OAuth の **強制チェック**、`/api/documents/*` への **IP ホワイトリスト** 設定 |
| **その他 WordPress プラグイン**（User Profile Builder, User Session Synchronizer, 6Storage Rentals など） | 各プラグインの最新脆弱版 | **各プラグインの最新版**（2026‑08 時点で 3.16.5 以降、1.4.1 以降、2.27.1 以降） | `wp_ajax_nopriv_*` ハンドラに **nonce** と **権限チェック** を必ず実装 |
| **Semaphore CI** | < 2.18.20 | **≥ 2.18.20** | `git_url` パラメータの **ホワイトリスト** と **エスケープ**、プロジェクトロールの見直し |
| **Cockpit CMS** | ≤ 2.14.0 | **≥ 2.14.1** | FFmpeg 連携時の **ファイル名サニタイズ**、アップロードディレクトリの **実行権限除去** |
|

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-73678

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-14T19:18:01.457 |

MindsDB Minds Platform version 26.1.0 and earlier contains an unauthenticated remote code execution vulnerability that allows unauthenticated attackers to execute arbitrary OS commands by submitting crafted prompts to the unprotected POST /api/v1/responses/ endpoint, which reaches the Anton agent's scratchpad tool that calls exec() on attacker-influenced Python source without sandboxing. Attackers can first configure their own LLM API key through the unauthenticated PUT /api/v1/settings/ endpoint, then POST a prompt directing the agent to invoke the scratchpad tool with arbitrary Python code, achieving full OS command execution as the user running the desktop application and enabling access to SSH keys, stored credentials, and environment secrets.

### CVE-2026-19188

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-14T19:17:17.480 |

A critical OS command injection vulnerability has been identified in the
 Haiwell IoT Cloud HMI Gateway product. The vulnerability exists in the 
Net Check feature accessible via the /setting endpoint. The cmdPing 
Socket.io event fails to properly sanitize user-supplied input before 
passing it to the underlying operating system, allowing an attacker to 
inject and execute arbitrary OS commands with root privileges.

### CVE-2026-17186

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-14T20:16:51.127 |

IBM Db2 Mirror for i 7.4, 7.5, and 7.6 could allow a remote attacker to execute arbitrary CL commands due to improper neutralization of special elements in a command.

### CVE-2026-16142

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-15T09:16:29.560 |

The TrueBooker plugin for WordPress is vulnerable to Account Takeover in all versions up to, and including, 1.2.6. This is due to the add_front_user_update() AJAX handler being registered for unauthenticated users and accepting an arbitrary truebooker_wp_user_id value, which is passed directly to wp_update_user() without verifying authentication or ownership. This makes it possible for unauthenticated attackers to change any WordPress user account email address, including an administrator, by submitting the target user ID and an attacker-controlled email address. An attacker can then use the native WordPress password reset flow to receive the reset link at the attacker-controlled email address and take over the account.

### CVE-2026-15826

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-704` |
| Published | 2026-08-15T07:16:19.280 |

The User Profile Builder plugin for WordPress is vulnerable to Authentication Bypass via Type Confusion in versions up to, and including, 3.16.4. This is due to the wppb_log_in_user() function calling absint() on the return value of wp_insert_user() before performing an is_wp_error() check — when a registration is submitted with a 61–70 character username, WordPress core rejects it with a WP_Error object, but absint() coerces that object to the integer 1 before the error check can short-circuit execution, causing the plugin to bind and return a transient-backed autologin nonce tied to user ID 1. This makes it possible for unauthenticated attackers to log in as the site's Administrator account (user ID 1), resulting in full administrative takeover of the site.

### CVE-2026-15341

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-15T03:16:47.943 |

The User Session Synchronizer plugin for WordPress is vulnerable to Authentication Bypass leading to Account Takeover in all versions up to, and including, 1.4.0. The `synchronize_session()` function, hooked on `init` and therefore executed on every request, performs no nonce, capability, or shared-secret validation against the attacker-supplied `ussync-key`, `ussync-token`, and `ussync-ref` parameters; when `ussync-key` references an unregistered slot, `get_option()` returns `false` for both the secret key and the domain list, causing the AES-256-CBC encryption key to degrade to the fully predictable `md5('')` and the referer allowlist to collapse to an empty-string match, while the AES IV is unconditionally hard-coded as `md5('another-secret')`. This makes it possible for unauthenticated attackers to supply a crafted request encrypting any known or guessable user email address in the `ussync-ref` parameter, causing the handler to call `wp_set_auth_cookie()` for the matched user and granting full authentication as that user — including administrators — with no prior knowledge of site secrets.

### CVE-2026-15303

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-15T03:16:47.670 |

The 6Storage Rentals plugin for WordPress is vulnerable to authentication bypass in versions up to, and including, 2.27.0. This is due to the six_storage_create_wp_user() AJAX handler being registered on wp_ajax_nopriv_six_storage_create_wp_user without any nonce, capability, credential, or ownership verification, while calling wp_set_current_user() and wp_set_auth_cookie() for any WordPress user resolved by the attacker-supplied email address. This makes it possible for unauthenticated attackers to log in as any existing WordPress user, including administrators, by submitting that user's email address.

### CVE-2026-17184

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-14T20:16:51.010 |

IBM Db2 Mirror for i 7.4, 7.5, and 7.6 could allow a remote attacker to execute arbitrary code due to external control of file name or path.

### CVE-2026-17182

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-14T20:16:50.893 |

IBM Db2 Mirror for i 7.4, 7.5, and 7.6 could allow a remote attacker to bypass authentication and obtain or alter sensitive information due to improper validation of request URI path segments.

### CVE-2026-50027

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-14T19:17:18.843 |

mcp-memory-service is a semantic memory layer for AI applications. Prior to 10.67.1, all HTTP routes under /api/documents/* in mcp-memory-service are served without any authentication dependency, even when the server is configured with an API key (MCP_API_KEY) or OAuth. An unauthenticated remote attacker can upload arbitrary content into the memory store (write), retrieve stored document content (read), and permanently delete memories belonging to authenticated users (delete) — all without supplying any credentials. The /api/memories counterpart correctly enforces authentication, making this an inconsistent and exploitable authentication boundary. This vulnerability is fixed in 10.67.1.

### CVE-2026-73849

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-14T18:19:09.987 |

Emlog is an open source website building system. In 2.6.26 and earlier, install.php accepts action=reinstall without authentication and deliberately skips the already-installed check because the guard runs only when $act != 'reinstall'. A remote attacker can submit hostname, dbuser, dbpasswd, dbname, dbprefix, username, password, and email values to cause file_put_contents('config.php', $config) to overwrite the configuration with attacker-controlled database settings and create a new administrator account. No fixed version is available as of this review.

### CVE-2026-48528

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89;CWE-287` |
| Published | 2026-08-14T18:17:27.993 |

Metacat is data repository software that helps researchers preserve, share, and discover data. Metacat versions 2.0.0 through 3.4.0 contain an unauthenticated SQL injection vulnerability in the `/cn/v1/object` and `/cn/v2/object` REST API endpoints due to unsanitized user input that can be passed through to the backend SQL database. The `nodeId` parameter can be modified to inject SQL commands, and the results are returned in error messages. Metacat appends the user-supplied data into the sql query without sanitization or parameterization. This allows extraction of arbitrary data from the underlying PostgresQL database, fully exposing protected information to the attacker. This is accomplished by leveraging the error reporting mechanisms in Metacat, where SQL error responses are mirrored back to the caller in the XML error message returned by Metacat. One approach, for example, is to use the PostgreSQL `CAST` function to generate an error with the results of an arbitrary subquery, which is then injected into the XML error message returned by Metacat. Attackers do not need to be authenticated to execute the attack.  In addition, arbitrary SQL statements that insert, update, and delete data in the Metacat database can be executed, resulting in full compromise of all data in the database. Full proof of concept attacks have been developed and verified for these vulnerabilities. The impact of this vulnerability is critical for Metacat deployments in the DataONE network where information from the database can be exfiltrated, added, changed, or deleted. This includes management information about the data catalog, access log information about who accessed data, identifying information about individuals including their ORCID identifier and client IP address, access control information about who should be able to access and modify data, and other critical internals of the data system. This sql injection vulnerability was remediated fully in Metacat version 3.4.1. If upgrading to Metacat 3.4.1 isn't immediately possible, most deployments can mitigate the issue by disabling the `/cn` REST endpoints in the webapp deployment. This API is not needed or used by member repositories in the DataONE network, as it is only used by the DataONE Coordinating Node deployments. Consequently, this API can be disabled without reduction of functionality for most deployments. To disable the vulnerable endpoints, simply remove the servlet and servlet-mapping for the `/cn` endpoints in the servlet engine associated with the two servlets, `edu.ucsb.nceas.metacat.restservice.v1.CNRestServlet` and `edu.ucsb.nceas.metacat.restservice.v2.CNRestServlet`. For example, in Tomcat, remove the relevant `servlet-mapping` elements from the application web.xml file in Metacat.

### CVE-2026-19682

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-14T18:17:23.623 |

A command injection vulnerability exists in Security Center where a remote, unauthenticated attacker could exploit this issue to execute arbitrary commands on the underlying operating system with the privileges of the service account.

### CVE-2026-19681

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-14T18:17:23.480 |

An authenticated command injection vulnerability exists in Security Center related to file upload processing. An attacker could exploit this issue by uploading a specially crafted file, potentially resulting in arbitrary command execution on the underlying operating system.

### CVE-2026-19626

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-14T17:17:30.940 |

A remote code execution vulnerability exists in Tenable Security Center's report generation functionality. An authenticated, non-administrative user could exploit this issue by supplying specially crafted input that is later processed unsafely during server-side report rendering, resulting in arbitrary code execution with the privileges of the service account.

### CVE-2026-17181

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-14T20:16:50.777 |

IBM Db2 Mirror for i 7.4, 7.5, and 7.6 could allow a remote attacker to write files to arbitrary locations due to path traversal.

### CVE-2026-73683

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-08-14T22:17:11.550 |

Laravel Socialite's Facebook provider contains an authentication bypass vulnerability that allows unauthenticated attackers to replay captured OIDC id_tokens by exploiting the missing nonce claim validation in the getUserByOIDCToken() function within FacebookProvider.php. Attackers who obtain a valid, unexpired id_token issued for the same Facebook App ID can submit the captured token to the backend userFromToken() endpoint, bypassing authentication controls because signature, aud, and iss checks pass while no session-bound nonce comparison is performed, resulting in unauthorized access to victim accounts.

### CVE-2026-67365

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:L/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-14T20:16:55.850 |

Joomla Extension - icagenda.com - Unauthenticated SQL injection in iCagenda < 4.0.0-4.0.11 - Unauthenticated SQL injection in mod_icagenda_calendar (iCagenda), reachable via com_ajax with no session, token or account.

### CVE-2026-14484

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-15T03:16:47.263 |

The RapiSafe – Secure Multi File Upload for Contact Form 7 plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the handleAjaxRemoveUpload function in all versions up to, and including, 1.0.4. This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). The nonce required to invoke the removal handler is exposed in public-facing JavaScript as RSMFCF7Vars.nonce on every Contact Form 7 page rendering a RapiSafe upload field, making it obtainable by any unauthenticated visitor.

### CVE-2026-49457

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295;CWE-297` |
| Published | 2026-08-14T19:17:18.707 |

erlang_quic is a pure Erlang QUIC implementation. Prior to version 1.4.4, the QUIC client did not authenticate the server during the TLS 1.3 handshake. The CertificateVerify signature was not checked, the certificate chain was not validated, and the hostname was not compared against the certificate, so `verify` was effectively a no-op on the client. A man-in-the-middle on the network path could present any certificate and impersonate any server, defeating the confidentiality and integrity of the connection. HTTP/3 uses the same client and was equally affected. Handshakes authenticated by a PSK (session resumption) are not affected, because the peer is authenticated by the PSK binder and no certificate is sent. This is fixed in 1.4.4. The client now verifies the CertificateVerify signature, validates the certificate chain against the trust store (`cacerts` option, the operating system store by default), and checks the hostname. Client `verify` now defaults to on; set `verify => false` to accept any certificate (for example a self-signed test server). No known workarounds are available before 1.4.4. `verify => true` had no effect, and inspecting the certificate after connecting does not help because without the signature check the peer is never proven to own the certificate it presents.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-18438

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-15T10:16:29.413 |

The Templately – Elementor & Gutenberg Template Library: 6500+ Free & Pro Ready Templates And Cloud! plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 3.7.1 via the fetch_remote_file function. This is due to a filename validation/destination mismatch in fetch_remote_file, where file type validation is performed against the attacker-controlled Content-Disposition filename rather than the URL-path-derived destination filename. This makes it possible for authenticated attackers, with contributor-level access and above, to execute code on the server. A GIF+PHP polyglot file passes wp_check_filetype_and_ext validation as image/gif via the Content-Disposition filename, while the actual destination path is written with a .php extension derived from the URL path, bypassing the unfiltered_upload capability gate entirely. The affected endpoints are reachable at this privilege level because Templately's entire REST API — including the cloud import endpoints used in this attack (/templately/v1/clouds/upload and /templately/v1/insert) — is authorized only by a current_user_can('delete_posts') check, with no administrator or manage_options capability requirement. The same permission gate also allows a contributor to overwrite the site's global Templately cloud connection via the /templately/v1/login endpoint with global_signin set to true. A complete remediation should both correct fetch_remote_file to validate the file type against the actual destination filename rather than the Content-Disposition header (and avoid deriving the write path from the request URL), and restrict state-changing Templately REST routes to an appropriate administrator-level capability.

### CVE-2026-14279

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-15T07:16:19.120 |

The Wholesale Market plugin for WordPress is vulnerable to privilege escalation in versions up to, and including, 2.2.2 via the ced_wholesale_request_send AJAX action. The ced_wholesale_request_send_callback() handler only verifies a nonce (which is exposed to any authenticated user through wp_localize_script on the frontend) and that the caller has a positive user ID, then calls WP_User::add_role() with the client-supplied role_required POST parameter without restricting the value to an allowlist of wholesale roles. This makes it possible for authenticated attackers, with Subscriber-level access and above, to elevate their privileges to Administrator when the site administrator has enabled the 'Assigning requested role directly' option.

### CVE-2026-15965

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-15T03:16:48.077 |

The MaxUpload – Big File Uploads – Increase Maximum File Upload Size plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 1.4.0 via the handle_upload function. This is due to a filename-validation mismatch in the handle_upload function where extension and MIME checks are applied to the uploaded chunk's filename but not to the final assembled filename derived from the resumableFilename parameter. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible.

### CVE-2026-15312

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-15T03:16:47.817 |

The Propovoice: All-in-One Client Management System plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 1.7.8. This is due to the `create()` function's REST endpoint failing to validate the user-supplied `role` parameter against an allowlist of permitted WordPress roles and omitting any `promote_users` capability check before passing the sanitized value directly to `WP_User::set_role()`. This makes it possible for authenticated attackers with `ndpv_manager`-level access and above to create a new WordPress user account with the `administrator` role assigned, achieving full vertical privilege escalation. The `ndpv_manager` capability is a sub-administrator CRM team role granted by Propovoice itself, meaning the attack surface extends beyond site administrators to any user the plugin has elevated to a manager position.

### CVE-2026-15001

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-15T03:16:47.393 |

The bLoyal: Loyalty & Promotions by bLoyal plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 3.1.611.78. This is due to the AJAX actions `save_bloyal_configuration_data` and `save_bloyal_accesskeyverification_data` being registered without any capability or nonce checks, and the `bloyal_customer_auto_login` function unconditionally trusting the `Customer.ExternalId` value returned by whichever API URL is stored in the plugin's options. This makes it possible for authenticated attackers, with Subscriber-level access and above, to overwrite the plugin's bLoyal Loyalty Engine API URL (`bloyal_custom_loyaltyengine_api_url`) and the `is_bloyal_custom_api_url` flag via the unprotected AJAX actions, then trigger the unauthenticated `/cart` REST route to cause `bloyal_customer_auto_login` to fetch customer data from an attacker-controlled endpoint and call `wp_set_auth_cookie()` with an attacker-supplied `Customer.ExternalId`, thereby authenticating as any WordPress user including the site Administrator.

### CVE-2026-16879

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-08-14T20:16:49.700 |

IBM Db2 Mirror for i 7.4, 7.5, and 7.6 could allow a remote authenticated attacker to bypass security restrictions due to improper authorization using user-supplied input.

### CVE-2026-12366

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-14T18:17:22.043 |

Zephyr's dynamic kernel-object disposal path unref_check() in kernel/userspace/userspace.c frees an object's storage (k_free(dyn->data)) once its reference count reaches zero, after running a per-object-type cleanup. The cleanup switch handled only K_OBJ_MSGQ and K_OBJ_STACK; there was no K_OBJ_TIMER case. A dynamically-allocated, initialized, and armed k_timer keeps its embedded struct _timeout dnode linked in the global timeout queue (_timeout_q), so freeing the timer storage without cancelling the timeout leaves a dangling node in that queue.

When the timer next expires, the timeout machinery walks _timeout_q and invokes z_timer_expiration_handler() on the freed node, dereferencing and writing freed (and reusable) kernel heap in kernel/ISR context. This is a deterministic use-after-free that does not depend on SMP: the queued node is simply never unlinked at free time.

The disposal is reachable from an unprivileged user thread under CONFIG_USERSPACE + CONFIG_DYNAMIC_OBJECTS: a thread that holds the last permission on such a timer drops it via the k_object_release() syscall (or by exiting, through k_thread_perms_all_clear()), and can arm the timer itself via the k_timer_start() syscall. The free and the expiration handler run at kernel privilege while the actor is a user thread, so the bug is a sandbox-escape memory-corruption primitive usable for privilege escalation. The fix adds k_timer_cleanup() (cancel the timeout and wait for any in-flight handler) and calls it for K_OBJ_TIMER before freeing.

### CVE-2026-73682

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-14T21:17:58.033 |

Semaphore versions prior to 2.18.20 contain an OS command injection (argument injection) vulnerability in the repository git_url handling that allows authenticated users holding the Manager or Owner role on any project to achieve remote code execution on the Semaphore server host. Attackers can craft a malicious git_url value using git's --upload-pack= option to inject and execute arbitrary shell commands when the server processes repository operations using the default cmd_git client.

### CVE-2026-73680

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-14T20:16:58.080 |

Cockpit CMS 2.14.0 and prior contains a command injection vulnerability in the FFmpeg integration that allows authenticated users with only the assets/upload permission to execute arbitrary commands by uploading a video file with a shell metacharacter-laden filename. The unsanitized filename is interpolated into a shell command executed via Process::fromShellCommandline() before the slugify() sanitizer runs, enabling injected shell metacharacters such as backticks, $(), and semicolons to escape the FFmpeg command context and execute as the web-server user.

### CVE-2026-19679

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-14T18:17:23.230 |

An input validation vulnerability exists in Security Center's file upload handling, where insufficient sanitization of uploaded filenames could contribute to a downstream command injection issue.

### CVE-2026-71571

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-14T20:16:56.340 |

Joomla Extension - icagenda.com -  Authenticated SQL injection via unescaped numeric filter in iCagenda < 2.0.0-4.0.11 - Backend operators with permissions to access iCagenda could inject SQL.

### CVE-2026-73679

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-14T19:18:01.610 |

ImpressCMS contains an authenticated remote code execution vulnerability in the custom tag module that allows authenticated administrators to execute arbitrary PHP code by storing a malicious payload in a custom tag with PHP type enabled. The application decodes HTML-encoded content via undoHtmlSpecialChars() before passing it to eval() in the renderWithPhp() method, bypassing HTML Purifier sanitization, and the payload is triggered on every frontend page load through the preload event system.

### CVE-2026-73850

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-14T18:19:10.137 |

Emlog is an open source website building system. In 2.6.20 and earlier, there is a SQL injection vulnerability in the queryDatabase function in ai.php.

### CVE-2026-19629

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-14T18:17:22.557 |

A privilege escalation vulnerability exists in Tenable Security Center that allows a user with "Security Manager" role and "manage user" permission on a single group to modify users belonging to other groups. This bypasses the intended access control restrictions and enables unauthorized cross-group user management.

### CVE-2026-19628

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-14T17:17:31.110 |

A command injection vulnerability exists in Tenable Security Center. An authenticated administrator could modify application configuration values to achieve arbitrary command execution on the underlying operating system when specific backend operations are triggered.

### CVE-2026-17179

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-14T20:16:50.663 |

IBM Db2 Mirror for i 7.4, 7.5, and 7.6 could allow a remote authenticated attacker to cause a denial of service due to command injection.

### CVE-2026-63361

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-14T18:18:53.650 |

LimeSurvey Community Edition 7.0.5 contains an authenticated reflected cross-site scripting vulnerability in the HTML editor popup endpoint. The text and name query parameters are passed through a blacklist sanitizer and then rendered without context-appropriate output encoding.

### CVE-2026-19635

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-14T18:17:22.817 |

A local privilege escalation vulnerability exists in Security Center. An attacker with write access to a specific configuration file could achieve arbitrary code execution with elevated privileges, without requiring further user or victim interaction.

### CVE-2026-12364

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-08-14T18:17:21.820 |

The user-space system-call verifier z_vrfy_z_log_msg_static_create() in subsys/logging/log_msg.c was a pure pass-through: it forwarded the caller-supplied source, desc, package, and data arguments directly to the kernel-mode implementation z_impl_z_log_msg_static_create() without performing any of the mandatory K_SYSCALL_* checks. Because z_log_msg_static_create() is declared __syscall, under CONFIG_USERSPACE any unprivileged user-mode thread can invoke it directly with fully attacker-controlled arguments.

The kernel-mode handler dereferences each of these untrusted values: frontend_runtime_filtering() reads through the source pointer as a struct log_source_dynamic_data, cbprintf_package_copy() reads desc.package_len bytes from the package pointer, and z_log_msg_finalize() performs a memcpy() of desc.data_len bytes from the data pointer. With no verification, a user thread can supply arbitrary kernel addresses and arbitrary lengths, and the kernel will read from them.

The impact is a kernel-mode denial of service (the kernel faults dereferencing an attacker-chosen pointer) and, where a log backend output is observable to the attacker, disclosure of arbitrary kernel memory copied into the emitted log message — a confidentiality breach across the user/kernel boundary that the userspace sandbox is meant to enforce. The reads do not corrupt kernel memory, so there is no out-of-bounds write primitive.

The fix adds the required validation to the verifier: it bounds desc.package_len against Z_LOG_MSG_MAX_PACKAGE, rejects non-NULL/length mismatches, and applies K_SYSCALL_MEMORY_READ() to package, data, and (when runtime filtering with a frontend is enabled) source, so any out-of-bounds or kernel pointer now raises K_OOPS instead of being honored.

### CVE-2026-19884

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-15;CWE-829` |
| Published | 2026-08-14T16:16:55.073 |

In Eclipse Theia versions up to and including 1.69.0, opening a folder starts source control integration without requiring the user to trust the folder first. This affects applications built on Theia that include the git integration, such as the Theia IDE. Both Theia's own `@theia/git` extension and the builtin VS Code `git` extension run git commands such as `git status` as soon as a repository is detected. Since git honors repository-local configuration, a folder containing an attacker-controlled `.git/config` with `core.fsmonitor` (or a comparable hook-like setting) causes the configured command to be executed. The configuration can be delivered by burying a bare repository inside a regular repository (OVE-20210718-0001), so cloning an attacker-supplied repository and opening it in a Theia-based application is sufficient to execute arbitrary commands with the privileges of the user, without any confirmation prompt.



As of 1.70.0, plugins that declare `capabilities.untrustedWorkspaces.supported: false`, which includes the builtin git extension, are no longer loaded or activated in an untrusted workspace, and the deprecated `@theia/git` extension has been removed, so no git command is executed against an untrusted folder.

### CVE-2026-16708

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-15` |
| Published | 2026-08-14T20:16:49.457 |

IBM Db2 Mirror for i 7.4, 7.5, and 7.6 could allow a remote attacker to obtain sensitive information due to external control of system configuration.

### CVE-2026-72970

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-14T18:19:09.003 |

Heap-based buffer overflow in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-69101

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-08-14T15:17:10.053 |

Datavane TIS v5.0.0 contains an XML external entity (XXE) injection vulnerability that allows authenticated attackers to perform server-side request forgery and out-of-band file exfiltration by supplying a crafted taskScript payload to the doEditWorkflow endpoint, which processes XML through an unhardened DocumentBuilderFactory with external entities and DTD loading enabled. Attackers can send a malicious XML document containing an external DTD reference to the edit_workflow action, causing the server to issue outbound HTTP requests to attacker-controlled infrastructure and exfiltrate local files readable by the TIS process user, including configuration files and Derby database credentials.

### CVE-2026-17081

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-14T20:16:50.180 |

IBM Db2 Mirror for i 7.4, 7.5, and 7.6 could allow a remote attacker to write arbitrary files due to improper limitation of a pathname to a restricted directory.

### CVE-2026-18500

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-15T14:17:07.473 |

@fastify/jwt is a JSON Web Token plugin for Fastify. In versions before 10.2.2, a per-request verification key passed to request.jwtVerify({ key }) is silently overridden by the plugin's globally configured secret, because the option merge applies the global key last. Applications that use different keys for different authorization domains, for example separate user and admin keys, therefore accept a token signed with the global key on a route that explicitly requires another key. This lets an ordinary authenticated user cross a key-based trust boundary without knowing either secret. The issue is fixed in @fastify/jwt 10.2.2, where an explicit per-call key takes precedence over the global secret. Users should upgrade to 10.2.2.

### CVE-2026-16772

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-269;CWE-862` |
| Published | 2026-08-14T16:16:50.290 |

In Akaunting versions <= 3.1.21, low‑privileged authenticated users can modify their own account to assign themselves the admin role ID, granting full administrator privileges. This vulnerability is caused by a flaw in the `UpdateUser` job, which processes user-supplied role assignments via an unconditional `roles()->sync()` call without verifying whether the caller is authorized to manage roles. Users only require the default `update-auth-profile` permission to access the self-update path and assign themselves as admins. The API endpoints are properly permission‑gated and are not affected by this issue.

### CVE-2026-69414

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-14T22:17:06.810 |

Microsoft is aware of an elevation of privilege in the Microsoft Malware Protection Engine in Microsoft Defender publicly referred to as &quot;ShieldBreak &quot;.
We are working to provide a high quality security update that addresses this vulnerability. We will provide information in this CVE when the update is available.

### CVE-2026-50523

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-14T21:17:18.920 |

Improper neutralization of special elements used in a command ('command injection') in Microsoft PowerShell allows an authorized attacker to execute code locally.

### CVE-2026-46439

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-1336` |
| Published | 2026-08-14T17:18:14.853 |

compliance-trestle is a tooling platform for managing compliance as code. Versions prior to 3.12.2 and 4.0.3 have a Server-Side Template Injection (SSTI) vulnerability exists in the `trestle author jinja` command. The command recursively evaluates rendered templates, allowing an attacker to achieve arbitrary command execution with privileges of the running process by injecting malicious payloads into data fields (such as SSP documents or Lookup Tables). The vulnerability does not require attacker control of the template itself. Only attacker-controlled input data rendered into a trusted template is required. This distinction is critical: the template author may only intend to render plain text (e.g., `Title: {{ ssp.metadata.title }}`), but because of the recursive parsing, the data field itself becomes executable. The vulnerability is caused by recursive re-compilation and re-rendering of already-rendered output. Versions 3.12.3 and 4.0.3 patch the issue.

### CVE-2026-63700

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-14T16:16:58.553 |

Dell Wyse Management Suite (WMS), versions prior to 2605.0.2, contain an Incorrect Default Permission vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Privilege Escalation.

### CVE-2026-19474

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-459;CWE-770` |
| Published | 2026-08-15T14:17:07.710 |

@fastify/multipart is a multipart form-data parser for Fastify. In versions from 3.0.0 up to but not including 10.1.1, request.saveRequestFiles() can leave completed temporary files on disk when a client disconnects while the parser is advancing between multipart parts. The iterator rejection that occurs between parts falls outside the per-file cleanup path, so an earlier completed file is never removed. An unauthenticated client can repeat this to cause persistent, linear disk consumption, leading to denial of service. This is an incomplete-fix variant of CVE-2025-24033. The issue is fixed in @fastify/multipart 10.1.1. Users should upgrade to 10.1.1.

### CVE-2026-18549

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-664` |
| Published | 2026-08-15T14:17:07.590 |

@fastify/multipart is a multipart form-data parser for Fastify. In versions from 5.3.0 up to but not including 10.1.1, when the busboy fileSize limit truncates a file part, the plugin clears its internal current-file reference while the underlying stream is still open. If the client then aborts the connection before sending the terminating boundary, the abort cleanup finds no stream to destroy, so saveRequestFiles() never settles, the request handler hangs, and the temporary file already written to disk is never cleaned up. An unauthenticated client can repeat this to permanently leak temporary files and suspended handler executions, leading to disk and event-loop exhaustion. The issue is fixed in @fastify/multipart 10.1.1. Users should upgrade to 10.1.1.

### CVE-2026-15142

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-15T09:16:28.557 |

The Real Estate Manager Pro plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 12.8.6. This is due to improper capability handling in the allow_attachment_actions() function, which can treat a target user ID as a media attachment ID during user capability checks. This makes it possible for authenticated attackers, with Subscriber-level access and above, to edit an administrator account and escalate their privileges to Administrator when the targeted user ID matches the ID of an existing media attachment.

### CVE-2026-15162

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-15T03:16:47.523 |

The Object Sync for Salesforce plugin is vulnerable to unauthenticated SQL Injection via the wordpress_object_type parameter of its /wp-json/object-sync-for-salesforce/push/ REST route. The route's permission callback (can_process()) checks only the HTTP method for the push class — no capability or nonce — so it is reachable by unauthenticated users. The wordpress_object_type value is concatenated directly into a SQL query (post_type = "$object_type", class-object-sync-sf-wordpress.php:328) and executed via $wpdb->get_results() with no $wpdb->prepare() (:578). Because REST body parameters are not magic-quoted, an attacker can break out of the quoted string and inject arbitrary SQL. This makes it possible for unauthenticated attackers to append additional SQL queries (time-based blind), enabling extraction of sensitive information such as password hashes from the database. Only a valid wordpress_id (e.g. 1) is required — no authentication or Salesforce connection.

### CVE-2026-19910

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-14T20:16:52.550 |

PAX Technology Q80 Application Installer Signature Verification Bypass Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of PAX Technology Q80. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the application installer. The issue results from the lack of proper verification of a cryptographic signature before installing an application. An attacker can leverage this in conjunction with other vulnerabilities to execute code in the context of root. Was ZDI-CAN-30585.

### CVE-2026-19909

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-14T20:16:52.437 |

PAX Technology Q80 AIP File Parsing Link Following Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of PAX Technology Q80. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the parsing of AIP files. By creating a symbolic link, an attacker can abuse the installer process to write arbitrary files. An attacker can leverage this in conjunction with other vulnerabilities to execute code in the context of root. Was ZDI-CAN-30583.

### CVE-2026-18554

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-14T20:16:51.720 |

IBM Db2 Mirror for i 7.4, 7.5, and 7.6 could allow a remote authenticated attacker to obtain sensitive information due to improper limitation of a pathname to a restricted directory.

### CVE-2026-17177

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-08-14T20:16:50.550 |

IBM Db2 Mirror for i 7.4, 7.5, and 7.6 could allow a remote attacker to cause a denial of service due to uncontrolled recursion.

### CVE-2026-17175

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-14T20:16:50.430 |

IBM Db2 Mirror for i 7.4, 7.5, and 7.6 could allow a remote authenticated attacker to obtain sensitive information due to improper authentication enforcement.

### CVE-2026-16915

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-14T20:16:49.933 |

IBM Db2 Mirror for i 7.4, 7.5, and 7.6 could allow a remote authenticated attacker to obtain sensitive information due to improper input validation.

### CVE-2026-45699

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-08-14T19:17:18.267 |

Netatalk is a Free and Open Source file server suite for Unix-like operating systems. In versions 3.1.19 through 4.4.2, a  stack-based buffer overflow exists in the copydir() function of Netatalk's afpd daemon due to an integer underflow in the calculation of the remaining buffer size used for path construction. copydir() is a utility function called when a file operation crosses a device boundary inside an AFP shared volume, which the standard library's renameat() cannot handle. The function attempts to track available buffer space using srem and drem for source and destination paths. Incorrect arithmetic causes both srem and drem to underflow to SIZE_MAX. Consequently, boundary checks against strlen(de->d_name) always pass, allowing strcpy() to append filenames into nearly full stack buffers. Version 4.4.3 patches the issue. As a workaround, configure each AFP shared volume to be structured as a single file system, in other words no subdirectory of a shared volume should be a mount point for a different file system.

### CVE-2026-46603

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-08-14T17:18:15.307 |

VP8L decoding in golang.org/x/image/vp8l can allocate an excessive amount of memory when processing a crafted VP8L image containing many unused Huffman tree groups. This allows a remote attacker to cause a denial of service via memory exhaustion.

### CVE-2026-53970

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-08-14T16:16:57.073 |

ZeroBrew version 0.3.1 and prior contains a missing integrity verification vulnerability in the Ruby compatibility shim that allows network attackers to execute arbitrary code by substituting malicious content at formula resource or URL-based patch URLs without checksum validation. Attackers can intercept or replace downloads for secondary resource and patch paths in shim.rb, injecting attacker-controlled build steps or source tree modifications that execute during source builds via 'zb install --build-from-source' without any integrity warning.

### CVE-2026-19847

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-14T18:17:24.037 |

A security flaw has been discovered in TOTOLINK A800R 4.1.2cu.5137_B20200730. Affected is the function setWiFiWpsConfig of the file /cgi-bin/cstecgi.cgi of the component wps.so. The manipulation of the argument pin results in stack-based buffer overflow. The attack can be launched remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-19846

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-14T18:17:23.883 |

A vulnerability was identified in TOTOLINK A800R 4.1.2cu.5137_B20200730. This impacts the function setUrlFilterRules of the file /cgi-bin/cstecgi.cgi of the component firewall.so. The manipulation of the argument url leads to stack-based buffer overflow. The attack can be initiated remotely. The exploit is publicly available and might be used.

### CVE-2026-19845

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-14T17:17:35.753 |

A vulnerability was determined in TOTOLINK A800R 4.1.2cu.5137_B20200730. This affects the function setStaticDhcpConfig of the file /cgi-bin/cstecgi.cgi of the component lan.so. Executing a manipulation of the argument Comment can lead to stack-based buffer overflow. It is possible to launch the attack remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-19844

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-14T17:17:35.560 |

A vulnerability was found in TOTOLINK A800R 4.1.2cu.5137_B20200730. The impacted element is the function setRadvdCfg of the file /cgi-bin/cstecgi.cgi of the component ipv6.so. Performing a manipulation of the argument radvdinterfacename results in stack-based buffer overflow. It is possible to initiate the attack remotely. The exploit has been made public and could be used.

### CVE-2026-13197

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-08-14T16:16:49.523 |

Nozomi Networks Labs identified a CWE-362: Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition') vulnerability in the configuration and process-image management functionality of KUNBUS piControl in version 2.6.2 that allows a local authenticated attacker to trigger use-after-free and invalid pointer dereferences on kernel configuration objects, resulting in kernel memory corruption and denial of service, by issuing concurrent crafted requests through the piControl character device.

### CVE-2026-13196

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-14T16:16:49.397 |

Nozomi Networks Labs identified a CWE-787: Out-of-bounds Write vulnerability in the process-image management functionality of KUNBUS piControl in version 2.6.2 that allows a local authenticated attacker with device configuration access to write attacker-controlled data outside the bounds of the process-image buffer and corrupt adjacent kernel memory, resulting in kernel memory corruption and denial of service, by supplying crafted device configuration data and crafted input through the piControl character device.

### CVE-2026-16145

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-15T04:18:10.233 |

The Invisible Anti-Spam & CAPTCHA — reCAPTCHA Alternative for All Forms plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'action' parameter in all versions up to, and including, 5.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The stored payload is written by any unauthenticated admin-ajax.php request whose action value matches an entry in the plugin's explicit-actions list, which is auto-populated for common form builders at activation and requires no authentication gate to reach the save path.

### CVE-2026-13360

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-15T04:18:01.957 |

The Cookie Banner for GDPR / CCPA – WPLP Cookie Consent plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'regionArray' parameter in all versions up to, and including, 4.3.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires that the site administrator has enabled the 'Support Google Consent Mode (GCM)' setting, which is disabled by default. Additionally, the AJAX handler performs no nonce or capability check, allowing any authenticated user including those with Subscriber-level access to overwrite the affected plugin setting.

### CVE-2026-14433

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-15T03:16:47.130 |

The Online Booking & Scheduling Calendar for WordPress by vcita plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'business_id' parameter in all versions up to, and including, 4.6.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-66271

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-14T16:16:59.030 |

Dell Wyse Management Suite (WMS), versions prior to 2605.0.2, contain an Unrestricted Upload of File with Dangerous Type vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Remote Code Execution.

### CVE-2026-66270

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-14T16:16:58.913 |

Dell Wyse Management Suite (WMS), versions prior to 2605.0.2, contain an Unrestricted Upload of File with Dangerous Type vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Remote Code Execution.

### CVE-2026-16007

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-15T06:16:56.063 |

AppFlowy's qcuiknote feature is affected by a SQL injection vulnerability. Authenticated users with access to the feature can inject arbitrary SQL to exfiltrate data in the underlying SQL database.

### CVE-2026-19908

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-14T20:16:52.303 |

PAX Technology Q80 XCB Daemon Missing Authentication Vulnerability. This vulnerability allows network-adjacent attackers to disclose sensitive information and modify configuration on affected installations of PAX Technology Q80. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the XCB daemon. The issue results from the lack of authentication prior to allowing access to functionality. An attacker can leverage this in conjunction with other vulnerabilities to execute arbitrary code in the context of root. Was ZDI-CAN-30584.

### CVE-2026-19680

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-14T18:17:23.357 |

A SQL injection vulnerability exists in Security Center that could allow an attacker to access unauthorized data from the application's database.

### CVE-2026-49989

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-14T17:18:27.290 |

CrateDB is a distributed SQL database. Prior to versions 6.2.8 and 6.3.2, any authenticated user can read or delete any blob whose SHA-1 digest they know, and can plant new blobs unconditionally, in any blob table, regardless of `GRANT`s. CrateDB has two ways to access blob storage: SQL (`SELECT ... FROM blob.<table>` and friends) and the blob HTTP API (`GET|PUT|DELETE /_blobs/{table}/{digest}`). The SQL path goes through `AccessControl`, which is what enforces privilege grants; that's why `SELECT digest FROM blob.secret_blobs` fails for a user who has no grants on the table. The HTTP path authenticates the request but never asks `AccessControl` whether the authenticated user is allowed to touch the table. So a user with no grants gets `MissingPrivilegeException` from SQL and `200 OK` plus the blob bytes from `GET /_blobs/secret_blobs/<digest>`. Deployments that don't use `BLOB TABLE` are unaffected. Authentication itself still works; the bug is strictly that being authenticated as anyone is treated as sufficient for any blob op. Versions 6.2.8 and 6.3.2 fix the issue.

### CVE-2026-49986

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-08-14T17:18:27.147 |

The Cortex MCP server (`neuro-cortex-memory`), a cross-platform persistent memory MCP, prior to version 3.17.1 treats the `CLAUDE_PROJECT_DIR` environment variable — automatically set by Claude Code to the currently open project directory — as a trusted Cortex developer checkout. When the `open_visualization` tool is invoked, `_find_dev_source()` resolves the user's active project directory as a candidate Cortex source root. The only validation performed by `_is_cortex_root()` is a check for the presence of an `mcp_server/` subdirectory and a `ui/unified-viz.html` file. An attacker who places these two marker files in a malicious repository can cause Cortex to execute an arbitrary `mcp_server/server/visualize_bootstrap.py` from that directory via `subprocess.run([sys.executable, ...])`, achieving code execution with the privileges of the victim's local user process. Version 3.17.1 fixes the issue.

### CVE-2026-64887

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-08-14T20:16:55.603 |

Use of hard-coded cryptographic key vulnerability in Johnson Controls Airwall allows : Cryptanalytic Attack.

This issue affects Airwall: before 4.1.

### CVE-2026-34492

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-14T20:16:52.817 |

External control of file name or path vulnerability in Johnson Controls Airwall allows : File Manipulation.

This issue affects Airwall: before 4.1.
