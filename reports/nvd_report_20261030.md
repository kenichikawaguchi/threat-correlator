# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-29 15:00 UTC
- **対象期間**: `2026-10-28T15:00:34.000Z` 〜 `2026-10-29T15:00:58.000Z`
- **重要CVE数**: 173 件（Critical 9.0+: 21 件 / High 7.0〜: 152 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS 7.0 以上の高リスク脆弱性は **30 件以上** 見つかり、特に **リモートコード実行 (RCE)** と **認証バイパス** が目立ちます。  
- Web アプリケーション系（WordPress・AVideo・XWiki など）での **入力検証不備** が多数報告され、プラグインやテーマの古いバージョンが攻撃対象に。  
- ネットワーク機器・組み込み系（Juniper、Yamaha、Sophos、Signal K 等）でも **認証なしで管理機能にアクセスできる** バックドア的脆弱性が続出。  
- CVSS が 9.8 以上の **完全リモート実行**（例：CVE‑2026‑61567/61564、CVE‑2026‑42922）や **全権限取得**（例：CVE‑2026‑103409）と、即時パッチ適用が必須のケースが集中しています。

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な影響 | 注目理由・影響範囲 |
|-----|--------|----------|-------------------|
| **CVE‑2026‑61567** / **CVE‑2026‑61564** | 10.0 | AVideo (8.1.0 未満) のライブストリーミング／インストーラで **認証不要のリモートコード実行** | `webSiteRootURL` パラメータを操作するだけで任意コード実行可能。AVideo は教育機関や中小企業で広く導入されているため、サーバ全体が乗っ取られるリスクが高い。 |
| **CVE‑2026‑42922** | 9.8 | FUXA (1.3.2‑2809) の /nodered エンドポイントで **認証バイパス + 任意コード実行** | Node‑RED を組み込んだ IoT 管理プラットフォーム。認証なしで HTTP リクエストを送るだけでシステム権限でシェルが起動でき、産業制御系での被害が懸念される。 |
| **CVE‑2026‑103409** | 9.8 | Juniper Networks Session Smart Router の管理 API が **認証なしで管理者権限取得** | ルータは企業の境界防御の要。URL パラメータ操作だけで root 権限取得可能。Juniper 製品は大手 ISP・金融機関でも使用されている。 |
| **CVE‑2026‑115245** | 9.8 | WordPress 「Chat AI with Dispatcher」プラグイン (≤ 2.4) の **任意ファイルアップロード → RCE** | プラグインは AI チャットボットとして急速に普及。アップロードされた PHP がそのまま実行され、サイト全体が乗っ取られる。 |
| **CVE‑2026‑113617** | 9.9 | WordPress 「Automated Import Products to Cart」プラグイン (≤ 1.0.4) の **任意ファイル読み取り/削除** | サブスクライバー権限でもデータベース認証情報取得や任意ファイル削除が可能。EC サイトの機密情報漏洩リスクが高い。 |

> **共通点**：すべて **認証不要**、もしくは **低権限ユーザー** で実行でき、**リモートから直接コード実行** もしくは **管理権限取得** が可能です。特に WordPress 系プラグインは多数のサイトで共通利用されているため、広範囲に波及する恐れがあります。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 / プラグイン | 現行脆弱バージョン | 修正済みバージョン | 対応策 |
|-------------------|-------------------|-------------------|--------|
| **AVideo** | < 8.1.0 | 8.1.0 以上 | 公式リポジトリから最新版へアップデート。`view/videosListToLive.php` と `install/checkConfiguration.php` のパラメータサニタイズが追加。 |
| **FUXA** | 1.3.2‑2809 以前 | 1.3.3 以上 | `/nodered` エンドポイントに認証ミドルウェアを導入したリリースへ更新。 |
| **Juniper Session Smart Router** | 該当ファームウェア (不明) | JunOS 2026‑R2 以降 | Juniper の公式アドバイザリに従い、管理 API の認証強化パッチを適用。 |
| **Chat AI with Dispatcher** (WordPress) | ≤ 2.4 | 2.4.1 以上 | ファイルアップロード時に MIME と拡張子の二重検証を実装したバージョンへ更新。 |
| **Automated Import Products to Cart** (WordPress) | ≤ 1.0.4 | 1.0.5 以上 | ファイルパスのサニタイズと権限チェックが追加されたリリースへ。 |
| **XWiki Remote Macros** | 1.13‑1.14.5 | 1.14.6 以上 | `excerpt-include` マクロのタイトルエスケープが修正。 |
| **LogixFast Auth** (WordPress) | ≤ 1.0.4 | 1.0.5 以上 | パスワードリセットコード送信先の検証ロジックが追加。 |
| **Bot for Telegram on WooCommerce** | ≤ 1.3.0 | 1.3.1 以上 | `permission_callback` が正しく認可チェックを行うよう修正。 |
| **openEQUELLA** | < 2026.1 | 2026.1 以上 | `system.execute()` のホワイトリスト化が実装。 |
| **FearlessCMS** | < 0.1.4 | 0.1.4 以上 | デバッグスクリプトに認証・CSRF 対策が追加。 |
| **Yamaha NWR100** | すべてのリリース | ファームウェア 2.5.0 以上 (※メーカー提供) | OS コマンドインジェクション対策パッチ適用。 |
| **StylemixThemes Motors** | ≤ 1.4.126 | 1.4.127 以上 | Blind SQLi 対策クエリパラメータのエスケープが追加。 |
| **Signal K Server** | < 2.33.0 | 2.33.0 以上 | `/skServer/ziplogs` エンドポイントに認証を必須化。 |
| **Sophos UTM** (EOL) | すべて | EOL でサポート終了 → **代替製品への移行** 推

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-61567

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T22:17:15.900 |

AVideo is a video-sharing Platform. Prior to 8.1.0, the live-streaming endpoint `view/videosListToLive.php` accepts an attacker-named streamer in `webSiteRootURL`, calls `Login::run` in `objects/Login.php`, and trusts the returned JSON as session state. An unauthenticated remote attacker who can host an HTTP service reachable by the encoder can self-grant `isLogged` and `canStream` without legitimate credentials. The endpoint requires only nonempty `playlists_id` and `APISecret` values; `APISecret` is forwarded rather than checked against a stored secret. This path never calls `Streamer::isURLAllowed` and therefore works regardless of the operator's streamer allowlist. It fetches a second attacker-controlled video-list response and interpolates `videos[].path` without shell argument escaping into `ffprobe` and `ffmpeg` commands passed to `exec`; `isAudio` calls `isVideo` to reach the `ffprobe` command. Paths containing shell delimiters execute arbitrary operating-system commands as the web-server user. The request filter does not inspect the video-list JSON. This can disclose database and stored streamer credentials, compromise the upstream platform using those credentials, modify files owned by the web-server user, establish persistence, and deny encoder service. This issue is fixed in version 8.1.0.

### CVE-2026-61564

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-28T22:17:15.750 |

AVideo is a video-sharing Platform. Prior to 8.1.0, the unauthenticated installer endpoint `install/checkConfiguration.php` assembles `videos/configuration.php` by interpolating request parameters, including `webSiteRootURL`, into single-quoted PHP string literals without escaping. An attacker can terminate a literal and inject PHP that executes as the web-server user when the generated, directly requestable file is loaded. Exploitation requires `videos/configuration.php` to be absent, as on every fresh deployment or after the file is removed or moved; an existing file blocks this endpoint. The supplied `systemRootPath` must contain index.php and a connection using `databaseHost`, `databaseUser`, and `databasePass` must succeed, but the attacker can point those parameters to their own database server and needs no target credentials. The write location is also derived from `systemRootPath` without a base-directory constraint. This permits arbitrary command execution, reading and overwriting files owned by the web-server user, persistent PHP code, and control over stored database connection settings. The endpoint additionally interpolates request values into streamer and configuration INSERT statements, creating a secondary SQL-injection sink. This issue is fixed in version 8.1.0.

### CVE-2026-113617

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-29T06:17:18.857 |

The Automated Import Products to Cart WordPress plugin before 1.0.4 does not sanitize a user-supplied file path before using it to read and delete files, allowing users with minimal permissions, such as subscribers, to read arbitrary files (including ones containing the database credentials) and delete arbitrary files on the server.

### CVE-2026-44179

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-10-28T16:17:07.400 |

XWiki Remote Macros provides XWiki rendering macros that are useful when migrating content from Confluence. From 1.13 until 1.14.5, the `excerpt-include` macro does not properly escape the included page's title and executes `excerpt` content with the macro's rights. The title handling in `xwiki-pro-macros-ui/src/main/resources/Confluence/Macros/ExcerptInclude.xml` and the rendering of `excerpt` content into XWiki syntax both allow syntax injection. Any user able to edit a page, even without script or programming rights, can supply executable macro syntax in the title or `excerpt` and cause remote code execution when the page is included. This affects confidentiality, integrity and availability of the whole XWiki installation. This issue is fixed in version 1.14.5.

### CVE-2026-115245

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-29T06:17:19.407 |

The Chat AI with Dispatcher WordPress plugin before 2.4 does not properly validate uploaded files, relying only on a spoofable client-supplied content type, allowing unauthenticated attackers to upload arbitrary files, including PHP, which can lead to remote code execution.

### CVE-2026-113616

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-29T06:17:18.740 |

The LogixFast Auth WordPress plugin before 1.0.4 does not deliver its password-reset one-time code to the resolved account's own email address, mailing it to the address supplied in the request instead, allowing unauthenticated attackers to reset any user's password, including an administrator's, and take over the account.

### CVE-2026-42922

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-10-29T04:18:36.777 |

A authorization bypass vulnerability exists in the /nodered functionality of FUXA (version(s): 1.3.2-2809). A specially crafted HTTP request can lead to a arbitrary code execution. An attacker can make an unauthenticated HTTP request to trigger this vulnerability.

### CVE-2026-109516

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-29T04:18:22.763 |

The Bot for Telegram on WooCommerce plugin for WordPress is vulnerable to Authentication Bypass leading to Account Takeover in all versions up to, and including, 1.3.0. The `/wp-json/woo-telegram/v1/main/` REST endpoint is registered with `permission_callback => '__return_true'` and performs no Telegram webhook signature verification, allowing an unauthenticated attacker to POST a forged bot update with a `message.chat.id` set to any WordPress login name; `bftow_get_user_system_id()` resolves this attacker-supplied value to the targeted account via `get_user_by('login', $tgId)` with no ownership proof, and writes a login token computed as `md5($_SERVER['HTTP_USER_AGENT'] . time())` — both inputs are fully attacker-controlled or bounded within seconds using the response's own `Date` header. The resulting token is redeemable at the unauthenticated, capability-check-free, and nonce-less `?action=bftow_create_order&bftow_token=` endpoint, which calls `wp_set_auth_cookie()` unconditionally via `login_user_by_id`, issuing a persistent authenticated session cookie for the targeted account to the attacker. This makes it possible for unauthenticated attackers to log in as any WordPress user, including administrators, given only that user's username.

### CVE-2026-103409

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-28T17:17:27.840 |

A Missing authentication for critical function vulnerability in Juniper Networks Session Smart Router allows an unauthenticated network-based attacker to obtain administrative privileges by passing crafted URL parameters to an insecure endpoint running as root.

Note that this vulnerability can only be exploited prior to the device being onboarded to Mist/Conductor. The issue can no longer be exploited once a device is onboarded to Mist/Conductor.

### CVE-2026-103406

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T17:17:25.830 |

An Improper Neutralization of Special Elements used in an OS Command vulnerability in the AutomatedProvisioner in Juniper Networks Session Smart Conductor allows a remote attacker to execute arbitrary commands as root via a specially crafted salt minion ID.

### CVE-2026-66088

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-749` |
| Published | 2026-10-29T02:16:52.523 |

In openEQUELLA before 2026.1, the system.execute() function available to the scripting engine runs supplied operating system commands without validation or an allow-list of permitted executables. A user able to create or edit scripts can use it to execute arbitrary commands with the privileges of the openEQUELLA service account.

### CVE-2026-63190

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-22;CWE-79;CWE-200;CWE-288;CWE-306` |
| Published | 2026-10-28T20:18:37.470 |

FearlessCMS is a flat-file `content` management system centered on simplicity and open source. Prior to version 0.1.4, five debug/test PHP scripts under `admin/` perform privileged operations without `isLoggedIn()` authentication checks, CSRF protection or adequate `path` validation. On PHP's built-in development server, including the default Docker deployment, `router.php` checks an unnormalized admin URI prefix while the filesystem resolves dot segments, so `/./admin/` bypasses the admin login gate and executes those scripts directly. In `admin/debug_save_flow.php`, attacker-controlled `path` and `content` reach `file_put_contents` for arbitrary `.md` writes under `content`/ or outside it through `path` traversal, enabling site defacement and stored JavaScript in public pages; `print_r($_POST)` output without `htmlspecialchars` escaping also causes reflected cross-site scripting. The `admin/debug_content.php` `path` parameter reaches `scandir()`, `file_get_contents()` and `posix_getpwuid()`, permitting arbitrary directory enumeration and `.md` file reads that expose absolute paths, ownership, permissions, hashes and `content` previews. The `admin/preview-handler.php` endpoint accepts JSON `content` and `title` and writes enumerable files under `content/_preview/`, enabling stored cross-site scripting and disk exhaustion. The `admin/testdebug.php` endpoint appends to `admin/testdebug.log` without authentication, also enabling disk exhaustion. The `admin/test_redirect.php` script exposes a test artifact but escapes its inputs and is not itself an XSS sink. Stored script execution can steal sessions and compromise administrators when they view affected `content`. Reads and writes execute with PHP's privileges; the tested deployment runs PHP as root, amplifying filesystem impact. This issue is fixed in version 0.1.4.

### CVE-2026-97854

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-29T12:17:14.443 |

Yamaha wireless LAN router NWR100 provided by Yamaha Corporation contains an OS command injection vulnerability. Arbitrary OS commands may be executed by sending a specially crafted request to the affected product.

### CVE-2026-115964

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-29T11:17:31.220 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in StylemixThemes Motors motors-car-dealership-classified-listings allows Blind SQL Injection.This issue affects Motors: from n/a through 1.4.126.

### CVE-2026-114358

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-29T09:17:07.910 |

This
vulnerability exists in the Radius
Xenia M2M Platform due to insufficient validation of user supplied input in
the password recovery functionality in the web management interface. An
unauthenticated remote attacker could exploit this vulnerability by supplying
crafted SQL query through input fields to the targeted system. 



Successful exploitation of this vulnerability
could allow the attacker to gain unauthorized access to sensitive information,
enumerate database structure or modify database records on the targeted system.

### CVE-2026-118690

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-28T22:17:13.070 |

Signal K Server before 2.33.0 contains a missing authentication vulnerability that allows unauthenticated remote attackers to download log archives via the /skServer/ziplogs endpoint. Attackers can extract the JWT secretKey from security.json in the ZIP, forge administrator tokens, and create persistent admin accounts for full server control.

### CVE-2026-119050

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-10-29T14:17:51.990 |

Agno through 3.1.11 contains an unsafe reflection vulnerability in PandasTools that allows attackers to invoke arbitrary pandas functions by supplying model-controlled function names to getattr(). Attackers can use prompt injection to make the agent call pandas.read_pickle on attacker-controlled paths for code execution, or call other readers to read local files.

### CVE-2026-118633

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-35` |
| Published | 2026-10-28T19:17:31.537 |

A path traversal vulnerability allows a remote unauthenticated attacker to execute arbitrary code as root in Sophos UTM (all versions) after winning a race condition by sustaining repeated attacks for a few minutes when the email proxy is used with scanning enabled. Sophos UTM is end-of-life and the patch must be installed manually.

### CVE-2026-117574

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-28T20:17:21.417 |

A flaw was found in ai-gateway-payload-processing. An authenticated remote attacker can exploit this vulnerability by submitting a request specifying another tenant's model identifier in the request body or header. Because the service does not verify authorization before retrieving credentials from the shared store, it injects the target tenant's application programming interface (API) keys into the request. This flaw allows an attacker to perform unauthorized requests and consume another tenant's large language model (LLM) resources and quotas.

### CVE-2026-118264

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444;CWE-863` |
| Published | 2026-10-28T19:17:31.237 |

Echo is a Go web framework. From 4.0.0 until 4.16.1 and 5.4.1, Echo's Proxy middleware selects a raw tunnel from a client WebSocket upgrade request before verifying that the configured upstream accepted the upgrade. If the upstream rejects the upgrade with an ordinary keep-alive response, later HTTP requests on the connection are sent directly to that upstream without passing through Echo's router or route-specific middleware. This can bypass authentication or authorization enforced only by Echo routes, but requires an accessible proxy route, a cooperating rejected-upgrade response, and a target without independent upstream authorization. This issue is fixed in 4.16.1 and 5.4.1.

### CVE-2026-103693

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T06:17:17.197 |

The Frontend Dashboard WordPress plugin before 3.0.5, ProfileGrid  WordPress plugin before 6.0.0.5 do not prevent an unauthenticated user from storing a serialized PHP object in user metadata that is deserialized when a public profile is viewed, allowing PHP object injection that can lead to arbitrary file write and potential remote code execution.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-118579

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-912` |
| Published | 2026-10-28T23:17:09.940 |

A weakness has been identified in D-Link DIR-505 1.10B02. The impacted element is the function main of the file /secmark1524.cgi of the component Web Management CGI. This manipulation of the argument accu/pass/code/hash/cmds causes backdoor. The attack is possible to be carried out remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-103506

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-10-28T17:17:28.797 |

An authenticated user in Grafana can read SSO client secrets and modify instance-wide SSO settings without the required permissions (missing authorization). This affects Grafana OSS and Enterprise 13.2 installations with the experimental kubernetesSsoSettingsApi feature toggle enabled, which is disabled by default.

### CVE-2026-116399

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-29T14:17:50.260 |

Cross-Site Request Forgery (CSRF) vulnerability in InstaWP InstaWP Connect instawp-connect allows Cross Site Request Forgery.This issue affects InstaWP Connect: from n/a through 0.1.4.2.

### CVE-2026-115967

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-10-29T11:17:31.493 |

Weak Authentication vulnerability in Hamid Alinia Login with phone number login-with-phone-number allows Authentication Abuse.This issue affects Login with phone number: from n/a through 1.8.78.

### CVE-2026-86794

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T06:17:24.350 |

The Community Events WordPress plugin before 1.6.0 does not have authorisation or nonce checks when processing public event submissions, and does not escape several of the submitted values before outputting them in the administration dashboard and on the public calendar, allowing unauthenticated users to inject arbitrary web scripts that will execute in the browser of an administrator reviewing the submission.

### CVE-2026-61546

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346;CWE-350` |
| Published | 2026-10-28T22:17:15.590 |

AnkiMCP is an Anki addon that implements an MCP server, enabling AI assistants to interact with the Anki flashcard application. Prior to version 0.21.0, `anki_mcp_server/mcp_server.py` globally disables FastMCP DNS-rebinding protection through `TransportSecuritySettings` with `enable_dns_rebinding_protection=False`, including for the default local Streamable HTTP listener. The defaults in `anki_mcp_server/config.py` enable `http_enabled` on `127.0.0.1:3141`, with an empty `http_path` selecting the root endpoint. No bearer token, API key, session secret, strict `Host` allowlist or strict `Origin` allowlist is enforced before `initialize`, `tools/list` and `tools/call` reach MCP dispatch. A victim who visits a malicious web page while Anki and the listener are running can have browser requests rebound to loopback, allowing the attacker to `initialize` MCP, enumerate tools, read the local collection, and perform enabled non-destructive note/deck creation or updates. The attacker needs neither LAN position nor a local process. Available operations depend on enabled tool filters; destructive tools are hidden unless `enabled_destructive_tools` is opted into, limiting deletion-level impact but not the exposed read/write operations. The reported harness confirms real MCP tool dispatch with substituted Anki bridge responses rather than demonstrating destructive changes to a real collection. Disabling protection for tunnels/proxies also disables it for the normal loopback configuration. This issue is fixed in version 0.21.0.

### CVE-2026-78674

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T20:18:47.330 |

The BPMN System REST APIs do not sufficiently validate input parameters, allowing authenticated users to submit crafted requests that can lead to the execution of arbitrary commands on the server.

An authenticated user can leverage this vulnerability to execute arbitrary commands with the privileges of the product's runtime account. The scope of potential damage is contingent upon the permissions assigned to this account.

### CVE-2026-118688

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-61` |
| Published | 2026-10-28T19:17:35.973 |

wasmtime-wasi in Wasmtime before 36.0.18, 37.0.0 before 48.0.6, and 49.0.0 before 49.0.3 re-appends a trailing slash to rename source paths, causing renameat on macOS and FreeBSD hosts to follow directory symlinks. A guest with sandbox write access can rename a relative symlink such as "up/" to move host directories into its sandbox and read or write them.

### CVE-2026-118619

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-28T17:18:29.103 |

Ultralytics Google Drive Download Path Traversal Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Ultralytics. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the handling of downloads from Google Drive. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to execute arbitrary code in the context of the current process. Was ZDI-CAN-32376.

### CVE-2026-118610

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-28T17:18:28.137 |

Alpine iLX-F511 Android Auto Service Stack-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of Alpine iLX-F511 devices. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the Android Auto service. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a fixed-length stack-based buffer. An attacker can leverage this vulnerability to execute code in the context of root. Was ZDI-CAN-29015.

### CVE-2026-118606

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-749` |
| Published | 2026-10-28T17:18:27.677 |

Alpine iLX-F511 Framework Service Exposed Dangerous Function Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of Alpine iLX-F511 devices. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the framework service. The issue results from an exposed dangerous function. An attacker can leverage this vulnerability to execute code in the context of root. Was ZDI-CAN-29006.

### CVE-2026-106079

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T17:17:32.060 |

An Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability in AccessManager in Juniper Networks Session Smart Router and Session Smart Conductor allows an attacker with config-write privileges to achieve arbitrary command execution as root in the YANG configuration.

### CVE-2026-103408

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-28T17:17:26.520 |

A Stack Buffer Overflow vulnerability in the DHCP client in Juniper Networks Session Smart Router allows an unauthenticated attacker on the local network to achieve remote code execution via a malicious DHCP reply.

### CVE-2026-103407

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-28T17:17:26.240 |

An Improper Limitation of a Pathname to a Restricted Directory vulnerability in ConfigDirector in Juniper Networks Session Smart Router and Session Smart Conductor allows an authenticated REST user to read, overwrite, or delete arbitrary certificate and key files on the host filesystem via the certificate and private-key REST API.

### CVE-2026-103403

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T17:17:24.997 |

An Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability in AccessManager in Juniper Networks Session Smart Router and Session Smart Conductor allows an attacker to perform arbitrary file deletion and arbitrary command execution via the deletion of an audit rule.

### CVE-2026-103402

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-28T17:17:24.433 |

An Insufficient Verification of Data Authenticity vulnerability in PCLI in Juniper Networks Session Smart Router and Session Smart Conductor allows an attacker with write access to the model cache directory to execute arbitrary code and escalate privileges via the processing of unverified cache files.

### CVE-2026-103401

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-28T17:17:24.070 |

An Improper Link Resolution Before File Access ('Link Following') vulnerability in the unauthenticated web server handlers in Juniper Networks Session Smart Router and Session Smart Conductor allows a local unprivileged user to overwrite arbitrary files as root via unauthenticated API endpoints.

This vulnerability can be exploited on Mist-managed routers and on unmanaged Routers that have not yet been onboarded to a Conductor. Routers already managed by Conductor are not affected.

### CVE-2026-56828

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285;CWE-862` |
| Published | 2026-10-28T16:17:08.220 |

Shopper is a Headless e-commerce Admin Panel. From 2.8.0 until 2.8.1, three Shopper Livewire admin components retain authorization gaps after the earlier team-settings authorization fix. A staff member with only `view_users` and `access_dashboard` can mutate permissions, create an administrator, or delete roles. In `packages/admin/src/Livewire/Components/Settings/Team/Permissions.php`, `togglePermission` and `removePermission` authorize `view_users` rather than the stronger `access_setting` permission; `packages/admin/resources/views/livewire/components/settings/team/permissions.blade.php` exposes permission IDs in `wire:click` handlers. The attacker can grant arbitrary permissions to the bound role, including `access_setting` on the attacker's own role, or delete permission definitions. In `packages/admin/src/Livewire/SlideOvers/CreateTeamMember.php`, `mount()` and `store()` also accept `view_users`, and the client-selected `role_id` can identify the admin role, allowing creation of a pre-verified administrator with an attacker-chosen password. In `packages/admin/src/Livewire/Pages/Settings/Team/RolePermission.php`, `deleteAction` has no action authorization and is only conditioned on `can_be_removed`, while page access requires `view_users`. Deleting a removable role removes access for assigned users, enabling RBAC denial of service as well as privilege escalation. This issue is fixed in version 2.8.1.

### CVE-2026-116778

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-862` |
| Published | 2026-10-28T16:17:06.947 |

FOG is a free open-source cloning/imaging/rescue suite/inventory management system. Prior to 1.5.10.2253 and 1.6.0-RC-1, an authenticated API-enabled user with uType=1 who possesses both the user's API token and the global FOG API token can use PUT /fog/storagenode/{id}/edit to modify Storage Node user, pass, and ftppath fields because the API validates the credentials but does not enforce an administrator-only role. With storage replication enabled and a usable Storage Node, FOGImageReplicator interpolates those fields into an lftp command executed through proc_open() by the root-running service, allowing the low-privileged user to execute commands as root. This issue is fixed in versions 1.5.10.2253 and 1.6.0-RC-1.

### CVE-2026-119052

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-29T14:17:52.310 |

llama.cpp b2877 before b11935 contains an uncaught exception vulnerability in the ggml-rpc server that allows unauthenticated remote attackers to crash the rpc-server by sending oversized message lengths. After the HELLO handshake, attackers can send a command such as SET_TENSOR with a length above std::vector::max_size(), triggering an uncaught std::length_error that aborts the process and denies service to all clients.

### CVE-2019-25781

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-29T14:17:39.170 |

Python-Markdown 3.0 through 3.11.2 contains an algorithmic complexity vulnerability in inline link parsing that allows remote attackers to exhaust CPU through unmatched brackets. Attackers can submit short Markdown containing repeated [ or ![ characters, forcing LinkInlineProcessor.getText() and getLink() into quadratic scans that keep workers busy for minutes.

### CVE-2026-49142

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-29T13:17:12.713 |

OpenEMR before 8.5.0 contains an authenticated SQL injection vulnerability in the Syndromic Surveillance module that allows users with Clinician-level privileges to read and modify arbitrary database contents by submitting crafted values in the form_icd_codes[] POST parameter to the syndromicsurveillance/index endpoint. Attackers can inject an unquoted numeric IN() clause and UNION DISTINCT SELECT statement using hex-encoded literals to abuse MySQL extractvalue() for error-based exfiltration of bcrypt password hashes and execute stacked queries that reset passwords, resulting in full administrative account takeover.

### CVE-2026-119028

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-29T12:17:12.310 |

oapi-codegen 2.0.0 before 2.8.1 contains a code injection vulnerability that allows attackers to inject Go code by supplying non-literal enum entries in integer, number, or boolean schemas. Attackers controlling an OpenAPI document can craft an enum entry that closes the const block in constants.tmpl and injects a func init(), executing code when the generated package is built and imported.

### CVE-2025-62841

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-29T08:17:00.057 |

An use of hard-coded cryptographic key vulnerability has been reported to affect HBS 3 Hybrid Backup Sync and Hybrid Backup Sync. If exploited, the vulnerability could allow remote attackers to compromise the security of the system.

We have already fixed the vulnerability in the following version:
HBS 3 Hybrid Backup Sync 26.4.0.521 and later
Hybrid Backup Sync 26.4.0.521 and later
Hybrid Backup Sync 26.4.1.563 and later

### CVE-2025-62839

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-29T08:16:59.863 |

An use of hard-coded cryptographic key vulnerability has been reported to affect HBS 3 Hybrid Backup Sync and Hybrid Backup Sync. If exploited, the vulnerability could allow remote attackers to compromise the security of the system.

We have already fixed the vulnerability in the following version:
HBS 3 Hybrid Backup Sync 26.4.0.521 and later
Hybrid Backup Sync 26.4.0.521 and later
Hybrid Backup Sync 26.4.1.563 and later

### CVE-2026-118694

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-28T22:17:13.700 |

python-markdown2 through 2.5.5 contains a denial of service vulnerability that allows remote users to exhaust CPU by submitting Markdown with unclosed inline link destinations. Attackers can submit repeated '[a](' or '![a](' sequences, causing _find_balanced to rescan the remaining document for each link and consume quadratic CPU time.

### CVE-2026-118689

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-28T22:17:12.920 |

OvenMediaEngine through 0.21.0 contains a denial of service vulnerability in OvtPacket::LoadHeader() that allows unauthenticated attackers to stall connections by sending payload_length values above 32750. Attackers can send crafted OVT packets to the OVT listener to hold connections open indefinitely and accumulate buffered memory, disrupting origin-to-edge stream relay.

### CVE-2026-118686

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-28T19:17:35.633 |

EspoCRM before 9.3.11 and 10.x before 10.0.8 contains a denial of service vulnerability in which the password-redaction regular expression applied during API error handling consumes excessive CPU on long request bodies. Unauthenticated remote attackers can concurrently send a small number of large API requests to exhaust server workers, making EspoCRM slow or unavailable to legitimate users.

### CVE-2026-118649

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-10-28T19:17:33.263 |

n8n before 2.43.5 and 2.44.x before 2.44.1 accepts a client-supplied workflow ID and caches each workflow's owner project in memory by that ID, so a crafted ID such as __proto__ makes the Data Table project check match every project. An authenticated member who can create and run workflows can list, read, modify, and delete Data Table rows in all projects of the instance.

### CVE-2026-111419

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-29T10:17:03.440 |

A sensitive information exposure vulnerability exists on the Foxit official website because JavaScript code contains third-party authorization information. This may allow unauthorized parties to obtain or misuse the exposed credentials.

### CVE-2026-89216

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-29T06:17:24.800 |

The vTables  WordPress plugin before 0.3 does not properly sanitise and escape a parameter before using it in a SQL statement, which allows unauthenticated attackers to perform SQL injection attacks and extract data from the database.

### CVE-2026-113387

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-29T02:16:49.937 |

The Ortto plugin for WordPress before 1.0.25 did not authenticate configuration update requests, relying only on a secret exposed in public HTML. An unauthenticated threat actor could overwrite the plugin's configuration to serve arbitrary scripts.

### CVE-2026-61572

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-28T22:17:16.347 |

AVideo is a video-sharing Platform. Before the initial remediation attempt in 8.1.0, `url_get_contents` in `objects/functions.php` accepts caller-controlled destinations after only `FILTER_VALIDATE_URL` syntax validation, without rejecting private, loopback, or link-local addresses, and disables TLS peer verification. `Login::isLogged` reauthenticates using the attacker-settable `encoder_aVideoURL` cookie together with arbitrary nonempty `encoder_user` and `encoder_pass` cookies, and `Login::run` stores the raw fetched body in `result`. The unauthenticated `objects/login.json.php` endpoint returns that session object, enabling full-response exfiltration through a supplied `siteURL`; its `Streamer::isURLAllowed` gate allows all sites when the operator allowlist is empty, the default. An unauthenticated remote attacker can read internal HTTP and HTTPS responses, including cloud instance-metadata credentials, and reach internal TCP services. A further pre-authentication FTP variant in `view/youtubeDl.json.php` routes an ftp `videoURL` into `FTPDownloader`; `parseFtpUrl` in `objects/FTPDownloader.php` accepts its host and port for `ftp_connect`. This also enables requests to internal FTP services. Untrusted self-signed HTTPS certificates are accepted, and no account or operator interaction is required. Version 8.1.0 contains an initial remediation attempt that removes raw-response reflection and adds destination checks, but private-network exemptions and login TLS-verification defaults leave complete remediation of the described internal-network and TLS variants unresolved.

### CVE-2026-118755

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T22:17:14.370 |

Volmarg Personal Management System through 2.1.0 contains an OS command injection vulnerability that allows authenticated users to execute shell commands via unescaped folder paths in the storage module's tree command. Attackers can create a directory under upload/files containing shell metacharacters such as $(...) and then move or copy it, running commands as the web server user.

### CVE-2026-118668

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-863` |
| Published | 2026-10-28T21:16:57.263 |

langgraph-api implements the LangGraph API for rapid development and testing. From 0.1.2 until 0.15.0, JavaScript or TypeScript custom authentication Store authorization handlers can return a rewritten namespace that is not carried across the runtime boundary and applied before the Store operation. An authenticated user can therefore access another user's Store namespace when a deployment relies on namespace rewriting for isolation, allowing unauthorized reads, overwrites, searches, or deletions. Python custom authentication and handlers that reject unauthorized namespaces instead of rewriting them are not affected. This issue is fixed in version 0.15.0.

### CVE-2026-118660

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-28T21:16:56.123 |

Happy DOM is a JavaScript implementation of a web browser without its graphical user interface. Prior to 21.0.0, Happy DOM loads iframe src URLs and link rel="stylesheet" href URLs by default while parsing untrusted HTML on the server because disableIframePageLoading and disableCSSFileLoading default to false. An attacker who controls parsed HTML can therefore cause server-side requests to arbitrary internal or cloud endpoints without an application opt-in and may expose confidential responses or credentials returned by those endpoints. This issue is fixed in version 21.0.0.

### CVE-2026-76418

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-690` |
| Published | 2026-10-28T20:18:47.063 |

A vulnerability in the Remote Access SSL VPN service of Cisco Secure Firewall Adaptive Security Appliance (ASA) Software and Cisco Secure Firewall Threat Defense (FTD) Software could allow an unauthenticated, remote attacker to cause the device to reload unexpectedly, resulting in a denial of service (DoS) condition. This vulnerability is due to logic errors when secondary authentication is configured on a tunnel group. An attacker could exploit this vulnerability by sending a crafted request when connecting to the SSL remote access VPN. A successful exploit could allow the attacker to cause the affected device to reload, resulting in a DoS condition.

### CVE-2026-61542

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-28T20:18:27.213 |

Gearboy is a Game Boy, Game Boy Color, and Super Game Boy emulator and debugger with an embedded MCP server. Gearsystem, the affected component, has an optional `--mcp-http` mode that accepts unauthenticated MCP requests from any reachable network peer despite localhost-only documentation and logging. In the described `platforms/shared/desktop/mcp/mcp_transport.h` transport, the socket binds `INADDR_ANY`, normally on port 7777, and POST requests to `/mcp` reach dispatch without `Authorization`, `Host`, or `Origin` checks. Responses and OPTIONS advertise `Access-Control-Allow-Origin: *`. A peer can initialize an MCP session and invoke exposed emulator/debugging operations; even a garbage bearer token does not block dispatch, while a loopback-bind negative control prevents network access. The reported impact is bounded to the emulator process, debugging state, and local files accepted as media, rather than demonstrated host code execution. Gearboy 3.8.7 contains a patch.

### CVE-2026-118683

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-28T19:17:35.160 |

MONAI from 1.2.0 before 1.6.1 contains a remote code execution vulnerability in ConfigWorkflow.__init__, which passes a bundle's configs/logging.conf to logging.config.fileConfig that eval()s handler class and args fields. Attackers can publish a malicious bundle whose logging.conf runs arbitrary Python at workflow construction when a victim loads or runs the bundle.

### CVE-2026-118254

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T19:17:29.763 |

Highcharts JS is a JavaScript charting library based on SVG. From 2.0.0 until 3.2.0, Highcharts Grid writes pagination language strings into the DOM as markup instead of text. An attacker who controls the Grid language configuration can provide elements with event handlers, which execute in the hosting page origin when pagination controls render. Exploitation requires pagination to be enabled but does not require additional user interaction. This issue is fixed in 3.2.0.

### CVE-2026-118245

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T18:17:15.403 |

Highcharts JS is a JavaScript charting library based on SVG. From 1.0.0 until 4.2.2, Highcharts Dashboards uses chartConstructor as an unchecked property lookup in the Highcharts namespace and invokes the selected member with the component container and chartOptions. An attacker who controls dashboard configuration can select a public utility function instead of a supported chart constructor, causing attacker-controlled options to be copied to the container as properties or attributes. Markup and event handlers can then execute in the hosting page origin when the board renders. No user interaction beyond rendering the board is required. This issue is fixed in 4.2.2.

### CVE-2026-39736

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-29T14:17:54.523 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Crocoblock JetEngine jet-engine allows SQL Injection.This issue affects JetEngine: from n/a through 3.9.0.1.

### CVE-2026-115965

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-29T11:17:31.357 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in BuddyPress BuddyPress buddypress allows Blind SQL Injection.This issue affects BuddyPress: from n/a through 14.5.2.

### CVE-2026-118753

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-28T22:17:14.047 |

FreeImage (danoli3 fork) before 3.19.25 contains a heap buffer overflow vulnerability in PluginGIF.cpp that allows attackers to write past the canvas allocation via unclipped GIF frame rectangles. Attackers can craft a GIF whose frame left plus width exceeds the logical screen width, causing GifPlaybackCompositeFrame() and GifPlaybackFillRect() to corrupt heap memory when loaded with GIF_PLAYBACK.

### CVE-2026-118752

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-28T22:17:13.857 |

FreeImage (danoli3 fork) before 3.19.22 contains a heap buffer overflow vulnerability in the PBM RLE decoder of PluginIFF.cpp that lacks bounds checks on ByteRun1 runs. Attackers can supply a crafted IFF/LBM PBM file with runs straddling scanline ends to write up to 127 controlled bytes past the heap-allocated bitmap.

### CVE-2026-118242

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T18:17:14.963 |

Highcharts JS is a JavaScript charting library based on SVG. From 2.3.0 until 3.2.0, Highcharts Grid creates SVG path elements from rendering.icons object definitions and previously copied every child key with setAttribute. An attacker who controls Grid configuration can supply event-handler attribute names in an icon definition. Because custom icons override built-ins, the attacker can replace default sort or pagination icons, and script runs in the hosting page origin when a user hovers over or activates the affected icon. This issue is fixed in 3.2.0.

### CVE-2026-116797

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T18:17:14.607 |

Highcharts JS is a JavaScript charting library based on SVG. From 2.0.0 until 3.2.0, Highcharts Grid Pro input renderers copy the cells.renderer.attributes and cells.editMode.renderer.attributes maps to input or select elements with raw setAttribute calls. An attacker who controls column configuration can add event-handler attributes to every rendered row or to the control created when a cell enters edit mode. Script then runs in the hosting page origin when a user hovers over or focuses an input or begins editing. This issue is fixed in Grid Pro 3.2.0.

### CVE-2026-112357

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-10-28T16:17:01.843 |

GFI KerioConnect (Kerio Connect) Outlook Connector (Offline Edition), 'KOFF', before 10.0.9 Patch 2 contains a local privilege escalation vulnerability caused by weak installer permissions that leave the product directory writable by the built-in Users group. A local non-administrative attacker can replace the searchd.exe service binary used by the bundled KOFFIndexingService, which runs as LocalSystem, to execute arbitrary code with NT AUTHORITY\SYSTEM privileges upon the next service start or reboot.

### CVE-2026-97860

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-10-29T12:17:14.577 |

YMS-VPN8 and YMS-VPN8-CP provided by Yamaha Corporation register Windows services with unquoted file paths. A user who has write permissions on the system drive may be able to execute arbitrary code with SYSTEM privileges.

### CVE-2026-103665

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-10-29T12:17:08.980 |

The installer for Yamaha LAN Monitor for Windows provided by Yamaha Corporation may insecurely load Dynamic Link Libraries (DLLs). When the installer is launched in a directory containing a specially crafted DLL file, the malicious DLL may be loaded, resulting in arbitrary code execution with administrative privileges.

### CVE-2026-118669

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-28T22:17:12.610 |

OAuthLib is an implementation of the OAuth request-signing logic for Python 3.6+. Prior to 4.0.0, the client_credentials and Resource Owner Password Credentials token grant handlers can authenticate request.client as one confidential client while retaining an attacker-supplied request.client_id for validate_grant_type and validate_scopes. A lower-privilege authenticated client can therefore cause grant and scope authorization to use another client's identity when an application validator relies on the documented client_id argument, potentially issuing tokens with unauthorized grants or scopes. Validators that authorize exclusively from request.client may not be affected. This issue is fixed in version 4.0.0.

### CVE-2026-118648

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T19:17:33.093 |

n8n before 1.123.85, 2.x before 2.43.5, and 2.44.x before 2.44.1 contains a stored cross-site scripting vulnerability because some webhook response paths, such as error responses and responses without headers, omit the sandbox Content-Security-Policy. Authenticated members who can create and activate workflows can serve HTML that runs on the n8n origin, letting scripts act with the session of users who open the webhook URL.

### CVE-2026-118255

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T19:17:29.900 |

Highcharts JS is a JavaScript charting library based on SVG. From 2.0.0 until 3.2.0, Highcharts Grid applies credits.href to the credits link without validating the URL scheme. An attacker who controls Grid configuration can provide a javascript URL, and activating the credits link runs script in the origin of the hosting page with access to that application's data and session state.This issue is fixed in Grid Pro 3.2.0.

### CVE-2026-118253

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T19:17:29.627 |

Highcharts JS is a JavaScript charting library based on SVG. From 1.0.0 until 4.2.3, Highcharts Dashboards edit mode parses fullscreen language labels as HTML rather than inserting them as text. An attacker who controls Dashboards language options can supply markup with event handlers, which execute in the hosting page origin when the fullscreen control is rendered. The label is reachable only when edit mode is enabled and viewFullscreen is present in the context-menu items. This issue is fixed in 4.2.3.

### CVE-2026-118252

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T19:17:29.483 |

Highcharts JS is a JavaScript charting library based on SVG. From 1.0.0 until 4.2.3, Highcharts Dashboards edit-mode sidebar parses component language strings as HTML rather than inserting them as text. An attacker who controls the Dashboards language configuration can provide markup containing event handlers, which execute in the hosting page origin when a user opens the edit-mode sidebar and the affected labels render. This issue is fixed in 4.2.3.

### CVE-2026-118251

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T19:17:29.340 |

Highcharts JS is a JavaScript charting library based on SVG. Prior to 11.4.9, 12.6.1, and 13.1.0, Highcharts assigns credits.href to the window location when the credits label is clicked without checking the URL against the allowed-scheme list. An attacker who controls chart configuration can provide a javascript URL and run script in the origin of the hosting page when a user clicks the credits label. Highcharts Stock, Maps, and Gantt are included because they ship from the same package. This issue is fixed in 11.4.9, 12.6.1 and 13.1.0.

### CVE-2026-118246

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T18:17:15.540 |

Highcharts JS is a JavaScript charting library based on SVG. From 10.0.0 until 11.4.9, 12.6.1, and 13.1.0, Highcharts applies breadcrumbs.style as SVG attributes rather than CSS and does not filter the attribute names. An attacker who controls chart configuration can provide event-handler keys through drilldown.breadcrumbs, navigation.breadcrumbs, or hierarchical series breadcrumb options. The keys become active handlers on the breadcrumb button and execute in the hosting page origin after the user navigates to a level and hovers over or activates the button. Styled-mode charts do not apply this option and are not affected. This issue is fixed in 11.4.9, 12.6.1 and 13.1.0.

### CVE-2026-21157

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-29T01:17:23.187 |

Improper input validation in Bixby prior to version 4.0.85.6 allows privileged local attackers to launch arbitrary activity.

### CVE-2025-14260

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-28T20:17:14.790 |

Due to the improper implementation of access control rules, the WSO2 product accepts user-supplied input related to resource location without enforcing expected validation constraints. This can be exploited by an unauthenticated actor to direct the server to make requests to arbitrary network locations.

Exploiting this vulnerability allows a malicious actor to access both internal and external resources, available through the network or filesystem, that are reachable by the WSO2 product. This could potentially lead to unauthorized access to sensitive data and systems.

### CVE-2026-118687

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-441` |
| Published | 2026-10-28T19:17:35.807 |

Coder before 2.29.21, 2.30.0 before 2.34.12, 2.35.0 before 2.35.9, 2.36.0 before 2.36.7, and 2.37.0 before 2.37.4 does not validate the audience claim of GCE instance-identity JWTs at the POST /api/v2/workspaceagents/google-instance-identity endpoint. Attackers who obtain an unexpired format=full identity token minted for another relying party can replay it to obtain that workspace agent's session token, which remains valid until the workspace's next build.

### CVE-2026-116794

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-28T18:17:14.127 |

russh is a Rust SSH client and server library that includes an SSH agent protocol implementation. From 0.50.0-beta.12 until 0.65.0, the agent server's Connection::try_sign path in russh/src/keys/agent/server.rs recognizes SSH_AGENT_CONSTRAIN_CONFIRM but returns a hard-coded successful result instead of calling Agent::confirm. In applications that override Agent::confirm to require user approval or another policy check, a process that can reach the agent socket, including the remote side of a forwarded agent, can use a key added through ssh-add -c without that check and can authenticate or sign data as the user while the key remains loaded. The separate Agent::confirm_request hook still runs for every signing request, so checks implemented there remain effective, and implementations that retain the default always-successful Agent::confirm do not lose an approval check through this regression. This issue is fixed in version 0.65.0.

### CVE-2026-59979

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-10-28T16:17:08.620 |

YosemiteCrew provides organization-based service and task management. In the source-reported affected main and dev snapshots, YosemiteCrew's service and PMS task-library/template routes omit organization and permission checks. `authorizeCognito` in `apps/backend/src/middlewares/auth.ts` sets the authenticated user's ID but does not provide the `withOrgPermissions()` and `requirePermission(...)` checks used by protected siblings. In `apps/backend/src/routers/service.router.ts`, `PATCH /fhir/v1/service/:id` and `DELETE /fhir/v1/service/:id` are authentication-only, while `GET /fhir/v1/service/:id` has no authentication middleware. The trace through `apps/backend/src/controllers/web/service.controller.ts` to `apps/backend/src/services/service.service.ts` passes a global record ID into `ServiceModel.findById(oid)` without an `organisationId` filter. In `apps/backend/src/routers/task.router.ts`, `PUT /v1/task/pms/library/:libraryId`, `POST /v1/task/pms/templates`, `PATCH /v1/task/pms/templates/:templateId` and `DELETE /v1/task/pms/templates/:templateId` likewise lack organization/role enforcement. Any registered platform user, including a patient/companion-app account, can modify or delete another organization's service catalogue and PMS task-library/template data, affecting bookings and billing; service records can additionally be read without authentication. An earlier security change protected create routes but left these sibling operations exposed. A fixed release cannot be established from the available evidence.

### CVE-2026-119051

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-29T14:17:52.157 |

flat through 6.0.1 contains an uncontrolled resource allocation vulnerability in unflatten() that allows attackers to create huge sparse arrays via unbounded numeric keys. Attackers can supply flattened keys such as a.4294967294, causing iteration with forEach, spread or JSON.stringify to block the Node.js event loop.

### CVE-2026-118665

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-10-28T21:16:56.827 |

GraphQL Tools provides utilities for building, stitching, and mocking GraphQL schemas. Prior to version 1.1.36 of the GraphQL Tools legacy WebSocket executor package, buildWSLegacyExecutor in packages/executors/legacy-ws/src/index.ts retains request.extensions.connectionParams in the closure-scoped executorConnectionParams object after cleanupWebsocket closes a connection. When one executor is reused across different authorization contexts, a later request that omits a sensitive key can send an earlier caller's Authorization or tenant value in its connection_init payload, causing the downstream server to authenticate the later caller as the earlier user. Applications that create a new executor for every request are not affected. This issue is fixed in version 1.1.36 of the GraphQL Tools legacy WebSocket executor package.

### CVE-2026-118664

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-10-28T21:16:56.687 |

decode-uri-component provides a more robust alternative to decodeURIComponent. Prior to 0.5.1, decodeUriComponent in index.js falls back to customDecodeURIComponent after native decoding throws, and the fallback collects every distinct percent-encoded run before performing a full-string regular-expression replacement for each entry. Malformed input containing many distinct runs can therefore make both the number of replacements and the scanned input length grow together, causing quadratic CPU consumption and blocking the Node.js event loop; request-body inputs can reach the demonstrated size, while ordinary URL header limits reduce the practical delay. This issue is fixed in version 0.5.1.

### CVE-2026-118684

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-327` |
| Published | 2026-10-28T19:17:35.320 |

MONAI before 1.6.1 contains an insufficient integrity verification vulnerability in check_hash() that silently returns True when hash_val is None, with MD5 as the default hash type. Attackers performing man-in-the-middle or registry compromise can substitute bundles, datasets, or model archives downloaded without hashes, enabling malicious file delivery and potential code execution.

### CVE-2026-118262

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-772` |
| Published | 2026-10-28T19:17:30.950 |

Echo is a Go web framework. From 4.15.0 until 4.16.1 and 5.4.1, Echo's Proxy middleware can retain a handler, copy goroutines, and network connections after a WebSocket client disconnects when the upstream keeps its connection open. The raw proxy waits for both copy directions without reliably closing the peer connection when one direction ends, including when a rejected upgrade response uses HTTP keep-alive. Repeated connections can accumulate resources and cause denial of service, depending on proxy-route accessibility, upstream behavior, and connection deadlines. This issue is fixed in 4.16.1 and 5.4.1.

### CVE-2026-118261

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-409` |
| Published | 2026-10-28T19:17:30.810 |

Echo is a Go web framework. From 4.0.0 until 4.16.1, Echo v4's opt-in Decompress middleware exposes a gzip-decoded request stream without limiting its expanded size. A small compressed request can expand into a very large body when a handler reads or binds it, consuming excessive memory or CPU and allowing repeated or concurrent requests to cause denial of service. The middleware is not enabled by default, and limiting only the compressed request size does not bound the decoded size. This issue is fixed in 4.16.1.

### CVE-2026-118260

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-10-28T19:17:30.663 |

Echo is a Go web framework. From 4.0.0 until 4.16.1, Echo v4's opt-in BodyDump middleware reads complete request bodies into memory before handlers run and retains complete response bodies for the dump callback without capture limits. An unauthenticated client that can reach a route using BodyDump can submit large bodies or influence large responses, causing repeated or concurrent allocations that exhaust process memory. BodyDump is not enabled by default, and external request limits may reduce request-side exposure but do not bound response capture. This issue is fixed in 4.16.1.

### CVE-2026-96228

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-29T04:18:45.110 |

SSL Wireless SMS Notification for WordPress is vulnerable to Authentication Bypass in all versions up to, and including, 3.8.1. The public final_login_ajax_action handler resolves a user and issues an authenticated session by matching the wp_sslcare_otp table on only the attacker-supplied phone and cap_data, without verifying the SMS OTP or any server-side single-use state. Because cap_data was chosen by the attacker in the public otp_login_ajax_action step (which stores the row before sending the SMS), the finalize step trivially matches and the user is looked up solely by the sslcare_login_phone meta. This makes it possible for unauthenticated attackers who know a phone-linked user's number to take over that account.

### CVE-2026-85749

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-566;CWE-639` |
| Published | 2026-10-28T23:17:11.100 |

MailWatch for MailScanner is a web-based front-end to MailScanner. Prior to 1.2.27, any authenticated MailWatch user, including the U/user, D/domain-admin, and H/host roles, can release to inbox or permanently delete the quarantined mail of any other user or domain by supplying an arbitrary message `id` to `mailscanner/quarantine_action.php`. The action path calls `quarantine_list_items()` in `mailscanner/functions.php`, which selects from `maillog` by the supplied identifier without the per-role `global_filter` applied by listing and read views. The action requires a valid session and CSRF token, but the caller can submit a token from the caller's own session; ownership of the requested message is never checked. Message identifiers are enumerable, allowing a low-privilege user to invoke `quarantine_release()` or `quarantine_delete()` for other users' or domains' quarantined messages, force-delivering mail held by the quarantine or permanently deleting it. This issue is fixed in version 1.2.27.

### CVE-2026-109411

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-178` |
| Published | 2026-10-28T20:17:17.007 |

An access control bypass flaw was found in Samba's vfs_ceph_rgw module in it's openat() function. An authenticated user can bypass access controls to read or overwrite restricted files on shares configured with the experimental vfs_ceph_rgw module. When a client requests an existing file using mismatched character casing, the module fails to perform a case-insensitive lookup correctly, causing the server to treat the operation as creating a new file. As a result, the server skips standard permission checks on the existing file, allowing the attacker to access or overwrite sensitive data owned by other users.

### CVE-2026-84725

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-28T18:17:20.420 |

when EAP runs with -secmgr, the openjdk-orb's JDKBridge honours attacker-supplied CDR codebase URLs during object unmarshalling on :3528, allowing an unauthenticated attacker to load and instantiate arbitrary classes from a remote URL in the server JVM before EJB security interceptors run.

### CVE-2026-93851

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-28T22:17:17.310 |

Mattermost versions 11.9.x <= 11.9.1, 11.8.x <= 11.8.5, 11.7.x <= 11.7.10 fail to validate the target post ID in the Agents plugin's mention reminder component, which allows an authenticated user who can post in a channel visible to a system administrator to cause the administrator's browser to send an unintended API request, resulting in replacement of an installed plugin and code execution on the server, via a crafted post containing a forged mention reminder that the administrator clicks. Mattermost Advisory ID: MMSA-2026-00742

### CVE-2026-118605

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-28T17:18:27.560 |

Alpine iLX-F511 prh_sdp_service_search_decode Stack-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of Alpine iLX-F511 devices. An attacker must first obtain the ability to pair a malicious Bluetooth device with the target system in order to exploit this vulnerability.

The specific flaw exists within the prh_sdp_service_search_decode function. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a stack-based buffer. An attacker can leverage this vulnerability to execute code in the context of root. Was ZDI-CAN-29069.

### CVE-2026-118603

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-28T17:18:27.323 |

Alpine iLX-F511 vCard Parsing Stack-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected Alpine iLX-F511 devices. User interaction is required to exploit this vulnerability in that the target must connect to a malicious Bluetooth device.

The specific flaw exists within the parsing of vCard data. The issue results from the lack of proper validation of user-supplied data prior to copying it to a fixed-length stack-based buffer. An attacker can leverage this vulnerability to execute code in the context of root. Was ZDI-CAN-29017.

### CVE-2026-93523

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-28T17:18:53.220 |

A heap buffer overflow caused by a XIPassiveUngrabDevice request with an out-of-range modifier value in X.Org X Server before 21.1.15 and XWayland before 24.1.14 could be used by authenticated X clients to crash or potentially execute code in X server context.

### CVE-2026-82961

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-28T17:18:43.680 |

The GPIO syscall handlers in drivers/gpio/gpio_handlers.c did not validate the pin argument supplied by a user-mode caller. z_vrfy_gpio_pin_configure(), z_vrfy_gpio_pin_get_config() and z_vrfy_gpio_pin_interrupt_configure() verified only the device object (K_SYSCALL_DRIVER_GPIO() / K_SYSCALL_OBJ()) and then passed the caller-supplied gpio_pin_t straight through to z_impl_gpio_pin_*() and on to the driver. The only pin check in include/zephyr/drivers/gpio.h was __ASSERT(gpio_port_pin_is_supported(cfg->port_pin_mask, pin), ...), which compiles to nothing unless CONFIG_ASSERT is enabled, so in a production build no check existed at all.

GPIO drivers use pin as a shift count and as an array index on the documented assumption that it is a pin the controller supports. On STM32, for example, gpio_stm32_pin_interrupt_configure() turns pin into an EXTI line and stm32_gpio_intc_set_irq_callback() writes data->cb[line_num].cb and data->cb[line_num].data into a NUM_EXTI_LINES-entry array (default 16) in drivers/interrupt_controller/intc_gpio_stm32.c, guarded only by a compiled-out __ASSERT_NO_MSG(); the same function then reads exti_irq_table[line_num] and calls irq_enable() on the result. Other controllers index fixed-size per-pin configuration tables the same way — drivers/gpio/gpio_ite_it8xxx2_v2.c reads an MMIO base pointer out of wuc_base[8] with the caller's pin and performs a read-modify-write through it.

The issue is reachable only in builds with CONFIG_USERSPACE=y (the file is compiled under that symbol), by a user-mode thread that has been granted access to a GPIO device object. Such a grant is intended to authorize control of that port's pins; the missing validation instead lets the thread drive a supervisor-mode out-of-bounds write of a function pointer and an associated void * past a kernel .bss array, and out-of-bounds reads that feed irq_enable() and MMIO accesses — an escape from the user-mode sandbox that can lead to kernel memory corruption, arbitrary code execution, or a crash.

The fix validates pin against the controller's gpio_driver_config.port_pin_mask with gpio_port_pin_is_supported() in every pin-taking z_vrfy_ handler and returns -EINVAL otherwise, complemented by an unconditional pin >= GPIO_MAX_PINS_PER_PORT range check added to the shared z_impl_gpio_pin_*() inlines.

### CVE-2026-118618

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-28T17:18:28.990 |

Ultralytics parse_model Code Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Ultralytics. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parse_model function. The issue results from the lack of proper validation of a user-supplied string before using it to execute Python code. An attacker can leverage this vulnerability to execute code in the context of the current user. Was ZDI-CAN-30121.

### CVE-2026-118617

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-28T17:18:28.867 |

Ultralytics load_dataset_cache_file Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Ultralytics. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the load_dataset_cache_file function. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of the current user. Was ZDI-CAN-30124.

### CVE-2026-118616

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-28T17:18:28.730 |

Ultralytics parse_model Code Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Ultralytics. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parse_model function. The issue results from the lack of proper validation of a user-supplied string before using it to execute Python code. An attacker can leverage this vulnerability to execute code in the context of the current user. Was ZDI-CAN-30123.

### CVE-2026-118615

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T17:18:28.597 |

Ultralytics torch_safe_load Command Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Ultralytics. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the torch_safe_load function. The issue results from the lack of proper validation of a user-supplied string before using it to execute a system call. An attacker can leverage this vulnerability to execute code in the context of the current user. Was ZDI-CAN-30122.

### CVE-2026-118614

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-28T17:18:28.483 |

Ultralytics check_det_dataset Code Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Ultralytics. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the check_det_dataset function. The issue results from the lack of proper validation of a user-supplied string before using it to execute Python code. An attacker can leverage this vulnerability to execute code in the context of the current user. Was ZDI-CAN-30119.

### CVE-2026-118613

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-28T17:18:28.363 |

Ultralytics torch_load Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Ultralytics. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the torch_load function. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of the current user. Was ZDI-CAN-29652.

### CVE-2026-118602

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-749` |
| Published | 2026-10-28T17:18:27.200 |

Alpine iLX-F511 Fiv.System Exposed Dangerous Method Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of Alpine iLX-F511. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the Fiv service. The issue results from an exposed dangerous method. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of root. Was ZDI-CAN-29095.

### CVE-2026-93522

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-28T16:17:10.183 |

A heap buffer overflow caused by mismatched size usage in CopyArea CPU-to-FBO path in X.Org X Server before 21.1.15 and XWayland before 24.1.14 could be used by authenticated X clients to crash or potentially execute code in the X server context.

### CVE-2026-93521

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-28T16:17:10.060 |

A buffer overflow in RandR
ChangeProviderProperty requests in X.Org X Server before 2.1.25 and XWayland before 24.4.14 could be used by authenticated X clients to crash or execute code within the X server context.

### CVE-2026-93520

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-28T15:17:10.667 |

A heap buffer overflow caused by mismatching size calculations between XkbAllocNames and  ChangeKeycodeRange in X.org X server before 2.1.25 and XWayland before 24.1.14 could be used by authenticated X clients to crash or potentially execute code in X server context.

### CVE-2026-93519

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-28T15:17:10.547 |

A buffer overflow when handling pointer barriers in the XFIXES extension in X.Org X server before 21.1.25 and XWayland before 24.1.14 could be used by authenticated X clients to crash or potentially execute code in X server context.

### CVE-2026-93518

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-28T15:17:10.430 |

An integer truncation issue in XkbResizeKeyType() that could lead to a heap buffer overflow by authenticated X clients in X.org X server before 21.1.25 and XWayland before 24.1.14 could be exploited for crashes or potential code execution in the X server.

### CVE-2026-119027

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-29T12:17:12.167 |

oapi-codegen 2.5.0 before 2.8.1 contains a code injection vulnerability that allows attackers to inject Go code by supplying a crafted servers[].x-go-name value emitted unescaped by the server-urls template. Attackers who control an OpenAPI document can define an injected func init() that executes when the victim builds and imports the generated package.

### CVE-2026-119025

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-29T12:17:12.017 |

open 7.2.0 before 11.0.0 contains an OS command injection vulnerability that allows attackers to execute PowerShell code by supplying crafted URLs on Windows and WSL. Attackers can embed $(...) subexpressions in URLs, such as OAuth authorization_endpoint values from malicious MCP servers, which execute when index.js passes them unescaped to powershell -EncodedCommand.

### CVE-2026-118682

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-28T22:17:12.763 |

KaringX ClashMi through 1.0.32.1801 disables TLS certificate validation by default in the HttpUtils helper, allowing attackers to intercept HTTPS traffic by presenting any certificate. Attackers operating the user's proxy node can serve a forged update manifest omitting sha256 to deliver a malicious installer, achieving code execution when the update runs.

### CVE-2026-13451

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-28T20:17:23.037 |

A flaw was found in KServe. A namespace-scoped user with create/update permissions on InferenceService custom resources can exploit this vulnerability by providing a malicious `storageUri`. This Server-Side Request Forgery (SSRF) vulnerability allows the `storage-initializer` init container to issue arbitrary outbound HTTP/HTTPS requests from inside the cluster. This can lead to information disclosure, including credential theft for the node's Identity and Access Management (IAM) role or access to internal cluster services.

### CVE-2026-88967

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-20;CWE-522;CWE-918` |
| Published | 2026-10-28T17:18:46.090 |

A user with query access to an Azure Monitor data source in Grafana can cause server-side requests to an attacker-controlled endpoint that disclose the data source's Azure access token (server-side request forgery).

### CVE-2026-118510

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-28T17:18:26.780 |

A type-handling flaw in the relationship query building of this MongoDB integration library can cause a check for the absence of a related record to be compiled with an identifier of the wrong data type. In an application that relies on such a check to decide which documents a request may see or act on, a user with basic privileges may be served, may change, or may remove documents that the check was intended to withhold. The failure is silent and produces no error.

### CVE-2026-100105

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-28T17:17:21.797 |

A user with permission to edit contact points but not their protected fields can change protected settings, such as a contact point's destination URL, by switching an integration to a legacy schema version, which can expose stored credentials and redirect alert notifications (incorrect authorization).

### CVE-2026-54455

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-20;CWE-89` |
| Published | 2026-10-28T22:17:15.273 |

OpenCATS is an open-source applicant tracking system and recruitment CRM for staffing agencies and hiring teams. Prior to version 0.10.0, activity DataGrid date filtering in `home:CallsDataGrid` and `activity:ActivityDataGrid` uses request-controlled `period`, `startDate` and `endDate` parameters without sufficient validation or escaping. The vulnerable code is in `modules/home/dataGrids.php` and `modules/activity/dataGrids.php`. The `startDate` and `endDate` values are inserted into SQL string comparisons without safe escaping, and `period` can directly influence generated SQL. An authenticated user with access to the affected DataGrid endpoints can alter the intended query to access sensitive database contents, including user account data, candidate records, contact details, company information, job orders and activity history. A valid OpenCATS login is required; unauthenticated exploitation is not established. This issue is fixed in version 0.10.0.

### CVE-2026-116641

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-28T22:17:12.100 |

The DB Tools rely on the TLS implementation in Golang’s standard library, which generally uses the system CA store. However, the crypto/x509 package also has its own internal denylist of known-bad CA certificates. Golang 1.27.3 adds the eMudhra certificates to this list.




DB Tools version 100.19.0 was compiled with Golang 1.26.8, which does not include this check.




The issue is resolved by updating to Golang 1.27.3 in DB Tools 100.20.0

### CVE-2026-110184

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-29T12:17:09.917 |

The Newsmatic theme for WordPress is vulnerable to blind SQL Injection via the 'slug' parameter in all versions up to, and including, 1.5.0 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-33924

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-29T11:17:33.010 |

Two OS command injection vulnerabilities were discovered in the update installation functionality due to insufficient validation of the update bundle contents. An attacker with administrative privileges can remotely supply a crafted update bundle that, when installed, causes arbitrary commands to be executed with root privileges, allowing the attacker to read or modify sensitive data, change the appliance configuration, or shut down the appliance.

### CVE-2026-33923

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-29T11:17:32.847 |

A signature verification vulnerability was discovered in the update installation functionality due to inconsistent validation of the update bundle contents. An attacker with administrative privileges can remotely supply a crafted update bundle that passes signature verification but runs an unsigned script when the bundle is installed. The script runs with root privileges, allowing the attacker to read or modify sensitive data, change the appliance configuration, or shut down the appliance.

### CVE-2026-115599

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-29T11:17:30.070 |

Missing Authorization vulnerability in ThimPress LearnPress learnpress allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects LearnPress: from n/a through 4.4.11.

### CVE-2026-114193

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-29T11:17:28.080 |

Missing Authorization vulnerability in Eyal Fitoussi GEO my WordPress geo-my-wp allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects GEO my WordPress: from n/a through 4.5.5.5.

### CVE-2026-111418

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-29T10:17:03.313 |

A server-side request forgery (SSRF) vulnerability exists in the Foxit official website’s HTML-to-PDF conversion service. Support for ZIP-formatted input can bypass restrictions on requests to internal IP addresses, potentially allowing discovery of internal network resources.

### CVE-2026-111417

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-29T10:17:03.160 |

A broken access control vulnerability exists in the Foxit official website’s HTML-to-PDF conversion service due to the use of a shared token for submitted conversion documents. This may allow unauthorized users to access documents submitted by other users.

### CVE-2026-111739

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-29T06:17:18.627 |

The Two Factor Authentication WordPress plugin before 1.17.0, All-In-One Security (AIOS)  WordPress plugin before 5.5.0 do not bind the account whose two-factor code is verified to the account being authenticated, allowing an attacker who knows a victim's password and holds their own two-factor-enabled account to satisfy the victim's second-factor check with their own code and obtain the victim's session.

### CVE-2026-93904

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-29T04:18:44.543 |

The Social Web Suite – Social Media Auto Post, Social Media Auto Publish plugin for WordPress is vulnerable to generic SQL Injection via the 'exclude_posts' parameter in all versions up to, and including, 4.1.12 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. The HMAC authentication gate protecting the endpoint is bypassable on any freshly activated installation where an administrator has not yet visited the settings page, because the secret_key option remains empty until lazily generated at that point, allowing an attacker to compute a valid token using hash_hmac('sha256', '', $timestamp) with any chosen timestamp.

### CVE-2026-93855

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-29T04:18:43.923 |

The SendPress Newsletters plugin for WordPress is vulnerable to time-based SQL Injection via the 'subscriberid' parameter in all versions up to, and including, 1.26.1.20 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. The nonce gating the handler uses the hardcoded action value 'sendpress-is-awesome', which is rendered on the same public page served by the [sp-form formid="manage"] shortcode, making it trivially obtainable by unauthenticated visitors and effectively bypassing the nonce as an access control.

### CVE-2026-93757

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-29T04:18:43.763 |

The Wild Apricot Login plugin for WordPress is vulnerable to Authentication Bypass via SSO Email-Collision Account Binding in all versions up to, and including, 1.0.18. When no WildApricot contact-ID mapping is found for an incoming SSO login, the plugin falls back to a network-global `get_user_by('email', ...)` lookup in `Module.php` to resolve a WordPress user, then `UserSynchronizer::syncWaContact()` binds and `Controller::login()` issues a session cookie via `wp_set_auth_cookie()` for that resolved user — both guarded only by `is_super_admin()` — without ever requiring proof of ownership of the matched WordPress account such as a password, local account-linking confirmation, inbox verification, or administrator approval. This makes it possible for attackers with custom-level WildApricot membership access to authenticate as an existing WordPress subsite administrator on a path-based Multisite network, obtaining a valid network-global authentication cookie for the victim without their credentials. Exploitation requires that the attacker control a WildApricot contact whose email address matches the target WordPress administrator's email — achievable via a public zero-fee membership application on the connected WildApricot organization — and that they complete the SSO flow on any subsite where Wild Apricot Login is active; because WordPress user identities and authentication cookies are network-global, the cookie issued on that subsite is equally valid on any other subsite where the victim user holds an administrator role.

### CVE-2026-61569

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-28T22:17:16.043 |

AVideo is a video-sharing Platform. Prior to 8.1.0, the unauthenticated streamer login at `objects/login.json.php` passes the `user` parameter to `Streamer::get` in `objects/Streamer.php`, where it is interpolated into a single-quoted MariaDB SELECT without parameterization or escaping. Although `objects/security.php` strips literal single quotes, `html_entity_decode` in `objects/Login.php` restores entity-encoded quotes before the query. The supplied `siteURL` must pass the streamer allowlist, which allows all sites when empty by default, and an attacker-hosted login response must set `canUpload` or `isAdmin` to reach `Streamer::createIfNotExists`. That function calls `Streamer::get` before its additional allowlist check. UNION results are exposed through `streamers_id`, while failures return the rendered query and MariaDB error. An attacker can read arbitrary encoder database data, including stored upstream streamer credentials, allowlist configuration, and queue records, without encoder credentials. Stacked statements are not permitted by the mysqli driver and the tested database account lacks global FILE privilege, so the demonstrated vector is bounded to reads rather than server-side file writes. Stolen streamer credentials can provide continued upstream access until rotated. This issue is fixed in version 8.1.0.

### CVE-2026-118804

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-28T22:17:14.963 |

Bricks Builder 2.4.3 and before contains a broken access control vulnerability that allows unauthenticated attackers to access restricted post content by submitting crafted post_status and post_type values in the originalQueryVars parameter to the POST /wp-json/bricks/v1/query_result REST endpoint using a publicly obtainable nonce. Attackers can set post_status to draft or private, or post_type to shop_coupon, to disclose unpublished posts, private content, and WooCommerce coupon data that is otherwise blocked by the standard WordPress REST API routes.

### CVE-2026-118803

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-1336` |
| Published | 2026-10-28T22:17:14.827 |

Bricks Theme 2.4.3 and before contains an unauthenticated dynamic-data tag injection vulnerability that allows anonymous attackers to control the urlParams object in the query_result REST endpoint, causing the submitted value to be re-parsed as a Bricks dynamic data tag. Attackers can inject tags such as author_meta:user_pass, author_meta:user_email, or cf_coupon_amount to leak post meta and the post author's user record, including the password hash, without authentication.

### CVE-2026-118659

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-28T21:16:55.967 |

Happy DOM is a JavaScript implementation of a web browser without its graphical user interface. Prior to 21.0.2, the Happy DOM server-renderer package's ServerRendererServer accepts unauthenticated HTTP/2 requests and resolves attacker-controlled :path values against server.targetOrigin in #onIncomingRequest in packages/@happy-dom/server-renderer/src/ServerRendererServer.ts without confirming that the resolved origin remains trusted before calling fetch. A protocol-relative path can change the destination to an arbitrary HTTP or HTTPS endpoint reachable by the server, including local and internal services, and the proxy relays the fetched response headers and body to the requester. This issue is fixed in version 21.0.2.

### CVE-2026-118650

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-177;CWE-863` |
| Published | 2026-10-28T20:17:21.850 |

Echo is a Go web framework. Prior to 4.16.0 and 5.4.0, a globally mounted middleware.Static instance can interpret an encoded request path differently from Echo's router because the router matches the still-encoded path while the static handler uses the decoded URL.Path. The advisory demonstrates an encoded slash resolving to a file under the static root through the global static middleware, but the source is internally inconsistent about whether a route or group guard protects the corresponding literal path in that global-mount configuration. This issue is fixed in 4.16.0 and 5.4.0.

### CVE-2026-116795

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407;CWE-1333` |
| Published | 2026-10-28T18:17:14.303 |

RE2JS is the JavaScript port of RE2, a regular expression engine that provides linear time matching. From 2.2.0 until 2.8.7, enabling LOOKBEHINDS and using repeated matching through matcher().find(), matchAll(), split(), or matcher().replaceAll() can cause quadratic total work. Machine.match restarts lookbehind scanning from offset zero for each requested start position, while Matcher-based APIs request capture slots that prevent the early exit used for captureless matching. Dense matches therefore repeatedly rescan the input, allowing attacker-influenced text to monopolize a single-threaded worker and deny service. This issue is fixed in version 2.8.7.

### CVE-2026-103410

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190;CWE-835` |
| Published | 2026-10-28T17:17:28.177 |

An Integer Overflow vulnerability in the DPI certificate scanner in Juniper Networks Session Smart Router allows an unauthenticated remote attacker to cause a denial of service via a specially crafted TLS server certificate.

### CVE-2026-47235

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-10-28T16:17:07.563 |

SimulationCraft is a tool to explore combat mechanics in World of Warcraft. In builds after release-820-01 and before the identified May 7, 2026 nightly, the `bcp_api.cpp` loop over the JSON `sockets` array uses `slot_data["sockets"].Size()` without bounding `gem_idx` by `MAX_GEM_SLOTS`, which is four in `engine/sc_enums.hpp`. The destination `gem_id` and `gem_bonus_id` arrays in `engine/item/item.hpp` have only four elements. More than four socket entries therefore write beyond `gem_id` into the adjacent `gem_bonus_id` vector storage; `bonus_list` entries can also access `gem_bonus_id` out of bounds. Corrupting a vector's `_M_start` pointer causes the `item_t` destructor to free an attacker-influenced pointer during normal cleanup. The advisory reports crashes and code execution demonstrated in a testing environment. Attack inputs can arrive through a malicious `.simc` profile with a `[[equipment]]` section, a compromised addon export, or `Battle.net API` responses modified by an attacker with a privileged network position. The fix is contained in the nightly build identified as simc-1205-01-516b5d7; no containing release tag is available.

### CVE-2026-15564

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-29T06:17:20.590 |

Wildfly's IIOP listener may permit deserialization of input streams before authentication is performed. An attacker who can gain access to the IIOP port may be able to construct and send malicious objects and achieve deserialization, if the target EJB allows untyped method parameters, and depending on the potential gadget chains available in the running classpath.

### CVE-2026-114488

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-29T06:17:19.103 |

A flaw was found in Wildfly. A remote attacker can bypass authentication on IIOP EJB invocations as the CSIv2 security interceptor accepts ITTPrincipalName identity assertions in the service context without verifying transport-level authentication, allowing a pre-auth attacker on the port 3528 to impersonate any principal on every IIOP-exposed @Remote EJB.

### CVE-2026-6647

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-613` |
| Published | 2026-10-28T20:18:44.080 |

In deployments of WSO2 Identity Server configured with a case-insensitive user store and a case-sensitive database for identity data, mismatches in username case handling can occur. This inconsistency results in OAuth token revocation operations failing to correctly identify usernames containing mixed-case characters during certain lifecycle events, preventing tokens from being invalidated.

A malicious actor can exploit this vulnerability by possessing a valid access or refresh token associated with a mixed-case username. In affected configurations, these tokens may not be revoked when expected. The actor can then leverage these unrevoked tokens, before their expiry, to continue performing actions that should have been restricted, effectively bypassing intended access controls.

### CVE-2026-61571

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-306;CWE-862` |
| Published | 2026-10-28T22:17:16.193 |

AVideo is a video-sharing Platform. Prior to 8.1.0, the encoder lacks a global authentication layer and exposes control and status PHP endpoints to anonymous network callers. `view/run.php` has a commented-out guard and invokes `Encoder::run()`. `view/queue.json.php` calls `Encoder::getAll(true)`, reveals streamer URLs through `getSiteURL()`, and triggers processing with `execRun()`. `view/status.php` returns `Access-Control-Allow-Origin` with a wildcard, reads the queue, triggers processing, and exposes host memory statistics through `ServerMonitor::getMemory()` when `serverStatus` is set. `view/listFiles.json.php` checks only `Login::canBulkEncode()`, which admits anonymous callers whenever `disableBulkEncode` is empty, the default. Its `path` parameter is resolved with `realpath()` and listed with `scandir()` without a base-directory restriction. An unauthenticated attacker can drive the privileged queue processor, read queue and streamer-site information, obtain memory statistics and enumerate media file names and paths in any directory readable by the web-server user. Enumeration is limited to configured media extensions and does not itself disclose arbitrary file contents. This issue is fixed in version 8.1.0.

### CVE-2026-119049

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-29T14:17:51.827 |

FreeMail before 5.3.2 contains an authorization bypass vulnerability that allows authenticated users to claim another user's existing mailbox via the POST /api/create endpoint. Attackers who know a victim's address can become co-owners through assignMailboxToUser to read messages and verification codes, set forwarding, and delete mail.

### CVE-2026-96767

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T12:17:14.300 |

The NEX-Forms – Ultimate Forms Plugin for WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'type' parameter in all versions up to, and including, 9.3.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-115821

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T12:17:11.767 |

The NewsmanApp plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'billing_first_name, billing_last_name' parameter in all versions up to, and including, 3.7.29 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This vulnerability is only exploitable when the Newsman Remarketing feature is enabled and a non-empty Remarketing ID is configured in the plugin settings.

### CVE-2026-107743

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T10:17:02.580 |

The Mapster WP Maps plugin for WordPress is vulnerable to Stored Cross-Site Scripting in versions up to, and including, 2.0.5. This is due to the /wp-json/mapster-wp-maps/save-mapmaker REST route being registered with a permission_callback that unconditionally returns true (no capability check, no nonce), together with the mapster_write_config_to_acf() helper only sanitizing string config values with sanitize_text_field() — which strips HTML tags but leaves quote characters intact — and the mapster_wp_map shortcode renderer in mapster_wordpress_maps_shortcode_display() concatenating the stored loading_background_color value into a single-quoted inline style attribute without esc_attr(). This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-115301

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-29T06:17:20.080 |

The Contact Form by Supsystic  WordPress plugin before 1.11.1 does not sandbox the template engine used to render its forms and allows stored form-editor content to reach that engine as executable template code, enabling an administrator to perform server-side template injection and execute arbitrary code on the server. The injected template is compiled and executed whenever any visitor loads a page containing the form, so the stored payload also lets an unauthenticated visitor read server-side secrets such as authentication salts and database credentials.

### CVE-2026-96741

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T04:18:45.600 |

The DSGVO All in one for WP plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content via Output Buffer Regex Corruption in all versions up to, and including, 5.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is only exploitable when the administrator has enabled both the 'Google Tag Manager' integration and the 'Replace integration automatically [Beta]' option, and requires the crafted comment to be approved by an administrator.

### CVE-2026-96669

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T04:18:45.430 |

The Food Store – Online Food Delivery & Pickup plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'service_type' Cookie in all versions up to, and including, 1.5.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The attack is seeded unauthenticated by supplying a payload via the ?type= query parameter on the public checkout page, which the plugin writes directly into the browser's service_type cookie; this cookie value is later persisted to order meta and rendered unescaped in the admin panel.

### CVE-2026-96666

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T04:18:45.273 |

The Schema App Structured Data plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content via 'Remove Microdata' Output Filter in all versions up to, and including, 2.3.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires that an administrator has enabled the plugin's 'Remove Microdata' option and approves the malicious comment.

### CVE-2026-54453

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74;CWE-94` |
| Published | 2026-10-28T22:17:15.100 |

OpenCATS is an open-source applicant tracking system and recruitment CRM for staffing agencies and hiring teams. Prior to version 0.10.0, the Professional License configuration feature in `SettingsUI` (`manageProfessional`) accepts administrator-controlled license key input that is reconstructed into a PHP `define()` statement in `config.php` without safe escaping. Because the application includes `config.php`, crafted input can alter the file's PHP syntax and cause persistent arbitrary PHP execution with the web server process privileges. An authenticated administrator must have Settings module access and permission to update Professional License configuration, and `config.php` must be writable for this write-based path. Successful exploitation can read, modify or delete application data, expose candidate, contact, company, job order and user account information, alter the installation or configuration, and provide a foothold for further attacks. Unauthenticated exploitation and exploitation without Settings access are not established. This issue is fixed in version 0.10.0.

### CVE-2026-118257

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79;CWE-116` |
| Published | 2026-10-28T19:17:30.207 |

Vue I18n is the internationalization plugin for Vue.js. From 11.1.10 until 11.4.14 and from 12.0.0-alpha.4 until 12.0.0-alpha.5, sanitizeTranslatedHtml() escapes markup and event-handler text inside an iframe srcdoc value but leaves the srcdoc attribute active. Browsers decode the character references and parse the value as a same-origin nested HTML document, allowing attacker-controlled parameters or translation content placed in srcdoc to execute script when applications enable escapeParameter and render translations as HTML through v-html. Versions 9.14.5 and 10.0.8 are also affected and are no longer supported, while i18n-t rendering is not affected. This issue is fixed in versions 11.4.14 and 12.0.0-alpha.5.

### CVE-2026-118250

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-10-28T18:17:16.543 |

Highcharts JS is a JavaScript charting library based on SVG. From 6.1.0 until 11.4.9, 12.6.1, and 3.1.0, Highcharts follows dot-separated series.keys paths without filtering each segment. An attacker who controls series.keys and matching point data can use a path through __proto__ to assign arbitrary named properties to Object.prototype. Those properties are visible to all JavaScript in the page, and no user interaction is required beyond rendering the chart. This issue is fixed in 11.4.9, 12.6.1, and 3.1.0.

### CVE-2026-118249

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-10-28T18:17:16.273 |

Highcharts JS is a JavaScript charting library based on SVG. From 13.0.0 until 13.1.0, Highcharts builds series data columns by using point option keys directly as column IDs. Own enumerable __proto__ and constructor keys from parsed point objects can therefore direct integer-indexed writes to Object.prototype or the Object constructor. The inherited values affect reads and for-in enumeration across the page and can disrupt rendering or alter consuming application behavior without user interaction beyond rendering the chart. This issue is fixed in 13.1.0.

### CVE-2026-118244

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T18:17:15.260 |

Highcharts JS is a JavaScript charting library based on SVG. From 12.0.0 until 12.6.1 and 13.1.0, Highcharts falls back to assigning raw markup to innerHTML when DOMParser cannot return a document, before its allow-list is applied. In Chromium, the Trusted Types callback can throw while a beforeprint handler runs, so a page that redraws a chart during beforeprint can insert untrusted HTML text options into the hosting document. Event handlers in that markup then run in the page origin when printing begins. The issue affects HTML-rendered titles, labels, data labels, responsive text, and the Stock, Maps, and Gantt products shipped in the same package. This issue is fixed in 12.6.1 and 13.1.0.

### CVE-2026-116796

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T18:17:14.460 |

Highcharts JS is a JavaScript charting library based on SVG. From 10.3.2 until 11.4.9, 12.6.2, and 13.1.1, Highcharts accepts an SVG anchor xlink:href attribute without applying the allowed-scheme check used for href and src. An attacker who controls a chart text option can preserve a javascript URL in serialized chart output. When exported or server-rendered SVG is parsed again and a user activates the link, script runs in the origin of that document. This issue is fixed in 11.4.9, 12.6.2 and 13.1.1.

### CVE-2026-109822

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-922` |
| Published | 2026-10-29T12:17:09.773 |

Yamaha wireless LAN router NWR100 provided by Yamaha Corporation contains an issue with insecure storage of sensitive information. Configuration files generated by the CONFIG file export function may be read by an unauthenticated attacker.

### CVE-2026-116409

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T11:17:31.630 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WP Swings Upsell Order Bump Offer for WooCommerce upsell-order-bump-offer-for-woocommerce allows Reflected XSS.This issue affects Upsell Order Bump Offer for WooCommerce: from n/a through 3.1.6.

### CVE-2026-115963

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-29T11:17:31.097 |

Missing Authorization vulnerability in VideoWhisper.com Broadcast Live Video videowhisper-live-streaming-integration allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Broadcast Live Video: from n/a through 7.3.9.

### CVE-2026-115611

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T11:17:30.207 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in PluginUs.Net TableOn posts-table-filterable allows Reflected XSS.This issue affects TableOn: from n/a through 1.0.7.

### CVE-2026-115592

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T11:17:29.937 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in OceanWP OceanWP oceanwp allows Reflected XSS.This issue affects OceanWP: from n/a through 4.2.7.

### CVE-2026-112827

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-29T11:17:27.473 |

Missing Authorization vulnerability in VillaTheme HANDMADE – Dropshipping for Etsy and WooCommerce handmade-dropshipping-for-etsy-and-woo allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects HANDMADE – Dropshipping for Etsy and WooCommerce: from n/a through 1.0.10.

### CVE-2026-117611

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-29T10:17:03.730 |

Improper certificate validation in Checkmk <2.5.0p18, <2.4.0p39, <2.3.0p52 and 2.2.0 (EOL): the Certificate Authority stores bundled with "certifi" and "webpki-roots" include a root CA that trusts eMudhra (emSign) intermediate certificates whose private keys are public.

### CVE-2026-118905

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-94` |
| Published | 2026-10-29T06:17:20.343 |

Node Version Manager (nvm) is a POSIX-compliant shell function for managing multiple node.js versions. In versions 0.31.2 through 0.40.5, `nvm_ls` filters installed versions with a sed program that embeds the requested version pattern in a `\#...#` address, escaping `.` (and, since 0.40.4, `#`) but not backslash. A version string containing `#` (or `\#`) therefore closes the address early, and the rest of it is parsed as sed commands: with GNU sed, the `e` command runs a shell command as the user; with BSD sed, the `w` and `r` commands write and read files. This is reachable whenever an attacker-influenced version string is passed to `nvm use`, `nvm which`, `nvm ls`, `nvm version`, `nvm run`, or `nvm exec`, or to `nvm-exec` via `NODE_VERSION`, and at least one version is installed. nvm's own `.nvmrc` parser strips comments, so a bare `nvm use` is not affected; however, the bash `cdnvm` and zsh `load-nvmrc` auto-switch hooks documented in the README read `.nvmrc` as-is and pass it to `nvm ls` and `nvm version`, so a user with one of those hooks installed runs the attacker's command just by changing into a directory under a malicious `.nvmrc`; scripts that run `nvm use "$(cat .nvmrc)"` are affected the same way. Version 0.40.6 passes any version pattern containing `#` or a newline through the `.nvmrc` content parser first, so no `#` reaches the sed program.

### CVE-2026-66090

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-29T02:16:52.803 |

In openEQUELLA before 2026.1, the XML parser used for item metadata does not disable external entity resolution. A user permitted to create items (CREATE_ITEM) can submit crafted XML to POST /api/item and cause the server to read arbitrary files accessible to the openEQUELLA service, or make requests to attacker-specified locations (SSRF), including cloud instance metadata services.

### CVE-2026-118692

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T22:17:13.387 |

CherryTree through 1.7.2 contains an OS command injection vulnerability in CtActions::link_clicked that allows attackers to execute commands by embedding shell metacharacters in web link URLs. When the non-default Custom Web Link Clicked Action option is enabled, attackers can supply crafted documents whose links pass $(...), backticks, or semicolons unquoted to std::system, running commands as the victim on click.

### CVE-2026-118678

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-10-28T19:17:33.957 |

n8n before 2.41.4 and 2.42.x before 2.42.1 contains a prototype pollution vulnerability that allows low-privileged users to alter built-in object behaviour by saving workflows with specially named connection keys. Attackers can add keys such as __proto__ to workflow connections, which the periodic history compaction task processes, causing logins and writes to fail with server errors.

### CVE-2026-118646

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-28T19:17:32.760 |

n8n before 1.123.85, 2.43.5, and 2.44.1 contains a regular expression denial of service vulnerability that allows authenticated members to block the event loop via crafted glob patterns. Attackers who can create and run workflows can submit a wildcard-heavy File(s) Selector pattern causing exponential backtracking, making the UI, API, webhooks, and health checks unresponsive until restart.

### CVE-2026-103411

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-28T17:17:28.397 |

An Integer Underflow vulnerability in DhcpMessageDecoder in Juniper Networks Session Smart Router allows an attacker with local network access to cause information disclosure and a denial of service via a malicious DHCP reply.

### CVE-2026-118984

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-620` |
| Published | 2026-10-29T11:17:32.257 |

OmniRoute 3.8.0 before 3.8.52 contains an unverified password change vulnerability that allows holders of manage- or admin-scoped API keys or oma_ access tokens to change the management password without the current password. Attackers can send POST requests to /api/settings/require-login to lock out the operator, take over dashboard login, or disable the login requirement entirely.

### CVE-2026-118645

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-10-28T19:17:32.597 |

n8n before 1.123.85, 2.x before 2.43.5, and 2.44.x before 2.44.1 contains a filter injection vulnerability in the Quick Base node, which sends the Where filter to the Quick Base API as raw query text. Attackers supplying untrusted input such as webhook data used to build the filter can make Get Many return every record or Delete remove every record with the workflow credential's privileges.

### CVE-2026-116776

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:H/UI:P/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-28T16:17:06.773 |

USB Test is a lightweight Windows CLI utility for verifying sector integrity and detecting overreported capacity on USB flash drives. Prior to version 1.1.5, getSectorSize() in USB Test/src/driveinfo.cpp trusts DISK_GEOMETRY.BytesPerSector returned by IOCTL_DISK_GET_DRIVE_GEOMETRY without checking whether the call succeeded or enforcing size bounds. USB Test/src/drivetest.cpp uses the value for division and to size a heap buffer before memcpy(buffer.data(), &sector, 8), so a physically connected malicious USB storage device can report a value below eight bytes and cause repeated out-of-bounds writes, or report zero and cause a divide-by-zero denial of service when a user starts a drive test. The heap corruption can crash the elevated application and may permit arbitrary code execution. This issue is fixed in version 1.1.5.
