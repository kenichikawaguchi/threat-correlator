# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-11 15:00 UTC
- **対象期間**: `2026-08-10T15:00:43.000Z` 〜 `2026-08-11T15:00:50.000Z`
- **重要CVE数**: 206 件（Critical 9.0+: 56 件 / High 7.0〜: 150 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件以上** に上り、うち **10 件が CVSS 10.0／9.9** と極めて高いリスクを示しています。共通する傾向は以下の通りです。

| 傾向 | 内容 |
|------|------|
| **認証なしでコード実行が可能** | Electron アプリ、SAP Commerce Cloud、Siemens SIMATIC IoT2050、Metabase など、認証・権限チェックが不十分な API が直接 OS コマンドやデータベースへ渡されている。 |
| **シェルコマンドインジェクション** | 多くの PaaS 系プロダクト（Dokploy 系列）で、ユーザー入力が `child_process.exec` へそのまま渡され、root 権限でコマンド実行が可能になる。 |
| **SQL インジェクション** | Metabase、YesWiki、e107 などの Web アプリで、パラメータがエスケープされずに SQL 文へ組み込まれ、データベース全体が漏洩・改竄できる。 |
| **デフォルト認証クレデンシャルの乱用** | SAP Commerce Cloud のデフォルト認証クライアント、SIMATIC の Node‑RED インターフェースが認証なしで利用可能。 |
| **影響範囲の広さ** | 産業制御系（SIMATIC IoT2050）やエンタープライズ向け EC（SAP Commerce Cloud）といったミッションクリティカルなシステムまでが対象となっている。 |

> **結論**：認証・入力検証の欠如が多数の高危険度脆弱性の根本原因であり、**「デフォルト設定のまま運用」** が最大のリスクファクターです。

---

## 2. 特に注目すべき CVE（上位 5 件）

| CVE | CVSS | 製品・コンポーネント | 主な問題点 | 影響範囲・被害シナリオ |
|-----|------|----------------------|------------|------------------------|
| **CVE‑2026‑48056** | 10.0 | Streambert (Electron デスクトップアプリ) | IPC ハンドラ `run-download` が実行ファイルパスを検証せず、renderer プロセスから任意ローカルバイナリを実行できる。 | 攻撃者はユーザーの権限で任意コードを実行し、マルウェアの永続化や情報窃取が可能。 |
| **CVE‑2026‑58115** | 10.0 | Siemens SIMATIC IoT2050 Advanced (Industrial OS + Node‑RED) | Node‑RED の HTTP インターフェースが認証を要求せず、プログラミングノードに無制限アクセスできる。 | 産業制御システムのフローを書き換え、PLC への不正制御やデータ改ざんが実行可能。 |
| **CVE‑2026‑58231** | 10.0 | SAP Commerce Cloud | デフォルト認証クライアントが不適切に公開され、入力検証が欠如した API に特別に細工したリクエストを送るだけで任意コード実行が可能。 | コマースサイト全体が乗っ取り対象となり、顧客情報・決済データが漏洩・改竄される危険性。 |
| **CVE‑2026‑72899** / **CVE‑2026‑72898** (Metabase) | 10.0 | Metabase (オープンソース BI) | 公開カード/ダッシュボードのフィルターパラメータ、及び `/reset_password` エンドポイントで SQL インジェクションが成立。 | 攻撃者はデータベース管理者権限で任意 SQL を実行し、全データベースを取得・改ざん、さらに管理者アカウント取得が可能。 |
| **CVE‑2026‑72603** | 9.9 | wg‑easy (WireGuard 管理 UI) | `client name` フィールドに改行で `PostUp` ディレクティブを注入でき、root 権限で OS コマンド実行が可能。 | VPN サーバー上で任意コードが走り、内部ネットワーク全体への踏み台化が容易になる。 |

> **選定理由**：上記 5 件は **CVSS が最高点に近く、認証不要または低権限での利用が可能** である点、さらに **産業・商取引・インフラ** といった重要領域に直接影響する点で優先的に対策すべきです。

---

## 3. 推奨アクション

### 3.1 共通的な緊急対策
1. **直ちにパッチ適用**  
   - 各ベンダーが提供する **最新安定版** へアップデートする。  
   - パッチが未提供の場合は **ベンダーの緊急アドバイザリ** を確認し、回避策（設定変更・サービス停止）を実施。

2. **認証・アクセス制御の強化**  
   - デフォルトの認証クレデンシャルは **全て無効化**、もしくは **強力なパスフレーズ** に置き換える。  
   - 外部から直接アクセスできる管理 API（Node‑RED, SAP Cloud API, wg‑easy の IPC 等）は **VPN／IP フィルタ** で内部ネットワークに限定。

3. **入力検証・サニタイズの徹底**  
   - シェルコマンドにユーザー入力を渡す箇所は **パラメータ化**、もしくは **安全なラッパー関数**（例: `child_process.execFile`）へ置き換える。  
   - SQL クエリは必ず **プリペアドステートメント**／**ORM のバインディング** を使用。

4. **監視・ロギング**  
   - 高リスク API へのリクエストは **WAF** で可視化し、異常なパラメータ（改行・シェルメタ文字）を検知。  
   - 侵入テストやレッドチーム演習で **CVE の PoC** が再現できないか定期的に検証。

5. **インシデント対応体制の確認**  
   - 影響が確認された場合の **フォレンジック手順**、**バックアップからの復旧** 手順を最新化。  
   - 特に産業制御系（SIMATIC IoT2050）は **OT セキュリティチーム** と連携し、PLC への影響評価を実施。

### 3.2 製品別具体的アップデート指示

| 製品 | 現行バージョン (脆弱) | 推奨バージョン (修正済) | アップデート手順の要点 |
|------|----------------------|------------------------|------------------------|
| **Streambert** | < 2.5.0 |

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-48056

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-749` |
| Published | 2026-08-11T14:17:14.170 |

Streambert is a cross-platform Electron Desktop App to stream and download video content. Versions prior to 2.5.0  improperly validate executable paths supplied to the  run-download  IPC handler, allowing a compromised renderer process to execute arbitrary local binaries with the application’s privileges. Version 2.5.0 contains a patch.

### CVE-2026-58115

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-11T13:19:00.190 |

A vulnerability has been identified in SIMATIC IoT2050 Advanced (6ES7647-0BA00-1YA2) (All versions < V4.3.4.1 running Industrial OS with Node-RED installed). Affected devices do not enforce authentication on the Node-RED HTTP interface, allowing unauthenticated access to programming nodes that are capable of executing system commands on the server.
This could allow an unauthenticated remote attacker to create malicious flows through the HTTP interface in order to execute arbitrary code on the underlying server with maximum privileges.

### CVE-2026-58231

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-11T11:17:15.390 |

SAP Commerce Cloud allows an unauthenticated
attacker to abuse a default authentication client and submit specially crafted
input to certain functions lacking sufficient validation. Successful
exploitation could enable arbitrary code execution and compromise internal
components, resulting in high impact on confidentiality, integrity, and
availability of the application.

### CVE-2026-72899

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-10T18:18:53.490 |

Metabase allows an unauthenticated attacker to inject arbitrary SQL via a publicly shared card or dashboard that exposes a field-filter (dimension) parameter.

### CVE-2026-72898

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-10T18:18:53.300 |

Metabase allows a remote, unauthenticated attacker to inject arbitrary SQL via the '/reset_password' database endpoint and gain administrator access to the connected Metabase instance.

### CVE-2026-72603

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-11T12:17:43.383 |

An OS command injection vulnerability in wg-easy 15.3.0 allows users with the clients.create permission to execute arbitrary commands as root by injecting newline-delimited WireGuard PostUp directives into the client name field. The client name is written to the WireGuard configuration file without neutralizing newline characters, allowing injection of arbitrary directives that are executed by wg-quick with root privileges. An attacker with clients.create permission achieves root code execution on the host.

### CVE-2026-72911

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-10T21:17:25.993 |

ERPNext is a free and open source Enterprise Resource Planning tool. Prior to 15.118.0 and 16.29.0, the validate_template and render_template calls in erpnext/accounts/doctype/process_statement_of_accounts/process_statement_of_accounts.py render subject, body, and pdf_name fields with unrestricted globals including frappe.utils, allowing an authenticated user with a common operational role to inject template expressions, execute arbitrary server-side code, and read data across the application. This issue is fixed in versions 15.118.0 and 16.29.0.

### CVE-2026-18948

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-10T21:17:21.290 |

A flaw was found in Feast. The system improperly deserializes user-defined functions (UDFs) stored in its registry, which are serialized using the 'dill' library. This allows a remote attacker to store a malicious UDF, leading to unauthenticated arbitrary code execution on the feature server in default configurations. An authenticated attacker can also achieve arbitrary code execution on the registry server by bypassing authorization checks during deserialization. This vulnerability can result in cross-tenant data access and lateral movement within the system.

### CVE-2026-14450

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-10T21:17:19.487 |

A flaw was found in the MaaS API. This vulnerability allows any pod within the cluster to bypass the Kuadrant AuthPolicy gateway by forging HTTP headers, specifically `X-MaaS-Username` and `X-MaaS-Group`, which are trusted verbatim. This lack of first-party authentication enables an attacker to gain unauthorized access and escalate privileges. The concrete consequences include the ability to mint Kubernetes ServiceAccount tokens in other tenants' namespaces, revoke API keys, and exfiltrate sensitive model access configuration.

### CVE-2026-72902

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T20:17:35.707 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, Dokploy allows an authenticated user to execute arbitrary commands on a local or SSH-connected target server because registry.testRegistry and registry.testRegistryById in apps/dokploy/server/api/routers/registry.ts interpolate the password field into an execAsyncRemote shell command instead of using safeDockerLoginCommand. This issue is fixed in version 0.29.13.

### CVE-2026-72901

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T20:17:35.570 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, Dokploy allows an authenticated low-privilege member to execute arbitrary commands on the control-plane host because the volumeName field accepted by volumeBackup.create and volumeBackup.runManually is interpolated without quoting in packages/server/src/utils/volume-backups/backup.ts and executed through child_process.exec, with Docker socket access making execution host/root-equivalent. This issue is fixed in version 0.29.13.

### CVE-2026-72886

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-863` |
| Published | 2026-08-10T20:17:35.423 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). From 0.29.2 until 0.29.13, schedule.create and schedule.update in apps/dokploy/server/api/routers/schedule.ts derive serviceId from applicationId or composeId and execute the owner/admin host-schedule gate only in the alternative branch, allowing a member with access to one application to attach its applicationId to a dokploy-server schedule and run a supplied script as root through schedule.runManually. This issue is fixed in version 0.29.13.

### CVE-2026-72882

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T20:17:34.860 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). In 0.28.8 and earlier, an authenticated user who can create or update file mounts for a service can inject shell metacharacters into filePath, causing Dokploy to execute attacker-controlled commands on the configured remote managed server over SSH. In the default deployment model, this yields direct remote host RCE from the web interface.

### CVE-2026-72880

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T20:17:34.560 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, the apiCreateCertificate schema in packages/server/src/db/schema/certificate.ts accepts a client-supplied certificatePath, and packages/server/src/services/certificate.ts joins that value to the certificate root without confinement. An authenticated user with certificate create or delete permission can use certificatePath to write attacker-controlled certificate content outside the intended directory or delete an out-of-root directory. This vulnerability is fixed in 0.29.13.

### CVE-2026-72876

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-639;CWE-862` |
| Published | 2026-08-10T20:17:33.967 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, swarm.getNodes, swarm.getNodeInfo, swarm.getNodeApps, and swarm.getAppInfos in apps/dokploy/server/api/routers/swarm.ts accept another organization’s serverId without an activeOrganizationId ownership check, and getNodeInfo in packages/server/src/services/docker.ts interpolates nodeId into execAsyncRemote, allowing a caller with server:read permission to execute arbitrary commands as the configured SSH user on another tenant’s server. This issue is fixed in version 0.29.13.

### CVE-2026-72872

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T19:17:36.177 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, application.saveBitbucketProvider stores bitbucketOwner and bitbucketRepository without validation and cloneBitbucketRepository in packages/server/src/utils/providers/bitbucket.ts interpolates those values into git clone commands executed through execAsync or execAsyncRemote, allowing a member with service deployment permission to execute arbitrary operating system commands on the Dokploy host or target server. This issue is fixed in version 0.29.13.

### CVE-2026-72869

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-08-10T19:17:35.753 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, the backup.restoreBackupWithLogs tRPC subscription passes the databaseName parameter to restore builders in packages/server/src/utils/restore/utils.ts, where PostgreSQL, MariaDB, MySQL, and MongoDB commands embed the value in nested shell text executed by Node.js exec. An authenticated user with backup:restore permission can supply a crafted databaseName that the host /bin/sh expands before docker exec, resulting in arbitrary commands running in the Docker-privileged host context. This issue is fixed in version 0.29.13.

### CVE-2026-72868

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-862` |
| Published | 2026-08-10T19:17:35.600 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, apps/dokploy/server/api/routers/destination.ts interpolates the accessKey, secretAccessKey, region, endpoint, provider, and bucket fields from destination.testConnection into an rclone ls command executed through child_process.exec. The `withPermission("destination", "create")` path permits a low-privileged organization member to reach the mutation, close a quoted argument with a crafted field, and execute arbitrary commands in the root Dokploy container, which has access to the host Docker socket. This issue is fixed in version 0.29.13.

### CVE-2026-72867

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-78;CWE-602` |
| Published | 2026-08-10T19:17:35.443 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). From 0.29.3 until 0.29.13, the incomplete fix for CVE-2026-45628 leaves packages/server/src/db/schema/compose.ts branch fields without server-side validation, allowing a direct compose.update request to store a malicious customGitBranch, branch, gitlabBranch, bitbucketBranch, or giteaBranch. A low-privileged authenticated user can trigger compose.deploy, which passes the stored branch to shell-based Git clone commands in packages/server/src/utils/providers/git.ts, github.ts, gitlab.ts, bitbucket.ts, and gitea.ts, resulting in arbitrary host command execution. This issue is fixed in version 0.29.13.

### CVE-2026-72865

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T19:17:35.160 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, the compose.update operation stores an unvalidated composePath that packages/server/src/utils/builders/compose.ts and packages/server/src/services/compose.ts interpolate into docker compose -f, docker stack deploy -c, and touch shell commands executed through /bin/sh -c. An authenticated member with compose write and deploy permission can supply a crafted composePath, trigger compose.deploy or startCompose, and execute arbitrary operating-system commands in the Docker-privileged Dokploy host context. This issue is fixed in version 0.29.13.

### CVE-2026-72864

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-10T19:17:35.010 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, the local branch of /docker-container-terminal in apps/dokploy/server/wss/docker-container-terminal.ts authenticates with validateRequest but does not authorize the attacker-controlled containerId against the caller's role, organization, or service access before passing it to `docker exec`, allowing any authenticated member to obtain a root shell in arbitrary containers on a self-hosted instance. This issue is fixed in version 0.29.13.

### CVE-2026-72863

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-639;CWE-862` |
| Published | 2026-08-10T19:17:34.870 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, Dokploy's WebSocket handlers (in-app terminals and log streamers) authenticate the session but never authorize it. They establish who the user is via validateRequest() and then proceed without consulting the role/permission model that every tRPC procedure enforces. Any authenticated member, can therefore open an interactive shell into any container on the host, including the dokploy container that mounts the Docker socket, and from there obtain root on the host, escaping the application and crossing every tenant boundary. This vulnerability is fixed in 0.29.13.

### CVE-2026-72862

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T18:18:53.047 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, the mariadb.ts, mongo.ts, mysql.ts, postgres.ts, redis.ts, and libsql.ts Dokploy database service deployment functions pass user-controlled dockerImage fields unquoted into docker pull ${dockerImage} shell commands on the remote-server code path. This vulnerability is fixed in 0.29.13.

### CVE-2026-72740

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T18:18:52.723 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, packages/server/src/utils/providers/git.ts parses the user-controlled customGitUrl with sanitizeRepoPathSSH and interpolates its domain into the ssh-keyscan command from addHostToKnownHostsCommand without shell quoting, allowing an authenticated member with service deployment permission and an attached SSH key to execute arbitrary commands on the Dokploy host during deployment. This issue is fixed in version 0.29.13.

### CVE-2026-72738

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T18:18:52.430 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, the backup.listBackupFiles tRPC endpoint in apps/dokploy/server/api/routers/backup.ts passes the search parameter through normalizeS3Path and interpolates it into an rclone lsjson command executed by child_process.exec(), allowing an authenticated user with backup:read permission to execute arbitrary commands on the Dokploy host. This issue is fixed in version 0.29.13.

### CVE-2026-72736

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-10T18:18:52.123 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, Dokploy passes user-controlled values directly into shell commands via unquoted template literal interpolation in the registry credential testing and Docker Swarm cluster management endbpoints. Both endpoints have a safe local code path (using execFileAsync or the Docker API) but a vulnerable remote path (using execAsyncRemote which runs the shell string via SSH). This vulnerability is fixed in 0.29.13.

### CVE-2026-72735

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-10T18:18:51.977 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, writeTraefikConfigRemote in packages/server/src/utils/traefik/application.ts serializes user-controlled Traefik configuration with yaml.stringify and interpolates the resulting yamlStr into an echo command executed through execAsyncRemote. Single quotes in redirect regex and replacement fields, basic authentication usernames, domain host values, or middleware configuration can terminate the shell quoting and execute arbitrary commands on managed remote servers with the configured SSH user's privileges. This vulnerability is caused by an incomplete fix for CVE-2026-45630. This issue is fixed in version 0.29.13.

### CVE-2026-72733

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T18:18:51.673 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, the backup.restoreBackupWithLogs tRPC subscription builds database restore shell pipelines from the user-controlled databaseName and backupFile fields without safely separating them from shell syntax. packages/server/src/utils/restore/utils.ts interpolates databaseName into database-specific restore commands, while packages/server/src/utils/restore/postgres.ts and the analogous restore modules interpolate backupFile into rclone paths. An authenticated member with backup-restore permission can inject operating-system commands that execute in the Dokploy host context through execAsync or execAsyncRemote, even when no valid database container or backup file exists. This issue is fixed in version 0.29.13.

### CVE-2026-46670

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-11T14:17:13.863 |

YesWiki is a wiki system written in PHP. Prior to version 4.6.4,  an unauthenticated SQL injection in the Bazar form-import path (`FormManager::create()`) allows any unauthenticated visitor of a default YesWiki install to inject arbitrary SQL into an `INSERT` statement and read the full database, including `yeswiki_users.password` hashes. Version 4.6.4 fixes the issue.

### CVE-2026-72599

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-11T12:17:42.907 |

An SQL injection vulnerability in e107 2.4.0 allows unauthenticated remote attackers to execute arbitrary SQL via the news item page ID parameter. The parameter is concatenated without escaping into a SQL WHERE clause. An unauthenticated attacker can read, modify, or delete all database contents including administrator credentials.

### CVE-2026-72550

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-11T12:17:40.607 |

An SQL injection vulnerability in Friendica through the 2026.08-dev branch allows unauthenticated remote attackers to execute arbitrary SQL statements via the photo-view order parameter. The parameter is concatenated unescaped into a SHOW COLUMNS query via a bare PDO::query() call, enabling stacked statement injection. An unauthenticated attacker can read, modify, or delete the entire database.

### CVE-2026-10579

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-11T09:17:12.260 |

A flaw was found in Picketlink Federation SAML; the unsolcited response handler would accept forged assertions with no verification or validation, permitting an unauthed attacker to authenticate as any principal in any role. This could lead to information disclosure, access to restricted operations, or other flaws.

### CVE-2026-34265

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T01:17:20.240 |

SAP NetWeaver Application Server ABAP allows an unauthenticated attacker to exploit logical errors in DIAG protocol parsing, resulting in memory corruption. This vulnerability could potentially disclose sensitive system information or crash the system, leading to a high impact on the confidentiality, integrity, and availability of the application.

### CVE-2026-18972

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-11T13:17:56.997 |

An authenticated attacker can spoof another GUI user's identity by sending their request with the custom header \"Grpc-Metadata-USER\". This can lead to an account takeover attack from a user with low privileges to administrator.

### CVE-2026-72878

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T20:17:34.277 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, Dokploy's backup and restore pipeline constructs shell commands by directly interpolating user-controlled database fields into bash -c "..." and sh -c "..." strings, then executes them via child_process.exec(). An authenticated admin/owner can inject arbitrary OS commands that execute on the host machine running Dokploy (not just inside a container). This vulnerability is fixed in 0.29.13.

### CVE-2026-72877

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T20:17:34.133 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, the dockerImage field is interpolated without quoting into shell commands in buildRemoteDocker() in packages/server/src/utils/providers/docker.ts and is validated only as an optional string. An authenticated user with application create or update permission can use shell command substitution in dockerImage to execute arbitrary commands on the local build host or a remote SSH build target, exposing host secrets and other projects. This issue is fixed in version 0.29.13.

### CVE-2026-72737

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-08-10T18:18:52.280 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). In 0.29.8 and earlier, backup.create, backup.update, and backup.restoreBackupWithLogs in apps/dokploy/server/api/routers/backup.ts accept a client-controlled destinationId and use the referenced destination without verifying that destination.organizationId equals ctx.session.activeOrganizationId. An authenticated member with backup permissions for a service in one organization can cause another organization's S3 accessKey and secretAccessKey to be materialized by packages/server/src/utils/backups/utils.ts getS3Credentials on the attacker's service host, read that organization's backup objects, or redirect and poison backups across tenant boundaries.

### CVE-2026-72879

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T20:17:34.420 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.8, the getRegistryCommands() function in packages/server/src/utils/cluster/upload.ts interpolates registry.password and registry.registryUrl directly into a shell command without escaping. An authenticated user with project access can configure malicious registry credentials and trigger a swarm deployment to execute arbitrary OS commands on the Dokploy server, read or modify host files, and access other containers through Docker. This issue is fixed in version 0.29.8.

### CVE-2026-48046

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-08-11T14:17:14.020 |

Streambert is a cross-platform Electron Desktop App to stream and download video content. Versions prior to 2.5.0 contain an unvalidated auto-updater URL vulnerability that allows a compromised renderer process to make the main process download and execute an arbitrary binary, resulting in remote code execution. Version 2.5.0 contains a patch.

### CVE-2026-72785

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T13:19:09.220 |

Craft CMS 5.0.0-RC1 through 5.10.5 contains an incorrect authorization vulnerability. A control-panel user holding only the viewCategories permission (without saveCategories) for a category group can permanently modify that group's category structure — reordering and re-parenting categories — via the structures/move-element action. The structureEditable flag is computed from the view permission rather than the save permission, and the StructuresController authorizes the mutating action on that read-time session grant without a save re-check. Because a category's URI is derived from its position in the structure, moving a category changes its URL and those of its descendants and can corrupt navigation menus built from the category taxonomy. The issue is fixed in 5.10.6.

### CVE-2026-19425

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-11T05:17:14.680 |

Travel Agency Management System developed by Win Men Intermational has a SQL Injection vulnerability. Unauthenticated remote attackers can inject arbitrary SQL commands to read, modify, and delete database contents.

### CVE-2026-48161

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-506` |
| Published | 2026-08-10T23:16:51.343 |

react18-use is a React 19 use hook shim. Between 2026-05-19 01:07:01 and 2026-05-19 15:20:43, the default branch contained malicious commits 7b79148d1495a2505f9277da295a98cf176f4496 through 7b79148d1495a2505f9277da295a98cf176f4496 that executed remote attacker-controlled code on developer machines during `npm install`. The commits were removed by force-push, but local clones, forks, and direct-SHA URLs may still contain them, and `npm install` against an affected checkout will still execute the code today. The package was not published to npm. `src/install.js` was added and wired into the `postinstall` script. It fetched a JavaScript payload from an attacker-controlled HTTPS endpoint (configurable via an environment variable), disabled TLS verification, and evaluated the response as code with `require` available. Execution was deliberately skipped on CI and cloud/serverless environments, targeting developer workstations. The second-stage payload was attacker-hosted and cannot be reconstructed. Assume full compromise of anything reachable from a Node process with the user's permissions. Those who ran `npm install` against an affected checkout on a developer machine on or after 2026-05-19 01:07:01 should treat the machine as compromised, rotate every credential the machine could reach, audit account activity since 2026-05-19 01:07:01, and clean local clones.

### CVE-2026-72904

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78;CWE-94;CWE-95` |
| Published | 2026-08-10T21:17:25.117 |

Firecrawl turns entire websites into LLM-ready markdown or structured data. Prior to 2.11.32, a critical arbitrary file read vulnerability exists in Firecrawl's extraction functionality due to unsafe schema dereferencing of user-supplied JSON schemas in apps/api/src/lib/extract/helpers/dereference-schema.ts. The affected code invokes the json-schema-ref-parser dependency with default resolver settings, allowing external and local file references to be resolved during schema processing. An authenticated attacker can supply a malicious schema containing a $ref within default, const, or enum fields that are not traversed by AJV validation. By triggering a dereference error, file contents from the extract worker filesystem may be included in persisted error messages returned through the extraction API, enabling arbitrary file reads and SSRF against internal or external HTTP endpoints. This issue is fixed in version 2.11.32.

### CVE-2026-48160

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-506` |
| Published | 2026-08-10T21:17:23.303 |

react-tracked provides state usage tracking with Proxies. Between 2026-05-18 19:26:36 and 2026-05-19 15:22:45, the default branch contained malicious commits 6978272a7d6ca02225cb747ea69f427512e33699 through 949f1a3d6bb1ff7d1a0dec892afd773e742627e8 that executed remote attacker-controlled code on developer machines during `npm install`. The commits were removed by force-push, but local clones, forks, and direct-SHA URLs may still contain them, and `npm install` against an affected checkout will still execute the code today. The package was not published to npm. `src/install.js` was added and wired into the `postinstall` script. It fetched a JavaScript payload from an attacker-controlled HTTPS endpoint (configurable via an environment variable), disabled TLS verification, and evaluated the response as code with `require` available. Execution was deliberately skipped on CI and cloud/serverless environments, targeting developer workstations. The second-stage payload was attacker-hosted and cannot be reconstructed. Assume full compromise of anything reachable from a Node process with the user's permissions. Those who ran `npm install` against an affected checkout on a developer machine on or after 2026-05-18 19:26:36 should treat the machine as compromised, rotate every credential the machine could reach, audit account activity** since 2026-05-18 19:26:36, and clean local clones.

### CVE-2025-13294

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-10T20:17:24.583 |

An unauthenticated SQL injection vulnerability exists in the web server of TBEA TLogger V2.1.0.0B0.0.0.0. Multiple HTTP endpoints incorporate attacker-controlled parameters directly into SQLite queries without sufficient validation or parameterization. A remote unauthenticated attacker can exploit these endpoints to read, modify, or delete data stored in the device's CCU.db database.

### CVE-2025-13293

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-10T20:17:23.493 |

A hard-coded or default root account credential in TBEA TLogger V2.1.0.0B0.0.0.0 allows an unauthenticated remote attacker to obtain root-level access to the device via the exposed SSH service. The root password can be recovered from the password hash stored in /etc/shadow and used to authenticate to the SSH service. Successful exploitation provides full administrative control of the affected device.

### CVE-2026-48159

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-506` |
| Published | 2026-08-10T18:17:49.547 |

use-reducer-async is a React useReducer with async actions. Between 2026-05-18 16:29:52 and 2026-05-19 15:26:07, the default branch contained malicious commits da72edbde5705efcec6c62e0a3dcb73687b78dc8 through df07d5711458d8b46e11dd7afaaa21e88cafabfb that executed remote attacker-controlled code on developer machines during `npm install`. The commits were removed by force-push, but local clones, forks, and direct-SHA URLs may still contain them, and `npm install` against an affected checkout will still execute the code today. The package was not published to npm. `src/install.js` was added and wired into the `postinstall` script. It fetched a JavaScript payload from an attacker-controlled HTTPS endpoint (configurable via an environment variable), disabled TLS verification, and evaluated the response as code with `require` available. Execution was deliberately skipped on CI and cloud/serverless environments, targeting developer workstations. The second-stage payload was attacker-hosted and cannot be reconstructed. Assume full compromise of anything reachable from a Node process with the user's permissions. Those who ran `npm install` against an affected checkout on a developer machine on or after 2026-05-18 16:29:52 should treat the machine as compromised, rotate every credential the machine could reach, audit account activity since 2026-05-18 16:29:52, and clean local clones.

### CVE-2026-16626

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-08-10T18:17:41.667 |

Improper restriction of XML external entity reference vulnerability (unauthenticated) in Jaspersoft JasperReports Server.

This issue affects JasperReports Server: from 9.0.0 before HF-9 and from 10.0.0 before HF-10.

### CVE-2026-48158

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-506` |
| Published | 2026-08-10T16:19:48.117 |

use-context-selector is a React useContextSelector hook in userland Between 2026-05-18 15:57:18 and 2026-05-19 15:24:34, the default branch contained malicious commits 9d8481a513b7b0d1c0941b220c69b25de748641b through 6f2dae054ca014068bdbbb4db96006424d674124 that executed remote attacker-controlled code on developer machines during
`npm install`. The commits were removed by force-push, but local clones, forks, and direct-SHA URLs may still contain them, and `npm install` against an affected checkout will still execute the code today. The package was not published to npm. `src/install.js` was added and wired into the `postinstall` script. It fetched a JavaScript payload from an attacker-controlled HTTPS endpoint (configurable via an environment variable), disabled TLS verification, and evaluated the response as code with `require` available. Execution was deliberately skipped on CI and cloud/serverless environments, targeting developer workstations. The second-stage payload was attacker-hosted and cannot be reconstructed. Assume full compromise of anything reachable from a Node process with the user's permissions. Those who ran `npm install` against an affected checkout on a developer machine on or after 2026-05-18 15:57:18 should treat the machine as compromised, rotate every credential the machine could reach, audit account activity** since 2026-05-18 15:57:18, and clean local clones.

### CVE-2026-47754

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-22;CWE-862` |
| Published | 2026-08-10T16:19:47.797 |

Metacat is data repository software that helps researchers preserve, share, and discover data. Versions 2.x through 2.19.1 and all 1.x versions contain an unauthenticated path traversal in the `archiveEntryName` parameter of the `action=read` endpoint that is part of the original 1.x Metacat API. `ArchiveHandler.readArchiveEntry()` concatenates the user-supplied parameter into a filesystem path without validation, and the surrounding `hasReadPermission()` check is commented out. An unauthenticated remote attacker can read any file accessible to the Tomcat process by sending a single GET request. Proof-of-concept exploits have been demonstrated and verified against this vulnerability, and it should be considered easily exploitable for any Metacat deployment < 3.0.0 by any user with access to the 1.x API. Through this vulnerability, production 2.x deployments are exposed to credential theft, client certificate and private key exfiltration enabling member node impersonation within the federation, embargoed research data disclosure, and broad system reconnaissance. Given Metacat's deployment footprint across the DataONE network of repositories and federally funded research programs, the population of exposed 2.x instances is non-trivial. The vulnerability was eliminated in Metacat version 3.0.0 and after by eliminating the entire Metacat 1.x API that exposed this vulnerability. The vulnerability was remediated in April 2024 with the release of Metacat 3.0.0, which removed the legacy Metacat API including ArchiveHandler.java. The commit message and issue reference architectural cleanup, not a security fix, and no advisory or CVE was issued. The 2.x branch was not and will not be backported, as is standard practice in Metacat, which only supports the most current release. 2.19.1 remains vulnerable with identical code and is beyond its supported lifetime. As a workaround, disable or restrict 1.x API servlets. Because the vulnerable 1.x API is no longer used or necessary in most Metacat deployments, restricting access to the old API endpoints can reduce or eliminate exposure for 2.19.x deployments.  After removing those features, restart Tomcat or whichever software is hosting the servlets.

### CVE-2026-13738

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-11T12:17:37.923 |

CommServe contained an authorization bypass vulnerability affecting a limited set of command execution operations.  Software customers upgrade to resolved maintenance release.  Update all Commvault installations, including Commserve, Webserver, Command Center, Media Agents, Clients and HyperScale X.

### CVE-2026-13737

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-11T12:17:37.180 |

CommServe contained an allowlist bypass vulnerability affecting command execution authorization.  Software customers upgrade to resolved maintenance release. Update all Commvault installations, including Commserve, Webserver, Command Center, Media Agents, Clients and HyperScale X.

### CVE-2025-15681

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-10T20:17:25.157 |

TBEA TLogger V2.1.0.0B0.0.0.0 contains an authentication bypass in its web server. After a user has previously authenticated to the device, an unauthenticated attacker can directly access protected functionality through the /index.asp endpoint without providing valid credentials. This allows the attacker to access functionality intended for authenticated users and may expose or modify device configuration and data. Logging out from the bypassed state can additionally cause the web server to crash.

### CVE-2026-19516

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-11T06:17:13.433 |

A caller-supplied X-Grafana-URL request header controls the destination of mcp-grafana's outbound requests, and the grafana_api_request tool lets the caller also choose the HTTP method, path, and body. Because the destination is not restricted to the configured Grafana instance, a caller can direct requests at internal, loopback, and link-local network services (including metadata endpoints) and read the responses, resulting in server-side request forgery. The fix for CVE-2026-15583 prevented the configured service-account token from being sent to unintended destinations but did not restrict the destinations themselves.

### CVE-2026-13716

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-35` |
| Published | 2026-08-11T06:17:12.870 |

Path traversal in server import and admin file upload in Crafty Controller. Allows a remote, authenticated attacker to upload files to arbitrary paths permitted to the Crafty Controller application and perform remote code execution.

### CVE-2026-44758

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-11T01:17:20.670 |

SAP Manufacturing Integration and Intelligence (MII) allows an attacker with high privileges to submit specially crafted input to certain affected functionality, which is processed without sufficient validation. Successful exploitation could allow the attacker to execute arbitrary commands on the underlying operating system, resulting in high impact on confidentiality, integrity, and availability of the application.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-72772

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-08-11T13:19:07.623 |

n8n before 2.32.1 (and before 2.31.5) is vulnerable to account takeover via the Token Exchange Embed Login feature. When a validly-signed incoming token was matched to a local account by its email claim, the service did not verify that the email claim was verified, nor that the trusted key's permitted role ceiling covered that account. As a result, anyone able to obtain a token accepted by a configured trusted key (for example, a trusted issuer emitting unverified email addresses) could authenticate as any existing user and gain full account control. This issue only affects instances where the embed login feature is enabled and at least one trusted key source is configured.

### CVE-2026-72562

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-11T12:17:42.190 |

An SQL injection vulnerability in Pimcore admin-ui-classic-bundle through version 2.3 allows authenticated backend users to execute arbitrary SQL via the DataObject grid id column filter. The filter value is concatenated directly into the SQL WHERE clause without parameterization. An attacker with backend access can exfiltrate or modify all database contents.

### CVE-2026-72561

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-11T12:17:42.073 |

A broken access control vulnerability in Peppermint Lab Peppermint through commit ba6e217 allows any authenticated non-administrative user to reconfigure the platform global OIDC/SSO settings via an unprotected configuration endpoint. The endpoint performs no administrative role check before applying new OIDC issuer settings. An attacker can redirect all SSO logins to an attacker-controlled identity provider, enabling credential harvesting for all platform users.

### CVE-2026-72558

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-11T12:17:41.697 |

An SQL injection vulnerability in CiviCRM through 6.18.alpha1 allows authenticated staff to read the entire database via the contact search RLIKE clause. The clause concatenates a user-supplied value into the SQL query without sanitization. An attacker with staff-level access can exfiltrate all database contents including donor and member records.

### CVE-2026-72557

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-11T12:17:41.547 |

An unrestricted file upload vulnerability in Cockpit CMS 2.6.0 allows authenticated users to upload files of any extension including PHP scripts via the asset upload endpoint. The allowed_uploads configuration defaults to wildcard (*) and uploaded files are stored in a web-accessible directory. An attacker with any authenticated account can upload a PHP webshell and execute arbitrary OS commands on the server.

### CVE-2026-72556

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-11T12:17:41.377 |

A remote code execution vulnerability in ZoneMinder 1.39.17 allows any authenticated user to execute OS commands by exploiting a broken permission check in the Filter class. The canEdit() and canDelete() methods invoke nonexistent methods on the ZM\User class, causing PHP __call() to return a truthy value that bypasses the permission check for all users. Any authenticated user can trigger filter-based OS command execution regardless of their assigned role.

### CVE-2026-72551

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-11T12:17:40.733 |

A remote code execution vulnerability in Apioo Fusio 8.8.3 allows authenticated users with the Developer role to execute arbitrary OS commands by exploiting a PHP-Sandbox allow-list bypass. The sandbox allow-list permits functions that transitively invoke system(), enabling a developer to escape the sandbox and gain OS command execution on the server. An attacker with a Developer-role account can achieve full server compromise.

### CVE-2026-72538

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-11T12:17:39.100 |

An argument injection vulnerability in PrefectHQ Prefect through 3.8.2 allows authenticated users to achieve remote code execution via the git_clone pull step branch field. The branch parameter is passed directly to git pull without sanitization, enabling injection of arbitrary git arguments. This represents a distinct code path from the incomplete fix applied for CVE-2026-5366 and allows command execution on the Prefect server.

### CVE-2026-72537

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-11T12:17:38.977 |

A privilege escalation vulnerability in Authentik Security authentik through 2026.5.6 allows an attacker with a source-scoped SCIM provisioning token to take over any user account including superusers by provisioning a SCIM user that matches an existing local user by username. The SCIM user ingest function adopts pre-existing local accounts by username without validating scope boundaries. An attacker can rewrite or delete any account, including the superuser, using only a limited provisioning credential.

### CVE-2026-72534

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-11T12:17:38.610 |

A privilege escalation vulnerability in Authentik Security authentik through 2026.5.6 allows an attacker with a source-scoped SCIM provisioning token to gain superuser privileges by provisioning a SCIM group that matches an existing administrator group by name. The SCIM group ingest function adopts any existing group by name and replaces its membership without validating the source scope against the target group. An attacker can grant their provisioning token full IdP superuser access and lock out all existing administrators.

### CVE-2026-72533

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-11T12:17:38.487 |

An authentication bypass vulnerability in Portainer CE through 2.44.0 allows authenticated low-privileged users to bypass Docker proxy authorization checks via non-canonical URL normalization, defeating all authorization middleware. The proxy endpoint fails to normalize request paths before applying access controls, allowing crafted requests to be interpreted differently by the proxy and the authorization layer. Successful exploitation grants the attacker root-level access to the underlying Docker host.

### CVE-2026-13739

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-11T12:17:38.047 |

A legacy endpoint in Command Center contained an unauthenticated server-side request forgery (SSRF) vulnerability related to the handling of arbitrary target URLs.  Software customers upgrade to resolved maintenance release.  Update Command Center.

### CVE-2026-15555

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-11T09:17:12.540 |

A flaw was found in JBoss marshalling. The Infinispan session replication path deserializes replicated session data via the JBoss Marshalling River unmarshaller with no class filtering — enabling RCE via deserialization gadget chains on every cluster node.

### CVE-2026-58243

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-11T01:17:22.160 |

SAP ABAP Development Tools does not perform necessary authorization checks for certain functionality, allowing an attacker with low privileges to execute unauthorized database operations against SAP NetWeaver AS ABAP. Successful exploitation could allow the attacker to read sensitive data, modify application data, and disrupt access for legitimate users, resulting in high impact on confidentiality, integrity, and availability.

### CVE-2026-18982

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-08-10T21:17:21.833 |

A flaw was found in the RHOAI training-operator. This vulnerability allows a user with standard edit or admin roles in any Kubernetes namespace to escalate their privileges. Through the creation of training jobs, an attacker can impersonate service accounts, access the host filesystem, and potentially execute arbitrary code remotely. This issue arises from the aggregation of training job permissions onto native Kubernetes edit and admin ClusterRoles, coupled with unrestricted PodTemplateSpec passthrough.

### CVE-2026-18951

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-10T21:17:21.710 |

A flaw was found in the Red Hat OpenShift AI (RHOAI) overlay for the training operator. The RHOAI overlay incorrectly aggregates `trainjobs` management permissions into the native Kubernetes `edit ClusterRole`. This allows any user with `edit ClusterRole` permissions in a namespace to create, modify, and delete `TrainJobs`. When combined with a separate vulnerability (TRN-01) that permits arbitrary pod configurations, a remote attacker with namespace editor privileges could exploit this to escalate privileges, potentially leading to arbitrary code execution.

### CVE-2026-18950

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-10T21:17:21.583 |

A flaw was found in odh-dashboard. An authenticated user of the dashboard can exploit a vulnerability related to how RoleBindings are created. The system does not properly validate the `roleRef` field, allowing a user to specify an arbitrary role, including highly privileged ones like `cluster-admin`. This can lead to privilege escalation, where an attacker gains unauthorized elevated access within their namespace and potentially persistent control over the system.

### CVE-2026-18949

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-08-10T21:17:21.443 |

A flaw was found in odh-dashboard. This vulnerability allows an attacker, who has compromised the dashboard's Service Account (SA) token, to exploit overly broad permissions granted to the SA. This enables the attacker to escalate their privileges to cluster-administrator level, gain access to sensitive data like credentials and keys across the entire cluster, and disrupt multi-tenant isolation.

### CVE-2026-18617

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-915` |
| Published | 2026-08-10T21:17:20.250 |

A flaw was found in the Data Science Pipelines Operator (DSPO). A namespace editor can exploit a vulnerability in the spec.database.customExtraParams field, which allows for the injection of dangerous parameters into the MySQL Data Source Name (DSN) string. By manipulating these parameters, an attacker can enable LOCAL INFILE functionality and exfiltrate sensitive files, such as the service account token, from the operator pod. This can lead to privilege escalation, allowing a namespace editor to gain cluster-admin privileges.

### CVE-2026-13717

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-10T21:17:19.343 |

A flaw was found in the Red Hat OpenShift AI (RHOAI) MaaS Gateway. Improper configuration of the Gateway in a model-serving context allows a standard user with low privileges to intercept, read, log, and alter all MaaS model traffic. This includes sensitive information such as access keys, input prompts, and outputs, leading to significant information disclosure and data tampering.

### CVE-2026-72883

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-10T20:17:35.003 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, the WebSocket handlers in apps/dokploy/server/wss/terminal.ts, apps/dokploy/server/wss/docker-container-terminal.ts, apps/dokploy/server/wss/docker-container-logs.ts, and apps/dokploy/server/wss/docker-stats.ts validate organization membership but do not enforce checkServiceAccess, accessedServerIds, or accessedServices, allowing an authenticated organization member to obtain root terminal access and read logs or statistics for restricted servers and services. This issue is fixed in version 0.29.13.

### CVE-2026-72875

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T20:17:33.830 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, settings.readTraefikFile in apps/dokploy/server/api/routers/settings.ts passes a path accepted by apiReadTraefikConfig to readConfigInPath in packages/server/src/utils/traefik/application.ts, where configPath is interpolated into execAsyncRemote as cat ${configPath}, allowing a user with traefikFiles.read permission to execute arbitrary commands on a managed server through shell metacharacters. This issue is fixed in version 0.29.13.

### CVE-2025-15683

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-306` |
| Published | 2026-08-10T20:17:25.420 |

TBEA TLogger V2.1.0.0B0.0.0.0 contains multiple unauthenticated denial-of-service vulnerabilities in its web server. An unauthenticated remote attacker can invoke specific HTTP endpoints to reboot or reset the device, clear application data, or terminate the web server through a segmentation fault. In addition, multiple action endpoints process attacker-controlled parameters using unsafe string operations such as sprintf() and strcat() without adequate bounds checking, allowing crafted input to trigger buffer overflows and crash the web server. The affected endpoints include onRestart, onReset, ClearData, uploadInvFile, getIndiaRPData, YearCaparity, TotalfaultData, recordData, InvHistoryData, CollectHistoryData, InvFaultData, GetPortTableByParm, and UpdatePortConfig.

### CVE-2026-72866

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-10T19:17:35.303 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, the WebSocket handler in apps/dokploy/server/wss/terminal.ts validates a session but does not authorize access to the requested server. An authenticated user can connect to /terminal?serverId=local, select the special serverId=local branch, and obtain an interactive terminal on the Dokploy host without an organization role or server-access check. This issue is fixed in version 0.29.13.

### CVE-2026-72781

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-11T13:19:08.657 |

Craft CMS versions >= 5.0.0-RC1 before 5.10.7 and >= 4.0.0-RC1 before 4.18.3 contain a remote code execution vulnerability in the Twig sandbox mechanism. Because Craft marks the ElementInterface as safe (via the AllowedInSandbox attribute) and the sandbox allowlisting extends to the entire class hierarchy (craft\base\Component up to yii\base\Component), an authenticated attacker with permission to access the control panel can render a malicious Twig template that abuses the yii\base\Component arbitrary function-call gadget to execute arbitrary code, even when the Twig sandbox is enabled via enableTwigSandbox().

### CVE-2026-72779

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-08-11T13:19:08.360 |

Craft CMS 5.0.0-RC1 before 5.10.6 and 4.0.0-RC1 before 4.18.2 contain an arbitrary file read vulnerability. The create() Twig function restricts class instantiation using a 5-entry blocklist that does not include SplFileObject, allowing an authenticated administrator (with allowAdminChanges=true) to configure a malicious entry type title or URI format that instantiates SplFileObject in a non-sandboxed template context. When a user subsequently creates an entry in the affected section, arbitrary files on the server (such as .env containing the security key and database credentials) are read and rendered as entry titles.

### CVE-2026-72778

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-08-11T13:19:08.207 |

Craft CMS versions from 4.0.0-RC1 before 4.18.2 and from 5.0.0-RC1 before 5.10.6 contain an authenticated remote code execution vulnerability in the control panel element-search condition handling. Craft cleanses the outer request-controlled condition array via Component::cleanseConfig(), but Conditions::createCondition() later decodes and merges the JSON string in condition.config without re-running cleanseConfig() on the decoded configuration. Because condition.config is a JSON string during the first cleanse, Yii special config keys such as 'as ...' and 'on ...' can be hidden inside it and, after JSON decoding, are interpreted by Yii as behavior/event configuration during FieldLayout object creation. An attacker with an authenticated control panel session (and a valid CSRF token) can exploit this to execute operating system commands as the PHP/web user.

### CVE-2026-72767

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-11T13:19:06.940 |

n8n before 1.123.67, 2.x before 2.31.5, and 2.32.x before 2.32.1 contain a remote code execution vulnerability in the Git node. Authenticated users with rights to create and execute workflows can stage a crafted local repository that causes git to run hooks under default git security settings, executing arbitrary commands as the n8n process user. Both self-hosted and cloud instances are affected.

### CVE-2026-72765

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-11T13:19:06.670 |

n8n before 2.31.5 and before 2.32.1 contain a sandbox escape vulnerability in expression evaluation. An authenticated user with permission to create or modify workflows can craft expressions using arrow-function bodies to bypass the expression sandbox, triggering system command execution on the host running n8n. The issue is fixed in versions 2.31.5 and 2.32.1.

### CVE-2026-72746

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-11T13:19:05.520 |

FreeRDP before 3.30.0 contains a server-side authentication bypass in the RDSTLS handshake. When a server is configured with RdstlsSecurity = TRUE, the handshake dispatches inbound PDUs based solely on the attacker-supplied wire pduType without verifying that the received PDU is the one required at the current step. Because the rdpRdstls object is calloc-zeroed, its resultCode defaults to 0 (RDSTLS_RESULT_SUCCESS). An unauthenticated remote client can send a Capabilities PDU instead of the required Authentication Request PDU; rdstls_process_capabilities() returns success without ever setting resultCode, so the server responds with an AUTHRSP carrying resultCode SUCCESS and treats the session as authenticated without evaluating any password, redirection GUID, or auto-reconnect cookie. This affects the released FreeRDP 3.x series (e.g., 3.27.1) and master HEAD; at the time of the advisory no patched version was available.

### CVE-2026-72745

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T13:19:05.370 |

FreeRDP before 3.30.0 contains an out-of-bounds vulnerability in kerberos_DecryptMessage() (winpr/libwinpr/sspi/Kerberos/kerberos.c). The 16-bit EC (extra count) field of a peer-supplied GSS Wrap token (RFC 4121) is used directly in pointer arithmetic to locate the encrypted regions without being bounds-checked, while only RRC and the total buffer length are validated. A malicious peer (server or client) can supply a large EC value (up to 0xFFFF) during CredSSP/NLA authentication, moving the decrypt operation's base pointers past the end of the ~60-byte token buffer. Because the AES-CTS-HMAC enctypes decrypt in place before the HMAC integrity check, this results in an out-of-bounds read and in-place out-of-bounds write, potentially leading to information disclosure, memory corruption, or denial of service.

### CVE-2026-69109

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-35` |
| Published | 2026-08-11T13:19:02.030 |

A vulnerability has been identified in Siemens License Server (SLS) (All versions < V5.3). The affected application is vulnerable to a path traversal vulnerability due to lack of sanitization of user input. This could allow a remote attacker to access arbitrary files on the application.

### CVE-2026-73160

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-11T09:17:15.030 |

Affected versions of cti-transmute contain an SSRF vulnerability in the /fetch_misp_event and /misp_search_events endpoints.


The URL validation routine checked whether a supplied hostname was itself an IP literal and rejected private, loopback, link-local, or reserved IPs. However, ordinary domain names were accepted without resolving them first. An attacker could therefore use a hostname whose DNS record pointed to an internal address and cause the cti-transmute server to issue requests into its internal network. The commit explicitly states that anonymous callers could make the server request the internal target and read the response.


The fix resolves hostnames using socket.getaddrinfo(), checks that every resolved address is globally routable, and additionally places @login_required on both affected MISP fetch/search routes.

### CVE-2026-19424

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-11T03:17:36.157 |

Chiline Cloud developed by Inventec Appliances has a Insecure Direct Object Reference vulnerability. Unauthenticated remote attackers can modify a specific parameter to read other users' sensitive data.

### CVE-2025-30237

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-10T23:16:48.640 |

The affected TP-Link Aginet devices contain a flaw in the web management interface where authentication
checks are not consistently enforced on certain endpoints. An attacker can send
specially crafted requests to bypass authentication and directly invoke
privileged functionality without valid credentials. This issue arises from
improper enforcement of access control mechanisms on sensitive operations.





Successful
exploitation may allow an unauthenticated attacker to execute privileged
operations and gain full control of the device.

### CVE-2026-18608

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-250` |
| Published | 2026-08-10T21:17:19.990 |

A flaw was found in the Data Science Pipelines Operator (DSPO). The operator's ClusterRole, which defines its permissions, includes extensive privileges beyond what is necessary for its operation. These excessive permissions, such as the ability to execute commands within pods and manage cluster-wide roles, could be exploited. If the DSPO pod were compromised, an attacker could leverage these privileges to gain full administrative control over the entire Kubernetes cluster.

### CVE-2026-72884

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T20:17:35.140 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, sanitizeCommand in packages/server/src/utils/builders/compose.ts only trims whitespace and strips surrounding quotes from compose.command before exportEnvCommand and docker command interpolation, allowing an authenticated user who can update a Compose service to inject shell metacharacters and execute arbitrary commands on the Dokploy host. This issue is fixed in version 0.29.13.

### CVE-2026-72874

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T20:17:33.690 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, cloneGitRepository in packages/server/src/utils/providers/git.ts interpolates customGitUrl and customGitBranch into a git clone command passed to execAsync or execAsyncRemote, allowing an authenticated user with application access to execute arbitrary operating system commands on the Dokploy host by setting a malicious custom Git URL and triggering deployment. This issue is fixed in version 0.29.13.

### CVE-2026-71966

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T20:17:32.723 |

CyberPanel 2.4.3, fixed in commit eca0c3c, contains an authenticated command injection vulnerability in the remote backup transfer feature that allows authenticated attackers to execute arbitrary OS commands by controlling a remote server's API response. Attackers can inject malicious commands through a crafted directory name in the remote server's API response, which bypasses security middleware validation and is passed unsanitized to the OS command execution function.

### CVE-2026-71965

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-10T20:17:32.580 |

CyberPanel 2.4.3, fixed in commit eca0c3c, contains an authenticated remote code execution vulnerability in the remote backup feature that allows authenticated attackers to gain root-level SSH access by supplying a malicious remote server address. Attackers can exploit the unverified SSH public key retrieval process to write an attacker-controlled public key directly to /root/.ssh/authorized_keys, granting persistent root access to the host system.

### CVE-2026-69118

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863;CWE-1336` |
| Published | 2026-08-10T20:17:32.310 |

Cachet through 2.4.1 contains a server-side template injection vulnerability in incident template rendering that allows authenticated users to execute arbitrary PHP code. Attackers can create malicious incident templates with Blade directives or Twig filters that execute system commands when incidents are created, achieving remote code execution as the web server process.

### CVE-2025-15682

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-10T20:17:25.290 |

TBEA TLogger V2.1.0.0B0.0.0.0 contains an unauthenticated resource exhaustion vulnerability in its web server. An unauthenticated remote attacker can send PUT requests to the /tmp/ endpoint, causing the web server to create persistent files containing attacker-controlled data under /opt/myapp/webserver/. The generated files are not removed because the web server attempts to move them into a non-existent directory. Repeated requests can therefore exhaust available storage and cause a denial-of-service condition.

### CVE-2026-72870

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T19:17:35.897 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, the buildRemoteDocker() function in packages/server/src/utils/providers/docker.ts interpolates the application-controlled dockerImage value directly into a docker pull shell command. An authenticated user with project access can set a crafted dockerImage through application.update and trigger application.deploy, causing execAsync() to execute arbitrary operating-system commands as the Dokploy server process. This issue is fixed in version 0.29.13.

### CVE-2026-71962

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-10T19:17:31.400 |

Flowise versions 2.2.4 through 3.1.4 contain a missing authorization vulnerability in the POST /api/v1/openai-assistants-file/download endpoint that allows unauthenticated attackers to access private files by exploiting the endpoint's inclusion in the global authentication whitelist, which bypasses all session and API key verification. Attackers can supply valid chatflowId, chatId, and fileName identifiers to retrieve files from any chatflow on the instance, including private chatflows belonging to other workspaces or organizations.

### CVE-2026-72730

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-10T17:17:37.507 |

Discourse is an open-source discussion platform. Prior to 2026.1.6, 2026.5.2, 2026.6.1, and 2026.7.0, the Rich Text Editor rendered a chat-transcript username as HTML, allowing stored cross-site scripting. This issue is fixed in versions 2026.1.6, 2026.5.2, 2026.6.1, and 2026.7.0.

### CVE-2026-19539

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-11T14:17:13.580 |

Authorization Bypass Through User-Controlled Key in the ticket management component in Roskus Prospero Flow CRM before 5.4.9 allows authenticated users of any company to read the full content (title, description, and attachments) of tickets belonging to another company, to hijack another company's tickets by reassigning their company_id, and to delete another company's tickets without any authorization check, via the ticket's numeric identifier, because the read and save operations retrieve the record without constraining the query to the authenticated user's company, and the delete controller type-hints a generic Illuminate\Http\Request instead of the TicketDeleteRequest that would enforce the required permission.

### CVE-2026-72536

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-11T12:17:38.857 |

A missing authentication vulnerability in Chaskiq through commit 46dfdd1 allows unauthenticated remote attackers to manipulate any tenant Stripe subscription via the stripeCreateIntent GraphQL mutation. The mutation lacks authentication and authorization checks, exposing Stripe payment intent creation to unauthenticated callers. An attacker can create payment intents and alter billing for any tenant without credentials.

### CVE-2026-72535

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-11T12:17:38.733 |

A missing authentication vulnerability in Chaskiq through commit 46dfdd1 allows unauthenticated remote attackers to mint Stripe Billing Portal sessions for any tenant via the stripeCustomerPortal GraphQL mutation. The mutation performs no authentication or authorization checks before creating a customer portal session linked to any tenant Stripe account. An attacker can access and manage subscription data for any tenant without credentials.

### CVE-2025-30241

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T23:16:50.670 |

Certain web
interface components in affected TP-Link Aginet devices do not validate and sanitize user-supplied input properly before
passing it to system-level command execution functions.  An authenticated adjacent attacker may inject
specially crafted input to execute arbitrary operation system commands with
elevated privileges.









Successful
exploitation may allow execution of arbitrary system commands, potentially
leading to full device compromise.

### CVE-2025-30238

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-10T23:16:49.900 |

In affected TP-Link Aginet devices, insufficient
authorization validation allows authenticated low-privileged users to execute higher-privileged
operations.





An attacker
may perform administrative actions such as creating privileged accounts or
modifying critical configuration settings.

### CVE-2026-10754

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-10T18:17:39.053 |

Pega Platform versions 8.5.0 through 25.1.2 are affected by an improper validation of cryptographic signatures that may allow an attacker to bypass security controls.

### CVE-2026-19433

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-10T15:17:43.330 |

Authorization Bypass Through User-Controlled Key in the contact management component in Roskus Prospero Flow CRM before 5.4.8 allows authenticated users of any company to blindly overwrite the contact data of another company and to download that contact's personal data as a vCard via the contact's numeric identifier, because the save and export operations retrieve the record without constraining the query to the authenticated user's company.

### CVE-2026-16053

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-08-11T07:17:28.233 |

Zohocorp ManageEngine M365 Manager Plus and M365 Security Plus versions below 4820 are affected to Authenticated Path Traversal vulnerability in Exchange Online backup module.

### CVE-2025-30239

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-08-10T23:16:50.173 |

In affected TP-Link Aginet devices, use of
hardcoded cryptographic keys embedded in the firmware to protect sensitive
configuration data may allow an attacker who has access to device storage to
recover the keys and decrypt stored data.





Successful
exploitation may allow access to decrypted sensitive configuration data,
including credentials and service-related information.

### CVE-2026-18947

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-08-10T21:17:21.130 |

A flaw was found in Feast. An authorization bypass vulnerability exists in the /materialize and /materialize-incremental endpoints. By sending a specially crafted request that omits the feature_views field, an attacker can bypass intended permission checks. This allows an unauthenticated remote attacker, or any authenticated user, to trigger a full re-materialization of all feature views. The consequence is a Denial of Service (DoS) due to data corruption and significant resource consumption across all tenants.

### CVE-2026-71576

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-10T17:17:36.060 |

A flaw was found in multicluster-global-hub. The manager component improperly validates the source identity of incoming CloudEvents on Kafka status topics. A remote attacker, after compromising a managed hub and obtaining its Kafka client certificate, can manipulate the self-asserted source identity. This allows the attacker to falsify or delete critical data, such as compliance, inventory, and cluster health information, belonging to other hubs in the database.

### CVE-2026-8917

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-822` |
| Published | 2026-08-11T03:18:01.900 |

Untrusted Pointer Dereference in ASUS GPU Tweak III, GPUTweakII, AI Suite3, and VGAdll: An IOCTL vulnerability allows a local attacker to write a specific value to an arbitrary memory address, potentially leading to privilege escalation.
Refer to the ' 
Security Update for ASUS GPU Tweak III, GPU Tweak II, AI Suite 3, and Armoury Crate Security Bulletin   ' section on the ASUS Security Advisory for more information.

### CVE-2026-8718

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-10T23:16:51.587 |

tls_opt_dtls_peer_connection_id_value_get() in subsys/net/lib/sockets/sockets_tls.c, which handles getsockopt(SOL_TLS, TLS_DTLS_PEER_CID_VALUE), passed the caller-supplied optval directly to mbedtls_ssl_get_peer_cid() without verifying the buffer was at least MBEDTLS_SSL_CID_OUT_LEN_MAX (default 32) bytes. mbedtls_ssl_get_peer_cid() copies the peer-negotiated DTLS Connection ID (length 1..MBEDTLS_SSL_CID_OUT_LEN_MAX) into that buffer without a destination-size parameter, so a caller-supplied optlen smaller than the CID causes a write of up to 31 bytes past the buffer end.

In CONFIG_USERSPACE builds the getsockopt syscall verifier (z_vrfy_zsock_getsockopt) bounce-buffers the user's optval into a kernel allocation of exactly optlen bytes (k_usermode_alloc_from_copy -> z_thread_malloc), so an unprivileged user thread that passes a small optlen on a connected DTLS socket with Connection ID enabled induces a kernel-heap buffer overflow, with the overflowing content being the remote peer's CID.

The defect requires CONFIG_MBEDTLS_SSL_DTLS_CONNECTION_ID, an established DTLS session with a negotiated peer CID, and (for the kernel-crossing case) CONFIG_USERSPACE. Introduced when the TLS_DTLS_CID option was added (v3.5.0).

The fix rejects callers whose optlen is below MBEDTLS_SSL_CID_OUT_LEN_MAX with -EINVAL.

### CVE-2026-71969

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-124;CWE-787` |
| Published | 2026-08-10T19:17:32.400 |

OP-TEE OS through 4.10.0, fixed in commit 7b8b494, contains a buffer underwrite vulnerability in the RSA NOPAD encrypt and decrypt operations within the mbedTLS software backend and SE050 hardware driver that allows a malicious Trusted Application to corrupt secure-world heap memory by supplying an input length exceeding the RSA modulus size. When src_len exceeds rsa_len, the subtraction expression wraps to a large unsigned value, causing a subsequent memcpy to write attacker-controlled data before the destination buffer in S-EL1 secure-world heap memory.

### CVE-2026-71968

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-08-10T19:17:32.263 |

OP-TEE OS through 4.10.0, fixed in commit 8794043, contains a use-after-free vulnerability in the Trusted Application loader that allows attackers with the ability to load a signed Trusted Application to corrupt secure-world kernel memory by setting the TA_FLAG_CONCURRENT flag in a user TA signed header. Attackers can cause two concurrent sessions to operate on the same shared context without locking, corrupting the uctx->vm_info.regions list during memref parameter mapping and unmapping to free vm_region nodes still in use, resulting in a use-after-free in S-EL1 secure-world kernel memory.

### CVE-2026-72734

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-10T18:18:51.823 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). From 0.28.7 until 0.29.13, the server.remove tRPC mutation in apps/dokploy/server/api/routers/server.ts accepts a caller-controlled serverId and calls haveActiveServices, findServerById, removeDeploymentsByServerId, and deleteServer without verifying that currentServer.organizationId equals ctx.session.activeOrganizationId. An authenticated owner or administrator with server:delete in one organization who previously observed another organization's serverId can delete that organization's server registration and deployment records, interrupt Dokploy management, and receive the associated plaintext SSH private key even though server.one denies the same cross-organization read. This issue is fixed in version 0.29.13.

### CVE-2026-69108

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-08-11T13:19:01.883 |

A vulnerability has been identified in Siemens License Server (SLS) (All versions < V5.1). The affected application is vulnerable to a local privilege escalation due to an insecure sudoers policy. This could allow an attacker to execute arbitrary commands and plant malicious files as root, leading to full system compromise.

### CVE-2026-72766

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-11T13:19:06.807 |

n8n before 1.123.67, 2.x before 2.31.5, and 2.32.x before 2.32.1 contain a type confusion vulnerability in the Send Email node, which does not enforce that its message fields are strings. A crafted non-string value supplied from a workflow expression into the text or HTML body field can be interpreted by the underlying mail library (Nodemailer) as a file path or URL, allowing arbitrary local file disclosure and server-side request forgery (SSRF). Exploitation requires a pre-existing active workflow with an unauthenticated webhook, valid SMTP credentials configured on the node, and untrusted input mapped directly into the body field; this is not a default configuration.

### CVE-2026-14886

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-10T20:17:26.683 |

Vault Enterprise's identity entity batch-delete endpoint is vulnerable to a cross-namespace authorization bypass that may allow an authenticated caller in one namespace to permanently delete the storage backing of entities belonging to another namespace. This vulnerability (CVE-2026-14886) is fixed in Vault Enterprise 2.0.4, 1.21.9, 1.20.14 and 1.19.20.

### CVE-2026-72596

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-11T12:17:42.543 |

A broken access control vulnerability in Ghost Foundation Ghost 5.x allows authenticated Author-role users to delete posts owned by other users. The post model permissible() cascade is missing the branch that handles the combined isAuthor and isDestroy condition, causing the authorization check to fall through and permit the deletion. An attacker with an Author account can delete any post on the platform.

### CVE-2026-72595

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-11T12:17:42.430 |

A broken access control vulnerability in BadChoice Handesk as of 2026-07-10 allows any authenticated agent to update ticket records belonging to other teams via the TicketsController@update endpoint. The endpoint calls no authorize() method and performs no team-scoped ownership check. An attacker with any agent account can modify, escalate, or corrupt tickets assigned to other teams.

### CVE-2026-72563

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-11T12:17:42.310 |

A broken access control vulnerability in BadChoice Handesk as of 2026-07-10 allows any authenticated agent to overwrite lead records belonging to other teams via the LeadsController@update endpoint. The endpoint performs no authorization check, and the Lead model has guarded set to an empty array making all columns mass-assignable. An attacker with any agent account can corrupt lead data across team boundaries.

### CVE-2026-72555

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-11T12:17:41.240 |

A broken access control vulnerability in Peppermint Lab Peppermint through commit ba6e217 exists because the Config.roles_active flag defaults to false, causing all permission checks on ticket, client, and user handlers to behave as no-ops on default installations. All authenticated users bypass ownership and administrative access controls. An attacker with any user account can read, modify, or delete tickets, clients, and users belonging to any other account.

### CVE-2026-15560

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-08-11T09:17:12.823 |

when EAP runs with -secmgr, the openjdk-orb's JDKBridge honours attacker-supplied CDR codebase URLs during object unmarshalling on :3528, allowing an unauthenticated attacker to load and instantiate arbitrary classes from a remote URL in the server JVM before EJB security interceptors run.

### CVE-2026-15556

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-11T09:17:12.687 |

A flaw was found in Picketlink's SP signature validation; a SAML response containing zero assertion elements matching the signature check can allow an attacker to forge a SAML response and auth as any principal with any roles on the protected application.

### CVE-2026-72903

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-10T21:17:24.980 |

Tabby (formerly Terminus) is a highly configurable terminal emulator. Prior to 1.0.235, a malicious SFTP server can return a backslash traversal filename through entry.name. In tabby-ssh/src/session/sftp.ts, SFTPSession.readdir() and _makeFile() use POSIX path processing that preserves the backslashes as ordinary filename characters. In tabby-ssh/src/components/sftpPanel.component.ts, downloadFolderRecursive() propagates item.name into the local relative path. In tabby-electron/src/services/platform.service.ts, ElectronDirectoryDownload.createFile() passes that path to Windows-native path.join(), and in tabby-electron/src/sftpContextMenu.ts, EditSFTPContextMenu.edit() passes item.name to path.join() for the temporary edit path. Windows interprets the preserved backslashes and parent-directory components as traversal, allowing attacker-controlled content to be created or overwritten outside the selected download directory or temporary edit directory. This issue is fixed in version 1.0.235.

### CVE-2026-15467

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-10T21:17:19.617 |

A flaw was found in the trustyai-service-operator's LMEvalJob controller. An authenticated user within the cluster can exploit this vulnerability by configuring a sidecar container to bypass existing security policies. This allows the user to enable and execute untrusted remote code, leading to arbitrary code execution within the cluster.

### CVE-2026-15581

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-10T21:17:19.743 |

A flaw was found in the TrustyAI Service (TAS) deployment. This vulnerability allows any pod on the cluster network to bypass authentication and directly access the TAS backend API. An attacker can exploit this to read, tamper with, or delete monitoring data and configurations, and inject arbitrary data into the service, potentially disrupting tenant operations.

### CVE-2026-66763

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-321` |
| Published | 2026-08-11T01:17:23.000 |

SAP BusinessObjects Business Intelligence Platform stores certain sensitive credentials associated with user objects using a hard-coded cryptographic key. An attacker with high privileges and local access to the server could retrieve these objects and decrypt the stored credentials. Successful exploitation could allow the attacker to obtain sensitive authentication data and modify protected information, resulting in a high impact on confidentiality and integrity. There is no impact on availability.

### CVE-2026-72693

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-11T09:17:14.340 |

`openvt -u` is intended to identify the owner of the current VT and then execute `login` as that user from a privileged context. In the documented `kbrequest`/init usage, the ownership test in `authenticate_user()` relies on `stat("/proc/<pid>/fd/0")`. `stat()` on `/proc/<pid>/fd/0` follows the symlink to the underlying TTY device node. As a result, `buf.st_uid` reflects the owner of the TTY node rather than the owner of the process holding the file descriptor. If the TTY owner returns to `root` or the getty owner after logout while an unprivileged process still has `fd 0` attached to that TTY, the check can incorrectly treat that process as belonging to the privileged console owner. Once that check succeeds, the `-u` path executes a passwordless login as the selected user. In the documented `kbrequest`/init deployment using `openvt -us`, this can result in passwordless `login -f root` on the spawned VT. This report establishes that privilege escalation path for that documented deployment; it does not claim equivalent reachability for deployments that do not use `openvt -u` from a privileged `kbrequest`/init path.

### CVE-2026-63622

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-10T21:17:23.550 |

A flaw was found in libvirt. A local attacker, specifically a process running as the confined `swtpm` user, could exploit a symlink-following vulnerability in the `virFileChownFiles()` function. By planting a symbolic link within the `swtpm` state directory, the attacker could trick the root-level libvirt daemon into changing the ownership of an arbitrary file to the `swtpm` user. This allows for privilege escalation from the `swtpm` sandbox to root-level file ownership control.

### CVE-2026-72762

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-11T13:19:06.230 |

n8n versions before 1.123.67, 2.31.5, and 2.32.1 contain an arbitrary file write vulnerability in the Edit Image node, which passes its output format parameter to the underlying image library without validation. An authenticated user able to run workflows can supply a crafted format value to write arbitrary files outside the node's working directory on the n8n instance.

### CVE-2026-18941

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-10T21:17:20.777 |

A flaw was found in Feast and feast-operator. The default configuration for both the Feast SDK and the feast-operator is "no_auth," meaning no security manager is installed. This default allows unauthenticated and unauthorized access to feature-server, registry-server, and offline-server endpoints. A remote attacker, by exploiting this missing authentication, could achieve remote code execution (RCE) by storing a malicious User-Defined Function (UDF) on the feature-server, trigger a denial of service (DoS) by forcing re-materialization of all tenant features, and gain unauthorized access to cross-tenant data.

### CVE-2026-66738

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-10T16:19:48.607 |

SPIP before 4.4.18 contains a code injection vulnerability in SQLite-backed installations. The navigation menu endpoint improperly handles array-typed user input, which bypasses input sanitization and allows the value to break out of an internal quoted string context when evaluated as PHP. An authenticated attacker with at minimum editor (redacteur) privileges can submit a single crafted GET request to /ecrire/?exec=navigation to execute arbitrary OS commands in the web server process. MySQL-backed installations are not affected.

### CVE-2026-44763

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-11T01:17:20.930 |

SAP Manufacturing Integration and Intelligence allows a privileged attacker to exploit insufficient file path validation in certain functions using specially crafted input. Exploitation also requires a legitimate user to subsequently access the attacker-influenced content and depends on conditions outside the attacker�s control. Successful exploitation could allow files to be written outside the intended directory and affect other components, resulting in a high impact on confidentiality, integrity, and availability.

### CVE-2026-18621

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-10T21:17:20.617 |

A flaw was found in Data Science Pipelines (DSP). An attacker with namespace editor privileges can bypass security hardening by submitting a malicious Argo Workflow through the V1 API path. This allows the API server to create pods with elevated privileges, acting as a 'confused deputy' on behalf of the attacker. Successful exploitation grants the attacker node-root access, enabling arbitrary code execution and full control over the underlying node.

### CVE-2026-72606

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-11T12:17:43.743 |

A server-side request forgery vulnerability in Pinry through 2.1.13 allows unauthenticated remote attackers to make the server issue HTTP requests to arbitrary internal or external hosts via the pin-from-URL feature. The feature passes the user-supplied URL directly to requests.get() without host or IP validation, and ALLOW_NEW_REGISTRATIONS defaults to true enabling anonymous triggering. An attacker can reach internal services or cloud metadata endpoints from the server.

### CVE-2026-72605

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-11T12:17:43.623 |

A missing authentication vulnerability in Swing Music 3.0.0 allows unauthenticated remote attackers to create arbitrary user accounts via the POST /auth/profile/create endpoint. The endpoint is allowlisted from JWT verification, permitting unauthenticated account creation. An attacker can register an account and use it to access protected functionality on the server.

### CVE-2026-72602

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-11T12:17:43.267 |

A path traversal vulnerability in AsyncFuncAI deepwiki-open through commit 16f35a0 allows unauthenticated remote attackers to obtain directory listings for arbitrary filesystem paths via the local-repository structure endpoint. The endpoint accepts an absolute filesystem path parameter and returns a directory listing without authentication, as WIKI_AUTH_MODE defaults to false. An attacker can enumerate sensitive directory contents on the host system.

### CVE-2026-72601

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-11T12:17:43.143 |

A broken access control vulnerability in CSZ CMS 1.3.2 allows unauthenticated remote attackers to read all form submissions including personally identifiable information via the admin form-submission viewer. The viewer endpoint lacks an authentication check and the framework authentication helper fails open. An unauthenticated attacker can access all contact form submissions without credentials.

### CVE-2026-72600

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-11T12:17:43.023 |

A broken access control vulnerability in Idurar IDURAR ERP CRM 4.1.0 allows unauthenticated remote attackers to download invoice PDF files containing customer PII via the /download router. The router is mounted without authentication middleware, making it publicly accessible. An attacker can enumerate MongoDB ObjectIds to download any invoice in the system without credentials.

### CVE-2026-72552

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-11T12:17:40.860 |

A server-side request forgery vulnerability in Dub as of 2026-07-10 allows unauthenticated remote attackers to make the server issue HTTP requests to arbitrary internal or external hosts via the metatags edge endpoint. The endpoint fetches any caller-supplied URL without applying a denylist or requiring authentication. An attacker can use this to scan internal services or exfiltrate data from cloud metadata endpoints.

### CVE-2026-72548

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-11T12:17:40.357 |

An information disclosure vulnerability in OpenSignLabs OpenSign through 2.37.0 allows unauthenticated remote attackers to retrieve any organisation tenant record via the gettenant Parse cloud function. The function accepts a contactId parameter and returns the full tenant record without authentication or authorization checks. An attacker can enumerate and disclose tenant configuration data for any organisation in the system.

### CVE-2026-72545

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-11T12:17:39.987 |

An insecure direct object reference vulnerability in OpenSignLabs OpenSign through 2.37.0 allows unauthenticated remote attackers to write to any contact record via the updatecontacttour Parse cloud function. The function performs no authentication or authorization before updating the target contact record. An attacker can corrupt or overwrite contact data for any user in the system without credentials.

### CVE-2026-72544

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-11T12:17:39.847 |

An integrity verification vulnerability in OpenSignLabs OpenSign through 2.37.0 allows unauthenticated remote attackers to forge document audit-trail entries via the triggerevent Parse cloud function. The function accepts viewer identity and IP address as caller-supplied parameters without authentication, allowing fabrication of arbitrary audit log entries. An attacker can tamper with the legal audit trail of any signed document, undermining non-repudiation.

### CVE-2026-72543

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-11T12:17:39.727 |

An insecure direct object reference vulnerability in OpenSignLabs OpenSign through 2.37.0 allows unauthenticated remote attackers to retrieve any contact record via the getcontact Parse cloud function. The function executes with useMasterKey and performs no authentication or authorization checks before returning the requested contact object. An attacker can enumerate and read all contact records including personally identifiable information without credentials.

### CVE-2026-71217

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-11T09:17:14.057 |

A flaw was found in iperf3. A remote attacker can exploit this vulnerability by sending crafted control-channel JSON with oversized numeric parameters, such as `parallel` and `len`, which are not properly validated by the server. This improper input validation can lead to excessive stream and thread creation, as well as large buffer allocations, causing resource exhaustion. Consequently, this can result in a Denial of Service (DoS) on the affected iperf3 server.

### CVE-2026-15567

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-11T09:17:13.530 |

A flaw was found in Wildfly. A remote unauthenticated attacker can trigger OutOfMemoryError as CSIv2Util's GSS token decoder reads an attacker-controlled length field without bounds checking and attempts to allocate a byte array of that size.

### CVE-2026-15565

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-11T09:17:13.370 |

A flaw was found in Undertow. A remote attacker can cause Out of Memory on websockets endpoint without authentication on any @ServerEndpoint class that has any @OnMessage method. This allows an attacker to cause Denial of Service attack without authentication and using only a standard WebSocket handshake.

### CVE-2026-15562

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-11T09:17:13.100 |

A flaw was found in EAP's jboss-remoting. A remote unauthenticated attacker who can reach :8080 (or :9990, or :4447) and complete an Upgrade: jboss-remoting handshake can cause OOM errors that degrade requests server-wide, leading to denial of service.

### CVE-2026-15561

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-11T09:17:12.963 |

A flaw was found in EAP's undertow http/1.1 chunked-transfer decoder. missing limits on size and count would allow an attacker to use an unauthenticated connection to drive the JVM to an OutOfMemory error, stopping all deployments on the listener, and achieving Denial of Service.

### CVE-2026-72915

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-10T22:17:10.360 |

Mastodon is a free, open-source social network server based on ActivityPub. From 4.6.0-beta.1 until 4.6.4 and 4.7.0-beta.1, any logged-in local user could use the show action in app/controllers/admin/collections_controller.rb to access personally identifying information about another local user in a collection because the controller used the general collection policy instead of the admin collection policy namespace. The exposed data included the other user's current email address and last-used IP address. This issue is fixed in versions 4.6.4 and 4.7.0-beta.1.

### CVE-2026-72914

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-405;CWE-770` |
| Published | 2026-08-10T22:17:10.193 |

Mastodon is a free, open-source social network server based on ActivityPub. Prior to 4.4.21, 4.5.14, 4.6.4, and 4.7.0-beta.1, the administrative statistics endpoints handled by Api::V1::Admin::MeasuresController and Api::V1::Admin::RetentionController checked authorization only after beginning expensive calculations. Anonymous callers could submit keys, start_at, and end_at parameters that caused long-running SQL queries in Admin::Metrics::Measure, Admin::Metrics::Retention, and Admin::Metrics::Dimension::BaseDimension, allowing repeated requests to exhaust server resources. This issue is fixed in versions 4.4.21, 4.5.14, 4.6.4, and 4.7.0-beta.1.

### CVE-2026-18618

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-10T21:17:20.370 |

A flaw was found in ml-metadata. The statically-linked gRPC stack in ml-metadata is outdated, making it vulnerable to known HTTP/2 denial of service (DoS) issues. An in-cluster attacker, with network access to the MLMD pod, could exploit these vulnerabilities by sending specially crafted HTTP/2 requests. This could lead to a denial of service by crashing the MLMD pod, disrupting all pipeline runs in the affected namespace.

### CVE-2026-18611

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-338` |
| Published | 2026-08-10T21:17:20.120 |

A flaw was found in the Data Science Pipelines Operator. This vulnerability allows an unauthenticated attacker to derive sensitive credentials, such as MariaDB root/user passwords and MinIO access/secret keys, if they can access the MinIO Route or MariaDB Service. The flaw occurs because the operator uses a cryptographically weak pseudo-random number generator (PRNG) to generate these credentials, making them predictable. Successful exploitation could lead to unauthorized access to all pipeline artifacts and metadata, resulting in significant information disclosure.

### CVE-2026-11810

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-10T21:17:19.223 |

The UpdateHub firmware-update agent's probe handler (z_impl_updatehub_probe() in subsys/mgmt/updatehub/updatehub.c) parses the JSON metadata returned by the update server into a fixed two-level nested-array struct. After parsing it validates only the outer array length (objects_len != 2) and then dereferences objects[1].objects[0].objects.sha256sum via strlen() without checking that the inner object array of element [1] is non-empty.

The metadata is attacker-influenceable network input: the agent fetches it over CoAP from the configured UpdateHub server during its routine OTA probe. A malicious or compromised update server (or, when DTLS is disabled, a network man-in-the-middle) can return a response whose second outer object array is empty. Because the parse target is zero-initialised, the corresponding objects[1].objects[0].objects.sha256sum pointer is NULL, and the subsequent strlen() dereferences address zero. The same defect exists in both the 'any boards' and 'some boards' metadata layouts.

The resulting CPU fault is fatal under Zephyr's default error handling, halting or resetting the device, so the flaw is a remotely triggerable denial of service. Impact is limited to availability; it is a read from NULL with no out-of-bounds write, memory corruption, or information disclosure. The fix rejects metadata whose inner object array is empty before any dereference, on both layouts.

### CVE-2026-72871

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-10T19:17:36.033 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, the unauthenticated /api/providers/github/setup route in apps/dokploy/pages/api/providers/github/setup.ts trusts gh_init organizationId and userId values from the state parameter and calls createGithub in packages/server/src/services/github.ts, allowing an attacker to insert a GitHub App provider containing client_secret, webhook_secret, and PEM private key material into another organization. This issue is fixed in version 0.29.13.

### CVE-2026-48048

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-359` |
| Published | 2026-08-10T16:19:47.967 |

XWiki Platform is a generic wiki platform. XWiki discovered that the patch for GHSA-5cf8-vrr8-8hjm was insufficient. Starting with version 6.2.1 and prior to versions 18.0.0RC1, 17.10.13, 17.4.9 and 16.10.17, with slightly modified parameters to the `LiveTableResults`, it is still possible to discover password hashes one bit at a time, so with 768 requests, the full password salt and hash can be retrieved of a user. The check for password (and email properties) has been adjusted in XWiki 18.0.0RC1, 17.10.13, 17.4.9 and 16.10.17. As a workaround, the patch can be applied manually to the wiki page `XWiki.LiveTableResultsMacros`.

### CVE-2026-50237

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-11T12:17:38.347 |

A Server-Side Request Forgery and supply chain flaw was found in the OpenShift Console Helm catalog proxy. A namespace tenant can plant a ProjectHelmChartRepository with an arbitrary URL that the console pod fetches server-side, bypassing tenant egress restrictions. Combined with catalog metadata poisoning and admin-mediated chart installation, this enables privilege escalation.

### CVE-2026-50236

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-11T12:17:38.183 |

An authenticated SSRF flaw was found in the OpenShift Console Dev Console webhook helpers. User-supplied target URLs are fetched server-side without validation, with path neutralization enabling arbitrary endpoint targeting and full response reflection from the console pod's privileged network position.

### CVE-2026-15563

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-11T09:17:13.233 |

A flaw was found in EAP's IIOP. The listener's NameService would accept bind operations without authentication, allowing an attacker to hijack JNDI lookups and binding them to a malicious ORB, achieving MITM or DoS on further invocations.

### CVE-2026-15554

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-11T09:17:12.400 |

the Undertow AJP listener honours forged ssl_cert and is_ssl AJP attributes without requiring any shared-secret authentication. This enables an unauthenticated attacker with direct TCP access to port 8009 to bypass CLIENT-CERT authentication by injecting a forged X.509 certificate via the AJP protocol.

### CVE-2026-64629

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-11T13:19:01.560 |

A vulnerability has been identified in Parasolid V38.0 (All versions < V38.0.235), Parasolid V38.1 (All versions < V38.1.230). The affected applications contains an out of bounds read vulnerability while parsing specially crafted X_T files. This could allow an attacker to execute code in the context of the current process.

### CVE-2026-59701

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-11T13:19:00.763 |

A vulnerability has been identified in Simcenter Femap (All versions < V2606.0001). The affected applications contains an out of bounds read vulnerability while parsing specially crafted BMP files. This could allow an attacker to execute code in the context of the current process.

### CVE-2026-59700

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-11T13:19:00.627 |

A vulnerability has been identified in Simcenter Femap (All versions < V2606.0001). The affected applications contains an out of bounds read vulnerability while parsing specially crafted BMP files. This could allow an attacker to execute code in the context of the current process.

### CVE-2026-59086

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T13:19:00.333 |

A vulnerability has been identified in Simcenter Nastran (All versions < V2606). The affected applications contain a stack overflow vulnerability while parsing specially strings as argument for one of the application binaries. This could allow an attacker to execute code in the context of the current process.

### CVE-2026-50064

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T13:18:58.990 |

A vulnerability has been identified in Solid Edge SE2025 (All versions < V225.0 Update 15), Solid Edge SE2026 (All versions < V226.0 Update 7). The affected applications contains an out of bounds write vulnerability while parsing specially crafted PSM files. This could allow an attacker to execute code in the context of the current process.

### CVE-2026-50063

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-11T13:18:58.860 |

A vulnerability has been identified in Solid Edge SE2025 (All versions < V225.0 Update 15), Solid Edge SE2026 (All versions < V226.0 Update 7). The affected applications contains an out of bounds read vulnerability while parsing specially crafted PAR files. This could allow an attacker to execute code in the context of the current process.

### CVE-2026-50062

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-11T13:18:58.720 |

A vulnerability has been identified in Solid Edge SE2025 (All versions < V225.0 Update 15), Solid Edge SE2026 (All versions < V226.0 Update 7). The affected applications contains an out of bounds read vulnerability while parsing specially crafted PAR files. This could allow an attacker to execute code in the context of the current process.

### CVE-2026-50061

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T13:18:58.583 |

A vulnerability has been identified in Solid Edge SE2025 (All versions < V225.0 Update 15), Solid Edge SE2026 (All versions < V226.0 Update 7). The affected applications contain a use-after-free vulnerability that could be triggered while parsing specially crafted DFT files. This could allow an attacker to execute code in the context of the current process.

### CVE-2026-50060

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T13:18:58.447 |

A vulnerability has been identified in Solid Edge SE2025 (All versions < V225.0 Update 15), Solid Edge SE2026 (All versions < V226.0 Update 7). The affected applications contain a use-after-free vulnerability that could be triggered while parsing specially crafted DFT files. This could allow an attacker to execute code in the context of the current process.

### CVE-2026-50059

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T13:18:58.313 |

A vulnerability has been identified in Solid Edge SE2025 (All versions < V225.0 Update 15), Solid Edge SE2026 (All versions < V226.0 Update 7). The affected applications contains an out of bounds write vulnerability while parsing specially crafted DFT files. This could allow an attacker to execute code in the context of the current process.

### CVE-2026-50058

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-11T13:18:58.153 |

A vulnerability has been identified in Solid Edge SE2025 (All versions < V225.0 Update 15), Solid Edge SE2026 (All versions < V226.0 Update 7). The affected applications contains an out of bounds read vulnerability while parsing specially crafted DFT files. This could allow an attacker to execute code in the context of the current process.

### CVE-2026-19418

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346;CWE-352` |
| Published | 2026-08-11T08:17:20.533 |

The referrer enforcement introduced with TYPO3-CORE-SA-2020-006 (CVE-2020-11069) became ineffective in TYPO3 v13.0, where TYPO3 CMS started serving the backend and Install Tool applications from the site's main entry script instead of the dedicated typo3/ directory.

Whether a request originated from the backend or Install Tool itself was determined by comparing the referrer against the directory of the entry script, which since then is the site root. As a consequence, requests originating from any script running on one of the TYPO3 instance's own domains, such as a frontend page, were accepted by backend routes and Install Tool endpoints.

Attackers able to execute JavaScript on one of those domains, for instance by exploiting a cross-site scripting vulnerability, could invoke these endpoints via Fetch/XHR with the privileges of an authenticated victim's user session. This issue affects TYPO3 CMS versions 13.0.0-13.4.33 and 14.0.0-14.3.5.

### CVE-2026-44765

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-11T01:17:21.180 |

Due to a Missing Authorization Check vulnerability in SAP Manufacturing Integration and Intelligence, an unauthenticated remote attacker could access scheduling-related application functions without proper authorization validation. Successful exploitation could allow the attacker to retrieve, create, modify, or delete application-managed scheduling data, causing a low impact on confidentiality, integrity, and availability.

### CVE-2026-44764

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-11T01:17:21.053 |

Due to a Missing Authorization Check vulnerability in SAP Manufacturing Integration and Intelligence, an unauthenticated attacker could send crafted requests to the Cost Servlet using specific parameter values. If processed by the application, these requests enable access to backend operations. Successful exploitation could allow the attacker to read, create, modify, or delete application-managed business data, resulting in a limited impact on the confidentiality, integrity, and availability of the affected system.

### CVE-2026-72913

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-93;CWE-150` |
| Published | 2026-08-10T21:17:26.297 |

Kitty is a cross-platform GPU based terminal. Prior to 0.48.2, the @kitty-echo and @kitty-ssh DCS handlers in kitty/window.py write unauthenticated data to the child shell's stdin, where handle_remote_echo accepts printable shell command characters and handle_remote_ssh calls get_ssh_data in kittens/ssh/utils.py, which emits a newline; chaining the handlers can execute attacker-controlled commands when a user displays untrusted terminal data. This issue is fixed in version 0.48.2.

### CVE-2026-59091

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-10T19:17:30.090 |

A flaw was found in GIMP's file format plugins, including those for PSD and PAA files. A remote attacker could exploit these vulnerabilities by tricking a user into opening a specially crafted image file. This could lead to unexpected application behavior or other potential security impacts without requiring further user interaction.

### CVE-2026-72763

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-11T13:19:06.367 |

n8n before 1.123.67, 2.31.5, and 2.32.1 validates credential-access only for a node's top-level credentials and not for credentials referenced inside an Execute Sub-workflow node's inline workflow JSON. A member with Editor access to a shared workflow (when workflow sharing is enabled) who knows a target credential's ID can reference that credential in the inline JSON; it passes save-time and runtime validation and resolves in the parent workflow's project context, allowing the attacker to use or exfiltrate credentials they are not permitted to access.

### CVE-2026-4757

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-08-11T06:17:16.427 |

A VAPIX API parameter had improper input validation which could allow code execution and potentially lead to a privilege escalation. This flaw can only be exploited after authenticating with an administrator-privileged service account.

### CVE-2026-73030

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-10T21:17:26.450 |

unearth through 0.18.2, fixed in commit 6c78164, contains a path traversal vulnerability in the is_within_directory function that fails to normalize paths before validation, allowing ../ sequences to bypass directory containment checks. Attackers can supply malicious tar archives with symlink members or traversal sequences to write files to arbitrary filesystem locations accessible to the process.

### CVE-2026-72782

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-668` |
| Published | 2026-08-11T13:19:08.797 |

Craft CMS versions >= 5.0.0-RC1 before 5.10.6 and >= 4.0.0-RC1 before 4.18.2 interpolate environment variables and secrets (via ${ENV_VAR} strings in the elementId parameter) into Twig templates before rendering, even when the Twig sandbox is enabled. An authenticated attacker with control panel access can render a malicious sandboxed Twig template and, using a blind error-based technique across many requests, incrementally leak arbitrary environment variables and secrets. These can be abused to forge sessions (via CRAFT_SECURITY_KEY), escalate privileges, and steal database, SMTP, API, or blob storage credentials. Fixed in 5.10.6 and 4.18.2.

### CVE-2026-72780

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-08-11T13:19:08.510 |

Craft CMS before 5.10.5 fails to persist updated credential counters after WebAuthn assertion validation in the passkey login endpoint. Attackers can replay captured login request bodies containing requestOptions and response to create additional authenticated sessions for victim accounts.

### CVE-2026-72774

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-11T13:19:07.893 |

n8n before 1.123.67, 2.31.5, and 2.32.1 contains a credential authorization bypass in the HTTP Request node. An authenticated member with edit access to a shared workflow can reference another user's credential while specifying the credential type via an expression. Because the pre-execution permission check compares the unresolved expression instead of the resolved credential type, the ownership check is skipped and the credential is loaded at execution time, allowing the member to use or exfiltrate a credential they were not granted. Exploitation requires knowing the target credential's identifier.

### CVE-2026-72771

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T13:19:07.490 |

n8n versions before 2.32.1 fail to enforce the Allowed HTTP Request Domains allowlist in multiple AI and LLM nodes when user-supplied base or endpoint URLs are configured. Low-privileged workflow editors with use-only access to shared credentials can redirect requests to attacker-controlled hosts and exfiltrate credential secrets for reuse against underlying services.

### CVE-2026-72770

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-11T13:19:07.353 |

n8n versions before 1.123.67 contain a path traversal vulnerability in the Git node's fetch, pull, and push-tags operations that allows authenticated users to bypass repository-path containment checks. Attackers with workflow create/execute rights can point allowlisted remote configurations at local paths outside the sandbox to pull arbitrary git repositories and read their files and history.

### CVE-2026-72749

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-08-11T13:19:05.960 |

n8n before 1.123.67, 2.31.5, and 2.32.1 contains a prototype pollution vulnerability in the Edit Fields (Set) node. The node assigns output fields via a dot-notation path setter without restricting the field name, allowing an authenticated user to name a field after an inherited built-in method path and corrupt a shared global in the main Node.js process. Because that global is used on the request-authentication path, the instance then fails every authenticated request, causing an instance-wide denial of service for all users until the process is restarted.

### CVE-2026-72609

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-11T12:17:44.120 |

An SQL injection vulnerability in Koha through 24.11.17, 25.05.12, 25.11.06, and 26.05.01 allows authenticated staff with the acquisition => order_receive permission to read arbitrary database contents via the orderby request parameter in acqui/parcels.pl. The parameter is passed to C4::Acquisition::GetInvoices, which allow-lists the column name but concatenates the direction token raw into the SQL ORDER BY clause without validation. Exploitation is blind (time-based) in production and allows extraction of patron PII, staff bcrypt password hashes, and two-factor secrets.

### CVE-2026-72607

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-11T12:17:43.867 |

A stored SQL injection vulnerability in Koha through 24.11.17, 25.05.12, 25.11.06, and 26.05.01 allows authenticated staff with the tools => items_batchmod permission to read arbitrary database contents by storing a SQL payload in the agefield value of an automatic item modification rule. The agefield value is stored verbatim to the system preference and later interpolated without parameterization into a SQL query in C4::Items::ToggleNewStatus (line 1228) when the scheduled cron job executes. The injection is SELECT-only under standard MariaDB/MySQL DBI single-statement execution; a time-based SLEEP payload is also achievable via the cron trigger. An attacker can read the entire Koha database including patron PII and staff bcrypt password hashes.

### CVE-2026-72547

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-11T12:17:40.233 |

An insecure direct object reference vulnerability in Attendize through commit 9289acb allows any authenticated event organiser to bulk import attendees into events belonging to other accounts via the postImportAttendee endpoint. The endpoint loads the target event by ID without verifying ownership against the requesting organiser account. An attacker can inject bulk attendee data into any event in the system regardless of account boundaries.

### CVE-2026-72546

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-11T12:17:40.110 |

An insecure direct object reference vulnerability in Attendize through commit 9289acb allows any authenticated event organiser to inject attendees and orders into events belonging to other accounts via the postInviteAttendee endpoint. The endpoint loads the target event by ID without scoping the query to the authenticated organiser account. An attacker can modify event data and financial records across account boundaries.

### CVE-2026-72694

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-11T09:17:14.493 |

A flaw was found in MRTG. When the MRTG daemon is started as a root user and subsequently drops privileges, a local, low-privileged attacker can exploit a symbolic link (symlink) following vulnerability. By influencing or pre-placing a symlink in the process ID (PID) file path, the attacker can trick the root process into changing the ownership of an arbitrary existing file to the daemon user. This can lead to local privilege escalation, allowing unauthorized access to or modification of sensitive files.

### CVE-2026-72910

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-10T21:17:25.860 |

ERPNext is a free and open source Enterprise Resource Planning tool. Prior to 15.112.0 and 16.22.0, the merge_account, pause_job_for_doc, trigger_job_for_doc, change_release_date, and update_cost_center functions across erpnext/accounts/doctype/account/account.py, erpnext/accounts/doctype/process_payment_reconciliation/process_payment_reconciliation.py, erpnext/accounts/doctype/purchase_invoice/purchase_invoice.py, and erpnext/accounts/utils.py omit required write permission checks, allowing authenticated limited users to modify protected data beyond their roles. This issue is fixed in versions 15.112.0 and 16.22.0.

### CVE-2026-72909

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-10T21:17:25.727 |

ERPNext is a free and open source Enterprise Resource Planning tool. Prior to 15.112.0 and 16.23.0, the ReceivablePayableReport prepare_conditions path in erpnext/accounts/report/accounts_receivable/accounts_receivable.py does not apply Customer and Supplier user permissions to the Payment Ledger Entry dynamic-link party field, allowing any authenticated user to read unauthorized cross-company financial data in Accounts Receivable and Accounts Payable reports. This issue is fixed in versions 15.112.0 and 16.23.0.

### CVE-2026-18620

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-10T21:17:20.490 |

A flaw was found in Data Science Pipelines. A restricted user, or tenant, can exploit an improper authorization vulnerability in the setDefaultServiceAccount function. By specifying a more privileged ServiceAccount (SA) during a CreateRun request, an attacker can bypass authorization checks. This allows the tenant to run their containers with elevated privileges, potentially leading to the disclosure of sensitive information (secrets) and the ability to execute commands within other users' pods.

### CVE-2026-69114

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-10T20:17:32.010 |

Spacebar Server before commit 8d126f4 contains a cross-channel message deletion vulnerability in the single-delete and bulk-delete message handlers that fail to scope message queries to the requested channel. Authenticated users with MANAGE_MESSAGES permission in any controlled channel can delete arbitrary messages in other channels by routing delete requests through their own channel.

### CVE-2026-71964

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-10T19:17:31.613 |

CyberPanel 2.4.3, fixed in commit eca0c3c, contains an arbitrary file read vulnerability in the file manager component that allows authenticated attackers to read sensitive system files by uploading a crafted ZIP archive containing symbolic links. Attackers can exploit the application's failure to validate symlinks before extraction, causing symbolic links targeting arbitrary filesystem paths outside the user's home directory to persist on disk and be accessed through the web interface.

### CVE-2026-72900

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-10T18:18:53.637 |

Metabase allows an authenticated, low-privileged attacker to read the entire Metabase application database.

### CVE-2026-70622

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-10T18:18:50.610 |

tar-rs versions 0.4.11 through 0.4.46 contain a symlink escape vulnerability in the Builder::append_dir_all() function that allows attackers to read files outside the intended source root directory by planting symlinks in an attacker-controlled directory. When a privileged process archives an untrusted directory, the function follows symlinks without verifying that resolved targets remain within the source root, causing out-of-bounds files to be included in the archive as regular files and disclosed to the attacker.

### CVE-2026-72731

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-10T17:17:37.663 |

Discourse is an open-source discussion platform. From 2026.1.0-latest until 2026.1.7, 2026.6.2, 2026.7.1, and 2026.8.0-latest.1, anyone able to run a parameterized Data Explorer query, including non-staff members of a group a query is shared with, could craft parameter values that escaped the intended query and executed arbitrary SQL through plugins/discourse-data-explorer/lib/discourse_data_explorer/data_explorer.rb and plugins/discourse-data-explorer/lib/discourse_data_explorer/workflows/sql_action/v1.rb. Recursive parameter interpolation allowed one parameter value to introduce another parameter, and parameter declarations in SQL comments could be used to inject a statement. Queries run in a read-only transaction, so data could not be modified, but any table could be read. This issue is fixed in versions 2026.1.7, 2026.6.2, 2026.7.1, and 2026.8.0-latest.1.

### CVE-2026-57263

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-759` |
| Published | 2026-08-11T13:18:59.607 |

A vulnerability has been identified in LOGO! Soft Comfort (All versions < V9). The project password feature in the affected products stores the password as an unsalted SHA-256 hash. This could allow an attacker who has obtained the project file to perform efficient offline dictionary or brute-force attacks against the unsalted hash.

### CVE-2026-57262

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-08-11T13:18:59.463 |

A vulnerability has been identified in LOGO! Soft Comfort (All versions < V9). Affected products use a static, hardcoded AES master key to encrypt project files. This could allow a local attacker to extract the master key from the application files or memory and use it to decrypt project files or remove project passwords entirely without knowing the actual user-defined password.

### CVE-2026-58230

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-601` |
| Published | 2026-08-11T01:17:21.307 |

SAP Approuter does not sufficiently validate certain token content under specific configurations. An unauthenticated attacker could send a specially crafted token to cause sensitive credential material to be sent to an attacker-controlled destination. The attack complexity is high due to non-default preconditions required in the target environment. This results in a high impact on confidentiality and a low impact on integrity and availability.

### CVE-2026-73033

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-10T21:17:26.610 |

Sucuri Security WordPress plugin through version 2.7.3 contains a path traversal vulnerability in the pageIntegritySubmission() method in src/integrity.lib.php that allows authenticated administrators to delete arbitrary files by supplying directory traversal sequences in the sucuriscan_integrity parameter. Attackers can manipulate the unsanitized file path concatenated with ABSPATH to traverse outside the WordPress installation directory and invoke unlink() on sensitive files such as wp-config.php and .htaccess, causing site outage or enabling malicious reinstallation.

### CVE-2026-72718

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-10T16:19:48.900 |

goose is general-purpose AI agent that runs on your machine. Prior to 1.44.0, the `goose review` command runs the system `git` executable to gather the diff for review without stripping attacker-controlled Git configuration. A malicious repository whose `.git/config` sets [`core] fsmonitor = <command>` causes Git to execute that command on the host during the index refresh performed by `git diff HEAD`. The command runs before goose contacts a model and without a submitted prompt, model call, tool approval, or trust prompt. The context-gathering Git process is not sandboxed and is outside goose's tool-permission model. Arbitrary commands run with the privileges and environment of the user running goose, allowing file access or modification and exfiltration of environment secrets and provider API keys. The vulnerable Git invocations are built by git_command() in crates/goose-cli/src/commands/review/handler.rs and are used by touched_files() and collect_diff() for `git diff --name-only HEAD` and `git diff HEAD`. This issue is fixed in version 1.44.0.
