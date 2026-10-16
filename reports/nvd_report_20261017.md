# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-16 15:00 UTC
- **対象期間**: `2026-10-15T15:00:52.000Z` 〜 `2026-10-16T15:00:52.000Z`
- **重要CVE数**: 248 件（Critical 9.0+: 36 件 / High 7.0〜: 212 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE の多くは **Web アプリケーション（特に WordPress プラグイン）** と **コンテナ／ミドルウェア** に集中しており、リモートからのコード実行・特権昇格が共通の攻撃パターンです。  
- CVSS が 9.0 以上の脆弱性が 30 件以上報告されており、**認証不要** で実行できるものが半数以上と、外部から直接攻撃が可能なリスクが顕在化しています。  
- 特に **コードインジェクション／PHP オブジェクトインジェクション**、**任意ファイルアップロード**、**認証バイパス** が頻出で、攻撃成功時は機密情報漏洩、サーバ乗っ取り、ネットワーク全体への横展開が想定されます。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な脆弱種別 | 影響範囲・被害シナリオ | 推奨される対策（概要） |
|-----|------|--------------|------------------------|------------------------|
| **CVE‑2026‑94169** | 10.0 | Code Injection (Command Injection) | WordPress テーマ **Theme‑one The Grid**（≤ 2.8.1）で、管理画面から任意のシェルコマンドが実行可能。攻撃者はサーバ上で任意のプログラムを走らせ、データベース改竄やマルウェア設置が可能になる。 | 直ちに 2.8.2 以降へアップデート。アップデートが遅れる場合は、`the_grid` ディレクトリへの実行権限を削除し、WAF で `wp-admin/admin‑ajax.php` の `action=the_grid_*` パラメータをブロック。 |
| **CVE‑2026‑105037** | 9.9 | 任意ファイル読取（パス・トラバーサル） | EnergizeLab の **station‑middleware** Docker イメージ（1.6.5‑1.8.2）で、低権限ユーザーが任意のサーバファイルを取得可能。`/etc/passwd` や内部シークレットが漏洩し、さらなる権限昇格につながる。 | 1.8.3 以降のイメージに更新し、`READ_FILE` エンドポイントへのアクセスを RBAC で `admin` のみ許可。不要なボリュームマウントは削除し、`docker run --read-only` を検討。 |
| **CVE‑2026‑57155** | 9.9 | 任意ファイル書込（ディレクトリトラバーサル） | **OPNsense**（FreeBSD ベースのファイアウォール）<br>バージョン < 26.1.11 で GeoIP インポート時に CSV の `country_code` が検証されず、`/usr/local/s…` 以下に任意ファイルを書き込める。攻撃者はルート権限で任意コードを配置できる。 | 26.1.11 以降にアップデート。GeoIP インポート機能を無効化し、外部からの CSV アップロードは内部ネットワークからのみ許可。 |
| **CVE‑2026‑104730** | 9.8 | PHP Object Injection (Unserialize) | WordPress プラグイン **Sunshine Photo Cart**（≤ 3.7.4）で、未認証リクエストに対しシリアライズデータを受け付け、任意の PHP オブジェクトを注入できる。リモートコード実行や管理者権限取得が可能。 | 3.7.5 以降へ更新。プラグインが不要なら削除し、`php.ini` の `unserialize_callback_func` を安全なハンドラに設定。 |
| **CVE‑2026‑84731** | 9.3 | 認証バイパス（ヘッダーインジェクション） | **Nutanix Prism Element** の管理 API が特定の内部ヘッダーを検証せず、外部からのリクエストで認証を回避できる。攻撃者はフル管理権限を取得し、クラスタ全体を制御可能。 | Nutanix が提供するパッチ（バージョン X.Y.Z 以降）を適用。API エンドポイントは外部ネットワークから遮断し、内部だけに限定。ヘッダー検証をカスタム WAF で強化。 |

> **注**：上記は CVSS が最高値（10.0）または 9.8 以上で、**リモートから認証不要**、かつ **広範囲な権限取得** が可能なものを抜粋しています。  

---

## 3. 推奨アクション  

### 3.1 パッケージ・プラグインの即時更新
| 製品 / パッケージ | 現行脆弱バージョン | 修正バージョン | 更新方法 |
|-------------------|-------------------|----------------|----------|
| `theme-one/the-grid` (WordPress) | ≤ 2.8.1 | 2.8.2 以上 | WordPress 管理画面 → 「プラグイン」→「更新」または `composer require theme-one/the-grid:^2.8.2` |
| `energizelab/station-middleware` (Docker) | 1.6.5‑1.8.2 | 1.8.3 以上 | `docker pull energizelab/station-middleware:1.8.3 && docker compose up -d` |
| `opnsense` (FreeBSD) | < 26.1.11 | 26.1.11 以上 | `opnsense-upgrade -d` で公式リポジトリからアップデート |
| `sunshine-photo-cart` (WordPress) | ≤ 3.7.4 | 3.7.5 以上 | WordPress 管理画面 → 「プラグイン」→「更新」 |
| `nutanix-prism-element` | 影響ありバージョン | ベンダー提供パッチ（X.Y.Z 以降） | Nutanix Support へ問い合わせ、パッチ適用手順に従う |

### 3.2 共通的な防御策
- **WAF / IDS のルール強化**  
  - `the_grid` 系コマンド実行パラメータ、`/api/*` 系エンドポイントへの不正リクエストをブロック。  
  - `station-middleware` の `READ_FILE` API へのアクセスは `admin` ロールのみ許可し、IP 制限を追加。  
- **最小権限の原則 (PoLP) の徹底**  
  - WordPress の管理者アカウントは 2 要素認証 (2FA) を必須化。  
  - Docker コンテナは `--read-only`、

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-94169

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-16T07:17:14.297 |

Improper Control of Generation of Code ('Code Injection') vulnerability in Theme-one The Grid the-grid allows Command Injection.This issue affects The Grid: from n/a through 2.8.1.

### CVE-2026-105037

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-10-15T21:17:04.350 |

EnergizeLab station-middleware (NestJS) Docker images 1.6.5 through 1.8.2 allow any registered, low-privilege account to read arbitrary files from the server by supplying an attacker-controlled file path. This exposes middleware files and server secrets.

### CVE-2026-57155

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73;CWE-78` |
| Published | 2026-10-15T16:18:17.300 |

OPNsense is a FreeBSD based firewall and routing platform. Prior to version 26.1.11, the Firewall Alias GeoIP importer's process_zip() and process_gzip() paths in src/opnsense/scripts/filter/lib/alias/geoip.py use an unvalidated CSV country_code value to construct output filenames below /usr/local/share/GeoIP/alias. A user with Firewall Alias Edit privilege can configure an attacker-controlled GeoIP source URL and supply an archive whose country code traverses into another existing directory, causing attacker-controlled content to be written as root with an -IPv4 or -IPv6 suffix. A crafted newsyslog fragment and oversized log file can use the default hourly root cron job to execute commands as root, resulting in complete firewall compromise. This issue is fixed in version 26.1.11.

### CVE-2026-104730

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-16T07:17:08.267 |

The Sunshine Photo Cart – Client Photo Gallery & Photo Proofing for Photographers plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 3.7.4 via deserialization of untrusted input . This makes it possible for unauthenticated attackers to inject a PHP Object. No known POP chain is present in the vulnerable software, which means this vulnerability has no impact unless another plugin or theme containing a POP chain is installed on the site. If a POP chain is present via an additional plugin or theme installed on the target system, it may allow the attacker to perform actions like delete arbitrary files, retrieve sensitive data, or execute code depending on the POP chain present. If a POP chain is present via an additional plugin or theme installed on the target system, the attacker can store the malicious payload unauthenticated via the public favorites page and trigger deserialization by viewing any image in a non-viewable or private gallery.

### CVE-2026-89079

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-16T06:17:12.410 |

The Theme My Login plugin for WordPress is vulnerable to privilege escalation via account takeover in versions up to, and including, 7.2.1. This is due to the plugin not properly validating a user's identity prior to updating their password. This makes it possible for unauthenticated attackers to change arbitrary user's passwords on multi-site setups in certain configurations.

### CVE-2026-103768

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-16T06:17:03.060 |

The ELEX WordPress HelpDesk & Customer Ticketing System plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 3.3.7 via the initMailPart function. This is due to insufficient file type validation when saving IMAP email attachments. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible.

### CVE-2026-109515

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-16T05:17:29.597 |

The MailOptin – Popup, Optin Forms & Email Newsletters for Mailchimp, HubSpot, AWeber Etc. plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 1.2.78.6 This is due to the `subscribe_to_email_list` endpoint accepting an attacker-supplied `optin_data[form_custom_field_mappings]` parameter without any allow-list validation on destination keys, allowing the attacker-controlled mapping to override the administrator's saved mapping and pass arbitrary `wp_users` column names — including `ID` and `user_pass` — directly into `wp_insert_user()` via the `subscribe()` function. This makes it possible for unauthenticated attackers to force `wp_insert_user()` into UPDATE mode on any existing account by supplying a target user's numeric `ID`, overwrite that account's password with a pre-hashed value of their choosing, and thereby take over any WordPress user account — including administrators — leading to full site compromise. Exploitation requires that a WordPress User Registration opt-in form is published somewhere on the site, though the form's UUID is visible in page source and no authentication, nonce, or capability check is required to reach the vulnerable endpoint.

### CVE-2026-109219

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-16T05:17:29.100 |

The Mang Board plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 2.4.4 via the mbw_file_upload function. This is due to missing file extension validation on the attacker-supplied image_path parameter, whose basename-derived file name bypasses the extension allowlist applied only to the separate file_name parameter. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible. Exploitation requires the board to be configured to allow guest posts, which is the plugin's default mode; the required nonce is printed on every public board page, making it readable by any unauthenticated visitor without a WordPress login.

### CVE-2026-104798

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-16T05:17:28.580 |

The My Calendar – Accessible Event Manager plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 3.8.7. The public `mcs` GET parameter is reflected into post content unsanitized before WordPress core's `do_shortcode` filter runs, allowing an unauthenticated attacker to inject a nested `[my_calendar above=...]` shortcode; `mc_generate_calendar_nav()` then splits the `above` attribute on commas and dispatches each element via `call_user_func()` with no authentication, authorization, or callable allowlist check. This makes it possible for unauthenticated attackers to invoke arbitrary loaded PHP functions, enabling a call chain in which the shortcode `$params` array is passed to `edit_user()` — which PHP coerces to integer `1` as the `$user_id` argument — overwriting the credentials of the initial Administrator account (user ID 1) and granting the attacker full wp-admin access. Exploitation is trivially reachable via the plugin's auto-generated `/my-calendar/` page, which is publicly accessible by default upon plugin activation.

### CVE-2026-111444

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-16T04:18:30.353 |

Wheels through 4.1.2 allows SQL injection on MySQL/MariaDB with backslash escaping enabled (NO_BACKSLASH_ESCAPES absent) when an application supplies request data to inline-literal paths. These include opt-in parameterize=false queries and IN lists, and positions in developer-written where strings that the parser does not bind, such as BETWEEN bounds, function arguments and LIKE ESCAPE literals. Doubling single quotes without accounting for backslash escapes allows a value to alter the query. Bound paths are not affected; whereBetween() is bound from 4.1.2. This is fixed in 4.2.0.

### CVE-2026-105038

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-15T21:17:04.467 |

The EnergizeLab Eilik and EilikO FastAPI AI inference and profiling services expose AI model administration functions without authentication. An unauthenticated remote attacker can change AI model configuration and switch the model in use at runtime.

### CVE-2026-18516

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-116` |
| Published | 2026-10-16T14:17:24.710 |

An output escaping vulnerability in the Audit Logs component of Crafty Controller allows a remote, unauthenticated attacker to perform stored cross-site scripting via HTTP header injection

### CVE-2026-105039

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-15T21:17:04.587 |

EnergizeLab station-middleware (NestJS) Docker images 1.6.5 through 1.8.2 do not check user roles on administrative APIs. Any authenticated low-privilege user can retrieve AI provider keys and change configuration and object-store contents.

### CVE-2026-57496

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-15T19:17:41.733 |

NetLicensing MCP Server is a natural-language interface that enables agentic applications to manage the software-licensing lifecycle in Labs64 NetLicensing. Prior to 0.1.8, netlicensing_get_product passes the caller-controlled product_number to src/netlicensing_mcp/tools/products.py, which interpolates it into a REST path consumed by nl_get() in src/netlicensing_mcp/client.py without path-segment validation. A traversal segment can be normalized from the intended product path to the /token endpoint, after which the response is serialized through _wrap_json instead of _wrap_json_token_read, bypassing redact_token_read() protections for APIKEY number and SHOP shopURL fields. An authenticated MCP client with a non-administrative API key can retrieve plaintext token values, and a recovered administrative token can provide broad read, write, and delete access to the NetLicensing account. This issue is fixed in version 0.1.8.

### CVE-2026-111283

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-305` |
| Published | 2026-10-15T22:19:29.747 |

BMC Helix Network Management on-prem before 26.3.01 contains an authentication bypass vulnerability that allows unauthenticated attackers to log in as the local administrator with any password when SAML single sign-on is configured. Attackers can submit the administrator username with an arbitrary password on the web login page to obtain a SuperAdmin session, modify device credentials, run device commands, and alter audit records.

### CVE-2026-110812

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502;CWE-918` |
| Published | 2026-10-15T17:17:16.110 |

Deserialization of untrusted data in the Gremlin graph data import component in Amazon Neptune engine might allow an authenticated remote actor with standard database permissions to execute arbitrary code and access internal service credentials.



To remediate this issue, users not enrolled in auto-update should upgrade to Amazon Neptune engine version 1.5.0.0.(Backports to 1.4.8.1 and 1.4.7.1)

### CVE-2026-105474

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-10-15T16:17:34.373 |

A server-side template injection exists in SolusVM 2 up to version 2.0.0-44576 that allows remote authenticated users to execute arbitrary code as root.

### CVE-2026-107617

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-16T14:17:16.510 |

An attacker can use a hard-coded credential to log in to EseeCloud devices.

### CVE-2026-111472

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-16T09:17:04.410 |

An SQL injection vulnerability has been discovered in TSG Profleet. The vulnerability could allow an attacker to retrieve, create, update and delete data from the database by sending a GET request using the ‘Identificación’ parameter of the ‘/cgi-bin/index.php’ endpoint.

### CVE-2026-94388

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-16T07:17:14.430 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in halfdata Green Popups halfdata-green-popups allows Blind SQL Injection.This issue affects Green Popups: from n/a before 7.6.3.

### CVE-2026-111329

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-10-15T22:19:31.063 |

JuggleIM im-server through 1.8.16 ships default administrator credentials admin/123456 that allow unauthenticated remote attackers to access the admin console on port 8090. Attackers can log in as administrator, even after account deletion since CheckLogin recreates it, to control tenant applications and app secrets.

### CVE-2026-111322

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-15T22:19:30.633 |

Archon 0.2.13 through 0.11.1 contains a missing authentication vulnerability that allows unauthenticated attackers to access the /api/* control API, which binds to 0.0.0.0 by default. Attackers with network access can send messages to the AI coding agent, which runs with bypassPermissions, to execute commands on the host as the Archon user.

### CVE-2026-111281

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-15T22:19:29.457 |

Jooan JA-A12 IP cameras with firmware 009_20171107 and 05.02.31.105 contain a remote code execution vulnerability that allows unauthenticated attackers to run root commands via hard-coded credentials. Attackers send singleCMD=SetDiagMode to /goform/SingleHandlebyCommand with an attacker-chosen authserverip and authcode, making the jooandiag daemon execute their commands through /bin/sh, giving full device control.

### CVE-2026-102764

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-15T21:17:00.117 |

The vulnerability exists within internal components of BeyondTrust’s Remote Support product. The components did not adequately validate the origin of the messages it received. Under the right conditions, this could allow an attacker to perform file operations on the appliance.

### CVE-2026-47218

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-15T19:17:39.257 |

runwasi facilitates running Wasm and WASI workloads managed by containerd. Prior to 0.6.1, containerd-shim-wasmtime-v1 can treat Wasmtime precompiled bytes supplied directly in an OCI image layer as a trusted artifact from the precompile-cache path and deserialize them as native code. An attacker who causes a victim to run a crafted image can bypass WebAssembly validation and execute native code in the shim zygote process, gaining the filesystem, environment, credentials, networking, and Linux syscall access available to the workload container. Downstream shims built with runwasi's containerd-shim-wasm precompile-cache API are also affected if they implement Compiler and trust executable precompiled artifacts from OCI image layers; the 0.6.1 boundary applies specifically to containerd-shim-wasmtime and does not independently certify downstream product releases. The flaw escapes the WASI sandbox to the workload container boundary, but it does not by itself bypass container isolation or provide direct host code execution. This issue is fixed in version 0.6.1.

### CVE-2026-84731

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:Y/R:U/V:C/RE:H/U:Red` |
| Weaknesses | `CWE-290;CWE-302;CWE-306` |
| Published | 2026-10-15T18:17:29.960 |

An unauthenticated remote attacker can bypass authentication and gain full access to administrative API endpoints in Nutanix Prism Element by including a crafted internal management HTTP header. The vulnerability is caused by a misconfiguration in the application's authentication filters.



Consequently, the server responds with a Set-Cookie header containing a valid JSESSIONID. This session cookie decodes to a JSON Web Token (JWT) granting maximum cluster administrative privileges. Successful exploitation allows the attacker to execute root-level commands on all Controller VMs (CVMs) in the cluster, leading to complete cluster destruction and unauthorized access to VM memory and virtual disks.

### CVE-2026-110958

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-122` |
| Published | 2026-10-15T16:17:48.467 |

A vulnerability was found in Wavlink WN530HG4B M30HG4B_V260724. The impacted element is an unknown function of the file api.cgi. The manipulation results in heap-based buffer overflow. It is possible to launch the attack remotely. The exploit has been made public and could be used. Upgrading to version 2026-09-24-841a51c6d5_tclinux.bin is sufficient to resolve this issue. The affected component should be upgraded. The vendor confirms: "We confirm the finding, and it has already been addressed. In the current firmware the api=info&client=app handler no longer builds a shell command: the login script is now invoked through an argument vector (execvp) instead of system(), and the client address is length-limited and null-checked."

### CVE-2026-110957

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-10-15T15:17:30.640 |

A vulnerability has been found in Wavlink WL-WN530BE2-A up to M30BE2_V250604. The affected element is the function sub_12580 of the file api.cgi of the component Login Processing. The manipulation of the argument REMOTE_ADDR leads to os command injection. It is possible to initiate the attack remotely. The exploit has been disclosed to the public and may be used. Upgrading to version 2026-09-24-841a51c6d5_tclinux.bin is sufficient to fix this issue. You should upgrade the affected component. The vendor confirms: "We confirm the finding, and it has already been addressed. In the current firmware the api=info&client=app handler no longer builds a shell command: the login script is now invoked through an argument vector (execvp) instead of system(), and the client address is length-limited and null-checked."

### CVE-2026-111391

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-10-16T12:16:33.197 |

SGLang 0.5.10 through 0.5.22 contains a code injection vulnerability in _evaluate_filter() that allows remote attackers to execute Python code by escaping the eval() sandbox through re.search __globals__. Attackers can send a crafted filter expression to the unauthenticated /dumper/configure endpoint when DUMPER_SERVER_PORT is set, running code in the scheduler process on the next forward pass.

### CVE-2026-111312

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-15T22:19:30.053 |

OpenHealth through 0.2.0 contains a missing authentication and authorization vulnerability in the /api/health-data/[id] GET, PATCH and DELETE handlers that query records by id without session or authorId checks. Unauthenticated attackers who know a HealthData record id can read another user's medical record data and file metadata, overwrite it with arbitrary JSON, or delete it.

### CVE-2026-111356

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-10-15T22:19:33.647 |

MacCMS v10 through 2026.1000.4056 does not limit attempts on the six-digit password recovery code, allowing unauthenticated attackers to take over member accounts. Attackers knowing a victim's email or phone can request a code and brute-force findpass_reset to overwrite the member's password.

### CVE-2026-105032

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-434` |
| Published | 2026-10-15T21:17:03.753 |

The EnergizeLab Eilik and EilikO AI skill upload endpoint, served by the FastAPI AI inference and profiling services, does not require authentication and does not constrain uploaded file paths. An unauthenticated remote attacker can use path traversal to write arbitrary files, and thereby tamper with AI skill files used by Eilik and EilikO robots.

### CVE-2026-55240

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-10-15T19:17:40.290 |

Tianji is an open source analytics, uptime monitoring, and server status platform. Prior to 1.31.29, formatString() in src/server/utils/template.ts passes survey feedTemplate and monitor notification templates to lodash template(), while the default evaluate pattern remains enabled. A workspace administrator can store an evaluate block using the <% code %> form, and the public survey.submit endpoint renders a survey template when an unauthenticated user submits a response. The compiled template executes server-side JavaScript in the Tianji Node.js process, allowing command execution, secret disclosure, data modification, or service disruption. This issue is fixed in version 1.31.29.

### CVE-2026-111235

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-204;CWE-862;CWE-863` |
| Published | 2026-10-15T19:17:36.693 |

An authorization bypass vulnerability exists in the REST API of multiple versions of OpenNMS Meridian and Horizon. The /rest/** Spring Security filter chains authorize requests with intercept-url rules that name the HTTP method as an uppercase token, compare the method case-sensitively, and have no terminal deny rule. A request that uses a non-canonical (for example lowercase) method token matches no rule and is processed without authentication. A remote, unauthenticated attacker can read the monitored inventory and can create, modify, or delete resources through the REST API, which includes injecting events to fabricate or suppress alarms. The /rest/alarms chain has the same missing deny rule and discloses whether an alarm exists through a difference in the response. The fix adds a terminal deny rule to each REST filter chain.



The solution is to upgrade to Meridian 2024.3.14, 2025.0.11, 2026.0.1 and Horizon 36.0.5 or newer. Meridian and Horizon installation instructions state that they are intended for installation within an organization's private networks and should not be directly accessible from the Internet.

### CVE-2026-102946

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-290;CWE-345;CWE-347` |
| Published | 2026-10-15T19:17:13.423 |

joserfc is a Python library that provides an implementation of several JSON Object Signing and Encryption (JOSE) standards. Prior to 1.7.4, joserfc.jws.deserialize_json() accepts a JWS General JSON Serialization with an empty signatures array as authenticated. The verify_general_json() loop performs no iterations for the empty array and returns success because no signature check failed, allowing an attacker without a signing key to supply an arbitrary payload that relying applications may treat as authentic. The issue affects the General JSON Serialization path; compact JWS and JWT decoding, Flattened JSON serialization, and JWE JSON processing do not follow this vulnerable path. This issue is fixed in version 1.7.4.

### CVE-2026-47168

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-15T15:17:34.917 |

EspoCRM is an open source customer relationship management application. Prior to 9.3.7, an authenticated administrator can supply crafted serialized PHP object data that is stored in background MassAction or Export parameters and later deserialized by the application. The deserialization paths do not restrict allowed classes, allowing attacker-controlled object instantiation and arbitrary code execution on the server. This issue is fixed in version 9.3.7.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-62679

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-15T17:17:26.820 |

Lychee is a free, open-source photo-management tool. Prior to 7.6.4, SecurePathController, which serves GET /image/{path}, concatenates the attacker-controlled path with the local storage root and performs a string-prefix check before canonicalizing dot segments. Under the supported non-default configuration with temporary_image_link_enabled enabled, temporary_image_link_when_logged_in disabled, and secure_image_link_enabled disabled, any authenticated user can submit encoded traversal segments that pass the prefix check and are later resolved by filesystem operations. This permits reading files available to the web process, including application configuration and other users' private images, and disclosed APP_KEY or database credentials can enable further compromise. This issue is fixed in version 7.6.4.

### CVE-2026-111413

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-16T14:17:23.710 |

Cross-Site Request Forgery (CSRF) vulnerability in aThemeArt aThemeArt Theme Helper athemeart-theme-helper allows Cross Site Request Forgery.This issue affects aThemeArt Theme Helper: from n/a through 1.0.8.

### CVE-2026-109119

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-16T11:17:00.927 |

Improper Privilege Management in the user management API endpoint (/api/users/{username_or_id}) in Rdiffweb allows authenticated users to elevate their privileges to administrator by modifying the role parameter in a POST request.

### CVE-2026-111311

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-16T09:17:04.250 |

The DoubleScale | All-in-One CRM – Sales, Multi-Channel Marketing, Newsletter, Booking, Helpdesk, Automation, MCP & More plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 1.5.1 via the store_upload function. This is due to a fail-open extension allow-list in extension_is_allowed() that returns true when wp_check_filetype() yields an empty type for unrecognized extensions such as .php, combined with magic-byte-only MIME detection and no capability check beyond is_user_logged_in(). This makes it possible for authenticated attackers, with subscriber-level access and above, to upload files that may be executable, which makes remote code execution possible. Exploitation requires the Helpdesk module to be enabled, as the vulnerable REST endpoint is only registered when that module is active.

### CVE-2026-92553

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-16T07:17:14.150 |

The YaySMTP – WP Mail SMTP with Email Logs, Tracking & Reports plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 2.7.7 via the putFile function. This is due to insufficient file type validation in the putFile function, as sanitize_file_name() does not strip executable extensions and no allow-list, MIME check, or safe-extension rename is applied. This makes it possible for authenticated attackers, with subscriber-level access and above, to upload files that may be executable, which makes remote code execution possible. The only server-side guard is a .htaccess file containing 'Require all denied' written by writeGuards(), which is silently ignored by nginx and by Apache configured with AllowOverride None, meaning RCE is fully achievable on those server configurations.

### CVE-2026-92115

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-10-16T07:17:13.907 |

The WP Photo Album Plus plugin for WordPress is vulnerable to authenticated Command Injection in all versions up to, and including, 9.3.02.002 via the `value` parameter of the `update-photo` AJAX action. This is due to insufficient shell escaping within the `wppa_image_magick_a()` function, where the attacker-controlled `value` parameter is concatenated raw — without `escapeshellarg()` — into an ImageMagick command string before being passed to `exec()`; further, `wppa_decode()` actively restores percent-encoded shell metacharacters (e.g., `%26`→`&`, `%23`→`#`) rather than stripping them, allowing crafted payloads to survive sanitization and break out of the ImageMagick argument context. This makes it possible for authenticated attackers holding the plugin-defined `wppa_upload` capability to execute arbitrary operating-system commands as the web-server user, achieving full remote code execution on the underlying server. Exploitation requires ImageMagick to be enabled on the server; the `wppa_upload` capability is a plugin-level privilege that site administrators may grant to lower-privileged WordPress roles via the plugin's Users settings, broadening the pool of potential attackers beyond administrators.

### CVE-2026-85659

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-16T06:17:11.493 |

The PilotPress plugin for WordPress is vulnerable to Privilege Escalation via Account Takeover in all versions up to, and including, 2.0.43. The vulnerability exists because the `update_cc_details()` AJAX handler forwards an attacker-supplied `username` parameter to ONTRAPORT via `api_call('update_cc_details', ...)` before performing the local `username_exists()` collision check, and aborts without rolling back the remote rename when a collision is detected — leaving the remote ONTRAPORT contact renamed to an existing WordPress Administrator's login. On a subsequent login attempt, `user_login()` (hooked to `wp_authenticate`) authenticates against ONTRAPORT using the renamed login and the attacker's own password, resolves the local WordPress user row via `get_user_by('login', $username)` — which now selects the real Administrator's row — and calls `wp_set_password()` against that Administrator's user ID; because the `user_level != 10` guard only suppresses PilotPress's own cookie issuance rather than returning a `WP_Error` to core, WordPress proceeds to validate the newly-synchronized password and issues a full Administrator authentication cookie to the attacker. This makes it possible for authenticated attackers with Subscriber-level access and above — specifically any PilotPress member holding a valid ONTRAPORT contact and the Customer Center nonce — to fully take over an Administrator account.

### CVE-2026-111282

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-15T22:19:29.600 |

Driftregion iso14229 before 0.10.1 contains an integer wraparound in Handle_0x38_RequestFileTransfer that lets unauthenticated attackers bypass the file path length check. Attackers can send a short RequestFileTransfer (SID 0x38) request with filePathAndNameLength 0xFFFC-0xFFFF, causing callbacks to read past the receive buffer, crashing targets or disclosing memory.

### CVE-2026-110922

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-15T22:19:27.570 |

Use after free in Prerender in Google Chrome prior to 155.0.8059.84 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-110921

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-15T22:19:27.473 |

Use after free in V8 in Google Chrome prior to 155.0.8059.84 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110920

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-15T22:19:27.367 |

Memory corruption in V8 in Google Chrome prior to 155.0.8059.84 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110919

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-15T22:19:27.267 |

Use after free in V8 in Google Chrome prior to 155.0.8059.84 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110915

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-15T22:19:26.843 |

Use after free in Compositing in Google Chrome prior to 155.0.8059.84 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-110914

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-15T22:19:26.737 |

Memory corruption in Workers in Google Chrome prior to 155.0.8059.84 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-110913

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-15T22:19:26.620 |

Memory corruption in DOM in Google Chrome prior to 155.0.8059.84 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-108452

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-15T21:17:10.907 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-108451

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-10-15T21:17:10.790 |

Numeric truncation error in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108450

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-10-15T21:17:10.673 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108449

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T21:17:10.553 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108447

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T21:17:10.317 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108446

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-15T21:17:10.200 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-108445

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-15T21:17:10.077 |

Stack-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108444

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T21:17:09.957 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code over a network.

### CVE-2026-108443

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-193` |
| Published | 2026-10-15T21:17:09.840 |

Off-by-one error in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108442

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-15T21:17:09.727 |

Use after free in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108441

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T21:17:09.607 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108440

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-15T21:17:09.493 |

Stack-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108439

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T21:17:09.377 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108437

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T21:17:09.140 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108432

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T21:17:08.540 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108431

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-15T21:17:08.420 |

Stack-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108430

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T21:17:08.303 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108429

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T21:17:08.190 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108428

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T21:17:08.067 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108427

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122` |
| Published | 2026-10-15T21:17:07.947 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-108426

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T21:17:07.820 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-105040

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-15T21:17:04.703 |

The EnergizeLab Eilik NestJS auth service accepts a user-controlled user ID in account update requests (mass assignment). A registered user can set another account's identifier and take over that account.

### CVE-2026-105033

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-15T21:17:03.883 |

The EnergizeLab AI Station (RK3562) firmware image ships with default root credentials and SSH enabled. An attacker with network access to the device can log in as root and take full control of it.

### CVE-2026-106708

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-15T20:17:06.420 |

XXL-JOB 3.5.0-SNAPSHOT and earlier contains a Cross-Site Request Forgery (CSRF) vulnerability in the user management controller (JobUserController). The endpoints /user/insert, /user/update, and /user/delete lack CSRF protection and do not restrict HTTP method.

### CVE-2026-106700

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-15T20:17:06.297 |

ELADMIN v2.7 and earlier contains an improper access control vulnerability in the user-management endpoint PUT /api/users/resetPwd of me.zhengjie.modules.system.rest.UserController. The method lacks the method-level authorization check applied to all other user-management endpoints and performs no role-level or ownership validation in UserServiceImpl.resetPwd. Any authenticated user of any role can reset the password of arbitrary users, including the built-in administrator.

### CVE-2026-55239

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-15T19:17:40.143 |

Tianji is an open source analytics, uptime monitoring, and server status platform. Prior to 1.31.29, the getDateQuery() function in src/server/utils/prisma.ts constructs raw SQL through Prisma.sql() by interpolating the timezone request value without parameter binding. The timezone value can reach affected analytics queries through request data or the timezone HTTP header, and workspaceProcedure permits any authenticated workspace member, including a read-only viewer, to reach those queries. An attacker can execute arbitrary SQL against the shared PostgreSQL database, which can disclose or modify credentials, API keys, and tenant data or make the service unavailable. This issue is fixed in version 1.31.29.

### CVE-2026-85634

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-15T17:17:29.250 |

A flaw was found in the ContentRepositoryImpl.copyExplodedContent function of the wildfly-core library, which is used by WildFly and JBoss EAP to manage server deployments. The issue occurs when the library processes an unsanitized deployment name. Due to a missing containment check, an attacker with the Deployer RBAC role can use path traversal sequences to access files outside the restricted deployment directory. This can allow the attacker to delete arbitrary directories or create files with arbitrary content, leading to a full privilege escalation to the management SuperUser role.

### CVE-2026-107564

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-16T13:16:54.013 |

An unauthenticated remote attacker may use an allocation of resources without limits or throttling weakness in the affected product to cause high CPU load leading to a denial of service.

### CVE-2026-111382

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-16T03:18:05.400 |

FreeRDP before 3.32.0 contains a client-side heap out-of-bounds write vulnerability in general_LumaToYUV444 and general_ChromaV2ToYUV444 that allows malicious RDP servers to corrupt client memory. Attackers can send RDPGFX AVC444 or AVC444v2 frames with odd-height region rects ending at surface height to write past U/V planes, enabling heap corruption and potential code execution.

### CVE-2026-111380

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-16T03:18:05.123 |

FreeRDP from 3.29.0 before 3.32.0 contains an integer overflow in the Apple audin backends (audin_mac.m, audin_ios.m), which compute the audio queue buffer size as FramesPerPacket * 2 * nChannels in UINT32 arithmetic, bypassing the CVE-2026-91962 fix. A malicious RDP server can send FramesPerPacket of 2^30 in the audin Open PDU to wrap the multiplication, causing undersized AudioQueueAllocateBuffer allocations and a heap out-of-bounds write in macOS and iOS clients.

### CVE-2026-111378

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-16T03:18:04.850 |

FreeRDP from 3.0.0 before 3.32.0 contains an uncontrolled resource consumption vulnerability in parse_nla_mode_pdu that allows unauthenticated attackers to exhaust server memory. Attackers can complete TLS and stream bytes not beginning with the DER SEQUENCE tag 0x30, causing unbounded receive buffer growth before NLA authentication.

### CVE-2026-111352

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-15T22:19:33.043 |

ThinkCMF through 8.0.1 contains an incorrect authorization vulnerability in RestAdminBaseController that allows restricted backend administrators to call every admin REST API endpoint because Auth::check() fails open when no admin_api rule exists. Attackers with a valid admin-type API token can list member emails and mobile numbers, disable members, and call PUT admin/roles/{id}/authorize to grant themselves full administrator rights.

### CVE-2026-111279

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-10-15T22:19:29.157 |

Dragonfly through 2.0.2 contains an unbounded memory allocation vulnerability that allows unauthenticated clients to exhaust memory by passing a negative COUNT to HRANDFIELD, ZRANDMEMBER or SRANDMEMBER. Attackers can send a single command against a one-element key with a huge negative COUNT to trigger the OOM killer, terminating the instance for all clients.

### CVE-2026-111277

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-15T22:19:28.770 |

NivoCart through 2.5.1 contains a missing authorization vulnerability in the download() action of account/order that allows unauthenticated attackers to retrieve guest order invoices by supplying an order_id. Attackers can iterate the order_id parameter, which matches guest orders stored with customer_id 0, to disclose guest names, addresses, telephone numbers, emails, purchased items, and totals.

### CVE-2026-55872

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-15T19:17:41.303 |

GYM One is open-source gym management software for fitness centers, personal trainers, and sports clubs. Prior to 1.4.1, GYM One's admin/users/index.php renders the stored firstname, lastname, and email profile fields into the administrator user list without HTML output encoding. An attacker who can store values in those fields can cause content to execute in an administrator's browser when the administrator visits /admin/users/. The persistent script can access administrator-session data or perform actions with the administrator's privileges until the stored record is removed. This issue is fixed in version 1.4.1.

### CVE-2026-111160

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-15T19:17:31.100 |

LightLLM through 1.2.0 contains a denial of service vulnerability that allows unauthenticated attackers to crash the inference worker by supplying the internal pd_kv_trans_params field to the /generate endpoint. Attackers can send a single request whose parameters cause pickle.loads to fail in InferSamplingParams, killing the inference thread while /health stays up and all later requests hang until restart.

### CVE-2026-104150

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-10-15T19:17:14.603 |

AdonisJS HTTP Server is a package for handling HTTP requests in the AdonisJS framework. Prior to 8.2.2 and 9.1.1, the regular expression returned by router.matchers.slug() contains adjacent greedy repetitions with overlapping character classes. When an application applies this matcher to an attacker-controlled route parameter, a long slug ending in a character rejected by the final assertion causes quadratic backtracking and excessive CPU use. Route matching occurs before route and group middleware, so authentication or rate-limiting middleware attached to the route may not prevent an unauthenticated request from blocking the Node.js event loop and stopping the worker from serving unrelated requests or health checks. This issue is fixed in versions 8.2.2 and 9.1.1.

### CVE-2026-97712

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-15T16:18:26.137 |

Sonatype Nexus Repository 3 allows a user that holds the role create or role update permission to grant roles and privileges that the account does not hold. This can give the user more access than intended, up to full administrative access.

### CVE-2026-109449

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-15T16:17:43.963 |

In Symfony Expression Language versions prior to 5.4.54, 6.4.48, 7.4.21, and 8.1.9, the parser of the ExpressionLanguage component built its node tree with no bound on its depth. An expression made of tens of thousands of nested unary operators, array literals, binary operators or property accesses crashed the PHP process, while the tree was being freed.


#[Assert\ExpressionSyntax] passes the validated value to ExpressionLanguage::lint(), so an application validating expressions written by its users could be crashed by a single request, and so could any code parsing untrusted expressions.

This issue affects symfony/expression-language through v5.4.53, v6.0.0-BETA1 through v6.4.47, v7.0.0-BETA1 through v7.4.20, and v8.0.0-BETA1 through v8.1.8.

### CVE-2026-109413

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-15T15:17:24.993 |

In Symfony YAML prior to versions 5.4.54, 6.4.45, 7.4.18, and 8.1.6, Yaml\Parser::lexInlineStructure() recursed through lexInlineMapping() and lexInlineSequence() for every { and [ of an inline collection, without entering the nesting level that the rest of the parser bounds with maxNestingLevel. A document made of deeply nested inline collections, such as [[[[...]]]], exhausted the stack while it was being lexed: depending on the PHP version and its stack settings, the process crashed or the request ended with a fatal error.



Any code parsing untrusted YAML is affected. That includes #[MapRequestPayload] when the Yaml component is installed and the endpoint does not restrict acceptFormat: a single unauthenticated request with a YAML content type is enough.



This issue affects symfony/yaml through v5.4.53, v6.0.0-BETA1 through v6.4.44, v7.0.0-BETA1 through v7.4.17, and v8.0.0-BETA1 through v8.1.5.

### CVE-2026-108082

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-15T15:17:22.583 |

Symfony is a PHP framework for web and console applications and a set of reusable PHP components. Prior to versions 5.4.54, 6.4.46, 7.4.19, and 8.1.7, HeaderUtils::split() parsed header values with a pattern whose token alternative also matched whitespace, followed by a (?<!\s) lookbehind. A run of whitespace placed before a separator could be divided among the iterations of the enclosing repetition in exponentially many ways, and the engine tried all of them before settling. HeaderBag calls it for the Cache-Control header whenever a Request is built, so any application handling HTTP requests is reachable, with no authentication.



A single request carrying such a header costs close to a second of CPU (813 ms for a run of 17 spaces in an 8 KB header on PHP 8.5, doubling with each extra space). From 18 spaces on, preg_match_all() gives up at pcre.backtrack_limit and split() returns an empty array, so every directive of the header is silently dropped.



This issue affects symfony/http-foundation v4.1.0-BETA1 through v5.4.53, v6.0.0-BETA1 through v6.4.45, v7.0.0-BETA1 through v7.4.18, and v8.0.0-BETA1 through v8.1.6.

### CVE-2026-14452

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-10-16T10:18:05.653 |

Improper validation of the reset_url parameter of the Setup in-page search in Checkmk <2.5.0p15, <2.4.0p38, <2.3.0p51 and 2.2.0 (EOL) allows an attacker to execute arbitrary script in the session of an authenticated user with Setup access, or to redirect that user to an arbitrary external site, by tricking the user into opening a crafted URL and clicking the Reset button or submitting an empty search.

### CVE-2026-111446

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-16T04:18:30.763 |

Wheels 4.0.0 through 4.1.2 exposes password-less development tools under /wheels/* to remote clients when enablePublicComponent=true, as it is by default in development. Before 4.1.2 these tools have no local-access restriction; in 4.1.2 the restriction trusts client-supplied headers without checking the connecting peer. Remote clients can obtain application settings, environment/datasource details and routes, and start test runs. Where application tests use the primary datasource, those runs can write to the real application database. The separately protected migrator and CLI endpoints are not affected. This is fixed in 4.2.0.

### CVE-2026-109813

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-16T03:18:02.277 |

A hard-coded cryptographic key vulnerability exists in the `/usr/bin/sysman` of some of Moxa's industrial computing products. An unauthenticated attacker with adjacent network access could exploit the exposed private key material to compromise the confidentiality and integrity of communications.

### CVE-2026-75941

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-16T00:17:05.420 |

A potential vulnerability was reported in the Lenovo Legion Zone application, distributed exclusively in the Chinese market, that could allow an attacker on the same logical network to execute arbitrary code.

### CVE-2026-111366

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-15T22:19:34.557 |

cool-admin-midway through 8.0.0 contains an authorization bypass vulnerability that allows department-limited admins to manage users outside their departments by supplying arbitrary user ids. Attackers holding sys:user:* permissions can call /admin/sys/user/info, update, or delete to read records, reset passwords and roles, or delete accounts.

### CVE-2026-45165

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:N/R:U/V:D/RE:M/U:Amber` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-15T19:17:38.653 |

An authorization flaw in Idira Conjur version 13.9.0 allows an authenticated user with limited privileges to perform unauthorized actions on a policy branch. Under specific circumstances, an attacker could potentially leverage this to retrieve unauthorized secrets, alter administrative access controls on the branch or cause a denial of service (DoS). Idira Security Bulletin CA26-38.

### CVE-2026-111231

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-15T19:17:36.110 |

Netgate pfSense CE through 2.9.0 contains an authorization bypass vulnerability that allows read-only WebGUI users to replace config.xml because config_restore() and config_install() ignore the 'User - Config: Deny Config Write' privilege. Attackers holding page privileges for services_acb.php, uploadconfig.php, diag_confbak.php, or diag_backup.php can install a chosen config.xml to gain root-level code execution after reload or reboot.

### CVE-2026-111229

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-15T19:17:35.813 |

pfSense CE 2.7.0 through 2.9.0 contains a command injection vulnerability in services_captiveportal_hasync.php that allows users with only the Captive Portal HA privilege to execute commands as root. Attackers can set backwardsyncip to a malicious XMLRPC server returning connected_users with shell metacharacters in ip or mac fields, which captiveportal_load_pfctl passes unescaped to a pfctl shell command.

### CVE-2026-111226

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-15T19:17:35.373 |

pfSense CE 2.4.5 through 2.9.0 contains an OS command injection vulnerability that allows authenticated WebGUI users with Advanced Admin Access privilege to execute commands as root via Login Protection settings. Attackers can submit sshguard threshold, block time, or detection time values containing newlines or $(...) that are written unvalidated to sshguard.conf and sourced as root on restart.

### CVE-2026-111223

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-10-15T19:17:34.943 |

Netgate pfSense CE 2.7.0 through 2.9.0 contains a configuration injection vulnerability that allows authenticated users with IPsec Mobile privileges to execute commands as root via the login_banner field. Attackers can submit a single-line banner containing '}' to escape the unquoted strongswan.conf attr value and define charon.start-scripts entries that charon executes as root on restart.

### CVE-2026-111220

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-10-15T19:17:34.500 |

pfSense CE through 2.9.0 contains a crontab injection vulnerability in interfaces_ppps_edit.php that allows authenticated users to execute commands as root by injecting newlines into the ptpid or reset hour/minute fields. Attackers holding the 'WebCfg - Interfaces: PPPs: Edit' privilege can submit crafted POST values that configure_cron() writes unescaped into /etc/crontab, running arbitrary root commands on schedule.

### CVE-2026-111218

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-15T19:17:34.210 |

Netgate pfSense CE 2.7.0 through 2.9.0 contains an OS command injection vulnerability that allows authenticated users with Traffic Shaper Limiters privileges to execute root commands by tampering with the limiter number field. Attackers can submit a malicious hidden 'number' value when editing a limiter, then delete it so delete_queue() passes the unquoted value to dnctl via /bin/sh as root.

### CVE-2026-111217

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-15T19:17:34.067 |

Netgate pfSense CE through 2.9.0 contains an OS command injection vulnerability that allows authenticated users with Virtual IP edit privileges to execute commands as root by storing an unvalidated CARP VHID. Attackers can supply a VHID containing shell metacharacters that executes via interface_ipalias_configure() ifconfig calls or get_carp_interface_status() when CARP status is rendered.

### CVE-2026-111216

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-15T19:17:33.907 |

Netgate pfSense CE through 2.9.0 contains an OS command injection vulnerability that allows authenticated users with gateway edit privileges to execute commands as root by injecting shell metacharacters into an IPv6 link-local zone index. Attackers can set a gateway Monitor IP whose unvalidated zone carries a payload, which start_dpinger() passes unescaped to the dpinger shell command when monitoring is applied.

### CVE-2026-111215

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-15T19:17:33.757 |

Netgate pfSense CE through 2.9.0 contains an OS command injection vulnerability that allows authenticated users to execute commands as root by supplying a crafted wireless parent interface name. Attackers with limited Wireless Edit or Interface Assignments privileges can submit values like ath0;<cmd> via interfaces_wireless_edit.php or interfaces_assign.php, which interface_wireless_clone() interpolates unescaped into an ifconfig shell command.

### CVE-2026-111214

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-15T19:17:33.603 |

Netgate pfSense CE 2.7.0 through 2.9.0 contains an OS command injection vulnerability that allows authenticated users with QinQ edit privilege to run commands by storing an unvalidated parent interface name. Attackers can save a crafted 'if' value, then edit the QinQ entry so it is interpolated into ifconfig shell commands, executing commands as root.

### CVE-2026-55103

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-345;CWE-863` |
| Published | 2026-10-15T18:17:27.163 |

Discourse ActivityPub adds ActivityPub support to Discourse. Prior to commit 1c8518b0f2abdf31cbea3e0b242f74d8994a9ba5, inbound ActivityPub processing does not sufficiently verify that the actor authenticated by the signed request matches the Activity actor and owns the referenced federated post. A remote attacker can exploit these missing identity and ownership checks to edit, delete, or reply to federated posts without the required permissions. This vulnerability is fixed with commit 1c8518b0f2abdf31cbea3e0b242f74d8994a9ba5.

### CVE-2026-111399

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-16T13:16:55.733 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in PT Norther Lights Production MapSVG mapsvg-lite-interactive-vector-maps allows SQL Injection.This issue affects MapSVG: from n/a through 8.16.1.

### CVE-2026-92982

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-10-15T16:18:23.657 |

A flaw was found in Ansible Operator Plugins. A low-privileged Kubernetes user can exploit a Jinja2 template injection vulnerability by crafting malicious custom resource (CR) specification values. These values are processed by Ansible without proper sanitization, allowing embedded Jinja2 expressions to be executed within the operator pod. This can lead to arbitrary code execution and privilege escalation, granting the attacker control over the operator's service account with cluster-wide permissions.

### CVE-2026-103509

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1220` |
| Published | 2026-10-15T15:17:20.757 |

P4 Search (formerly Helix Search) returns stored credentials in cleartext through its configuration API to users with administrative privileges on the connected P4 Server, allowing privilege escalation.
This affects 2026.4.2 and earlier and is fixed in 2026.4.3.

### CVE-2026-110936

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-10-15T15:17:30.383 |

A vulnerability has been identified in Siemens Software Center (All versions). The affected application loads dynamic-link libraries (DLLs) from an uncontrolled search path. This could allow an authenticated local attacker to place a specially crafted DLL in a directory that the application searches, leading to arbitrary code execution with the privileges of the affected application.

### CVE-2026-111389

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-16T03:18:06.540 |

Frappe HRMS 14.x before 14.38.2, 15.x before 15.64.0, and 16.x before 16.18.0 contains a SQL injection vulnerability in some endpoints caused by missing input validation. Any authenticated attacker, including a low-privilege account, can send specially crafted requests to these endpoints to extract sensitive information from the database.

### CVE-2026-111280

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-15T22:19:29.317 |

snap7 through 1.4.3 contains an out-of-bounds write vulnerability in TSnap7MicroClient::opReadArea() that allows malicious S7 peers to overflow client buffers via an unchecked DataLength field. Rogue or impersonated PLCs can return crafted ReadVar responses causing memcpy of up to 65535 bytes into caller buffers, crashing SCADA, HMI, or gateway processes and corrupting memory.

### CVE-2026-77470

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-472;CWE-915` |
| Published | 2026-10-15T17:17:27.997 |

Lychee is a free, open-source photo-management tool. Prior to 7.7.1, the Supporter or Pro webshop POST /api/v2/Shop/Checkout/Process flow accepts an unrestricted additional_data array and CheckoutService::preparePurchaseParameters() merges it after server-computed purchase parameters. Because later string keys overwrite earlier keys, an unauthenticated buyer can replace amount, currency, returnUrl, cancelUrl, or transactionId before CheckoutService::processPayment() passes the parameters to a non-PayPal Omnipay gateway. An attacker can therefore make a gateway accept a successful payment for an attacker-selected amount and obtain auto-fulfilled goods while underpaying the merchant. The issue requires an enabled webshop, a purchasable item, and an affected Omnipay gateway. This issue is fixed in version 7.7.1.

### CVE-2026-77466

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-184` |
| Published | 2026-10-15T17:17:27.580 |

Lychee is a free, open-source photo-management tool. Prior to 7.7.0, Lychee hides the Omnipay Dummy test provider from the checkout options in production through OmnipayFactory::get_supported_providers(), but CreateSessionRequest validates only that the submitted provider is an OmnipayProviderType and does not enforce OmnipayProviderType::isAllowed(). A buyer, including a guest when webshop_allow_guest_checkout is enabled, can submit Dummy directly and complete the test gateway flow without a real payment. When webshop_auto_fulfill_enabled is enabled, OrderCompletedListener::fullfillOrder() can then release the purchasable item. The issue requires access to the Supporter or Pro webshop and an enabled purchasable item. Testing bypassed the closed-source license middleware, so whether the real license layer performs additional payment-provider validation remains unverified. The payment finalize status check itself is not the root cause. This issue is fixed in version 7.7.0.

### CVE-2026-45452

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-134` |
| Published | 2026-10-15T16:18:11.983 |

Use of Externally-Controlled format string vulnerability in Unitronics Unitronics UniStream Pro/UniLogic.

This issue affects Unitronics UniStream Pro/UniLogic: Unitronics UniStream Pro versions only (B10 / C10) – UniLogic versions prior to 1.41.329.

### CVE-2026-45451

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-15T16:18:11.787 |

: Improper Authentication vulnerability in Unitronics Unitronics UniStream Pro/UniLogic.

This issue affects Unitronics UniStream Pro/UniLogic: Unitronics UniStream Pro versions only (B10 / C10) – UniLogic versions prior to 1.41.329.

### CVE-2026-45450

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-15T16:18:11.617 |

: Improper Restriction of Operations within the Bounds of a Memory Buffer vulnerability in Unitronics Unitronics UniStream Pro/UniLogic.

This issue affects Unitronics UniStream Pro/UniLogic: Unitronics UniStream Pro versions only (B10 / C10) – UniLogic versions prior to 1.41.329.

### CVE-2026-45449

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-15T16:18:10.993 |

: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability in Unitronics Unitronics UniStream Pro/UniLogic.

This issue affects Unitronics UniStream Pro/UniLogic: Unitronics UniStream Pro versions only (B10 / C10) – UniLogic versions prior to 1.41.329.

### CVE-2026-111347

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-15T22:19:32.300 |

go-ldap-admin through 0.6.2 embeds a hard-coded RSA private key, published in the public repository, that protects encrypted login passwords. Unauthenticated attackers who capture encrypted passwords can decrypt them offline or via the /base/decryptpwd endpoint, recovering cleartext LDAP credentials for reuse.

### CVE-2026-111330

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-916` |
| Published | 2026-10-15T22:19:31.210 |

JuggleIM im-server through 1.8.16 contains a weak password hashing vulnerability that stores admin console passwords as unsalted SHA-1 digests via tools.SHA1 in services/accountservice.go. Attackers who obtain the accounts table through database access or backups can crack console passwords using precomputed tables or GPU brute force.

### CVE-2026-105034

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-10-15T21:17:03.997 |

The EnergizeLab Eilik NestJS auth service issues device tokens for arbitrary robot serial numbers without authentication. An unauthenticated remote attacker can obtain a valid device token for any serial number and act as that device against the cloud services.

### CVE-2026-111234

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-10-15T19:17:36.543 |

SimplePie through 1.9.0 contains a local file read vulnerability that allows malicious feed servers to read server files by supplying file:// URLs in redirects or autodiscovery links. Attackers can return a Location header or feed link pointing to a file:// path, causing file_get_contents() to read files accessible to the web server process.

### CVE-2026-61838

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-639` |
| Published | 2026-10-15T17:17:26.677 |

Lychee is a free, open-source photo-management tool. Prior to 7.6.3, GET /api/v2/Zip authorizes album and photo archives through AlbumPolicy::canDownload() and PhotoPolicy::canDownload() without first enforcing AlbumPolicy::canAccess(). For a public, password-protected album with grants_download enabled, an unauthenticated attacker who knows the shared album identifier can download a ZIP archive without supplying the password or unlocking the album, even though browsing endpoints deny access. The archive exposes the album's photos and can include full-resolution originals and associated metadata when grants_full_photo_access is enabled. This issue is fixed in version 7.6.3.

### CVE-2026-100349

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-15T16:17:30.640 |

kin-openapi is a Go project for handling OpenAPI files. Prior to 0.146.0, openapi3filter.ValidateResponse passes a nil response header schema to decodeValue when an OpenAPI document declares the header with content instead of schema. The document passes validation, but every response validation for the affected operation dereferences the nil schema and panics even when the response does not contain the declared header. Applications that ingest an untrusted specification can expose this as remote availability impact, while applications using only trusted local specifications still crash when the affected operation is exercised. This issue is fixed in version 0.146.0.

### CVE-2026-75903

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-16T08:17:13.513 |

The Vulnity Security plugin for WordPress is vulnerable to authentication bypass in all versions up to, and including, 1.4.3 This is due to insufficient protection of the delegated-login pairing credential file on Nginx-based installations, where the plugin's generated server configuration snippet guards the wrong directory path. This makes it possible for unauthenticated attackers to retrieve the stored credentials, forge signed REST API requests, and log in as an administrator.

### CVE-2026-97296

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-16T07:17:14.693 |

Deserialization of Untrusted Data vulnerability in Rocketgenius, Inc Gravity Forms gravityforms allows Object Injection.This issue affects Gravity Forms: from n/a before 3.1.1.

### CVE-2026-109447

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-16T06:17:08.020 |

The User Profile Builder – Beautiful User Registration Forms, User Profiles & User Role Editor plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 4.0.3 via the `role` parameter handled by the `wppb_add_meta_to_user_on_activation()` function. The vulnerability exists because the activation handler passes the attacker-supplied role value directly to `WP_User::set_role()` with no allow-list validation, and the 4.0.3 reserved-name check exempts pre-existing form fields from the block, allowing a legacy field with meta-name `role` to persist and bridge attacker-controlled request input into the serialized signup record stored in `wp_signups`. This makes it possible for unauthenticated attackers to gain a fully activated WordPress administrator account by submitting `role=administrator` through the public `[wppb-register]` shortcode form and subsequently clicking the confirmation activation link. Exploitation requires the site to have a legacy form field with meta-name `role` carried over from before the 4.0.3 upgrade, email confirmation enabled, and open user registration — all stable site-state conditions once established.

### CVE-2026-109221

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-16T05:17:29.227 |

The Groundhogg — CRM, Newsletters, and Marketing Automation plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the copy_file function in all versions up to, and including, 4.9.3 This makes it possible for authenticated attackers, with Sales Representative-level access and above, to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). This is exploitable by any user holding the plugin-defined import_contacts capability, which is granted by default to the plugin's custom Sales Representative role.

### CVE-2026-103895

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-16T05:17:28.333 |

The miniOrange OTP Login, Verification and SMS Notifications plugin for WordPress is vulnerable to Authentication Bypass in versions up to, and including, 5.5.8 via the `mo_by_pass_login()` function. This is due to `mo_delay_otp_process()` short-circuiting the authentication flow before password validation or the administrator intent gate (added in 5.5.6) can run, combined with the Delay OTP grace flag (`mov_last_verified_dttm`) being stored as a `user_meta` row keyed solely by target user ID with no binding to the originating session, cookie, IP address, or device. This makes it possible for unauthenticated attackers to authenticate as any WordPress user — including administrators — by submitting only a known username with the `mo_wp_login_intent=otp` parameter and any non-empty password, thereby inheriting a legitimate user's open Delay OTP grace window without ever supplying correct credentials. Exploitation requires the site to have OTP-only login (`wp_login_skip_password=1`, `wp_login_skip_password_fallback=0`) and Delay OTP Verification (`wp_login_delay_otp=1`) enabled, and the target account must currently be within its configured Delay OTP interval.

### CVE-2026-111447

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-472` |
| Published | 2026-10-16T04:18:30.960 |

Wheels 1.1 through 4.1.2 resolves nestedProperties() records by posted primary key without checking that they belong to the parent being saved. A user able to submit a nested form for their own parent can update and reassign another parent's hasMany or hasOne rows, or delete them when allowDelete=true. Nested belongsTo records can also be edited by posting another associated record's key. New child rows with composite primary keys not made up of foreign keys retain posted key values, allowing the request to choose their identity. This is fixed in 4.2.0.

### CVE-2026-111445

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-669` |
| Published | 2026-10-16T04:18:30.563 |

Wheels 4.0.0 through 4.1.2 before 4.2.0 replaces incoming scope conditions with a primary-key condition in findByKey() and exists(key=). For exists(key=), production with error information disabled returns true for an out-of-scope key instead of throwing. Applications relying on scopes for ownership or tenant authorization can therefore load and subsequently modify or delete another user's or tenant's record when the key comes from a request. The 4.2.0 fix combines key conditions with incoming scope, query-builder or where conditions in findByKey(), exists(key=), updateByKey() and deleteByKey(). Other scope-aware finders, aggregates, updateAll() and deleteAll() are not affected.

### CVE-2026-104745

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-16T04:18:21.607 |

The Customer Email Verification for WooCommerce plugin for WordPress is vulnerable to Privilege Escalation via the `alg_wc_ev_verify_email` parameter in versions up to, and including, 3.3.0. The vulnerability exists because `alg_wc_ev_generate_user_code()` generates the per-user activation secret using `wp_rand(100)` when the plugin's 'Encoding method' is set to 'hashids', producing only ~101 possible values (~7 bits of entropy); the resulting token is a reversible Hashids encoding with no cryptographic MAC, and the unauthenticated `verify()` handler — hooked to `init` at `PHP_INT_MAX` with no nonce check and no rate limiting — accepts and acts on the attacker-controlled `?alg_wc_ev_verify_email=` GET parameter directly. This makes it possible for unauthenticated attackers to gain authentication as any unverified WordPress account, including administrator-level accounts, by brute-forcing the trivially small activation code space via a forged verification URL. Exploitation requires that the 'Encoding method' setting be changed to 'hashids' (non-default), that the attacker recover or brute-force the Hashids salt (which defaults to an `md5(time())` value set at first initialization), and that the target account's email address remain unverified.

### CVE-2026-55587

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-10-15T19:17:40.657 |

AliasVault is a privacy-first password manager with built-in email aliasing. Prior to 0.29.4, the AliasVault browser extension passkey provider does not bind passkey requests to the actual webpage origin or verify that the requested relying-party identifier matches the current website. A malicious website can provide forged origin and relying-party values and, if a victim with a matching stored passkey approves the AliasVault passkey prompt, obtain a valid assertion for a different website. Exploitation requires the extension to be installed, unlocked, and configured as a passkey provider, requires a stored passkey for the impersonated site, and cannot occur silently because the victim must approve the prompt. The server, web application, and mobile applications are not affected. This issue is fixed in version 0.29.4.

### CVE-2026-63442

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-117` |
| Published | 2026-10-15T16:18:19.157 |

OPNsense is a FreeBSD based firewall and routing platform. Prior to version 26.1.11, the unauthenticated WebGUI login usernamefld accepts carriage-return and line-feed characters that survive LOG_AUTH processing through syslog-ng-lockout.conf into the syslog-ng program destination feeding lockout_handler. The consumer's readline() processing treats an injected fragment as a separate authentication event and selects the first syntactically valid IP address from the forged line. An attacker with network access to the login page can forge failure events for another IP, causing that IP to be added to the sshlockout PF table and its active states to be killed, or forge accepted events that reset an attacker's own brute-force counter. This can block administrative, DNS, gateway, or monitoring addresses and can bypass password-guessing lockout without authentication. This issue is fixed in version 26.1.11.

### CVE-2026-111094

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-15T16:17:48.993 |

In JetBrains TeamCity before 2026.2, 
2026.1.4, 
2025.11.8 remote code execution via a whitelist bypass in the build messages protocol was possible

### CVE-2026-104932

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-16T06:17:05.590 |

The Search Regex plugin for WordPress is vulnerable to PHP Object Injection in version 3.5 via deserialization of untrusted input in the replace_all function. This allows authenticated attackers, with subscriber-level access and above, to inject a PHP Object. The additional presence of a POP chain allows attackers to execute code.

### CVE-2026-93953

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-16T04:18:43.143 |

The Backuply – Backup, Restore, Migrate and Clone plugin for WordPress is vulnerable to SQL Injection via the Biographical Info field (second-order, via restore) in all versions up to, and including, 1.5.8 due to insufficient escaping on the user supplied parameter and the lack of sufficient preparation on an existing SQL query. Backuply exports the Biographical Info value verbatim inside an INSERT statement written to the backup's SQL dump (wp_usermeta). When an Administrator later restores such a backup, the crafted payload breaks out of that INSERT statement and appends attacker-controlled SQL that executes with full database privileges. This makes it possible for authenticated attackers, with subscriber-level access and above, to write arbitrary data to the database — in particular to update the default_role option in wp_options to administrator (and enable open user registration) — so that a subsequently registered account is automatically granted the Administrator role, resulting in privilege escalation and full site takeover. Because the injection executes inside an INSERT during restore with no response returned to the attacker, the primitive is used to modify database records rather than to read existing data directly.

### CVE-2026-58390

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-15T16:18:17.890 |

OPNsense is a FreeBSD based firewall and routing platform. Prior to version 26.1.11, the OpenVPN connection-status dashboard widget in src/opnsense/www/js/widgets/OpenVPNClients.js and the connection-status view place a client common_name into data-common-name attributes without quote-safe encoding. Exploitation requires an OpenVPN server configured with username-as-common-name and RADIUS or LDAP authentication, plus the ability to provision or self-register a valid backend username containing a double quote; deployments where the same administrator controls both the identity backend and firewall do not cross a separate trust boundary. An authenticated client using that username can close the attribute and add an event handler, while the local user database is not affected because its username validator rejects quotes. Script executes in an administrator's session when the administrator opens the dashboard or connection-status page and the injected event is triggered; the demonstrated payload used pointer movement over the client row rather than unconditional page-load execution. The advisory demonstrates that the script can read config.xml, invoke privileged APIs, reset the root password, and obtain root command execution. This issue is fixed in version 26.1.11.

### CVE-2026-111095

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-15T16:17:49.103 |

In JetBrains TeamCity before 2026.2, 
2026.1.4, 
2025.11.8 stored XSS in the classic project overview was possible

### CVE-2026-104715

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-16T07:17:08.090 |

A flaw was found in cifs-utils. This flaw allows an unprivileged local user to achieve privilege escalation. When a privileged service mounts a Common Internet File System (CIFS) share using a user-controlled credentials file, input values are not properly sanitized before being assembled into mount options. A local attacker can exploit this vulnerability to inject unauthorized mount options, allowing them to bypass permission checks and execute files with administrative (root) privileges.

### CVE-2026-111451

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-16T04:18:31.667 |

Wheels CLI 4.0.0 through 4.1.1 insufficiently validates or escapes caller-supplied values and package contents. Deploy release/version/rollback values can execute shell commands on deploy hosts as the SSH user and on the CI runner during builds. Package removal and destroy paths can delete unintended files; package extraction can overwrite other vendor files; generator names can write outside the project or inject executable CFML into generated code. Inputs may originate from CI variables, branch names, packages or an AI agent using the CLI's MCP tools. Also relevant are unencoded display properties in generated scaffold show views since 4.1.0 and in generated admin views, permitting stored XSS, and stale process-ID handling in RustCFML server commands that can terminate an unrelated process. This is fixed in 4.1.2; existing affected generated views also require the documented edit.

### CVE-2026-108433

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-807` |
| Published | 2026-10-15T21:17:08.657 |

Reliance on untrusted inputs in a security decision in Microsoft Office Word allows an unauthorized attacker to bypass a security feature locally.

### CVE-2026-105035

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-15T21:17:04.113 |

The EnergizeLab FirmwareUpdater (AArch64 ELF, distributed in the CDN bin.zip) uses a single hard-coded AES key shared by all installations. An attacker who recovers the key from the updater can decrypt and forge firmware packages for any device that trusts it.

### CVE-2026-55246

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-10-15T18:17:27.317 |

bincookie is a header-only binarycookies parser. Prior to 0.1.9, bincookie_init_file() in bincookie.h allocates a buffer using the actual .binarycookies file length but trusts the file-controlled num_pages field as the loop bound for byte-swapping page_sizes entries. A crafted file can make the loop read and write beyond the heap allocation, and related unvalidated page sizes and cookie_offsets can drive additional out-of-bounds accesses in page and cookie iteration. Applications that parse an attacker-supplied binarycookies file may crash or suffer heap corruption that can potentially enable code execution. This issue is fixed in version 0.1.9.

### CVE-2026-111091

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-15T16:17:48.637 |

In JetBrains Junie CLI before 26.8.3 code execution was possible via an untrusted project's MCP server configuration

### CVE-2026-110746

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-23` |
| Published | 2026-10-15T15:17:28.487 |

A local privilege escalation vulnerability in TotalAV allows an unprivileged local user to forge the gRPC IPC authentication token, through loading IPC.dll and abuse the SYSTEM service's within TotalAV to execute arbitrary code as NT AUTHORITY\SYSTEM.

### CVE-2026-111224

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-15T19:17:35.090 |

pfSense CE through 2.9.0 contains an OS command injection vulnerability in the OpenVPN openvpn.connect_async.sh script that allows authenticated VPN users to execute commands as root via crafted usernames. Attackers authenticated through RADIUS or LDAP can use usernames containing single quotes and shell metacharacters to break out of the eval'd pfctl anchor name on connect or disconnect.

### CVE-2026-53574

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-15T15:17:35.180 |

EspoCRM is an open source customer relationship management application. From 8.1.0 until 9.3.8, an authenticated non-administrator can submit a crafted where parameter to the GET entity streamAttachments endpoint because that query path permits complex expressions. Boolean-based blind SQL injection can extract arbitrary database information, including active administrator session tokens, and can enable full privilege escalation. This issue is fixed in version 9.3.8.

### CVE-2026-63618

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-16T13:16:57.127 |

Exposure of Sensitive Information (system level configuration info) to an Unauthorized Actor vulnerability in Apache Kylin.



This issue affects Apache Kylin: from 4 through 5.0.4.



Users are recommended to upgrade to version 5.0.5, which fixes the issue.

### CVE-2026-105958

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-16T13:16:53.480 |

A flaw was found in spice-server. Multiple migration data handlers use client-supplied offsets from SPICE_MSGC_MIGRATE_DATA messages without bounds validation, allowing a malicious authenticated SPICE client during VM live migration to read arbitrary heap memory or trigger heap corruption via out-of-bounds read and write operations on the message buffer.

### CVE-2026-105959

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-16T12:16:31.733 |

A flaw was found in spice-server. The GLZ encoder dictionary restore path truncates a size_t allocation size to int when calling the malloc callback, allowing a malicious authenticated SPICE client during VM live migration to trigger a massive heap buffer overflow by sending a crafted max_encoders value in migration data.

### CVE-2026-92766

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-16T09:17:04.963 |

The Vitepos – Point of Sale (POS) for WooCommerce plugin for WordPress is vulnerable to generic SQL Injection via the 'src_by' parameter in all versions up to, and including, 3.5.1 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. This makes it possible for unauthenticated attackers, or authenticated attackers holding any POS role (such as vtpos-cashier), to exploit the vulnerability, as the /vitepos/v1/vendor/list REST route's permission callback requires only a POS role assignment rather than any elevated WordPress capability.

### CVE-2026-14177

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-204` |
| Published | 2026-10-16T09:17:04.533 |

Observable response discrepancy vulnerability in IKAS Technology Inc. Ikas E-Commerce Infrastructure allows Account Footprinting.

This issue affects ikas E-Commerce Infrastructure: through 2026-07-13.

### CVE-2026-103896

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-16T06:17:03.417 |

The 10Web Booster – Website speed optimization, Cache & Page Speed optimizer plugin for WordPress is vulnerable to a limited file write via path traversal in versions up to, and including, 2.34.5 This is due to the OptimizerWebPageCache::get_cache_file_dir() function concatenating raw, unsanitized $_GET parameter names and values into the on-disk cache path, and the cache_content() sink calling mkdir() and file_put_contents() on the result with no realpath containment check — unlike the sibling delete_page_cache(), which does perform one. This makes it possible for unauthenticated attackers to create arbitrary directories (mode 0777, recursively) outside the cache root and write a cached page into them. The write is LIMITED: the filename is always 'source.html', so the extension is fixed, and the content is the rendered page buffer rather than attacker-supplied data. PHP files cannot be written and code execution is not possible; the demonstrated impact is cache poisoning and arbitrary directory creation.

### CVE-2026-111114

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-16T05:17:30.350 |

The Nexter Extension – Security, Performance, Code Snippets & Site Toolkit plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 4.7.11 The vulnerability exists because the `/?reset-view` handler in `role_switcher_to_view_admin_as()` performs no nonce or capability check when the supplied username matches the authenticated caller, and because the plugin's only cleanup mechanism — the `profile_update` hook — does not fire when WordPress performs a bulk role change via `wp-admin/users.php?action=promote`, which calls `WP_User::set_role()` directly and leaves a stale `administrator` value in the `nxtext_view_admin_original_role` user meta. This makes it possible for authenticated attackers with Subscriber-level access or above to restore the stale stored Administrator role to their own account, effectively escalating their privileges to Administrator. Exploitation requires that the attacker's account previously held the Administrator role and used the View Admin Role Switcher feature before being demoted specifically through the bulk role-change control rather than the Edit User screen, as only the bulk path bypasses the `profile_update` hook that would otherwise have cleared the stored original role.

### CVE-2026-110590

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-16T05:17:29.973 |

The Klarna for WooCommerce plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 4.13.3 This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to access any order's secret order_key and full billing and shipping PII — including first name, last name, email address, phone number, street address, postcode, city, region, and country — emitted inline as the klarna_payments_params JavaScript variable, enabling full store-wide order enumeration. Because WooCommerce order IDs are sequential integers and no order_key or authenticated session is required, every order in the store can be trivially enumerated with sequential GET requests to the order-pay endpoint.

### CVE-2026-109400

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-16T05:17:29.350 |

The InstaWP Connect – 1-click WP Staging & Migration plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 0.1.4.1 This is due to the plugin registering its admin page via `add_management_page()` using a role name returned by `InstaWP_Setting::get_allowed_role()` as the required capability — which WordPress resolves as a real capability match for any user holding that role — combined with `generate_section_field()` rendering the master API key from the `instawp_api_options` option directly as the `value` attribute of a plain-text HTML input with no additional `manage_options` or equivalent capability check. This makes it possible for authenticated attackers with Subscriber-level access and above to read the plaintext master API key, use its SHA-256-derived secret as a bearer token accepted by the plugin's REST API `validate_api_request()`, and call `POST /wp-json/instawp-connect/v2/auto-login` to mint a 30-second single-use login URL that sets an administrator authentication cookie — fully escalating their privileges. Exploitation requires the site to be actively connected to InstaWP and an administrator to have added the attacker's role to the plugin's Sync Tab Access list (`instawp_sync_tab_roles`); notably, the settings tab suppression logic only hides the tab when `administrator` is absent from the list entirely, meaning a mixed configuration retaining administrator alongside a lower role still serves the full settings page — including the API key — to the lower-privileged user.

### CVE-2026-107746

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-16T05:17:28.837 |

The FunnelKit – Funnel Builder for WooCommerce Checkout plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 3.16.0.6 This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to retrieve billing PII — including full name, street address, email address, and phone number — for any WooCommerce order on the site by submitting an enumerable sequential order ID. This is only exploitable on sites where a FunnelKit thank-you page exists that renders the [wfty_order_meta] or [wfty_order_total] shortcode.

### CVE-2026-107659

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-16T05:17:28.710 |

The Modula Image Gallery – Photo Grid & Video Gallery plugin for WordPress is vulnerable to Sensitive Information Exposure in all versions up to, and including, 3.0.11 via the 'id (post ID in /wp-json/wp/v2/modula-gallery/{id}) or none for collection route' parameter. This makes it possible for unauthenticated attackers to extract the plaintext Password Protect password and username for every published gallery from the modulaSettings REST field. The plugin's own /wp-json/modula/v2/gallery/{id}/settings endpoint correctly redacts the password for unauthenticated callers via redact_settings_for_public(), but no equivalent redaction is applied on the core /wp-json/wp/v2/modula-gallery path exposed by show_in_rest=true CPT registration.

### CVE-2026-103525

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-16T05:17:28.210 |

The FluentCart A New Era of eCommerce – Faster, Lighter, and Simpler plugin for WordPress is vulnerable to Insecure Direct Object Reference in all versions up to, and including, 1.7.0 via the 'order_id + billing_address_id (also shipping_address_id)' parameter due to missing validation on a user controlled key. This makes it possible for unauthenticated attackers to read and exfiltrate another customer's stored billing and shipping address PII — including street address, city, state, postcode, phone number, company name, VAT number, and legal registration ID — by enumerating sequential AUTO_INCREMENT order and address ID pairs. The id-equality guard intended to restrict address reuse is bypassed because the attacker controls both halves of the compared pair, and the unauthenticated AJAX entry point imposes only a soft rate limit of 5 requests per 60 seconds rather than any authentication or ownership check.

### CVE-2026-109468

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-15T21:17:12.880 |

Allocation of resources without limits or throttling in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-108448

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T21:17:10.440 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-105036

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-494` |
| Published | 2026-10-15T21:17:04.230 |

EnergizeLab AI Station firmware, EilikO Linux robot firmware v2.1_20260617182218_release, and the EnergizeLab Windows desktop app 3.1.2 download firmware updates over plain HTTP and do not verify their integrity or authenticity. An attacker able to intercept or modify the traffic can substitute a malicious update.

### CVE-2026-97370

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-15T19:17:49.983 |

Junrar is an open source Java RAR archive library. Prior to 7.6.1, RarVM.ExecuteCode in src/main/java/com/github/junrar/unpack/vm/RarVM.java can repeatedly execute a VM_JMP instruction whose target is greater than or equal to the prepared program's codeSize. The setIP() function returns success without changing the instruction pointer or decrementing maxOpCount, and the jump handler continues before loop-end accounting, leaving both values unchanged. A crafted RAR4 archive can therefore keep an extraction thread in an infinite CPU loop and exhaust archive-processing worker capacity. The RAR virtual machine does not expose native process execution, so the supported impact is availability loss rather than code execution. This issue is fixed in version 7.6.1.

### CVE-2026-87018

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248;CWE-617` |
| Published | 2026-10-15T19:17:46.600 |

undici is an HTTP client library for Node.js. In versions 4.2.1 through 6.29.0, 7.0.0 through 7.30.0, and 8.0.0 through 8.12.1, the client process crashes when a TLS 1.2 server renegotiates after the connection is established and presents a different, CA-trusted certificate whose hostname does not match the requested host. Node.js re-runs hostname verification on the renegotiated handshake and destroys the socket with a certificate-altname error, but undici's established-socket error handler asserted that this error code could never occur, so the peer-controlled error became an uncaught assertion that terminates the Node.js process, affecting both the HTTP/1.1 and HTTP/2 paths. A malicious or compromised HTTPS endpoint reached through undici or the global fetch() can crash the client with a single server-initiated renegotiation, taking down all in-flight requests and background work in the process, and exploitation needs no CA compromise because the attacker controls the endpoint and can present two ordinary valid certificates. Only TLS 1.2 is affected, since TLS 1.3 does not support renegotiation. The issue is fixed in undici 6.29.1, 7.30.1, and 8.12.2, and users should upgrade to one of those versions or later. As a workaround, restrict outbound connections to TLS 1.3 so renegotiation cannot occur, when the target endpoints support it.

### CVE-2026-111222

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-10-15T19:17:34.797 |

Netgate pfSense CE through 2.9.0 contains a php.ini injection vulnerability that allows authenticated users with General Setup privileges to inject directives by submitting an unvalidated timezone value. Attackers can embed a quote and newline to add auto_prepend_file pointing at /var/db/zoneinfo, executing PHP as root after php.ini is regenerated at boot or php-fpm restart.

### CVE-2026-111221

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-10-15T19:17:34.650 |

Netgate pfSense CE through 2.9.0 contains a configuration injection vulnerability that allows authenticated WebGUI users to inject mpd5 commands by submitting an unescaped RADIUS shared secret. Attackers with L2TP or PPPoE Server edit privileges can POST a secret containing a quote and newline to vpn_l2tp.php or services_pppoe_edit.php, appending an up-script that executes as root when a session starts.

### CVE-2026-111219

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-10-15T19:17:34.357 |

Netgate pfSense CE through 2.9.0 contains a newline injection vulnerability in services_pppoe_edit.php that allows privileged users to inject mpd.secret entries via unvalidated username POST fields. Attackers with the PPPoE Server Edit privilege can add a line whose secret begins with '!', making mpd5 run commands as root when a PPPoE client authenticates.

### CVE-2026-110874

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-15T19:17:24.353 |

Dolibarr before 23.0.4 contains a PHP object injection vulnerability in jsonOrUnserialize() in functions.lib.php, which calls unserialize() without class restrictions when json_decode() fails. Attackers able to write stored extrafields, export configurations or blocked log entries can plant serialized objects that trigger gadget chains for code execution or file manipulation.

### CVE-2026-109869

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248;CWE-459` |
| Published | 2026-10-15T19:17:21.770 |

undici is an HTTP client library for Node.js. In versions 6.23.0 through 6.29.0, 7.18.0 through 7.30.0, and 8.0.0 through 8.12.1, its fetch() implementation crashes the Node.js process when a malicious server returns a response with more than five content codings and closes the connection before sending the body. undici rejects such responses because of a content-encoding limit, but it created the internal response stream before that check and returned without attaching an error listener or aborting the request, so the early close surfaces a content-length mismatch on the orphaned stream, which Node.js treats as an unhandled error and terminates the process. A remote, unauthenticated server can trigger this with a single response, even when the application correctly catches the fetch() rejection, resulting in a denial of service. The issue is fixed in undici 6.29.1, 7.30.1, and 8.12.2, and users should upgrade to one of those versions or later. There is no workaround.

### CVE-2026-104827

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-15T19:17:14.933 |

react/http is an event-driven, streaming HTTP client and server implementation for ReactPHP. From 1.0.0 until 1.11.1, React\Http\Browser uses ClientRequestStream::handleData() to append response-header bytes to an internal buffer without enforcing a size limit. A remote server can send a valid status line and partial header, withhold the \r\n\r\n or \n\n header terminator, and continue streaming data so the buffer grows for the life of the connection. Applications that fetch attacker-controlled or attacker-influenced URLs, including URLs reached through redirects, can exhaust PHP memory_limit and crash the event-loop or worker process. Confidentiality and integrity are unaffected. This issue is fixed in version 1.11.1.

### CVE-2026-103936

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248;CWE-755` |
| Published | 2026-10-15T18:17:22.433 |

libp2p is a JavaScript implementation of the libp2p networking stack. Prior to 6.0.28, the @libp2p/webrtc webRTCDirect() Node.js listener processes unauthenticated STUN Binding Requests before PeerId authentication, Noise, muxing, protocol negotiation, connection creation, or connection-manager admission. The listener in packages/transport-webrtc/src/private-to-public/utils/stun-listener.ts forwards the packet-controlled request.ufrag into DirectRTCPeerConnection.setLocalDescription, where the value is reused as an ICE password without validating its required length and character set. A short credential causes node-datachannel or libdatachannel to raise an uncaught native invalid_argument and abort the process with SIGABRT, allowing a single remote UDP packet to deny service. The confirmed impact is process termination only, with no demonstrated memory corruption, code execution, browser impact, confidentiality impact, integrity impact, or connection-limit bypass. This issue is fixed in version 6.0.28.

### CVE-2026-61611

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-307` |
| Published | 2026-10-15T17:17:26.537 |

Lychee is a free, open-source photo-management tool. Prior to 7.6.1, POST /api/v2/Album::unlock has no throttle, attempt counter, backoff, CAPTCHA, or lockout. UnlockAlbumRequest::authorize() permits any caller to submit attempts, and app/Actions/Album/Unlock.php verifies each guess with Hash::check without limiting repeated failures. A remote unauthenticated attacker who knows or can obtain an album identifier can automate password guesses against a password-protected album and, if the password is recovered, gain access to its private photo collection. This issue is fixed in version 7.6.1.

### CVE-2026-100409

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-177;CWE-180` |
| Published | 2026-10-15T17:17:07.923 |

OpenNext Cloudflare is an open Next.js adapter for Cloudflare. From 0.3.0 until 1.20.2, applications that enable enableCacheInterception, rely on middleware for access control, and have a matching cached protected route process encoded pathnames inconsistently between middleware matching and cache lookup. An unauthenticated attacker can use a percent-encoded pathname that does not match authorization middleware but decodes to the cache key of a protected route, causing cached content to be returned without authorization. Malformed encodings can also be partially decoded, allowing cache lookup to continue with a pathname that middleware did not evaluate consistently. This issue is fixed in version 1.20.2.

### CVE-2026-100354

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-15T17:17:07.780 |

kin-openapi is a Go project for handling OpenAPI files. Prior to 0.149.0, runtime request, response, and direct schema validation lacks cycle detection when an allOf, anyOf, or oneOf chain refers back to an ancestor schema, even though loading and document validation accept the circular reference. A request or response that reaches the affected schema causes unbounded recursion in Schema.visitJSON or openapi3filter.decodeValue and exhausts the Go goroutine stack. The resulting fatal stack overflow cannot be caught with recover and terminates the entire process, including unrelated requests. This issue is fixed in version 0.149.0.

### CVE-2026-100353

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-15T17:17:07.627 |

kin-openapi is a Go project for handling OpenAPI files. From 0.136.0 until 0.149.0, three openapi3filter decoder paths that were missed by the fix for GHSA-p6wj-qrr4-pgh5 lack a nil-items guard for legal OpenAPI 3.1 array schemas. An unauthenticated remote client can trigger a deterministic nil-pointer panic through an array query parameter, a deepObject query parameter containing an array property, or an application/x-www-form-urlencoded request body whose array property appears inside an allOf, anyOf, or oneOf subschema. The query and composed-body paths reach urlValuesDecoder.parseArray, while the deepObject path reaches buildResObj, and all pass a nil items schema into code that dereferences it. This issue is fixed in version 0.149.0.

### CVE-2026-97394

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248;CWE-476` |
| Published | 2026-10-15T16:18:25.273 |

kin-openapi is a Go project for handling OpenAPI files. From 0.136.0 until 0.143.0, openapi3filter accepts OpenAPI 3.1 array schemas without an items keyword and then dereferences the nil Schema.Items value while decoding application/x-www-form-urlencoded or multipart/form-data request bodies, response headers, and other array parameter surfaces. A remote unauthenticated client can reach an affected operation with a nonempty request or matching response and deterministically trigger a nil-pointer panic during ValidateRequest or ValidateResponse. OpenAPI 3.0 documents are not affected because document validation rejects arrays without items, and JSON request bodies use a different decoder path. This issue is fixed in version 0.143.0.

### CVE-2026-95155

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-15T16:18:24.470 |

FasterXML Jackson 1.x, confirmed in jackson-mapper-asl versions 1.8.3, 1.9.2, 1.9.11, 1.9.12, and 1.9.13, allows attackers to cause a denial of service by supplying deeply nested JSON input to an application that deserializes untrusted JSON using ObjectMapper.readValue.

### CVE-2026-111093

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-23` |
| Published | 2026-10-15T16:17:48.883 |

In JetBrains Datalore before 2026.2.1 unauthenticated path traversal via the report blob endpoint allowed reading arbitrary files

### CVE-2026-100352

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-754` |
| Published | 2026-10-15T16:17:31.307 |

kin-openapi is a Go project for handling OpenAPI files. Prior to 0.148.0, the OpenAPI 3.1 validation path passes YAML NaN and infinity numeric values to santhosh-tekuri/jsonschema v6.0.2 without applying kin-openapi's existing finite-number guards. A remote unauthenticated client can send an application/yaml or application/x-yaml request body containing .nan, .inf, or -.inf to an operation with a numeric constraint, causing the dependency to create and dereference a nil big.Rat during ValidateRequest. Standard net/http servers recover the panic per connection, while other hosts or application goroutines may terminate the process. This issue is fixed in version 0.148.0.

### CVE-2026-95179

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-15T15:17:38.790 |

An issue in lottie-android 6.7.1 and earlier (and master) allows a remote attacker to cause a denial of service via a crafted Lottie animation JSON containing a cyclic precomposition reference graph that triggers uncontrolled recursion in BaseLayer.forModel and CompositionLayer.

### CVE-2026-108116

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-74` |
| Published | 2026-10-15T15:17:22.753 |

In Progress Kendo UI for jQuery prior to v2026.3.1015, specially crafted filter values in the PivotGrid XMLA transport could alter MDX predicates or inject XML markup into SOAP requests, potentially exposing data accessible through the configured XMLA connection.

### CVE-2026-109829

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-346;CWE-524` |
| Published | 2026-10-15T19:17:21.513 |

undici is an HTTP client library for Node.js. In versions 7.0.0 through 7.30.0 and 8.0.0 through 8.12.1, when an originless Agent composes the redirect and cache interceptors in that order with a shared cache store, the cache builds its key from the original request URL before the redirect handler changes the origin, so a response produced after a cross-origin redirect is stored under the original key. An attacker who controls the target of a redirect from a trusted URL can have their response cached under that trusted URL and served to later callers, allowing persistent cache poisoning, and the same key confusion lets a private, non-stored redirect response to a user-specific resource be stored under the original URL and served to a later unauthenticated caller, disclosing private data. Applications are affected only when an originless Agent, a shared cache store, and the redirect-then-cache composition are all used. The issue is fixed in undici 7.30.1 and 8.12.2, which verify the producing origin still matches the cache key and preserve each redirect hop's cache-control policy before storing, and users should upgrade to one of those versions or later. As a workaround, compose the cache interceptor before the redirect interceptor, use per-origin dispatchers and cache stores, or disable shared caching on redirect-capable requests.

### CVE-2026-109383

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-15T19:17:20.853 |

undici is an HTTP client library for Node.js. In versions 4.0.0 through 6.29.0, 7.0.0 through 7.30.0, and 8.0.0 through 8.12.1, its Agent dispatcher passes its constructor options through a JSON-based deep clone before forwarding them to each per-origin pool, and because JSON cannot represent functions, a caller-supplied tls option containing a checkServerIdentity callback is silently dropped before it reaches the TLS layer. As a result, a TLS peer whose certificate a custom checkServerIdentity was written to reject, but which passes Node's default hostname and chain checks, is silently accepted. Because Agent is the default dispatcher behind request, fetch, and setGlobalDispatcher, this affects the path most applications use, and EnvHttpProxyAgent is affected on its direct and no-proxy routes as well, while only applications that pass a function-valued tls option such as a custom checkServerIdentity for certificate or public-key pinning are at risk. The issue is fixed in undici 6.29.1, 7.30.1, and 8.12.2, which preserve the tls option outside the JSON clone so custom verification callbacks are forwarded unchanged, and users should upgrade to one of those versions or later. As a workaround, pass the TLS options through connect instead of tls, or for proxied destinations use requestTls and proxyTls.

### CVE-2026-108334

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-917` |
| Published | 2026-10-15T19:17:20.187 |

A flaw was found in the internal WebAssembly (WASM) shim used by the Kuadrant operator. When generating the CEL predicate that determines whether Gateway-level authentication and rate limiting should run, the shim does not correctly escape values from HTTPRoute match fields. A user who can create or modify an HTTPRoute attached to a shared Gateway can provide a crafted path, header, or query match value that causes the predicate to skip those checks. The request is still forwarded to the route’s backend.

### CVE-2026-100351

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-289;CWE-436` |
| Published | 2026-10-15T16:17:31.110 |

kin-openapi is a Go project for handling OpenAPI files. From 0.144.0 until 0.147.0, openapi3filter.ValidationHandler validates an operation selected from decoded URL.Path while a downstream gorilla/mux router configured with UseEncodedPath can dispatch a different operation selected from URL.RawPath. When a public exact route and a protected parameterized route use the same method and overlap after decoding, an unauthenticated remote request containing an encoded path separator can be validated as public and then dispatched to the protected handler without invoking the configured AuthenticationFunc. The reachable path parameter is constrained to an encoded representation that decodes to the public literal route, and proxies that canonicalize the URI before forwarding prevent this specific mismatch. This issue is fixed in version 0.147.0.

### CVE-2026-79840

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-15T15:17:37.810 |

A buffer overflow vulnerability in HPE NonStop XABroker may cause memory corruption, resulting in application crash.

### CVE-2026-79839

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-15T15:17:37.693 |

A buffer overflow vulnerability in HPE NonStop ODBC/MX Server may cause memory corruption, resulting in application crash.

### CVE-2026-79838

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-15T15:17:37.580 |

A buffer overflow vulnerability in HPE NonStop ODBC/MX Services may cause memory corruption, resulting in application crash.

### CVE-2026-103508

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-10-15T15:17:20.547 |

P4 Search (formerly Helix Search) allows an authenticated user holding administrative privileges on the connected P4 Server to supply a crafted logging configuration that causes files to be written or deleted outside the intended logging directory. This could lead to code execution as the P4 Search service account. This issue affects P4 Search 2026.4.2 and earlier.



Perforce resolved it in 2026.4.3.

### CVE-2026-107648

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T12:16:32.053 |

The WP Sessions Time Monitoring Full Automatic plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'action (also function, plugin, post_type, post_status, ids, loggedout, and POST post_title)' parameter in all versions up to, and including, 1.1.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-96768

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T10:18:05.863 |

The GoSMTP Pro plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content via Email Log Body in all versions up to, and including, 1.2.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The exploit is made possible because WordPress comment kses does not strip entity-encoded tag delimiters, allowing the payload to pass moderation as safe text before being decoded into live HTML by core email notification functions and written verbatim into the plugin's email log database table.

### CVE-2026-109224

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T09:17:04.113 |

The SureCart – Ecommerce Made Easy For Selling Physical Products, Digital Downloads, Subscriptions, Donations, & Payments plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 4.9.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful execution requires the affected comment to appear on a post that loads the surecart-components runtime (e.g. via a [sc_buy_button] shortcode) and contains no sc-checkout element, as these conditions trigger the innerHTML sink in sc-cart-loader.

### CVE-2026-87111

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T08:17:13.650 |

The User Registration PRO – Custom Registration Form, Login Form, and User Profile WordPress Plugin plugin for WordPress is vulnerable to Stored Cross-Site Scripting via HTTP Referer Header in all versions up to, and including, 6.2.9 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This vulnerability is present only in the premium build of the plugin and is not present in the free WordPress.org distribution. The nonce required to call the vulnerable AJAX endpoint is localized into the page source of every front-end page for anonymous visitors, making it fully obtainable by unauthenticated attackers.

### CVE-2026-97640

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T07:17:14.823 |

The WPConsent – Cookie Banner & Cookie Consent for Privacy Compliance (GDPR / CCPA / EU Compliance Cookie Notice) plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content via Simple HTML DOM Parser Noise-Key Restoration (mXSS) in all versions up to, and including, 1.1.9 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the Script Blocking feature to be enabled, and the exploit chain depends on an attacker submitting two coordinated comments — one embedding event-handler syntax inside an allowed &lt;code&gt; element and one placing the deterministic ___noise___ restoration key inside an allowed &lt;abbr title=""&gt; attribute — with the key offset confirmable via an unauthenticated wpconsent_debug=1 request.

### CVE-2026-110701

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T07:17:11.643 |

The CP Multi View Events Calendar plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'CalendarTitle' parameter in all versions up to, and including, 1.4.42 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires that an administrator has enabled the "Allow edition in frontend?" option on at least one calendar view, which exposes the unauthenticated add endpoint and a publicly accessible nonce.

### CVE-2026-109193

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T07:17:09.417 |

The HivePress – Business Directory, Listings & Classified Ads Plugin plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the '<custom user attribute slug> (e.g. hp_custom_link)' parameter in all versions up to, and including, 1.7.32 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires that an administrator has configured a custom user attribute with a display_format template placing the %value% token inside an href, src, or style attribute context, which is a documented and expected use of the plugin's attribute display feature.

### CVE-2026-107768

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T07:17:09.103 |

The TranslatePress – Translate Multilingual sites with AI Translation plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 3.3.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the target site to allow unmoderated comment submission on at least one post and to have a secondary language configured — both conditions reflect TranslatePress's primary use case.

### CVE-2026-96570

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T06:17:13.630 |

The Schema & Structured Data for WP & AMP plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'saswp_review_text' parameter in all versions up to, and including, 1.67 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The nonce that serves as the only authorization gate is publicly printed in the [saswp-reviews-form] shortcode HTML, making it obtainable by any anonymous visitor and rendering it ineffective as an access control boundary.

### CVE-2026-95809

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T06:17:13.300 |

The Opti-Behavior – Self-Hosted Heatmaps, Session Recordings, Funnels, A/B Testing & Smart Insights plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via 'country_name' Location Parameter in all versions up to, and including, 1.9.2.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The heatmap recording endpoint accepts unauthenticated requests protected only by a nonce that any visitor can freely obtain via the public opti_behavior_refresh_nonces AJAX action, removing any practical barrier to injecting the malicious payload.

### CVE-2026-95686

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T06:17:12.963 |

The Opti-Behavior – Self-Hosted Heatmaps, Session Recordings, Funnels, A/B Testing & Smart Insights plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via the 'targetUrl' parameter in all versions up to, and including, 1.9.2.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The ingest endpoint is gated only by a nonce that is publicly emitted to every anonymous visitor on tracked pages via optiBehaviorHeatmapConfig.nonce, meaning no account or authentication of any kind is required to write the malicious payload.

### CVE-2026-89051

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T06:17:12.167 |

The WP Ghost (Hide My WP Ghost) – Security & Firewall plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'replaceHeadersAndTags' function in versions up to, and including, 7.0.12 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user clicks on the injected link.

### CVE-2026-111122

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T06:17:09.250 |

The SiteOrigin CSS plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via the 'href' parameter in all versions up to, and including, 1.6.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires the malicious comment to be approved and an administrator to subsequently open the Visual Inspector and click the attacker's anchor link, both of which are plausible interactions during routine comment triage.

### CVE-2026-109513

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T06:17:08.407 |

The NotificationX – FOMO, Live Sales Notification, WooCommerce Sales Popup, GDPR, Social Proof, Announcement Banner & Floating Notification Bar plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'name' parameter in all versions up to, and including, 3.3.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires that an administrator has previously enabled a WordPress.org Reviews campaign and placed the notificationx-pro/notificationx dynamic block on a public page, both of which are documented, supported plugin workflows.

### CVE-2026-109232

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T06:17:06.790 |

The Salon Booking System – Appointment Booking for Salons, Barbershops & Spas plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'sln[<checkout-field-key>]' parameter in all versions up to, and including, 10.31.9 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires that the site administrator has configured at least one custom checkout field of type Html or File, which is a standard documented plugin feature.

### CVE-2026-107764

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T06:17:06.380 |

The SiteOrigin CSS plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via the 'url (comment_author_url)' parameter in all versions up to, and including, 1.6.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is possible because WordPress core's esc_url() preserves HTML entity-encoded characters, allowing a crafted entity-encoded payload in the comment 'Website' field to survive storage and be DOM-decoded by the browser into executable markup at the sink.

### CVE-2026-104000

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T06:17:04.667 |

The Simply Schedule Appointments plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'status' parameter in all versions up to, and including, 1.6.12.35 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The malicious payload is stored unconditionally because debug logging is enabled by default, and the debug-log viewer is accessible to anyone holding the site-wide Support PIN (an HMAC-MD5 of AUTH_SALT displayed in wp-admin), meaning the injected script will execute against the administrator's session during ordinary support or troubleshooting workflows.

### CVE-2026-103999

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T06:17:03.927 |

The Ultra Addons for Contact Form 7 plugin for WordPress is vulnerable to Stored Cross-Site Scripting via File Upload in all versions up to, and including, 3.5.54 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The extension blocklist gatekeeper is bypassed by uploading text-type files (.txt, .csv, .vtt, .srt, .asc) whose contents begin with an HTML payload such as '<BODY onload=…>', as the check classifies these files as text/plain without inspecting their byte content.

### CVE-2026-100186

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T06:17:02.317 |

The User Profile Builder – Beautiful User Registration Forms, User Profiles & User Role Editor plugin for WordPress is vulnerable to Stored Cross-Site Scripting via First Name Field in all versions up to, and including, 4.0.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This vulnerability is only exploitable when the Email Confirmation feature is enabled in Profile Builder.

### CVE-2026-109998

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T05:17:29.717 |

The Mang Board plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'content' parameter in all versions up to, and including, 2.4.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is exploitable because the wp_ajax_nopriv_mb_template endpoint is publicly accessible without authentication, nonce verification is not enforced for the content_reply mode, and admin-ajax.php responds with Content-Type: text/html, causing browsers to execute injected tags embedded in the JSON response body.

### CVE-2026-97339

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T04:18:44.817 |

The Complianz GDPR/CCPA Cookie Consent Banner plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content via yotu-wp Cookie-Blocker Filter in all versions up to, and including, 7.5.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The exploit bypasses WordPress's wp_kses comment sanitization because the payload uses only allow-listed tags and hides executable tokens inside quoted attribute values as plain text; the XSS is only realized when Complianz's own output-buffer filter performs str_replace() rewrites that break out of the attribute context, and requires the comment to be approved before it executes for visitors.

### CVE-2026-109990

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T04:18:26.860 |

The Flying Scripts: Delay JavaScript to Improve Site Speed & Performance plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 1.2.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The exploit bypasses WordPress core's save-time kses sanitization entirely because the payload uses only kses-allowed elements — an &lt;abbr title&gt; attribute and &lt;code&gt; text content — and the XSS is introduced post-save when the plugin's output-buffer rewriter substitutes a double-quote-bearing &lt;code&gt; body into the &lt;abbr title&gt; attribute via predictable, unsalted ___noise___ placeholder keys.

### CVE-2026-109207

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T04:18:26.583 |

The RSS Aggregator by Feedzy – Feed to Post, Autoblogging, News & YouTube Video Feeds Aggregator plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'media:thumbnail@url' parameter in all versions up to, and including, 5.2.11 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the attacker to control an external RSS feed that the target site has already configured for import; no WordPress account or special plugin configuration is needed beyond that condition.

### CVE-2026-107758

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T04:18:24.003 |

The Colibri Page Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 1.0.390 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injected payload survives storage because the widened comment allow-list permits SVG elements with arbitrary data-* attributes; execution occurs because colibri.js, enqueued globally on every front-end page, reads the stored data-target value via jQuery.data() — which HTML-entity-decodes it — and passes the resulting string directly into jQuery(), which parses a leading '<' as HTML and fires the embedded event handler.

### CVE-2026-104828

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-15T19:17:15.083 |

HtmlUnit Neko is an HtmlUnit adaptation of NekoHTML. Prior to 5.4.0, HTMLWriterFilter writes decoded TEXTAREA and TITLE character content without entity encoding because both elements are treated as special content. During a parse-and-serialize round trip, entity references inside these escapable raw-text elements are decoded by the parser and then emitted as raw markup by printCharacters(), changing the document's semantics. Applications that use htmlunit-neko in an HTML sanitizer, content filter, or other parse-transform-serialize pipeline can therefore turn attacker-controlled encoded text into executable markup when the output is rendered by a browser. This issue is fixed in version 5.4.0.

### CVE-2026-111396

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-16T13:16:55.497 |

Missing Authorization vulnerability in Liquid Web / StellarWP Advanced Post Manager advanced-post-manager allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Advanced Post Manager: from n/a through 4.5.6.

### CVE-2026-101300

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-16T09:17:03.703 |

Server-Side Request Forgery (SSRF) reported in the ticket sales chart PDF export functionality of Wegow. According to the report, an authenticated user with a promoter account can manipulate the <svg> parameter of the POST request generated by selecting Download PDF. The content is processed by the export.highcharts.com service, which sends HTTP requests to attacker-controlled external resources and embeds their responses in the generated PDF. The reported behavior allows the export service to be used as an intermediary for these requests.

### CVE-2026-16453

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-472` |
| Published | 2026-10-16T08:17:12.640 |

Mattermost versions 11.10.x <= 11.10.0, 11.7.x <= 11.7.9, 11.9.x <= 11.9.1, 11.8.x <= 11.8.5 fail to verify the integrity of the SAML RelayState POST parameter which allows an authenticated SAML user to join any team, including invite-only teams, via forging the team_id or invite_id fields in the RelayState.. Mattermost Advisory ID: MMSA-2026-00727

### CVE-2026-96339

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T07:17:14.560 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Houzez.co Houzez houzez allows Reflected XSS.This issue affects Houzez: from n/a through 4.4.0.

### CVE-2026-111387

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-212` |
| Published | 2026-10-16T03:18:06.217 |

Nezha from 2.2.5 before 2.3.15 contains an information disclosure vulnerability that allows authenticated users to retrieve third-party credentials because listDDNS omits WebhookURL and WebhookRequestBody redaction. Admins or PATs with nezha:ddns:read scope can call GET /api/v1/ddns to read cleartext tokens embedded in every user's DDNS webhook profiles.

### CVE-2026-111384

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-16T03:18:05.740 |

Nezha 1.0.0 before 2.3.15 contains a memory exhaustion vulnerability in the dashboard file manager WebSocket endpoint because fmStream never calls SetReadLimit, leaving message size unbounded. Authenticated users with file manager scopes can send one oversized binary message to /api/v1/ws/file/:id, triggering an OOM kill that drops all agent monitoring.

### CVE-2026-111383

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-16T03:18:05.537 |

Nezha from 2.0.13 before 2.3.15 contains a resource exhaustion vulnerability that allows authenticated users to open unbounded concurrent connections to the /api/v1/ws/transfer WebSocket endpoint. Attackers can hold thousands of subscriptions created by ServerTransferClass.Subscribe without limits, exhausting file descriptors, memory, and goroutines and blocking agent gRPC reconnections.

### CVE-2026-111377

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-16T03:18:04.703 |

FreeRDP from 2.0.0 before 3.32.0 contains an unbounded reassembly vulnerability in WTSProcessChannelData that fails to enforce cumulative fragment limits. Authenticated clients can start a static virtual channel message, withhold the LAST flag, and send endless fragments to exhaust server memory.

### CVE-2026-84823

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-16T00:17:05.573 |

A flaw was found in WildFly. A user with the `Monitor` role, which is the lowest standard Role-Based Access Control (RBAC) role, can exploit a path traversal vulnerability in the `take-snapshot` operation. By manipulating the `name` parameter, this user can write a copy of the server configuration to an arbitrary location. This allows the `Monitor` role to read back the server configuration, including sensitive credentials, which would otherwise be restricted by RBAC, leading to information disclosure.

### CVE-2026-111369

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-15T22:19:35.013 |

ClassroomIO through 1.0.0 contains an incorrect authorization vulnerability in the PUT and DELETE /:lessonId lesson routes that allows any course member, including students, to modify lessons. Authenticated students can supply arbitrary lesson ids to change titles and stored HTML content or delete lessons in their course and in other courses and organizations.

### CVE-2026-111364

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-15T22:19:34.260 |

MinDoc through 2.2-beta.2 contains an insecure direct object reference vulnerability in DocumentController.Content that allows authenticated users to read documents from unauthorized books. Attackers holding a non-observer role on any book can name that book and iterate sequential document ids to read markdown and HTML from private books.

### CVE-2026-111363

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-15T22:19:34.103 |

BISHENG through 3.0.0-beta4 contains an insecure direct object reference vulnerability that allows authenticated low-privileged users to read other users' parsed documents by supplying arbitrary file_id values. Attackers can enumerate sequential file ids against GET /api/v1/knowledge/file_bbox to retrieve extracted page text from other users' and tenants' knowledge bases.

### CVE-2026-111359

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-15T22:19:33.937 |

CRMEB 5.6.1 through 6.0.0 contains an insecure direct object reference vulnerability that allows authenticated storefront users to read and claim other users' orders via the gift-order API. Attackers can enumerate sequential order IDs in gift_detail to harvest buyer identities and the gift_key, then call receive_gift to redirect paid goods to their address.

### CVE-2026-111313

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-15T22:19:30.200 |

JobOps through 0.13.1 contains a server-side request forgery vulnerability in the POST /api/manual-jobs/fetch handler that allows authenticated users, or unauthenticated clients in demo mode, to make the server fetch internal destinations. Attackers can supply loopback, private, or cloud metadata addresses in the url field to read returned page content, disclosing instance metadata and internal service data.

### CVE-2026-111170

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-15T19:17:33.153 |

kedro-datasets from 9.3.0 through 9.6.0 contains a path traversal vulnerability in MatplotlibDataset.save() that allows attackers to write files outside the dataset directory by supplying absolute plot names. Because validate_sub_path() strips leading slashes while pathlib's join discards the base path, attackers can create or overwrite files anywhere the process can write.

### CVE-2026-77467

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-10-15T17:17:27.727 |

Lychee is a free, open-source photo-management tool. Prior to 7.7.0, Lychee enables ImageMagick PDF support with Ghostscript but does not apply an effective pre-render limit to PDF page dimensions in ImagickHandler::loadPdf(). An authenticated user who can upload a small PDF with an oversized /MediaBox can cause Imagick::readImage() to consume substantial CPU before failing to produce an image. When QUEUE_CONNECTION selects synchronous processing the request can occupy a web worker, while the official asynchronous Docker configuration can clog the shared image-processing queue and delay other work. The advisory did not identify a Ghostscript sandbox escape. This issue is fixed in version 7.7.0.

### CVE-2026-105065

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-15T17:17:12.160 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in 8theme.com XStore xstore allows Reflected XSS.This issue affects XStore: from n/a before 9.7.9.

### CVE-2026-97665

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-15T16:18:25.490 |

A missing authorization check in Nexus Repository 3's NuGet Components API upload path allows an account holding only repository read and browse privileges to upload and persist NuGet symbol packages (.snupkg) to a hosted repository, bypassing the write-permission check enforced for ordinary package uploads. Exploitation requires a hosted NuGet repository with Symbol Server enabled. If anonymous access is enabled, the built-in anonymous user holds read and browse privileges across all repositories by default, so this precondition can also be met without an authenticated account.

### CVE-2026-71490

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-15T16:18:19.723 |

OPNsense is a FreeBSD based firewall and routing platform. Prior to 26.1.11, OPNsense\Core\ACL::hasPrivilege() appends a directly assigned comma-separated <priv> value as one string and then uses an exact comparison when checking user-config-readonly. A user directly assigned both a component write privilege and user-config-readonly can therefore be treated as lacking the read-only restriction, and MVC APIs protected by throwReadOnly() can persist configuration changes for that component. Group privileges are not affected by the same parser flaw because the group path already splits comma-separated values. This issue is fixed in version 26.1.11.

### CVE-2026-53582

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-91;CWE-643` |
| Published | 2026-10-15T16:18:12.827 |

OPNsense is a FreeBSD based firewall and routing platform. Prior to version 26.1.10, the Trust module stores attacker-controlled certificate authority and certificate refid values and interpolates them into XPath expressions in src/opnsense/mvc/app/models/OPNsense/Trust/FieldTypes/CAsField.php and src/opnsense/mvc/app/models/OPNsense/Trust/FieldTypes/CertificatesField.php. A user with CA Manager or Certificate Manager privileges can submit a crafted refid and repeatedly retrieve the object to obtain a boolean refcount oracle, allowing values in config.xml to be recovered character by character. Exposed values can include password hashes, API credentials, certificate private keys, VPN key material, and high-availability credentials, enabling privilege escalation and compromise of other security domains. This issue is fixed in version 26.1.10.

### CVE-2026-9703

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-15T15:17:39.180 |

Grafana's data source proxy did not apply role-based access control to write requests forwarded to Loki data sources. A user holding only the Viewer role on an affected Grafana instance could send POST, PUT and DELETE requests through the proxy to the Loki rules API (/loki/api/v1/rules), allowing them to create, modify and delete Loki alerting rules. Because those rules are stored by Loki rather than by Grafana, the change took effect for every user of that Loki data source, not only for the Viewer who made the request.

Exploitation requires an authenticated Viewer account on the Grafana instance and a configured Loki data source; no other privileges are needed. Both Grafana OSS and Grafana Enterprise are affected. The defect is in Grafana's data source proxy; Loki itself is not vulnerable and does not need to be patched.

### CVE-2026-111381

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-16T03:18:05.267 |

FreeRDP before 3.32.0 contains a heap buffer overflow vulnerability in persistent_cache_read_entry_v2 that allows local attackers to corrupt heap memory via integer wraparound in bitmap size calculation. Attackers can craft a persistent cache v2 file with oversized width and height values that causes mismatched entry size accounting and fixed 16 KiB reads, leading to crashes or code execution when loaded.

### CVE-2026-111379

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-16T03:18:04.980 |

FreeRDP before 3.32.0 contains a heap buffer overflow vulnerability in persistent_cache_read_entry_v3 that allows local attackers to corrupt memory by supplying a crafted v3 persistent cache file. Attackers can set large width and height values that wrap the size calculation in persist_cache_get_data, causing fread to overflow an undersized buffer and potentially execute code.

### CVE-2026-105228

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-16T03:17:58.517 |

This vulnerability allows remote attackers to disclose sensitive information on affected installations of Delta ISPSoft.

### CVE-2026-105227

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-16T03:17:58.357 |

This vulnerability allows remote attackers to disclose sensitive information on affected installations of Delta ISPSoft.

### CVE-2026-92629

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-16T00:17:07.190 |

A potential improper authorization vulnerability was reported in Lenovo Baiying PC Client, distributed exclusively in the Chinese market, that could allow a local authenticated user to execute arbitrary code with elevated privileges.

### CVE-2026-89057

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-16T00:17:06.417 |

A potential authentication bypass vulnerability was reported in some Lenovo tablets that could allow a user with physical access to gain unauthorized device access.

### CVE-2026-111365

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-15T22:19:34.407 |

cool-admin-midway through 8.0.0 contains an authorization bypass vulnerability that allows non-superadmin admins to read, modify, or delete other admins' roles by supplying arbitrary role ids. Attackers holding ordinary sys:role permissions can call /admin/sys/role/info, update, or delete with another admin's role id to rewrite menu and department grants, changing other users' effective access.

### CVE-2026-111357

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-15T21:17:13.190 |

Ivanti Connect Secure 22.8R2.4 mishandles the manner in which the dsinvoked broker trusts DSCache configuration data, leading to privilege escalation to root, as exploited in the wild in October 2026.

### CVE-2026-111105

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.0/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-197` |
| Published | 2026-10-15T18:17:26.670 |

Telegram rlottie Numeric Truncation Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Telegram. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the rlottie library. The issue results from the lack of proper validation of user-supplied data, which can result in a write before the start of an allocated buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-30207.
