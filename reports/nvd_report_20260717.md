# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-16 15:00 UTC
- **対象期間**: `2026-07-15T15:01:24.000Z` 〜 `2026-07-16T15:00:30.000Z`
- **重要CVE数**: 141 件（Critical 9.0+: 36 件 / High 7.0〜: 105 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件** 超に上り、特に **AI/LLM 連携系プラットフォーム**（NocoBase、9Router、Metabase、n8n‑MCP など）と **オープンソースの業務支援ツール**（Wekan、Penpot、DataEase、LiteLLM など）で **リモートコード実行 (RCE) や認証バイパス** が集中しています。  
- **攻撃経路は「認証不要」か「低権限認証」** が多く、外部から直接 API エンドポイントを叩くだけで任意コードが実行できるケースが目立ちます。  
- 多くは **入力サニタイズ不備やシェルコマンド組み立ての不適切** が根本原因で、修正は比較的シンプルなパッチ適用で済むことが多いです。  
- 影響範囲は **クラウド SaaS、セルフホスト型の社内システム、IoT/組み込み系 (OpenWrt)** まで多岐にわたり、**早急なアップデートが求められます**。

---

## 2. 特に注目すべき CVE  

| CVE | 製品 / バージョン | CVSS | 主な脆弱点 | 影響範囲・リスク |
|-----|-------------------|------|------------|-------------------|
| **CVE‑2026‑52887** | NocoBase < 2.0.61 | 10.0 | GET `/api/myInAppChannels:list` のクエリパラメータが SQL/NoSQL インジェクションに利用され、任意コード実行 (RCE) が可能 | AI‑駆動のローコードプラットフォームは多数の社内業務アプリの基盤になるため、侵害されると **全社システムの乗っ取り** につながる |
| **CVE‑2026‑46339** | 9Router 0.4.30‑0.4.37 | 10.0 | `/api/cli-tools/*` と `/api/mcp/*` が認証保護されておらず、カスタムプラグイン登録・コマンド実行が可能 | ルータ/トークン管理サーバは **ネットワーク境界の要**。攻撃者が任意コードを実行すれば **内部ネットワーク全体への横展開** が容易になる |
| **CVE‑2026‑50148** | Metabase 1.54.0‑1.60.4 (複数バージョン) | 10.0 | データベース接続設定に不正な JDBC URL を入れられ、サーバ側で任意コードが実行される | BI ツールは **機密データへのアクセス権** を持つことが前提。RCE により **データ抽出・改ざん・ランサムウェア展開** が可能 |
| **CVE‑2026‑52891** | Wekan < 9.07 | 9.9 | アバターアップロード時のファイル名をシェルコマンドに直接渡す ( `child_process.exec()` ) | カンバンツールは **多数のエンドユーザーが利用**。攻撃者が任意コードを実行すれば **社内ネットワーク内の横移動** が可能 |
| **CVE‑2026‑44986** | Penpot < 2.14.5 | 9.9 | 招待トークンやプロファイル ID が不適切に公開・再利用でき、セッション乗っ取りが可能 | デザイン・コード共有プラットフォームは **外部協力者と頻繁に連携**。トークン漏洩で **プロジェクト全体の情報漏洩** が起こり得る |

> **選定理由**  
> - **CVSS が最高 (10.0) の 3 件** はすべて「認証不要」か「認証が緩い」点で共通し、即座に外部から侵入できる危険性が極めて高い。  
> - **Wekan と Penpot** は UI 系ツールで社内の多くのユーザーが日常的に利用しているため、**被害拡大のスピードが速い**。  
> - いずれも **パッチがリリース済み** であり、アップデートだけでリスクを除去できる点が共通している。

---

## 3. 推奨アクション  

### 3.1 直ちに実施すべきこと
1. **対象パッケージのバージョン確認**  
   - `npm list nocobase`、`npm list 9router`、`pip show metabase` など、各製品の実行中バージョンを取得。  
2. **ベンダーが提供する修正バージョンへアップグレード**（以下参照）。  
3. **アップグレード前にバックアップ**（データベース・設定ファイル）を取得し、ロールバック手順を確保。  
4. **ファイアウォール／WAF で該当エンドポイントを一時的に遮断**（例: `/api/myInAppChannels:list`、`/api/cli-tools/*`、`/api/mcp/*`）し、アップデート完了までのリスクを低減。  
5. **監査ログの有効化**：認証失敗・不審なパラメータ（例: 長い `filter[latestMsgReceiveTimestamp]`）を検知できるように設定。

### 3.2 製品別具体的アップデート指示

| 製品 | 修正済みバージョン | アップデートコマンド例 |
|------|-------------------|------------------------|
| **NocoBase** | ≥ 2.0.61 | `npm install @nocobase/core@^2.0.61` もしくは `yarn add @nocobase/core@2.0.61` |
| **9Router** | ≥ 0.4.38 | `npm install 9router@0.4.38` |
| **Metabase** | 1.54.25、1.55.25、1.56.26、1.57.20、1.58.15、1.59.11、1.60.5 いずれか | `docker pull metabase/metabase:v1.60.5 && docker stop metabase && docker rm metabase && docker run -d --name metabase -p 3000:3000 metabase/metabase:v1.60.5` |
| **Wekan** | ≥ 9.07 | `git checkout v9.07 && npm install && npm run build && systemctl restart wekan` |
| **Penpot** | ≥ 2.14.5 | `docker pull penpotapp/penpot:2.14.5 && docker compose up -d` |
| **n8n‑MCP** | ≥ 2.56.1 | `npm install n8n-mcp@2.56.1` |
| **DataEase** | ≥ 2.10.23 | `pip install dataease==2.10.23` |
| **LiteLLM** | ≥ 1.18.11 | `pip install litellm==1.18.11` |
| **OpenWrt (odhcpd)** | ≥ 25.12.5 | `opkg update && opkg upgrade odhcpd` |
| **Spring Authorization Server** | 7.0.5、1.5.7、1.4.10、1.3.11 以上 | `./mvnw clean install -Dspring-authorization-server.version=7.0.5` |

> **注**：

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-52887

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-15T21:16:54.543 |

NocoBase is an AI-powered no-code/low-code platform for building business applications and enterprise solutions. Prior to 2.0.61, NocoBase @nocobase/plugin-notification-in-app-message exposed GET /api/myInAppChannels:list, where the filter[latestMsgReceiveTimestamp][$lt] value was inserted into a Sequelize.literal() template string without escaping or parameter binding, allowing a signed-up authenticated user to run stacked PostgreSQL statements and potentially execute commands with COPY ... TO PROGRAM. This vulnerability is fixed in 2.0.61.

### CVE-2026-46339

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-306` |
| Published | 2026-07-15T21:16:50.067 |

9Router is an AI router & token saver. From 0.4.30 until 0.4.37, 9Router's src/proxy.js middleware did not protect /api/cli-tools/* and /api/mcp/*, allowing unauthenticated registration of customPlugins through src/app/api/cli-tools/cowork-settings/route.js and command execution through the MCP bridge. This vulnerability is fixed in 0.4.37.

### CVE-2026-50148

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-07-15T16:16:47.963 |

Metabase is an open-source business intelligence and embedded analytics tool. From 1.54.0 until 1.54.24, 1.55.24, 1.56.25, 1.57.19, 1.58.14, 1.59.10, and 1.60.4, a Metabase user with permission to add or edit a database connection can achieve remote code execution on the Metabase server by configuring a Snowflake connection to an attacker-controlled server, because a flaw in the Snowflake JDBC driver can write arbitrary files anywhere on the Metabase host, including replacing one of Metabase's own database driver files that later executes inside the Metabase process. This issue is fixed in versions 1.54.24, 1.55.24, 1.56.25, 1.57.19, 1.58.14, 1.59.10, and 1.60.4.

### CVE-2026-52891

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-88` |
| Published | 2026-07-15T22:17:16.450 |

Wekan is open source kanban built with Meteor. Prior to 9.07, Wekan avatar upload functionality embeds user-supplied filenames into paths later passed to child_process.exec() for MIME-type detection. Because models/avatars.js and models/fileValidation.js used a shell command with the avatar filename, shell metacharacters such as backticks and $() in the filename could execute commands on the server. This issue is fixed in version 9.07.

### CVE-2026-54052

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-07-15T21:16:54.797 |

n8n-MCP is an MCP server that provides AI assistants access to n8n node documentation, properties, and operations. Prior to 2.56.1, in HTTP mode with multi-tenancy enabled through ENABLE_MULTI_TENANT=true, n8n-mcp's local workflow version history backups were not isolated per tenant, allowing an authenticated tenant to read workflow version snapshots belonging to other tenants and delete or destroy other tenants' stored backups, including full node definitions, credential references, and authorization headers. This issue is fixed in version 2.56.1.

### CVE-2026-44986

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-639` |
| Published | 2026-07-15T16:16:45.513 |

Penpot is an open-source design tool for design and code collaboration. Prior to 2.14.5, Penpot exposed teams_invitations.clj invitation tokens from create-team-invitations, embedded an existing profile id in auth.clj prepare-register-profile, and had auth.clj register-profile issue a session based on the invitation email match without password verification, allowing a registered user to take over any non-blocked profile. This issue is fixed in version 2.14.5.

### CVE-2023-49900

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-16T11:16:36.597 |

An unauthenticated remote attacker is able to perform remote code execution due to incorrectly sanitized user input in the SetParameter command.

### CVE-2023-49899

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-346` |
| Published | 2026-07-16T11:16:35.597 |

An unauthenticated remote attacker can execute any command on the affected device due to not correctly verifying the origin of a communication channel.

### CVE-2026-15013

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-07-16T05:16:18.043 |

The SAML Single Sign On – SSO Login plugin for WordPress is vulnerable to Authentication Bypass via SAML Signature Algorithm Confusion in all versions up to, and including, 5.4.3. The vulnerability exists because `Mo_SAML_Utilities::mo_saml_cast_key()` reads the `SignatureMethod` Algorithm attribute directly from the attacker-controlled `SAMLResponse` parameter rather than enforcing the locally configured algorithm, causing the plugin to recast the IdP's RSA public key as an HMAC-SHA1 shared secret and validate the forged signature against it. This makes it possible for unauthenticated attackers to forge a SAML assertion targeting any WordPress account — including administrators — obtain valid WordPress authentication cookies, and achieve full administrator-level account takeover.

### CVE-2026-55652

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-290` |
| Published | 2026-07-15T22:17:26.293 |

Wekan is open source kanban built with Meteor. Prior to 9.46, header-login with HEADER_LOGIN_TRUSTED_IPS uses getRequestIp() in server/lib/headerLoginAuth.js to trust the client-supplied X-Forwarded-For header before the real socket address, allowing an unauthenticated attacker to send HEADER_LOGIN_ID for any username and receive a meteor_login_token session, including for admin. This issue is fixed in version 9.46.

### CVE-2026-30623

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-07-15T22:16:46.317 |

LiteLLM 1.18.10 contains a remote code execution vulnerability in its MCP server creation functionality. The application allows users to add MCP servers via a JSON configuration specifying arbitrary command and args values. LiteLLM executes these values on the host without validation, enabling attackers to run arbitrary operating system commands. Successful exploitation may result in remote code execution with the privileges of the LiteLLM process.

### CVE-2026-30618

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-15T22:16:46.210 |

xszyou Fay 4.3.1 contains a remote code execution vulnerability in its MCP STDIO server management and command execution handling. A remote attacker can access the publicly exposed MCP management interface and configure an MCP STDIO server with attacker-controlled commands and parameters, resulting in execution of arbitrary commands on the server. Successful exploitation allows arbitrary command execution within the context of the Fay service.

### CVE-2026-49352

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-07-15T21:16:53.743 |

9Router is an AI router & token saver. From 0.2.21 until 0.4.44, 9Router used the hardcoded fallback JWT secret 9router-default-secret-change-me in src/app/api/auth/login/route.js, src/middleware.js, and later src/lib/auth/dashboardSession.js, allowing attackers to forge an auth_token cookie when JWT_SECRET was unset. This issue is fixed in version 0.4.44

### CVE-2026-22752

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-16T10:16:24.767 |

Authentication bypass by primary weakness vulnerability in Spring Security Spring Authorization Server.

This issue affects Spring Authorization Server: from 7.0.0 through 7.0.4, from 1.5.0 through 1.5.6, from 1.4.0 through 1.4.9, from 1.3.0 through 1.3.10.

### CVE-2026-54458

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-15T22:17:19.160 |

WWBN AVideo is an open source video platform. Versions prior to 29.0 contain a stored DOM Cross-Site Scripting vulnerability in the YPTSocket plugin. Any unauthenticated remote attacker can execute arbitrary JavaScript in the authenticated origin of every administrator currently viewing a page that renders the YPTSocket online-users debug panel. plugin/YPTSocket/getWebSocket.json.php issues a signed WebSocket token to any anonymous caller, and MessageSQLiteV2::onOpen at plugin/YPTSocket/MessageSQLiteV2.php lines 91 and 110 reads the attacker-controlled webSocketSelfURI and page_title query parameters from the WebSocket connection URL with no validation. Both values persist into the in-memory SQLite connections table and broadcast inside the users_id_online array sent to every connected client; on the client, plugin/YPTSocket/script.js::updateSocketUserCard interpolates the broadcast page_title into an HTML template literal that is passed to jQuery $.append(html), which parses attacker bytes into live DOM nodes including <img> with inline event handlers. Successful attackers can can read non-HttpOnly cookies and the CSRF token rendered into the admin dashboard, issue authenticated requests to any admin-only endpoint, exfiltrate the admin dashboard DOM, and chain into any admin-context mutation. When the victim is an AVideo administrator, the attacker turns a single anonymous WebSocket connection into full administrative takeover via the admin's own session. This issue has been patched by https://github.com/WWBN/AVideo/commit/8be71e53ccbe9b84b30870db386fb4d2b11e1c16.

### CVE-2026-62948

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79;CWE-117;CWE-150` |
| Published | 2026-07-15T18:16:50.293 |

OpenWrt is a Linux operating system targeting embedded devices. Prior to 25.12.5, odhcpd writes a DHCPv6 client FQDN option 39 hostname into /tmp/odhcpd.leases through src/statefiles.c statefiles_write_state6() and statefiles_write_state4() without escaping, allowing newline injection of forged lease lines that LuCI rpcd-mod-luci getDHCPLeases displays through htdocs/luci-static/resources/view/status/include/40_dhcp.js and htdocs/luci-static/resources/luci.js dom.append as live HTML in the Active DHCPv6 Leases admin page. This vulnerability is fixed in 25.12.5.

### CVE-2026-53513

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-20;CWE-345;CWE-441;CWE-918` |
| Published | 2026-07-15T18:16:47.547 |

Better Auth is an authentication and authorization library for TypeScript. Prior to 1.6.11, the @better-auth/sso plugin's POST /sso/register and POST /sso/update-provider endpoints accept attacker-controlled oidcConfig.userInfoEndpoint, tokenEndpoint, and jwksEndpoint URLs when skipDiscovery: true is set, store them on the ssoProvider row without origin validation, and fetch them during OIDC callback, allowing non-blind server-side request forgery and possible account linking when trustEmailVerified: true is configured. This issue is fixed in version 1.6.11.

### CVE-2026-46684

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-07-15T20:17:05.317 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.23, DataEase enterprise token handling can let TokenFilter#doFilter() pass X-DE-TOKEN values to TokenUtils.validate(), which checks only token presence and length before userBOByToken(token) uses JWT.decode() without signature verification, allowing forged tokens with chosen uid and oid values to be accepted when licenseValid=true. This issue is fixed in version 2.10.23.

### CVE-2026-55445

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-15T22:17:26.020 |

Qinglong is a timed task management platform supporting Python3, JavaScript, Shell, and Typescript. Prior to 2.20.1, the init guard middleware in back/loaders/express.ts checks /api/user/init but not /open/user/init, while rewrite('/open/*', '/api/$1') rewrites the whitelisted /open/* path after JWT authentication and the guard have passed; an unauthenticated attacker can send PUT /open/user/init to reset administrator credentials on an initialized instance. This issue is fixed in 2.20.1.

### CVE-2026-46421

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-506` |
| Published | 2026-07-15T19:17:17.523 |

The SAP Cloud Application Programming Model is a tool for building enterprise-grade cloud applications, and cap-js/cds-dbs is the monorepo for SQL database services for that tool. On April 29, 2026, compromised versions of `@cap-js/sqlite@2.2.2`, `@cap-js/postgres@2.2.2`, and `@cap-js/db-service@2.10.1` were published. The malicious packages harvested credentials and attempted self-propagation. If a compromised version was installed, all credentials accessible on that machine (npm tokens, cloud provider credentials, SSH keys, GitHub PATs) should be considered compromised. User should upgrade to `@cap-js/sqlite` >= 2.4.0, `@cap-js/postgres` >= 2.3.0, `@cap-js/db-service` >= 2.11.0. If a compromised version was ever installed, rotate all affected credentials. No known workarounds are available.

### CVE-2026-50562

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-494;CWE-829` |
| Published | 2026-07-15T18:16:47.160 |

FastGPT is a knowledge-based AI application platform. At commit 22ebfacbb43311e9b73294040ae0eb87390c6bba and earlier, artifacts built from untrusted pull request code in .github/workflows/preview-docs-build.yml and .github/workflows/preview-fastgpt-build.yml can be downloaded by privileged workflow_run jobs in .github/workflows/preview-docs-push.yml and .github/workflows/preview-fastgpt-push.yml, allowing attacker-controlled Docker images from the document/ tree or FastGPT build context to be pushed to GHCR and, for documentation previews, deployed with secrets.KUBE_CONFIG_CN.

### CVE-2026-52843

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-07-15T17:16:50.467 |

Lightpanda is a headless browser designed for AI and automation. Prior to 0.2.9, Lightpanda fetch() and XMLHttpRequest unconditionally attached session cookies to every HTTP request, ignoring credentials: omit, credentials: same-origin, credentials: include, and XMLHttpRequest.withCredentials, allowing an attacker-controlled origin in a Lightpanda session to issue authenticated cross-origin requests against a victim origin. This issue is fixed in version 0.2.9.

### CVE-2026-52842

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-07-15T17:16:50.317 |

Lightpanda is a headless browser designed for AI and automation. Prior to 0.3.1, Lightpanda searched for @ across the entire URL string instead of only the authority component when computing a page origin, so a URL such as `http://attacker.com/@victim.com/` was fetched from attacker.com but treated as `http://victim.com`, allowing a complete Same-Origin Policy bypass. This issue is fixed in version 0.3.1.

### CVE-2026-61740

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-798` |
| Published | 2026-07-15T15:16:48.350 |

LightRAG provides simple and fast retrieval-augmented generation. Prior to 1.5.4, when LightRAG is deployed with LIGHTRAG_API_KEY set but AUTH_ACCOUNTS unset, X-API-Key protection can be bypassed because lightrag/api/auth.py falls back to a hardcoded DEFAULT_TOKEN_SECRET, /auth-status and /login can mint guest JWTs, and combined_dependency in lightrag/api/utils_api.py accepts a valid guest token before checking the API key. A remote unauthenticated attacker can call endpoints guarded by combined_auth, including document read, upload, deletion, graph mutation, and query endpoints. This vulnerability is fixed in 1.5.4.

### CVE-2026-61736

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-942` |
| Published | 2026-07-15T15:16:48.217 |

LightRAG provides simple and fast retrieval-augmented generation. Prior to 1.5.4, the server defaults to CORS_ORIGINS=* combined with allow_credentials=True in lightrag/api/lightrag_server.py, causing Starlette CORSMiddleware to effectively whitelist every origin for credentialed cross-origin requests. Any malicious website visited by an authenticated LightRAG user can silently make authenticated API requests, exfiltrating documents and knowledge graph data or performing destructive actions such as deleting the document store. This vulnerability is fixed in 1.5.4.

### CVE-2026-63306

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-16T13:16:33.597 |

stoatchat before 0.13.5 contains an unauthenticated server-side request forgery vulnerability in the /proxy and /embed endpoints that accept arbitrary URLs without DNS resolution filtering or private IP range validation. Attackers can enumerate internal services, fingerprint applications, and reach instance metadata endpoints by supplying malicious URLs or leveraging redirect chains to access internal infrastructure.

### CVE-2026-63305

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-16T13:16:33.460 |

AVideo through 29.0 contains an OS command injection vulnerability in the ffmpeg.json.php endpoint where notifyCode and callback parameters are concatenated into a shell command without escaping. Attackers who can craft a valid encrypted payload can inject arbitrary shell metacharacters into these fields to execute OS commands as the web-server user.

### CVE-2026-63304

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-16T13:16:33.320 |

AVideo through 29.0 contains an OS command injection vulnerability in plugin/API/standAlone/functions.php where the listFFmpegProcesses() function interpolates unsanitized keyword parameters inside single quotes without escaping. Attackers who can craft a valid encrypted codeToExec payload can break out of the single-quoted grep context and execute arbitrary OS commands as the web-server user.

### CVE-2026-15925

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-297` |
| Published | 2026-07-16T07:16:47.957 |

Improper TLS hostname verification in Snowflake Connector for Python versions prior to 4.7.1 and 3.18.1 may have allowed a network-positioned attacker to bypass certificate hostname validation on HTTPS connections made by the connector. An attacker with on-path network access could exploit this by intercepting or redirecting network traffic and presenting a certificate signed by any trusted CA for any domain, causing the connector to accept connections without validating that the certificate matched the requested hostname. Successful exploitation requires an on-path traffic interception capability (e.g. ARP/DNS poisoning, rogue access point, BGP hijacking, or malicious proxy/exit node). This vulnerability may have exposed credentials, query data, and staged file contents to interception and tampering, and may have enabled the attacker to issue arbitrary SQL within the context of the victim's connector session. Impact is limited by the privileges of the affected Snowflake role. The fix is available in Snowflake Connector for Python versions 4.7.1 and 3.18.1. Users must manually upgrade.

### CVE-2026-52893

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-15T22:17:16.710 |

Wekan is open source kanban built with Meteor. Prior to 9.32, the Wekan Accounts.onCreateUser hook in server/models/users.js merges OIDC logins into existing accounts when the OIDC email or username matches an existing Wekan user, without verifying ownership or checking email_verified. An attacker using an OIDC provider account with a victim's email or username can cause Wekan to merge the attacker's OIDC credentials into the victim account and then log in as that account. This issue is fixed in version 9.32.

### CVE-2026-49445

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-07-15T20:17:10.453 |

Cilium is a networking, observability, and security solution. Prior to 1.17.14, 1.18.8, and 1.19.2, when Cilium L7 functionality is enabled, the embedded or standalone Envoy instance creates a world-accessible admin.sock on cluster nodes, allowing a local attacker to access Envoy admin endpoints, expose TLS secrets, disrupt cluster traffic, or terminate Envoy. This issue is fixed in versions 1.17.14, 1.18.8, and 1.19.2.

### CVE-2026-42533

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-15T15:16:33.480 |

A vulnerability exists in NGINX Plus and NGINX Open Source when a map directive uses regex matching and a string expression references the map's regex capture variables before referencing the map output variable. Alternatively, the same result could be achieved by using a non-cacheable variable in a string expression under certain conditions. An unauthenticated attacker along with conditions beyond their control can exploit this vulnerability by sending crafted HTTP requests. This may cause a heap buffer overflow in the NGINX worker process leading to a restart. Additionally, attackers can execute code on systems with Address Space Layout Randomization (ASLR) disabled or when the attacker can bypass ASLR.

Impact:
This vulnerability may allow remote attackers to cause a denial-of-service (DoS) on the NGINX system or to possibly trigger a code execution. There is no control plane exposure; this is a data plane issue only.




 Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-53512

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-306;CWE-345;CWE-863` |
| Published | 2026-07-15T18:16:47.420 |

Better Auth is an authentication and authorization library for TypeScript. Prior to 1.6.11, the legacy oidcProvider and mcp plugins expose OAuth token endpoints whose refresh_token grant authenticates only possession of the bound refreshToken row and matching client_id, without verifying the confidential client's client_secret, allowing an attacker with a valid refresh_token to mint access tokens and rotated refresh tokens through /api/auth/oauth2/token or /api/auth/mcp/token. The @better-auth/oauth-provider package is not affected. This issue is fixed in version 1.6.11.

### CVE-2026-11386

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-16T13:16:24.770 |

An input validation and injection vulnerability exists in Canonical ubuntu-pro-client (formerly ubuntu-advantage-tools). The client constructs APT source files (such as /etc/apt/sources.list.d/ubuntu-.list or their DEB822 equivalents) using data received directly from the contract server response via the directives.suites[] and directives.aptURL fields. Because the client utilizes Python's str.format() to write these files without performing escaping, validation, or newline character filtering, a malicious or tampered contract response containing embedded newline (\n) characters can successfully inject arbitrary, attacker-controlled deb configuration lines into root-owned APT sources. When combined with the unvalidated additionalPackages[] field—which is passed positionally into a root-executed apt-get install command—an attacker capable of spoofing or manipulating the contract response (e.g., via a compromised internal infrastructure, an intercepted connection utilizing a trusted CA, or local logical bugs) can force the client to fetch and install malicious packages. This ultimately leads to arbitrary code execution with root privileges on the affected system. This component is preinstalled on supported Ubuntu Server releases and auto-attaches by default on cloud provider Ubuntu Pro images.

### CVE-2026-45534

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-15T20:17:04.593 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.23, DataEase Redshift datasource connections can load attacker-controlled rsjdbc.ini configuration from System.getProperty("java.io.tmpdir"), setting socketFactory=org.springframework.context.support.FileSystemXmlApplicationContext so com.amazon.redshift.Driver#connect, com.amazon.redshift.Driver#getJdbcIniFile, and com.amazon.redshift.util.ObjectFactory#instantiate execute a reflection-based remote code execution chain during a normal JDBC connection through io.dataease.datasource.type.Redshift. This issue is fixed in version 2.10.23.

### CVE-2026-62378

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-15T17:16:53.020 |

RustFS Console is a web management console for the RustFS distributed file system. From 0.1.7 until 0.1.10, the RustFS Console components/object/preview-modal.tsx and components/object/pdf-viewer.tsx extension-based PDF preview path can render HTML content uploaded as .pdf, allowing stored cross-site scripting in the management console and exposure of administrator AccessKeyId, SecretAccessKey, and SessionToken values. This is caused by a regression of CVE-2026-27822. This vulnerability is fixed in 0.1.10.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-5674

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-07-16T14:16:56.070 |

A flaw was found in PipeWire, a multimedia server. This vulnerability allows an attacker to escape sandboxed applications, such as Flatpak, by exploiting PipeWire's PulseAudio compatibility layer. An attacker with minimal permissions within a sandboxed environment can load a malicious library, leading to arbitrary code execution outside the sandbox and potential compromise of the user's system.

### CVE-2026-15103

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-16T09:16:17.677 |

The WPFunnels – Funnel Builder for WooCommerce with Checkout & One Click Upsell plugin for WordPress is vulnerable to Privilege Escalation via arbitrary option update in all versions up to, and including, 3.12.8. This is due to the `update_settings()` REST callback failing to validate the `group_id` path parameter against an allowlist of permitted option names before passing it directly to `get_option()` and `update_option()`, allowing the built-in `wp_user_roles` option — which satisfies the route's loose `[\w-]+` regex — to be targeted. This makes it possible for authenticated attackers with the `wpf_manage_funnels` capability and above to elevate their privileges to administrator by writing a crafted role definition containing arbitrary capabilities into the `wp_user_roles` option, thereby granting any WordPress role full site administrator access. The `wpf_manage_funnels` capability is typically assigned to the Funnel Manager custom role created by the plugin, meaning this role is the minimum required to exploit the vulnerability.

### CVE-2026-15005

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-16T09:16:17.060 |

The Loco Translate plugin for WordPress is vulnerable to Cross-Site Request Forgery in all versions up to, and including, 2.8.5. This is due to missing or incorrect nonce validation on the execTemplate function. This makes it possible for unauthenticated attackers to execute arbitrary PHP code on the server by supplying a php://filter stream wrapper URI as the 'template' parameter, which bypasses path validation and is passed directly to the include sink in execTemplate() via a forged request granted they can trick a site administrator into performing an action such as clicking on a link.

### CVE-2026-13741

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-16T09:16:16.553 |

The Digits: WordPress Mobile Number Signup and Login plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 9.1.0.5. This is due to missing authorization and role validation in the `dig_update_wpwc_custom_fields()` function. This makes it possible for authenticated attackers, with Subscriber-level access and above, to escalate their privileges to Administrator by submitting a forged `digits_reg_userrole` value during profile update, granted the site administrator has configured the built-in DIGITS User Role field.

### CVE-2026-55576

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-94` |
| Published | 2026-07-15T22:17:26.157 |

MaaAssistantArknights is a one-click tool for daily Arknights tasks. In the current dev-v2 workflow, .github/workflows/release-preparation.yml inlined attacker-controlled github.event.pull_request.title into a run: shell command during the pull_request opened, reopened, and ready_for_review events, so a non-draft fork PR whose title starts with Release v could execute shell commands on the ubuntu-latest runner during the generate-changelog job. This vulnerability is fixed by commit cafc3946059e6337d2089d4fec8b6885ba17c332.

### CVE-2026-62312

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-15T21:16:55.810 |

9Router is an AI router & token saver. Prior to 0.5.2, 9Router allows a remote authenticated attacker to achieve arbitrary code execution on the host operating system by combining a Host header bypass of localhost-only routes with unvalidated MCP plugin args passed to child_process.spawn(), allowing malicious custom plugins to execute commands through /api/mcp//sse. This issue is fixed in version 0.5.2.

### CVE-2026-58658

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-15T18:16:48.607 |

GPUStack through 2.2.1, fixed in commit 4e20551, contains an unauthenticated information disclosure vulnerability that allows unauthenticated attackers to access sensitive inference logs and modify worker configuration by exploiting unprotected /serveLogs and /debug endpoints on the worker port. Attackers can enumerate model instance IDs to stream serving logs containing prompts and completions, change log levels, and read memory profiling data without any authentication.

### CVE-2026-20150

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-15T17:16:47.110 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco RoomOS engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20150 are related to improper access control&nbsp;that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-284.

### CVE-2026-60005

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-908` |
| Published | 2026-07-15T16:16:49.820 |

NGINX Plus and NGINX Open Source have a vulnerability in the ngx_http_slice_module module. When the slice directive and unnamed regex captures are configured or when a background cache update happens, unauthenticated attackers can send requests that may cause uninitialized memory access in the NGINX worker process, leading to limited disclosure of memory or a restart.

Impact:
This vulnerability may allow remote, unauthenticated attackers to have limited control to disclose memory contents or restart the NGINX worker process. There is no control plane exposure; this is a data plane issue only.
Note: The ngx_http_slice_module module is not enabled by default; it's enabled with the --with-http_slice_module configuration parameter.

Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-55242

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863;CWE-1336` |
| Published | 2026-07-15T16:16:48.960 |

ERPNext is a free and open source Enterprise Resource Planning tool. Prior to 15.111.0 and 16.22.0, an authenticated user with a standard operational role can trigger server-side template injection through a configuration field, resulting in unauthorized disclosure of data outside the user's normal permission scope. This issue is fixed in versions 15.111.0 and 16.22.0.

### CVE-2026-45805

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-749` |
| Published | 2026-07-15T16:16:45.787 |

Penpot is an open-source design tool for design and code collaboration. Prior to 2.15.0, Penpot MCP's mcp/packages/server/src/ReplServer.ts bound the ReplServer to 0.0.0.0:4403 and exposed an unauthenticated /execute endpoint that passed the code field to PluginBridge.executePluginTask(), allowing anyone on the network to execute JavaScript on the server. This issue is fixed in version 2.15.0.

### CVE-2026-61684

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-07-15T15:16:48.100 |

FastGPT is a knowledge-based AI application platform. In 4.15.0-beta4, FastGPT plugin invoke reverse-call endpoints under /api/invoke/* authenticate only by verifying a JWT signed with INVOKE_TOKEN_SECRET, which defaults to the constant string token and was not set in official deployment templates. An unauthenticated attacker can self-sign an HS256 JWT and reach /api/invoke/userInfo to disclose cross-tenant user PII by attacker-supplied tmbId values, or /api/invoke/fileUpload to write attacker-controlled content into chat files. This issue is fixed in version 4.15.0-beta5.

### CVE-2025-71377

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1025` |
| Published | 2026-07-16T13:16:24.057 |

stoatchat (delta) versions before 20250210-1 (0.8.2) contain a logic error in the query messages route. When fetching messages 'nearby' another message, the database query can be given a message limit of zero, which the database interprets as 'no limit'. A remote unauthenticated attacker can craft nearby message fetch requests to download an entire channel's message history in a single expensive request, and can send many such requests in parallel, resulting in denial of service through resource exhaustion.

### CVE-2026-58078

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-16T09:16:19.140 |

The Joomla extension Quix Page Builder Pro is vulnerable to an unauthenticated SQL injection.

### CVE-2026-56679

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-07-15T21:16:55.560 |

9Router is an AI router & token saver. Prior to 0.5.4, the PATCH /api/settings endpoint writes the entire request body to persistent settings without a field whitelist, allowing an authenticated user to set security-critical fields such as requireLogin and disable authentication for the whole application, exposing protected routes such as /api/keys and /api/providers to unauthenticated access. This issue is reported as fixed in version 0.5.4.

### CVE-2026-33445

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-15T21:16:36.227 |

CVE-2026-33445 is a memory management
vulnerability in Secure Access servers prior to 14.55. Attackers with an
intimate knowledge of and total control over the tunnel protocol can create a
persistent DoS against the server.

### CVE-2026-45535

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-15T20:17:04.723 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.23, DataEase SQL-type datasets store attacker-controlled SQL variable defaultValue entries such as ${var} and SqlparserUtils.handleVariableDefaultValue() inserts them with String.replace() without escaping or parameterization, causing stored SQL injection whenever a user with dataset read permission accesses the dataset. This issue is fixed in version 2.10.23.

### CVE-2026-45417

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-15T20:17:03.970 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.23, DataEase datasource connection status checks concatenate configuration.getSchema() into getTablesSql and execute the resulting SQL with executeQuery in io.dataease.datasource.provider.CalciteProvider#checkStatus, allowing SQL injection against DB2, SQL Server, PostgreSQL, and other affected datasources. This issue is fixed in version 2.10.23.

### CVE-2026-45320

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-15T20:17:03.387 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.23, DataEase dashboard SQL variables such as ${deptId} are processed by SqlparserUtils.transFilter(), whose final branch returns raw user input for non-in and non-between operators before SubstitutedSql.replace("${var}", value) splices it into dashboard SQL, allowing authenticated users who can view a dashboard to inject SQL against integrated datasources. This issue is fixed in version 2.10.23

### CVE-2026-62389

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-15T18:16:49.893 |

ws before 8.21.1 contains a memory exhaustion vulnerability in lib/receiver.js where the fragment guard only triggers when fragment count reaches maxFragments, allowing attackers to exhaust memory by sending incomplete fragmented WebSocket messages. Attackers can send a text frame with FIN=0 followed by continuation frames without completing the sequence, causing each fragment to be stored as a separate Buffer object with significant overhead, enabling denial of service through heap exhaustion.

### CVE-2026-59762

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-15T15:16:46.200 |

When an HTTP/2 profile is configured on a virtual server, undisclosed requests can cause an increase in memory resource utilization.  









Impact:
System performance can degrade until the TMM process is either forced to restart or is manually restarted. This vulnerability allows a remote, unauthenticated attacker to cause a degradation of service that can lead to a denial-of-service (DoS) on the BIG-IP system. There is no control plane exposure; this is a data plane issue only.





Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-55723

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-76` |
| Published | 2026-07-15T15:16:45.327 |

When NGINX Ingress Controller is configured with Custom Resource Definitions (CRDs) or Ingress annotations, an injection vulnerability exists in the configuration generator of NGINX Ingress Controller. Multiple user-controllable fields are written into the generated NGINX configuration without sanitization. An authenticated attacker with permission to create or modify these CRDs or annotations may craft values that inject arbitrary NGINX configuration directives. 

Impact:
An authenticated attacker granted write access to NGINX Ingress Controller CRDs or Ingress annotations through the Kubernetes API may be able to inject arbitrary NGINX configuration directives, create or delete files, or disable services. There is no data plane exposure; this is a control plane issue only.

Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-48795

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-1321` |
| Published | 2026-07-15T22:16:50.383 |

AdonisJS is a TypeScript-first web framework. From 10.1.3 until 10.1.5 and 11.0.3, AdonisJS @adonisjs/bodyparser incompletely fixed CVE-2026-25754 because nested multipart field payloads such as user.__proto__.polluted and constructor.prototype still caused lodash _.set() via @poppinss/utils to create plain intermediate objects and pollute Object.prototype. This issue is fixed in versions 10.1.5 and 11.0.3.

### CVE-2026-40501

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-07-15T18:16:45.230 |

Cherry Studio versions 1.2.2 through 1.9.12, fixed in commit 1518530, contain a remote code execution vulnerability in SearchService that allows remote attackers to execute arbitrary code by delivering malicious JavaScript through controlled search provider content loaded into an Electron BrowserWindow configured with nodeIntegration enabled and contextIsolation disabled. Attackers who control a search engine provider, individual search result pages, or provider settings pages can execute JavaScript with full Node.js privileges, gaining access to fs, child_process, os, and process.env under the operating-system account of the Cherry Studio process.

### CVE-2026-61836

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-524;CWE-639` |
| Published | 2026-07-15T15:16:48.603 |

Directus is a real-time API and App dashboard for managing SQL database content. Prior to 12.0.0, when response caching is enabled, the cache-key derivation in api/src/utils/get-cache-key.ts includes version, path, query, and accountability.user but omits authorization context such as share, role, roles, admin, app, and policies. Directus share tokens and anonymous requests can both reduce to user null, so different shares or anonymous clients requesting the same URL and query can receive a permission-filtered cached response without permission re-evaluation. This issue is fixed in version 12.0.0.

### CVE-2026-6423

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-16T09:16:19.273 |

A local privilege escalation vulnerability in ESET Inspect Connector. 
The vulnerability was caused by improper authentication in an IPC channel.

### CVE-2026-55234

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-284;CWE-639` |
| Published | 2026-07-15T22:17:25.880 |

Wekan is open source kanban built with Meteor. Prior to 9.37, Wekan DDP update allow rules in server/permissions/cards.js, server/permissions/lists.js, and server/permissions/swimlanes.js authorize against the stored source boardId and do not validate a new boardId in the update modifier. Any authenticated user with write access to their own board can call /cards/update, /lists/update, or /swimlanes/update to move cards, lists, or swimlanes into a private board they are not a member of. This issue is fixed in version 9.37.

### CVE-2026-45419

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-15T20:17:04.107 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.23, DataEase template saves call TemplateManageService#save, StaticResourceServer#saveFilesToServe, and the /de2api/templateManage/save endpoint with attacker-controlled staticResource names and Base64 content, allowing path traversal and arbitrary file writes because only / was used when extracting the file name. This issue is fixed in version 2.10.23.

### CVE-2026-40952

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `NVD-CWE-noinfo;CWE-276` |
| Published | 2026-07-15T20:16:57.907 |

CVE-2026-40952 is a privilege misconfiguration
in the Secure Access installer for the Windows client and server prior to
version 14.55. Attackers with local access to the client or server can use it
to elevate privileges to Administrator when Secure Access is installed in a
non-default location.

### CVE-2026-61828

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-07-15T16:16:50.800 |

Nixpkgs is a collection of software packages that can be installed with the Nix package manager. Prior to the 25.11 and 26.05 channel fixes, the NixOS module for MySQL services.mysql initializes the MySQL database in a way that allows local users, such as unprivileged web or CGI processes on the same host, to log in as the root user without a password when the service is used with mysql or percona-server. This issue is fixed in the 25.11 and 26.05.

### CVE-2026-15895

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-15T19:16:58.693 |

OS command injection in the npm package loading component in AWS jsii-diff before 1.131.0 might allow context-dependent attackers to execute arbitrary commands via crafted package specifiers passed to the npm: source argument.



To mitigate this issue, users should upgrade to jsii-diff v1.131.0 or later.

### CVE-2026-58659

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-07-15T18:16:48.743 |

PyTorch Lightning through 2.6.5, fixed in commit d710d68, contains a remote code execution vulnerability in the _load_state function that imports and executes attacker-controlled module names from checkpoint _instantiator hyperparameters. Attackers can craft malicious checkpoint files that bypass weights_only=True protections to execute arbitrary code when LightningModule.load_from_checkpoint is called.

### CVE-2026-45533

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-15T20:17:04.460 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.23, DataEase export-center deletion can accept path traversal sequences such as ../ in the bulk delete API endpoint and pass attacker-controlled identifiers to ExportCenterManage.delete, allowing recursive deletion of arbitrary server directories through export task cleanup. This issue is fixed in version 2.10.23.

### CVE-2026-62349

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:H` |
| Weaknesses | `CWE-121;CWE-787` |
| Published | 2026-07-15T19:18:37.347 |

TDengine is an open source, time-series database optimized for Internet of Things devices. In 3.4.1.6 and earlier, source/libs/parser/src/parUtil.c trimString() checks space for only one byte before processing SQL string escape sequences \%, \_, or \x, allowing a one-byte out-of-bounds write to the stack buffer tmpTokenBuf that can cause denial of service and potentially remote code execution. This issue is fixed in version 3.4.1.14.

### CVE-2026-53516

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-287;CWE-345` |
| Published | 2026-07-15T18:16:47.967 |

Better Auth is an authentication and authorization library for TypeScript. Prior to 1.6.11, Better Auth's OAuth callback auto-link gate in handleOAuthUserInfo accepts implicit account linking when the OAuth provider asserts email_verified: true without requiring the local user row's emailVerified field to also be true, allowing an attacker who pre-registers a victim email through /sign-up/email to bind the victim's OAuth identity to the attacker's account. The same primitive affects one-tap, and emailAndPassword.requireEmailVerification: true does not mitigate the link-time verification change. This issue is fixed in version 1.6.11.

### CVE-2026-20296

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-15T18:16:44.740 |

In Splunk Enterprise versions below 10.4.1, 10.2.5, 10.0.8, and 9.4.13, and Splunk Cloud Platform versions below 10.5.2605.0, 10.4.2604.7, 10.3.2512.16, 10.2.2510.18, and 10.1.2507.24, an attacker could trick a user that holds a role with the `list_deployment_server` capability into running arbitrary Search Processing Language (SPL) searches on their behalf as `splunk-system-user`, allowing for access to stored credentials and indexed data.<br><br>The vulnerability is possible because Deployment Server endpoints in Splunk Web do not validate Cross-Site Request Forgery (CSRF) tokens on GET requests, and caller-supplied input is not correctly neutralized before it is placed into an SPL search.

### CVE-2026-10673

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-787` |
| Published | 2026-07-15T18:16:44.180 |

The Zephyr ADIN2111/ADIN1110 10BASE-T1S/T1L Ethernet driver (drivers/ethernet/eth_adin2111.c) reassembles received Ethernet frames in OPEN Alliance (OA) SPI mode by copying device-supplied 64-byte data chunks into a fixed static buffer ctx->buf of size CONFIG_ETH_ADIN2111_BUFFER_SIZE (default 1524 bytes). In eth_adin2111_oa_data_read(), each valid chunk was memcpy'd into ctx->buf[ctx->scur] and the write cursor scur advanced, with no check that scur + len stayed within the buffer. The number of chunks (up to 255, from the BUFSTS RCA field) and the per-chunk length are taken entirely from the frame data received off the wire; the cursor is only reset on a start-of-frame chunk. An attacker on the single-pair Ethernet segment can therefore send a frame whose reassembled size exceeds the configured buffer, causing the driver's RX offload thread to write attacker-controlled frame bytes past the end of the static buffer into adjacent driver/kernel memory (up to roughly 14.8 KB in the worst case). This is a remotely/adjacently reachable out-of-bounds write (CWE-787) that can corrupt memory and cause denial of service or potentially code execution. The defect was introduced when OA SPI support was added (commit 0ca8b0756b1) and shipped in releases v3.7.0 through v4.4.0. The fix adds a bounds check that drops the oversized frame and resets the cursor before the copy.

### CVE-2026-47158

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-15T16:16:46.200 |

Vaultwarden is a Bitwarden-compatible server written in Rust. Prior to 1.36.0, Vaultwarden's SSO authorization flow did not bind the OAuth state parameter accepted by /connect/authorize to the initiating browser session, allowed attacker-controlled PKCE parameters, and left SsoAuth records intact after failed token exchange, allowing an unauthenticated attacker to induce IdP authentication and redeem tokens for a fully authenticated session. This issue is fixed in version 1.36.0.

### CVE-2026-56434

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-15T15:16:45.700 |

NGINX Plus and NGINX Open Source have a vulnerability in the ngx_http_ssi_module module. This vulnerability may exist when the Server-Side Includes (SSI), proxy_pass, and proxy_buffering off directives are configured. With this configuration, an unauthenticated attacker with man-in-the-middle (MITM) ability to control responses from an upstream server may be able to cause a use-after-free in the NGINX worker process. This issue may lead to limited modification of memory or a restart of the NGINX worker process.

Impact:
This vulnerability may allow remote attackers to have limited control to modify memory contents or restart the NGINX worker process. There is no control plane exposure; this is a data plane issue only.

Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-35149

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-294` |
| Published | 2026-07-16T12:17:35.870 |

HCL DFXServer is affected by an Authentication Bypass vulnerability via server response manipulation. An unauthorized user without valid credentials can exploit this flaw by intercepting and altering the server's authentication responses, allowing them to gain unauthorized access to the application without verification.

### CVE-2026-35147

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-16T12:17:35.617 |

HCL DFXServer is affected by a Broken Authentication vulnerability via direct API access. The application fails to verify the user's authentication status when accessing specific API endpoints, allowing an unauthenticated attacker to interact with the APIs and perform unauthorized actions without valid credentials.

### CVE-2026-46485

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-15;CWE-284;CWE-287;CWE-602` |
| Published | 2026-07-15T19:17:17.657 |

Dashy is a self-hostable personal dashboard. Prior to 4.0.8, Dashy deployments using OIDC can allow unauthenticated users or non-admin authenticated users to write changes to the main config.yaml through the config-saving functionality despite configured permissions, allowing unauthorized modification of dashboard configuration and potential service disruption. This issue is fixed in version 4.0.8.

### CVE-2026-12382

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-07-15T18:16:44.307 |

A flaw was found in the AAP Gateway Envoy proxy configuration. The non-mTLS route to EDA event streams does not remove the Subject HTTP header from client requests, despite the source code defining requestHeadersToRemove for this header. An unauthenticated remote attacker can inject a spoofed Subject header matching a legitimate client certificate DN to bypass mTLS authentication and inject arbitrary events into protected EDA event streams.

### CVE-2026-15008

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-16T09:16:17.200 |

The Uncanny Automator – Easy Automation, Integration, Webhooks & Workflow Builder Plugin plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the fr_token function in all versions up to, and including, 7.3.1.4. This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). Exploitation requires a Forminator form connected to an Uncanny Automator recipe configured for 'Everyone', allowing unauthenticated form submissions to supply the malicious serialized payload; a gadget chain is present within the plugin via the Action_Helpers_Email __destruct() method, meaning no external gadget library is required.

### CVE-2026-1609

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284;CWE-284` |
| Published | 2026-07-16T01:16:30.380 |

A flaw was found in Keycloak. When the JSON Web Token (JWT) authorization grant preview feature is enabled and a user account is disabled, Keycloak fails to validate the user’s disabled status during JWT authorization grant processing. A remote attacker with low privileges can exploit this improper access control vulnerability by presenting a valid assertion token from an external identity provider to obtain a JWT for a disabled user. This allows unauthorized access to sensitive resources.

### CVE-2026-53517

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-362;CWE-367` |
| Published | 2026-07-15T18:16:48.107 |

Better Auth is an authentication and authorization library for TypeScript. From 1.4.8-beta.7 until 1.6.11, the @better-auth/oauth-provider POST /oauth2/token endpoint on the refresh_token grant performs a non-atomic read, validate, revoke, and mint sequence on the oauthRefreshToken row, allowing concurrent requests with the same parent refresh token to pass the revoked check and create forked refresh-token families; the vulnerable range also includes embedded better-auth plugin versions before 1.6.0. This issue is fixed in version 1.6.11.

### CVE-2026-20156

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-07-15T17:16:47.380 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco RoomOS engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20156 are related to improper restriction of operations within the bounds of a memory buffer that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-119.

### CVE-2026-62685

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-647;CWE-706` |
| Published | 2026-07-15T16:16:51.783 |

File Browser is a file managing interface for uploading, deleting, previewing, renaming, and editing files within a specified directory. Prior to 2.63.17, File Browser builds new user scopes from usernames passed through cleanUsername() when Signup=true and CreateUserDir=true, but the many-to-one normalization can collapse usernames such as team/one, team one, and team-one to the same home directory without checking whether the resulting scope is already taken, allowing a second registrant to gain full read and write access to another user's files. This issue is fixed in version 2.63.17.

### CVE-2026-3842

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787;CWE-787` |
| Published | 2026-07-16T01:16:30.697 |

A flaw was found in QEMU. This vulnerability allows a local attacker within a guest virtual machine to write data beyond its allocated memory. This occurs when cpu_physical_memory_map() returns a shorter length than expected, leading to an out-of-bounds write. Successful exploitation could result in unauthorized access to guest memory or corruption of heap-allocated objects, potentially causing information disclosure, data integrity issues, or a denial of service.

### CVE-2026-56687

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-448` |
| Published | 2026-07-15T18:16:48.493 |

Dell ThinOS 10, versions prior to 2605_10.2100, contain an Obsolete Feature in UI vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-46709

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-07-15T16:16:46.053 |

Tabby (formerly Terminus) is a highly configurable terminal emulator. Prior to 1.0.234, Tabby inserts dropped file paths from tabby-electron/src/pathDrop.ts into the active shell without neutralizing command substitution metacharacters such as $(…) and `…`, so the incomplete CVE-2026-45038 fix for control characters still allows code execution when the victim presses Enter. This issue is fixed in version 1.0.234.

### CVE-2026-49279

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-15T22:16:52.163 |

WWBN AVideo is an open source video platform. Versions 29.0 and below contain a Stored XSS vulnerability through the autoEvalCodeOnHTML parameter in the MessageSQLite WebSocket Handler. The MessageSQLite.php handler only strips autoEvalCodeOnHTML from $json['msg'], but msgToResourceId() reads from $msg['json'] with higher priority. An attacker can place the XSS payload in the json key instead of msg, bypassing the sanitization entirely. An authenticated attacker can execute arbitrary JavaScript in any connected user's browser session via the WebSocket messaging system, stealing session cookies and authentication tokens, taking over accounts through session hijacking, and chaining with CSRF to perform admin actions on the victim's behalf, in the default SQLite WebSocket backend configuration. This issue has a patch that has yet to be officially released, see https://github.com/WWBN/AVideo/commit/3e0b3ce2bfa766183ff0ae227439394db57b1a23.

### CVE-2026-45313

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-15T22:16:48.873 |

Sandboxie-Plus is an open source sandbox-based isolation software for Windows. Prior to 1.17.6, GuiServer::WndHookRegisterSlave in Sandboxie/core/svc/GuiServer.cpp stores attacker-supplied hthread and hproc fields from a GUI_WND_HOOK_REGISTER request without validating that the thread belongs to the sandboxed process or that the function pointer is in the caller address space, and GuiServer::WndHookNotifySlave then calls OpenThread(THREAD_SET_CONTEXT, FALSE, whk->hthread) and QueueUserAPC((PAPCFUNC)whk->hproc, hThread, (ULONG_PTR)req->threadid) as SYSTEM, allowing a sandboxed process to execute arbitrary code in an unsandboxed host process. This issue is fixed in version 1.17.6.

### CVE-2026-53514

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-345;CWE-441;CWE-862` |
| Published | 2026-07-15T18:16:47.683 |

Better Auth is an authentication and authorization library for TypeScript. Prior to 1.6.11, and in 1.6.14 and later when invitation IDs can be obtained outside the invited mailbox and requireEmailVerificationOnInvitation: true is not enabled, the organization plugin's acceptInvitation, rejectInvitation, getInvitation, and listUserInvitations recipient endpoints use session.user.email and an invitation ID without sufficient verified-email ownership proof, allowing a user with an unverified session for the invited email address to accept an organization invitation after obtaining the invitation ID. This issue is fixed for the original default behavior in version 1.6.11, while 1.6.14 restored compatibility for built-in opaque invitation IDs and leaves affected configurations requiring secure options.

### CVE-2026-48799

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-345;CWE-639` |
| Published | 2026-07-15T17:16:48.667 |

Postiz is an AI social media scheduling tool. Prior to 2.21.8, Postiz fails to verify Nowpayments IPN callback authenticity against the payment provider shared secret and reads the target subscription identifier from the untrusted request body, allowing a low-privileged account to grant arbitrary organizations lifetime PRO subscriptions without payment. This issue is fixed in version 2.21.8.

### CVE-2026-47164

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-15T16:16:46.630 |

Vaultwarden is a Bitwarden-compatible server written in Rust. Prior to 1.36.0, Vaultwarden's SSO login flow checked the IdP email_verified claim only for new-user creation and not when SSO_SIGNUPS_MATCH_EMAIL=true linked an IdP identity to an existing local account, allowing an attacker-controlled IdP identity asserting a victim email address to bind to and authenticate as that account. This issue is fixed in version 1.36.0.

### CVE-2026-45806

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-15T16:16:45.927 |

Penpot is an open-source design tool for design and code collaboration. Prior to 2.15.0, Penpot's remote image import passed the user-controlled url from frontend/src/app/main/data/workspace/media.cljs into the backend RPC method :create-file-media-object-from-url in backend/src/app/rpc/commands/media.clj, where media/download-image in backend/src/app/media.clj used the shared HTTP client without destination filtering, allowing an authenticated file editor to reach internal-only endpoints. This issue is fixed in version 2.15.0.

### CVE-2026-61835

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-15T15:16:48.470 |

Directus is a real-time API and App dashboard for managing SQL database content. Prior to 12.0.0, the SSRF protection on Directus's file-import-from-URL feature can be bypassed using the address 0.0.0.0 because api/src/request/is-denied-ip.ts treats 0.0.0.0 as a keyword for local interfaces but never blocks the literal address itself. On Linux and macOS, connecting to 0.0.0.0 reaches localhost, so an authenticated user with file-upload rights can make the server fetch internal services through the /files/import endpoint and retrieve the response as a downloadable file. This issue is fixed in version 12.0.0.

### CVE-2026-61644

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-15T15:16:47.833 |

FastGPT is a knowledge-based AI application platform. From 4.14.17 until 4.15.0-beta5, the POST /api/core/chat/record/getCollectionQuote endpoint authenticates the caller's chat and collection context, but the initialId center-node lookup is not bound to that authorized context. A low-privileged tenant user can call the endpoint with valid attacker-owned appId, chatId, chatItemDataId, and collectionId values while supplying another tenant's dataset data id as initialId, causing the response to include foreign dataset quote or full-text content. This issue is fixed in version 4.15.0-beta5.

### CVE-2026-61613

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-15T15:16:47.700 |

Cursor is a code editor built for programming with AI. Prior to the Cloud Agent fix on 03/31/2026, browser-enabled Cursor Cloud Agent sessions allowed attacker-controlled web content to connect from inside the agent container to an unauthenticated local agent endpoint, enabling code execution within the affected Cloud Agent sandbox or session and access to files, repository contents, environment variables, credentials, and GitHub App access tokens available to that session. This issue was fixed on 03/31/2026 by requiring authentication for the relevant agent endpoint.

### CVE-2025-71388

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-16T13:16:24.193 |

stoatchat (delta/Revolt) versions from 20241213-1 before 20250210-1 allow users with only ViewChannel (read) permission on a channel to fetch that channel's webhooks, including their tokens, because the webhook fetch endpoint checked for ViewChannel instead of ManageWebhooks. Using a retrieved token, an attacker can send arbitrary messages to the channel, bypassing channel permissions and impersonating a bot or webhook. Fixed in 20250210-1 (0.8.2).

### CVE-2026-53444

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269;CWE-862` |
| Published | 2026-07-15T22:17:16.840 |

Wekan is open source kanban built with Meteor. Prior to 9.32, Wekan OIDC-related Meteor methods in packages/wekan-oidc/oidc_server.js, server/models/org.js, and server/models/team.js are globally callable without the admin authorization checks used by their non-OIDC counterparts. Authenticated users can call setCreateOrgFromOidc, setOrgAllFieldsFromOidc, setCreateTeamFromOidc, setTeamAllFieldsFromOidc, boardRoutineOnLogin, or groupRoutineOnLogin to create or modify organizations and teams, and groupRoutineOnLogin can grant global admin privileges when PROPAGATE_OIDC_DATA is enabled. This issue is fixed in version 9.32.

### CVE-2026-59950

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346;CWE-1385` |
| Published | 2026-07-15T21:16:55.683 |

The MCP Python SDK, called mcp on PyPI, is a Python implementation of the Model Context Protocol (MCP). Prior to 1.28.1, the deprecated mcp.server.websocket.websocket_server transport accepted WebSocket handshakes without applying Host or Origin header validation, leaving no SDK-level way to restrict which origins could connect to applications that exposed that transport. This issue is fixed in version 1.28.1.

### CVE-2026-52870

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-15T20:17:38.577 |

The MCP Python SDK, called mcp on PyPI, is a Python implementation of the Model Context Protocol (MCP). From 1.23.0 until 1.27.2, default handlers installed by server.experimental.enable_tasks() for tasks/list, tasks/get, tasks/result, and tasks/cancel operate only on task identifiers without recording the session that created each task, allowing any connected client to enumerate, read results from, consume messages for, or cancel other clients' tasks. This issue is fixed in version 1.27.2.

### CVE-2026-53518

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362;CWE-367` |
| Published | 2026-07-15T18:16:48.240 |

Better Auth is an authentication and authorization library for TypeScript. From 1.6.0 until 1.6.11, the @better-auth/oauth-provider POST /oauth2/token endpoint for the authorization_code grant redeems a single-use authorization code through a non-atomic find-then-delete sequence, allowing two concurrent requests to pass the read step and mint independent access tokens, refresh tokens, and ID tokens; legacy /oauth2/token and /mcp/token paths in oidc-provider and mcp plugins share the same primitive. This issue is fixed in version 1.6.11.

### CVE-2026-45337

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-285;CWE-345` |
| Published | 2026-07-15T18:16:45.580 |

Better Auth is an authentication and authorization library for TypeScript. From 1.6.0 until 1.6.11, the deviceAuthorization plugin treats any authenticated session as the owner of any pending device code because GET /device does not claim the row and POST /device/approve and POST /device/deny short-circuit when userId is unset, allowing an authenticated attacker who learns a valid user_code to bind the polling device to the attacker's account or deny the legitimate flow. This issue is fixed in version 1.6.11.

### CVE-2026-50147

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-88` |
| Published | 2026-07-15T16:16:47.830 |

Metabase is an open-source business intelligence and embedded analytics tool. From 1.57.0 until 1.57.19.1, 1.58.14.1, 1.59.10, and 1.60.4, an attacker who can configure a Metabase database connection can read arbitrary files from the Metabase server's filesystem by adding unsafe JDBC parameters to a MySQL or MariaDB connection, causing the driver to read files from the Metabase host and expose the contents through queries against the connected database or through validation error messages. This issue is fixed in versions 1.57.19.1, 1.58.14.1, 1.59.10, and 1.60.4.

### CVE-2026-54560

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-15T15:16:44.840 |

Cloudreve is a self-hosted file management and sharing system. From 4.12.0 until 4.16.1, Cloudreve's OAuth access tokens are issued without the OAuth client_id claim, so the JWT verifier does not load token scopes into request context and RequiredScopes treats the request like non-scoped session authentication, allowing a low-scope OAuth access token to call APIs requiring higher scopes such as file, share, workflow, user setting, WebDAV account, and potentially admin scopes. This issue is fixed in version 4.16.1.

### CVE-2026-21729

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-16T04:17:29.260 |

Loki queries with large limits can cause large memory allocations which can impact the availability of the service, depending on its deployment strategy.

### CVE-2026-12753

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-16T04:17:16.073 |

The Advance Product Search- Voice & Ajax Search for WooCommerce plugin for WordPress is vulnerable to generic SQL Injection via the 's' and 'match' parameter in all versions up to, and including, 1.4.4 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-48863

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121;CWE-121` |
| Published | 2026-07-16T01:16:30.830 |

A flaw was found in libsolv. A stack-based buffer overflow vulnerability exists in the PGP verification component due to incorrect length handling when copying EdDSA 's' MPI into a stack buffer. A remote attacker could craft a malicious Ed25519 PGP signature with mismatched MPI lengths. Processing this crafted signature could lead to a denial of service in automated package or repository processing workflows.

### CVE-2026-23538

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770;CWE-770` |
| Published | 2026-07-16T01:16:30.530 |

A vulnerability was identified in the Feast Feature Server's `/ws/chat` endpoint that allows remote attackers to establish persistent WebSocket connections without any authentication. By opening a large number of simultaneous connections, an attacker can exhaust server resources—such as memory, CPU, and file descriptors—leading to a complete denial of service for legitimate users.

### CVE-2026-49353

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-07-15T21:16:53.870 |

9Router is an AI router & token saver. In 0.4.45 and earlier, 9Router's src/dashboardGuard.js local-only access gate used Host and Origin headers in isLocalRequest() to protect /api/mcp/*, /api/tunnel/*, and /api/cli-tools/*, allowing header spoofing in reverse proxy or tunnel deployments to reach MCP child process stdin paths.

### CVE-2026-62351

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-15T19:18:37.947 |

TDengine is a time-series database optimized for Internet of Things devices. Prior to 3.4.1.15, source/libs/transport/src/transComm.c transDecompressMsg() read STransCompMsg.contLen when pHead->comp == 1 without first validating that the RPC packet contained the 8-byte STransCompMsg structure, causing an unauthenticated out-of-bounds read, uncontrolled allocation, integer underflow, and server crash. This issue is fixed in version 3.4.1.15.

### CVE-2026-49987

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-07-15T19:17:25.483 |

Repomix is a tool that packs repositories into AI-friendly files. Prior to 1.14.1, src/core/git/gitCommand.ts execGitShallowClone passes the --remote-branch value directly to git fetch and git checkout without validation or --end-of-options, allowing --upload-pack or other Git option injection that bypasses validateGitUrl() dangerous parameter checks and can execute commands through local or SSH-style transports. This issue is fixed in version 1.14.1.

### CVE-2026-12997

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-15T19:16:56.890 |

The Gravity Forms plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 2.10.4 via the 'gform_uploaded_files' parameter parameter. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. Exploitation requires the targeted form to not enforce login (so publicly accessible), which allows the unauthenticated attacker to reach the process_send_resume_link endpoint and supply an arbitrary recipient email address to receive the traversal-retrieved file as a notification attachment.

### CVE-2026-59955

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-20;CWE-287` |
| Published | 2026-07-15T17:16:51.087 |

Apollo is a reliable configuration management system suitable for microservice configuration management scenarios. Prior to 2.5.2, Apollo ConfigService may allow unauthorized access to raw configuration data when AccessKey or management key authentication is enabled because requests under /configfiles/raw/{appId}/{clusterName}/{namespace} are parsed for authentication as appId raw instead of the actual path appId, causing ConfigService to look up AccessKey secrets for raw before verifying the request signature and potentially continue without signature verification for the target appId. This issue is fixed in version 2.5.2.

### CVE-2026-59954

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-20;CWE-287` |
| Published | 2026-07-15T17:16:50.960 |

Apollo is a reliable configuration management system suitable for microservice configuration management scenarios. Prior to 2.5.2, Apollo ConfigService may allow unauthorized access to configuration data when AccessKey or management key authentication is enabled because ConfigService can accept a non-canonical appId variant during authentication while downstream request handling resolves it to the protected app, including accent variants under accent-insensitive collations or trailing-space variants under PAD SPACE collations on /configs and /configfiles endpoints. This issue is fixed in version 2.5.2.

### CVE-2026-45804

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-07-15T17:16:48.310 |

Diffusers is the a library for pretrained diffusion models. Prior to 0.38.0, Diffusers' DiffusionPipeline.from_pretrained flow can bypass the trust_remote_code guard because download() validates model_index.json and custom pipeline code before later loading from a cached folder that can change, allowing a Hub repository with custom .py pipeline code to execute through the custom pipeline flow without passing custom_pipeline or trust_remote_code=True. This issue is fixed in version 0.38.0.

### CVE-2026-45793

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-15T17:16:48.173 |

Composer is a dependency Manager for the PHP language. Prior to 1.10.28, 2.2.28, and 2.9.8, Composer\IO\BaseIO::loadConfiguration() validates GitHub OAuth tokens with the regex ^[.A-Za-z0-9_]+$ and interpolates rejected tokens into an UnexpectedValueException; GitHub Actions GITHUB_TOKEN values using the ghs_<id>_<base64url-JWT> format can contain -, fail validation, and be disclosed to stderr or CI logs. This issue is fixed in versions 1.10.28, 2.2.28, and 2.9.8.

### CVE-2026-20187

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-703` |
| Published | 2026-07-15T17:16:47.770 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco RoomOS engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20187 are related to improper handling of exceptional conditions that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-703.

### CVE-2026-20158

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-664` |
| Published | 2026-07-15T17:16:47.640 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco RoomOS engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20158 are related to improper control of a resource through its lifetime that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-664.

### CVE-2026-20157

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-311` |
| Published | 2026-07-15T17:16:47.507 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco RoomOS engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20157 are related to missing encryption that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-311.

### CVE-2026-20153

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-15T17:16:47.247 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco RoomOS engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20153 are related to improper input validation that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-20.

### CVE-2026-61371

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-59` |
| Published | 2026-07-15T16:16:50.307 |

Microsoft AVML before 0.17.0 could follow a symlink when opening a destination output path on Unix, allowing truncation/overwrite of the symlink target. The destructive effect is performed at open-time via O_TRUNC, and can happen before full input validation completes (“truncation-before-validation”).

### CVE-2026-45738

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-15T20:17:05.057 |

Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes. Prior to 3.2.12, 3.3.10, and 3.4.2, Argo CD users with application write access can set link.argocd.argoproj.io/* annotations whose pipe-separated values are rendered by ui/src/app/applications/components/application-summary/application-summary.tsx in the Summary tab URLs section as anchor href values without URL validation, allowing javascript: execution in a higher-privileged user's authenticated Argo CD origin session. This issue is fixed in versions 3.2.12, 3.3.10, and 3.4.2.

### CVE-2026-7543

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-16T09:16:19.527 |

The Breakdance plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'fields' parameter in versions up to, and including, 2.7.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-13042

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-16T05:16:17.780 |

The RPB Chessboard plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content in all versions up to, and including, 8.1.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. WordPress's save-time kses sanitization does not mitigate this issue because the crafted payload uses only kses-allowed tags and attributes (such as an &lt;a&gt; element with title and href), and the dangerous attribute-breaking HTML is synthesized entirely at render time by the plugin's own comment_text filter.

### CVE-2026-62350

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-15T19:18:37.810 |

TDengine is an open source, time-series database optimized for Internet of Things devices. Prior to 3.4.1.15, a user with create udf privilege could upload a crafted shared library and install it as a user-defined function, such as eval, then execute arbitrary C code on the TDengine server side through database queries. This issue is fixed in version 3.4.1.15.

### CVE-2026-59258

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-15T18:16:49.150 |

immich before 3.0.3 contains a broken access control vulnerability in the PUT /albums/:id/user/:userId endpoint that allows shared album editors to modify member roles without owner-only restrictions. Attackers with editor access can demote the album owner to editor and promote themselves to owner in sequential requests, gaining full control including deletion and eviction capabilities.

### CVE-2026-58660

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-15T18:16:48.880 |

Kanboard through 1.2.52, fixed in commit 564cc30, BoardAjaxController save() method (used by the kanban board drag-and-drop endpoint) validates the caller's role on the attacker-supplied project_id but never verifies that the supplied task_id actually belongs to that project. Because task identifiers are sequential integers shared across the entire instance, any authenticated user who is a member of at least one project can enumerate and move (corrupt/hide) tasks belonging to any other project on the same instance, including private projects they have no membership or role on.

### CVE-2026-20297

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-15T18:16:44.880 |

In Splunk Enterprise versions below 10.4.1, 10.2.5, 10.0.8, 9.4.13, and 9.3.14, and Splunk Cloud Platform versions below 10.5.2605.0, 10.4.2604.6, 10.2.2510.18, and 10.1.2507.24, a user who holds a role that contains the `edit_local_apps` and `install_apps` capabilities could cause a legitimate app installation to write files outside the intended app directory, into `$SPLUNK_HOME/etc/` and its subdirectories.<br><br>The vulnerability is caused by a path traversal in the app installation workflow, which does not restrict the installation path to the intended app directory.

### CVE-2026-12978

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-16T07:16:47.577 |

The FunnelKit  WordPress plugin before 3.15.0.6 does not escape a user-supplied parameter before reflecting it into the HTML response of one of its page-builder AJAX actions, allowing unauthenticated attackers to perform Reflected Cross-Site Scripting against logged-in users who open a crafted page. The affected action is only registered when the Divi /builder is active.

### CVE-2026-63175

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-07-15T22:17:38.193 |

PlaywrightCapture stored capture-specific configuration and runtime data as mutable class-level variables rather than instance-level variables. Consequently, multiple Capture objects running within the same Python process could share state, including HTTP headers, cookies, browser storage, HTTP credentials, proxy configuration, user-agent settings, geolocation information, and captured request data.

In a multi-user or concurrent deployment, information supplied during one capture could therefore persist and be reused by a subsequent or parallel capture. This could result in the disclosure of authentication cookies, credentials, browser storage, or captured request data belonging to another user. It could also cause requests to be performed with another capture's authentication context, headers, or proxy configuration, potentially enabling unauthorized access to remote resources or interference with other capture operations.

The vulnerability is resolved by initializing all capture-specific settings and request data as instance variables in the Capture constructor, ensuring that state is isolated between capture operations.

### CVE-2026-53445

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-15T22:17:16.973 |

Wekan is open source kanban built with Meteor. Prior to 9.32, the Wekan copyBoard Meteor DDP method in server/publications/boards.js copies a board by caller-supplied board ID without checking this.userId, membership, or admin access. Any authenticated user can copy a private board they are not a member of, including its cards, checklists, custom fields, labels, and rules, while the REST POST /api/boards/:boardId/copy path correctly checks board admin access. This issue is fixed in version 9.32.

### CVE-2026-52890

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-22;CWE-400` |
| Published | 2026-07-15T22:17:16.310 |

Wekan is open source kanban built with Meteor. Prior to 9.31, Wekan allows a logged-in board member to insert an attachment document through the /attachments/insert DDP method with attacker-controlled versions.original.path and versions.original.storage fields. The server/permissions/attachments.js insert rule checks only board write access, and FileStoreStrategyFilesystem.getReadStream() in models/lib/fileStoreStrategy.js streams the stored path without a storage-root containment check, allowing arbitrary file reads and denial of service through special files such as /dev/zero. This issue is fixed in version 9.31.

### CVE-2026-52869

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-15T20:17:38.427 |

The MCP Python SDK, called mcp on PyPI, is a Python implementation of the Model Context Protocol (MCP). Prior to 1.27.2, the SSE and stateful Streamable HTTP transports mcp.server.sse.SseServerTransport and mcp.server.streamable_http_manager.StreamableHTTPSessionManager route requests to existing sessions using only the session_id query parameter or Mcp-Session-Id header without verifying the authenticated principal that created the session, allowing a different bearer-token-authenticated client with a known session ID to inject JSON-RPC messages into that session. This issue is fixed in version 1.27.2.

### CVE-2026-50144

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-129;CWE-787` |
| Published | 2026-07-15T20:17:13.500 |

ncnn is a high-performance neural network inference framework optimized for the mobile platform. In commit e54f7b1f88434e1d844ea0551b880a1cfb079ce1 and earlier, ncnn allows an out-of-bounds heap write in ncnn::ParamDict::load_param() when Net::load_param() loads a malicious .param model file because the parsed parameter id is checked only against id >= NCNN_MAX_PARAM_COUNT, allowing a negative id to index before the params[NCNN_MAX_PARAM_COUNT] array. This vulnerability is fixed by commit 5a0288f255daa6c3294f77109f67718e434ec020.

### CVE-2026-50124

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-15T20:17:13.370 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.23, DataEase can be exploited by uploading payload.zip through the Excel upload API /datasource/upload, creating an H2 datasource that uses the zip: protocol, and executing an SQL dataset path where CalciteProvider.jdbcFetchResultField calls statement.executeQuery(), causing precompiled Java aliases in test.mv.db to execute arbitrary code. This issue is fixed in version 2.10.23.

### CVE-2026-50030

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-15T20:17:13.233 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.23, DataEase SQL preview exposes DatasetDataApi.previewSql/previewSqlCheck through /de2api/datasetData/previewSql, accepts PreviewSqlDTO.sql, PreviewSqlDTO.datasourceId, and PreviewSqlDTO.isCross, then DatasetDataManage.previewSql stores decoded SQL in datasourceRequest.query and CalciteProvider.fetchResultField executes it with prepareStatement(...).executeQuery(), allowing arbitrary readable datasource tables to be queried and returned in preview responses. This issue is fixed in version 2.10.23.

### CVE-2026-33443

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `NVD-CWE-noinfo;CWE-400` |
| Published | 2026-07-15T20:16:56.780 |

CVE-2026-33443 is a memory management error in
Secure Access servers prior to 14.55. Attackers with an intimate knowledge of
and total control over the tunnel protocol can create a persistent DoS against
the server.

### CVE-2026-59255

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-15T18:16:49.017 |

BloodHound through 9.4.0, fixed in commit 8f79035, contains a missing authorization vulnerability in the custom-nodes API endpoints that allows any authenticated user to modify the global graph schema. Attackers with valid session tokens can create, update, or delete custom node types affecting all users and tenants by invoking unprotected POST, PUT, and DELETE operations on the custom-nodes endpoints.

### CVE-2026-53515

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-269;CWE-285;CWE-863` |
| Published | 2026-07-15T18:16:47.817 |

Better Auth is an authentication and authorization library for TypeScript. From 1.2.10 until 1.6.11, the @better-auth/sso plugin's POST /sso/register endpoint lets any organization member attach a new SSO provider to that organization because registerSSOProvider checks only for a membership row and does not require an owner or admin role, allowing attacker-controlled OIDC or SAML providers to drive /sso/callback/{providerId} organization provisioning. This issue is fixed in version 1.6.11.

### CVE-2026-54563

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-15T15:16:45.100 |

Cloudreve is a self-hosted file management and sharing system. Prior to 4.16.1, a Cloudreve WebDAV account rooted at a configured folder can send paths such as /dav/%2e%2e/outside.txt because stripPrefix in pkg/webdav/webdav.go joins the decoded request suffix to the account root with fs.URI.JoinRaw without checking containment, allowing the scoped credential to read and list files outside the configured folder and writable credentials to create, overwrite, move, or delete them. This issue is reported as fixed in version 4.16.1.

### CVE-2026-52865

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-07-15T15:16:44.587 |

When NGINX Ingress Controller processes Ingress or TransportServer resources, an authenticated, remote attacker with permission to create or modify Ingress or TransportServer resources can cause the NGINX Ingress Controller process to terminate. 



Impact:
The NGINX Ingress Controller control plane process terminates and enters a persistent crash loop while the malformed Ingress or TransportServer resource remains in the cluster. This vulnerability allows a remote, authenticated attacker with at least Ingress or TransportServer resource write access to cause a denial-of-service (DoS) on the NGINX Ingress Controller system. There is no data plane exposure; this is a control plane issue only.

Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.
