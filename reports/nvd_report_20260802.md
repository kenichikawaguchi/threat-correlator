# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-01 15:00 UTC
- **対象期間**: `2026-07-31T15:00:30.000Z` 〜 `2026-08-01T15:00:14.000Z`
- **重要CVE数**: 81 件（Critical 9.0+: 23 件 / High 7.0〜: 58 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが **9.0 以上** の高リスク脆弱性が多数報告されています。共通する傾向は、**認証バイパス・情報漏洩・リモートコード実行** が容易に成立する点で、特にオープンソースの管理パネル、WordPress プラグイン、IoT ルータ、Kubernetes 用 Webhook、認証フレームワークに集中しています。多くは「入力検証の欠如」や「暗号設定のデフォルト不備」に起因しており、攻撃者は低権限ユーザーでも管理者権限取得や機密情報取得が可能です。  

---

## 2. 特に注目すべき CVE  

| CVE | 製品・コンポーネント | スコア | 主な影響 | 修正バージョン (公開済み) |
|-----|----------------------|--------|----------|---------------------------|
| **CVE‑2026‑52855** | **Wings (Pterodactyl のサーバー制御プレーン)** | 9.9 (CVSS:3.1) | `{{config.}}` プレースホルダーの処理ミスにより、低権限ユーザーが `config.token`、`config.token_id`、`config.docker.registries` などの機密情報を取得可能。認証情報漏洩 → 完全なサーバー乗っ取りリスク。 | **1.12.3** 以降 |
| **CVE‑2026‑15964** | **WordPress プラグイン “Single Sign On For TNG”** | 9.8 (CVSS:3.1) | `wp_ajax_nopriv_ssoprocess_ajax` が認証なしで呼び出せるため、パスワードリセット機能を悪用し認証バイパスが成立。管理者権限取得が可能。 | **2.0.1** (開発者が提供したパッチ) |
| **CVE‑2026‑67822** | **Tenda W6‑S ルータ (ファームウェア 1.0.0.4(510))** | 9.8 (CVSS:3.1) | `/goform/wifiSSIDset` エンドポイントで `sprintf` が長さチェックなしに 64 バイトバッファへ書き込むスタックベースバッファオーバーフロー。遠隔から任意コード実行が可能。 | **1.0.0.5** (公式ファームウェア) |
| **CVE‑2026‑54725** | **vault‑secrets‑webhook (Kubernetes Mutating Webhook)** | 9.6 (CVSS:3.1) | `vault.security.banzaicloud.io/vault-addr` アノテーションを不正に操作でき、Pod 生成時に任意の Vault シークレットを注入可能。K8s クラスタ全体で機密情報漏洩・権限昇格。 | **1.23.1** 以降 |
| **CVE‑2026‑67336** | **better‑auth (oidcProvider / mcp プラグイン)** | 9.4 (CVSS:4.0) | OIDC プロバイダーが `none` アルゴリズムを許可し、PKCE の plain モードをデフォルトで受け入れるため、署名なしトークンや認可コードの盗聴が可能。トークン偽造による認証バイパス。 | **1.6.11** 以降 |

> **選定理由**  
> - **スコアが最高 (9.9‑9.6)** で、かつ **遠隔からの権限取得や機密情報漏洩** が直接的に可能。  
> - 影響範囲が広く、**インフラ全体 (K8s クラスタ、IoT ルータ、ゲームサーバー管理パネル) や多数の Web サイト** に波及。  
> - ベンダーがすでにパッチをリリースしている点から、**速やかな対策が実行可能** であることも重要です。

---

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
1. **パッチ適用を最優先**  
   - 上記 CVE の修正版がリリース済みの場合は、**直ちにアップデート** してください。  
   - アップデートが遅延する環境は、**ネットワークレベルでのアクセス制御**（IP フィルタリング、WAF ルール）で暫定的に保護します。

2. **機密情報のローテーション**  
   - `config.token` 系や Vault シークレット、OAuth/OIDC トークンなど、漏洩が疑われるシークレットは **すべて再生成** し、古いトークンは無効化してください。

3. **監査ログの強化**  
   - 認証バイパスや不正な API 呼び出しが記録されていないか、**ログ集約・SIEM** でリアルタイム監視を設定。  
   - 特に `wp_ajax_nopriv_*` 系エンドポイントや `/goform/*` へのリクエストは警戒対象です。

### 3.2 製品別具体的アクション  

| 製品 | 現行バージョン → 推奨バージョン | 追加対策 |
|------|--------------------------------|----------|
| **Wings (Pterodactyl)** | `< 1.12.3` → **1.12.3** 以上 | - `config.*` プレースホルダーの使用を一時的に無効化<br>- 既存の `config.token` 系シークレットを全て再生成 |
| **Single Sign On For TNG (WordPress)** | `≤ 2.0.0` → **2.0.1** (公式パッチ) | - プラグインの `ssoprocess_ajax` フックを無効化し、代替認証方式へ切替<br>- 管理画面のユーザー権限を最小化 |
| **Tenda W6‑S ルータ** | ファームウェア **1.0.0.4** → **1.0.0.5** | - 不要な `wifiSSIDset` API を外部から遮断（ACL）<br>- 管理者パスワードを強力なものに変更し、SSH/HTTPS のみ許可 |
| **vault‑secrets‑webhook** | `< 1.23.1` → **1.23.1** 以上 | - `vault-addr` アノテーションの使用を制限し、RBAC で Webhook の実行権限を最小化<br>- 既存の Pod

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-52855

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-200;CWE-522` |
| Published | 2026-07-31T17:16:33.313 |

Wings is the server control plane for Pterodactyl, a free, open-source game server management panel. Prior to 1.12.3, {{config.}} placeholders in egg configuration-file templates allow a low-privileged user to read {{config.token}}, {{config.token_id}}, and {{config.docker.registries}} from the full daemon configuration. This issue is fixed in version 1.12.3.

### CVE-2026-15964

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-620` |
| Published | 2026-08-01T09:17:00.137 |

The Single Sign On For TNG plugin for WordPress is vulnerable to Authentication Bypass via unauthenticated password reset in all versions up to, and including, 2.0.0. This is due to the `ssoprocess_ajax()` function — registered on `wp_ajax_nopriv_ssoprocess_ajax` and therefore reachable without authentication — accepting an attacker-supplied `email` parameter with the `setnewpassword` operation and calling `reset_password()` on the resolved account without any ownership token, email confirmation link, or capability check. The sole guard is a call to `check_ajax_referer()`, which provides no authorization barrier because the `ssoajaxnonce` nonce is publicly broadcast on every front-end page via `wp_localize_script()` into the `SSOPWDREQUIREMENT` JavaScript object; since WordPress computes nonces for logged-out visitors against a shared anonymous session context, any unauthenticated visitor can scrape a valid nonce from the homepage and use it to authenticate the request. This makes it possible for unauthenticated attackers to change the password of any WordPress account, including administrator accounts, enabling complete site takeover.

### CVE-2026-67822

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-31T17:16:35.210 |

Tenda W6-S 1.0.0.4(510) contains a stack-based buffer overflow vulnerability in the /goform/wifiSSIDset endpoint. The function formwrlSSIDset uses sprintf to copy user-controlled 'GO' and 'index' parameters into a 64-byte stack buffer without length restriction, leading to stack overflow.

### CVE-2026-54725

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-31T18:17:17.013 |

vault-secrets-webhook is a Kubernetes mutating webhook that makes direct secret injection into Pods possible. Prior to 1.23.1, parseVaultConfig() in pkg/webhook/config.go accepts the vault.security.banzaicloud.io/vault-addr annotation, MutateConfigMap and MutateSecret call newVaultClient in pkg/webhook/webhook.go, and vault.security.banzaicloud.io/vault-serviceaccount can cause a ServiceAccount JWT to be sent to an attacker-controlled Vault address. This issue is fixed in version 1.23.1.

### CVE-2026-67336

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-327` |
| Published | 2026-08-01T13:17:04.557 |

better-auth versions before 1.6.11 contain insecure cryptographic defaults in the oidcProvider and mcp plugins that advertise the none algorithm and accept plain PKCE by default. Attackers can exploit algorithm negotiation to accept unsigned tokens or intercept authorization codes when PKCE plain is used instead of the required S256 method.

### CVE-2026-67330

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-01T13:17:03.677 |

@better-auth/scim (a better-auth plugin) versions >= 1.4.0-beta.27 through <= 1.6.21 and >= 1.7.0-beta.0 through <= 1.7.0-beta.9 contain an authorization bypass. SCIM token issuance did not reject provider IDs already used by existing SSO, SAML, OIDC, generic OAuth, or social account providers, and the same logical provider ID was used for both SCIM provider configuration and account ownership. An authenticated user could mint a SCIM token whose provider ID collided with an existing provider namespace, causing SCIM user routes to resolve account rows the token never provisioned. This allowed listing, reading, updating (including rewriting global profile/email fields without uniqueness checks), and deleting global user accounts and sessions, resulting in account takeover and unauthorized deprovisioning. Fixed in 1.6.22 and 1.7.0-beta.10 (1.7.0-rc.0).

### CVE-2026-67305

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-01T13:17:00.113 |

FreeRDP Windows client before 3.29.0 contains a heap buffer overflow vulnerability in the clipboard virtual channel when processing CLIPRDR_FILE_CONTENTS_RESPONSE PDUs without validating the server-provided size against the destination buffer. A malicious RDP server can send a response with a data payload significantly larger than requested, causing arbitrary heap memory corruption that may enable remote code execution when a user performs a paste operation.

### CVE-2026-58048

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-31T17:16:34.190 |

Improper preservation of SQL mode when renaming databases in  cPanel allows execution of SQL in root context.

### CVE-2026-17566

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-115` |
| Published | 2026-07-31T16:17:00.037 |

pgAdmin 4's Import/Export Data tool builds a psql \copy (...) command line by interpolating a user-supplied SQL query into a Jinja template and passing the rendered line to psql via --command. To stop an attacker from breaking out of the (...) wrapper, create_import_export_job() (route POST /import_export/job/<sid>, gated only by the ordinary, commonly-granted tools_import_export_data permission) validated the query with a hand-written parenthesis-balance checker, _is_query_parens_balanced(). That checker always treated a backslash before a single quote (\') as escaping the quote, i.e. as if standard_conforming_strings were off. PostgreSQL has defaulted standard_conforming_strings to on since 9.1 (2010), the default on every PostgreSQL version pgAdmin 4 currently supports (13-18); under that default psql's own \copy tokenizer treats \ as an ordinary character, so a single quote immediately after it closes the string literal. A query such as SELECT 'a\') TO PROGRAM 'echo pwned' x' was therefore accepted as "balanced" by pgAdmin's checker (which believed the ) was still inside the string), while psql, run through the actual rendered command line, closes the string at that point and treats the following ) as the end of the wrapping \copy (...) subquery, exposing an attacker-chosen TO PROGRAM '<command>' clause that psql executes via popen() -- independent of a subsequent syntax error later on the same line. This is the same class of bug as CVE-2025-12762/CVE-2025-13780 (RCE via psql meta-command/COPY injection during PLAIN-format dump restore), reached through an independently written defense in a different module (Import/Export Data rather than Restore) that had its own, different logic bug (inverted backslash-escape semantics rather than a BOM-defeated regex anchor).

The fix rejects any backslash inside a single-quoted string in the query outright, rather than picking one of the two possible psql interpretations. This is intentionally conservative: because the correct interpretation of \ depends on the target server's standard_conforming_strings setting, which the checker cannot reliably know at validation time, refusing the query is safer than guessing.

This issue affects pgAdmin 4: from the introduction of _is_query_parens_balanced() before 9.18.

### CVE-2026-17351

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89;CWE-115` |
| Published | 2026-07-31T16:16:59.807 |

The fix for CVE-2026-12045 in pgAdmin 4 9.16 required the LLM-supplied query passed to the AI Assistant's execute_sql_query tool to parse, via sqlparse, as exactly one non-transaction-control statement before running it inside a BEGIN TRANSACTION READ ONLY wrapper. sqlparse's string-literal lexing can disagree with PostgreSQL's own parser: under standard_conforming_strings = on (PostgreSQL's default since 9.1), a backslash immediately before a quote is an ordinary character to PostgreSQL, but sqlparse treats it as escaping the quote. A payload such as SELECT '\';COMMIT;CREATE TABLE pwn(x int);SELECT 1 --' therefore parses as a single SELECT to sqlparse's validator, while PostgreSQL executes it as four statements: the smuggled COMMIT ends the wrapping read-only transaction, and the trailing ROLLBACK becomes a no-op. This reintroduces the same write/RCE bypass CVE-2026-12045 was meant to close, reachable via the same indirect prompt-injection delivery (an attacker plants the payload in any object the AI Assistant may read; the LLM emits it as a tool call).

An initial candidate fix ran the query with psycopg's execute(..., prepare=True), intending to force PostgreSQL's own Parse step (extended query protocol) to reject multi-statement text regardless of sqlparse's classification. This candidate fix does not work as submitted: psycopg3's PrepareManager silently ignores the prepare argument whenever the connection's prepare_threshold is None, which is pgAdmin's default for every server connection (the per-server "Prepare threshold" field is blank unless an administrator explicitly sets it) -- psycopg3 falls back to the simple query protocol, the same multi-statement-capable path the bypass exploits, so the candidate fix closes nothing on any real-world default configuration.

The corrected fix sets conn.prepare_threshold = 0 directly on the dedicated, single-use read-only connection the AI Assistant tool opens, structurally forcing the extended query protocol independent of any server-level configuration. Verified against a live PostgreSQL 18 instance: the payload executes successfully under the prepare_threshold=None (default) behavior, and is rejected with "cannot insert multiple commands into a prepared statement" once prepare_threshold=0 is set on that connection.

This issue affects pgAdmin 4: from 9.13 before 9.17.

### CVE-2026-67342

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-01T13:17:05.417 |

ArcadeDB versions before 26.7.2 contain an authorization bypass vulnerability in HTTP handlers for time series, batch, Prometheus, and Grafana endpoints that fail to validate database access permissions. Attackers can access and modify databases they are not authorized to use by directly calling affected endpoints with arbitrary database parameters.

### CVE-2026-67341

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-01T13:17:05.273 |

ArcadeDB versions before 26.7.2 fail to enforce scripting authorization checks on the SQL DEFINE FUNCTION statement with LANGUAGE js. Attackers with database access can execute arbitrary JavaScript code by submitting DEFINE FUNCTION statements, bypassing security controls intended to restrict scripting to administrators.

### CVE-2026-67340

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-01T13:17:05.127 |

ArcadeDB before 26.7.2 (arcadedb-engine) allows trigger scripts to look up host classes in java.lang.* (via Java.type) because ScriptTriggerExecutor adds java.lang.* to the allowed packages. An authenticated user with UPDATE_SCHEMA permission can create a JavaScript trigger that invokes java.lang.Runtime.getRuntime().exec() (or ProcessBuilder), achieving OS command execution when the trigger fires.

### CVE-2026-67324

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-01T13:17:02.770 |

GitPython 3.1.50 fails to recognize joined short-option forms such as -u<value> (the short form of --upload-pack=<value>) when enforcing its default unsafe-option gate. When an application passes attacker-influenced clone options into Repo.clone_from(..., multi_options=..., allow_unsafe_options=False), an attacker can supply -u<helper> to bypass the gate that blocks --upload-pack/-u, causing Git to execute the specified helper command during clone. Fixed in 3.1.51.

### CVE-2026-67294

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-01T13:16:58.523 |

FreeRDP before 3.29.0 improperly validates the Extended Key Usage (EKU) purpose of the peer certificate during client-side server TLS authentication. In x509_utils_verify(), when server-purpose (X509_PURPOSE_SSL_SERVER) verification fails, the code falls back to client-purpose and any-purpose verification, so a trusted, hostname-matching certificate valid only for clientAuth can be accepted as the RDP server certificate. In environments relying on EKU separation between client and server certificates, this allows a clientAuth-only certificate issued by a trusted CA to bypass server certificate purpose validation.

### CVE-2026-67293

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-01T13:16:58.380 |

FreeRDP before 3.29.0 (affected versions <= 3.28.0) contains an improper certificate hostname validation vulnerability. The TLS hostname matcher (tls_match_hostname() in libfreerdp/crypto/tls.c) treats a wildcard pattern such as *.example.com as matching any hostname ending in .example.com, so it incorrectly accepts a wildcard certificate for multi-label subdomains like a.b.example.com (which OpenSSL's X509_check_host() rejects). This weakens TLS server authentication under wildcard-certificate conditions.

### CVE-2026-67292

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-130` |
| Published | 2026-08-01T13:16:58.240 |

FreeRDP before 3.29.0 contains a buffer over-disclosure vulnerability in the gateway WebSocket transport (libfreerdp/core/gateway/websocket.c). The client's Pong reply reuses a fixed 1024-byte response stream whose length is not sealed to the actual received Ping payload, so a malicious gateway/WebSocket peer sending a non-empty Ping control frame causes the client to reply with an overlong Pong that discloses bytes beyond the received payload (the peer receives the masking key and can unmask the reply). A zero-length Ping reaches an assertion and terminates the client (denial of service).

### CVE-2026-67289

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-113` |
| Published | 2026-08-01T13:16:57.803 |

FreeRDP before 3.29.0 (affected versions <= 3.28.0) does not validate CRLF and control characters in the server-controlled RDP redirection TargetNetAddress field. This value is copied into the client's ServerHostname and, when the client connects through an HTTP proxy, is written directly into the proxy CONNECT request line and Host header by http_proxy_connect() without filtering. A malicious or compromised RDP server can send a crafted redirection PDU containing embedded control characters to inject arbitrary headers/requests into the HTTP proxy CONNECT request.

### CVE-2026-66402

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-01T13:16:57.487 |

FreeRDP before 3.29.0 (affected versions <= 3.28.0) contains multiple TLS certificate identity validation weaknesses in tls_verify_certificate(), tls_match_hostname(), and x509_utils_get_dns_names(). Because FreeRDP performs custom Common Name and DNS SAN string matching instead of using OpenSSL's length-aware identity validation APIs, it (1) truncates DNS SAN values at embedded NUL bytes (accepting e.g. 'victim.example\0.attacker.example' as 'victim.example'), (2) accepts a matching Common Name even when non-matching DNS SAN entries are present, and (3) accepts IP-literal targets via DNS/CN matching without comparing iPAddress SANs. Under a trusted or misissued certificate chain, an attacker positioned to present such a certificate can bypass server identity verification, weakening TLS server authentication.

### CVE-2026-68771

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-31T22:17:03.630 |

ComfyUI v0.23.0 contains an unsafe deserialization vulnerability in the LoadTrainingDataset node that allows unauthenticated remote attackers to execute arbitrary Python code by uploading a crafted pickle file and triggering its deserialization. Attackers can upload a malicious shard_*.pkl file via the unauthenticated POST /upload/image endpoint and then queue a workflow graph via POST /prompt referencing the uploaded file, causing torch.load to deserialize the attacker-controlled pickle payload using __reduce__ and execute arbitrary commands as the ComfyUI process user.

### CVE-2026-68770

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-31T21:17:32.440 |

sentence-transformers contains a security control bypass vulnerability that allows attackers to achieve arbitrary code execution by exploiting a logic flaw in the import_module_class helper within sentence_transformers/util/misc.py, where the guard condition includes an 'or os.path.exists(model_name_or_path)' clause that satisfies the trust gate whenever the supplied path exists on the local filesystem, regardless of the trust_remote_code=False argument. Attackers who can control or influence the contents of a model directory on disk can place malicious Python files such as modeling_*.py referenced via modules.json, causing the code to execute at import time when an application loads the model with SentenceTransformer(path, trust_remote_code=False), bypassing the documented security contract and achieving code execution within the loading process.

### CVE-2026-17349

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522;CWE-639` |
| Published | 2026-07-31T16:16:59.480 |

/misc/workspace/adhoc_connect_server, part of the Workspaces feature introduced in pgAdmin 4 9.0, when passed the id of an existing server, clones that server via Server.clone(), which copies every column from the source row, including user_id, shared, shared_username, and the stored credential fields password, save_password, and tunnel_password. When a non-owner triggered an adhoc connect against another user's (in practice, typically an administrator's) shared server, the clone inherited that user's ownership, shared flag, and stored database credentials verbatim. pgAdmin persisted this cross-tenant, credential-bearing server row before the connection was even attempted, so it survived even when the connection subsequently failed. The non-owner could then open the newly-owned clone and pgAdmin would connect using the source user's stored database password on the non-owner's behalf, granting the non-owner use of database credentials -- and whatever database privileges they confer -- that were never their own.

Fix forces the cloned adhoc record's ownership fields (user_id, shared, shared_username) and stored credential fields (password, save_password, tunnel_password) to belong to the calling user and be cleared/private before committing, regardless of the source server's ownership, sharing state, or stored credentials. A regression test asserts that an adhoc connect triggered by a non-owner against another user's shared server persists a row owned by the caller, not shared, and without the source's stored credentials.

This issue affects pgAdmin 4: from 9.0 before 9.17.

### CVE-2026-3141

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-01T06:16:26.030 |

The FormGent plugin for WordPress is vulnerable to unauthorized arbitrary file deletion due to a missing capability check on the /wp-json/formgent/responses/attachments REST API endpoint in all versions up to, and including, 1.9.2 This is due to the REST API route being registered without any authentication middleware in routes/rest/api.php. This makes it possible for unauthenticated attackers to delete arbitrary files within the formgent uploads directory. Additionally, on Linux servers where the wp-content/uploads/formgent directory does not yet exist (the default state after plugin installation), the path traversal protection can be bypassed, enabling deletion of arbitrary files including wp-config.php which can lead to complete site takeover via a fresh WordPress installation.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-16635

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-01T09:17:00.970 |

The Pronamic Pay plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 10.1.0 This is due to the `maybe_update_user_role()` function passing an attacker-controlled Gravity Forms field value (`$lead[$feed->user_role_field_id]`) directly into `WP_User::set_role()` without any allowlist validation, capability comparison, or permission check to constrain which roles can be assigned. This makes it possible for authenticated attackers, with Subscriber-level access and above, to escalate their own WordPress account to Administrator by tampering with the role field value in a form submission. Exploitation requires that an administrator has already configured a Pronamic Pay payment feed in Gravity Forms with the **Update User Role** option enabled and mapped to a form field; once that configuration is in place, no further preconditions exist to prevent an authenticated attacker from exploiting this vulnerability.

### CVE-2026-15988

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-01T08:16:29.610 |

The AI Engine – The Chatbot, AI Framework & MCP for WordPress plugin for WordPress is vulnerable to Cross-Site Request Forgery in all versions up to, and including, 3.6.5 This is due to missing or incorrect nonce validation on the reauth_for_authorize function. This makes it possible for unauthenticated attackers to create new administrator accounts with attacker-supplied credentials via a CSRF-based REST authentication bypass, granted they can trick a site administrator into performing an action such as clicking on a link. This bypass can be combined with WordPress's ?_method=POST method-override support to convert a top-navigation GET request into an authenticated POST to the REST users endpoint, requiring no existing account on the attacker's part.

### CVE-2026-15414

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-01T03:16:25.757 |

The Subscriptions for WooCommerce plugin for WordPress is vulnerable to Privilege Escalation in versions up to, and including, 2.0.0. This is due to the `save_meta_boxes()` function persisting the `_wps_plan_user_role` membership plan meta from `$_POST` without an allowlist that excludes privileged roles — the only validations applied, `sanitize_key()` and `wp_roles()->is_role()`, both accept `'administrator'` as a valid value, and the UI's `disabled` attribute on the role dropdown is a client-side-only control trivially bypassed via DevTools or a direct POST request; additionally, because the `wps_membership_plan` custom post type is registered with `capability_type => 'post'`, any user who can edit posts satisfies the `current_user_can('edit_post', $post_id)` guard in `save_meta_boxes()`. This makes it possible for authenticated attackers, with Contributor-level access and above, to escalate their privileges to Administrator by storing `'administrator'` as the role granted on membership acquisition, which the Pro companion plugin then applies via `add_role()` during membership lifecycle events. Successful exploitation requires the Subscriptions for WooCommerce Pro companion plugin to be active, as it is the component that reads the stored `_wps_plan_user_role` meta via `get_post_meta()` and calls `add_role()` to apply the role during membership lifecycle events.

### CVE-2026-67343

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-01T13:17:05.563 |

ArcadeDB versions before 26.7.2 fail to properly redact the cluster token in the GET /api/v1/server endpoint, allowing authenticated users to retrieve the arcadedb.ha.clusterToken value in cleartext. Attackers can use the leaked token with X-ArcadeDB-Cluster-Token and X-ArcadeDB-Forwarded-User headers to impersonate root and execute administrative actions including user creation, database operations, and server shutdown.

### CVE-2026-67331

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-01T13:17:03.833 |

better-auth SCIM versions from 1.5.0 before 1.7.0-beta.4 fail to bind non-organization SCIM providers to their creator by default, allowing authenticated users to manage other users' providers. Attackers can regenerate SCIM bearer tokens, invalidate legitimate tokens, and authenticate to SCIM API routes with the attacker-controlled token.

### CVE-2026-67327

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-01T13:17:03.227 |

better-auth versions >= 1.1.3 and < 1.6.22 (and pre-release versions >= 1.7.0-beta.0 and < 1.7.0-beta.10) are vulnerable to account takeover via pre-account hijacking on magic-link and email-OTP sign-in when open email/password registration is enabled. An attacker registers an account with the victim's email address and an attacker-chosen password; the account remains unverified. When the legitimate owner later signs in via the magic-link or email-OTP passwordless flow, the account is marked verified without removing the pre-existing password or revoking existing sessions, so the attacker's password remains valid, granting persistent access to the victim's account. Fixed in 1.6.22 and 1.7.0-beta.10.

### CVE-2026-67325

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-01T13:17:02.923 |

GitPython before 3.1.51 contains an incomplete command injection blocklist that fails to account for git's long-option prefix abbreviation feature. Attackers can bypass the unsafe options guard by using abbreviated option names like upload_p instead of upload_pack, which git resolves to dangerous options and executes arbitrary commands.

### CVE-2026-67322

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-01T13:17:02.493 |

GitPython before 3.1.52 is vulnerable to environment-variable exfiltration in Repo.clone_from(). The caller-supplied remote URL is passed through Git.polish_url(), which on non-Cygwin platforms calls os.path.expandvars() on the URL before invoking git clone. An attacker who controls the clone URL can embed $NAME or ${NAME} tokens that are expanded to the values of the hosting process's environment variables (e.g., AWS_SECRET_ACCESS_KEY or GITHUB_TOKEN). The resulting URL, now containing the secret, is transmitted over the network to an attacker-controlled host during the clone attempt, disclosing the secret.

### CVE-2026-67304

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-01T13:16:59.970 |

FreeRDP before 3.29.0 contains a null pointer dereference vulnerability in smartcard device control request cleanup when reader-state decoding fails. Attackers can send malformed smartcard IRP requests with non-zero cReaders and truncated reader-state data to crash the process via null pointer access in free_reader_states functions.

### CVE-2026-67301

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-01T13:16:59.530 |

FreeRDP before 3.29.0 contains out-of-bounds read vulnerabilities in the async update message proxy for the PolygonSC and PolygonCB primary drawing orders. When AsyncUpdate is enabled (e.g., xfreerdp /async-update), update_message_PolygonSC() and update_message_PolygonCB() allocate a fresh points array but copy point data from the address of the order structure instead of from polygonSC->points / polygonCB->points, resulting in a client-side out-of-bounds read. A malicious or compromised RDP server sending crafted PolygonSC/PolygonCB update orders can trigger memory disclosure or a client crash.

### CVE-2026-67300

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-01T13:16:59.393 |

FreeRDP before 3.29.0 contains client-side heap use-after-free vulnerabilities in the async update message proxy for RAIL WINDOW_STATE_ORDER and NOTIFY_ICON_STATE_ORDER when AsyncUpdate is enabled. When a malicious or compromised RDP server sends crafted update orders, the message proxy shallow-copies structures containing nested parser-owned pointers (e.g., titleInfo.string, windowRects, visibilityRects, icon buffers). The parser frees those nested buffers after the callback returns, so the queued async message later dispatches stale pointers, potentially causing memory corruption or a client crash.

### CVE-2026-67299

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-01T13:16:59.250 |

FreeRDP before 3.29.0 contains a client-side heap use-after-free in the async update message proxy for WINDOW_ICON_ORDER when AsyncUpdate is enabled (e.g. xfreerdp /async-update). In update_message_WindowIcon() a shallow CopyMemory() overwrites a freshly allocated lParam->iconInfo with the parser-owned windowIcon->iconInfo pointer. After the parser callback returns, update_recv_window_info_order() frees window_icon.iconInfo, but the queued async message still retains and later dispatches that stale pointer. A malicious or compromised RDP server sending a crafted RAIL Window Alternate Secondary Order with WINDOW_ORDER_ICON can trigger use-after-free, leading to memory corruption and client crash.

### CVE-2026-67298

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-08-01T13:16:59.107 |

FreeRDP versions 3.28.0 and earlier contain a heap buffer overflow in the server-side RAIL channel handler (rail_server_handle_messages() in channels/rail/server/rail_main.c). When processing a RAIL PDU header, the code subtracts RAIL_PDU_HEADER_LENGTH from the peer-controlled orderLength field without first verifying orderLength is at least the header length. For orderLength values 0..3 this causes an unsigned integer underflow to a very large size, which bypasses the Stream_EnsureRemainingCapacity() capacity check (due to pointer arithmetic wraparound) and is then passed to WTSVirtualChannelRead(), resulting in an out-of-bounds heap write. A malicious or compromised RDP client can exploit this to corrupt the heap and crash the server. Fixed in FreeRDP 3.29.0.

### CVE-2026-67297

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-01T13:16:58.967 |

FreeRDP before 3.29.0 fails to enforce the RESPONSE_SIZE_LIMIT when processing Transfer-Encoding: chunked HTTP responses in http_response_recv_body(). Attackers controlling a malicious RD Gateway endpoint can send oversized chunked response bodies to exhaust client memory resources without triggering the configured size limit.

### CVE-2026-67296

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-01T13:16:58.830 |

FreeRDP before 3.29.0 contains a denial of service vulnerability in the RDPEI server channel handler that fails to validate maximum PDU body length before stream allocation. A malicious RDP client can send a header-only RDPEI message with a large declared body length to force excessive memory allocation on the server.

### CVE-2026-67291

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-01T13:16:58.097 |

FreeRDP before 3.29.0 (affected versions <= 3.28.0) contains a heap out-of-bounds read in update_process_glyph_fragments()/glyph_cache_fragment_put() in libfreerdp/cache/glyph.c. When handling a GLYPH_FRAGMENT_ADD update, the code reads a one-byte server-controlled declared fragment size but does not verify it fits within the remaining received buffer before allocating and copying that many bytes. A malicious RDP server can send a short fragment with an oversized declared size, causing the client to read beyond the allocated buffer, resulting in an out-of-bounds read and client crash.

### CVE-2026-67290

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-01T13:16:57.940 |

FreeRDP before 3.29.0 contains a heap out-of-bounds read vulnerability in the TSMF FFmpeg decoder when parsing AVC1 MPEG2VIDEOINFO media types with insufficient ExtraData. Attackers can send malformed media format data from a server to trigger a crash by reading fixed offsets without validating source buffer length.

### CVE-2026-67288

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-01T13:16:57.650 |

FreeRDP before 3.29.0 contains a null pointer dereference vulnerability in smartcard cache request decoders that accept NULL NDR pointers for LookupName in SCARD_IOCTL_READCACHEA and SCARD_IOCTL_WRITECACHEA operations. When smartcard emulation is enabled, attackers can send crafted smartcard cache requests with NULL lookup-name pointers to trigger strlen() on a null pointer, causing client process termination.

### CVE-2026-53502

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-31T19:17:09.577 |

Thumbor is an open-source photo thumbnail service by globo.com. Prior to 7.8.0, file_loader decodes percent-encoded path segments after its root-boundary validation, allowing traversal outside FILE_LOADER_ROOT_PATH through watermark or frame filter input. This issue is fixed in 7.8.0.

### CVE-2026-55100

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23;CWE-74` |
| Published | 2026-07-31T18:17:17.480 |

hashi-vault-js is a Node.js module for interacting with the HashiCorp Vault API. Prior to 0.5.2, src/Vault.js concatenates unencoded identifier values including name, username, group, role, and version into Vault request paths and query strings instead of using encodeURIComponent() and URLSearchParams, allowing path traversal and query parameter injection. This issue is fixed in version 0.5.2.

### CVE-2026-54729

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-31T18:17:17.173 |

DSSRF is a Node.js library that provides a wide range of utilities and advanced SSRF defense checks. Prior to 1.0.5, is_url_safe can treat localhost as safe when DNS resolver 1.1.1.1 returns NXDOMAIN because dns.resolve4 yields no address and no dns.lookup fallback occurs, allowing server-side request forgery. This issue is fixed in version 1.0.5.

### CVE-2026-17346

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-31T16:16:58.970 |

The fix for CVE-2026-12044 in pgAdmin 4 9.16 hardened qtLiteral and switched sixteen COMMENT ON / pgstattuple / pgstatindex templates to it, but missed several sinks that had been placed in test_sql_string_literal_lint.py's ALLOWLIST on the incorrect assumption that schema, table, publication, and subscription names sourced from pg_catalog via the browser tree could never contain an apostrophe. PostgreSQL permits arbitrary characters in quoted identifiers, so a low-privileged user able to CREATE TABLE, CREATE PUBLICATION, or CREATE SUBSCRIPTION can plant an apostrophe'd object name that breaks out of the unescaped '{{ name }}' template interpolation the moment any user (including a higher-privileged one) opens that object's Statistics or Dependencies tab, allowing arbitrary SQL statement injection in the viewing user's database session.

Affected sinks: the Index Statistics query for all-indexes listing (coll_stats.sql, both the 16_plus and default PostgreSQL-version template variants -- distinct from the single-index stats.sql path already fixed in CVE-2026-12044), and the publication and subscription dependencies.sql / get_position.sql templates (both the pg and ppas/EPAS dialect variants for publications).

Fix switches all of these templates to qtLiteral(conn) for name interpolation, and updates publications/__init__.py and subscriptions/__init__.py to pass conn=self.conn into the dependencies.sql render_template call so the qtLiteral filter has a connection to quote against. The corresponding ALLOWLIST entries in test_sql_string_literal_lint.py are removed now that these sinks are properly escaped rather than merely assumed safe. A behavioral regression test renders each fixed template with a stacked-statement apostrophe payload and asserts both that the object name appears exactly as qtLiteral-escaped and that the rendered SQL parses as exactly one statement, verifying the assertion genuinely fails against the pre-patch raw-interpolation form.

This issue affects pgAdmin 4: the Index Statistics sink from 1.0, and the Publications/Subscriptions sinks from 5.0, both before 9.17.

### CVE-2026-67328

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-01T13:17:03.380 |

@better-auth/sso versions before 1.6.21 contain multiple authentication bypass vulnerabilities in SSO provider handling that allow attackers to sign in as arbitrary users. Attackers can exploit domain verification parsing mismatches, orphaned provider accounts, unbound SAML assertions, or reflected XSS on logout endpoints to gain unauthorized session access and account takeover.

### CVE-2026-67323

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-01T13:17:02.637 |

GitPython before 3.1.51 fails to guard against dangerous Git options passed as keyword arguments in Repo.archive() and git.ls_remote(), allowing command injection via options such as --exec/--upload-pack (leading to arbitrary command execution). Additionally, Repo.iter_commits() and Repo.blame() do not check for leading-dash revision arguments, so a revision like --output=<path> can cause Git to open and truncate an arbitrary file. Exploitation requires an application that passes attacker-controlled arguments to these methods.

### CVE-2026-67344

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-01T13:17:05.700 |

ArcadeDB before 26.7.2 fails to enforce the UPDATE_SCHEMA database permission on the ALTER TYPE ... CUSTOM and ALTER TYPE ... BUCKETSELECTIONSTRATEGY SQL operations, which map to setCustomValue and setBucketSelectionStrategy in LocalDocumentType. An authenticated user with only read access (e.g., a read-only API token) can submit these ALTER TYPE statements via the HTTP command endpoint to mutate a type's custom schema metadata and bucket-selection strategy, bypassing the documented updateSchema permission boundary and potentially corrupting schema metadata and record routing.

### CVE-2026-9044

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-31T23:17:26.767 |

An OS command injection vulnerability exists in the VPN module of TP-Link AXE75 V1 routers. This vulnerability allows an adjacent, authenticated attacker to execute arbitrary commands on the device by importing a specially crafted VPN client configuration file. The issue arises from improper filtering of special characters. 

Successful exploitation of this vulnerability may enable an attacker to gain full control of the affected device, potentially compromising configuration integrity, network security, and service availability.

### CVE-2026-67320

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-01T13:17:02.217 |

axios in a Node.js deployment using the HTTP adapter can route requests through an attacker-controlled proxy. axios hardens merged request configuration by creating a null-prototype object, but request interceptors run after the merge; a common immutable interceptor pattern such as {...config} or Object.assign({}, config) converts the hardened config back into a regular object. axios then dispatches that object without re-hardening it, and the Node HTTP adapter reads config.proxy through the prototype chain. If an attacker can pollute Object.prototype.proxy, affected requests can be routed through an attacker-controlled proxy. For plaintext HTTP requests, the proxy can observe Authorization headers, Basic auth from config.auth, method, absolute URL, Host, and request body, and can return its own response. This does not establish browser impact or HTTPS header/body disclosure under normal TLS validation. Affected versions are >=0.31.1 (fixed in 0.33.0) and >=1.15.2 (fixed in 1.18.0).

### CVE-2026-67355

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201` |
| Published | 2026-08-01T13:17:06.283 |

guzzlehttp/guzzle versions before 7.15.1 fail to preserve host-only cookie scope, storing the request host in the Domain field instead of marking cookies as host-only. Attackers controlling child hosts can receive host-only cookies intended only for parent hosts, potentially disclosing session identifiers and authorization tokens when the same cookie jar is reused across trust boundaries.

### CVE-2026-67354

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201` |
| Published | 2026-08-01T13:17:06.143 |

guzzlehttp/guzzle versions before 7.15.1 contain an information disclosure vulnerability in RedirectMiddleware. When the optional allow_redirects.referer setting is enabled, the middleware copies the URI fragment (the portion after '#') from the referring request into the generated Referer header when following a same-scheme redirect (e.g., HTTPS to HTTPS). An attacker who controls the redirect destination can read this fragment from the incoming Referer header, potentially disclosing one-time login secrets, access tokens, state values, or other sensitive client data to a server never meant to receive it. The referer setting is disabled by default. Fixed in 7.15.1, which strips the fragment before generating the Referer value.

### CVE-2026-67311

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-01T13:17:01.000 |

Budibase before 3.38.1 contains a server-side request forgery vulnerability in the REST datasource integration that fails to validate HTTP redirects against the IP blacklist. Attackers with Builder role can configure a REST datasource pointing to an external server that returns a redirect to internal IP addresses, bypassing blacklist protection to access cloud metadata endpoints and internal services.

### CVE-2026-62959

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-195` |
| Published | 2026-07-31T20:16:53.357 |

Coturn is a free open source implementation of TURN and STUN Server. From 4.5.2 through 4.14.0, when Coturn is started with --acme-redirect <URL> and exposes a plaintext-TCP listener, an unauthenticated remote client can send a single ordinary HTTP GET request and receive a 301 response whose Location header contains up to ~870 bytes of adjacent process heap memory. The leaked region is a recycled network receive buffer that is reused without being zeroed, so on a busy server it can contain data from other clients' requests (TURN credentials, OAuth tokens, relayed payloads). Root cause is a signed→unsigned conversion. This issue is fixed in version 4.15.0.

### CVE-2026-53501

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-347` |
| Published | 2026-07-31T19:17:09.413 |

Thumbor is an open-source photo thumbnail service by globo.com. Prior to 7.8.0, Thumbor’s HMAC validation can be bypassed due to the use of Python’s .replace() when removing the signature from the URL before validation. Since .replace() removes all occurrences of the substring, an attacker can insert the same signature multiple times in the URL and manipulate the final URL used for validation. This allows crafting URLs where the validated string differs from the actual requested resource, enabling loading images from unintended domains or paths. This issue is fixed in 7.8.0.

### CVE-2026-53500

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-31T19:17:09.247 |

Thumbor is an open-source photo thumbnail service by globo.com. Prior to 7.8.0, the ALLOWED_SOURCES configuration passes plain strings to re.match() without escaping dots, so a hostname differing at dot positions can match the allowlist. This issue is fixed in 7.8.0.

### CVE-2026-67607

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-07-31T16:17:11.913 |

LightFTP 2.3.1 contains a race condition vulnerability that allows remote attackers to crash the server by racing a fresh connection that reuses the FTP context against an in-progress ABRT cleanup. Attackers can exploit the unprotected re-check of WorkerThreadId between worker_thread_cleanup() and pthread_join() outside of MTLock to cause pthread_join() to operate on an invalid thread ID, resulting in a server crash. CVE-2024-11144 identifies an incomplete fix of this vulnerability.

### CVE-2026-18141

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-07-31T16:17:05.387 |

A flaw was found in aap-gateway, a component of Ansible Automation Platform's Event-Driven Ansible (EDA). An unauthenticated remote attacker can bypass mutual Transport Layer Security (mTLS) authentication for event streams. This is achieved by manipulating the event stream URL and forging the HTTP Subject header. The system also inadvertently discloses the expected certificate subject in error messages, which simplifies the attack. This vulnerability allows an attacker to inject arbitrary events into EDA, potentially triggering automated workflows.

### CVE-2026-16144

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-01T09:17:00.690 |

The Kali Forms — Contact Form & Drag-and-Drop Builder plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 2.4.20 via the _save_data function. This is due to insufficient validation of the 'thisPermalink' field value before it overwrites a trusted callable placeholder, allowing attacker-controlled strings to reach call_user_func() in _save_data(). This makes it possible for unauthenticated attackers to execute code on the server. Exploitation requires the target form to define a field with a name matching one of the reserved placeholder keys ('thisPermalink', 'entryCounter', or 'submission_link'), as check_if_placeholders_changed() only processes POST keys present in the form's field_type_map.

### CVE-2026-15450

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-01T09:16:59.023 |

The Nex Forms – Ultimate Form Builder – Lite plugin for WordPress is vulnerable to arbitrary file deletion via path traversal in versions up to, and including, 9.2.3. This is due to the delete_file() AJAX handler retrieving a file path from the database and passing it directly to unlink() with no validation (no realpath(), basename(), or allowlist check), combined with the insert_record() AJAX handler that lets the same authenticated user store an arbitrary value in the target 'location' column (wp_kses() only strips HTML tags and does not neutralize path traversal or absolute paths). This makes it possible for authenticated attackers, with admin-level access and above, to delete arbitrary files on the affected site's server, including wp-config. When the plugin's user-level option is configured to something else, this may be exploitable with lower privileges.

### CVE-2026-53510

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-31T20:16:51.530 |

Savon is a Ruby SOAP client. From 0.9.8 until 2.17.2, Savon::Model .all_operations interpolates attacker-controlled WSDL operation names into Ruby source passed to module_eval, allowing Ruby code execution in the application process. This issue is fixed in version 2.17.2.

### CVE-2026-67309

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-01T13:17:00.703 |

Traefik versions >= v3.7.0 and <= v3.7.7 contain a path traversal vulnerability in the Kubernetes Ingress NGINX provider's RewriteTarget middleware (generated from the nginx.ingress.kubernetes.io/rewrite-target annotation). When an Ingress path uses a regex that captures attacker-controlled text without requiring a path separator (e.g., path /api(.*) with rewrite target /$1), a crafted request such as /api../admin matches the public router, is rewritten to a dot-segment traversal path (/../admin), and is forwarded without post-replacement normalization validation. A backend that normalizes dot segments resolves the path to a protected endpoint (e.g., /admin) reachable only through a separate router secured with BasicAuth, DigestAuth, or ForwardAuth, resulting in route-level authentication bypass. The issue is fixed in v3.7.8.

### CVE-2026-34641

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-31T23:17:23.563 |

Premiere Pro is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-17347

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-88` |
| Published | 2026-07-31T16:16:59.140 |

The MASTER_PASSWORD_HOOK setting, introduced in pgAdmin 4 7.2, lets an administrator configure an external command that returns a per-user encryption key, with %u in the configured string replaced by the current user's name. The previous implementation substituted the username directly into the command string and executed the result with subprocess.Popen(..., shell=True). Because the username can originate from an external authentication source (OAuth/OIDC claims, Kerberos, webserver auth) rather than a value pgAdmin fully controls, a username containing shell metacharacters (';', '$()', backticks, pipes, '&&', newlines) allowed an authenticated user to execute arbitrary commands as the pgAdmin service account in any deployment where the configured hook string uses %u.

Fix tokenises the trusted, administrator-configured hook string into an argument vector first (using shlex in POSIX-quoting mode, with backslash-escaping disabled so Windows-style paths are not mis-parsed), substitutes the untrusted username into the individual argv elements, and executes with shell=False. The username is therefore always confined to a single argv element; any shell metacharacters it contains are inert. Administrators whose MASTER_PASSWORD_HOOK previously relied on shell features (pipes, redirection, environment-variable expansion, globbing) within the hook string itself must move that logic into the invoked script, since it is no longer interpreted by a shell.

This issue affects pgAdmin 4: from 7.2 before 9.17.

### CVE-2026-10685

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-31T15:16:27.433 |

The Zephyr Bluetooth GATT client CCC-write response handler gatt_write_ccc_rsp() in subsys/bluetooth/host/gatt.c invoked the application's params->subscribe() callback after it had already called params->notify(conn, params, NULL, 0).

Per the public GATT API, a notify callback with NULL data is the documented signal that the subscription has terminated and the bt_gatt_subscribe_params struct may be freed or reused by the application; calling subscribe() on the struct afterwards is a use-after-free, including an indirect call through the freed params->subscribe function pointer.

The error branch is remotely (adjacent) reachable: a Zephyr device acting as a GATT client that calls bt_gatt_subscribe() can be driven into this ordering when a connected GATT server peer answers the CCC write with an ATT Error Response (the peer-supplied error code flows through att_error_rsp -> att_handle_rsp into gatt_write_ccc_rsp).

For applications that free or recycle subscription parameters in their notification-termination handler, this results in memory corruption, a crash (denial of service), or potentially attacker-influenced control flow. The fix reorders the handler so the subscribe() callback runs before the terminating notify(NULL) in both the error and unsubscribe paths.

### CVE-2026-15006

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-01T03:16:25.460 |

The Bit integrations – Form Integration, Webhook, Spreadsheets, CRM, LMS & Email Automation plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 2.9.0 via the processAttachment function. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information.

### CVE-2026-62999

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-180` |
| Published | 2026-07-31T20:16:53.523 |

Copier is a library and CLI app for rendering project templates. From 9.5.0 through 9.16.0, percent-encoded parent-directory segments or encoded path separators in a template URL can match a configured trusted repository prefix before an HTTP server or Git transport decodes the path, allowing unsafe template features from a repository outside the trusted prefix to run after user interaction. This issue is fixed in version 9.17.0.

### CVE-2026-53599

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-31T20:16:51.847 |

REDAXO is a PHP-based content management system. From 5.18.2 until 5.21.1, rex_mediapool::isAllowedExtension in redaxo/src/addons/mediapool/lib/mediapool.php lets an authenticated backend user with media[upload] permission upload a JPEG/PHP polyglot named shell.php.any.jpg, which web servers with multi-extension PHP handlers can execute as the web-server user. This issue is fixed in version 5.21.1.

### CVE-2026-53505

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-31T19:17:10.123 |

Thumbor is an open-source photo thumbnail service by globo.com. Prior to 7.8.0, Thumbor's filters:proportion(<value>) filter does not enforce an upper bound on <value> and runs in the post-transform phase. An attacker can trigger extremely large resizes (CPU/memory exhaustion) and cause denial of service. This issue is fixed in 7.8.0.

### CVE-2026-53504

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-31T19:17:09.920 |

Thumbor is an open-source photo thumbnail service by globo.com. Prior to 7.8.0, the convolution filter regular expression performs exponential backtracking on crafted repeated numeric input, allowing a URL request to exhaust processing time. This issue is fixed in 7.8.0.

### CVE-2026-53503

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-369` |
| Published | 2026-07-31T19:17:09.737 |

Thumbor is an open-source photo thumbnail service by globo.com. Prior to 7.8.0, Thumbor's filters:convolution(<matrix>, <columns>, <should_normalize>) filter passes the user-controlled <columns> value to a C extension (thumbor/ext/filters/_convolution.c) where it is used as a divisor (for % and /) without validating columns > 0. When columns=0, the C code triggers undefined behavior; on x86_64 this reliably results in a fatal divide-by-zero trap (SIGFPE) and crashes the Thumbor process, causing a remote denial of service. This issue is fixed in 7.8.0.

### CVE-2026-52856

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-129;CWE-248;CWE-617;CWE-755` |
| Published | 2026-07-31T17:16:33.460 |

Wings is the server control plane for Pterodactyl, a free, open-source game server management panel. Prior to 1.13.0, a malformed packet received during the SFTP connection handshake causes a Go panic. This issue is fixed in version 1.13.0.

### CVE-2026-18446

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-436` |
| Published | 2026-07-31T15:16:27.983 |

fast-uri before 4.1.2, 3.1.5, and 2.4.4 requires a literal double forward slash to recognize a URI authority, so a reference that uses a backslash based introducer in place of it (backslash backslash, forward slash backslash, or backslash forward slash) is parsed with no authority and folds into the path. Node's native WHATWG URL parser instead treats a backslash as interchangeable with a forward slash for special schemes, so the two parsers extract different hosts from the same input. Applications that use fast-uri to enforce host based policy such as allowlists, SSRF filtering, or redirect validation before passing the same URL into Node's URL or fetch consumers can be steered to an unintended host. Upgrade to fast-uri 4.1.2, 3.1.5, or 2.4.4.

### CVE-2026-67326

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-01T13:17:03.063 |

GitPython before 3.1.50 fails to validate newline characters in the section parameter of config_writer(), allowing attackers to inject arbitrary section headers into .git/config. Attackers can inject newlines to create a forged [core] section with hooksPath pointing to attacker-controlled directories, achieving remote code execution when git hooks are triggered.

### CVE-2026-54737

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-1321` |
| Published | 2026-07-31T18:17:17.330 |

@phun-ky/defaults-deep is a library like lodash defaultsDeep with array preservation and no lodash dependency. Prior to 2.0.5, defaultsDeep() recursively merges user-supplied objects without filtering proto, constructor, and prototype, allowing properties to be written to Object.prototype. This issue is fixed in version 2.0.5.

### CVE-2026-15052

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-01T09:16:58.893 |

The MailChimp Subscribe Form, Optin Builder, PopUp Builder, Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Form Field Values in all versions up to, and including, 4.3.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-67337

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-01T13:17:04.693 |

better-auth versions before 1.4.9 contain a two-factor authentication bypass vulnerability when session.cookieCache is enabled. Attackers with valid primary credentials can access authenticated routes without completing second-factor verification by exploiting premature session caching.

### CVE-2026-67329

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-01T13:17:03.523 |

@better-auth/stripe versions >= 1.4.11 and < 1.6.21, and >= 1.7.0-beta.0 and < 1.7.0-beta.10, contain an authorization bypass in organization subscription actions. The middleware validates the organization ID taken from the request query string against the authorizeReference callback, but the handler reads the organization ID only from the request body and falls back to the caller's active organization from their session. When these differ, an authenticated member of multiple organizations can perform subscription actions (cancel, change plan, restore, billing portal access) against an organization they belong to but should not manage, and can access another organization's billing details including payment methods, invoices, and subscription state.

### CVE-2025-71403

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-08-01T13:16:56.607 |

better-auth versions before 1.1.20 contain a bypass vulnerability in trustedOrigins validation logic affecting absolute URLs and wildcard domains. Attackers can construct malicious callbackURL parameters that pass origin checks and trigger open redirects to steal sensitive tokens for account takeover.

### CVE-2026-65981

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-31T21:17:31.857 |

Coturn is a free open source implementation of TURN and STUN Server. Prior to 4.15.0, a server using --mobility authenticates a resumed REFRESH request with the resuming user's credentials but does not verify that identity against the original allocation owner, allowing an authenticated attacker who obtains a victim MOBILITY-TICKET to receive and inject relayed traffic and consume the victim's quota. In the handle_turn_refresh resume branch, the victim allocation (orig_ss) is located solely by the attacker-controlled mobile id, and credentials are only adopted (via copy_auth_parameters) when the resuming session is unauthenticated. Because the attacker's session already has hmackey_set set to 1 from its own prior authentication (which is never reset for long-term-credential sessions), the credential copy is skipped and check_stun_auth validates the REFRESH against the attacker's own identity rather than the allocation owner's. This issue is fixed in version 4.15.0.

### CVE-2026-67307

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-01T13:17:00.403 |

Wazuh 5.0.0-beta1 (fixed in 5.0.0-beta3) does not validate or override the cluster_name and cluster_node fields in inventory-sync Start FlatBuffer messages, while validating only the agentid against the authenticated agent identity. This allows a low-privileged enrolled agent to spoof cluster attribution in indexed inventory and vulnerability documents by forging wazuh.cluster.name values and influencing the document _id prefix, potentially tampering with inventory records or, in shared-indexer multi-cluster deployments, poisoning another cluster's records when numeric agent IDs collide.
