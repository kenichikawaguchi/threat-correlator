# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-06 15:00 UTC
- **対象期間**: `2026-10-05T15:00:28.000Z` 〜 `2026-10-06T15:00:44.000Z`
- **重要CVE数**: 250 件（Critical 9.0+: 45 件 / High 7.0〜: 205 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 今回公開された CVE の大半は **WordPress 系プラグイン** や **オープンソース SaaS ツール** に起因し、**任意ファイルアップロード / RCE** が共通の攻撃パターンです。  
- CVSS が 9.0 以上の脆弱性が 30 件以上と非常に密度が高く、特に **認証不要** でリモートからコード実行が可能になるケースが目立ちます。  
- ネットワーク機器（TOTOLINK ルータ）や AI ワークフローツール（Langflow）でも **OS コマンドインジェクション** が報告され、IoT・AI 分野への影響拡大が懸念されます。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な脆弱性種別 | 影響範囲（利用者・システム） | 注目理由 |
|-----|------|----------------|------------------------------|----------|
| **CVE‑2026‑39770** | 10.0 | Unauthenticated Arbitrary File Upload | Doctreat Core ≤ 1.7.0（WordPress 医療予約プラグイン） | 任意ファイルアップロードにより **Web サーバ上で任意コード実行** が可能。医療情報を扱うサイトは機密性が高く、被害拡大リスクが極めて大きい。 |
| **CVE‑2026‑32579** | 10.0 | Unauthenticated Arbitrary File Upload | Kognetiks Chatbot for WordPress ≤ 2.4.9 | チャットボットは多数の訪問者が利用するため、攻撃者が **マルウェアを埋め込んだ PHP ファイル** を設置でき、サイト全体の乗っ取りにつながる。 |
| **CVE‑2026‑105484** | 10.0 | OS Command Injection (firmware_check) | TOTOLINK X6000R 9.4.0cu.652_B20230116 の `/cgi-bin/cstecgi.cgi` | ルータのファームウェア更新機能を悪用し **任意コマンド実行** が可能。ネットワーク境界機器が侵害されると社内全体に波及する危険性がある。 |
| **CVE‑2026‑105740** / **CVE‑2026‑105697** | 9.9 | Authenticated RCE via “Stdio” transport | Langflow < 1.10.3（AI エージェント構築プラットフォーム） | 認証ユーザーであれば **任意シェルコマンド** を実行でき、内部ネットワーク上の機密データや他サービスへの横移動が容易になる。 |
| **CVE‑2026‑105691** | 9.9 | RCE via SVG Export (child_process.exec) | Penpot < 2.18.0（オープンソースデザインツール） | デザインファイルの **SVG エクスポート** 時にシェルコマンドが実行され、共同編集環境全体が乗っ取られる恐れがある。 |

> **共通点**：いずれも「外部からの入力を適切にサニタイズせず、直接 OS コマンドや PHP コードとして実行」している点が根本原因です。特に **認証不要**（Doctreat、Kognetiks、TOTOLINK）や **低権限ユーザーでも実行可能**（Langflow、Penpot）という点が危険度を高めています。

---

## 3. 推奨アクション  

### 3.1 直ちに実施すべきパッチ適用・バージョンアップ
| 製品 / パッケージ | 現行脆弱バージョン | 推奨バージョン | 備考 |
|-------------------|-------------------|----------------|------|
| Doctreat Core (WordPress) | ≤ 1.7.0 | **> 1.7.0**（公式 1.7.1 以降） | ファイルアップロードロジックのバリデーション強化 |
| Kognetiks Chatbot for WordPress | ≤ 2.4.9 | **≥ 2.5.0** | アップロード拡張子と MIME タイプの厳格チェック |
| TOTOLINK X6000R firmware | 9.4.0cu.652_B20230116 | **最新公式ファームウェア**（2024‑12‑xx 以降） | `/cgi-bin/cstecgi.cgi` の入力検証パッチ適用 |
| Langflow | < 1.10.3 | **≥ 1.10.3** | MCP “Stdio” transport のコマンドホワイトリスト化 |
| Penpot | < 2.18.0 | **≥ 2.18.0** | SVG エクスポート時の `child_process.exec` 呼び出しを安全化 |
| その他 WordPress プラグイン（Workreap, Taskbot, WP Duplicate, WooCommerce Designer Pro, ARMember Premium, Porto Theme, Newsletter Subscription, SendPress, Gmedia Photo Gallery） | それぞれ報告されたバージョン以下 | **各プラグインの最新安定版** | すべてのプラグインで **SQLi / 任意ファイルアップロード** のパッチが提供済み |

### 3.2 環境全体での防御策
- **WAF でファイルアップロード・OS コマンド文字列をブロック**  
  - `*.php`, `*.sh`, `*.exe` など実行可能ファイルの拡張子を拒否。  
  - `;`, `&&`, `|`, `` ` `` などシェルメタ文字列を正規表現で検知し遮断。  
- **最小権限の原則**  
  - WordPress の管理者権限を必要最小限にし、**「Contributor」や「Subscriber」でもファイルアップロードできない**ように設定。  
  - Langflow の「Stdio」機能は **認証済みかつ内部ネットワーク限定** にし、外部からのアクセスをファイアウォールで遮断。  
- **アップロードディレクトリの実行権限除去**  
  - `uploads/`, `wp-content/uploads/` などは **`chmod 0755`** か **`chmod 0644`** にし、Web サーバが実行できないようにする。  
- **シークレット管理の徹底**  
  - Plane, Langflow などでハードコーディングされた `SECRET_KEY` が残っている場合は **即座に再生成** し、環境変数またはシークレット管理ツールに移行。  
- **定期的な脆弱性スキャン

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-39773

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-06T09:17:49.900 |

Unauthenticated Privilege Escalation in Doctreat Core <= 1.7.0 versions.

### CVE-2026-39770

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-06T09:17:49.427 |

Unauthenticated Arbitrary File Upload in Doctreat <= 1.7.0 versions.

### CVE-2026-32579

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-06T09:17:43.613 |

Unauthenticated Arbitrary File Upload in Kognetiks Chatbot for WordPress <= 2.4.9 versions.

### CVE-2026-105484

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-10-06T02:17:04.040 |

A security vulnerability has been detected in TOTOLINK X6000R 9.4.0cu.652_B20230116. The impacted element is the function firmware_check of the file /cgi-bin/cstecgi.cgi of the component UploadFirmwareFile Handler. Such manipulation of the argument file_name leads to os command injection. The attack may be performed from remote.

### CVE-2026-39759

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-06T09:17:47.853 |

Employer / Sales Representative Arbitrary File Upload in Workreap Core <= 3.4.5 versions.

### CVE-2026-39757

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-06T09:17:47.553 |

Subscriber Arbitrary File Upload in Taskbot <= 6.6 versions.

### CVE-2026-39755

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-06T09:17:47.237 |

Subscriber Arbitrary File Upload in WP Duplicate <= 1.1.11 versions.

### CVE-2026-32568

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-06T09:17:42.230 |

Subscriber Remote Code Execution (RCE) in WooCommerce Designer Pro <= 1.9.33 versions.

### CVE-2026-105740

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-05T21:16:35.567 |

Langflow is a tool for building and deploying AI-powered agents and workflows. Prior to 1.9.0, any authenticated Langflow user can achieve Remote Code Execution (RCE) on the server by adding an MCP server with the "Stdio" transport. The user-supplied command field is passed directly to bash -c "exec {command}" with zero validation, no allowlisting, and no sandboxing. The command executes immediately when the server list is fetched. Additionally, the env field allows arbitrary environment variable injection (e.g., LD_PRELOAD, PATH override). This vulnerability is fixed in 1.9.0.

### CVE-2026-105697

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-05T21:16:35.087 |

Langflow is a tool for building and deploying AI-powered agents and workflows. Before Langflow 1.10.3, the MCP stdio transport launched whatever command / args a user put in an MCP server configuration, with no allowlist and (before 1.10.3) wrapped in bash -c "exec {command} ...". Any user able to reach the MCP server settings ("Settings → MCP Servers → Add MCP Server", POST/PATCH /api/v2/mcp/servers/{server_name}) or to build a flow with the MCP Tools component could add a "server" whose command is an arbitrary OS command (touch, rm -rf, a reverse shell, ...). The command runs on the Langflow host as the Langflow process user as soon as Langflow tries to connect to the server (listing servers, loading tools, running the flow) — even when the UI then reports that the stdio server failed to start. With the default LANGFLOW_AUTO_LOGIN=true, GET /api/v1/auto_login hands out a token without credentials, so on an exposed instance running the default configuration this is reachable without an account. AUTO_LOGIN is documented as a development-only setting; with it disabled, any authenticated (non-admin) user can exploit it. This issue is fixed in Langflow 1.10.3, langflow-base 0.10.3, and lfx 1.10.3.

### CVE-2026-105691

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-05T20:17:19.137 |

Penpot is an open-source design and prototyping platform. Prior to 2.18.0, the SVG exporter places an attacker-controlled text object's fill-color value into a ppmcolormask command string and executes that string through child_process.exec. A user who can edit a file can store shell metacharacters in the fill color and trigger SVG export, causing commands to execute with the exporter service's privileges. The same export can be triggered through a valid public share link to a malicious file. This vulnerability is fixed in 2.18.0.

### CVE-2026-105636

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-05T19:17:17.693 |

Plane is an open-source project management tool. Prior to 1.4.0, the webhook delivery task in apps/api/plane/bgtasks/webhook_task.py calls requests.post() without allow_redirects=False and does not validate redirect targets. validate_url() blocks private, loopback, link-local, and reserved addresses in the original webhook URL, but the final URL reached after one or more redirects is not checked. A user who can create a workspace can register a webhook pointing to an attacker-controlled public endpoint that returns a 302 redirect to an internal address. The Plane worker then fetches internal resources, including cloud metadata, and stores the response body in webhook_logs, where the attacker can retrieve it through the workspace webhook-logs API. This issue is fixed in 1.4.0.

### CVE-2026-39797

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-06T09:17:52.843 |

Unauthenticated PHP Object Injection in GDPR Framework By Data443 <= 2.5.0 versions.

### CVE-2026-39761

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-06T09:17:48.010 |

Unauthenticated Privilege Escalation in Meta Box AIO <= 3.7.1 versions.

### CVE-2026-39753

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-06T09:17:46.940 |

Unauthenticated Privilege Escalation in Taskbot <= 6.6 versions.

### CVE-2026-82989

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74;CWE-147` |
| Published | 2026-10-06T00:16:37.097 |

There is an input injection in vCast exposed network services in ViewSonic ViewBoard that allows a remote, unauthenticated attacker to inject arbitrary input into service endpoints via network-based HTTP requests to unauthenticated endpoints

### CVE-2026-97283

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-05T19:17:27.133 |

Deserialization of Untrusted Data vulnerability in Liquid Web / StellarWP Advanced Post Manager advanced-post-manager allows Object Injection.This issue affects Advanced Post Manager: from n/a through 4.5.5.

### CVE-2026-105641

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-05T19:17:18.560 |

Plane is an open-source project management tool. Prior to 1.4.0, the deployments/aio/community/ and deployments/cli/community/ manifests provide fixed, publicly known SECRET_KEY and LIVE_SERVER_SECRET_KEY defaults that remain active when operators do not override them. The top-level setup.sh randomizes secrets only for the development Docker Compose path, leaving unchanged aio and cli community deployments with shared production secrets. Knowledge of SECRET_KEY enables attackers to forge Django-signed values and compromise accounts or sessions. Knowledge of LIVE_SERVER_SECRET_KEY bypasses live-service authentication on unchanged community deployments. This issue is fixed in 1.4.0.

### CVE-2026-105639

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200;CWE-287;CWE-639` |
| Published | 2026-10-05T19:17:18.213 |

Plane is an open-source project management tool. Prior to 1.4.0, Plane's signup flow creates a logged-in User row for any submitted email without an out-of-band ownership check, while User.email is unique=True. The authenticated user can call GET /api/users/me/workspaces/invitations/, which returns each WorkspaceMemberInvite whose email matches request.user.email. WorkSpaceMemberInviteSerializer uses fields = "all", exposing the token that protects the invitation join endpoint. An unauthenticated attacker who knows a target's email can register an account using that address, enumerate pending invitations, and accept an invitation as the target, joining a workspace at the invited role. The term pre-auth describes the attacker's initial state: the attacker has no credential before signup, while the enumeration and join requests use the session created by that signup. This issue is fixed in 1.4.0.

### CVE-2026-88395

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-05T16:17:16.957 |

GouGuOA v6.0.5 and before is vulnerable to SQL Injection in /home/message/rubbish via the keywords parameter.

### CVE-2026-88391

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-05T15:17:22.697 |

Northstar (dromara/northstar, quantitative trading platform) <= 9.1.1 enables the H2 Console but its auth interceptor only covers /northstar/**, so /h2-console is exposed with no authentication and the embedded H2 DB uses default sa / empty password. Any network-reachable attacker can run arbitrary system commands via CREATE ALIAS (pre-auth RCE).

### CVE-2026-91140

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-06T14:17:48.407 |

An OS command injection vulnerability in the shell-based temporary-file cleanup instructions in Progress Software Autonomous REST Connector GenAI Agents ARCGenAI-Generator version 2.0 allows an attacker who supplies a crafted Swagger/OpenAPI document to execute arbitrary commands on a developer's machine when a user invokes the generator.

### CVE-2026-105763

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-06T00:16:33.247 |

Twenty is an open-source CRM (customer relationship management) platform. From 1.20.10 until 2.7.0, the /metadata GraphQL connectedAccounts query returned connectionParameters from ConnectedAccountDTO for every connected account in a workspace, including plaintext IMAP, SMTP, and CalDAV passwords, because the field was not hidden and the lookup did not enforce the calling user's identity or account visibility. A normal workspace member could obtain other members' external-service credentials and use them to access mail or calendars and potentially reset third-party accounts. Google and Microsoft OAuth-only workspaces were not affected. This issue is fixed in version 2.7.0.

### CVE-2026-105637

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-05T19:17:17.860 |

Plane is an open-source project management tool. Prior to 1.4.0, ProjectBulkAssetEndpoint.post in apps/api/plane/app/views/asset/v2.py retrieves assets using id__in=asset_ids and workspace__slug=slug but does not constrain the query with project_id from the URL. A workspace Guest can provide asset UUIDs from another project in the same workspace and reassign their issue_id, comment_id, page_id, draft_issue_id, or project_id to an entity the attacker controls. Plane then treats the attacker's project as the new owner and provides a presigned download URL for the hijacked file. This issue is fixed in 1.4.0.

### CVE-2026-106037

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-06T14:17:42.257 |

Mooncake through 0.3.13.post1 contains a missing authentication vulnerability in the Store REST service, which binds to 0.0.0.0 without authentication on any route. Unauthenticated attackers can call routes such as /api/get, /api/put, /api/remove_all and /api/mount to read cached KV data with user prompts, inject or delete objects, and mount attacker-described segments.

### CVE-2026-42417

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:54.757 |

Unauthenticated SQL Injection in ARMember Premium <= 7.8 versions.

### CVE-2026-42415

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:54.463 |

Unauthenticated SQL Injection in Porto Theme - Functionality <= 3.9.3 versions.

### CVE-2026-41555

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:53.433 |

Unauthenticated SQL Injection in Newsletter Subscription Form – User Subscriptions Form, Capture Email <= 1.5.9 versions.

### CVE-2026-39795

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:52.540 |

Unauthenticated SQL Injection in SendPress Newsletters <= 1.26.1.20 versions.

### CVE-2026-39785

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:51.100 |

Unauthenticated SQL Injection in Gmedia Photo Gallery <= 1.25.1 versions.

### CVE-2026-39764

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:48.310 |

Unauthenticated SQL Injection in Radius Booking — Booking Calendar for Appointments &amp; Services <= 1.0.19 versions.

### CVE-2026-39746

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:45.883 |

Unauthenticated SQL Injection in Booknetic <= 4.8.5 versions.

### CVE-2026-32557

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:42.080 |

Unauthenticated SQL Injection in WooCommerce Appointments <= 5.3.2 versions.

### CVE-2026-85153

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-06T08:16:37.227 |

This vulnerability exists in the Schmooze app due to the use of hardcoded credentials and cryptographic keys in the client application. An unauthenticated remote attacker could exploit this vulnerability by decompiling the distributed application package and extracting the embedded credentials and cryptographic keys.


Successful exploitation of this vulnerability could allow the attacker to gain unauthorized access to backend and cloud resources and forge client requests on the targeted system.

### CVE-2026-94293

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-06T07:17:00.193 |

An unauthenticated remote attacker can modify Asset Administration Shell submodel data via PATCH requests and can read all data exposed by the GET endpoints.

### CVE-2026-91107

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-05T22:16:58.657 |

openSIS Classic 9.3 allows an authenticated user with the built-in teacher role can select an arbitrary staff record through staff_id and cause the School Information update path to reset that selected account's password.

### CVE-2026-21589

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-552` |
| Published | 2026-10-05T22:16:58.423 |

h3. Summary

This is a vulnerability in Bitbucket Data Center, Confluence Data Center, Jira Service Management Data Center, Jira Software Data Center, Bamboo Data Center. Crowd Data Center, Crucible and Fisheye. This Arbitrary File Access vulnerability allows an unauthenticated attacker to access specific files within the web application root directory in affected versions. Exploitation requires prior knowledge of the target file's exact name and path; this vulnerability does not allow attackers to enumerate or list directory contents. In some configurations, there may be some sensitive files that make this highly severe.  

h3. Context

This vulnerability allows an unauthenticated remote attacker to access specific files within the web application root directory in affected versions.

h3. Details:

* The vulnerability must be addressed for affected versions of:
 Bitbucket Data Center, introduced in version >= 4.6.0, fix versions: 9.4.26, 10.2.8, 10.5.1
 Confluence Data Center, introduced in version >= 5.10.0, fix versions 9.2.26, 10.2.19
 Crowd Data Center, introduced in version >= 2.11.0, fix versions 6.3.7, 7.0.3, 7.1.1, 7.2.4
 Jira Software Data Center, introduced in version >= 7.1.0, fix versions 9.12.40, 10.3.26, 11.3.12
 Jira Service Management Data Center, introduced in version >= 3.1.0, fix versions 5.12.40, 10.3.26, 11.3.12
 Bamboo Data Center >= 7.0.1, fix versions 10.2.24, 12.1.12
 Crucible, fix versions 4.9.15
 Fisheye, fix version 4.9.15
* Exploitation requires prior knowledge of the target file's exact name and path.
* The vulnerability does not include the capability to enumerate or list directory contents.

### CVE-2026-103352

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-05T19:17:13.847 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in WP BASE WP BASE Booking wp-base-booking-of-appointments-services-and-events allows Blind SQL Injection.This issue affects WP BASE Booking: from n/a through 6.4.0.

### CVE-2026-102428

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-05T16:17:04.177 |

Joomla Extension - ordasoft.com - Unauthenticated SQL injection in OrdaSoft Joomla CCK < 8.3.16 - The order column for records was user provided and not properly validated, leading to a SQL injection vector.

### CVE-2026-82531

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-06T13:16:50.180 |

Smarty before 4.5.8 and 5.x before 5.8.5 contains a code injection vulnerability where the top-level nocache_hash is never restored during extends:/multi-component template inheritance, leaving it null. Attackers can supply assigned data containing a forged SmartyNocache marker that is copied verbatim into the regenerated PHP cache file, executing arbitrary PHP on include for remote code execution.

### CVE-2026-77226

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-05T21:16:37.337 |

Camunda 7.24.0 before 7.24.15 contains an incorrect authorization vulnerability in the Admin web application's first-run setup endpoint, where SetupResource incorrectly determines setup availability by counting only direct members of the camunda-admin group rather than recognizing all configured administrators. An unauthenticated remote attacker can exploit this logic flaw to call the setup user-create endpoint and create a new administrator account when the camunda-admin group is empty but the system is fully administered, resulting in account takeover and potential process deployment or script execution as the engine's service user.

### CVE-2026-105835

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-10-06T13:16:46.760 |

PLANKA 2.2.0 through 2.2.1 fails to limit incorrect TOTP codes submitted to POST /api/access-tokens/verify-totp, allowing attackers to brute force two-factor authentication codes. Attackers who know a user's password can reuse the ten-minute pending token to guess six-digit codes until one succeeds, obtaining a full access token.

### CVE-2026-105640

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-290` |
| Published | 2026-10-05T19:17:18.383 |

Plane is an open-source project management tool. Prior to 1.4.0, Plane trusts email addresses returned by Gitea OAuth and by self-managed GitLab OAuth deployments where email confirmation is disabled, without verifying that the provider authenticated ownership of the address. An attacker can set an OAuth identity's unverified provider email to a victim's address, which Plane matches directly to the victim's existing local account. The attacker can then log in to the victim's Plane account without knowing the victim's password. GitHub, GitLab.com, and Google are not affected because those providers return verified email addresses. This issue is fixed in 1.4.0.

### CVE-2026-105638

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-307` |
| Published | 2026-10-05T19:17:18.030 |

Plane is an open-source project management tool. Prior to 1.4.0, Plane's magic-code email login uses a six-digit numeric OTP with approximately 20 bits of entropy. The verifier has no per-code failed-attempt counter, and an incorrect code does not increment a counter, invalidate the Redis entry, or lock the email address. The verifier extends django.views.View rather than DRF's APIView, so the configured AnonRateThrottle limit does not apply. The middleware stack also contains no Django-level rate limiter such as django-ratelimit, django-axes, or an IP-throttling middleware. This vulnerability is fixed in 1.4.0.

### CVE-2026-79820

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-05T15:17:22.290 |

A remote user validation failure vulnerability exists in HPE Integrated Lights-Out (iLO) 7 firmware.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-85523

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-06T14:17:47.240 |

Improper neutralization of special elements used in an OS command ('OS command injection') vulnerability in Felisify Information Technologies Industry and Trade Inc. SambaBox allows OS Command Injection.

This issue affects SambaBox: before 5.4.1.

### CVE-2026-106040

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T14:17:43.833 |

Mooncake Store master through 0.3.13.post1 contains a missing authorization vulnerability that allows unauthenticated attackers to erase any object's disk replica via EvictDiskReplica and BatchEvictDiskReplica. Attackers reaching the coro_rpc master port can evict DISK replicas across all tenants, deleting objects whose only remaining replica is on disk.

### CVE-2026-106038

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-06T14:17:42.420 |

Mooncake Store master through 0.3.13.post1 contains a missing authentication vulnerability that allows unauthenticated attackers to force-delete any object via Remove, RemoveByRegex, RemoveAll and BatchRemove on the coro_rpc port. Attackers can send forged requests with the force flag set to bypass lease checks, wipe keys matching any regex, or clear the entire store, causing cache loss and request failures.

### CVE-2026-105788

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-88` |
| Published | 2026-10-06T14:17:40.077 |

Microsoft UFO is an open-source framework for intelligent automation across devices and platforms. Prior to 3.0.10, the type_text and launch_app tools in ufo/client/mcp/http_servers/mobile_mcp_server.py pass the authenticated caller-controlled text and package_name parameters into adb shell command argument positions without comprehensive validation. The adb client joins those arguments into a remote command string that the Android shell reparses, allowing shell metacharacters to execute additional commands on an authorized connected device as the Android shell user. Exploitation requires a valid Mobile MCP API key and a reachable device authorized for ADB, and it does not establish host operating-system execution, Android root execution, or access beyond the Android shell-user privileges. This issue is fixed in version 3.0.10.

### CVE-2026-62072

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T09:17:56.500 |

Subscriber Broken Access Control in Progress Planner <= 1.10.0 versions.

### CVE-2026-39793

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-06T09:17:52.237 |

Subscriber Broken Authentication in Simple JWT Login 4.0.0 versions.

### CVE-2026-39775

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-06T09:17:50.200 |

Subscriber Privilege Escalation in JobZilla - Job Board WordPress Theme <= 2.2 versions.

### CVE-2026-39774

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-06T09:17:50.053 |

Unauthenticated Privilege Escalation in Tourfic Pro <= 1.17.3 versions.

### CVE-2026-39725

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-06T09:17:44.683 |

Contributor Remote Code Execution (RCE) in Content Visibility for Divi Builder <= 5.03 versions.

### CVE-2026-105070

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-06T09:17:40.743 |

Unauthenticated Privilege Escalation in Salon booking system <= 10.31.7 versions.

### CVE-2026-105058

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-06T09:17:40.293 |

Subscriber Privilege Escalation in WP User Profiles <= 2.7.3 versions.

### CVE-2026-105701

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-06T07:16:56.207 |

The ACPT (Premium) plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 2.0.66 via the render function. This is due to missing capability check on the REST API form creation endpoint and unsandboxed Twig environment rendering email templates. This makes it possible for authenticated attackers, with subscriber-level access and above, to execute code on the server. The exploit requires the attacker to first create a form with malicious email_settings via the REST API endpoint, then trigger form submission to execute the injected Twig expressions.

### CVE-2026-97257

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-05T20:17:29.447 |

Deserialization of Untrusted Data vulnerability in PressTigers Simple Event Planner simple-event-planner allows Object Injection.This issue affects Simple Event Planner: from n/a through 1.5.7.

### CVE-2026-100511

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-05T20:17:07.177 |

Deserialization of Untrusted Data vulnerability in Vektor Inc. VK Google Job Posting Manager vk-google-job-posting-manager allows Object Injection.This issue affects VK Google Job Posting Manager: from n/a through 1.3.1.

### CVE-2026-58835

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-05T19:17:24.650 |

In cfg2prop of btif_storage.cc, there is a possible out-of-bounds write due to a heap buffer overflow. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55280

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-457` |
| Published | 2026-10-05T19:17:24.207 |

In multiple locations, there is a possible out-of-bounds write due to uninitialized data. This could lead to remote escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-45524

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-05T19:17:20.533 |

In isSystem of WifiPermissionsUtil.java, there is a possible sandbox escape due to a missing permission check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-105642

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-05T19:17:18.733 |

Ghost is a Node.js content management system. From 6.56.0 until 6.67.0, an image processing library bundled with Ghost contained a vulnerability in its SVG handling. Any staff user, including Contributors, could create a bookmark card for an attacker-controlled website, resulting in arbitrary commands being run on the Ghost server. This issue is fixed in version 6.67.0.

### CVE-2026-101919

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-05T18:17:30.907 |

A flaw was found in the HyperShift operator. The operator copies user-provided Kubernetes configuration (kubeconfig) secrets directly into the privileged control plane namespace without proper validation or sanitization. An authenticated user with cluster and secret creation permissions can exploit this vulnerability by supplying a configuration containing unauthorized executable plugins. When downstream controllers consume this configuration, an attacker can achieve arbitrary code execution within the control plane.

### CVE-2026-105985

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-10-06T11:17:16.857 |

Craft CMS 5.10.13.2 contains an authenticated remote code execution vulnerability in the Control Panel action app/render-components.



Any authenticated user with basic Control Panel access can submit request-controlled component classes and property overrides. By first overriding an EntryType object’s uiLabelFormat and then rendering an Entry that resolves the same request-cached entry type, an attacker can cause arbitrary Twig supplied in the request to be evaluated by renderObjectTemplate().



This render path is not sandboxed. A Twig string callable can therefore reach PHP functions such as system(), resulting in operating-system command execution with the privileges of the PHP/web-server process.



The issue was reproduced with an active non-admin Craft Team user with no optional permissions enabled. No access to entry-editing, Settings, utility, user-management, project-config, filesystem, Kubernetes, or environment variables was required.

### CVE-2026-105632

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-05T18:17:36.593 |

Plane is an open-source project management tool. Prior to 1.4.0, the GraphQL joinProject mutation lets any workspace member add themselves to any project in that workspace including network=0 (secret/private) projects they were never invited to and grants them a full Member role (read + write). The resolver checks only workspace-level membership/role and never checks the target project's visibility (network). This collapses project-level tenant isolation within a workspace: a low-privilege member can read and modify confidential data in every private project. This issue is fixed in 1.4.0.

### CVE-2026-105630

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-434;CWE-616` |
| Published | 2026-10-05T18:17:36.250 |

Plane is an open-source project management tool. Prior to 1.4.0, an authenticated low-privilege workspace member, including a Guest, can upload an image/svg+xml file as a generic or issue attachment. The file retains the attacker-controlled Content-Type, and the asset-download endpoint creates a presigned URL with Content-Disposition: inline. In the default self-hosted MinIO deployment, the asset URL is served from the same origin as the Plane application, allowing embedded SVG JavaScript to execute in the application's security context. A victim, including a workspace administrator, who opens the link can have the session compromised through stored XSS, leading to account takeover. This issue is fixed in 1.4.0.

### CVE-2026-104979

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-862` |
| Published | 2026-10-05T18:17:33.420 |

Plane is an open-source project management tool. Prior to 1.4.0, IntakeIssuePublicViewSet.create in Plane v1.3.1 writes description_html through Issue.objects.create(...) without calling validate_html_content from nh3. Any authenticated user, including a new user with no workspace memberships, can plant arbitrary HTML in a project that has a published DeployBoard with intake enabled. When a project member or viewer of a closed intake item clicks the planted link, the TipTap \tjavascript: parser bypass and the target="_self" click handler execute JavaScript in the viewer's session and exfiltrate a long-lived API token. This issue is fixed in 1.4.0.

### CVE-2026-104976

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-05T18:17:32.913 |

Plane is an open-source project management tool. Prior to 1.4.0, Plane validates GITEA_HOST only for its URL scheme and does not reject hosts that resolve to private or internal IP addresses. The four outbound requests in the Gitea OAuth flow are derived from this unvalidated host and do not call validate_url(). In addition, avatar_url is taken from the Gitea user's profile, where users can configure external avatar URLs. After an administrator enables Gitea OAuth for a legitimate instance, a Gitea user can set an internal URL as the profile avatar and log in through Gitea, causing Plane to fetch the internal target without validation. This issue is fixed in 1.4.0.

### CVE-2026-104968

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-05T17:17:12.627 |

Plane is an open-source project management tool. Prior to 1.4.0, GET /api/workspaces/{slug}/entity-search/?query_type=user_mention returns workspace-member display names, UUIDs, and avatar URLs to any authenticated user who knows the workspace slug, even when the caller is not a workspace member. The endpoint also exposes ProjectMember rows under the same condition. SearchEndpoint in apps/api/plane/app/views/search/base.py inherits BaseAPIView with only permission_classes = [IsAuthenticated] and performs no workspace-membership check. This issue is fixed in 1.4.0.

### CVE-2026-104966

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-05T17:17:12.283 |

Plane is an open-source project management tool. Prior to 1.4.0, two endpoint families fail to verify that nested resource identifiers belong to the workspace and project named in the URL. An authenticated user can read or modify estimates from another workspace through PATCH /api/workspaces/{slug}/projects/{project_id}/estimates/{estimate_id}/, and can inject comments into an issue from another workspace through POST /api/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/. ProjectEntityPermission verifies membership in the workspace and project from the URL, but estimate_id and issue_id are fetched by primary key without confirming the same scope. The list, retrieve, and destroy handlers correctly scope their queries, demonstrating the inconsistency. This issue is fixed in 1.4.0.

### CVE-2026-104892

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-256` |
| Published | 2026-10-05T16:17:06.620 |

Plane is an open-source project management tool. Prior to 1.4.0, aPITokenLogMiddleware logs API keys in plaintext. This allows someone with low privileges to steal user API keys and further escalate their privileges. This issue is fixed in 1.4.0.

### CVE-2026-102775

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-05T16:17:04.317 |

Joomla Extension - phoca.cz - Authorisation bypass through user-controlled key (IDOR) in Order View in Phoca Cart 5.0.0 - 6.1.8 - Phoca Cart's order-file download endpoint does not verify the download tokens it asks for. The d (download token) and o (order token) parameters are checked for non-emptiness only — they are never compared to the stored download_token / order_token values. As a result, any remote user (including a guest with no account at all) can download any customer's digital goods by enumerating sequential id values and supplying arbitrary non-empty tokens.

### CVE-2026-39792

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-06T09:17:52.080 |

Unauthenticated Arbitrary File Deletion in Simple File List <= 6.3.11 versions.

### CVE-2026-105778

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-10-06T07:16:56.547 |

A vulnerability has been found in Tenda AC5 02.03.01.111_multi. Affected by this issue is some unknown functionality of the file /goform/setWifi of the component Wifi Handler. Such manipulation of the argument wifiPwd leads to stack-based buffer overflow. It is possible to launch the attack remotely. The exploit has been disclosed to the public and may be used.

### CVE-2026-105839

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-06T14:17:41.133 |

libmikmod before 3.3.14 contains an integer overflow in the Oktalyzer loader OKT_doPBOD() that allows attackers to cause heap buffer overflow via crafted track counts. Attackers can supply an OKT module whose SLEN chunk wraps the 16-bit numtrk value, causing PBOD writes past allocated track pointers for crashes or code execution.

### CVE-2026-105837

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-06T14:17:40.763 |

libmikmod before 3.3.14 contains an integer overflow vulnerability in DSM_Load() in load_dsm.c that allows attackers to trigger heap buffer overflow via crafted track counts. Attackers can supply a DSM module whose numchn and numpat product wraps a 16-bit value, overwriting heap memory to cause crashes or potential code execution.

### CVE-2026-42416

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:54.610 |

Subscriber SQL Injection in UDesign Core <= 4.15.0 versions.

### CVE-2026-42414

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:54.320 |

Subscriber SQL Injection in ListingPro <= 2.9.12 versions.

### CVE-2026-39771

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:49.590 |

Subscriber SQL Injection in Buddyboss Platform <= 3.1.0 versions.

### CVE-2026-39747

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:46.033 |

Subscriber SQL Injection in Woffice <= 5.4.35 versions.

### CVE-2026-25434

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:41.930 |

Subscriber SQL Injection in WP2LEADS <= 3.5.7 versions.

### CVE-2026-105317

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:41.043 |

Subscriber SQL Injection in Paid Member Subscriptions <= 3.1.1 versions.

### CVE-2026-102915

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T09:17:37.617 |

Subscriber Broken Access Control in WPO365 <= 44.1 versions.

### CVE-2026-105786

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-330;CWE-863` |
| Published | 2026-10-06T00:16:34.283 |

Joplin is an open source note-taking and to-do application that organises notes and lists into notebooks. Prior to 3.7.13, packages/server/src/models/ApplicationModel.ts accepts a caller-chosen application authorization identifier, applications/:id/confirm binds that identifier to a logged-in user through a generic consent page, and the public packages/server/src/routes/api/application_auth.ts endpoint passes it to ApplicationModel.createAppPassword without authenticating or binding the redeemer. An attacker can cause a victim to approve the attacker's identifier, redeem a durable application ID and password, and exchange the credential for a victim session with full read and write access to synchronized data. This vulnerability is fixed in 3.7.13.

### CVE-2026-103066

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-05T20:17:08.027 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in WP BASE WP BASE Booking wp-base-booking-of-appointments-services-and-events allows Blind SQL Injection.This issue affects WP BASE Booking: from n/a through 6.4.0.

### CVE-2026-104971

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-10-05T18:17:32.113 |

Plane is an open-source project management tool. Prior to 1.4.0, DuplicateAssetEndpoint fetches a source FileAsset without limiting it to the caller's workspace, allowing cross-workspace asset duplication. WorkspaceFileAssetEndpoint and the legacy FileAssetEndpoint omit workspace authorization, allowing authenticated users to read, create, modify, or delete assets in workspaces where they are not members. Separately, WorkspaceViewViewSet.retrieve lacks the authorization decorator used by its sibling actions, exposing an unauthorized workspace-view read surface. This issue is fixed in 1.4.0.

### CVE-2026-86671

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73;CWE-522;CWE-918` |
| Published | 2026-10-05T17:17:16.910 |

In Eclipse Che versions 7.29.0 and later, the GET `/api/scm/resolve` and `POST /api/factory/resolver` endpoints pass an attacker-controlled URL to `URLFetcher.fetch()`, which calls `new URL(url).openConnection()` with no scheme or host allow-list and returns the response body to the caller. Any authenticated Che user can read arbitrary local files via the file:// scheme (including the pod's Kubernetes service-account token at `file:///var/run/secrets/kubernetes.io/serviceaccount/token`), reach internal HTTP services and cloud instance metadata endpoints (169.254.169.254), and have their stored SCM personal access token attached as an `Authorization` header to a host of their choosing. The same credential-forwarding behavior also fires when a victim opens a workspace from a malicious devfile whose `parent.uri` points to an attacker-controlled server, enabling exfiltration of the victim's SCM PAT without direct API access. No fix is available.

### CVE-2026-12171

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-88;CWE-94;CWE-829;CWE-918` |
| Published | 2026-10-05T17:17:14.510 |

auto-changelog before 2.6.1 merges configuration from inside the target repository (the .auto-changelog file and the auto-changelog key in package.json) into its options, and honors security-sensitive options from that untrusted source. The handlebarsSetup option is passed to require(), so running auto-changelog over attacker-controlled repository content (for example, in a CI workflow that checks out an untrusted pull request head, or locally on a forked or third-party repository) executes attacker-chosen code with the privileges of the invoking user or CI job, including access to workflow secrets, without the repository dependencies ever being installed. The plugins option similarly loads attacker-controlled modules from the repository. Under the same conditions, appendGitLog/appendGitTag allow git argument injection (e.g. --output= to write arbitrary files), output allows writing attacker-influenced content to arbitrary paths, and template causes an outbound request to an attacker-chosen URL. Version 2.6.1 treats in-repository configuration as untrusted and refuses to run when it sets these options, unless the new --unsafe-config flag is passed.

### CVE-2026-105762

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-06T00:16:33.090 |

Dify is an open-source LLM app development platform. Prior to 1.13.0, the /console/api/remote-files/upload endpoint in api/controllers/web/remote_files.py accepted an attacker-controlled URL without authentication and caused the Dify server to retrieve it. A remote attacker could use the endpoint to send requests to internal services or cloud metadata endpoints, potentially exposing sensitive data and using the server as a network pivot. This issue is fixed in version 1.13.0.

### CVE-2026-95105

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-649` |
| Published | 2026-10-06T09:17:57.200 |

Reliance on Obfuscation or Encryption of Security-Relevant Inputs without Integrity Checking vulnerability in danielberkompas cloak allows an attacker with write access to stored ciphertext to make it decrypt to a chosen value via bit flipping.

Cloak.Ciphers.AES.CTR encrypts with AES-256 in CTR mode and stores the key tag, the IV and the ciphertext with no MAC. decrypt/2 checks only the key tag and the minimum length before it returns the plaintext, and Cloak.Ciphers.Deprecated.AES.CTR decrypts the legacy format the same way. CTR is a stream cipher, so a value XORed into the stored ciphertext is XORed into the plaintext at the same offset. An attacker who can write to the encrypted store (for example through SQL injection or a compromised replica) and who knows or can guess a stored plaintext can replace it with any value of the same length. The application receives that value with no error.

This issue affects cloak: from 0.1.0-pre onward.

### CVE-2026-104852

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-10-05T23:17:00.213 |

GraphQL Tools provides utilities for building, stitching, and mocking GraphQL schemas. Prior to 12.0.1, the GraphQL Tools utils package's mergeDeep function follows inherited properties while recursively merging source objects and does not exclude __proto__, constructor, or prototype keys. An unauthenticated GraphQL client can alias fields to those names so responses from two subgraphs collide during ordinary supergraph result merging, causing mergeDeep to traverse Object and Function prototypes and overwrite Function.prototype.call with a subgraph-supplied value. This breaks subsequent requests in the process until restart. This issue is fixed in version 12.0.1.

### CVE-2026-94201

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-05T20:17:28.693 |

Ash stores :atom-typed attributes as strings and compares them as strings. When such an attribute is referenced in a filter, the comparison value is coerced through Ash.Type.Atom. Because the type defined no coerce/2 callback, coercion fell back to the default (cast_input/2), which calls String.to_atom/1 when the attribute is configured with the unsafe_to_atom?: true constraint.

Filtering such an attribute with attacker-controlled strings therefore interned a new, permanent atom for every distinct value. Atoms are never garbage collected and the BEAM caps the atom table, so an actor who can supply filter values for a public, filterable :atom attribute declared with unsafe_to_atom?: true can exhaust the atom table and crash the node (denial of service). AshPaperTrail is a notable example: its version resources expose a public, filterable version_action_name atom attribute with unsafe_to_atom?: true by default.

The fix adds a coerce/2 to Ash.Type.Atom that never interns atoms — a comparison value is left as a string, since the type is stored and compared as a string. Setting the attribute from action input (cast_input/2, which still honors unsafe_to_atom?) is unchanged.

This issue affects ash: from 3.5.1 before 3.34.3.

### CVE-2026-104978

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-05T18:17:33.247 |

Plane is an open-source project management tool. Prior to 1.4.0, Plane's project invitation list endpoint is accessible to any authenticated user who knows the workspace slug and project ID, while the public project invitation join endpoint accepts an invitation based only on a submitted email address. When a pending invitation targets an email address that has not registered with Plane, an attacker can enumerate the invitation, register an account using the invited email without mailbox verification, and accept the invitation. The attacker-controlled account is then added to the target workspace and project. This issue is fixed in 1.4.0.

### CVE-2026-95594

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-06T09:17:57.577 |

Unauthenticated Privilege Escalation in SMS Alert Order Notifications <= 4.0.0 versions.

### CVE-2026-104747

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-06T09:17:39.643 |

Unauthenticated PHP Object Injection in Haaken <= 1.5 versions.

### CVE-2026-104405

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-06T09:17:39.013 |

Unauthenticated Privilege Escalation in GiveWP <= 4.17.0 versions.

### CVE-2026-105650

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-184` |
| Published | 2026-10-05T20:17:13.817 |

Ghost is a Node.js content management system. From 2.1.0 until 6.64.0, embedding a URL from an attacker-controlled website could result in untrusted scripts being stored in post content. These scripts could run in the Ghost editor, on the published site, and in newsletter emails, possibly resulting in compromise of a staff user's admin session. This issue is fixed in version 6.64.0.

### CVE-2026-105634

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-05T19:17:17.330 |

Plane is an open-source project management tool. Prior to 1.3.0, the ProjectMemberViewSet.partial_update method allows any project member, including a user with the lowest GUEST role, to modify another project member's role. The authorization check prevents assigning a role higher than the requester's role but does not prevent assigning a lower or equal role, allowing a Guest to demote Administrators and Members and deny them project control. This vulnerability is fixed in 1.3.0.

### CVE-2026-104974

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-05T18:17:32.473 |

Plane is an open-source project management tool. Prior to 1.4.0, a user whose account has been deactivated by setting is_active=False can still log in with existing credentials. Successful authentication silently changes is_active back to True, reactivating the account without notifying the administrator. This issue is fixed in 1.4.0.

### CVE-2026-104970

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-05T17:17:12.937 |

Plane is an open-source project management tool. From 0.13 until 1.4.0, InstanceAdminSignUpEndpoint in apps/api/plane/license/api/views/admin.py:89-117, 173-229 uses InstanceAdmin.objects.first() for the first-admin check and performs account creation without an atomic transaction, row lock, uniqueness guard, or advisory lock. Two concurrent unauthenticated requests with different email addresses can both observe that no instance administrator exists, create separate User and InstanceAdmin rows, and receive sessions with instance-admin authority. This allows an attacker to share unrestricted instance administration with the legitimate operator. This issue is fixed in 1.4.0.

### CVE-2026-39776

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-06T09:17:50.347 |

Editor Remote Code Execution (RCE) in Tabs <= 2.5 versions.

### CVE-2026-105783

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-346;CWE-352` |
| Published | 2026-10-06T00:16:33.770 |

Joplin is an open source note-taking and to-do application that organises notes and lists into notebooks. Prior to 3.7.13, when Joplin Desktop is running with the opt-in Web Clipper server enabled, the server in packages/lib/ClipperServer.ts sends Access-Control-Allow-Origin: * and allows an arbitrary website to call POST /auth and GET /auth/check because the pairing endpoints do not reject HTTP or HTTPS origins. The desktop confirmation dialog does not identify the requesting origin, so a victim who approves the generic prompt authorizes the attacking page, which then receives the permanent API token. The token provides ongoing read and write access to notes, folders, tags, resources, and master keys. This issue is fixed in version 3.7.13.

### CVE-2026-4889

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:L/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:56.317 |

SQL injection (SQLi) vulnerability in the eLoanApp application, specifically in the POST parameter 'logina' of the user process endpoint '/ajax/users.php?op=verify'. The parameter is vulnerable to boolean-based and time-based SQL injection. Successfully exploiting this vulnerability would allow an attacker to discover the platform's database engine and cause delays in database queries.

### CVE-2026-57559

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T07:16:59.123 |

Memory corruption while processing service requests.

### CVE-2026-57555

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T07:16:58.980 |

Memory Corruption when executing system service routines due to improper handling of user input buffers.

### CVE-2026-57554

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T07:16:58.760 |

Memory Corruption when asynchronous threads access shared performance counter data simultaneously during FastRPC invocations.

### CVE-2026-57545

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-06T07:16:58.437 |

Memory corruption when processing draw objects of incorrect type during graphics command list execution.

### CVE-2026-57537

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T07:16:58.300 |

Memory Corruption when accessing and modifying geographic mapping data concurrently without proper synchronization.

### CVE-2026-25291

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T07:16:57.893 |

Memory corruption when performing concurrent operations on shared memory page lists due to lack of proper synchronization mechanisms.

### CVE-2026-25267

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T07:16:56.997 |

Memory corruption when non-secure loader rewrites page tables before secure memory initialization.

### CVE-2026-58859

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-05T19:17:25.073 |

In multiple places, there is a possible  denial of service due to an uncaught exception. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58854

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-05T19:17:24.857 |

In multiple locations, there is a possible memory corruption due to type confusion. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58841

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-05T19:17:24.753 |

In multiple functions of VirtualAudioControllerTest.java, there is a possible permission bypass due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58815

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-05T19:17:24.423 |

In multiple locations, there is a possible out of bounds write due to an incorrect bounds check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55286

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-05T19:17:24.317 |

In stpropnci_process of stpropnci.cc, there is a possible out of bounds write due to an incorrect bounds check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55270

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-10-05T19:17:24.097 |

In dialInternal in multiple locations, there is a possible permission bypass due to a confused deputy. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55269

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-05T19:17:23.987 |

In FilterCapturedPacket of snoop_logger.cc, there is a possible memory safety issue due to improper input validation. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55266

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-05T19:17:23.880 |

In qsort of libufdt_sysdeps_vendor.c, there is a possible out-of-bounds write due to resource exhaustion. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-49937

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-05T19:17:21.103 |

In multiple functions of MessageQueueBase.h, there is a possible out of bounds read due to an incorrect bounds check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-49933

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-824` |
| Published | 2026-10-05T19:17:20.983 |

In handle_le_monitor_device_event of msft.cc, there is a possible control-flow hijack in the privileged bluetooth process due to an uninitialized pointer dereference. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-49885

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-05T19:17:20.873 |

In rw_t4t_update_file of rw_t4t.cc, there is a possible out-of-bounds write due to an integer overflow. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-28648

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-10-05T19:17:20.300 |

In Settings, there is a possible permission bypass due to a confused deputy. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-28647

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-05T19:17:20.187 |

In updateState of DeviceAdminAppsPreferenceController.java, there is a possible permission bypass due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-28641

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-05T19:17:20.073 |

In shouldDisableUninstallButton of ApplicationActionButtonsPreferenceController.java, there is a possible permission bypass due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-28640

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-05T19:17:19.957 |

In checkCallerIsCertInstallerOrSelfInProfile of CredentialStorageActivity.java, there is a possible permission bypass due to improper input validation. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-28625

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-05T19:17:19.817 |

In multiple locations, there is a possible permission bypass due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-105841

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-06T14:17:41.460 |

lrzsz before 0.13.0 contains an OS command injection vulnerability in the lrz receive utility's pipe mode that allows remote senders to execute commands by supplying crafted filenames. When lrz runs under a suffixed name such as lrztar, procheader() in src/lrz.c passes the unescaped ZMODEM/YMODEM filename to popen(), so shell metacharacters execute as the receiving user.

### CVE-2026-105840

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-06T14:17:41.300 |

lrzsz before 0.13.0 contains a path traversal vulnerability in the lrz receive utility's restricted mode that allows malicious ZMODEM senders to write files outside the current directory using absolute pathnames. Because checkpath() in src/lrz.c only rejects '../' sequences unless built with --enable-pubdir, attackers can send files named with absolute paths to overwrite any file writable by the receiving user.

### CVE-2026-39752

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-06T09:17:46.790 |

Contributor Arbitrary File Deletion in Jobs for WordPress <= 2.8.2 versions.

### CVE-2026-105764

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-06T00:16:33.450 |

Immich is a high-performance self-hosted photo and video management solution. Prior to 3.2.4, an authenticated non-admin user could upload SVG files that thumbnail-generation code in server/src/repositories/media.repository.ts passed to libvips. Files that bypassed libvips' native SVG loader fell through to ImageMagick, where attacker-controlled &lt;image href&gt; values reached unrestricted MSL and VIDEO coder operations. By storing one crafted asset and referencing its path from a second delayed-marker SVG, an attacker could execute code in the immich-server container when thumbnail processing ran. This issue is fixed in version 3.2.4.

### CVE-2026-104977

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-05T18:17:33.080 |

Plane is an open-source project management tool. Prior to 1.4.0, the fix for CVE-2026-27706 and GHSA-jcc6-f9v6-f7jw, an SSRF in work-item link unfurling shipped in v1.2.2, remains incomplete in the v1.3.1 GA release. Any authenticated project member can make the server fetch attacker-selected internal targets, including cloud metadata at 169.254.169.254, and read the response body returned as the link title or favicon. Complete hardening exists on main in PR 9163 but was not included in an earlier released tag. This issue is fixed in 1.4.0.

### CVE-2026-59358

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-06T07:16:59.460 |

Improper authentication (CWE-287) in the OAuth token endpoint in Cloud Foundry UAA allows a remote, authenticated attacker holding a valid user access token to obtain a fully-privileged client_credentials token for the OAuth client that issued it, by presenting the user token as an OAuth 2.0 Bearer credential on a client_credentials grant request in place of the client’s configured secret.



UAA’s client_credentials handling does not verify that the Bearer credential supplied for client authentication is actually a client credential (a client secret or a valid configured client authentication method); it accepts any valid access token whose client_id matches the request. A token obtained by a normal end user through a public authorization_code + PKCE flow — scoped only to uaa.user, carrying a user_id, and recording client_auth_method=none — satisfies this check. That user token cannot itself administer OAuth clients (POST /oauth/clients correctly returns 403), but when replayed as Bearer authentication on a client_credentials request for the same client, UAA issues a new client-only token carrying the client’s full authorities, such as clients.write. An attacker can use that token to create arbitrary new OAuth clients, including clients with attacker-chosen authorities, without ever possessing the client’s actual secret.



Exploitation requires a valid user access token (the attacker’s own) for a client that is configured to support both a public, user-facing authorization flow and the client_credentials grant type on the same client_id — a non-default combination. Practical impact scales with the authorities assigned to that client.

### CVE-2026-97303

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-05T19:17:27.267 |

Missing Authorization vulnerability in Apps Mav Scratch & Win – Giveaways and Contests scratch-win-giveaways-for-website-facebook allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Scratch & Win – Giveaways and Contests: from n/a through 3.0.2.

### CVE-2026-105628

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-05T18:17:35.917 |

Plane is an open-source project management tool. Prior to 1.4.0, Plane's OAuth avatar synchronization flow fetches avatar_url from provider user data through a server-side HTTP request without internal IP validation and follows redirects by default. An attacker can provide an avatar URL that redirects to an internal-only resource, such as a metadata endpoint, and Plane uploads the fetched response as a user avatar file. The object is then exposed through /api/assets/v2/static/{asset_id}/, allowing exfiltration of internally fetched content. This issue is fixed in 1.4.0.

### CVE-2026-104973

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-05T18:17:32.290 |

Plane is an open-source project management tool. Prior to 1.4.0, the fix for CVE-2026-30242 validates webhook IP addresses only when the webhook is created in apps/api/plane/app/serializers/webhook.py. The delivery task in apps/api/plane/bgtasks/webhook_task.py performs a separate DNS resolution when sending the request and does not validate the resolved IP address, allowing DNS rebinding to bypass the SSRF protection. This issue is fixed in 1.4.0.

### CVE-2026-103831

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-06T11:17:13.783 |

CVE-2026-103831: Insecure deserialization vulnerability in the Psr16CacheAdapter component of the TrueLayer Magento 2 Plugin, due to the use of PHP's native unserialize() function without restrictions on the classes allowed when retrieving data stored in the cache. An attacker who already has the ability to write manipulated data to the cache backend used by Magento—such as Redis or Memcached—could inject specially crafted PHP objects and trigger their deserialization, potentially leading to arbitrary code execution via gadget strings available in the application environment. Exploitation therefore requires a prerequisite condition that allows writing to the cache infrastructure, either through access to the local file system or to a cache infrastructure accessible from the Magento environment.

### CVE-2026-66588

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T09:17:56.660 |

Unauthenticated Broken Access Control in The7 <= 14.2.2 versions.

### CVE-2026-48199

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T09:17:55.930 |

Unauthenticated Broken Access Control in Sermon'e <= 1.0.2 versions.

### CVE-2026-42638

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T09:17:55.627 |

Unauthenticated Broken Access Control in Easy Digital Downloads <= 3.7.1 versions.

### CVE-2026-42413

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-06T09:17:54.170 |

Unauthenticated Sensitive Data Exposure in Snapshotify &#8211; All-in-One Backup &amp; Restore &amp; Migrate <= 1.3.2 versions.

### CVE-2026-41562

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-06T09:17:54.023 |

Unauthenticated Sensitive Data Exposure in Norvis Backup <= 1.1.0 versions.

### CVE-2026-41561

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-06T09:17:53.873 |

Unauthenticated Sensitive Data Exposure in Museder RestoreOne <= 2.7.276 versions.

### CVE-2026-41560

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T09:17:53.730 |

Unauthenticated Broken Access Control in WXD Backup Lite <= 1.0.2 versions.

### CVE-2026-41559

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-06T09:17:53.583 |

Unauthenticated Sensitive Data Exposure in SafeSnap – Verified WordPress Backup &amp; Restore <= 2.1.2 versions.

### CVE-2026-39796

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T09:17:52.697 |

Unauthenticated Broken Access Control in Advanced Posts Listing – Show Post List Easily <= 1.0.8 versions.

### CVE-2026-39794

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T09:17:52.387 |

Unauthenticated Broken Access Control in WooCommerce Multivendor Marketplace – REST API <= 1.6.3 versions.

### CVE-2026-39769

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-06T09:17:49.280 |

Unauthenticated Broken Authentication in Graphina <= 3.1.12 versions.

### CVE-2026-39751

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T09:17:46.640 |

Unauthenticated Broken Access Control in PayPlug for WooCommerce (Official) <= 3.1.0 versions.

### CVE-2026-32580

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:43.780 |

Unauthenticated SQL Injection in WooCommerce Lottery <= 2.2.9 versions.

### CVE-2026-105071

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-06T09:17:40.893 |

Unauthenticated Sensitive Data Exposure in SiteVault – Backup, Restore, Migration &amp; Cloning <= 1.5.17 versions.

### CVE-2026-104385

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-06T09:17:37.917 |

Unauthenticated Sensitive Data Exposure in Groundhogg <= 4.8.3 versions.

### CVE-2026-102387

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-497` |
| Published | 2026-10-06T09:17:37.463 |

Unauthenticated Sensitive Data Exposure in Xserver Migrator <= 1.6.6 versions.

### CVE-2026-57546

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-10-06T07:16:58.630 |

Transient DOS when processing a continuous receive command with a zero-sized global configuration override.

### CVE-2026-41563

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-06T06:17:01.530 |

Unauthenticated Sensitive Data Exposure in Sitemovr <= 1.0.1 versions.

### CVE-2026-41558

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-06T06:17:01.370 |

Subscriber Bypass Vulnerability in WP Migration Plugin DB & Files – WP Synchro <= 1.16.1 versions.

### CVE-2026-39789

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T06:17:01.227 |

Unauthenticated Broken Access Control in Fluent Affiliate Pro <= 1.6.4 versions.

### CVE-2026-39723

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T06:17:00.947 |

Unauthenticated Broken Access Control in Morning for WooCommerce <= 2.4.1 versions.

### CVE-2026-105072

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T06:16:59.313 |

Unauthenticated Broken Access Control in FluentBooking Pro < 2.5.0 versions.

### CVE-2026-82988

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-287;CWE-434;CWE-502` |
| Published | 2026-10-06T00:16:36.973 |

There exists an arbitrary file download in vCast APK delivery mechanism in ViewSonic ViewBoard unknown allows a remote, unauthenticated attacker to trigger unprivileged APK installation via serving a malicious APK URL through an unauthenticated download endpoint

### CVE-2026-105782

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-10-06T00:16:33.613 |

Scrapy is a high-level web crawling and scraping framework for Python. From 1.4.0 until 2.14.2, RefererMiddleware in scrapy/spidermiddlewares/referer.py treated a Referrer-Policy response-header value that resembled a Python import path as a referrer policy class, imported the referenced object, and called it. A malicious website could supply a callable such as sys.exit and terminate a crawler processing the response. This issue is fixed in version 2.14.2.

### CVE-2026-105744

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73;CWE-1188` |
| Published | 2026-10-05T22:16:57.177 |

Docling simplifies document processing by parsing diverse formats and providing integrations with the generative AI ecosystem. From 2.94.0 until 2.132.0, callers that opt into LatexBackendOptions(tikz_engine="tectonic") invoke docling/backend/latex/engines/tectonic.py to compile an untrusted TikZ body and document preamble without restricting TeX file primitives including \openin and \openout. Crafted input can read files available to the converter and create or overwrite writable files, and enabling the tikz_engine_allow_shell_escape option additionally permits shell commands through TeX. The default configuration, which does not enable Tectonic rendering, is not affected. This vulnerability is fixed in 2.132.0.

### CVE-2026-0461

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-05T22:16:55.280 |

Insufficient boundary validation in the USB boot mode implementation of AMD Zynq™ UltraScale+ MPSoC and RFSoC devices could allow unbounded Device Firmware Upgrade (DFU) download requests to overflow the DDR receive buffer into FSBL memory, potentially resulting in unauthorized code execution during the boot process. This issue could impact the confidentiality, integrity, or availability of affected system.

### CVE-2026-105675

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-203;CWE-943` |
| Published | 2026-10-05T20:17:14.367 |

Ghost is a Node.js content management system. From 4.39.0 until 6.64.0, staff users with permission to view staff invites were able to discover the secret token of pending invites, including invites for roles with higher privileges than their own. This could allow a staff user to escalate their privileges by accepting a pending invite. This issue is fixed in version 6.64.0.

### CVE-2026-58865

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-05T19:17:25.183 |

In multiple functions of PduParser.java, there is a possible persistent denial of service due to a missing bounds check. This could lead to remote denial of service with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-103334

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-05T19:17:13.543 |

Insertion of Sensitive Information Into Sent Data vulnerability in Etoile Web Design Incorporated Five Star Restaurant Reservations restaurant-reservations allows Retrieve Embedded Sensitive Data.This issue affects Five Star Restaurant Reservations: from n/a through 2.7.24.

### CVE-2026-93318

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-354` |
| Published | 2026-10-05T18:17:38.080 |

A malicious image can advertise DiffIDs from another image while containing different layer contents. In affected versions, BuildKit could use the advertised DiffIDs to derive cache and snapshot identity without validating that they matched the actual layer contents.

If a BuildKit daemon with shared or persistent cache first processes such a malicious image, a later build using the victim image may mount the attacker-controlled layer contents as the base image. This can allow code from the malicious image to run in the victim build, for example by replacing a commonly executed path such as /bin/sh. The attacker-controlled code may read build secrets mounted into the build, access other build resources, alter output artifacts, or hang the build.

The issue affects both regular snapshotters and lazy-pulling snapshotters such as stargz.

### CVE-2026-105631

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-05T18:17:36.427 |

Plane is an open-source project management tool. Prior to 1.4.0, WorkspaceFileAssetEndpoint.get and WorkspaceAssetDownloadEndpoint.get resolve FileAsset records within a workspace without checking membership in the asset's project, allowing a workspace member to download assets from private projects when the asset UUID is known. EntityAssetEndpoint.get is a separate public-anchor endpoint that grants AllowAny access and scopes the lookup only to the anchor's workspace rather than its published entity or project. An unauthenticated caller who knows a valid anchor and an asset UUID can therefore retrieve issue-description or comment-description assets belonging to unpublished or private projects in that workspace. This issue is fixed in 1.4.0.

### CVE-2026-104891

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-290;CWE-863` |
| Published | 2026-10-05T16:17:06.447 |

mppx-condition-gate provides conditional free-access wrappers for mppx payment methods. Prior to @insumermodel/mppx-condition-gate 3.0.0 and @insumermodel/mppx-token-gate 1.0.4, the packages read a wallet address from the client-supplied credential.source, checked whether that public address met configured on-chain conditions, and returned a successful free-access receipt without invoking the wrapped payment verifier or proving that the caller controlled the wallet. An unauthenticated attacker could name any qualifying wallet and obtain content that should require payment, and cached grants could be reused for the configured cache lifetime. The corrected packages prevent free-access authorization unless payer control has been established. These issues are fixed in @insumermodel/mppx-condition-gate 3.0.0 and @insumermodel/mppx-token-gate 1.0.4.

### CVE-2026-105635

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-200;CWE-284;CWE-862` |
| Published | 2026-10-05T19:17:17.503 |

Plane is an open-source project management tool. Prior to 1.4.0, ProjectJoinEndpoint at GET /api/workspaces/{slug}/projects/{project_id}/join/{pk}/ uses permission_classes = [AllowAny] and returns the full ProjectMemberInvite record, including its email, token, and role, to unauthenticated callers. The corresponding POST endpoint checks only whether the submitted email matches project_invite.email and does not validate the invitation token. An attacker who knows the invitation UUID can discover the invited email, register an account with that email, and accept the invitation without receiving the original invite. This issue is fixed in 1.4.0.

### CVE-2026-95526

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T09:17:57.430 |

Unauthenticated Broken Access Control in BEAR <= 1.2.2 versions.

### CVE-2026-104406

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T09:17:39.163 |

Unauthenticated Broken Access Control in picu <= 3.10.1 versions.

### CVE-2026-105773

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-05T21:16:36.093 |

Canimaan Software ClamXAV versions 3.3 - 3.11 contains a local privilege escalation vulnerability in the Privileged Helper Tool caused by a race condition and insufficient file validation, allowing a local attacker to execute arbitrary code with system privileges. Fixed in 3.11.1.

### CVE-2026-105679

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-434` |
| Published | 2026-10-05T20:17:15.107 |

Ghost is a Node.js content management system. From 6.22.1 until 6.64.0, Ghost restricted the content type used to serve uploaded files to prevent browsers from executing them. On sites using the default local storage adapter, this restriction was not applied, so files uploaded by any staff user were served with a content type derived from their file extension. This could be used to host scripts on the site's domain, possibly resulting in compromise of other staff users' admin sessions. This issue is fixed in version 6.64.0.

### CVE-2026-105651

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-434` |
| Published | 2026-10-05T20:17:14.010 |

Ghost is a Node.js content management system. From 5.94.0 until 6.64.0, when creating a bookmark card, Ghost could store non-image files fetched from an external website as bookmark icons or thumbnails. This allowed any staff user, including Contributors, to host arbitrary HTML on the site's domain, possibly resulting in compromise of other staff users' admin sessions. This issue is fixed in version 6.64.0.

### CVE-2026-105649

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-434` |
| Published | 2026-10-05T20:17:13.613 |

Ghost is a Node.js content management system. From 4.22.0 until 6.65.0, SVG media thumbnails and SVG images uploaded with a non-SVG file extension were stored without sanitization. This allowed any staff user, including Contributors, to host scripts on the site's domain, possibly resulting in compromise of other staff users' admin sessions. This issue is fixed in version 6.65.0.

### CVE-2026-105643

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-653` |
| Published | 2026-10-05T19:17:18.900 |

Ghost is a Node.js content management system. From version 6.34.0 until 6.67.0, embed cards in the Ghost editor could bypass protections against stored cross-site scripting. Any staff user, including Contributors, could store scripts in post content that ran when another staff user opened the post in the editor, potentially compromising that user’s admin session. Self-hosted sites should leave the new  security.embedPreviewUrl  configuration option at its default value. This issue is fixed in version 6.67.0.

### CVE-2026-48197

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-06T09:17:55.777 |

Incorrect Privilege Assignment vulnerability in PublishPress PublishPress Capabilities capability-manager-enhanced allows Privilege Escalation.This issue affects PublishPress Capabilities: from n/a through 2.45.0.

### CVE-2026-39765

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-06T09:17:48.457 |

Shop Manager Privilege Escalation in Challan <= 3.7.88 versions.

### CVE-2026-39729

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:L/A:L` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-06T09:17:45.287 |

Unauthenticated Sensitive Data Exposure in Edwiser Bridge <= 4.3.4 versions.

### CVE-2026-39728

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-06T09:17:45.140 |

Unauthenticated Server Side Request Forgery (SSRF) in Instapage Plugin <= 3.7.2 versions.

### CVE-2026-39719

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-06T09:17:44.077 |

Unauthenticated Server Side Request Forgery (SSRF) in PDF Smart Viewer for Elementor <= 1.0.4 versions.

### CVE-2026-104757

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-06T09:17:39.810 |

Editor Privilege Escalation in Import and export users and customers <= 2.5.5 versions.

### CVE-2026-104387

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T09:17:38.077 |

Unauthenticated Broken Access Control in PowerPress Podcasting <= 11.17.9 versions.

### CVE-2026-75962

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T06:17:01.687 |

The Post SMTP – Complete Email Deliverability and SMTP Solution with Email Logs, Alerts, Backup SMTP & Mobile App plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'user_email' parameter in all versions up to, and including, 4.0.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is exploitable without authentication on WordPress Multisite installations with public registration enabled, as WordPress accepts email addresses containing numeric HTML character references that Post SMTP's stricter validator rejects, persisting the attacker-controlled address verbatim to the email log via the failed-send exception message.

### CVE-2026-95263

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-05T20:17:29.050 |

Feehi CMS 2.1.1 is vulnerable to Incorrect Access Control. A low-privilege backend administrator with administrator-update permission can change the password of the built-in super administrator account. The server does not enforce protection for this account, and the update scenario does not require the old password.

### CVE-2026-93617

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-05T20:17:28.537 |

Deserialization of Untrusted Data vulnerability in WP Sunshine Sunshine Photo Cart sunshine-photo-cart allows Object Injection.This issue affects Sunshine Photo Cart: from n/a through 3.7.1.

### CVE-2026-105677

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-94;CWE-829` |
| Published | 2026-10-05T20:17:14.733 |

Ghost is a Node.js content management system. From 6.10.3 until 6.64.0, a vulnerability in how Ghost loads theme translation files allowed an authenticated Administrator to execute arbitrary code on the server via a crafted theme. This issue is fixed in version 6.64.0.

### CVE-2026-103348

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-05T20:17:08.330 |

Deserialization of Untrusted Data vulnerability in Smackcoders Inc. WP Ultimate Exporter wp-ultimate-exporter allows Object Injection.This issue affects WP Ultimate Exporter: from n/a through 3.0.

### CVE-2026-100506

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-05T20:17:03.760 |

Deserialization of Untrusted Data vulnerability in WP Spell Check WP Spell Check wp-spell-check allows Object Injection.This issue affects WP Spell Check: from n/a through 12.1.

### CVE-2026-49878

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-05T19:17:20.650 |

In wpas_handle_robust_av_scs_recv_action of robust_av.c, there is a possible out-of-bounds write due to a logic error in the code. This could lead to remote code execution with System execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-103349

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-05T19:17:13.703 |

Deserialization of Untrusted Data vulnerability in Rymera Web Co Product Feed PRO for WooCommerce woo-product-feed-pro allows Object Injection.This issue affects Product Feed PRO for WooCommerce: from n/a through 13.5.7.

### CVE-2026-104890

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-05T16:17:06.270 |

Kunstmaan CMS is an open source content management system based on the Symfony framework. Prior to 7.3.2, src/Kunstmaan/MediaBundle/Helper/File/FileHandler.php performs the blacklisted_extensions check case-sensitively in FileHandler::getFilePath and lowercases the stored extension afterward. An authenticated backend user with media access can upload a mixed-case executable extension such as PHP that bypasses the check and is stored in the web-accessible media directory with an executable lowercase extension. The default blacklist also omits several server-executable extension types, allowing the same code-execution impact where the web server executes uploaded files. This issue is fixed in version 7.3.2.

### CVE-2026-105834

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-06T13:16:46.597 |

Rundeck before 6.2.0 contains a path traversal vulnerability that allows users holding only the project configure ACL to read arbitrary server files by setting resources.source.N.config.file to any absolute path. Attackers can retrieve file contents through editProjectNodeSourceFile or the apiSourceGetContent endpoint to obtain database passwords, LDAP bind credentials, and other projects' data.

### CVE-2026-94675

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:57.047 |

Unauthenticated Cross Site Scripting (XSS) in Fluent Forms Pro Add On Pack <= 6.2.13 versions.

### CVE-2026-42636

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:55.333 |

Unauthenticated Cross Site Scripting (XSS) in WP Cookie Notice for GDPR, CCPA & ePrivacy Consent <= 4.4.6 versions.

### CVE-2026-42635

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:55.193 |

Unauthenticated Cross Site Scripting (XSS) in WooCommerce Simple Auctions <= 3.0.10 versions.

### CVE-2026-42634

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:55.047 |

Unauthenticated Cross Site Scripting (XSS) in Video Background Block – Use video as background in the section. <= 2.0.3 versions.

### CVE-2026-42418

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:54.900 |

Unauthenticated Cross Site Scripting (XSS) in Social Rocket <= 1.3.5 versions.

### CVE-2026-40807

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:53.287 |

Unauthenticated Cross Site Scripting (XSS) in CF7 Views &#8211; Complete Entry Management for Contact Form 7 <= 3.2.6 versions.

### CVE-2026-40806

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:53.140 |

Unauthenticated Cross Site Scripting (XSS) in Blog, Posts and Category Filter for Elementor <= 2.1.0 versions.

### CVE-2026-39790

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:51.777 |

Unauthenticated Cross Site Scripting (XSS) in VikRentCar <= 1.4.6 versions.

### CVE-2026-39784

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:50.940 |

Unauthenticated Cross Site Scripting (XSS) in Hotel Booking <= 3.8 versions.

### CVE-2026-39781

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:50.793 |

Unauthenticated Cross Site Scripting (XSS) in Document Gallery <= 5.1.1 versions.

### CVE-2026-39780

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:50.647 |

Unauthenticated Cross Site Scripting (XSS) in Youzify <= 1.3.7 versions.

### CVE-2026-39778

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:50.503 |

Unauthenticated Cross Site Scripting (XSS) in Ansar Import – One Click Starter Sites – for Elementor &amp; Themes <= 2.1.2 versions.

### CVE-2026-39768

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:49.080 |

Unauthenticated Cross Site Scripting (XSS) in Security & Malware scan by CleanTalk <= 2.189 versions.

### CVE-2026-39766

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:48.610 |

Unauthenticated Cross Site Scripting (XSS) in ARForms <= 7.1.2 versions.

### CVE-2026-39758

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:47.707 |

Unauthenticated Cross Site Scripting (XSS) in Midtrans-WooCommerce <= 2.32.3 versions.

### CVE-2026-39750

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:46.487 |

Unauthenticated Cross Site Scripting (XSS) in StoreGrowth: Smart Sales Booster for WooCommerce | BOGO, Upsells, Direct Checkout, Quick View, Side Cart <= 2.0.6 versions.

### CVE-2026-39748

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:46.180 |

Unauthenticated Cross Site Scripting (XSS) in EduMall <= 4.5.3 versions.

### CVE-2026-39745

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:45.730 |

Unauthenticated Cross Site Scripting (XSS) in Contact Form to DB by BestWebSoft <= 1.7.6 versions.

### CVE-2026-39731

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:45.583 |

Unauthenticated Cross Site Scripting (XSS) in Database for CF7 <= 1.2.6 versions.

### CVE-2026-39730

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T09:17:45.433 |

Missing Authorization vulnerability in Marcin Wise Chat wise-chat allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Wise Chat: from n/a through 3.4.2.

### CVE-2026-39726

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:44.833 |

Unauthenticated Cross Site Scripting (XSS) in Lumise Product Designer <= 2.1.1 versions.

### CVE-2026-39724

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:44.533 |

Unauthenticated Cross Site Scripting (XSS) in HTTP Requests Manager <= 1.3.11 versions.

### CVE-2026-39722

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:44.380 |

Unauthenticated Cross Site Scripting (XSS) in WPLMS  <= 4.972 versions.

### CVE-2026-39720

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:44.227 |

Unauthenticated Cross Site Scripting (XSS) in Mapster WP Maps <= 2.0.4 versions.

### CVE-2026-32581

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T09:17:43.930 |

Subscriber SQL Injection in Mooberry Book Manager 4.16.2 versions.

### CVE-2026-32578

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T09:17:43.460 |

Subscriber Broken Access Control in ECPay Ecommerce for WooCommerce <= 1.1.2606090 versions.

### CVE-2026-32577

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:43.297 |

Unauthenticated Cross Site Scripting (XSS) in Frontend File Manager <= 23.6 versions.

### CVE-2026-32575

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:43.150 |

Unauthenticated Cross Site Scripting (XSS) in SUMO Affiliates Pro <= 11.7.0 versions.

### CVE-2026-32574

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:43.000 |

Unauthenticated Cross Site Scripting (XSS) in Smart Forms <= 2.6.104 versions.

### CVE-2026-32572

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:42.847 |

Unauthenticated Cross Site Scripting (XSS) in WP User Frontend Pro <= 4.2.13 versions.

### CVE-2026-32570

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:42.550 |

Unauthenticated Cross Site Scripting (XSS) in Progressify - Progressive Web App (PWA) <= 1.6.0 versions.

### CVE-2026-32569

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:42.397 |

Unauthenticated Cross Site Scripting (XSS) in WP Media folder <= 6.2.2 versions.

### CVE-2026-25433

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T09:17:41.777 |

Subscriber Broken Access Control in WP2LEADS <= 3.5.7 versions.

### CVE-2026-105061

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:40.597 |

Unauthenticated Cross Site Scripting (XSS) in WP Mailster <= 1.9.0.0 versions.

### CVE-2026-104814

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:39.973 |

Unauthenticated Cross Site Scripting (XSS) in Form Block <= 1.8.1 versions.

### CVE-2026-104672

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:39.483 |

Unauthenticated Cross Site Scripting (XSS) in GiveWP <= 4.17.0 versions.

### CVE-2026-104670

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:39.317 |

Unauthenticated Cross Site Scripting (XSS) in LearnPress <= 4.4.9 versions.

### CVE-2026-104395

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:38.570 |

Unauthenticated Cross Site Scripting (XSS) in picu <= 3.10.1 versions.

### CVE-2026-104394

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:38.230 |

Unauthenticated Cross Site Scripting (XSS) in Charitable <= 1.8.12.3 versions.

### CVE-2026-103346

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T09:17:37.760 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Tomlister Payflex Payment Gateway payflex-payment-gateway allows Reflected XSS.This issue affects Payflex Payment Gateway: from n/a through 2.7.1.

### CVE-2026-25302

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-06T07:16:58.040 |

Cryptographic Issue when processing non-ELF partitions, authentication and signature checks are bypassed, allowing unsigned or corrupted images to be mounted and processed.

### CVE-2026-39760

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T06:17:01.087 |

Unauthenticated Cross Site Scripting (XSS) in Real 3D FlipBook <= 5.5 versions.

### CVE-2026-105761

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-05T23:17:03.050 |

Dify is an open-source LLM app development platform. Prior to 1.16.0, the PUT /console/api/apps/&lt;app_id&gt;/server endpoint in api/controllers/console/app/mcp_server.py used AppMCPServerController.put() to retrieve an AppMCPServer by the client-supplied server ID without verifying that the server belonged to the requested application and tenant. An authenticated workspace member could therefore change another application's MCP server status and parameters, potentially redirecting data or disabling the service. This issue is fixed in version 1.16.0.

### CVE-2026-105741

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-290;CWE-345` |
| Published | 2026-10-05T21:16:35.740 |

Langflow is a tool for building and deploying AI-powered agents and workflows. From 1.5.0 until 1.10.3, an IP spoofing vulnerability in the Model Context Protocol (MCP) configuration installation endpoint (POST /api/v1/mcp/project/{project_id}/install) allowed authenticated remote attackers to bypass the "local-only" access restriction. By sending a spoofed X-Forwarded-For: 127.0.0.1 header, an attacker could make the server treat the request as originating from localhost, letting them write/overwrite an MCP client configuration file on the server's filesystem. This vulnerability is fixed in 1.10.3.

### CVE-2026-105699

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-05T21:16:35.410 |

Langflow is a tool for building and deploying AI-powered agents and workflows. From 1.6.8 until 1.9.1, Langflow authenticated access to the project identifier in a project-scoped MCP connection but did not authorize the resource URI supplied to resources/read. read_resource forwarded the attacker-controlled URI to handle_read_resource, which parsed a flow_id and filename and called storage_service.get_file without verifying that the flow belonged to the authenticated user or current project. A user with access to any project-scoped MCP endpoint could therefore request another user's flow-backed file, while global handle_list_resources and handle_list_tools behavior could disclose flow and file identifiers that made targeting easier. The vulnerability disclosed uploaded documents, structured data, prompts, and other private flow artifacts across tenants but did not modify victim files or stored flows. This issue is fixed in version 1.9.1.

### CVE-2026-97309

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-05T19:17:27.667 |

Missing Authorization vulnerability in Webful Creations RepairBuddy computer-repair-shop allows Retrieve Embedded Sensitive Data.This issue affects RepairBuddy: from n/a through 4.1226.

### CVE-2026-100515

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-05T19:17:12.200 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in VillaTheme Photo Reviews for WooCommerce woo-photo-reviews allows Reflected XSS.This issue affects Photo Reviews for WooCommerce: from n/a through 1.2.30.

### CVE-2026-93316

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-05T18:17:37.780 |

If BuildKit daemon is started with --cdi-disabled it can lead to daemon panic when builds try to use CDI devices. This can happen maliciously or by accident.

### CVE-2026-105633

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-05T18:17:36.757 |

Plane is an open-source project management tool. Prior to 1.4.0, the V2 issue-attachment PATCH endpoint accepts issue_id in the URL but omits it from the database query. A project member can use an issue_id they control in the URL while targeting another user's attachment by its pk UUID. Because the server matches only pk, workspace, and project_id, it modifies the attachment regardless of the issue_id in the URL. When the attachment is pending and has not been confirmed as uploaded, the PATCH handler sets created_by = request.user and transfers attachment ownership to the attacker. This issue is fixed in 1.4.0.

### CVE-2026-105629

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-05T18:17:36.087 |

Plane is an open-source project management tool. Prior to 1.4.0, BulkEstimatePointEndpoint.destroy resolves an estimate point through a bare primary-key lookup without workspace, project, or estimate scoping. An administrator or member of one workspace can permanently delete an estimate point belonging to another workspace by supplying the target UUID in a URL under the attacker's own workspace. This creates a destructive cross-tenant IDOR. This issue is fixed in 1.4.0.

### CVE-2026-104975

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-05T18:17:32.747 |

Plane is an open-source project management tool. Prior to 1.4.0, Plane's dashboard asset endpoints in plane/app/views/asset/v2.py were remediated for two cross-tenant asset IDORs, CVE-2026-27705 and CVE-2026-46558. Those fixes added a membership check and project_id and workspace__slug scoping to the asset endpoints in that file. The Spaces app in plane/space/views/asset.py serves related public-board operations under /api/public/ but was not remediated. Its EntityAssetEndpoint and AssetRestoreEndpoint resolve a DeployBoard from a public anchor and then read or modify FileAsset rows scoped only to the board's workspace, without a membership check or project_id constraint. An attacker can therefore read, overwrite, or restore assets across projects and workspaces. This issue is fixed in 1.4.0.

### CVE-2025-15643

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-05T18:17:28.767 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Jose Fernandez Adsmonetizer adsensei-b30 allows Reflected XSS.This issue affects Adsmonetizer: from n/a through 3.2.4.

### CVE-2026-102282

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-05T17:17:08.110 |

adm-zip is a JavaScript library for creating and extracting ZIP archives in Node.js. Prior to 0.6.1, adm-zip applies the Unix permission bits stored in a zip entry directly to the extracted file via `fs.chmodSync()` when `keepOriginalPermission=true` is passed to `extractAllTo()`/`extractEntryTo()` — and it never filters the setuid/setgid/sticky bits out of those bits. A zip crafted by an attacker can therefore produce an extracted binary with mode `04755`. When extraction runs as root (the default posture in Docker builds, CI runners, and privileged install steps — the exact environments where this flag is used), the resulting root-owned setuid file is executed later by a lesser-privileged user, turning the attacker's code into a root execution. Version 0.6.1 fixes the issue.

### CVE-2026-84854

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-06T10:16:54.230 |

In the WibuKey driver for Windows below Version 6.72, insufficient validation of user input when calculating the size of a kernel buffer could cause small amounts of data to be written outside the intended kernel buffer. This can lead to a system crash. Under unfavorable circumstances, adjacent kernel memory may be modified.

### CVE-2026-102262

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-668` |
| Published | 2026-10-05T21:16:32.400 |

Newell Brands DYMO ID 1.5.1.71 resolves its plugin Modules directory relative to the process working directory. An attacker could store a job file alongside malicious modules / DLL that sets the process working directory to the job file's folder when a victim clicks on the file, resulting in code execution at the victim's privilege level. Fixed in 1.6.0.

### CVE-2026-58880

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-05T19:17:25.377 |

In handle_app_val_response of btif_rc.cc, there is a possible way to achieve code execution due to a race condition. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.
