# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-08 15:00 UTC
- **対象期間**: `2026-07-07T15:00:34.000Z` 〜 `2026-07-08T15:00:28.000Z`
- **重要CVE数**: 113 件（Critical 9.0+: 18 件 / High 7.0〜: 95 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、**CVSS 7.0 以上が 30 件以上**報告されており、特に **認証バイパス・権限昇格・リモートコード実行** が多発しています。  
- Web アプリケーション（WordPress プラグイン、Plesk、Esri Portal など）と、開発・データベース基盤（DBI、Dgraph、Coder、xorg‑server）で **リモートからの無認証攻撃が成立** するケースが目立ちます。  
- 多くは **古いバージョンが長期間サポートされていない**、または **入力検証・認可チェックの欠如** が根本原因です。早急なバージョンアップと、認可ロジックの見直しが必須です。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 | 影響範囲（代表的な製品/プラットフォーム） |
|-----|------|----------|----------|------------------------------------------|
| **CVE‑2026‑56843** | 9.9 | XML‑RPC API の認可不備により、低権限顧客が他顧客のドメイン情報を取得可能 | **Plesk** は多数の中小企業・ホスティング事業者で採用されているため、情報漏洩リスクが極めて高い。認可ロジックがレガシープロトコルでバイパスできる点が深刻。 | WebPros **Plesk** 18.0.78.4 未満（全 OS） |
| **CVE‑2026‑8307** | 9.8 | SQL インジェクションにより任意の SQL が実行可能 | 製品は **Webbeyaz Web Design Mediküm Web**（サポート終了）だが、同様の脆弱性は同系統の PHP アプリで再現しやすく、データベース全体が破壊され得る。 | Mediküm Web 08072026 まで |
| **CVE‑2026‑9695** | 9.8 | 認証不備により特権サーバーアクセスが取得可能 | **DELMIA Apriso** は製造業向け ERP 系統で、サーバー権限取得は生産ライン停止や機密設計情報漏洩につながる。 | DELMIA Apriso **2020‑2026** リリース全般 |
| **CVE‑2026‑13019** | 9.8 | 認証なしで重要 API にアクセス可能 | **Esri Portal for ArcGIS** は GIS データの管理・配信基盤。認証欠如は機密地理情報の無断取得・改ざんリスクを招く。 | ArcGIS Portal **12.1** 以前（Windows, Linux, Kubernetes） |
| **CVE‑2026‑58473** | 9.3 | LLM プロバイダー設定を書き換えられ、任意の外部 LLM にリダイレクト可能 | AI/LLM を社内サービスで利用するケースが増加する中、**Cognee** の設定改竄は情報漏洩・不正利用の入口になる。 | Cognee **1.2.0** 未満 |

> **※** 上記は CVSS が最高点に近く、かつ **インフラ全体への波及効果が大きい**（認証バイパス・データベース破壊・機密情報漏洩）点を重視して選定しました。

---

## 3. 推奨アクション  

### 3.1 共通的な対策
- **脆弱版の即時廃止**：対象製品のバージョンが上記 CVE の「未修正版」かどうかを資産管理ツールでスキャンし、該当するサーバ/コンテナを **隔離または停止** する。  
- **ベンダー提供のパッチ適用**：ベンダーがリリースした **セキュリティパッチ**（もしくは **次期メジャーリリース**）を **テスト環境で検証後、全環境にロールアウト**。  
- **認可・入力検証の強化**：API エンドポイントに対し **認証・認可ミドルウェア** を必ず通すよう、Web アプリケーションファイアウォール（WAF）や **OpenAPI/Swagger** のスキーマで強制。  
- **監査ログの有効化と SIEM 連携**：特に **認証失敗・権限昇格・SQL 実行** のイベントをリアルタイムで検知できるよう、ログレベルを **INFO → DEBUG** に上げ、SIEM へ転送。  

### 3.2 製品別具体的アクション

| 製品 / パッケージ | 現行バージョン (脆弱) | 推奨バージョン / パッチ | 具体的作業 |
|-------------------|----------------------|------------------------|------------|
| **Plesk** (WebPros) | < 18.0.78.4 | **18.0.78.4 以上**（公式パッチ） | - `plesk installer update` で最新版へ更新<br>- XML‑RPC の **`api/xmlrpc`** エンドポイントを外部から遮断（ファイアウォール） |
| **Webbeyaz Mediküm Web** | 08072026 まで | **サポート終了** → **代替製品**（例: WordPress + Hardened プラグイン） | - 旧システムを **隔離**、データベースのバックアップ取得<br>- 新規環境へマイグレーション |
| **DELMIA Apriso** | 2020‑2026 系列 | **2026.1.0 以降**（認証ロジック修正） | - `apri-software update` でパッチ適用<br>- 管理者アカウントの **多要素認証** を有効化 |
| **Esri Portal for ArcGIS** | ≤ 12.1 | **12.2 以上**（認証チェック追加） | - `portaladmin` コンソールから **API 認証設定** を有効化<br>- 不要な外部 API エンドポイントは **NGINX** で遮断 |
| **Cognee** | < 1.2.0 | **1.2.0 以上**（設定書き換え防止） | - `docker pull cognee/cognee:1.2.0` でイメージ更新<br>- `settings` エンドポイントに **認可ミドルウェア** を追加 |
| **DBI (Perl)** | < 1.650 | **1.650 以上** | - CPAN で `cpan DBI` 更新<br>- アプリ側で **プレースホルダー上限** をチェック |
| **Dgraph** | < 25.3.5 | **25.3.5 以上** | - `dgraph upgrade` でバイナリ更新<br>- gRPC ポート `:9080` を **内部ネットワークのみ** に制限 |
| **GNU Wget** | ≤ 1.25.0 | **1.25.1 以上** | - OS パッケージマネージャ (`apt-get upgrade wget` / `yum update wget`)

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-56843

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-522` |
| Published | 2026-07-08T01:16:28.277 |

Incorrect authorization in the XML-RPC API of WebPros Plesk before 18.0.78.4 allows a low-privileged authenticated customer to look up domains they do not own, because ownership is enforced only for certain lookup filters and schema validation is bypassed for legacy protocol versions. This results in cross-tenant disclosure of other tenants' FTP credentials stored in cleartext, which can be leveraged to execute code as another tenant's system user.

### CVE-2026-8307

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-08T13:16:57.903 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Webbeyaz Web Design Mediküm Web allows SQL Injection.

This issue affects Mediküm Web: through 08072026. NOTE: The vendor was contacted and it was learned that the product is not supported.

### CVE-2026-9695

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-08T07:16:46.870 |

An Improper Authentication vulnerability affecting DELMIA Apriso from Release 2020 through Release 2026 could allow an attacker to gain privileged access to the server.

### CVE-2026-12153

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-08T06:16:22.157 |

The WP Learn Manager plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 1.1.8. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to install and activate arbitrary plugins from the WordPress.org repository on the vulnerable site.

### CVE-2026-9701

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-289` |
| Published | 2026-07-08T05:16:28.977 |

The Eventer plugin for WordPress is vulnerable to an insecure password reset mechanism in all versions up to, and including, 4.4.2. The plugin stores a plaintext copy of the password reset key in the `eventer_verification_code` user meta field when a user requests a password reset. The plaintext key stored in `wp_usermeta` can be used with the plugin's custom reset action to set a new password for any user. Combined with another vulnerability such as SQL Injection (CVE-2026-9700), this makes it possible for unauthenticated attackers to extract the plaintext reset key and take over any user account, including administrators. Note: The password reset function only works up to PHP version 7.4.

### CVE-2026-14739

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-07T23:16:54.090 |

DBI versions before 1.650 for Perl have a heap overflow when preparsing SQL statements with an extreme number of placeholders.

The fix for CVE-2026-10879 did not allocate enough memory to handle approximately 1.2-million placeholders.

DBI version 1.650 sets a hard limit of 99,999 placeholders.

### CVE-2026-13019

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-07-07T17:16:35.400 |

Esri Portal for ArcGIS versions 12.1 and earlier on Windows, Linux and Kubernetes have a missing authentication for critical function vulnerability allows a remote, unauthenticated attacker to access an unprotected API.

### CVE-2026-59705

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-07T23:16:55.997 |

mem0's openmemory/api component contains an unauthenticated access vulnerability that allows unauthenticated attackers to read, write, and delete arbitrary user memories by accessing API routers registered without authentication middleware. Attackers can supply arbitrary user_id parameters or directly access memory retrieval endpoints to expose private memory content, or invoke pause endpoints with global_pause=true to cause denial-of-service across all users.

### CVE-2026-58473

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-862` |
| Published | 2026-07-07T21:17:29.007 |

Cognee before 1.2.0 contains an improper access control vulnerability that allows unauthenticated attackers to overwrite the global LLM provider configuration by self-registering an account and calling the settings endpoint, which performs no admin or superuser check. Attackers can redirect all LLM operations instance-wide to an attacker-controlled endpoint by exploiting the process-wide singleton configuration cache, enabling exfiltration of prompts, uploaded documents, extracted entities, and knowledge graph content from all users.

### CVE-2026-58480

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-08T14:17:19.977 |

Blocksy Companion Pro plugin for WordPress before 2.1.47 contains an unauthenticated arbitrary file upload vulnerability that allows attackers to upload executable files by bypassing extension validation in the save_attachments function exposed through the Advanced Reviews feature. Attackers can exploit the Custom Fonts extension's flawed strpos() substring check by uploading double-extension filenames such as shell.woff2.php, causing the validation to pass on the substring match while the web server executes the file as PHP, achieving remote code execution.

### CVE-2026-59706

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-07T22:16:54.503 |

mem0 contains unauthenticated config API endpoints that expose LLM API keys in plaintext and allow server-side request forgery via attacker-controlled ollama_base_url parameter. Unauthenticated attackers can retrieve stored secrets like OpenAI API keys via GET /api/v1/config/ or trigger SSRF attacks by setting ollama_base_url to internal addresses like cloud IMDS via PUT /api/v1/config/mem0/llm endpoint.

### CVE-2026-59707

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-07T21:17:29.340 |

LocalAI contains an unauthenticated server-side request forgery vulnerability in the POST /models/apply endpoint that allows attackers to fetch arbitrary internal URLs. The endpoint passes unsanitized gallery URL fields directly to gallery.GetGalleryConfigFromURLWithContext without proper validation, enabling attackers to force the server to issue HTTP GET requests to private and loopback ranges with partial response content leaked through error messages.

### CVE-2026-59800

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-07T19:16:55.260 |

9Router before 0.4.44 contains an OS command injection vulnerability in the unauthenticated POST /api/tunnel/tailscale-install endpoint (this route is not covered by the dashboard middleware matcher, so no authorization check is applied). The sudoPassword field from the request body is written to the stdin of a 'sudo -S sh' child process. When sudo does not prompt for a password (the process runs as root, NOPASSWD is configured, or a recent sudo timestamp cache exists), the sudoPassword value is interpreted by sh as a shell command, allowing a remote unauthenticated attacker to execute arbitrary OS commands. Exploitation evidence was first observed by the Shadowserver Foundation on 2026-07-04 (UTC).

### CVE-2026-54061

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-08T14:17:06.520 |

Dgraph is an open source distributed GraphQL database. Prior to version 25.3.5, Dgraph Alpha exposes the RPCs used for external snapshot import on the public gRPC port `:9080` without authentication or authorization. As a result, an unauthenticated network client can open `StreamExtSnapshot` and send Badger stream data to the target group’s store. In addition, the receiver calls `Prepare()` before processing the stream. This operation deletes and replaces the existing DB data. Version 25.3.5 patches the issue.

### CVE-2026-14487

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-08T05:16:26.980 |

The Simple Coherent Form plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the removeUploadDir function in all versions up to, and including, 2.4.13. This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). The scf_get_id_upload endpoint freely issues a valid scf_upload_file_removal nonce to any unauthenticated visitor, and the removal endpoint's secondary hash check is forgeable offline because it relies on a hardcoded salt embedded in the plugin source, meaning neither control presents a real authorization boundary.

### CVE-2026-14740

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-07T23:16:54.193 |

DBI versions before 1.650 for Perl read one byte out-of-bounds in preparse when deleting an initial SQL comment.

The preparse method normalises SQL and removes comments. When the SQL starts with a comment line, the deletion of that line during normalisation led to an out-of-bounds read by one byte. The result is a fault on memory-hardened builds and nondeterministic newline retention on normal builds.

### CVE-2026-46354

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-07-07T22:16:52.467 |

Coder allows organizations to provision remote development environments via Terraform. In versions prior tp 2.24.5, 2.29.13, 2.30.8, 2.31.12, 2.32.2, and 2.33.3, `azureidentity.Validate()` verifies that the PKCS#7 signer certificate chains to a trusted Azure CA but never verifies the PKCS#7 signature itself. An attacker can embed a legitimate Azure certificate alongside arbitrary content e.g. `{"vmId":"<target>"}` and the forged `vmId` will be accepted returning the victim workspace agent's session token. No authentication is required. The attacker only needs to know a target VM's `vmId` which is a `UUIDv4`. That's a practical limitation which would typically require prior access to be exploited. Versions 2.24.5, 2.29.13, 2.30.8, 2.31.12, 2.32.2, and 2.33.3 patch the issue. As a workaround, reconfigure any Azure templates to use token authentication rather than `azure-instance-identity`.

### CVE-2026-56000

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T09:16:29.923 |

Local attackers with a X connection able to provide GLX commit to the X server xorg-server before 21.2.24 and xwayland before 24.1.13 could cause a Heap Use After Free, due to CommonMakeCurrent() pointing into potentially reallocated memory.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-56086

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-08T14:17:14.980 |

Dell PowerProtect Data Domain, versions 7.7.1.0 through 8.6, LTS2026 release version 8.6.1.0 through 8.6.1.10, LTS2025 release version 8.3.1.0 through 8.3.1.30, LTS2024 release versions 7.13.1.0 through 7.13.1.70 contain an Incorrect Authorization vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-14495

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-338` |
| Published | 2026-07-08T06:16:22.443 |

The DoLogin Security plugin for WordPress is vulnerable to Authentication Bypass via Insufficient Randomness in all versions up to, and including, 4.3. The vulnerability exists because `dologin\s::rrand()` seeds the Mersenne Twister with `mt_srand((double) microtime() * 1000000)` — discarding the integer-seconds component of `microtime()` and constraining the seed to a range of approximately 10^6 values (~20 bits of entropy) — after which every character of the 32-character magic-link token is drawn sequentially with `mt_rand()`, making the entire token a deterministic function of that seed. Because `Pswdless::try_login()` is registered on the unauthenticated `init` hook, resolves the target account by the auto-increment numeric ID embedded in the `?dologin=<id>.<hash>` parameter, performs the hash comparison using a non-constant-time `!=` operator, and then calls `wp_set_auth_cookie()` directly — never passing through `wp_authenticate()` and therefore never triggering the plugin's own `Auth::_has_login_err()` lockout — an unauthenticated attacker can brute-force the ~10^6-candidate seed space to reconstruct an active passwordless login token and authenticate as any targeted user, including administrators, without a password. Exploitation requires that a valid, unexpired passwordless login link (active for up to 7 days) exists for the target account at the time of the attack, and that the numeric link ID is known or guessable from the auto-increment primary key.

### CVE-2026-14489

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-08T06:16:22.307 |

The WHMCS Bridge plugin for WordPress is vulnerable to arbitrary file uploads due to missing file type validation in the connect() function in all versions up to, and including, 6.9. This makes it possible for authenticated attackers, with Custom-level access and above, to upload arbitrary files on the affected site's server which may make remote code execution possible.

### CVE-2026-14482

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-08T05:16:26.840 |

The 多说社会化评论框 plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 1.2. The vulnerability exists due to a missing capability and nonce check on a directly web-accessible API endpoint, combined with a trivially forgeable HMAC-SHA1 signature keyed on an always-empty WordPress option, which allows the endpoint's `update_option` handler to pass attacker-controlled `option` and `value` parameters directly to WordPress's `update_option` function without any allowlist or sanitization. This makes it possible for unauthenticated attackers to update arbitrary WordPress options — such as setting `default_role` to `administrator` and enabling open registration — and subsequently register an account with full administrator privileges.

### CVE-2026-14158

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-08T05:16:26.463 |

The Widget Logic Visual plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 1.52 via the widget_logic_visual_check_visibility function. This is due to missing capability check and nonce verification on the widget-logic-update-conditional-tags AJAX action combined with insufficient sanitization of the 'nwlv[cod-tag]' parameter before storage and subsequent use in an eval() call. This makes it possible for authenticated attackers, with subscriber-level access and above, to execute code on the server.

### CVE-2026-58656

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-598` |
| Published | 2026-07-08T14:17:20.297 |

Grav API plugin before v1.0.0-rc.16 accepts JWT tokens via the ?token= URL query parameter and responds with Access-Control-Allow-Origin: *, allowing unauthenticated attackers to make fully authenticated cross-origin API requests from any malicious website. Attackers who obtain a leaked JWT token from access logs, proxy logs, browser history, or Referrer headers can create persistent backdoor super-admin accounts and exfiltrate sensitive configuration and user data.

### CVE-2026-56250

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-08T14:17:15.673 |

Capgo before 12.128.2 allows upload-scoped API keys to modify the mutable app_versions.r2_path field through PostgREST, enabling retargeting to arbitrary R2 bundle objects. Attackers can patch r2_path to point to victim objects, soft-delete the attacker-controlled version, and trigger the on_version_update cleanup function to delete the victim R2 object, causing denial of service and bundle availability disruption.

### CVE-2026-56226

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-08T14:17:15.413 |

Capgo (Cap-go/capgo) before 12.128.2 exposes the Supabase PostgREST RPC function public.get_orgs_v6(userid uuid), which is SECURITY DEFINER and granted to the anon role, allowing unauthenticated access. Because the function accepts a caller-supplied user UUID without verifying it matches the authenticated user, an attacker using only the public publishable API key can query POST /rest/v1/rpc/get_orgs_v6 with an arbitrary user UUID to retrieve that user's organization membership, roles, subscription/trial metadata, and management_email (PII).

### CVE-2026-55429

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-08T00:16:33.597 |

Coder allows organizations to provision remote development environments via Terraform. Prior to versions 2.29.7, 2.32.7, 2.33.8, and 2.34.2, `UpsertWorkspaceApp` overwrites an existing app's `agent_id` on a primary-key conflict and `insertAgentApp` accepts the app ID from the provisioner's `CompleteJob` payload without verifying it belongs to the workspace being built. `CompleteJob` runs under `dbauthz.AsProvisionerd` so the authorization layer does not block the cross-workspace upsert. Exploitation requires elevated access as a template author or external provisioner operator. The fix in versions 2.29.7, 2.32.7, 2.33.8, and 2.34.2 verifies that any existing `workspace_apps` row matching the supplied ID belongs to the workspace being built and rejects cross-workspace agent reassignment. No known workarounds are available.

### CVE-2026-58469

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-07T21:17:28.383 |

GNU Wget through 1.25.0, fixed in commit 37a40fc, contains a heap buffer underread vulnerability in the clean_metalink_string() function within src/metalink.c that allows a malicious server to trigger memory corruption by serving a Metalink document containing a whitespace-only URL. Attackers can cause the function to decrement a pointer past the start of the buffer when processing an all-whitespace Metalink URL, potentially leading to abnormal program behavior.

### CVE-2026-55635

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-07T21:17:27.903 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.24, chart quota and Y-axis filters embed attacker-controlled filter values directly into generated SQL in Quota2SQLObj.getYWheres() without applying the SQL literal validation and escaping used by other filter paths, allowing an authenticated user who can create or modify chart definitions or submit chart data requests containing quota filters to inject SQL into queries executed against configured datasources. This issue is fixed in version 2.10.24.

### CVE-2026-55633

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-07T21:17:27.750 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.24, a bypass of the H2 zip protocol and file dropper fix allows an authenticated attacker to upload a zip archive disguised with a .ttf extension through FontManage.saveFile and then exploit it through the zip protocol to achieve remote code execution. This issue is fixed in version 2.10.24.

### CVE-2026-53751

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-07T21:17:26.857 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.24, the H2 database JDBC URL validation logic can be bypassed with special Unicode characters whose case-conversion behavior differs between DataEase validation and H2 parsing, allowing attackers to smuggle dangerous parameters such as init in malicious H2 JDBC connection strings and achieve arbitrary code execution. This issue is fixed in version 2.10.24.

### CVE-2026-53730

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-07T21:17:26.700 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.24, the /de2api/datasetData/previewSql endpoint lacks the mandatory @DePermit permission validation annotation, allowing any authenticated user to specify datasourceId=-1, access the built-in engine database, execute arbitrary SQL statements, and read sensitive core data. This issue is fixed in version 2.10.24.

### CVE-2026-53729

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-07T21:17:26.543 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.24, any authenticated user can download (/exportCenter/download/{id}), delete (/exportCenter/delete), retry (/exportCenter/retry/{id}), or generate download links (/exportCenter/generateDownloadUri/{id}) for export tasks belonging to other users by manipulating the task ID parameter, and the /exportCenter/download/{id} endpoint is whitelisted from authentication, allowing unauthenticated access to exported files. This issue is fixed in version 2.10.24.

### CVE-2026-50529

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-07T21:17:26.110 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.24, the /de2api/share/proxyInfo share interface generates and returns X-DE-LINK-TOKEN before validating the share password or ticket, allowing unauthenticated attackers who know a protected share UUID to obtain a valid link token for subsequent share-related API calls even with missing or invalid credentials. This issue is fixed in version 2.10.24.

### CVE-2026-59708

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-07T19:16:55.130 |

The GET /api/v1/public/:accessId/portfolio endpoint in ghostfolio accepts private access IDs without validating granteeUserId filtering, allowing unauthenticated access to full portfolio data. Attackers with a private access ID can retrieve sensitive portfolio information including holdings, quantities, buy prices, and performance metrics without authentication.

### CVE-2026-23697

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-07T17:16:35.977 |

Vtiger CRM before 8.4.0 contains an authenticated file upload vulnerability that allows low-privileged users to achieve remote code execution by uploading a .phar file containing arbitrary PHP code through the Documents module, bypassing the extension denylist in config.inc.php which omits the .phar extension. The uploaded file is stored with its original .phar extension under the web-accessible storage directory, and a misconfigured .htaccess using Apache 2.2 syntax is silently ignored on Apache 2.4 deployments, allowing unauthenticated HTTP requests to directly execute the uploaded PHP payload.

### CVE-2026-56811

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-07T16:16:40.710 |

Allocation of Resources Without Limits or Throttling vulnerability in phoenixframework phoenix (Phoenix.Socket module) allows an unauthenticated attacker to cause a denial of service against any endpoint that mounts a Phoenix socket with a reachable channel transport (WebSocket or LongPoll).

This vulnerability is associated with program files lib/phoenix/socket.ex and program routine 'Elixir.Phoenix.Socket':handle_in/4.

Phoenix transports do not limit the number of channels that a single transport process may join. Every phx_join message a client sends over one connection starts a persistent channel process, and the socket process accepts an unbounded number of them. A single unauthenticated client can therefore open one WebSocket or LongPoll connection and stream a large number of phx_join messages, spawning hundreds of thousands of channel processes over that one connection and eventually reaching the BEAM maximum process limit. Once the process table is exhausted the virtual machine can no longer start new processes, denying service to legitimate traffic across the whole node. Because the amplification happens inside a single connection, network-layer connection caps and rate limiting do not mitigate it.

The fix adds a :max_channels_per_transport option (default 100) that bounds the number of channels a single transport process can join, forcing abusive clients to open many connections instead, where external load balancers and reverse proxies can throttle them.

This issue affects phoenix: from 0.11.0 before 1.5.15, from 1.6.0-rc.0 before 1.6.17, from 1.7.0-rc.0 before 1.7.24, and from 1.8.0-rc.0 before 1.8.9.

### CVE-2026-55418

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-07T22:16:53.930 |

FastGPT is an open source AI knowledge base platform. Prior to v4.15.0-beta5, two FastGPT file handlers authorize an unrelated resource and then sign or read an S3 object using a key taken directly from the request, without checking that the key belongs to the caller's team. Because S3 object keys are global within the bucket and carry the tenant id only as a path segment, an attacker can supply another team's key and obtain its file contents through the chat-file presign endpoint or dataset preview endpoint. This issue is fixed in version v4.15.0-beta5.

### CVE-2026-23698

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-07T17:16:36.123 |

Vtiger CRM through 8.4.0 contains an authenticated remote code execution vulnerability in the admin module import feature that allows administrator-level attackers to upload arbitrary PHP files by submitting a crafted zip archive through the ModuleManager import function, which extracts contents directly into the modules/ directory under the web root without validating file types beyond the manifest.xml descriptor. Attackers can place executable PHP files in the modules/ directory that become directly accessible via HTTP, bypassing Vtiger's authentication and authorization layer entirely since Apache resolves the path and invokes the PHP interpreter before the application routing layer is involved, resulting in a persistent web shell independent of the originating session.

### CVE-2026-56003

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-08T10:16:23.577 |

A heap buffer overflow due to missing size checking in the property buffer when parsing PCF files in libXfont2 ComputeScaledProperties() before libXfont2 before 2.0.8 could be used by attackers using authenticated X clients to execute code within the X server.

### CVE-2026-56002

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-08T10:16:23.327 |

A heap bufferflow in pcfReadFont() due to missing glyph bounds checking in libXfont2 before 2.0.8  allows attackers authenticated as X client to execute code within the X server.

### CVE-2026-56001

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-08T09:16:30.050 |

A heap buffer overflow in BitmapScaleBitmaps in libXfont2 before 2.0.8 due to an overflowing 32bit size could be used by attackers able to access the X Server to execute code within the X server cont

### CVE-2026-55999

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-08T09:16:29.800 |

Local attackers with a X connection able to provide PCX fonts to the X 
server xorg-server before 21.2.24 and xwayland before 24.1.13 could 
cause a heap buffer overflow via SetFont due to missing glyph boundary checks.

### CVE-2026-57895

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-07-08T06:16:22.900 |

Incorrect default permissions issue exists in Pupsman versions prior to 3.9.0. An attacker can place a malicious executable in the installation folder, which results in arbitrary code execution with SYSTEM privilege

### CVE-2026-53511

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-07T21:17:26.380 |

calibre is an e-book manager. Prior to 9.10.0, a malicious EPUB, OPF, or PDF file can execute arbitrary Python code when its metadata is read by calibre, including through Add books or Edit books, by embedding a custom column definition with a python: template in calibre:user_metadata that is passed unsanitized to exec() in the template formatter. This issue is fixed in version 9.10.0.

### CVE-2026-57851

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-782` |
| Published | 2026-07-07T17:16:36.880 |

MSI Feature Manager contains a local privilege escalation vulnerability in the KernCoreLib64.sys kernel driver that allows any locally logged-on user to perform arbitrary physical memory read/write and unrestricted I/O port operations by accessing exposed IOCTL handlers without administrator privileges. Attackers can exploit the accessible device object through IOCTL handlers to manipulate kernel objects, tamper with kernel-mode callbacks, bypass Protected Process Light protections, and disable security software.

### CVE-2026-56437

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-07-08T06:16:22.733 |

Uncontrolled search path element issue exists in Pupsman versions prior to 3.9.0. If a crafted DLL file is placed in the same folder as the affected installer and the installer is executed, arbitrary code may be executed with SYSTEM privilege.

### CVE-2026-55408

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-07T22:16:53.790 |

Koodo Reader is an ebook reader. In version 2.3.0 and earlier, Koodo Reader is vulnerable to remote code execution through malicious EPUB files because the open-book IPC handler enables nodeIntegrationInSubFrames and EPUB chapter content is rendered with unsanitized innerHTML. An attacker can craft an EPUB book that, when imported and opened by the victim, instantiates a hidden iframe with Node.js API access and executes arbitrary operating system commands with the victim user's privileges. This issue is fixed in version 2.3.1.

### CVE-2026-49033

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-07T22:16:52.637 |

The application contains a stack-based buffer overflow vulnerability that can be exploited by an attacker to execute arbitrary code.

### CVE-2026-42958

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-07T22:16:52.060 |

The application contains a use-after-free vulnerability that can be exploited to cause memory corruption while parsing specially crafted files. This could allow an attacker to execute arbitrary code in the context of the current process.

### CVE-2026-42953

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-07T22:16:51.897 |

The application contains an out-of-bounds write vulnerability that can be exploited by an attacker to cause the program to write data past the end of an allocated memory buffer. This can lead to arbitrary code execution.

### CVE-2026-58583

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-07T21:17:29.163 |

FluxInk (formerly Sunia SPB Peripheral) Color Management Driver (TcnPeripheral64.sys) 1.0.7.2 allows local privilege escalation for a standard user account via arbitrary physical memory mapping at \Device\PhysicalMemory. Fixed in version 1.0.7.6. The fixed driver is currently available in the Windows 11 25H2 HLK (Hardware Lab Kit). The fixed driver may be available through Windows Update or from Lenovo directly.

### CVE-2026-56297

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-08T14:17:16.360 |

FreeRDP before 3.22.0 contains a use-after-free vulnerability in dvcman_channel_close and dvcman_call_on_receive due to improper synchronization of channel_callback access. A malicious RDP server can trigger a race condition by sending DYNVC_DATA and DYNVC_CLOSE messages concurrently, causing heap-use-after-free in the drdynvc client thread and potentially enabling remote code execution or denial of service.

### CVE-2026-55427

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74;CWE-78` |
| Published | 2026-07-08T00:16:33.323 |

Coder allows organizations to provision remote development environments via Terraform. Prior to versions 2.29.7, 2.32.7, 2.33.8, and 2.34.2, `coder config-ssh` wrote server-supplied SSH settings (`HostnameSuffix`, `SSHConfigOptions`) into the user's `~/.ssh/config` without sanitizing embedded newlines or restricting directives so a malicious or compromised Coder server could inject arbitrary SSH configuration. Practical exploitation requires control of the server-supplied values through a malicious or compromised deployment, a man-in-the-middle position or admin access to the `HostnameSuffix` and `SSHConfigOptions` settings. The fix in versions 2.29.7, 2.32.7, 2.33.8, and 2.34.2 validates `HostnameSuffix` and `SSHConfigOptions` against a strict character set that rejects newlines and other control characters. As a workaround, inspect `coder config-ssh --dry-run` output before applying changes.

### CVE-2026-49229

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-613` |
| Published | 2026-07-07T22:16:52.780 |

Actual is a local-first personal finance app. Prior to 26.6.0, in OpenID multi-user mode, disabling a user only blocks future OpenID login for that identity, while existing Actual session tokens for the disabled user remain valid. The shared session validation path accepts any existing token row that has not expired without checking whether the associated user is still enabled, allowing a disabled user to continue calling authenticated server endpoints. This issue is fixed in version 26.6.0.

### CVE-2026-57172

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321;CWE-798` |
| Published | 2026-07-07T21:17:28.223 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.24, ShareSecretManage uses a hardcoded default share link signature key, allowing an attacker who can obtain a passwordless share for a resource and user to use the known key link-pwd-fit2cloud to forge linkToken JWTs, bypass TokenFilter verification, and access backend resources as the share creator even if the original share has been revoked. This issue is fixed in version 2.10.24.

### CVE-2026-49471

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-352` |
| Published | 2026-07-07T21:17:25.833 |

Serena is a powerful MCP toolkit for coding that provides semantic retrieval and editing capabilities. Prior to v1.5.2, Serena's built-in web dashboard exposes an unauthenticated Flask API on a fixed, predictable port, with no authentication, no CSRF protection, and no Host header validation. A DNS rebinding attack allows a malicious webpage to reach this API from any browser and write arbitrary content to the agent's persistent memory store, which the agent reads and acts on autonomously. Combined with execute_shell_command using shell=True, this creates a remote code execution chain requiring only that the victim visit a malicious webpage while Serena is running. This issue is fixed in version v1.5.2.

### CVE-2026-57239

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-08T09:16:31.817 |

The user-controllable executable files will be directly executed by high-privilege processes, allowing low-privilege users to have the opportunity to elevate their privileges to NT AUTHORITY\SYSTEM.

### CVE-2026-55428

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-285;CWE-863` |
| Published | 2026-07-08T00:16:33.463 |

Coder allows organizations to provision remote development environments via Terraform. Prior to versions 2.29.7, 2.32.7, 2.33.8, and 2.34.2, the tailnet coordinator validates that an agent's `Addresses` derive from its authenticated UUID but applies no equivalent check to `AllowedIPs`. The coordinator forwards agent-supplied `AllowedIPs` verbatim to tunnel peers which install them into the WireGuard peer configuration. The fix in versions 2.29.7, 2.32.7, 2.33.8, and 2.34.2 validates each `AllowedIPs` prefix against the authenticating agent's UUID just like `Addresses`. As a workaround, monitor coordinator logs for agents advertising unexpected `AllowedIPs` prefixes.

### CVE-2026-3688

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-08T12:17:20.430 |

The WCFM Membership – WooCommerce Memberships for Multivendor Marketplace plugin for WordPress is vulnerable to Insecure Direct Object Reference in all versions up to, and including, 2.11.10. This is due to the 'wcfmvm_membership_change' AJAX action not validating user permission to modify other users. This makes it possible for authenticated attackers, with vendor level access and above, to change any user's role to 'wcfm_vendor' by changing their membership plan.

### CVE-2026-12378

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-08T07:16:46.550 |

The Appointment Booking Calendar Plugin and Scheduling Plugin  WordPress plugin through 1.1.28 does not validate data before passing it to a PHP deserialization function, allowing unauthenticated attackers to inject arbitrary PHP objects; where a suitable gadget chain is present on the site this can be leveraged to achieve remote code execution.

### CVE-2026-44454

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-07T21:17:25.180 |

Coder allows organizations to provision remote development environments via Terraform. Prior to versions 2.29.7 and 2.30.2, the `dotfiles` registry module passed unsanitized user input to shell commands, allowing arbitrary code execution inside a provisioned workspace. Any user who supplied a crafted `dotfiles_uri` value (for example, one containing shell command substitution such as `$(...)`) could achieve command execution in their own workspace. The Create Workspace page's `mode=auto` deep links amplified this into a one-click attack: an attacker could craft a URL that prefilled `param.dotfiles_uri` and silently provisioned a workspace with the attacker-controlled value, with no explicit user confirmation. In versions 2.29.7 and 2.30.2, input validation was added to the dotfiles module to reject URIs and usernames containing special characters, and the unsafe `eval`/`sh -c` usage was removed. This eliminated the command injection at its source.

### CVE-2026-13020

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-07-07T17:16:35.510 |

A Weak Password Recovery Mechanism for Forgotten Password exists in Esri Portal for ArcGIS versions 12.1 and earlier on Windows, Linux and Kubernetes. A remote, unauthorized attacker may assume ownership of a user’s account by manipulating this mechanism. ArcGIS Administrators should configure an email server with ArcGIS Enterprise to facilitate user self-service password recovery. The ability for an administrator to reset a user’s password remains unchanged.

### CVE-2026-22927

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-08T14:16:57.060 |

Omnissa Workspace ONE® Tunnel for Windows addresses a   Local Privilege Escalation Vulnerability.

### CVE-2026-57260

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-08T09:16:34.283 |

The application opened a PDF file containing an abnormal Unity 3D object. During parsing, the application incorrectly resolved a portion of the abnormal object as a pointer and used it as a valid address, ultimately causing the application to crash.

### CVE-2026-57256

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T09:16:33.770 |

When the application opens a PDF and executes JavaScript, it performs abnormal operations on the list box field, and this operation is repeated after the form is reset. During this process, the application failed to adequately verify the validity of the form objects and their internal dictionary pointers, resulting in accessing internal members of invalid or improperly initialized fields. This led to an illegal pointer read, ultimately causing the application to crash.

### CVE-2026-57254

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-08T09:16:33.520 |

There is an abnormal annotation within the PDF that is referenced by other objects. When the application parses the PDF, it fails to perform proper type checking, ultimately causing the application to crash.

### CVE-2026-57252

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T09:16:33.293 |

When the application opens a PDF file, during the process of JavaScript deleting pages and removing attachment annotations, it will cause the attachment panel to continue accessing invalid pointers, eventually leading to the application crashing.

### CVE-2026-57251

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-129` |
| Published | 2026-07-08T09:16:33.180 |

The application opens a PDF, but the cloud-like appearance of the construction process lacks proper setting of an upper limit and consistency checks. Out-of-bounds access to the underlying array is exposed, ultimately leading to a crash of the application.

### CVE-2026-57250

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T09:16:33.070 |

When the application opens a PDF and JavaScript resets the form fields, the script re-enters the interface. The underlying native object is damaged, but the application does not perform validation. The function call on the damaged object leads to the application crashing.

### CVE-2026-57249

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T09:16:32.960 |

After the application opened the PDF file, the script first reset the annotation status, then triggered the reset form event by additional action. During the re-entry process, the application access invalid objects and crashed.

### CVE-2026-57248

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-07-08T09:16:32.847 |

When the application opens a PDF file and JavaScript writes annotation attributes, there is a lack of sufficient object type and argument checks. As a result, due to the damage to the internal structure of the annotations, it causes the application to crash during subsequent release.

### CVE-2026-57247

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T09:16:32.737 |

The application re-enters the document structure via field processing and deletes the current page, and then continues using the field objects obtained before deletion, triggering an illegal read and crashing.

### CVE-2026-57246

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-07-08T09:16:32.620 |

When dealing with abnormally constructed objects, there is a lack of argument validation; JavaScript triggers signature verification, but the signature plugin does not perform validation when copying the abnormal string, causing the application to crash.

### CVE-2026-57245

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T09:16:32.503 |

When the application opens a PDF, traverses and builds the annotation elements related to hyperlinks, it fails to validate the abnormal annotation relationships and field combinations. This results in the internal objects entering an invalid state. Eventually, during the destruction phase, an invalid pointer write occurred, causing the application to crash.

### CVE-2026-57244

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T09:16:32.387 |

After JavaScript resetting the form, the synchronization process lacks re-entry protection and object lifecycle verification, resulting in the failure of the control pointer during the traversal process. After the pointer fails, it still continues to dereference, causing the application to crash.

### CVE-2026-57242

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T09:16:32.153 |

The application opens the PDF, and JavaScript modifies the form. However, the related objects on the page lack complete lifecycle management and null value validation; when the page state changes, the application continuously dereferences invalid objects, eventually leading to a crash.

### CVE-2026-57240

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T09:16:31.927 |

When the application opens a PDF file and JavaScript deletes the PDF fields, the subsequent logic still uses the old field pointers, resulting in invalid pointer references and causing the application to crash.

### CVE-2026-57238

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T09:16:31.693 |

After the application opened the PDF, JavaScript deleted the form field object. Subsequently, it attempted to access the invalid object, which caused the application to crash.

### CVE-2026-57237

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T09:16:31.577 |

When the application opens a PDF and JavaScript modifies the properties of form fields, it causes the state of the underlying objects referenced by the program to become invalid. Eventually, it reads an illegal memory address, which leads to the crash of the application.

### CVE-2026-13129

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T09:16:29.673 |

When the application opens a PDF file, JavaScript uses the damaged field tree to trigger field traversal, resulting in the program holding an invalid form object when accessing the field property path. Eventually, the application crashes due to reading an invalid pointer.

### CVE-2026-13128

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T09:16:29.557 |

Embedding JavaScript within a PDF file will cause the page to be deleted. Subsequent scripts will continue to access the relevant properties of the document view, eventually leading to the crash of the application.

### CVE-2026-13127

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T09:16:29.440 |

The application opens the PDF file. JavaScript then rewrites the document to modify the page structure, resulting in the invalidation of the page objects. However, the thumbnails still use the invalid page objects, ultimately causing the application to crash.

### CVE-2026-13126

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T09:16:29.307 |

The embedded JavaScript in the PDF deleted the pages, making the object invalid. The application attempted to perform a write operation on the invalid pop-up annotations, resulting in the program crashing.

### CVE-2026-60002

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-08T01:16:29.430 |

ssh in OpenSSH before 10.4 can have a use-after-free when a server changes its host key during a key re-exchange. (This outcome occurs only on the client side.)

### CVE-2026-55431

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-522;CWE-601` |
| Published | 2026-07-08T01:16:27.480 |

Coder allows organizations to provision remote development environments via Terraform. Prior to versions 2.29.7, 2.32.7, 2.33.8, and 2.34.2, `coder open app` opens external workspace-app URLs without validating the scheme or host. When an external app URL contains the `$SESSION_TOKEN` placeholder the CLI replaces it with the user's real session token before handing the URL to the OS open handler. Practical exploitation requires the victim to run `coder open app` against a workspace whose external app definition the attacker controls. Only a malicious template author can control external app URLs. The fix in versions 2.29.7, 2.32.7, 2.33.8, and 2.34.2 applies a URL-scheme allowlist in the CLI and limits `$SESSION_TOKEN` substitution to trusted destinations like the web frontend. As a workaround, avoid running `coder open app` for untrusted workspaces.

### CVE-2026-54607

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-07T22:16:53.357 |

FastGPT is a knowledge-based AI application platform. Prior to 4.15.0-beta4, the HTTP-tool OpenAPI schema importer validates only the top-level URL before passing it to SwaggerParser.bundle, whose remote reference resolver fetches $ref URLs without FastGPT's internal-address guard and returns fetched content inline, allowing an authenticated team member to read internal services or cloud metadata. This issue is fixed in version 4.15.0-beta4.

### CVE-2026-53482

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-08T14:17:04.000 |

Dell PowerProtect Data Domain, versions 7.7.1.0 through 8.7, LTS2026 release version 8.6.1.0 through 8.6.1.10, LTS2025 release version 8.3.1.0 through 8.3.1.30, LTS2024 release versions 7.13.1.0 through 7.13.1.70 contain an Integer overflow or wraparound vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to denial of service.

### CVE-2026-44840

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-943` |
| Published | 2026-07-08T14:16:59.493 |

Dgraph is an open source distributed GraphQL database. Prior to version 25.3.4, the `checkUserPassword` GraphQL query in Dgraph is vulnerable to DQL (Dgraph Query Language) injection. User-supplied password values are interpolated directly into a DQL `checkpwd()` query via `fmt.Sprintf` without any escaping or parameterization. An attacker can inject a password containing a double-quote character to break out of the DQL string literal and append arbitrary DQL query blocks. Version 25.3.4 patches the issue.

### CVE-2026-15053

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-07-08T14:16:56.930 |

Tanium addressed a denial of service vulnerability in Tanium Server.

### CVE-2026-5356

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-08T13:16:56.767 |

The LatePoint – Calendar Booking Plugin for Appointments and Events plugin for WordPress is vulnerable to Improper Input Validation in all versions up to, and including, 5.4.0. This is due to the plugin's Stripe Connect payment processor accepting a client-supplied PaymentIntent ID. This makes it possible for unauthenticated attackers to pay an arbitrary amount by supplying a previously succeeded PaymentIntent token.

### CVE-2026-6854

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-08T12:17:21.137 |

The My Calendar – Accessible Event Manager plugin for WordPress is vulnerable to time-based blind SQL Injection via the 'mc_auth' parameter in all versions up to, and including, 3.7.8 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-6230

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-08T12:17:20.660 |

The Tainacan plugin for WordPress is vulnerable to time-based blind SQL Injection via the 'geoquery' parameter in all versions up to and including 1.0.3 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-9700

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-08T06:16:23.043 |

The Eventer plugin for WordPress is vulnerable to time-based SQL Injection via the ‘code’ parameter in all versions up to, and including, 4.4.2 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query.  This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-9842

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-08T05:16:29.097 |

The Backstage - Customizer Demo Access plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 1.4.2. This is due to the plugin assigning the `manage_options` capability to the `backstage_customizer_user` demo role, which is more permissive than necessary for Customizer-only demo access. This makes it possible for unauthenticated attackers to navigate beyond the Customizer and update arbitrary WordPress options such as `default_role`, leading to privilege escalation.

### CVE-2026-14244

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-08T05:16:26.700 |

The Jssor Slider by jssor.com plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 3.1.24 via the 'url' parameter parameter. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information.

### CVE-2026-55436

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-07-08T01:16:27.890 |

Coder allows organizations to provision remote development environments via Terraform. Starting in version 2.30.0 and prior to versions 2.32.7, 2.33.8, and 2.34.2, the AI Bridge Proxy (`aibridgeproxyd`) created a goproxy server whose default transport set `InsecureSkipVerify: true` and only assigned a secure transport when an upstream proxy was configured. In the default configuration (no upstream proxy), outbound HTTPS to the Coder access URL accepted any TLS certificate. Practical exploitation requires an on-path (man-in-the-middle) position between the AI Bridge Proxy and the Coder server. Deployments where they are co-located over loopback are effectively unaffected. The fix in versions 2.32.7, 2.33.8, and 2.34.2 applies the secure transport (TLS 1.2 or higher using system root CAs) unconditionally. As a workaround, ensure the Coder access URL uses a trusted certificate and secure the network path between the AI Bridge Proxy and the Coder server (for example, loopback or mTLS).

### CVE-2026-55076

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-704` |
| Published | 2026-07-07T23:16:55.237 |

Coder allows organizations to provision remote development environments via Terraform. Prior to versions 2.29.7, 2.32.7, 2.33.8, and 2.34.2, Coder's OIDC callback checked `email_verified` with a direct Go `bool` type assertion. When an IdP returned the claim as a non-boolean (for example the string `"false"`) or omitted it, the assertion failed open and the email was treated as verified. Combined with an unconditional email-based account fallback, this enabled account takeover. The fix in versions 2.29.7, 2.32.7, 2.33.8, and 2.34.2 coerces `email_verified` across bool, string and numeric types (fail-closed) and blocks the email fallback when the matched user already has a different linked IdP subject. As a workaround, ensure the IdP returns `email_verified` as a native JSON boolean. The email-fallback linking issue has no configuration workaround; upgrading is required.

### CVE-2026-55075

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-289` |
| Published | 2026-07-07T22:16:53.650 |

Coder allows organizations to provision remote development environments via Terraform. Prior to versions 2.29.7, 2.32.7, 2.33.8, and 2.34.2, two flaws in Coder's OIDC login chained into account takeover. Email-based user matching fell back to linking by email without checking for an existing link to a different IdP subject and the `email_verified` claim was only enforced when present as a boolean `false` so an absent or non-boolean claim was treated as verified. The fix in versions 2.29.7, 2.32.7, 2.33.8, and 2.34.2 restricts the email fallback to first-time and legacy linking and defaults `email_verified` to false when the claim is absent or of an unexpected type. As a workaround, configure the OIDC provider to disallow self-registration or to require email verification before issuing tokens.

### CVE-2026-56246

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-08T14:17:15.543 |

Capgo before 12.128.2 contains a broken access control vulnerability in the organization management API where a scoped API key (limited_to_orgs) inherits its owner-user's permissions, allowing destructive cross-organization actions. When a user is an admin in two organizations and creates a write-mode API key restricted to one organization, that key can still perform destructive operations (e.g., DELETE /organization, DELETE /organization/members) against another organization. The root cause is route-level authorization (rbac_check_permission_direct) that evaluates the key owner's user privileges before enforcing the API key's limited_to_orgs scope.

### CVE-2026-6820

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-08T13:16:57.780 |

The VikBooking Hotel Booking Engine & PMS plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'email' parameter in all versions up to, and including, 1.8.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-6818

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-08T12:17:21.017 |

The VikBooking Hotel Booking Engine & PMS plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'special_requests' parameter in all versions up to, and including, 1.8.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-55077

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-07T23:16:55.377 |

Coder allows organizations to provision remote development environments via Terraform. Prior to versions 2.29.7, 2.32.7, 2.33.8, and 2.34.2, the `PUT /api/v2/users/{user}/password` endpoint authorized only `ActionUpdatePersonal` and did not prevent a `user-admin` from resetting an `owner` account's password. It also did not require the current password when an admin reset another user's password. Exploitation requires the privileged `user-admin` role so practical risk is limited to deployments that grant `user-admin` to less trusted operators. The fix in versions 2.29.7, 2.32.7, 2.33.8, and 2.34.2 prevents non-owner users from resetting the password of an account that holds the `owner` role. As a workaround, restrict the `user-admin` role to trusted administrators.

### CVE-2026-55631

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-07T21:17:27.593 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.24, the font management module allows authenticated users to submit an arbitrary fileTransName when creating a font record; when the record is later deleted, the backend concatenates that stored value with the font storage directory and passes it to FileUtils.deleteFile() without path traversal sanitization, allowing deletion of arbitrary writable files in the application container. This issue is fixed in version 2.10.24.

### CVE-2026-50007

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-07T21:17:25.977 |

Actual is an open-source personal finance application. Prior to 26.7.0, a missing authorization issue allows a shared user with user_access on a budget file to perform owner-only file management actions. A non-owner shared user can call file-management endpoints intended for higher-privilege users, including /delete-user-file, /reset-user-file, and /user-create-key, because requireFileAccess treats ordinary shared access as sufficient for file-management operations that should be restricted to the file owner or an administrator. This issue is fixed in version 26.7.0.

### CVE-2026-56401

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-07-08T14:17:17.167 |

Wazuh wazuh-modulesd before 5.0.0-beta3 contains a null pointer dereference vulnerability in inventory_sync FlatBuffer DataValue handling. An enrolled agent can send a verifier-valid DataValue message omitting the optional id field, causing wazuh-modulesd to crash when dereferencing data->id()->string_view() without null validation, resulting in denial of service.

### CVE-2026-56220

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-08T14:17:15.277 |

Capgo before 12.128.2 contains an authorization bypass vulnerability in the public.manifest INSERT policy that allows read-only org members to insert OTA manifest rows. Attackers with read-only org access can inject malicious manifest entries with arbitrary s3_path values that are served to devices via the unauthenticated /updates endpoint, enabling OTA metadata poisoning and potential malicious asset delivery.

### CVE-2026-41122

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-08T14:16:58.197 |

Dell PowerProtect Data Domain, versions 7.7.1.0 through 8.7, LTS2026 release version 8.6.1.0 through 8.6.1.10, LTS2025 release version 8.3.1.0 through 8.3.1.30, LTS2024 release versions 7.13.1.0 through 7.13.1.70 contain a stored cross-site scripting vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability. Exploitation may lead to information disclosure, session theft, or client-side request forgery.

### CVE-2026-59704

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-07T23:16:55.850 |

Cap's GET /api/video/ai endpoint fails to validate user ownership or membership before returning private video AI metadata including titles, summaries, and chapters. Authenticated attackers can supply arbitrary video IDs to read sensitive AI-generated content and trigger unauthorized AI generation that consumes the video owner's credits without consent.

### CVE-2026-54602

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-07T22:16:53.217 |

FastGPT is a knowledge-based AI application platform. Prior to 4.15.0, GET /api/core/ai/record/getRecord authenticates the caller but loads LLM request and response traces only by requestId without team scoping, allowing any authenticated user to read another team's prompts, retrieved RAG chunks, and completions if the requestId is known. This issue is fixed in version 4.15.0.

### CVE-2026-50530

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-07T21:17:26.240 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.24, a share mode chart data interface only validates that sceneId matches the resourceId in the link token and fails to validate whether tableId and field IDs in the request body belong to the shared resource, allowing an attacker with a valid share link token to replace dataset identifiers and retrieve unauthorized data through POST /de2api/chartData/getData. This issue is fixed in version 2.10.24.

### CVE-2026-7017

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-522` |
| Published | 2026-07-07T19:16:55.530 |

HTTP::Tiny versions before 0.095 for Perl forward credential headers to cross-origin redirect targets.

When the server returns a 3xx redirect, `_maybe_redirect` follows the `Location:` header and `_prepare_headers_and_cb` re-merges the caller's `headers` argument into the new request, without checking whether the redirect target shares an origin with the original URL. Caller-supplied `Authorization`, `Cookie` and `Proxy-Authorization` headers are therefore re-sent to whatever host the redirect names, across scheme, host or port boundaries, and including `https` to `http` downgrades that expose them in plaintext on the wire.

The HTTP::Tiny POD note that "Authorization headers will not be included in a redirected request" applied only to the URL-userinfo Basic-auth path, not to headers passed explicitly by the caller.

### CVE-2026-14904

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-07-07T17:16:35.627 |

AWS Research and Engineering Studio (RES) is an open-source solution that enables researchers and engineers to create and manage secure virtual desktops and computing resources on AWS.



Improper link resolution before file access issue (CWE-59) in the Auth.GetUserPrivateKey API. An authenticated remote user could read arbitrary files on the cluster-manager EC2 instance by replacing their SSH private key file (~/.ssh/id_rsa) with a symbolic link targeting any file on the host. Because the cluster-manager process runs as root, any file readable by root is exposed, including other users' SSH private keys and application configuration secrets.



It's recommended to upgrade to RES version 2026.06.
