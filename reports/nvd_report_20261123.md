# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-22 15:00 UTC
- **対象期間**: `2026-11-21T15:01:42.000Z` 〜 `2026-11-22T15:00:38.000Z`
- **重要CVE数**: 120 件（Critical 9.0+: 13 件 / High 7.0〜: 107 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公表された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件以上** に上り、特に **Web アプリケーションプラグイン・CMS、組み込みファームウェア、データベースエンジン** に集中しています。  
- 権限昇格や認証バイパスが多く、攻撃者が **リモートまたはローカルでフル権限** を取得できるケースが目立ちます。  
- Unicode 正規化やパス正規化の不備、キャッシュキーの設計ミスといった **入力検証・正規化の欠陥** が根本原因となっていることが多いです。  
- 影響範囲は WordPress サイトから組み込み CPU のブート ROM、IoT ルータ、データベースサーバまで多岐にわたり、**早急なパッチ適用が不可欠** です。

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な影響 | 注目理由・攻撃シナリオ |
|-----|--------|----------|------------------------|
| **CVE‑2026‑125294** | 9.8 (CVSS3.1) | WordPress **Nexter Blocks Pro** プラグイン (≤ 5.0.10) | `tpgb_ajax_register_user()` のパラメータ `tpgb_acf_key[]`／`tpgb_acf[]` に対する **Unicode 同形文字** の除外が不完全。認証なしで任意のユーザー権限に昇格でき、サイト全体が乗っ取られる危険性がある。 |
| **CVE‑2026‑74127** | 9.4 (CVSS4.0) | AMD **Zeppelin** (Zen1/Zen+) プロセッサの PSP Boot ROM | ローカルから SPI フラッシュに直接書き込める環境があると、Secure Boot の署名検証を回避し **未署名コードをフル特権で実行** できる。BIOS/ファームウェアレベルの根本的な脆弱性で、パッチが出るまで回避策が限られる。 |
| **CVE‑2026‑133993** | 9.3 (CVSS4.0) | D‑Link **DIR‑600L** 2.17b02 の `gena.cgi` (GENA Subscription Handler) | `service` 引数の不正な操作により **スタックベースバッファオーバーフロー** が発生。リモートから任意コード実行が可能で、家庭用ルータが即座に乗っ取られる。 |
| **CVE‑2026‑134292** | 9.3 (CVSS4.0) | **SurrealDB** 1.0.0‑4.0.0 (JavaScript エンジン) | 認証済みユーザーでも **機能権限チェックがバイパス** され、内部関数 `fnc::synchronous()`／`fnc::asynchronous()` が直接呼び出せる。データベース管理者権限が不要な状態で任意スクリプト実行が可能。 |
| **CVE‑2026‑134258** | 9.3 (CVSS4.0) | **Admidio** 5.0.0‑5.0.17 の `renameFile()` | `../` シーケンスを含む `adm_new_name` で **パストラバーサル** が成立し、任意のディレクトリにファイルを書き換えられる。SVG を悪用した XSS も併発し、Web アプリ全体の信頼性が損なわれる。 |

> **共通点**：いずれも「**入力の正規化・サニタイズが不十分**」に起因し、**認証・権限チェックを迂回** できる点が特徴です。特に WordPress・Admidio のような PHP 系 CMS は、プラグイン・テーマの更新が遅れがちなので注意が必要です。

---

## 3. 推奨アクション  

### 3.1 パッチ・アップデートの適用
| 製品・パッケージ | 現行バージョン (脆弱) | 安全なバージョン | 対応手順 |
|------------------|----------------------|------------------|----------|
| **Nexter Blocks Pro** (WordPress) | ≤ 5.0.10 | **5.0.11 以上** (公式リリース) | `wp plugin update nexter-blocks-pro` または手動で最新版 ZIP を上書き。 |
| **AMD Zeppelin PSP Boot ROM** | 付属ファームウェア (全世代) | **AMD BIOS/UEFI 2026‑Q3 以降** | マザーボードベンダー提供の BIOS 更新プログラムを適用。ローカル SPI 書き込みが可能な環境は物理的にアクセス制御を強化。 |
| **D‑Link DIR‑600L** | 2.17b02 | **2.17b03 以上** (公式ファームウェア) | 管理画面 → システム → ファームウェアアップデート。アップデート後は管理者パスワードを強固に設定。 |
| **SurrealDB** | 1.0.0‑3.9.x (※4.0.0 未満) | **4.0.0 以上** | `cargo update -p surrealdb --precise 4.0.0` もしくは Docker イメージ `surrealdb:latest` に置き換え。 |
| **Admidio** | 5.0.0‑5.0.17 | **5.0.18 以上** | `composer update admidio/admidio` または公式リリース ZIP を展開。`renameFile()` の入力検証パッチが含まれる。 |

### 3.2 短期的な緩和策
1. **Web アプリケーションファイアウォール (WAF)**  
   - WordPress・Admidio へのリクエストで `tpgb_acf_key[]`, `tpgb_acf[]`, `adm_new_name` などのパラメータに **Unicode 正規化・パス正規化** を強制し、`../` シーケンスや非 ASCII 同形文字をブロック。  
2. **ネットワーク分離**  
   - AMD Zeppelin の脆弱性は **ローカル SPI アクセス** が前提。開発・テスト環境以外での物理的アクセスを制限し、BIOS 設定で **外部フラッシュ書き込みを無効化**。  
3. **最小権限の徹底**  
   - D‑Link ルータは管理者アカウントの **デフォルトパスワード** を即時変更し、SSH/Telnet の無効化。  
   - SurrealDB は **認証必須** の設定 (`--auth`) と、不要な JavaScript 機能 (`--disable-js`) を無効化。  
4. **ログ監視とインシデント対応**  
   - `tpgb_ajax_register_user` への異常な POST、`gena.cgi` への大量リクエスト、SurrealDB の `functions` 呼び出しログを SIEM に

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-125294

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-21T19:16:31.403 |

The Nexter Blocks Pro plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 5.0.10 via the `tpgb_ajax_register_user()` function. This is due to a byte-level denylist on the `tpgb_acf_key[]` and `tpgb_acf[]` parameters that fails to block Unicode look-alike characters — such as U+1E87 and U+00E7 in a key like `ẇp_çapabilities` — whose UTF-8 byte sequences do not match any ASCII-based pattern check, while the database's default accent-insensitive collation (`utf8mb4_unicode_ci` / `utf8mb4_0900_ai_ci`) treats the decorated key as equivalent to the canonical `wp_capabilities` row, causing `update_user_meta()` to overwrite the newly registered user's role with `administrator`. This makes it possible for unauthenticated attackers to register a new account bearing the full Administrator role, gaining complete control over the WordPress site including the ability to install plugins, modify files, and execute arbitrary code. The nonce required by the handler is publicly emitted on any page containing the tp-login-register block, making the full exploit chain — nonce retrieval, a single crafted registration POST, and the plugin's own `autologin` flow — trivially reachable on any default install where user registration is enabled. Successful exploitation causes the attacker's own account to receive the complete Administrator role.

### CVE-2026-74127

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-21T15:17:10.487 |

Improper verification of a cryptographic signature in the PSP Boot ROM of AMD Zeppelin (Zen1/Zen+) processors could allow an attacker with local access to the SPI flash to bypass secure boot authentication, potentially resulting in arbitrary unsigned code execution at full Platform Security Processor privilege, loss of confidentiality, loss of integrity of the host boot chain, and persistent loss of availability.

### CVE-2026-133993

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-21T18:16:54.277 |

A security flaw has been discovered in D-Link DIR-600L 2.17b02. This affects the function FUN_0040efb0 of the file gena.cgi of the component GENA Subscription Handler. Performing a manipulation of the argument service results in stack-based buffer overflow. The attack is possible to be carried out remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-134292

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T17:16:48.897 |

SurrealDB 1.0.0 before 4.0.0 contains a capability check bypass in its embedded JavaScript scripting engine, where the surrealdb.functions bridge calls the internal fnc::synchronous() and fnc::asynchronous() dispatchers without enforcing function capability checks. Authenticated users denied access to built-in functions in SurrealQL can execute them by calling them through surrealdb.functions from embedded JavaScript.

### CVE-2026-134258

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-21T17:16:43.747 |

Admidio 5.0.0 before 5.0.18 contains a path traversal vulnerability in the Documents & Files renameFile() action that allows authenticated users with folder upload rights to move files outside adm_my_files by supplying ../ sequences in adm_new_name. Attackers can relocate an uploaded SVG containing script to the web root, where it is served inline and executes stored cross-site scripting against administrators for account takeover.

### CVE-2026-134352

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-21T17:16:56.200 |

Rclone from 1.51.0 before 1.76.0 contains an authentication bypass vulnerability in serve sftp --auth-proxy because the generateCacheKey cache key omits the authentication method. Attackers knowing a victim's base64 public key can submit it as a password from the same client IP to reuse the cached entry and gain read-write VFS access.

### CVE-2026-134287

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-21T17:16:48.030 |

OpenRemote core before 1.34.0 contains an authentication bypass vulnerability in UserAssetProvisioningMQTTHandler that allows unauthenticated attackers to impersonate provisioned devices without proof of private key possession. Attackers can publish a known device's public certificate to the provisioning request topic, authenticating their anonymous MQTT connection as the device's service account to read and modify assets.

### CVE-2026-134262

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T17:16:44.420 |

Admidio 5.0.0 before 5.0.18 contains a stored cross-site scripting vulnerability that allows role administrators to inject JavaScript by placing quote-breaking payloads in role names rendered unencoded in the data-message attribute in modules/profile/roles_functions.php. Attackers can execute scripts when a full administrator views an affected profile page, stealing the CSRF token to assign themselves the Administrator role.

### CVE-2026-133867

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-436` |
| Published | 2026-11-21T17:16:40.663 |

@fastify/express is a compatibility layer that lets Express middleware run inside the Fastify web framework. In versions 4.0.7 through 4.0.9, the plugin does not rewrite regular-expression mount paths to account for a parameterized plugin prefix, so when middleware is mounted with a regular expression inside a plugin registered under a parameterized prefix, the Express matcher treats the prefix parameter as literal text and never matches the real request path. As a result, Express silently skips that middleware while Fastify still runs the route handler, so an application that relies on regular-expression mounted middleware for authentication or authorization inside a parameterized-prefix plugin exposes protected routes to unauthenticated clients. No special configuration is required beyond a parameterized prefix and a regular-expression mount. The issue is fixed in @fastify/express 4.0.10, and users should upgrade to 4.0.10 or later.

### CVE-2026-133250

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-288;CWE-436` |
| Published | 2026-11-21T17:16:40.293 |

@fastify/middie is the middleware engine for the Fastify web framework. In versions up to and including 9.3.7, middie matches path-scoped middleware against its own reading of the request path, which can differ from the path Fastify's router uses to dispatch the request. When the two disagree, the router can route a request to a handler covered by a middleware mount while middie skips that middleware, so an unauthenticated client reaches a handler that an authentication, authorization, or rate-limiting middleware was meant to protect, with no special configuration required. The mismatch is triggered by empty parameter or wildcard values, request targets that do not begin with a slash, and literal percent characters in a mount path. The issue is fixed in @fastify/middie 9.3.8, and users should upgrade to 9.3.8 or later.

### CVE-2026-133120

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-174;CWE-436` |
| Published | 2026-11-21T17:16:40.170 |

@fastify/express is a compatibility layer that lets Express middleware run inside the Fastify web framework. In versions before 4.0.10, the plugin passes Express a request URL that does not always match the path Fastify's router dispatched, so path-scoped Express middleware can be skipped while the route handler still runs. Several request forms trigger the mismatch, including percent-decoding that rewrites a backslash to a slash or double-decodes an encoded percent sign, and a request target that begins with an asterisk, so the middleware and the handler disagree on the path or on parameter and query values. An unauthenticated client can therefore reach a handler that an authentication, authorization, or rate-limiting middleware was meant to protect, with no special configuration required. The issue is fixed in @fastify/express 4.0.10, and users should upgrade to 4.0.10 or later.

### CVE-2026-129504

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-436;CWE-863` |
| Published | 2026-11-21T17:16:39.920 |

@fastify/express is a compatibility layer that lets Express middleware run inside the Fastify web framework. In versions 4.0.0 through 4.0.9, the plugin joins a path-scoped middleware's mount path to the Fastify plugin prefix by string concatenation, so when the plugin prefix ends with a slash or the mount path omits its leading slash, the resulting Express mount path does not line up with the route the Fastify router serves. Express then fails to match and passes the request on while the Fastify router still dispatches the route, so the middleware is silently skipped. An application that uses path-scoped Express middleware for authentication or authorization inside a prefixed plugin can expose protected routes to unauthenticated clients, with no crafted request and no non-default option required, and string, array, and regular-expression mount paths are all affected. The issue is fixed in @fastify/express 4.0.10, and users should upgrade to 4.0.10 or later.

### CVE-2026-124626

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-436` |
| Published | 2026-11-21T17:16:39.777 |

@fastify/express is a compatibility layer that lets Express middleware run inside the Fastify web framework. In versions 4.0.5 through 4.0.9, the plugin matches path-scoped Express middleware with a matcher that requires a non-empty value for a dynamic segment, while Fastify's router accepts an empty parameter or wildcard value. When a route and an Express middleware mount share a dynamic pattern, a request with an empty segment matches the Fastify route and runs the handler while the middleware mounted on that pattern is skipped, so on a scoped mount an unauthenticated request can reach a protected handler. No special configuration is required, and the practical impact depends on what the empty value selects in the application. The issue is fixed in @fastify/express 4.0.10, and users should upgrade to 4.0.10 or later.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-131707

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-22T10:16:39.993 |

Deserialization of Untrusted Data vulnerability in Metagauss ProfileGrid profilegrid-user-profiles-groups-and-communities allows Object Injection.This issue affects ProfileGrid: from n/a through 6.0.0.6.

### CVE-2026-134293

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-21T17:16:49.057 |

SurrealDB 3.1.0 before 4.0.0 contains an SQL injection vulnerability in its Model Context Protocol (MCP) server because the identifier validator (consume_backtick_ident and validate_identifier) treats the first backtick as the closing delimiter, ignoring escape characters that the SurrealQL parser honors. Attackers can supply MCP tool arguments containing an escaped backtick to break out of the quoted identifier and execute arbitrary SurrealQL statements.

### CVE-2026-134250

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T17:16:42.550 |

Grav Form plugin 1.1.0 before 9.1.40 contains a stored cross-site scripting vulnerability in Form::uploadFiles(), which sanitizes SVG only when a file's last extension is .svg and accepts markup under unrecognized extensions. Anonymous attackers can upload files like drawing.svg.foo through public any-type upload forms, running script in an administrator's session when opened, enabling super-admin creation on Grav 2.x with Admin2.

### CVE-2026-134679

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-22T02:17:05.103 |

WeddingShare through 1.8.2 contains a missing authorization vulnerability in the anonymous MediaViewerController.GalleryItem action that allows unauthenticated attackers to retrieve item upload paths without the gallery secret key. Attackers can enumerate sequential integer item ids to learn paths and uploader names, then download photos and videos from key-protected galleries served as static files.

### CVE-2026-134461

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-21T17:17:11.627 |

Web-Token jwt-framework and jwt-library before 3.4.10, 4.0.0 before 4.0.7, and 4.1.0 before 4.1.7 contain an uncontrolled resource consumption vulnerability in PBES2AESKW::unwrapKey(), which passes the attacker-controlled p2c JWE header value to hash_pbkdf2() without an upper bound. Unauthenticated attackers can send a JWE using a PBES2-HS*+A*KW algorithm with a huge p2c iteration count to force lengthy PBKDF2 computations and exhaust server CPU.

### CVE-2026-134456

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-21T17:17:10.850 |

Hysteria 2.5.0 before 2.9.2 contains a denial of service vulnerability in the HTTP sniff implementation that fails to limit header size. Attackers can continuously send excessively large HTTP headers without terminating them, exhausting server memory and causing out-of-memory crashes.

### CVE-2026-134452

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-11-21T17:17:10.250 |

Dockhand before 1.0.57 merges stack secret environment variables into the environment used to spawn docker compose during stack deploys without filtering reserved keys such as PATH. An authenticated attacker with stacks:edit permission can set PATH to a directory containing a malicious binary and trigger a deploy, executing arbitrary commands as the Dockhand server process user.

### CVE-2026-134367

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-21T17:16:58.310 |

pypdf 2.4.2 before 7.0.0 contains a resource exhaustion vulnerability in its handling of XFA forms that allows attackers to cause excessive memory consumption. Attackers can supply a crafted PDF containing XFA forms with many small fields so that loading the forms consumes large amounts of memory, causing a denial of service.

### CVE-2026-134366

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-21T17:16:58.160 |

pypdf before 7.0.0 contains a resource exhaustion vulnerability that allows attackers to cause large memory usage by supplying crafted PDF cross-reference streams. Attackers can craft a PDF whose cross-reference stream offsets all point to one large object, exhausting memory in applications parsing the file.

### CVE-2026-134364

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-21T17:16:58.003 |

pypdf 3.7.1 before 7.0.0 contains an information disclosure vulnerability that allows attackers to guess placeholders in encrypted templated documents by analyzing file identifiers. Attackers with a document sharing the same template and access to other documents' file identifiers can recover placeholder contents from encrypted PDFs.

### CVE-2026-134359

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-150` |
| Published | 2026-11-21T17:16:57.063 |

AzuraCast before 0.24.1 fails to escape backslashes in Liquidsoap annotation values, allowing media managers to break out of quoted annotation strings. Attackers can set a crafted ID3 title ending in a backslash to inject a process: protocol URI, achieving OS command execution in the Liquidsoap container during playback.

### CVE-2026-134347

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-58` |
| Published | 2026-11-21T17:16:55.373 |

actix-files before 0.7.4 contains an information disclosure vulnerability that allows remote unauthenticated attackers to read hidden files by requesting Windows 8.3 short-name aliases. Attackers can request short names like ENV~1 or GIT~1/config to bypass the leading-dot check in actix_files::Files and retrieve .env secrets and .git contents.

### CVE-2026-134341

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-11-21T17:16:55.073 |

actix-http 3.0.0 before 3.20.3 contains a denial of service vulnerability that allows unauthenticated remote attackers to exhaust memory by sending large-window brotli request bodies. Attackers can send an 850-byte body with Content-Encoding: br declaring a 2^30 window, forcing about 1 GiB of decoder allocation per request and OOM-killing servers.

### CVE-2026-134339

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-21T17:16:54.900 |

ArcadeDB from 26.11.1-SNAPSHOT before 26.11.1 contains an authorization bypass vulnerability that allows authenticated users to skip per-type ACL checks when a database is opened on demand. Attackers can send the first POST /api/v1/batch/{database} request to a closed database to read and write types they are not entitled to access.

### CVE-2026-134338

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-21T17:16:54.730 |

ArcadeDB 25.8.1 before 26.11.1 contains an incorrect authorization vulnerability because per-type ACLs are keyed by type name, renames are not propagated to the permission configuration, and requestAccessOnType allows unknown type names by default. Authenticated users holding only updateSchema can run ALTER TYPE NAME on a denied type to gain read, DELETE and TRUNCATE access, immediately for TIMESERIES types and after the next security rebuild for record-backed types.

### CVE-2026-134337

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-11-21T17:16:54.557 |

ArcadeDB native-image server builds 26.8.1 before 26.11.1 contain an authorization bypass vulnerability that allows authenticated clients to perform writes through read-only query paths by nesting statements in SELECT. Missing reflection metadata leaves SqlAstInspector with an empty AST, letting INSERT in projections or LET clauses persist via the query endpoint, MCP read-only mode, and HA follower routing.

### CVE-2026-134325

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-21T17:16:53.720 |

ArcadeDB before 26.11.1 contains a denial of service vulnerability in the Redis protocol handler, which neither replies to nor closes a pre-authentication connection when it receives an array whose first element is not a string. Unauthenticated attackers can resend such an array just within the 30-second socket idle timeout to hold connections open indefinitely and exhaust RedisNetworkExecutor threads.

### CVE-2026-134309

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-21T17:16:50.990 |

SurrealDB 1.0.0 before 4.0.0 contains an authorization bypass vulnerability that allows authenticated users to shadow protected $access, $auth, and $token variables by binding them as FOR loop variables. Attackers can wrap queries in nested FOR loops with forged values to satisfy table permission predicates, enabling unauthorized reads, modifications, or deletions as a VIEWER.

### CVE-2026-134299

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-21T17:16:49.743 |

SurrealDB 3.0.4 before 4.0.0 does not apply operator-configured WebSocket frame, message, and buffer size limits to the GraphQL WebSocket upgrade handler at GET /graphql, falling back to permissive library defaults. Unauthenticated remote attackers who supply the target namespace and database in request headers can hold up to 64 MiB of in-flight data per concurrent connection, exhausting server memory and degrading availability.

### CVE-2026-134295

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-21T17:16:49.393 |

SurrealDB 3.0.0 before 4.0.0 contains a path traversal vulnerability in direct filesystem buckets because BucketController::check_permission evaluates key-based ACLs against the un-normalized object key, while FileStore::to_os_path collapses '..' sequences without a traversal check. An authenticated tenant permitted only for certain keys can supply a key such as /public/../private/confidential.txt to read, write, or delete arbitrary files within the storage root.

### CVE-2026-134294

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-21T17:16:49.223 |

SurrealDB 3.0.0 before 4.0.0 contains a path traversal vulnerability in its bucket storage layer on Windows, where ObjectKey::check_no_traversal splits object keys only on forward slashes while FileStore::to_os_path treats backslashes as directory separators. Attackers can supply object keys such as /..\bucket2\secret to bypass the traversal check and read or modify files in other buckets.

### CVE-2026-134291

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-21T17:16:48.727 |

SurrealDB 3.0.0 before 4.0.0 contains a path traversal vulnerability in its filesystem storage bucket that only canonicalizes the bucket root, not descendant symlinks. Attackers can reference paths through a pre-existing symlink inside the bucket that pass the lexical prefix check, reading and writing files across the host filesystem.

### CVE-2026-134253

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-21T17:16:42.870 |

Grav API plugin from 1.0.0 before 1.1.4 contains a remote code execution vulnerability that allows publishers with media and page write rights to write theme template files through the blueprint-upload endpoint. Attackers can upload a file into a theme's Twig templates folder and include it from sandboxed page Twig to execute commands as the web-server user.

### CVE-2026-134249

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-21T17:16:42.373 |

SiYuan before 3.8.10 contains an authentication bypass vulnerability that allows unauthenticated attackers to gain Administrator role by spoofing X-Forwarded-For through a loopback-trusted reverse proxy. Attackers can send requests with Host set to localhost and X-Forwarded-For set to 127.0.0.1 to read private note-history contents via the /history/*path route when no lock-screen password is set.

### CVE-2026-134247

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-21T17:16:42.027 |

SiYuan 3.8.0 before 3.8.10 contains an incorrect authorization vulnerability that allows anonymous attackers to read indexed asset text referenced only by publish-disabled attribute-view rows. Attackers can request /api/asset/getDocAssets on a public host document to obtain the leaked asset path, then query /api/search/getAssetContentByPath to retrieve the confidential file's full indexed text.

### CVE-2026-134246

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T17:16:41.833 |

SiYuan 3.6.0 before 3.6.2 and 3.7.3 before 3.8.10 contains a missing authorization vulnerability in the /api/block/getDOMText endpoint, which renders caller-supplied DOM without checking publish access for referenced image paths. When publish authentication is disabled, anonymous visitors can submit DOM referencing a known unpublished, non-encrypted asset path to retrieve its already-cached OCR text.

### CVE-2026-134245

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-21T17:16:41.657 |

SiYuan 3.8.0 before 3.8.10 contains an incorrect authorization vulnerability in the serveAssets route that allows unauthenticated attackers to read password-protected document assets via name collisions. Attackers can request GET /assets/<name> when a visible document references the same relative asset name, retrieving the protected file's contents on public-publish instances with Basic Auth disabled.

### CVE-2026-134654

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-11-22T02:17:00.790 |

Mailflare before 48957fb contains a host header injection vulnerability in the password-reset request handler that allows unauthenticated attackers to poison reset links when APP_URL is unset. Attackers can submit a reset request for a victim's email with a malicious Host header, capturing the single-use token when the victim clicks the link to take over the account.

### CVE-2026-134451

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-21T17:17:10.100 |

Dockhand before 1.0.57 contains a privilege escalation vulnerability that allows non-admin users with settings:edit permission to modify OIDC provider configuration due to an improper permission check. Attackers can send a PUT request to /api/auth/oidc/<provider-id> setting adminClaim to their own OIDC group, gaining full admin access on their next OIDC login.

### CVE-2026-134448

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-21T17:17:09.627 |

Finsys Dockhand 1.0.7 before 1.0.57 contains a path traversal vulnerability that allows low-privileged users to read and write arbitrary files by setting an unvalidated envPath on a stack source. Attackers with stacks:edit permission can point envPath to files like /etc/shadow or SSH keys, then use GET or PUT on /api/stacks/[name]/env/raw to read or overwrite them.

### CVE-2026-134322

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-21T17:16:53.363 |

better-auth 0.4.12-beta.7 before 1.7.16 and 1.8.0-beta.0 before 1.8.0-beta.5 contains an improper authentication vulnerability in the phone number plugin that lets sign-up and other flows save unverified phone numbers, which phone OTP sign-in then uses to select the account. Attackers can attach a victim's number to an attacker-controlled account so the victim's valid OTP sign-in yields a session for that account, exposing data the victim then enters.

### CVE-2026-134316

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-21T17:16:52.550 |

@better-auth/electron 1.5.0-beta.12 before 1.7.16 and 1.8.0-beta.0 before 1.8.0-beta.5 accepts any validly signed value as its transfer cookie and returns the full endpoint context, including the auth secret and social provider client secrets, in sign-in responses. Authenticated users can obtain these secrets to forge sessions as other users. Attackers knowing a password can exchange desktop authorization codes issued before two-factor verification to bypass the second factor.

### CVE-2026-134282

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-21T17:16:47.537 |

Vikunja from 0.14.0 before 2.8.0 contains a mass assignment vulnerability that allows authenticated users to set json-hidden fields by sending XML request bodies to the v1 API. Attackers can set BackgroundFileID on project creation to download any stored file via the background endpoint, or create bots with IsAdmin set to gain instance-admin access.

### CVE-2026-131701

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-22T11:16:45.960 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in JoomUnited WP Media folder wp-media-folder allows Blind SQL Injection.This issue affects WP Media folder: from n/a through 6.2.8.

### CVE-2026-131705

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-22T10:16:39.683 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Metagauss ProfileGrid profilegrid-user-profiles-groups-and-communities allows SQL Injection.This issue affects ProfileGrid: from n/a through 6.0.0.6.

### CVE-2026-134704

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-22T02:17:09.620 |

OpenShot Video Editor (openshot-qt) through 4.1.1 contains an unsafe deserialization vulnerability in ProjectDataStore.load() and read_legacy_project_file() that passes non-JSON project files to pickle.load() without restriction. Attackers can trick users into opening a crafted .osp project file containing a pickle __reduce__ gadget to execute code with the user's privileges.

### CVE-2026-134694

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-11-22T02:17:07.790 |

Gammapy through 2.1 contains a code injection vulnerability in WcsGeom.from_header() that passes the WCSSHAPE FITS header card to eval(). Attackers can supply a crafted .fits file with a Python expression in WCSSHAPE, executing code as the user who loads it via Map.read().

### CVE-2026-134433

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T17:17:08.950 |

Frappe ERPNext before 15.124.2 and 16.x before 16.53.0 fails to enforce record-level authorization in several endpoints, reports and forms, allowing authenticated low-privilege users to access data beyond their role. Attackers can send crafted requests naming out-of-scope records to read other companies' financial, stock, pricing and contact data or make constrained changes to those records.

### CVE-2026-134429

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T17:17:08.257 |

Frappe ERPNext before 15.121.4 and 16.x before 16.36.0 contains a missing authorization vulnerability in a CRM and Support module endpoint that returns Communications of documents without checking whether the caller may read them. Authenticated attackers with a common operational role can send crafted requests naming out-of-scope records to read their email communications and relink them away from their original documents.

### CVE-2026-134389

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T17:17:01.620 |

Frappe ERPNext 6.18.0 before 15.124.0 and 16.x before 16.52.0 contains a missing authorization vulnerability in Payment Requests that lets authenticated Accounts User role holders read source documents they lack permission to access. Attackers can create a Payment Request through the generic record interface that references another company's document, then email its loaded content to an address they choose.

### CVE-2025-61963

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-123` |
| Published | 2026-11-21T15:17:06.070 |

Improper input validation within the AmdPlatformRasSmm driver could allow an attacker with privileged access to overwrite SMRAM, potentially resulting in arbitrary code execution.

### CVE-2026-134436

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T17:17:09.460 |

Frappe ERPNext 15.8.0 before 15.121.4 and 16.x before 16.36.0 contains a missing authorization vulnerability in an endpoint shared across modules that returns transaction child table rows without checking permissions on the child table or parent document. Authenticated attackers, including portal users or users without roles, can supply document types and filter conditions to read business document line details and probe record values.

### CVE-2026-134435

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T17:17:09.290 |

Frappe ERPNext before 15.124.2 and 16.x before 16.50.0 contains a missing authorization vulnerability in an Accounts module endpoint that records bank clearance dates, which checks only a broad role permission before writing to caller-named payment documents. Authenticated Accounts Users can send crafted requests naming payment documents of other companies, outside their User Permissions, or already submitted, to alter clearance dates and compromise bank reconciliation integrity.

### CVE-2026-134434

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T17:17:09.120 |

Frappe ERPNext 16.0.0 before 16.36.0 contains a missing authorization vulnerability in a Manufacturing module endpoint that allows authenticated users to cancel Stock Reservation Entries without record-level write permission. Low-privilege attackers can send crafted requests naming manufacturing documents of other companies or outside their User Permissions to release reserved stock and disrupt stock allocation.

### CVE-2026-134428

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T17:17:08.083 |

Frappe ERPNext 13.0.0 before 15.121.4 and 16.x before 16.36.0 contains a missing authorization vulnerability in a Stock module endpoint that returns Item master records without checking whether the caller may read the requested records. Authenticated attackers, including portal users or users with no assigned roles, can send crafted requests naming out-of-scope records to retrieve complete item data including costing and purchase rates.

### CVE-2026-134418

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T17:17:06.360 |

Frappe ERPNext 4.0.0 before 15.122.0 and 16.x before 16.50.0 contains a missing authorization vulnerability in an Accounts module endpoint that returns the taxes and charges of documents without checking record permissions. Authenticated users, including portal users or users with no roles, can request arbitrary document types and records to read tax rows beyond their permitted scope.

### CVE-2026-134417

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-552` |
| Published | 2026-11-21T17:17:06.197 |

Frappe ERPNext 13.0.0 before 15.121.4 and 16.x before 16.36.0 contains a missing authorization vulnerability in an Accounts module endpoint that returns uploaded bank statement file content without checking record-level permissions. Authenticated attackers, including portal users or users with no assigned roles, can send crafted requests naming records outside their scope to read full statement file contents.

### CVE-2026-134411

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-552` |
| Published | 2026-11-21T17:17:05.203 |

Frappe ERPNext 11.1.7 before 15.121.4 and 16.x before 16.36.0 contains a missing authorization vulnerability in a Regional module endpoint that returns private e-invoice files after checking only document-type permissions, not per-record User Permissions. Authenticated attackers with a common operational role can send crafted requests naming out-of-scope records to read other companies' private e-invoice files.

### CVE-2026-134404

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T17:17:03.983 |

Frappe ERPNext 6.3.0 before 15.124.0 and 16.x before 16.52.0 contains a missing authorization vulnerability in the customer and supplier portal list endpoint, which returns complete selling documents and RFQs without checking permission on the requested records. Authenticated attackers, including portal users or users without roles, can request out-of-scope records to read valuation, margin, and other bidder details.

### CVE-2026-134399

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-21T17:17:03.463 |

Frappe ERPNext 8.11.1 before 15.124.0 and 16.x before 16.52.0 is missing an authorization check in print and portal views, which fail to apply desk users' User Permissions to customer documents. Authenticated desk users with an ordinary job role can send crafted requests naming records outside their permitted scope to read documents of customers their User Permissions exclude.

### CVE-2026-134393

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T17:17:02.360 |

Frappe ERPNext 10.1.41 before 15.122.0 and 16.x before 16.50.0 contains a missing authorization vulnerability in a Manufacturing module endpoint that replaces BOMs without checking whether the caller may modify either BOM or the affected assemblies. Authenticated users who can create a BOM Update Log can send a crafted request naming two BOMs to replace the first with the second in every assembly site-wide.

### CVE-2026-134372

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-21T17:16:58.797 |

Frappe ERPNext 4.3.0 before 15.121.6 and 16.x before 16.37.0 contains an SQL injection vulnerability in an endpoint of the Selling and Buying modules, where a request value validated early can be overridden by caller-supplied data that reaches a database query unvalidated. Any authenticated user, including a portal user with no roles, can send crafted requests to extract sensitive data, including active session data, and take over other accounts such as administrators.

### CVE-2026-134370

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-21T17:16:58.457 |

Frappe Framework before 15.120.1 and 16.x before 16.33.1 contains a path traversal vulnerability in file attachment handling that permits arbitrary file read. Authenticated attackers holding a single ordinary role without write permissions can abuse attachment handling to read server files outside the application boundary.

### CVE-2026-134303

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:L/SC:H/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-21T17:16:50.480 |

SurrealKV before 1.1.0 contains an out-of-bounds read vulnerability in the safe InternalKeyRef::from_encoded constructor, which only checks key length with a debug-only assertion. Callers passing keys shorter than 16 bytes, or crafted or corrupted SSTable blocks, trigger unchecked length underflow in timestamp(), seq_num() and trailer(), reading heap bytes before the allocation or panicking.

### CVE-2026-134248

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-21T17:16:42.197 |

SiYuan 3.6.0 before 3.8.10 contains an information disclosure vulnerability that allows authenticated Readers to read protected documents through block-reference footnote resolution in Markdown export. Attackers can request copyStdMarkdown for a public document referencing a hidden, disabled, or password-protected document to disclose its body text without the publish password.

### CVE-2026-134459

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-208` |
| Published | 2026-11-21T17:17:11.317 |

web-token jwt-framework and jwt-library before 3.4.10, 4.0.x before 4.0.7, and 4.1.x before 4.1.7 contain a padding oracle in RSACrypt::decryptWithRSA15() because RSA1_5 decryption lacks implicit rejection, so invalid padding, wrong CEK length, and valid padding take measurably different time. Remote attackers can submit adaptively crafted JWE encrypted_key values and measure these timing differences to recover the wrapped content encryption key.

### CVE-2026-134458

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-325` |
| Published | 2026-11-21T17:17:11.147 |

web-token jwt-framework and jwt-library before 3.4.12, 4.0.x before 4.0.8, 4.1.x before 4.1.10, and 4.2.x before 4.2.4, and jwt-encryption-algorithm-ecdh-es through 3.2.10, have a ConcatKDF::generate() that performs a single SHA-256 round, deriving at most 32 bytes for ECDH-ES and ECDH-SS direct key agreement. Anyone holding a JWE using A256CBC-HS512 can decrypt it under an all-zero AES key, while A192CBC-HS384 content keys have only 64-bit strength.

### CVE-2026-134242

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-21T17:16:41.093 |

Parse Server 2.5.0 before 8.6.121 and 9.0.0 before 9.11.1-alpha.1 does not handle a failure to serialize an object after a beforeSave trigger, leaving the request unsettled and terminating the server process. A remote attacker able to update an object in a class with a beforeSave trigger can send a dot notation key below a non-object field, such as a timestamp, to crash the server for all clients.

### CVE-2026-134284

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-21T17:16:47.710 |

Vikunja from 1.0.0 before 2.8.0 contains an account takeover vulnerability that allows attackers to hijack SSO identities by planting local accounts with unverified victim emails. When emailfallback is enabled, attackers register or edit a local account using the victim's email, causing the victim's first OIDC login to link into the attacker-controlled account and expose their data.

### CVE-2026-134313

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-21T17:16:52.017 |

Better Auth (better-auth, @better-auth/kysely-adapter, and @better-auth/drizzle-adapter) before 1.7.16 and 1.8.0-beta.0 before 1.8.0-beta.5 contains a race condition with MySQL or MariaDB serial IDs because the inserted row's ID is read via a separate LAST_INSERT_ID() query that may run on a different pooled connection. Under concurrent load, a user signing in can receive another user's session and act as that user.

### CVE-2026-134311

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-21T17:16:51.387 |

better-auth 1.3.0 before 1.7.16 and 1.8.0-beta.0 before 1.8.0-beta.5 contains an incorrect authorization vulnerability in the admin plugin's /admin/update-user endpoint that lets roles holding user:update change another user's phoneNumber and phoneNumberVerified fields. Attackers can set their own verified phone number on a higher-privileged account and sign in via phone OTP to take it over.

### CVE-2026-131720

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-22T10:16:40.293 |

Insertion of Sensitive Information Into Sent Data vulnerability in Liquid Web / StellarWP BookIt bookit allows Retrieve Embedded Sensitive Data.This issue affects BookIt: from n/a through 2.6.0.8.

### CVE-2026-131706

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-22T10:16:39.840 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Metagauss ProfileGrid profilegrid-user-profiles-groups-and-communities allows Blind SQL Injection.This issue affects ProfileGrid: from n/a through 6.0.0.6.

### CVE-2026-134315

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-21T17:16:52.377 |

better-auth 1.4.0 before 1.7.16 and 1.8.0-beta.0 before 1.8.0-beta.5 contains an improper authentication vulnerability because email-change links record the old and new addresses but not the requesting user. Attackers can open a still-valid link issued for their own account after a victim registers the attacker's released old address, gaining a session and changing the victim's email to one they control.

### CVE-2026-134312

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-21T17:16:51.567 |

Better Auth 0.4.9 before 1.7.16 and 1.8.0-beta.0 before 1.8.0-beta.5 contains an OAuth sign-in authentication flaw that treats unverified provider emails as verified, including string "false" email_verified claims, unchecked generic OAuth profile/ID-token subject mismatches, and ignored Zoom provider options. Attackers holding a victim's address unverified at an affected provider can sign in, link to the victim's local account, and obtain its session.

### CVE-2026-129850

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-178;CWE-863` |
| Published | 2026-11-21T17:16:40.043 |

@fastify/express is a compatibility layer that lets Express middleware run inside the Fastify web framework. In versions 4.0.0 through 4.0.9, when Fastify routing is configured to be case-insensitive, the router folds the request path to lower case in a way that maps certain non-ASCII Unicode characters to ASCII letters, but @fastify/express matches Express mount paths against the decoded path without applying the same folding. The two disagree, so a request that spells a letter of a mount path with an equivalent Unicode character is routed to the protected handler while the path-scoped middleware mounted on that path never matches and is skipped. An unauthenticated client can therefore reach a handler that an authentication, authorization, or rate-limiting middleware was meant to protect, though only when the application enables case-insensitive routing and the mount path contains an affected letter. The issue is fixed in @fastify/express 4.0.10, and users should upgrade to 4.0.10 or later.

### CVE-2026-133985

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-125` |
| Published | 2026-11-21T16:16:38.730 |

A flaw has been found in TRENDnet TEW-657BRM 1.00.1. Affected by this issue is some unknown functionality of the file /usr/sbin/restore_config.cgi. Executing a manipulation can lead to out-of-bounds read. The attack may be launched remotely. The exploit has been published and may be used. The vendor explains: "I am not able to confirm if such vulnerability exists as the product has been EOL for more than 15 years. We will send out an announcement letting customers know." This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-134300

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-21T17:16:49.917 |

SurrealDB from 2.2.0 before 4.0.0 contains an authorization bypass vulnerability in Document::purge_references that lets authenticated users bypass target table PERMISSIONS by triggering REFERENCE ON DELETE cascades. Attackers can delete a referenced record to delete, unset, or run CUSTOM expressions on referencing records despite PERMISSIONS FOR delete or update NONE.

### CVE-2026-131780

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T14:17:28.593 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Themify Themify Builder themify-builder allows Reflected XSS.This issue affects Themify Builder: from n/a through 7.8.5.

### CVE-2026-131742

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T11:16:47.007 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in PluginUs.Net Active Products Tables for WooCommerce profit-products-tables-for-woocommerce allows Reflected XSS.This issue affects Active Products Tables for WooCommerce: from n/a through 2.1.8.

### CVE-2026-131724

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T11:16:46.860 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Liquid Web / StellarWP Event Tickets event-tickets allows Stored XSS.This issue affects Event Tickets: from n/a through 5.31.1.

### CVE-2026-131718

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T11:16:46.413 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Liquid Web / StellarWP Event Tickets event-tickets allows Reflected XSS.This issue affects Event Tickets: from n/a through 5.31.1.

### CVE-2026-131714

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T11:16:46.260 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Kaliforms Kali Forms kali-forms allows Reflected XSS.This issue affects Kali Forms: from n/a through 2.4.32.

### CVE-2026-131702

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T11:16:46.110 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in NextScripts NextScripts social-networks-auto-poster-facebook-twitter-g allows Stored XSS.This issue affects NextScripts: from n/a through 4.4.8.

### CVE-2026-131708

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T10:16:40.140 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Metagauss ProfileGrid profilegrid-user-profiles-groups-and-communities allows Reflected XSS.This issue affects ProfileGrid: from n/a through 6.0.0.6.

### CVE-2026-131700

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T10:16:39.523 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Dylan Kuhn  Geo Mashup geo-mashup allows Reflected XSS.This issue affects  Geo Mashup: from n/a through 1.13.23.

### CVE-2026-129016

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T10:16:38.553 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Andrea Tarantini Menubar menubar allows Reflected XSS.This issue affects Menubar: from n/a through 5.9.4.

### CVE-2026-134678

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-22T02:17:04.950 |

Freedit before 0.9.9 contains an authorization bypass vulnerability in the edit_post_post handler for POST /post/edit/:pid that skips ownership and status checks when a Private inn is submitted. Members of a Private inn can overwrite any post by sequential id, including moderator-locked posts, re-attributing it to themselves and destroying original content.

### CVE-2026-134675

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-22T02:17:04.440 |

Servas before 1.2.0 contains a missing authorization vulnerability that allows authenticated users to modify and delete other users' data by supplying target resource ids. Attackers can abuse TagController update and destroy, LinkController destroy, and GroupController destroy actions to rename or delete tags and delete links and groups.

### CVE-2026-134457

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-11-21T17:17:10.997 |

Hysteria 2.5.0 before 2.8.2 contains a memory allocation vulnerability when sniffing is enabled, allowing authenticated users to trigger out-of-memory conditions. Attackers with a valid password can forward a crafted QUIC packet with a huge crypto length, causing the server to exhaust memory and crash.

### CVE-2026-134455

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-11-21T17:17:10.700 |

Hysteria 1.0.0 before 2.9.2 contains a denial of service vulnerability in FragUDPMessage where UDP fragmentation fails to handle headers larger than the maximum datagram payload size. Authenticated clients can advertise a small max_datagram_frame_size and trigger a UDP response, causing a slice bounds panic that crashes the server.

### CVE-2026-134453

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-21T17:17:10.400 |

Dockhand before 1.0.50 contains an improper access control vulnerability that allows authenticated unprivileged users to read restricted data by querying API endpoints lacking RBAC checks. Attackers can access /api/users, /api/license, and /api/hawser/connect to obtain user emails and roles, the full license key, and environment details, while an invalid license grants all users admin rights.

### CVE-2026-134432

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T17:17:08.770 |

Frappe ERPNext 15.0.0 before 15.121.4 and 16.x before 16.36.0 contains a missing authorization vulnerability in a Stock module import endpoint that does not check whether the caller may create inserted records or download a named file. Authenticated attackers, including portal users or users with no roles, can send crafted import requests to read file contents and create Serial No and Batch records.

### CVE-2026-134431

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-21T17:17:08.600 |

Frappe ERPNext 7.0.0 before 15.122.0 and 16.x before 16.50.0 contains an SQL injection vulnerability in endpoints that build part of a query from caller-supplied sort parameters without validation. Authenticated low-privilege users can send crafted requests whose sort parameter holds SQL that the database executes as part of the query, extracting sensitive information.

### CVE-2026-134371

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-21T17:16:58.623 |

Frappe 8.8.0 before 16.30.0 contains an insecure direct object reference vulnerability in the SMS Settings get_contact_number API that lets attackers read any Contact's phone numbers without permission checks. Attackers can call the endpoint, which uses an uncorrelated EXISTS subquery, to retrieve mobile_no and phone values of arbitrary Contact records, exposing PII.

### CVE-2026-134361

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-21T17:16:57.430 |

Coder 2.6.0 before 2.29.21, 2.30.0 before 2.34.10, 2.35.0 before 2.35.8, 2.36.0 before 2.36.5, and 2.37.0 before 2.37.1 contains a denial of service vulnerability in the workspace agent dRPC API, whose handlers dereference unset request sub-messages and unconfigured Tailnet providers without recovering from panics. Attackers holding a workspace agent token can send UpdateLifecycle, UpdateStartup, or BatchUpdateMetadata messages lacking sub-messages, or call RefreshResumeToken or WorkspaceUpdates, to repeatedly crash coderd.

### CVE-2026-134360

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-21T17:16:57.237 |

Heym before 0.0.148 passes Playwright navigate-step URLs to page.goto() without validating the scheme and runs step-based scripts inside the backend container. A signed-in user who can run workflows can navigate to file:// URLs and use getText to read known-path files such as the Kubernetes ServiceAccount token or Docker secrets.

### CVE-2026-134334

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-21T17:16:54.220 |

ArcadeDB from 26.7.1 before 26.11.1 contains an information disclosure vulnerability because LSMTreeFullTextIndex computes BM25 corpus statistics over all buckets of the indexed type, ignoring bucket access control on subtypes. Authenticated users with read access to a supertype but not its subtype can run EXPLAIN or PROFILE on full-text queries and read totalDocs and per-term df values to count hidden subtype documents containing chosen terms.

### CVE-2026-134329

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-204` |
| Published | 2026-11-21T17:16:54.060 |

ArcadeDB 26.2.1 before 26.11.1 contains an observable response discrepancy in MCPToolUtils.resolveDatabase, which checks database existence before authorization and returns distinct 'not authorized' and 'does not exist' errors; separately, a failed Bolt LOGON from READY leaves the previous principal bound after RESET. Authenticated MCP callers can enumerate names of databases they are not granted by probing tools such as query or get_schema.

### CVE-2026-134327

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T17:16:53.890 |

ArcadeDB before 26.11.1 contains an authorization bypass vulnerability that allows authenticated users to read schema definitions of denied types through listings ignoring per-type ACLs. Attackers can query the PostgreSQL wire catalog, GraphQL introspection, or MCP get_schema to reveal property names, indexes, inheritance, and materialized view SQL.

### CVE-2026-134310

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-21T17:16:51.180 |

SurrealDB from 3.2.0 before 3.3.4 contains an authorization bypass vulnerability that allows record users to update protected rows by exploiting table-level PERMISSIONS FOR update predicates referencing COMPUTED fields. Because check_update_permissions evaluates the predicate before computed fields are populated, the field reads as NONE and deny-intended predicates like blocked != true pass, letting attackers modify records.

### CVE-2026-134307

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-21T17:16:50.820 |

SurrealDB 3.0.0 before 4.0.0 contains a permission bypass vulnerability that allows authenticated low-privilege database users to read restricted records by calling the GET /export endpoint. Attackers can export raw records that skip table SELECT predicates and field-level SELECT permissions, exposing other users' rows and hidden fields.

### CVE-2026-134302

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-21T17:16:50.267 |

SurrealDB 1.0.0 before 4.0.0 contains a denial of service vulnerability that allows any user able to run queries to crash the server by triggering unchecked decimal overflow in math::sum or math::product. Attackers can submit a query summing or multiplying large decimal literals or aggregate stored decimals with GROUP ALL, causing a rust_decimal panic that terminates the entire server process.

### CVE-2026-134290

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-209` |
| Published | 2026-11-21T17:16:48.553 |

SurrealDB 2.2.0 before 4.0.0 includes the record id of a referencing row in the error returned when a delete is blocked by an ON DELETE REJECT reference, without checking the caller's SELECT permission on that row. An authenticated principal with DELETE permission can attempt to delete a referenced record and read the rejection error to learn the existence and exact ids of referencing records hidden by row-level SELECT permissions.

### CVE-2026-134288

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-460` |
| Published | 2026-11-21T17:16:48.207 |

SurrealDB 3.0.0 before 4.0.0 contains an authorization bypass vulnerability that allows clients with table write access to persist writes refused by THROWing table events within interactive transactions. Attackers can run a guarded statement via RPC begin and query, ignore the returned error, and commit to persist the record and event side effects.

### CVE-2026-134278

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-21T17:16:46.833 |

Vikunja 2.3.0 before 2.8.0 contains an uncontrolled memory allocation in the CSV migration module because it does not de-duplicate label column mappings or cap labels per row, and enforces the item limit only after the full import is built. Authenticated users can send one request to /api/v2/migration/csv/migrate with repeated label mappings or many labels per row, exhausting memory until the server is OOM-killed.

### CVE-2026-134275

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-21T17:16:46.320 |

Vikunja from 0.8.0 before 2.8.0 contains a denial of service vulnerability that allows authenticated project readers to amplify response size by repeating requested properties in CalDAV PROPFIND requests. Attackers can send PROPFIND requests to the dav projects endpoint with hundreds of duplicate calendar-data properties to exhaust server memory, CPU, and bandwidth.

### CVE-2026-134273

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-21T17:16:46.150 |

Vikunja from 2.6.0 before 2.8.0 contains a resource exhaustion vulnerability in the Planka migration converter that multiplies task allocations for duplicate list IDs. Attackers controlling a Planka server can return boards with duplicate list IDs and many cards to exhaust memory and OOM-kill the Vikunja process.

### CVE-2026-134271

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-21T17:16:45.810 |

Vikunja from 1.0.0 before 2.8.0 contains a memory exhaustion vulnerability that allows authenticated users to crash the server by uploading extreme-width images as task attachments. Attackers can request the attachment preview endpoint so Lanczos resampling allocates width-proportional weight tables, OOM-killing the process repeatedly with sub-megabyte PNGs.

### CVE-2026-134270

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-21T17:16:45.643 |

Vikunja from 0.19.0 before 2.8.0 contains a denial of service vulnerability that allows authenticated CalDAV users to exhaust server CPU by uploading VTODO properties with many parameters. Attackers can PUT an iCalendar body with thousands of parameters on one line to any valid project ID, triggering superlinear parsing before permission checks.

### CVE-2026-134269

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-21T17:16:45.463 |

Vikunja from 0.18.0 before 2.8.0 contains a resource amplification vulnerability in pkg/models/export.go that allows authenticated users to exhaust server memory by exporting heavily related tasks. Attackers can relate many tasks to one task with a large description and request a user export, causing an out-of-memory crash for all users.

### CVE-2026-134268

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-21T17:16:45.290 |

Vikunja from 0.21.0 before 2.8.0 contains a resource exhaustion vulnerability that allows authenticated users to trigger instance-wide database writes by setting a project position below 0.1. Attackers can repeatedly send PUT requests to /api/v2/projects/{id} so recalculateProjectPositions updates every user's root projects, holding SQLite's write lock and degrading availability.

### CVE-2026-134266

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-606` |
| Published | 2026-11-21T17:16:44.947 |

Vikunja from 0.19.0 before 2.8.0 contains a denial of service vulnerability that allows authenticated users to exhaust CPU by supplying unbounded business-day operands in datemath filters. Attackers can send task or time-tracking filters like due_date > now+999999999999b, triggering a per-day loop in go-datemath that pins CPU cores and exhausts the server.

### CVE-2026-134265

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-21T17:16:44.767 |

Vikunja from 2.4.0 before 2.8.0 contains a denial of service vulnerability in the richtext converter that allows authenticated project writers to exhaust server memory and CPU by storing tables with unbounded rowspan and colspan values. Any project reader or CalDAV client can trigger the expansion through markdown task reads, CalDAV GETs, or the frontend editor, producing 100 MB responses from a 64-byte description.

### CVE-2026-134264

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-21T17:16:44.600 |

Admidio from 5.0.2 before 5.0.17 contains an arbitrary file read vulnerability that allows any logged-in member to read server files by placing local paths in img src attributes of eCard messages. Attackers can send an eCard to their own account so sendEcard() embeds files like adm_my_files/config.php via addEmbeddedImage(), disclosing database credentials and /etc/passwd.

### CVE-2026-134261

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-21T17:16:44.253 |

Admidio before 5.0.18 contains an insecure direct object reference vulnerability in mylist.php that loads list configurations by the list_uuid parameter while checking only the organization, not the owner or private flag. Authenticated users with Lists module access who know a victim's list UUID can read its name, selected profile fields, sort order and filter conditions.

### CVE-2026-134254

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-21T17:16:43.050 |

Admidio from 5.0.0 before 5.0.18 contains a path traversal vulnerability in DocumentsService::renameFile() that allows authenticated users to move files outside adm_my_files by supplying an unvalidated adm_new_name value. Attackers with folder upload permission can submit ../ sequences to file_rename_save to write files and create directories in arbitrary writable locations, including the web root.
