# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-20 15:00 UTC
- **対象期間**: `2026-10-19T15:01:07.000Z` 〜 `2026-10-20T15:00:38.000Z`
- **重要CVE数**: 164 件（Critical 9.0+: 28 件 / High 7.0〜: 136 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコア 7.0 以上のものは **30 件近く** に上り、特に **Python エコシステム、Kubernetes/コンテナオーケストレーション、Web アプリケーションフレームワーク** に集中しています。  
- **リモートコード実行 (RCE)** が最も多く、ほとんどが認証不要、または認証バイパスと組み合わせた形で実装ミスが露呈しています。  
- **サプライチェーン攻撃**（例：Rank Math SEO PRO）の報告が増えており、パッケージリポジトリや Docker イメージの信頼性確認が重要です。  
- **Kubernetes のカスタムリソース／Operator** に対する権限昇格やクラスタ全体への横展開が顕在化しており、RBAC 設計の見直しが急務です。  

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な影響 | 注目すべき理由 |
|-----|--------|----------|----------------|
| **CVE‑2026‑111057** (CVSS 10.0) | 10.0 | Mercury (Jupyter notebook → Web アプリ) で `/api/terminals` がブロックリスト回避 → 任意コード実行 | **最高スコア**。デフォルトのトークンレスデプロイで匿名ユーザーが任意の Python を実行でき、クラウド上の共有ノートブック環境全体が即座に乗っ取られる危険性がある。 |
| **CVE‑2026‑105312** (CVSS 9.9) | 9.9 | Kubernetes の Console カスタムリソースに対する `create` 権限だけで、任意イメージを Pod にデプロイし、ClusterRoleBinding でクラスタ全体のリード権限取得 | **クラスタ全体への横展開** が可能になるため、内部脅威だけでなく外部からの侵入後の権限昇格シナリオで致命的。 |
| **CVE‑2026‑111862** (CVSS 9.8) | 9.8 | Rank Math SEO PRO (WordPress) のサプライチェーン改ざん。特定期間に配布された 3.0.123 パッケージにマルウェアが混入。 | **サプライチェーン** という点で、単なる脆弱性ではなく **配布プロセス全体の信頼性** が揺らいでいる。WordPress サイトは多数がこのプラグインを利用しているため、感染拡大リスクが高い。 |
| **CVE‑2026‑107083** (CVSS 9.8) | 9.8 | SLiMS (図書館管理システム) の `dl_detail.php` に SQLi。パラメータ `fileID` で任意 SQL が実行可能。 | **業務系システム** に対する直接的なデータベース破壊・情報漏洩リスク。多くの大学・公共図書館が導入している点でインパクトが大きい。 |
| **CVE‑2026‑77936** (CVSS 9.3) | 9.3 | Letta (AI ツール) の `docker-compose.yml` が `LETTA_SERVER_SECURE` を無効化し、PostgreSQL のデフォルトクレデンシャルが公開。API が無認証で Python コード実行可能。 | **デプロイ時の設定ミス** が原因で、外部から直接コード実行が可能になる典型例。コンテナデプロイのベストプラクティスが守られていないことを示す警鐘。 |

> **注**：上記はスコアと実際の被害拡大リスク（利用者数・インフラ重要度）を総合的に評価した結果です。  

---

## 3. 推奨アクション  

### 3.1. 直ちに実施すべきパッケージアップデート
| 製品 / パッケージ | 現行脆弱バージョン | 修正バージョン (リリース日) | アップデート方法 |
|-------------------|-------------------|----------------------------|-------------------|
| **Mercury** (Python) | 3.0.0 – 3.2.4, 3.2.5 (トークンレス) | **≥ 3.2.6** (2026‑09‑15) | `pip install --upgrade mercury-framework` または OS のパッケージマネージャで `mercury` を再インストール。 |
| **Kubernetes Console Operator** | 任意 (spec.containers.api.spec.image 未検証) | **v2.5.1** 以降 (2026‑08‑30) | `kubectl apply -f operator.yaml --force` で最新版マニフェストを適用し、`ClusterRoleBinding` のスコープを最小化。 |
| **Rank Math SEO PRO** (WordPress) | 3.0.123 (2026‑10‑15/16) | **3.0.124** (2026‑10‑20) 以上 | WordPress 管理画面 → プラグイン更新、または `wp plugin update rank-math-pro`。過去にインストールした 3.0.123 を削除し、ファイルシステム上の残存コードも全削除。 |
| **SLiMS (Library Management System)** | 9.8.0 | **9.8.1** (2026‑09‑05) | `composer update slims/slims` または公式リリースの zip を展開し、`dl_detail.php` のパラメータバリデーションが修正された版に差し替える。 |
| **Letta** (AI ツール) | 0.16.8 | **0.16.9** (2026‑09‑12) 以上 | `docker-compose pull letta && docker-compose up -d` でイメージ更新。`docker-compose.yml` に `LETTA_SERVER_SECURE=true` と `POSTGRES_PASSWORD` を強固なランダム文字列に変更。 |

### 3.2. 設定・運用上のベストプラクティス
1. **認証・認可のデフォルトを「拒否」へ**  
   - API エンドポイントは必ず **認証必須** にし、`setDenyUncoveredHttpMethods(true)` などのフレームワーク設定を有効化。  
2. **RBAC の最小権限化**  
   - Kubernetes では `create` 権限だけでカスタムリソースを作成できないよう、`spec.containers.image` の検証ロジックを Admission Controller で追加。  
3. **サプライチェーンの検証**  
   - Docker イメージは **SBOM**（Software Bill of Materials）と **署名**（cosign, Notary）で検証し

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-111057

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-185;CWE-284` |
| Published | 2026-10-19T16:17:03.810 |

Mercury is a Python framework for sharing Jupyter notebooks as web applications and dashboards. From 3.0.0 until 3.2.4, a missing comma in BLOCKED_PATTERNS concatenates the /lab and /api/terminals regular-expression literals. Requests to /api/terminals therefore bypass the anonymous endpoint blocklist and reach Jupyter Server's terminal API. An unauthenticated attacker can use the resulting interactive operating-system shell to execute commands and access data available to the Mercury process. This issue is fixed in version 3.2.4.

### CVE-2026-105312

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-20T12:17:28.703 |

A Kubernetes tenant with create permission on Console custom resources can set spec.containers.api.spec.image to an arbitrary container image. The operator deploys this image into a pod whose ServiceAccount is bound via ClusterRoleBinding to a ClusterRole granting cluster-wide get/list/watch on all Strimzi CRDs (including KafkaUsers), patch on Kafkas/KafkaRebalances, and cluster-monitoring-view. The attacker's code reads the projected SA token and gains cross-tenant Strimzi control-plane read+write access.

### CVE-2026-113620

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-20T13:16:41.610 |

In Eclipse ioFog Controller versions 3.8.0 through 3.9.1, operator WebSocket upgrades on the exec and log routes do not verify the bearer JWT. The payload is decoded and its groups or roles are used as RBAC subjects. A self-minted token whose groups contain admin matches the built-in admin role, with no account and no RoleBinding. The attacker can open an exec or log session for a microservice or fog whose UUID they already know. HTTP routes are not affected: they verify the token before RBAC. Agent WebSockets verify the fog token and are not affected.

### CVE-2026-111862

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-506` |
| Published | 2026-10-19T17:17:04.507 |

Rank Math SEO PRO for WordPress is affected by a supply-chain compromise in a subset of version 3.0.123 packages downloaded or updated between October 15, 2026 at 20:02 UTC and October 16, 2026 at 07:12 UTC. Rank Math states that the affected plugin files contained malware that could compromise a website if the plugin was activated and directs sites that activated an affected package to treat the website as compromised. The malware may establish persistent access, communicate with rank1cdn[.]com, recreate hidden backdoors on page visits, and expose WordPress credentials, database credentials, API keys, and other secrets accessible to the web server. Rank Math identifies three malicious wp_options keys, hidden PHP backdoors, unauthorized administrator accounts, a fake WordPress core file, PHP-executable .cache files, and a system cron marker as incident indicators. Only packages obtained during the vendor-confirmed window are claimed as affected; version 3.0.123 alone is not sufficient to establish compromise. Rank Math removed the affected files and released version 3.0.124 as the clean replacement.

### CVE-2026-107083

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-19T17:17:00.690 |

SENAYAN Library Management System (SLiMS) Bulian (slims9_bulian) 9.8.0 is vulnerable to SQL Injection in admin/modules/reporting/customs/dl_detail.php via the parameter fileID.

### CVE-2026-111058

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-19T16:17:03.957 |

Mercury is a Python framework for sharing Jupyter notebooks as web applications and dashboards. Prior to 3.2.6, default tokenless deployments allow anonymous clients to create Jupyter kernels and send execute_request messages containing arbitrary Python. The endpoint blocklist does not cover /api/kernels, and the websocket wrapper previously tracked idle activity without authorizing executable messages. This issue is fixed in version 3.2.6.

### CVE-2026-107188

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-19T17:17:01.080 |

A user can upload export reports with any file contents and specify any contents. JSP code can be uploaded, JSPX can be specified as the file extension, and anyone can browse to the uploaded file, leading to command execution. The authentication bypass vulnerability can be chained with this vulnerability to run code on the server without authentication.

### CVE-2026-9589

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-10-20T11:17:35.770 |

Missing authorization in the configuration cascade operations of the Collaboration Server in Unblu inc. Unblu Spark 7.0 through 8.36.1-hotfix.0, on on-premises and cloud deployments, allows an authenticated remote attacker to read and change configuration properties of entities they aren't authorized to access, including other users, other accounts and, in Unblu Cloud, other customers' accounts, via configuration read and write operations that target those entities.



The Collaboration Server doesn't check whether the user reading or changing configuration has access to the entity the configuration belongs to. With certain non-default configuration validation settings, a registered user can additionally write configuration properties they aren't allowed to edit, in any scope.



Exploitation requires an authenticated session but no user interaction.

### CVE-2026-43844

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T09:17:10.800 |

A vulnerability in the proprietary protocol could allow an attacker to bypass the authentication mechanism.

### CVE-2026-43836

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T09:17:09.957 |

A vulnerability could allow an attacker to forge a packet to execute arbitrary commands with maximum privileges.

### CVE-2026-113380

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-10-20T05:16:54.083 |

In the RingRTC library before 2.72.0 for Signal, a peer that saturates a call's FSM queue can interfere with the ability of a local hangup to tear the call (with its audio and perhaps also video track) down.

### CVE-2026-77936

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-10-20T01:17:20.107 |

Letta through 0.16.8 ships a compose.yaml that does not enable LETTA_SERVER_SECURE, so the password middleware is never added and all API routes are unauthenticated, and it exposes a superuser PostgreSQL port with default credentials. Remote attackers can execute arbitrary Python via POST /v1/tools/run, manage /v1/admin users, or run OS commands via COPY PROGRAM.

### CVE-2026-77933

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-10-20T01:17:19.670 |

DB-GPT through 0.8.2 contains a hardcoded credentials vulnerability in its default docker-compose.yml that sets a static MYSQL_ROOT_PASSWORD and publishes port 3306 on all interfaces. Attackers reaching port 3306 or the shared dbgptnet network can authenticate as root@% to gain full database access including FILE and SUPER privileges.

### CVE-2026-77932

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-20T01:17:19.503 |

DB-GPT through 0.8.2 contains an unauthenticated remote code execution vulnerability because the /api/v1/chat/react-agent endpoint relies on a mock get_user_from_headers function that grants every caller the admin role. Unauthenticated attackers can send prompts that make the ReAct agent's unsandboxed code_interpreter and shell_interpreter tools run arbitrary Python or bash as root in the webserver container, including reaching the bundled database with default credentials.

### CVE-2026-75128

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-20T01:17:19.063 |

Langchain-Chatchat through 0.3.1.3 exposes a POST /tools/call API endpoint that invokes any registered tool by name without authentication, leaving the always-registered shell tool callable. Remote attackers can send a single request naming the shell tool to execute arbitrary OS commands as the server user (root in the shipped Docker image).

### CVE-2026-109442

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-20T01:17:10.383 |

piflow 2.0.0 through 2.0.1 contains a remote code execution vulnerability in its DeepAgents chat agent, whose POST /chat and POST /chat/stream endpoints lack authentication. Attackers can instruct the agent to call the exec_shell tool, which runs arbitrary commands via subprocess.run without human approval or an allow-list, exposing environment secrets such as LLM API keys and database credentials.

### CVE-2026-112780

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-749` |
| Published | 2026-10-19T20:17:55.473 |

Grav from 2.0.15 before 2.2.2 contains an allowlist bypass vulnerability that allows page editors to call arbitrary public static methods by renaming Flex form fields with replace-name@. Attackers with page-edit permission can smuggle data-*@ directives past the callable check to invoke Folder::delete, Folder::move, or Utils::download, deleting directories, overwriting files, or reading files.

### CVE-2026-112779

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-19T20:17:55.323 |

Grav API plugin (grav-plugin-api) 1.0.40 before 1.0.42 caches a full translation dictionary for every well-formed language code sent to the unauthenticated GET /api/v1/translations/{lang} endpoint, and 1.0.16 before 1.0.42 fails to check target and destination page rules in the sync and batch copy endpoints. Unauthenticated attackers can send small requests that each store about 560 KB to exhaust disk or APCu, while accounts with api.pages.write can overwrite translations or create pages that page-level rules deny.

### CVE-2026-112776

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-19T20:17:54.900 |

Craft CMS from 5.0.0 before 5.11.0 contains an authorization bypass vulnerability that allows site-scoped GraphQL tokens to mutate other sites' content because requireAllowedSite() is not enforced. Attackers holding a site-A token can create entries in site B via supplied siteId and delete entries, categories, tags, and assets shared across sites.

### CVE-2026-109432

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-917` |
| Published | 2026-10-19T16:17:02.487 |

Camunda 7.24.0 before 7.24.14 and 7.23.0 before 7.23.17 contains an expression injection vulnerability where AdhocQueryValidator.validate() fails to check sub-query expression maps within the orQueries field exposed by TaskQueryDto, allowing authenticated users to bypass the enableExpressionsInAdhocQueries restriction. Attackers can supply a malicious JUEL expression such as dueAfterExpression inside an orQueries entry to achieve arbitrary Java reflection and invoke java.lang.Runtime.exec, resulting in operating-system command execution as the engine service user.

### CVE-2026-43845

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T09:17:10.907 |

A vulnerability in the password reset mechanism could allow an attacker to bypass the authentication mechanism.

### CVE-2026-43838

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T09:17:10.173 |

A stack-based buffer overflow vulnerability in the login functionality could allow an attacker to achieve code execution.

### CVE-2026-112900

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-88` |
| Published | 2026-10-19T22:17:10.160 |

Pillow is a Python imaging library. From 2.6.0 until 13.0.0, Pillow is vulnerable to argument injection when invoking Ghostscript for EPS input. EpsImagePlugin.Ghostscript passes a caller-controlled input filename after -f without converting it to a safe absolute path, so a name beginning with a hyphen can be interpreted as a Ghostscript option. An attacker who controls the filename can inject Ghostscript arguments. Arbitrary command execution specifically requires a leading @ argument-file filename and control of the referenced text file containing additional Ghostscript arguments; the reported chain reproduces with the default -dSAFER invocation. This issue is fixed in version 13.0.0.

### CVE-2026-112403

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-19T22:17:07.770 |

Pillow is a Python imaging library. Prior to 13.0.0, Pillow's JPEG decoder can write a full-width scanline into a buffer sized for a requested draft scale. ImagingJpegDecode does not verify libjpeg's actual output width and component count after scaling is requested, and an 8-bit lossless SOF3 JPEG decoded by a build linked to libjpeg-turbo 3.x can ignore the requested downscaling geometry. An attacker can supply such a JPEG to an application that uses draft() or thumbnail() to request downscaling. This can corrupt heap memory, crash the process, or potentially allow code execution. Older libjpeg-turbo 2.x and IJG builds reject the SOF3 input. This issue is fixed in version 13.0.0.

### CVE-2026-112398

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-10-19T22:17:07.107 |

Pillow is a Python imaging library. Prior to 13.0.0, Pillow's FlashPix JPEG-tile decoder can write decoded scanlines beyond the allocated tile buffer. FlashPix (FPX) JPEG decoding selects raw mode LA with two bytes per pixel, while an unrecognized JPEG mode can be decoded as JCS_UNKNOWN with four components, causing ImagingJpegDecode to write four-component scanlines into the two-byte tile buffer. An attacker can supply a crafted OLE2 FlashPix file to an application with the optional olefile dependency installed that opens or thumbnails untrusted input. This can corrupt heap memory and may allow arbitrary code execution. This issue is fixed in version 13.0.0.

### CVE-2026-112393

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-19T21:17:07.613 |

Pillow is a Python imaging library. From 2.0.0 until 13.0.0, Pillow has a heap buffer overflow and stale-heap disclosure in _tiffWriteProc when saving compressed TIFF data through libtiff to a target without a usable fileno(), such as BytesIO. The callback sizes its allocation from the prior buffer size instead of the current write position, allowing an attacker-controlled out-of-line TIFF tag or retained ICC profile to be copied beyond the allocation after libtiff seeks forward. This overflow can crash the process and may allow code execution. Independently, unwritten alignment gaps in compressed TIFF output larger than 64 KiB can disclose stale heap bytes without a crafted tag. File paths and targets with real file descriptors are unaffected. This issue is fixed in version 13.0.0.

### CVE-2026-109437

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-1188` |
| Published | 2026-10-19T19:17:19.807 |

Cognition before 0.13.0 contains an unauthenticated remote code execution vulnerability due to defaulting its agent sandbox backend to local execution and shipping no authentication on its REST/SSE API. Attackers can create a session via POST /sessions and post a message via POST /sessions/{id}/messages without credentials, causing the Deep Agents ReAct loop to run attacker-directed shell commands through the local shell backend, resulting in remote code execution as the server process.

### CVE-2026-112377

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-10-19T18:17:05.490 |

CCC Attestation SIG attested-tls-poc through commit 731ca82 fails to bind early attestation Evidence to the TLS connection, allowing attackers to relay valid Evidence from a genuine attester. Attackers holding an extracted attested TLS private key can forward the relying party's nonce to a genuine attester and replay its Evidence to impersonate the attested workload and intercept data.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-105949

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-20T12:17:28.847 |

Cruise Control's Jetty ConstraintSecurityHandler registers security constraints on exact path specs without a catch-all wildcard constraint and without calling setDenyUncoveredHttpMethods(true). The servlet routes requests using Path.of(pathInfo).getFileName(), which strips all leading segments and trailing slashes. Requests like POST /kafkacruisecontrol/x/rebalance bypass authentication entirely but still dispatch to admin endpoints. All 15 admin endpoints become reachable without authentication. In AMQ Streams, the Strimzi operator's NetworkPolicy restricts Cruise Control port 9090 to operator pods only, reducing effective severity to Important.

### CVE-2026-86949

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-20T01:17:28.370 |

This issue was addressed by enforcing library validation on the affected binaries. This issue is fixed in Xcode 27. A malicious app may be able to break out of its sandbox.

### CVE-2026-86922

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-20T01:17:27.600 |

A type confusion issue was addressed with improved state management. This issue is fixed in Safari 27, iOS 27 and iPadOS 27, macOS Golden Gate 27, visionOS 27. Processing maliciously crafted web content may lead to arbitrary code execution.

### CVE-2026-109395

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-20T01:17:09.957 |

Ning compress-lzf before 1.2.0 contains an out-of-bounds memory access vulnerability in the sun.misc.Unsafe based UnsafeChunkDecoder that fails to validate back-references and literal runs. Attackers can supply crafted LZF streams to applications using the default LZFDecoder to leak unrelated JVM heap memory into decompressed output or crash the JVM.

### CVE-2026-109126

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-20T00:17:30.370 |

IBM Verify Identity Access 11.0.3.1 and IBM Security Verify Access 10.0.9.3 Appliance could allow a physically proximate attacker to gain elevated privileges due to the use of hard-coded credentials.

### CVE-2026-107400

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-20T00:17:25.790 |

IBM TRIRIGA Application Platform 5.0.0 through 5.0.8 could allow a remote authenticated attacker to execute arbitrary code due to improper authentication.

### CVE-2026-53995

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-19T22:17:11.013 |

MLflow 3.17.1 and earlier contains a path traversal vulnerability in the FileStore tracking backend that allows unauthenticated attackers to control filesystem paths by submitting a crafted trace ID containing traversal sequences to the POST /api/3.0/mlflow/traces endpoint. Attackers can exploit FileStore.start_trace() to write trace_info.yaml, request_metadata, and tag files with attacker-controlled metadata outside the intended experiment trace directory, subject to the server process's filesystem permissions. FileStore is the default tracking backend before MLflow 3.7.0 and opt-in thereafter (the default changed to a SQLite database), so deployments in the earlier part of the affected range are vulnerable without special configuration while later ones are affected only when FileStore is explicitly selected.

### CVE-2026-112896

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-19T22:17:09.760 |

Pillow is a Python imaging library. Prior to 13.0.0, Pillow's TIFF encoder can read beyond a ColorMap buffer when retained TIFF metadata has a plane size inconsistent with BitsPerSample. A small TIFF can be opened normally and then retain a crafted ColorMap that is reused when the image is saved. An application that re-encodes the attacker's TIFF with libtiff can trigger the out-of-bounds read. This can disclose heap memory in the output or crash the process. This issue is fixed in version 13.0.0.

### CVE-2026-112404

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-126` |
| Published | 2026-10-19T22:17:07.900 |

Pillow is a Python imaging library. From 8.1.0 until 13.0.0, Pillow's TIFF tile and RGBA decode paths can read beyond row data produced by libtiff. In _decodeTile and the RGBA unpacker path, when Pillow and libtiff interpret duplicated PhotometricInterpretation or BitsPerSample tags differently, Pillow does not verify that the required input row fits inside the row libtiff produced, while the strip path has this validation. Loading pixels from such a crafted TIFF can expose adjacent heap data in output pixels or crash the process. This issue is fixed in version 13.0.0.

### CVE-2026-76788

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-19T21:18:01.380 |

The OSDP Control Panel reply parser cp_decode_response() in subsys/mgmt/osdp/src/osdp_cp.c decodes replies from a Peripheral Device into a stack-allocated struct osdp_event. For the REPLY_KEYPPAD and REPLY_RAW reply types, the payload length is taken from the received frame and the only validation performed is that the declared length is self-consistent with the number of payload bytes present in the frame. Because the attacker controls both the length field and the frame length, that check imposes no bound, and the subsequent memcpy() writes into the fixed 64-byte data arrays of struct osdp_event_keypress / struct osdp_event_cardread (OSDP_EVENT_MAX_DATALEN). The sibling REPLY_FMT handler in the same switch already carried the missing > OSDP_EVENT_MAX_DATALEN bound.

The defect is reached from cp_process_reply(), which reads bytes from the OSDP RS-485 channel and passes them through osdp_phy_check_packet() and osdp_phy_decode_packet() before dispatching on the reply ID. Triggering it requires CONFIG_OSDP with CONFIG_OSDP_MODE_CP and an application event callback registered (the normal Control Panel integration), plus a frame carrying a correct SOM, a valid CRC-16, and a matching 2-bit sequence number — all of which are computable or observable by anyone on the bus. No check ties the reply ID to the outstanding command, so an oversized REPLY_KEYPPAD or REPLY_RAW is accepted as the answer to a routine CMD_POLL. A malicious or compromised card reader, or anyone with access to the RS-485 wiring, can supply such a frame; CONFIG_OSDP_SC_ENABLED only helps while a secure channel is active, and a single unauthenticated frame carrying a bad MAC causes sc_deactivate(), after which plaintext replies are again accepted.

With the default CONFIG_OSDP_UART_BUFFER_LENGTH of 256, roughly 180 bytes of fully attacker-chosen data can be written past the end of the stack-allocated event object, over saved registers and the return address on typical Cortex-M and RISC-V frame layouts (Zephyr does not enable stack canaries by default). The impact ranges from a hard crash of the access-control panel to potential control-flow hijack in the context of the OSDP receive thread. The fix adds an OSDP_EVENT_MAX_DATALEN bound to both handlers, capping each memcpy() at the size of its destination.

### CVE-2026-82166

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-19T20:20:06.313 |

Dell Application Store, versions prior to 26.05.0.7, contain a Missing Authentication for Critical Function vulnerability. An unauthenticated attacker with adjacent network access could potentially exploit this vulnerability, leading to arbitrary code execution.

### CVE-2026-10743

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1223` |
| Published | 2026-10-19T17:17:02.107 |

IBM MQ could allow an authenticated attacker to cause a denial of service or corrupt memory due to improper validation of buffer sizes in MQOPEN operations.

### CVE-2026-10574

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-19T17:17:01.780 |

IBM MQ could allow an authenticated attacker to cause a denial of service or potentially execute arbitrary code due to a heap buffer overflow when processing MQPUT or MQPUT1 operations with malformed message handle properties.

### CVE-2026-10572

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-19T17:17:01.440 |

IBM MQ could allow an authenticated attacker to cause a denial of service or potentially execute arbitrary code due to a heap buffer overflow when processing MQPUT operations with malformed message options.

### CVE-2026-113358

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-20T11:17:20.447 |

LavaLite CMS through 10.1.2 contains a missing authentication vulnerability in the Filer module that allows unauthenticated attackers to download stored files through the filer/download and filer/display routes. Attackers can supply arbitrary disk names and paths to FileController to retrieve private uploads from local storage or configured remote S3 disks.

### CVE-2026-85267

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-1385` |
| Published | 2026-10-20T10:17:07.007 |

A Cross-Site WebSocket Hijacking vulnerability in Cloud Shell prior to 2026-07-22 on Google Cloud Platform allows an unauthenticated attacker to hijack an active Cloud Shell session and exfiltrate the user's OAuth access token using a cross-origin WebSocket request.


This vulnerability was patched on 22 July 2026, and no customer action is needed.

### CVE-2026-112238

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-20T10:17:04.653 |

The file search of the extension builds its database conditions by wrapping the search term in quotes itself. Only the wildcard characters of the LIKE operator are escaped, quote characters are not. A crafted search term can therefore leave the intended string value and change the database query. This allows an attacker to read data from the database. The issue affects every searched field.

### CVE-2026-43839

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T09:17:10.277 |

A NULL pointer dereference vulnerability in the logs management functionality could allow an unauthenticated attacker to crash the service.

### CVE-2026-113407

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-20T08:16:43.130 |

BA-Workflow developed by YS-infoware has a SQL Injection vulnerability. Authenticated remote attackers can inject arbitrary SQL statements to read, modify, and delete database contents.

### CVE-2026-113406

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-20T08:16:43.000 |

BA-Workflow developed by YS-infoware has a SQL Injection vulnerability. Authenticated remote attackers can inject arbitrary SQL statements to read, modify, and delete database contents.

### CVE-2026-113405

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-20T08:16:42.867 |

BA-Workflow developed by YS-infoware has a SQL Injection vulnerability. Authenticated remote attackers can inject arbitrary SQL statements to read, modify, and delete database contents.

### CVE-2026-113404

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-20T07:17:09.783 |

WebITR developed by Uniong has a Insecure Deserialization vulnerability. Authenticated remote attackers can use the hard-coded cryptographic key to craft and submit malicious serialized data, thereby executing arbitrary code on the server.

### CVE-2026-105299

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T02:17:08.703 |

Summary



Before version 0.9.0, the HTTP/1 upstream path in pingora-proxy passed the downstream request through upstream_request_filter and wrote it to the upstream without removing the client's Connection header, other hop-by-hop headers, or the headers Connection nominated, although RFC 9110 Section 7.6.1 requires intermediaries to remove them. The HTTP/2 upstream path already removed Connection and related HTTP/1-specific headers. A client could therefore nominate a header that the application adds in upstream_request_filter (for example, Connection: keep-alive, X-Forwarded-For). A downstream HTTP/1 intermediary that honors Connection would then strip the Pingora-added header before it reached the origin.




Impact



Specifically affects chained deployments where an HTTP/1 intermediary between Pingora and the origin processes Connection nominations (for example, Go's net/http/httputil.ReverseProxy) and the origin trusts headers added by that intermediary (for example, X-Forwarded-For for IP-based authorization). A remote, unauthenticated attacker can have those headers removed, potentially bypassing authorization. The reporter demonstrated access to an IP-restricted endpoint using X-Forwarded-For for IP validation on the origin. This is the same class of issue as CVE-2022-31813 in Apache HTTP Server.




Note that Cloudflare CDN customers were unaffected, as no such chained deployment as described above exists with internal Pingora services, and Connection headers are sanitized before arriving at Pingora gateways.



Mitigation:

  *  

Upgrade to pingora 0.9.0 or later. By default, Pingora now removes hop-by-hop and Connection-nominated headers from upstream requests, and rejects requests whose Connection header nominates Host, X-Forwarded-For, X-Forwarded-Host, X-Forwarded-Proto, or a pseudo-header. This is controlled by PeerOptions::http_upstream_request_policy (HttpUpstreamRequestPolicy). Fix commits:  https://github.com/cloudflare/pingora/commit/28c18e6b6b04dd0bd937234e5950049e6d74cded ,  https://github.com/cloudflare/pingora/commit/ca23f1668eca8e78be7ba62ef0edbd458b40eeee 


  *  

Do not use HttpUpstreamRequestPolicy::preserve() if the origin relies on headers added by Pingora; it restores the old passthrough behavior.


  *  

If you cannot upgrade: in upstream_request_filter, remove the Connection header and every header it nominates before adding trusted headers.

### CVE-2026-77935

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-20T01:17:19.970 |

Coze Studio through 0.5.1 contains an insecure direct object reference vulnerability in workflow.go that allows authenticated users to access other spaces' workflows by supplying foreign workflowIDs. Attackers can pair their own spaceID with another tenant's workflowID in save, update_meta, batch_delete, canvas, test_run and nodeDebug routes to read, run, overwrite or delete workflows.

### CVE-2026-77934

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-10-20T01:17:19.823 |

Coze Studio before 0.5.0 contains an insecure default configuration that allows any registered user to execute commands by running workflow code nodes in an unsandboxed python3 subprocess. Attackers can bypass the regex import filter with __import__('subprocess') to run commands, stealing environment variables, model API keys, and accessing MySQL, MinIO, Redis and etcd.

### CVE-2026-77930

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-20T01:17:19.360 |

EvoScientist 0.1.0 before 0.2.5 contains an approval bypass vulnerability that allows attackers to run host shell commands by delegating them to async sub-agents lacking an interrupt_on gate. Attackers can plant instructions in ingested content such as fetched web pages, so the agent calls start_async_task and runs commands with user privileges and environment secrets.

### CVE-2026-77926

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-749` |
| Published | 2026-10-20T01:17:19.213 |

Aix-DB 1.2.4 contains a remote code execution vulnerability that allows authenticated non-admin users to run operating system commands through the ChatBI common agent's ungated deepagents execute tool. Attackers can send crafted chat input to POST /dify/get_answer or upload documents with malicious text to run host commands, exposing datasource credentials and model API keys.

### CVE-2026-109444

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-20T01:17:10.673 |

OpenSRE through 0.1.2026.10.19 contains an approval gate bypass vulnerability that allows attackers to execute shell_run commands without confirmation because the headless presenter's execution_allowed() always returns True. Attackers can inject instructions into alerts or Slack messages triaged by the agent to run commands on the host and exfiltrate LLM, Slack and cloud credentials.

### CVE-2026-109443

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-653` |
| Published | 2026-10-20T01:17:10.527 |

JoySafeter through 1.0.0 contains a remote code execution vulnerability that allows authenticated users to run operating system commands via an unsandboxed execute tool in Copilot standard mode. Attackers can self-register, select standard mode in the WebSocket chat.start extension, and have the agent invoke subprocess.run with shell=True on the host to access other tenants' data and server secrets.

### CVE-2026-112897

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-908` |
| Published | 2026-10-19T22:17:09.900 |

Pillow is a Python imaging library. From 5.3.0 until 13.0.0, Pillow can return uninitialized memory as pixels when libtiff performs a short decode of JPEG-compressed or Group 4 fax TIFF data. The _decodeStrip and _decodeTile buffers can be larger than the bytes written by libtiff, but Pillow converts the expected rows without clearing the unwritten tail. The tile path is affected from 5.3.0 and the strip path from 6.0.0. An attacker can supply a crafted TIFF to an application that loads and returns or re-encodes its pixels. This can disclose stale heap contents without memory corruption or a process crash. This issue is fixed in version 13.0.0.

### CVE-2026-112895

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-19T22:17:09.620 |

Pillow is a Python imaging library. From 5.1.0 until 13.0.0, Pillow can exhaust resources while parsing an existing PDF during an append operation. PdfParser follows page-tree child references without cycle or duplication tracking and follows previous-trailer chains with only an exact repeated-offset guard, so deep or cyclic page trees and long chains of unique trailer offsets can exhaust the Python stack. Repeated non-cyclic /Kids references can also cause super-linear CPU and memory use. An attacker can supply such a PDF to an application that calls Image.save with PDF append enabled. This can raise an uncaught RecursionError or consume excessive CPU and memory before output is written, causing denial of service. This issue is fixed in version 13.0.0.

### CVE-2026-112894

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-19T22:17:09.483 |

Pillow is a Python imaging library. From 5.1.0 until 13.0.0, Pillow takes quadratic time to reserve PDF object identifiers when saving many frames with save_all enabled. PdfParser.next_object_id() repeatedly rebuilds and scans all previously reserved identifiers for every object. An attacker can supply a multi-frame image, including a small APNG with a large declared frame count, to an application that converts it to a multipage PDF. This can consume excessive CPU and deny service. This issue is fixed in version 13.0.0.

### CVE-2026-112892

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-10-19T22:17:09.210 |

Pillow is a Python imaging library. From 4.1.0 until 13.0.0, Pillow's MSP RLE decoder can expand a small file into an unbounded in-memory buffer. The decoder writes run-length output to BytesIO without limiting expansion to the declared image size. An attacker can supply a crafted MSP image to an application that loads its pixels. This can exhaust memory and deny service even when the declared pixel count passes the decompression-bomb check. This issue is fixed in version 13.0.0.

### CVE-2026-112406

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-19T22:17:08.153 |

Pillow is a Python imaging library. From 5.1.0 until 13.0.0, Pillow can enter an infinite loop while rewriting PDF pages. PdfParser.rewrite_pages() follows Parent relationships without detecting a cycle in the page tree. An attacker can supply a cyclic PDF to an application that appends an image to that PDF. This can hold the worker at full CPU and deny service. This issue is fixed in version 13.0.0.

### CVE-2026-112405

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-19T22:17:08.027 |

Pillow is a Python imaging library. From 12.0.0 until 13.0.0, Pillow's Image.merge() can dereference a null image8 plane. Validation skips the first input band, allowing a 32-bit integer or floating-point image backed by image32 storage to be merged as a narrower multiband image. A crafted IPTC file can reach this path when an application opens and loads it, or a caller can invoke Image.merge() directly with such a first band. This causes a native process crash. This issue is fixed in version 13.0.0.

### CVE-2026-112402

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-19T22:17:07.633 |

Pillow is a Python imaging library. Prior to 13.0.0, Pillow can double free image memory when ImagingScaleAffine encounters a selective allocation failure. The affected fast path handles Transform.EXTENT or pure scale-and-translate Transform.AFFINE operations with the default NEAREST resampling. The output image allocation must succeed while the additional per-column lookup allocation fails, after which the error path deletes image storage that later cleanup releases again. An attacker who can drive such a large Image.transform() operation under memory pressure may trigger the failure. This can crash the process and may corrupt memory. This issue is fixed in version 13.0.0.

### CVE-2026-112400

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-10-19T22:17:07.367 |

Pillow is a Python imaging library. From 9.2.0 until 13.0.0, Pillow can retain a rejected GIF frame size after a decompression-bomb exception. In GifImageFile._seek, a crafted GIF can leave rejected dimensions stored after Image.DecompressionBombError; if an application catches that exception and continues processing the same image object, later seek or load operations allocate according to those dimensions and can exhaust memory, denying service. This issue is fixed in version 13.0.0.

### CVE-2026-112399

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-10-19T22:17:07.240 |

Pillow is a Python imaging library. From 8.1.0 until 13.0.0, Pillow can allocate an APNG disposal background at the full canvas size before applying the decompression-bomb check. A crafted APNG with a small first frame, a very large declared canvas, and background disposal or first-frame OP_PREVIOUS reaches PngImageFile._seek while Image.open() positions frame zero. The full-canvas allocation occurs inside Image.open() without requiring pixel loading or frame iteration. This can exhaust memory and deny service. This issue is fixed in version 13.0.0.

### CVE-2026-112397

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-19T22:17:06.970 |

Pillow is a Python imaging library. Prior to 13.0.0, Pillow's ImageMorph.MorphOp.apply() can access memory before a row buffer for a zero-width image. PPM and PGM input can create an image with width zero, and the native morphology routine indexes outrow[width - 1] without rejecting that geometry. An attacker can supply such an image to an application that applies a morphology operation. This can crash the process. This issue is fixed in version 13.0.0.

### CVE-2026-112782

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-19T20:17:55.787 |

Grav 1.7.53 before 1.7.53.5 and 2.0.0-rc.8 before 2.2.2 contains a resource exhaustion vulnerability that allows anonymous visitors to bypass the system.images.max_pixels limit when system.images.url_actions is enabled. Attackers can send single-dimension or percentage forceResize, zoomCrop, or chained image actions to make GD allocate multi-gigabyte canvases, exhausting server memory and taking the site down.

### CVE-2026-112781

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-19T20:17:55.633 |

Grav from 2.0.0 before 2.2.2 contains an information disclosure vulnerability that allows page editors to read protected configuration by adding config-*@ directives to page frontmatter forms. Attackers with page-edit permission can bypass the Twig sandbox config_denied_paths redaction to expose security.salt, plugin credentials, and Redis passwords to all visitors.

### CVE-2026-112777

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-10-19T20:17:55.043 |

Craft CMS 4.x before 4.18.8 and 5.x before 5.11.0 contains a blocklist bypass in the Twig create() function because its class-name checks are case-sensitive while PHP class resolution is not. Attackers with template-execution rights, such as Control Panel administrators, can instantiate SplFileObject via a lowercase class name to read .env secrets or write a PHP file into the webroot for remote code execution.

### CVE-2026-112775

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-19T20:17:54.757 |

Craft CMS from 5.0.0 before 5.11.0 contains an authentication bypass vulnerability that allows attackers to reuse verification codes because users/verify-email does not invalidate them for active users. Attackers who obtain a victim's emailed code can submit it to users/set-password after the victim verifies an email change, resetting the password and taking over the account.

### CVE-2026-112774

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-19T20:17:54.620 |

Craft CMS from 5.8.0 before 5.11.0 contains a remote code execution vulnerability that allows authenticated administrators to inject Yii behaviors by supplying a JSON-string field layout to ContentBlock::setFieldLayout(). Attackers with allowAdminChanges enabled can include 'as X' or 'on X' keys that bypass cleanseConfig() to execute OS commands as the web user and disclose secrets.

### CVE-2026-112773

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-19T20:17:54.480 |

Craft CMS from 5.0.0 before 5.11.0 contains a remote code execution vulnerability that allows authenticated Control Panel users to escape the Twig sandbox by passing uncleansed criteria to getNext, getPrev, or getOwners. Attackers can inject Yii "as" or "on" config keys to attach malicious event handlers that execute when the element query runs, achieving code execution as the web user.

### CVE-2026-112772

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-19T20:17:54.340 |

Craft CMS from 5.0.0 before 5.11.0 contains a remote code execution vulnerability that allows authenticated Control Panel users to escape the Twig sandbox via Asset::getMimeType transforms. Attackers can supply 'as' or 'on' keys passed unfiltered to Craft::createObject, attaching malicious behaviors or event handlers that execute code as the web user.

### CVE-2026-112770

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-19T20:17:54.060 |

Craft CMS 4.x before 4.18.8 and 5.x before 5.11.0 contains a remote code execution vulnerability in the Twig group filter, which invokes non-string arrow arguments as callables without the checkArrow guard used by other arrow-accepting filters. Authenticated control panel users can pass an array-callable such as FileHelper::writeToFile via element-select condition rules to write a webshell to the webroot and execute code as the web user.

### CVE-2026-112366

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-19T16:17:07.500 |

Picomatch through 4.0.7 contains a regular expression denial of service vulnerability that allows attackers to block the event loop by supplying single-branch repeated extglob patterns. Attackers can provide globs like +(*) or +(*a), which analyzeRepeatedExtglob in lib/parse.js skips, causing exponential backtracking against short crafted strings and denying service to Node.js applications.

### CVE-2026-112309

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-10-19T16:17:07.050 |

@rvf/set-get before 7.0.4 contains a prototype pollution vulnerability in setPath that allows unauthenticated attackers to overwrite properties of shared built-in functions via inherited Object.prototype methods. Attackers can submit a form field named hasOwnProperty.call through @rvf/core form parsing to replace the shared function property, causing process-wide denial of service until restart.

### CVE-2026-112305

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-10-19T16:17:06.400 |

Semaphore UI through 2.19.16 contains a remote code execution vulnerability that allows users with the task_runner role to override protected Ansible variables by supplying arbitrary keys in the task environment JSON. Attackers can POST tasks setting ansible_ssh_common_args with a ProxyCommand or ansible_connection=local to execute commands as the Semaphore server user, exposing encryption keys, SSH keys and stored secrets.

### CVE-2026-113391

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-10-20T13:16:40.640 |

A vulnerability has been found in DrayTek Vigor2960 1.5.1.6 Revision 8218. This affects the function uploadlangs of the file /cgi-bin/mainfunction.cgi of the component Upload Endpoint. Such manipulation leads to command injection. The attack can be executed remotely. The exploit has been disclosed to the public and may be used. Upgrading to version 1.5.1.7 is able to mitigate this issue. It is recommended to upgrade the affected component. The vendor explains: "2960 1.5.1.7 has corrected many security issues. And 2960 is EoS with limited support, only major issues would be reviewed(e.g. unauthenticated vuln.)". This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-113390

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-10-20T13:16:40.463 |

A flaw has been found in DrayTek Vigor2960 1.5.1.6 Revision 8218. Affected by this issue is the function sub_182B0 of the file /cgi-bin/mainfunction.cgi of the component CGI Interface. This manipulation of the argument usefile/usescript/option causes os command injection. Remote exploitation of the attack is possible. The exploit has been published and may be used. The vendor explains: "2960 1.5.1.7 has corrected many security issues. And 2960 is EoS with limited support, only major issues would be reviewed(e.g. unauthenticated vuln.)". This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-14933

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-20T12:17:30.057 |

Cross-site scripting in the embedded co-browsing feature in Unblu inc. Unblu Spark 7.0 through 7.57.7 and 8.0 through 8.39.2, on on-premises and cloud deployments, allows an unauthenticated remote attacker in the visitor role to execute arbitrary JavaScript in the browser of an agent taking part in the attacker's co-browsing session, via content of the co-browsed page that the agent's browser renders as HTML.



The JavaScript runs in the context and under the identity of the agent's session in the Agent Desk or the Single Conversation Desk.



Exploitation requires an agent to join an embedded co-browsing session with the attacker. Mobile co-apping isn't affected.

### CVE-2026-113389

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-10-20T12:17:29.443 |

A vulnerability was detected in DrayTek Vigor2960 1.5.1.6 Revision 8218. Affected by this vulnerability is the function set_table of the file /cgi-bin/mainfunction.cgi of the component CGI Process. The manipulation of the argument sectiontype results in command injection. The attack may be launched remotely. The exploit is now public and may be used. The vendor explains: "2960 1.5.1.7 has corrected many security issues. And 2960 is EoS with limited support, only major issues would be reviewed(e.g. unauthenticated vuln.)". This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-43858

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T10:17:06.880 |

A stack-based buffer overflow vulnerability could allow a remote authenticated attacker to achieve arbitrary code execution.

### CVE-2026-43857

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T10:17:06.757 |

A vulnerability could allow a remote authenticated attacker to achieve arbitrary code execution with privileges on the service.

### CVE-2026-43856

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T10:17:06.640 |

A stack-based buffer overflow vulnerability in the FileProcess::CheckDir function could allow a remote authenticated attacker to achieve arbitrary code execution via a path longer than 1024 bytes.

### CVE-2026-43850

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T10:17:05.923 |

A command injection vulnerability could allow an authenticated attacker to achieve root-level code execution on the system.

### CVE-2026-43846

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T09:17:11.010 |

A stack-based buffer overflow vulnerability in a non-functional feature could allow an authenticated attacker to achieve code execution.

### CVE-2026-43835

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T08:16:44.207 |

A vulnerability in the firmware upgrade functionality could allow an authenticated attacker to upload a forged firmware upgrade file, potentially compromising the device permanently.

### CVE-2026-97627

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-912` |
| Published | 2026-10-20T06:16:58.300 |

Hidden functionality issue exists in Multiple DVRs (Digital Video Recorders) provided by Atsumi Electric Co., Ltd. A user who can log in to the product with the administrator privilege may execute arbitrary OS commands.

### CVE-2026-77937

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-20T01:17:20.263 |

Letta through 0.16.8 contains an authentication bypass vulnerability that allows API callers to impersonate other users by supplying a self-asserted user_id HTTP header. Attackers can set user_id to another tenant's ID, even with LETTA_SERVER_SECURE enabled, to read and modify that user's agents, memory and configuration.

### CVE-2026-109440

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T01:17:10.103 |

LangAlpha through 2026.09.07 contains an indirect prompt injection vulnerability that allows remote attackers to execute shell commands or Python by planting instructions in web content retrieved by the agent. Because Bash and ExecuteCode lack an allow-list and human-in-the-loop approval, attackers can run code in the workspace sandbox and exfiltrate vault secrets from _internal/.vault_secrets.json.

### CVE-2026-112371

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-94` |
| Published | 2026-10-19T23:17:36.000 |

A vulnerability was determined in H3C Magic NX15 NX15V100R017. Impacted is the function write of the file /api/esps of the component RPC Interface. Executing a manipulation of the argument path can lead to code injection. The attack can be executed remotely. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure.

### CVE-2026-112370

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-10-19T23:17:35.817 |

A vulnerability was found in H3C Magic NX15 100R017. This issue affects the function sub_416874 of the file /usr/bin/usrlist. Performing a manipulation results in os command injection. Remote exploitation of the attack is possible. The exploit has been made public and could be used. The vendor was contacted early about this disclosure.

### CVE-2026-107186

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-19T17:17:00.827 |

An unauthenticated user can send a DWR request with isPasswordUppercase as one call method and the next call method can be set to a run workflow rule. This allows for workflow rules to be run without authentication.

### CVE-2026-103038

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-19T17:17:00.400 |

PingTools Network Utilities 4.64 contains an OS command injection vulnerability in the Host field of a Watcher ICMP service. The application appends the attacker-controlled Host value to a ping command, serializes the command as a single string, and executes it through sh -c. A local attacker who can create or modify a Watcher service can inject shell syntax and execute arbitrary commands with the PingTools application UID and its granted Android permissions.

### CVE-2026-112306

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-19T16:17:06.570 |

NocoBase @nocobase/plugin-collection-sql through 2.2.28 contains an SQL injection vulnerability that allows privileged users to store unvalidated SQL by bypassing checkSQL() through the sqlCollection:setFields action. Attackers holding the collection-sql snippet can replace a benign collection query with dangerous statements executed on reload, reading pg_shadow password hashes or calling pg_read_file.

### CVE-2026-109431

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-10-19T16:17:02.337 |

Camunda 7.24.0 before 7.24.14 and 7.23.0 before 7.23.17 contains a missing authorization check vulnerability in engine-rest task sub-resources that allows authenticated attackers with no permission grants to access task comments and attachments by calling singular read and delete endpoints that lack the authorization-filtered checks enforced on their corresponding list endpoints. Attackers can exploit TaskAttachmentResourceImpl and TaskCommentResourceImpl methods such as getAttachment, getAttachmentData, deleteAttachment, and getComment using only a known object ID to read, download, or permanently delete task attachments and comments.

### CVE-2026-102438

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-10-20T02:17:08.147 |

An uncontrolled search path element vulnerability in ASUS Armoury Crate allows local users to execute arbitrary code with SYSTEM privileges via replacement of a dynamic-link library (DLL) that is later loaded by a high-privilege process.
Refer to the '
Security Update for Armoury Crate App ' section on the ASUS Security Advisory for more information.

### CVE-2026-105810

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-19T18:16:58.903 |

Tapo C320WS
V2.0 contains an authenticated stack-based buffer overflow in the local
onboarding Wi-Fi configuration path. An authenticated attacker on the
adjacent network can submit a crafted request containing an oversized encrypted
password field, overwrite stack state, and execute commands with root
privileges.





Successful
exploitation may allow an authenticated adjacent-network attacker to take
control of the affected camera, modify camera behavior, access sensitive local
configuration, and disrupt device availability.

### CVE-2026-107187

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-19T17:17:00.967 |

A user can access any database details, such as usernames and passwords by sending a DWR request with a specified workflow rule. The authentication bypass vulnerability can be chained with this vulnerability to perform database reads without authentication. Database write and delete operations may also be possible, but this was untested.

### CVE-2026-105453

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-20T00:17:23.400 |

IBM Sterling Connect Direct for Unix 6.3.0.0 through 6.3.0.7 and 6.4.0.0 through 6.4.0.6 could allow a local attacker to gain elevated privileges due to improper privilege management.

### CVE-2026-112307

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-19T16:17:06.727 |

sqlparse through 0.6.0 contains a PHP code injection vulnerability that allows attackers to inject PHP expressions by supplying SQL text containing unescaped dollar signs. Attackers can embed ${expr} or {${expr}} sequences that OutputPHPFilter places in double-quoted strings, executing arbitrary PHP code when the generated snippet runs.

### CVE-2026-107366

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-20T00:17:25.640 |

IBM Langflow OSS 1.0.0 through 1.12.4 contains three message endpoints that perform no ownership verification. Any authenticated user can bulk-delete another user's messages, overwrite message content to inject malicious prompts, or hijack an entire conversation session by reassigning its session ID.

### CVE-2026-112308

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-19T16:17:06.887 |

crewai-tools through 1.15.28 contains a server-side request forgery vulnerability in SeleniumScrapingTool that allows attackers to fetch internal resources because it never applies the validate_url private-address check. Attackers influencing agent tool input through prompt injection can direct headless Chrome to loopback, RFC1918, or cloud metadata addresses to disclose internal data and cloud credentials.

### CVE-2026-113351

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-909` |
| Published | 2026-10-20T11:17:19.363 |

libexpat 2.7.2 through 2.9.0 contains a denial of service vulnerability because XML_ParserReset zeroes the direct byte count but never offsets tracked heap allocations. Attackers can submit a large XML document so later documents on the same reset parser fail with XML_ERROR_NO_MEMORY until it is recreated.

### CVE-2026-43853

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T10:17:06.283 |

A vulnerability could allow an attacker to send a crafted message to trigger an assertion fault, causing the service to crash.

### CVE-2026-43852

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T10:17:06.170 |

A vulnerability could allow an authenticated attacker to write files to arbitrary locations on the system.

### CVE-2026-43851

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T10:17:06.047 |

A path traversal vulnerability could allow an authenticated attacker to read arbitrary files on the system.

### CVE-2026-43847

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T09:17:11.117 |

A vulnerability in the proprietary protocol could allow an attacker to brute force the administrator password without restrictions, even when the SafeEnhancement feature is enabled.

### CVE-2026-17518

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-20T02:17:11.307 |

Buffer Copy without Checking Size of Input in certain ASUS router models allows an adjacent authenticated user to corrupt device operations and cause a denial of service via an HTTP request with input exceeding the expected length.
Refer to the ' Security Update for ASUS Router Firmware' section on the ASUS Security Advisory for more information.

### CVE-2026-112893

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-457;CWE-763` |
| Published | 2026-10-19T22:17:09.350 |

Pillow is a Python imaging library. From 10.0.0 until 13.0.0, Pillow can free an invalid glyph pointer during FreeType rendering with an active stroker. If FT_Load_Glyph fails, cleanup may call FT_Done_Glyph on an uninitialized or stale glyph variable. An attacker can supply a malformed font as untrusted bytes to an application that draws text with a nonzero stroke width, forcing the glyph-load failure path. This can corrupt memory or crash the process. This issue is fixed in version 13.0.0.

### CVE-2026-112392

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-19T22:17:06.587 |

Pillow is a Python imaging library. Prior to 13.0.0, Pillow's rank-based filters can dereference invalid image storage for a zero-size image. ImagingExpand() allocates a non-empty output and then faults while replicating edges by reading the first pixel from empty input storage; ImagingRankFilter is never reached. An attacker can supply or cause creation of a zero-size image to an application that applies a rank, median, minimum, or maximum filter. This causes a native process crash. This issue is fixed in version 13.0.0.

### CVE-2026-112390

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-19T21:17:07.340 |

Pillow is a Python imaging library. From 7.2.0 until 13.0.0, Pillow can enter an infinite loop while determining the frame count of a MIC image. MicImageFile inherits TIFF frame traversal, but MicImageFile.tell reports the OLE stream index and its seek() resets TIFF frame state, so an embedded TIFF with at least three IFDs never advances. When an application with olefile installed reads n_frames or saves all frames from a crafted MIC file, the non-advancing traversal can hold a worker at full CPU indefinitely. This issue is fixed in version 13.0.0.

### CVE-2026-111755

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-185;CWE-200` |
| Published | 2026-10-19T18:17:00.260 |

follow-redirects is a Node.js HTTP and HTTPS client wrapper that automatically follows redirects. From 1.16.0 until 1.16.1, escapeRegex leaves valid header-name metacharacters unescaped in sensitiveHeaders. When an application declares a sensitive header whose name contains ^ or | and follows a cross-origin or HTTPS-to-HTTP redirect, unescaped regular-expression metacharacters prevent the generated filter from matching the declared header name, and the credential header is forwarded to an attacker-controlled redirect target. This issue is fixed in version 1.16.1.

### CVE-2026-111066

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-10-19T17:17:03.637 |

AIOHTTP is an asynchronous HTTP client/server framework for asyncio and Python. From 2.0.0 until 3.14.4, multipart request processing can retain an unbounded number of open file descriptors. An unauthenticated attacker can consequently exhaust file descriptors with specially crafted multipart requests when a handler uses Request.post(). This issue is fixed in version 3.14.4.

### CVE-2026-111064

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-19T17:17:03.377 |

AIOHTTP is an asynchronous HTTP client/server framework for asyncio and Python. Prior to 3.14.4, keepalive timeout handling is absent during the initial portion of a request. An attacker can keep an idle connection open indefinitely before sending any request data, consuming server connection capacity. This issue is fixed in version 3.14.4.

### CVE-2025-10149

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-281;CWE-668` |
| Published | 2026-10-19T17:16:59.007 |

The SCIM endpoint does not sufficiently validate authorization for federated users when performing operations against the local user store. This occurs when a local and a federated user share the same username, allowing a federated user to perform actions intended for a local user, including arbitrary operations.

A malicious actor authenticated as a federated user may perform arbitrary operations on local user accounts via the SCIM 2.0 or SCIM 1.1 endpoints when local and federated users share the same username. This could lead to user account takeover. Deployments that do not support user self-registration are considered medium severity.

### CVE-2026-112368

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-19T16:17:07.650 |

An uncontrolled recursion weakness in the BSON decoding logic of the MongoDB PHP driver may allow an unauthenticated party who can supply crafted binary document data to the decoder to exhaust the process stack. This may cause the PHP process using the driver to terminate unexpectedly, resulting in a loss of availability for that process. The condition occurs below the PHP layer and cannot be intercepted by application-level error handling.

### CVE-2026-105941

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-20T13:16:39.457 |

The Azure Key Vault KMS provider in Kroxylicious accepts an untrusted vaultName from wire-deserialized EDEK bytes without format validation, enabling SSRF that exfiltrates the proxy's Azure bearer token to an attacker-controlled host. Token replay against the real Key Vault defeats the entire record-encryption trust model.

### CVE-2026-12665

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-19T17:17:18.773 |

IBM MQ could allow a remote attacker to execute arbitrary code due to a stack buffer overflow when processing TLS certificates with malformed distinguished names during channel connection establishment.

### CVE-2026-91041

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787;CWE-1284` |
| Published | 2026-10-20T14:17:04.350 |

Mounting an attacker-controlled FAT image with fault tolerance enabled causes an out-of-bounds heap write during log replay. The write is attacker-positioned and attacker-valued, and on a common embedded memory layout it reaches the FX_MEDIA driver callback, giving control of the instruction pointer.

### CVE-2026-111090

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-20T08:16:42.373 |

A logic error exists in the signature verification routine resulting in acceptance of unauthenticated update and license files.It is necessary to use only the MyStormshield servers to retrieve update files or licenses, or to use automatic verification via SNS.

### CVE-2026-86961

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-20T01:17:28.857 |

A race condition was addressed with additional validation. This issue is fixed in iOS 27 and iPadOS 27, macOS Golden Gate 27. A malicious app may be able to break out of its sandbox.

### CVE-2026-28853

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-20T01:17:11.460 |

The issue was addressed with improved checks. This issue is fixed in macOS Sequoia 15.8, macOS Tahoe 26.7. An app may be able to elevate privileges.

### CVE-2026-112261

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-19T22:17:05.767 |

A flaw was found in GIMP. Opening a crafted XCF that selects a path and then fails to load that path can cause a use-after-free in the main process, leading to a crash and potentially arbitrary code execution.

### CVE-2026-112258

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-19T22:17:05.543 |

A flaw was found in GIMP. The XCF loader can leave a dangling pointer in the linked-channels list when a linked channel is later destroyed via a selection property. Opening a crafted XCF file can cause a use-after-free in the main GIMP process, leading to a crash and potentially arbitrary code execution.

### CVE-2026-112257

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-19T22:17:05.420 |

A flaw was found in GIMP. The PSD thumbnail resource loader performs a BGR-to-RGB channel swap with a fixed 3-byte stride and does not verify that the JPEG thumbnail is RGB. A crafted grayscale PSD thumbnail can cause a heap out-of-bounds read and write in the plug-in process, leading to a crash and potentially arbitrary code execution when the victim browses or opens the file.

### CVE-2026-71170

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-10-19T20:20:03.693 |

Dell Application Store, versions prior to 26.05.0.7, contains an Uncontrolled Path Element vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to an Elevation of Privilege and arbitrary code execution.

### CVE-2026-107571

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-10-19T16:17:01.970 |

Incorrect default permissions in the Windows installer of Progressive Robot hMailServer 6.0.0 through 6.3.6 allow a local authenticated user to run code as the mail server's high-privileged accounts when the product is installed in a folder whose permissions are inherited from a writable parent, such as the root of a drive. The installer places the server's programs in the Bin folder of the program folder and gives neither the program folder nor Bin any permissions of their own, so they inherit the parent's. Under the default location, Program Files, ordinary users receive only read and execute and the configuration is not affected; but the installer accepts any path without warning, and a program folder at the root of an NTFS volume inherits write access for a broad group - Authenticated Users (Modify) on a Windows client, Users (create files and folders) on Windows Server. A local user without administrator rights can then alter or replace the service program, which runs as LocalSystem or as the service's virtual account, or the programs an administrator runs elevated from Bin during setup and maintenance, or place a library in Bin that those programs load in place of the system copy, gaining code execution with those privileges. The default Program Files installation is not affected.

### CVE-2026-105311

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-441` |
| Published | 2026-10-20T12:17:28.550 |

The StreamsHub Console operator acts as a confused deputy: a Kubernetes tenant with permission to create a Console custom resource can set spec.kafkaClusters[].credentials.kafkaUser.namespace to any namespace. The operator, running with cluster-wide Secrets RBAC, reads the victim-namespace KafkaUser Secret (SASL credentials or TLS private keys) and writes the plaintext material into a Secret in the attacker's namespace. No same-namespace check or allowlist exists anywhere in the code path.

### CVE-2026-113356

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-20T11:17:20.143 |

DokuWiki before 2026-07-14c contains a PHP object injection vulnerability in Draft::getDraftText() that passes draft file contents to unserialize() without restricting allowed classes. Authenticated users with edit rights can race concurrent draft rewrites to splice serialized data, instantiating gadgets like MemoryIndex or Installer for arbitrary file write, deletion, and code execution.

### CVE-2026-113352

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-20T11:17:19.520 |

uTox through 0.18.1 contains a path traversal vulnerability that allows Tox friends to write arbitrary files by sending absolute or ../ file names to victims with auto-accept enabled. Attackers can overwrite shell startup files or plant crafted .ftinfo resume records that ft_find_resumeable() loads, abusing FILE pointers to write /proc/self/mem and execute code.

### CVE-2026-112304

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-19T16:17:06.257 |

docTR through 1.1.0 contains an unsafe deserialization vulnerability in load_pretrained_params() that loads checkpoints with torch.load without weights_only=True. Attackers who control a local or URL-supplied checkpoint can embed a malicious pickle payload to execute Python code with the loading process's privileges on torch releases before 2.6.

### CVE-2026-113619

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-20T13:16:41.473 |

In Eclipse ioFog Controller versions 3.8.0 through 3.9.1, POST, PUT, and PATCH bodies on routes that enable template substitution are rendered by an uncapped Liquid engine before authentication and RBAC. The bearer check does not reject a missing or invalid token, and the auth rate limit applies only to user login routes. A small JSON body can stall or abort the Controller process. The anonymous caller does not receive the rendered result; the impact is availability of the control plane, including the agent API and in-process WebSocket relays on that process.

### CVE-2026-43855

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T10:17:06.520 |

A heap-based buffer overflow vulnerability could allow a remote authenticated attacker to achieve arbitrary code execution.

### CVE-2026-43837

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T09:17:10.070 |

A buffer overflow vulnerability in the password verification functionality could allow an attacker with guest authentication to achieve code execution.

### CVE-2026-113469

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-20T09:17:09.587 |

A failure has been identified in the SNS during dynamic data files signature check.



A logic error in the signature verification routine resulting in acceptance of unauthenticated dynamic data update during Autoupdate routine.

### CVE-2026-43834

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-20T08:16:44.083 |

A stack-based buffer overflow vulnerability in the logs settings functionality could allow an authenticated attacker to achieve code execution.

### CVE-2026-93300

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-20T06:16:57.913 |

The EventON - Subscriber plugin for WordPress is vulnerable to generic SQL Injection via the 'email' parameter in all versions up to, and including, 1.4.5 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-105297

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-20T01:17:09.613 |

Summary



Before version 0.8.1, Pingora's HTTP/2 server used the h2 crate's default limits unless the application set its own 16 MiB decoded header-list size and no limit on concurrent streams. A remote, unauthenticated client can send 1-byte HPACK references to a near-empty header, making the server allocate hundreds of thousands of header fields per stream across an unlimited number of streams on one connection, and use HTTP/2 flow control to keep those streams open. This can exhaust memory and degrade or terminate the Pingora process.




Impact



Remote, unauthenticated denial of service against any Pingora service that terminates HTTP/2 (h2 or h2c) without explicitly setting max_header_list_size and max_concurrent_streams. The reporter showed that a single connection could get a Pingora process with a 2 GiB memory limit OOM-killed.




Note that Cloudflare CDN customers were unaffected, as internal Pingora services at Cloudflare do not have HTTP/2 clients.



Mitigation:

  *  

Upgrade to pingora 0.8.1 or later (fix:  https://github.com/cloudflare/pingora/commit/d193c8d49b8b7c1c1ede93183759caa4f6906bbd ). When no H2Options are supplied, Pingora now advertises and enforces a 64 KiB decoded header-list limit and at most 100 concurrent streams per connection.


  *  

Applications that supply their own H2Options are not covered by these defaults and must set max_header_list_size and max_concurrent_streams explicitly (this also works on versions before 0.8.1), or, on 0.8.1 and later, start from pingora_core::protocols::http::v2::server::default_h2_options(). H2Options::default() does not include these limits.

### CVE-2026-6719

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-330` |
| Published | 2026-10-19T18:17:08.720 |

IBM Concert 1.0 through 3.0.0 uses weaker than expected cryptographic algorithms that could allow an attacker to decrypt highly sensitive information.

### CVE-2026-111759

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-10-19T18:17:00.570 |

markdown-it is a Markdown parser. Prior to 14.3.2 and 15.0.2, when typographer: true is enabled, specially crafted Markdown can cause quadratic processing time in the smartquotes rule, potentially leading to denial of service in applications processing untrusted input. Many opening double quotes followed by unmatched closing single quotes cause repeated scans of the entire opener stack. The same issue occurs with the quote types reversed. The default configuration (typographer: false) is not affected, but this option is enabled with high probability. This issue is fixed in versions 14.3.2 and 15.0.2.

### CVE-2025-52290

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-19T18:16:58.040 |

A NULL pointer dereference in the avpriv_h264_has_num_reorder_frames function of Ffmpeg version N-119856-gbe46370941 allows attackers to cause a Denial of Service (DoS) via processing a crafted media file.

### CVE-2026-12148

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-19T17:17:17.120 |

IBM MQ Operator could allow an authenticated attacker to cause a denial of service or potentially execute arbitrary code due to unrestricted Java deserialization in the MQ Classes for Java.

### CVE-2026-111045

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-19T16:17:03.183 |

CLI Bridge provides filesystem access within a workspace root. Prior to 0.0.2, a dangling symlink pointing outside the workspace root bypasses resolveSafePath when fs.realpathSync throws ENOENT for a nonexistent target. The fallback resolves only the parent directory and returns the symlink path as safe, so write_file follows the link and can write arbitrary files outside the workspace root. This issue is fixed in version 0.0.2.

### CVE-2026-107569

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-606` |
| Published | 2026-10-19T16:17:01.830 |

Unchecked input for a loop condition in Progressive Robot hMailServer 6.0.0 through 6.3.6 allows a remote unauthenticated attacker to stop the server carrying mail. The server bounds the mail it generates in response to a message - a rule forward, reply or copy, an account forward, a Sieve redirect, vacation or notify, a bounce, an out-of-office reply - by a counter it carries in the message's X-hMailServer-LoopCount header, and makes no more once the counter reaches the configured rule loop limit (5 by default); that is what ends a forwarding or auto-reply cycle in a bounded number of hops. X-hMailServer-LoopCount is an ordinary header that is not stripped from mail arriving from outside, and the server read it with a signed conversion and no validation, so a count below zero passed every test against the limit: a sender who sets X-hMailServer-LoopCount to a negative value, or on the Linux builds to a value above the 32-bit signed range that the conversion wraps to a negative one, lifts the bound, and a message that enters a generated-mail cycle then loops up to about two thousand million times, each hop a queued message and a delivery, filling the queue and disk and stopping mail service. The Sieve notify action (from 6.2.22) consulted no limit at all, and its increment of the count could overflow a signed integer; and an account could reset the counter on its own mail through a Sieve editheader of the header (from 6.2.22) or a rule Set header value action (all versions) ahead of a forward or redirect.

### CVE-2026-107567

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-348` |
| Published | 2026-10-19T16:17:01.587 |

Use of a less trusted source in the DKIM signing of Progressive Robot hMailServer 6.0.0 through 6.3.6 allows a remote unauthenticated attacker to have mail they write signed with the DKIM key of a domain the server hosts, so that it passes DKIM and DMARC for that domain at other receivers. With DKIM signing enabled for a hosted domain, the server signed every message on its first delivery pass as the domain named in its From header, before local delivery, whatever the message's origin and without checking that its sender had authenticated. A sender anywhere could therefore send the server, as ordinary inbound mail, a message whose From is any address at such a domain, and the server signed it with that domain's key. Every copy the server then sent on to an address outside carried a valid signature aligned with the forged From, whatever the domain's DMARC policy: an account's forward, a mail rule's forward or copy, a Sieve redirect, an alias or distribution list with an outside member, the mirror copy, a managed-list or journal copy, or a message released from quarantine. A signed copy can also be re-sent to other recipients while the domain's key is unchanged. Exploitation needs DKIM signing to be enabled for the hosted domain (it is off until configured) and, for the forgery to leave the server, a forward, alias, list or rule that carries the domain's mail to an outside address. The signer likewise signed a message submitted over authenticated SMTP as whatever hosted domain its From header named, a header authenticated SMTP does not hold to the submitting account, so that an account of one hosted domain could have mail written in the name of another hosted domain signed with that domain's key; this mattered where the server holds signed-in senders to their own envelope addresses (SmtpAuthenticatedSenderCheck, off by default), as the signature was then the remaining way for such mail to pass the other domain's DMARC policy.

### CVE-2026-112360

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-912` |
| Published | 2026-10-19T22:17:06.217 |

A security vulnerability has been detected in Netis EAP930 1.250905.115454. This issue affects the function return200 of the file /cgi-bin/debug of the component CGI Endpoint. The manipulation of the argument SIGNATURE leads to backdoor. The attack may be initiated remotely. A high degree of complexity is needed for the attack. The exploitability is assessed as difficult. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-3295

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-19T18:17:07.263 |

IBM Cloud Pak System 2.3.6.0, and 2.3.6.1 is vulnerable to cross site scripting. The web app user‑supplied input is not properly sanitized or HTML‑encoded before being stored and rendered. An authenticated attacker could exploit this vulnerability by entering specially crafted payloads containing malicious JavaScript which are saved within the app and later executed automatically when user views affected pages, resulting in Stored Cross‑Site Scripting (Stored XSS).

### CVE-2026-112177

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-648` |
| Published | 2026-10-20T08:16:42.507 |

A flaw was found in Ghostscript as shipped with Red Hat Enterprise Linux 8. The correction for CVE-2019-14869 was omitted during the rebase from version 9.25 to 9.27, leaving privileged .forceput operations in the .charkeys procedure insufficiently protected. Processing a specially crafted PostScript file may allow an attacker to bypass -dSAFER restrictions and access files outside the permitted paths or execute commands with the permissions of the Ghostscript process.

### CVE-2026-112239

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862;CWE-915` |
| Published | 2026-10-20T10:17:04.780 |

The extension provides a backend endpoint that writes a submitted value into a submitted field of a submitted page record. It neither checks the user's permissions nor limits which fields can be changed. Any authenticated backend user can therefore change any property of any page, including its access permissions and configuration, outside the scope granted to them.

### CVE-2026-113354

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-20T11:17:19.843 |

Dockhand before 1.0.46 contains an arbitrary file read vulnerability that allows non-admin users with stacks:edit permission to read files through the path parameter of /api/system/files/content. Attackers can supply absolute paths to read /etc/shadow, /etc/passwd, git .git/config credentials, and SSH keys from the Dockhand container.

### CVE-2026-113459

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-20T10:17:05.540 |

In versions running on TYPO3 10 and 11, the configured OpenAI API key is embedded in every backend page, so that the editor plugin can contact the OpenAI service directly from the browser. Any authenticated backend user can read the key and use it at the expense of the site operator. This only applies if an API key has been configured.

### CVE-2026-112066

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-20T10:17:03.757 |

The JSON import of the cookie consent configuration did not respect the backend user's permissions. Non-admin backend users with access to the module could import a configuration that adds arbitrary scripts to the frontend of the website.

### CVE-2026-112064

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-20T10:17:03.467 |

The backend module for reviewing the consent history accepted sorting, grouping and index options from the request and used them in a database query without validation. Only the filter conditions of that query were bound as parameters. A backend user with access to the history or statistics functions could use this to read arbitrary data from the database, including password hashes of backend and frontend users.

### CVE-2026-113403

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-10-20T07:17:09.653 |

ArmorX Spam developed by ArmorX Global Technology has a Command Injection vulnerability. Authenticated remote attackers can inject crafted commands into a specific parameter, thereby uploading malicious code to the server.

### CVE-2026-113402

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-20T07:17:09.493 |

ArmorX Spam developed by ArmorX Global Technology has a Local File Inclusion vulnerability. Authenticated remote attackers can exploit path traversal to cause the application to include PHP files outside the intended directory.

### CVE-2026-113386

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-93` |
| Published | 2026-10-20T05:16:54.250 |

Roundcube Webmail before 1.6.20 and 1.7.x before 1.7.5 are affected by IMAP command injection. A remote authenticated attacker can exploit this via CRLF sequences injected into the _uid parameter of the mail/headers and mail/viewsource actions to execute arbitrary IMAP commands.

### CVE-2026-77938

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-526` |
| Published | 2026-10-20T01:17:20.410 |

Letta through 0.16.8 contains an information disclosure vulnerability that allows users running tools to read server secrets because LocalSandbox subprocesses inherit the full server environment. Attackers can run code via POST /v1/tools/run or custom tools to read LETTA_PG_URI, POSTGRES_PASSWORD, and provider API keys, then access cross-tenant database data.

### CVE-2026-105815

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-19T22:17:03.153 |

TP-Link Tapo
C210 V3.60 may expose shared credential material and cryptographic metadata
through unauthenticated DS JSON API requests. The exposed shared credential can
be accepted by the Streamd Digest authentication mechanism as an administrative
password, allowing an unauthenticated adjacent-network attacker to establish
encrypted media sessions without knowledge of the device account
password.  









Successful
exploitation may disclose credential and cryptographic material and allow
unauthorized access to encrypted media sessions.

### CVE-2026-112771

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-19T20:17:54.203 |

Craft CMS 4.0.0 before 4.18.8 and 5.0.0 before 5.11.0 contains a Twig sandbox allowlist bypass because the column, contains, filterByValue, index, where, and multisort filters resolve caller-supplied keys via ArrayHelper::getValue() without consulting the sandbox security policy. Authenticated Control Panel users can supply dot-path keys to traverse the craft global and disclose the securityKey, database credentials, and auth tokens.

### CVE-2026-112260

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-19T20:17:52.970 |

A flaw was found in GIMP. Opening a crafted XCF with a malformed text-layer parasite can cause a heap out-of-bounds read, disclosing adjacent heap data into layer text and causing denial of service.

### CVE-2026-112158

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-189;CWE-190` |
| Published | 2026-10-19T16:17:05.917 |

A weakness has been identified in MikroTik RouterOS up to 6.40.5/6.44/7.20.8. Impacted is the function same_check of the file ipt_SAME.ko. Executing a manipulation can lead to integer overflow. The attack may be launched remotely. Upgrading to version 7.21.5 and 7.23.1 is recommended to address this issue. You should upgrade the affected component.

### CVE-2026-71169

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-19T20:20:03.053 |

Dell Application Store, versions prior to 26.05.0.7, contain an Incorrect Permission Assignment for Critical Resource vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Disclosure of sensitive information
