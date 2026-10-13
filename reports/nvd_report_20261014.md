# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-13 15:01 UTC
- **対象期間**: `2026-10-12T15:00:33.000Z` 〜 `2026-10-13T15:01:01.000Z`
- **重要CVE数**: 360 件（Critical 9.0+: 56 件 / High 7.0〜: 304 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE のうち **CVSS 7.0 以上が 30 件以上** と、ハイリスク脆弱性が集中しています。  
- **リモートコード実行 (RCE)・特権昇格・情報漏洩** が共通の攻撃成果で、特に **Kubernetes、GitLab、SAP、IBM、Progress MarkLogic** といった基幹システム・開発プラットフォームで深刻な欠陥が報告されています。  
- 多くは **認証不要 (PR:N) または低権限 (PR:L) の攻撃者** が利用でき、攻撃経路はネットワーク直接公開、API エンドポイント、またはマルチテナント環境の設定ミスに依存しています。  

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な影響 | 注目理由 |
|-----|--------|----------|----------|
| **CVE‑2026‑65162** | 10.0 (CVSS3.1) | NVIDIA AIStore for Linux の ETL PodSpec 初期化 API で、Kubernetes の **host‑namespace / コンテナセキュリティ設定** を遠隔から書き換え可能。コード実行・特権昇格・情報漏洩が同時に成立。 | AI/ML インフラは高価資産であり、K8s クラスタ全体が乗っ取られるリスクが極めて高い。 |
| **CVE‑2026‑97229** | 10.0 (CVSS3.1) | GitLab CE/EE (19.2‑19.4 系) の正規表現パーサに未検証入力があり、**認証なしで任意コード実行** が可能。 | GitLab は CI/CD の中心であり、全社的なコードリポジトリが一瞬で危殆化。多くの企業がバージョン 19.2‑19.4 を未だ使用中。 |
| **CVE‑2026‑89111** | 10.0 (CVSS3.1) | SAP Cloud SDK for Python の OAuth2 SSRF。`tenant_subdomain` を操作し、**クライアント認証情報を外部サーバへ流出** できる。 | BTP (Business Technology Platform) のマルチテナントアプリは多数の顧客データを扱うため、認証情報漏洩は大規模なビジネスインパクトを伴う。 |
| **CVE‑2026‑85955** | 9.9 (CVSS3.1) | Progress MarkLogic Server 12.x/11.x の **XQuery 評価権限バイパス**。クエリ実行権限のみでサーバ側コード実行が可能。 | データベース層でのコード実行は、機密データの改ざん・抽出、さらには横展開攻撃に直結。 |
| **CVE‑2026‑109390** | 9.8 (CVSS3.1) | AnyDesk < 8.0.3 のヒープバッファオーバーフローにより、**リモートから root 権限でコード実行** が可能。Linux デスクトップ環境で広く利用されている。 | リモートデスクトップツールは内部ネットワークの踏み台として狙われやすく、攻撃成功時の被害範囲が広い。 |

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 / コンポーネント | 現行脆弱バージョン | 推奨バージョン / パッチ |
|----------------------|-------------------|------------------------|
| **NVIDIA AIStore for Linux** | すべてのリリース (legacy ETL API) | NVIDIA が提供する **2026‑Q3 パッチ**（リリースノート参照）または **v2.5.0 以降** |
| **GitLab CE/EE** | 19.2.x (<19.2.8), 19.3.x (<19.3.5), 19.4.x (<19.4.2) | **19.2.8**, **19.3.5**, **19.4.2** 以上へアップグレード |
| **SAP Cloud SDK for Python** | 1.0.0‑1.4.3 (含む) | **SDK 1.5.0 以降**（OAuth2 SSRF 修正） |
| **Progress MarkLogic Server** | 12.x <12.1.0, 11.x <11.3.7 | **12.1.0** 以上、または **11.3.7** 以上 |
| **AnyDesk** | 8.0.0‑8.0.2 | **8.0.3** 以降 |
| **IBM i (HTTP Server Administration)** | 7.3‑7.6 (未パッチ) | IBM の **2026‑09 Security Bulletin** に掲載のパッチ適用 |
| **IBM Db2 Mirror for i** | 7.4‑7.6 (未パッチ) | IBM の **2026‑10 Fix Pack** を適用 |
| **Wazuh** | 4.14.3‑4.14.7, 3.9.0‑4.14.7 | **4.14.8** 以上 |
| **Obsidian‑tc** | <1.3.1 | **1.3.1** 以上 |
| **HAProxy Data Plane API** | 2.2.0‑3.4.3 | **3.4.4** 以降 |
| **IBM DataStage on Cloud Pak for Data** | 5.4.0.0 | **5.4.1** 以上（パス・トラバーサル修正） |
| **Metasploit Framework Web Service** | すべてのリリース (msf‑ws) | **6.4.20** 以降（credential servlet 修正） |

> **※ ベンダーが提供する最新のセキュリティアドバイザリを必ず確認し、パッチ適用手順に従ってください。**

### 3.2 環境・設定のハードニング
1. **Kubernetes**  
   - `hostNetwork`, `hostPID`, `hostIPC` などの特権オプションは **デフォルトで無効** にし、PodSecurityPolicy / OPA Gatekeeper で制御。  
   - AIStore の ETL API へのアクセスは **ネットワークポリシーで内部のみ** に限定。

2. **GitLab**  
   - 外部からの正規表現パーサ呼び出しを **IP フィルタリング** で制限。  
   - `gitlab.rb` の `unrestricted_issues` 等、不要な機能は無効化。

3. **SAP Cloud SDK**  
   - `tenant_subdomain` パラメータは **ホワイトリスト** で検証し、外部リダイレクトは許可しない。  
   - OAuth2 のトーク

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-65162

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-10-13T13:17:32.837 |

NVIDIA AIStore for Linux contains a vulnerability in the legacy ETL Kubernetes PodSpec initialization API where a remote attacker may supply Kubernetes host-namespace and container-security settings. A successful exploit may lead to code execution, privilege escalation, information disclosure, data tampering, and denial of service.

### CVE-2026-97229

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T02:17:00.840 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 19.2 before 19.2.8, 19.3 before 19.3.5, and 19.4 before 19.4.2 that, under certain conditions, could have allowed an unauthenticated user to execute arbitrary code on the GitLab server via a specially crafted regular expression in a CI/CD configuration, due to insufficient regular expression validation.

### CVE-2026-89111

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-13T01:16:47.890 |

The SAP Cloud SDK for Python contains an OAuth2 SSRF vulnerability affecting multi-tenant BTP applications. An attacker who controls the tenant_subdomain parameter can redirect OAuth2 token requests to an attacker-controlled server, causing client credentials to be exfiltrated.

### CVE-2026-89110

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-749` |
| Published | 2026-10-13T01:16:47.767 |

SAP NetWeaver Visual Composer does not perform sufficient authorization checks in certain portal functionality. An attacker with low privileges could invoke internal operations on a preconfigured remote system. Depending on the remote connection configuration, this could lead to a full compromise of the remote system. This results in a high impact on confidentiality, integrity and availability.

### CVE-2026-89107

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T01:16:47.507 |

SAP S/4HANA (Manage Substitution/Validation Rules) does not sufficiently validate input processed by rule definition functionality that utilizes a domain-specific scripting language. An authenticated attacker with specific business privileges could submit specially crafted input, which is interpreted as executable ABAP code by the rule processing logic. Successful exploitation could allow the attacker to execute ABAP arbitrary code into the system, resulting in full compromise of the affected system and high impact on confidentiality, integrity, and availability of the system.

### CVE-2026-96119

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T00:17:02.053 |

IBM i 7.3, 7.4, 7.5, and 7.6 could allow a remote authenticated attacker to obtain sensitive information or execute arbitrary code on the system due to improper data sanitization by the HTTP Server Administration web application.

### CVE-2026-96012

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-264` |
| Published | 2026-10-12T20:17:10.723 |

IBM Db2 Mirror for i 7.4, 7.5, and 7.6 is vulnerable to privilege escalation. An authenticated attacker could craft a malicious request that bypasses additional authorization and input validation checks to execute malicious code. An attacker could exploit this vulnerability to obtain elevated privileges on the system.

### CVE-2026-77366

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-863` |
| Published | 2026-10-12T18:17:23.830 |

obsidian-tc is a governed, agent-ready Model Context Protocol server for Obsidian vaults. Prior to 1.3.1, tool dispatch does not compare the caller-controlled input.vault value with the vault bound to the caller, the JSON Web Token (JWT) has no vault claim, and the folder access-control list is shared globally. Any valid token can therefore select another configured vault and read, write, or delete its contents through affected tools. Version 1.3.1 fixes the vulnerability by binding tokens and request context to a vault and rejecting mismatched input.vault values before scope checks.

### CVE-2026-85955

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-12T16:17:07.070 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 allow a remote attacker with query-execution access to invoke an XQuery evaluation function without the additional required evaluation privilege, which could result in server-side code execution with elevated permissions.

### CVE-2026-85948

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-12T16:17:06.173 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 contain an XQuery injection flaw in a deprecated Management API package path. A remote attacker with manage-user-level privileges could exploit this flaw to obtain persistent unauthorized administrative control.

### CVE-2026-85947

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-12T16:17:06.040 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 contain an authorization flaw in certain forest-management operations. A remote attacker with forest-management privileges could exploit this flaw to create a persistent unauthorized administrator account, potentially resulting in complete unauthorized administrative control of the server.

### CVE-2026-87689

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-13T01:16:47.110 |

The Metasploit Framework Web Service REST API (msf-ws) exposes the credential store through Msf::WebServices::CredentialServlet. Every mutating and read route in this servlet calls warden.authenticate! before processing a request, except the update_credential (PUT) and delete_credentials (DELETE) handlers for /api/v1/credentials, which omit the authentication call entirely. Because these handlers call directly into lib/msf/core/db_manager/cred.rb, which performs no authorization check of its own, any client able to reach the web service on its default 0.0.0.0:8080 listener can read, modify, or permanently delete every stored credential record — including passwords, hashes, and private keys stored for a shared team engagement — without presenting any authentication. All published versions of Metasploit Framework through 6.5.4 are affected. The issue is fixed in 6.5.5 by adding warden.authenticate! as the first statement in both handlers, matching the pattern used by every other route in the API.

### CVE-2026-90920

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-12T22:17:05.683 |

IBM Maximo AI Service 9.1.0, and 9.2.0 could allow a remote attacker to execute arbitrary code due to improper control of code generation.

### CVE-2026-109575

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-12T20:17:09.443 |

In HAProxy Data Plane API 2.2.0 through 3.4.3 (and corresponding Enterprise Edition releases), Server.ConfigureAPI() has process-global authentication logic that improperly drops security controls across multiple transport types. When a TLS Certificate Authority (tls_ca) is configured and a numeric TLS port (tls_port) is specified, the application globally disables Basic authentication on its shared internal request handler. Because this handler is shared concurrently among HTTP, HTTPS, and UNIX domain socket listeners, and mutual TLS (mTLS) client certificate verification (tls.RequireAndVerifyClientCert) is enforced exclusively on the HTTPS server path, all other simultaneously active non-mTLS listeners fail open. Consequently, an unauthenticated attacker capable of reaching an affected HTTP or UNIX management endpoint can completely bypass credentials to gain full API administrative access. This allows unauthorized remote or local actors to read sensitive, cleartext HAProxy configuration data or replace the managed configuration entirely via the raw configuration endpoint. This has been fixed in versions 3.4.4, 3.3.9, 3.2.17, 3.0.25, 2.9.29, and their respective EE backports by migrating to a per-request TLS connection-state validation model.

### CVE-2026-57118

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-862` |
| Published | 2026-10-12T19:16:38.940 |

PraisonAI is a multi-agent teams system. Prior to praisonaiagents 1.6.59, AgentTeam.launch and the Agents alias register GET /{path}/list, POST /{path}, and `POST /{path}/{agent_id}' without access-control checks before listing agents or calling agent.chat. A remotely exposed server can therefore let unauthenticated clients enumerate agents, consume model resources, access connected private context, and trigger agent tools or workflow side effects. This vulnerability is fixed in praisonaiagents 1.6.59.

### CVE-2026-109390

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-130` |
| Published | 2026-10-12T15:17:07.980 |

AnyDesk before 8.0.3 allows unauthenticated remote attackers to execute arbitrary code via a heap-based buffer overflow, as demonstrated on Linux for command execution as root without the victim approving desktop control. In the stream packet handler for mode 5 in the session protocol, a payload length value is not validated.

### CVE-2026-82110

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-12T23:17:42.533 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary code due to improper validation of pathname during a path traversal.

### CVE-2026-82103

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-12T23:17:42.110 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to obtain sensitive information due to an exposure of sensitive information to an unauthorized actor.

### CVE-2026-82101

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-12T23:17:41.897 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to cause a denial of service due to a path traversal vulnerability.

### CVE-2026-9191

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-346` |
| Published | 2026-10-12T16:17:08.223 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 do not sufficiently isolate user-supplied code executed through certain REST and XDBC evaluation paths from HTTP request, response, and session state. An attacker able to execute code through an affected path could perform unauthorized actions or compromise an authenticated session.

### CVE-2026-85956

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-12T16:17:07.193 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 allow a remote attacker with delegated database-administrator privileges to perform backup or restore operations on forests outside the authorized database scope, which could result in unauthorized access to or modification of security-critical data.

### CVE-2026-74041

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-10-13T14:17:40.860 |

Wazuh 4.14.3 before 4.14.8 contains a case-sensitivity mismatch between the ossec.conf validator and wazuh-logcollector that bypasses remote-command validation. Authenticated users with manager:update_config can inject an uppercase LOG_FORMAT command localfile that the collector runs as root on reload.

### CVE-2026-74040

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T14:17:40.720 |

Wazuh versions from 3.9.0 before 4.14.8 contain an arbitrary file overwrite vulnerability in MasterHandler.process_files_from_worker allowing a cluster worker to overwrite protected master files. Attackers controlling a worker can use a trailing-slash basename bypass and missing extra_valid enforcement to overwrite ossec.conf and agent.conf, achieving root remote code execution across the manager and every agent.

### CVE-2026-63354

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T10:17:18.450 |

Affected devices do not properly validate and sanitize visual marker data contained in imported CSV trace files before rendering it on the Trace page.

This could allow an attacker to social engineer an authorized user who holds the function right “Read diagnostics” into importing a specially crafted trace file. Successful exploitation could allow attacker-controlled JavaScript to execute in the user’s browser session and perform PLC operations through the web server within the scope of the user’s authorization.

### CVE-2026-63353

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T10:17:18.040 |

Affected devices do not properly sanitize comment fields contained in imported trace files before rendering them on the Trace page.

This could allow an attacker to social engineer an authorized user who holds the function right “Read diagnostics” into importing a specially crafted trace file. Successful exploitation could allow attacker-controlled JavaScript to execute in the user’s browser session and perform PLC operations through the web server within the scope of the user’s authorization.

### CVE-2026-63350

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-10-13T10:17:16.777 |

Affected devices do not properly restrict executable content contained in imported trace files.

This could allow an attacker to social engineer an authorized user who holds the function right “Read diagnostics” into importing a specially crafted trace file. Successful exploitation could allow attacker-controlled JavaScript to execute in the user’s browser session and perform PLC operations through the web server within the scope of the user’s authorization.

### CVE-2026-108929

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-88` |
| Published | 2026-10-12T21:17:09.410 |

A flaw has been found in Netcore NR268 1.7.121109. The affected element is the function execvp of the file /router/DDNSset.cgi of the component DDNS. Executing a manipulation of the argument Hostname can lead to argument injection. The attack can be launched remotely.

### CVE-2026-109520

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-267` |
| Published | 2026-10-13T14:17:26.800 |

A flaw has been found in Colorful iGameCenter 2.0.0.82. Affected by this vulnerability is the function MmMapIoSpace in the library AMDRyzenMasterDriver.sys of the component Dispatch Handler. This manipulation of the argument SystemBuffer causes privilege defined with unsafe actions. The attack needs to be launched locally. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-109110

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-10-13T09:17:15.370 |

A flaw has been found in Wavlink WL-WN592AX6 250422. This issue affects the function system of the component wmapd Daemon. Executing a manipulation can lead to os command injection. It is possible to launch the attack remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-109109

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-10-13T08:17:00.110 |

A vulnerability was detected in Wavlink WL-WN530BE1-A 251117. This vulnerability affects the function strcpy of the file /cgi-bin/ExportAllSettings.cgi of the component Settings Export CGI. Performing a manipulation of the argument HTTP_COOKIE/X-Cmd results in stack-based buffer overflow. It is possible to initiate the attack remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-109758

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798;CWE-1321` |
| Published | 2026-10-13T04:17:14.843 |

Perforce Helix Authentication Service (HAS) deployments that retain the shipped default SCIM bearer token are vulnerable to unauthorized access when the SCIM endpoint is reachable by an attacker. In version 25.2, the installation templates contain a default credential which the installer copies into the active configuration; the installer and configuration script do not automatically replace that value with a random token. An attacker who knows the default token can authenticate to the SCIM API and perform user and group operations allowed by the configured provisioning backend. 





This issue can be chained with CVE-2026-61834 in affected releases of the scim-patch dependency. A crafted SCIM PATCH request can cause server-side prototype pollution, corrupt application state, and disrupt service availability, including health checks and SCIM or SSO requests. In a later test, this primitive was confirmed to enable remote code execution in a Node.js 24/Express deployment through available gadget chains involving child_process, EJS/Pug, or Passport. 





This vulnerability exists in version 2022.1 - 2025.2 of HAS however the underlying defect was removed in version 2026.1 which was released July 17th 2026. The vulnerability was identified in older versions of HAS after version 2026.1 was released.

### CVE-2026-44828

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-538` |
| Published | 2026-10-12T22:17:04.160 |

Qexo is an open source online editor for static blogs. From 4.0.0 until 4.2.0, Qexo exposes /api/init_step/ through init_step_api without authentication, authorization, or a setup-completion guard. An unauthenticated requester with a valid CSRF token obtained from a public page can submit the first initialization step and reset the INIT setting, causing the instance to re-enter the setup flow. The setup response and /init/ page can expose stored PROVIDER configuration, including service credentials, in frontend content. This issue is fixed in version 4.2.0.

### CVE-2026-109569

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-10-12T21:17:13.653 |

sandboxed.sh through 1.3.0 contains a container escape vulnerability that allows code in container workspaces to access the host filesystem because nsenter attaches without --root. Agent-run code in a container workspace can resolve absolute paths on the host to read and modify host files, bypassing documented isolation.

### CVE-2026-109566

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-12T21:17:13.190 |

Rapyd Admin from 9.0.0 before 9.20.0 contains a hard-coded credentials vulnerability that allows remote unauthenticated attackers to gain super-admin access through an AuthSeeder-created admin@laravel account with password admin. The account is seeded by the setup installer and silently re-created on every rpd:make run, letting attackers log in as a global super admin bypassing per-record authorization and tenant scoping.

### CVE-2025-71429

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-12T21:17:07.817 |

GPT-SoVITS through 20250606v2pro contains an OS command injection vulnerability in tools/uvr5/vr.py that allows unauthenticated attackers to execute commands via output folder paths. Attackers can enter shell substitutions like $(...) in the UVR5 WebUI output folder textboxes with mp3 or m4a export to run commands as the server user.

### CVE-2026-108918

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-10-12T18:17:22.353 |

A vulnerability was identified in Edimax BR-6208AC 1.32. Impacted is an unknown function of the file /goform/formWlanMP. The manipulation of the argument readE2P leads to command injection. It is possible to initiate the attack remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-108917

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-10-12T18:17:22.163 |

A vulnerability was determined in Edimax BR-6208AC 1.32. This issue affects some unknown processing of the file /goform/formAutoFWupgrade. Executing a manipulation of the argument tftpsIP can lead to command injection. The attack may be performed from remote. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-109372

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-12T17:17:34.800 |

ZITADEL 4.x before 4.19.2 and 3.x through 3.4.15 contains an authentication bypass in the SAML identity-provider intent callback, which verifies the assertion signature using the provider named in the request URL but resolves the user from the login intent without checking they match. Attackers with organization-administrator permission can register a SAML provider with their own signing key to obtain authenticated sessions as any user linked to another SAML provider on the instance, including in other organizations.

### CVE-2026-109321

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1391` |
| Published | 2026-10-12T17:17:27.247 |

Grav Login OAuth plugin (grav-plugin-login-oauth) before 1.4.3 provisions OAuth accounts as ordinary Grav users with a deterministic <provider>.<id> username and an unsalted MD5 hash of the provider identifier as the password, without disabling password login. Unauthenticated remote attackers who learn or guess a provider identifier can reproduce these credentials and log in, gaining administrative control of privileged accounts.

### CVE-2026-108907

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-12T17:17:13.373 |

A vulnerability was determined in Netcore NR268 1.7.121109. Affected is the function user_ok of the component CGI Execution. This manipulation causes improper authentication. The attack can be initiated remotely. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-92681

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-12T16:17:07.323 |

In @neo4j/graphql versions up to and including 7.6.3, @authentication directives applied at the schema level or on the Query or Mutation types are silently ignored for top-level fields annotated with @cypher. Only @authentication directives placed directly on the individual fields are enforced. An application that exposes a top-level @cypher field and relies on schema-level or type-level @authentication to protect it allows unauthenticated callers to invoke the field and run the configured Cypher statement with the privileges of the GraphQL service account, which may permit reading and modifying data. Fixed in 7.6.4.

### CVE-2026-109573

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T23:17:22.557 |

phpMyFAQ before 4.1.9 contains an SQL injection vulnerability in PdoMysql::escape(), which escapes single quotes with backslashes that are treated literally when MySQL or MariaDB runs in NO_BACKSLASH_ESCAPES mode. Unauthenticated attackers can send a Unicode right single quotation mark in the search parameter of api/autocomplete, which is normalized to an ASCII quote, to read credentials and configuration secrets, modify records, or drop tables.

### CVE-2020-37279

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-12T21:17:05.570 |

easy-pdf-merge 0.1.0 through 0.2.6 contains an OS command injection vulnerability that allows attackers to execute commands by injecting shell metacharacters into source paths, destination path, or maxHeap option. Attackers can supply file names or options containing double quotes, semicolons, $() or backticks, which child_process.exec() runs through a shell with the Node.js process privileges.

### CVE-2026-109422

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-749` |
| Published | 2026-10-12T20:17:08.840 |

NetEase Cloud Music client for Windows (cloudmusic.exe) versions 3.1.38 and 3.1.39.205426 contains a remote code execution vulnerability in the renderer-process IPC bridge os.navigateExternal, which passes caller-supplied URLs to ShellExecuteW without validating the URL scheme. An attacker able to inject content into the renderer, such as by forging the /pc/upgrade/get API response using a publicly known AES key over an unvalidated TLS connection, can invoke os.navigateExternal with a file:// URL through an img onerror payload to execute arbitrary local binaries under the logged-in user's account.

### CVE-2026-109373

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-441` |
| Published | 2026-10-12T17:17:35.110 |

ZITADEL 3.0.0 before 4.19.2 contains an authentication bypass vulnerability in the Login V2 UI that allows unauthenticated attackers to obtain other users' session tokens by forging unsigned session cookies. Attackers can guess time-ordered session IDs around a victim's sign-in and supply them with empty tokens to receive rotated tokens, taking over accounts including MFA-completed administrator sessions.

### CVE-2026-109357

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-90` |
| Published | 2026-10-12T17:17:33.020 |

LibreNMS before 26.9.0 contains an LDAP filter injection in ldap-authorization and ad-authorization modes because usernames are inserted unescaped into LDAP search filters and authentication only checks user existence. When REMOTE_USER is not forwarded, unauthenticated attackers can send a wildcard username via HTTP Basic Authorization (PHP_AUTH_USER) to match all users and groups and gain admin access.

### CVE-2026-109238

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-12T17:17:14.420 |

Crawl4AI 0.7.0 before 0.9.4 contains a server-side request forgery vulnerability that allows API clients to reach internal addresses by enabling link_preview_config on /crawl requests. Attackers can supply a controlled page with include_external and include_patterns set, causing AsyncUrlSeeder to fetch internal, private, and cloud-metadata links and return their parsed head data.

### CVE-2026-109399

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-12T16:17:05.557 |

SWUpdate through 2026.05.1 contains an improper certificate validation vulnerability in crypto/swupdate_cms_verify_openssl.c that trusts untrusted X.509 certificates embedded in CMS SignedData for chain building. Attackers holding a signing key from a sibling intermediate under the same root can embed that intermediate in the signature to install malicious updates.

### CVE-2026-109391

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-12T16:17:04.373 |

Square Squash through commit e73f280 contains an insecure deserialization vulnerability that allows unauthenticated attackers to store crafted YAML via the POST /api/1.0/symbolication endpoint. When occurrences referencing the attacker-controlled symbolication UUID are symbolicated, the stored values are passed to YAML.load with SafeYAML in unsafe mode, enabling arbitrary Ruby object deserialization and potential code execution.

### CVE-2026-65173

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-13T13:17:33.540 |

NVIDIA AIStore for Linux contains a missing authentication vulnerability in the token-revocation endpoint where an unauthenticated remote attacker may submit crafted token-revocation lists. A successful exploit may lead to data tampering and denial of service.

### CVE-2026-89108

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T01:16:47.637 |

SAP Manufacturing Integration and Intelligence does not sufficiently enforce authorization boundaries within certain administrative functionality. An attacker with MII administrator privileges could submit a specially crafted request to provision an account with elevated privileges on the underlying Java application server. Successful exploitation could allow the attacker to gain administrative control over the underlying system, extending the impact beyond the vulnerable application. This results in a high impact on confidentiality, integrity and availability.

### CVE-2026-53997

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307;CWE-640` |
| Published | 2026-10-12T21:17:17.400 |

Netherman Portal del Hermano (portaldelhermano.es) before 2026-10-06 contains a broken authentication vulnerability in its password-recovery flow at the POST /password/create-access and POST /password/email endpoints, allowing unauthenticated attackers to take over any member account across all tenants by exploiting the lack of rate limiting and distinct error messages that act as oracles for each of the four identity-verification factors (DNI, date of birth, phone number, last four IBAN digits). Attackers can confirm the DNI via the oracle, brute-force the date of birth and IBAN digits, obtain the phone number through open-source intelligence, then submit an attacker-controlled email field so the password reset link is delivered to them, enabling full account takeover including profile data, full IBAN, and fiscal documents.

### CVE-2026-109423

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-12T20:17:08.993 |

NetEase Cloud Music client for Windows (cloudmusic.exe) versions 3.1.38 and 3.1.39.205426 contains a TLS certificate validation vulnerability that allows a network-adjacent attacker to intercept and decrypt HTTPS traffic by failing to validate the server certificate chain, verify the hostname, or consult any Windows certificate trust store. Attackers can perform a man-in-the-middle attack using a rogue certificate authority to decrypt traffic, capture the MUSIC_U session credential sent in authenticated API requests, and modify server responses in transit, enabling account takeover and transport-layer response forgery.

### CVE-2026-108362

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-10-12T20:17:08.073 |

Privasys Remote Attestation TLS Clients provides multi-language utilities for verifying attested TLS connections. Prior to 0.11.0, TEE attestation evidence in Privasys attested TLS is accepted without requiring an explicitly authorized platform identity. When a network attacker can forge evidence or extract attestation secrets from a compromised unrevoked platform, the verifier accepts valid measurements from a different unrevoked TEE platform as though they came from the intended Attester. The attacker can impersonate the attested TLS endpoint. This issue is fixed in version 0.11.0.

### CVE-2026-87744

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-425` |
| Published | 2026-10-12T19:16:40.277 |

A flaw was found in Quarkus REST Data Panache. This vulnerability allows unauthenticated attackers to bypass security controls on generated endpoints. When a developer customizes a specific operation using @MethodProperties without explicitly re-declaring security roles, the code generator silently drops class-level security requirements. This results in the affected endpoint defaulting to permissive, unauthenticated access, potentially leading to unauthorized information disclosure or data modification.

### CVE-2026-109394

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-12T16:17:04.920 |

Thirty bees through 1.7.0 contains an authentication bypass vulnerability in PasswordController::resolveCustomer() that allows unauthenticated attackers to reset registered customers' passwords using guest account tokens. Attackers can place a guest order with the victim's email, then use the guest secure key to reset and take over the victim's account when guest checkout is enabled.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-44415

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-35` |
| Published | 2026-10-13T10:17:16.293 |

Affected systems do not properly restrict access to internal APIs and paths for authenticated users. This could allow an authenticated remote attacker to access sensitive internal information, which in the worst case could be leveraged to facilitate unauthorized access to the system or result in the deletion of data.

### CVE-2026-49483

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345;CWE-732` |
| Published | 2026-10-12T22:17:04.320 |

Code for IBMi is a Visual Studio Code extension for maintaining and compiling ILE languages on the IBMi platform. Prior to 3.0.1, IBMi components implementing IBMiComponent were accepted after checking that a procedure existed without reliably verifying component integrity. Components installed with broad public permissions allow another local account to alter a program such as GETMBRINFO. A later connection can execute the altered program under the connecting account because the LONG_COMMENT marker alone does not establish integrity. This issue is fixed in version 3.0.1.

### CVE-2026-102073

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-13T10:17:14.157 |

A vulnerability has been identified in APOGEE MBC (PPC) (BACnet) (All versions), APOGEE MBC (PPC) (P2 Ethernet) (All versions), APOGEE MEC (PPC) (BACnet) (All versions), APOGEE MEC (PPC) (P2 Ethernet) (All versions), APOGEE PXC Compact (BACnet) (All versions < V3.5.7), APOGEE PXC Compact (P2 Ethernet) (All versions < V2.8.21), APOGEE PXC Modular (BACnet) (All versions < V3.5.7), APOGEE PXC Modular (P2 Ethernet) (All versions < V2.8.21), TALON TC Compact (BACnet) (All versions < V3.5.7), TALON TC Modular (BACnet) (All versions < V3.5.7). The affected product web service does not properly validate the length of user-controllable input. This could allow an unauthenticated remote attacker to read portions of device memory or to cause a denial-of-service condition.

### CVE-2026-103418

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T08:16:59.560 |

Firefox for iOS directly interpolated the page’s HTML language attribute into translation JavaScript, allowing attacker-controlled markup to execute code in Firefox’s privileged content world and bypass the page’s Content Security Policy. This vulnerability was fixed in Firefox for iOS 157.1.

### CVE-2026-89113

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T01:16:48.153 |

SAP Commerce Cloud does not sufficiently validate certain user-supplied input before it is incorporated into a database query. An authenticated user could send specially crafted requests to affected functionality to inject arbitrary SQL commands. Successful exploitation could allow the user to read, modify or delete sensitive data from the application's database, resulting in a high impact on confidentiality, integrity and availability of the application.

### CVE-2026-82108

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-12T23:17:42.317 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of special elements used in an OS command.

### CVE-2026-82096

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-12T23:17:41.680 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-19622

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-12T23:17:37.107 |

IBM Planning Analytics 2.0, and 2.1 could allow a remote attacker to bypass authentication and escalate privileges due to improper validation of sub-requests.

### CVE-2026-19620

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-12T23:17:36.980 |

IBM Planning Analytics 2.0, and 2.1 could allow a remote attacker to gain unauthorized administrative access due to improper authentication.

### CVE-2026-102627

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-12T23:17:19.457 |

IBM TRIRIGA Application Platform 5.0.0 through 5.0.8 could allow a remote authenticated attacker to execute arbitrary code due to improper validation of file paths during archive extraction.

### CVE-2026-84318

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-10-12T21:17:22.360 |

Nginx UI is a web user interface for the Nginx web server. From 2.0.0-rc.6 until 2.4.1, the MCP tool nginx_config_add writes nginx configuration files to disk and triggers an nginx reload without calling config.ValidateConfigFile. The identical flow in the REST API (POST /api/configs) does call that function and correctly rejects dangerous directives. An authenticated attacker can exploit this gap to write config files containing any blocked directive (perl, js_import, load_module, user root, etc.), bypassing nginx-ui's entire security layer. On a server with the nginx Perl, njs, or Lua module loaded, this is post-authentication Remote Code Execution. This issue is fixed in version 2.4.1.

### CVE-2026-84317

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-693` |
| Published | 2026-10-12T21:17:22.213 |

Nginx UI is a web user interface for the Nginx web server. Prior to 2.4.1, internal/config/validation.go (ValidateConfigFile) is a security control that blocks dangerous nginx directives — js_*, perl_*, load_module of the njs/perl modules, and user root. It is enforced on three of the four config-write paths: api/config/add.go, api/config/modify.go, and mcp/config/config_modify.go. The fourth path — the MCP tool nginx_config_add (mcp/config/config_add.go) — does NOT call it: it writes the caller-supplied content straight to disk and reloads nginx. An authenticated MCP caller (or an MCP agent induced via prompt injection) can therefore inject exactly the directives the control is meant to block, leading to nginx code execution on deployments where the njs/perl module is available (e.g. the official Docker image). This issue is fixed in version 2.4.1.

### CVE-2026-84316

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-184` |
| Published | 2026-10-12T21:17:22.067 |

Nginx UI is a web user interface for the Nginx web server. Prior to 2.4.1, config.ValidateConfigDirectives splits configuration by newline and checks only the first directive token on each line even though Nginx permits multiple semicolon-separated directives on one line. An authenticated caller can place a benign directive first and a restricted load_module, js_import, perl, or user root directive later on the same line, or can use an unrestricted include directive to load restricted content. These mechanisms bypass validation on REST, nginx_config_modify, site, and stream write paths; when an executable module is available, the injected configuration can execute code in the Nginx worker context. This issue is fixed in version 2.4.1.

### CVE-2026-84313

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-10-12T21:17:21.597 |

Nginx UI is a web user interface for the Nginx web server. Prior to 2.4.1, POST /api/otp_enroll and POST /api/finish_passkey_register are registered outside RequireSecureSession and accept a normal authenticated session without verifying the current password. An attacker with a stolen JWT can bind an attacker-controlled TOTP secret when the victim has not already enabled TOTP, or can register an attacker-controlled passkey because that path has no equivalent existing-enrollment guard. These changes create persistent account access that can survive a password change and interfere with the legitimate user's authentication. This issue is fixed in version 2.4.1.

### CVE-2021-48012

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-10-12T21:17:06.057 |

fast-toml through 0.5.4 contains a prototype pollution vulnerability that allows attackers to modify Object.prototype by supplying TOML containing __proto__, constructor or prototype key segments. Attackers can pass [__proto__] or [constructor.prototype] table headers or __proto__.x dotted keys to parse() to pollute all objects, causing denial of service or authorization bypass.

### CVE-2026-57143

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-20;CWE-918` |
| Published | 2026-10-12T19:16:39.110 |

PraisonAI is a multi-agent teams system. Prior to praisonaiagents 1.6.62, searxng_search and the search_web SearxNG provider pass the LLM-controlled searxng_url parameter directly to requests.get without validating its scheme, host, port, or resolved address. Prompt-injected content can direct the default search tool to internal JSON services, distinguish open and closed internal ports, and attempt cloud-metadata requests, with returned JSON results entering agent context. This issue is fixed in praisonaiagents 1.6.62.

### CVE-2026-105465

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-12T19:16:37.610 |

IBM Db2 11.5.0 through 11.5.9, and 12.1.0 through 12.1.5 is vulnerable to privilege escalation when db2locssh is enabled with the db2 instance.

### CVE-2026-105464

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-12T19:16:37.450 |

IBM Db2 11.5.0 through 11.5.9, and 12.1.0 through 12.1.5 for Linux, UNIX and Windows (includes DB2 Connect Server) could allow a local attacker to gain elevated privileges due to improper privilege management.

### CVE-2026-77363

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-346;CWE-1385` |
| Published | 2026-10-12T18:17:23.513 |

obsidian-tc is a governed, agent-ready Model Context Protocol server for Obsidian vaults. Prior to 1.3.1, the Streamable HTTP transport does not validate the Host or Origin header or enable DNS-rebinding protection. When the documented loopback configuration uses auth.mode set to none, a malicious web page can send requests to the local MCP endpoint and receive unrestricted vault access through the http-local caller. Version 1.3.1 fixes the vulnerability by enabling host, origin, and DNS-rebinding validation.

### CVE-2026-109371

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-12T17:17:34.547 |

ZITADEL 3.0.0 before 4.18.0 contains a missing authentication vulnerability in the hosted Login V1 UI, where the change-username handler acts on the account bound to a login flow before any factor is verified. Unauthenticated attackers can submit a victim's login name and then post a new username to rename any active human user, including administrators, locking them out.

### CVE-2026-74034

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T14:17:40.087 |

Wazuh from 4.1.0 before 4.14.8 contains a missing origin check in wm_agent_upgrade that allows enrolled agents to issue upgrade_custom commands with attacker-controlled file_path. Attackers can inject an upgrade_custom message over the agent channel to read arbitrary files as root, exfiltrating /etc/shadow and client.keys.

### CVE-2026-109967

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-13T14:17:36.390 |

yt-dlp-web-ui through 4.0.0 contains a NULL pointer dereference vulnerability in the Service.Formats JSON-RPC method that allows remote unauthenticated attackers to crash the server. Attackers can send a single request with a url value like --version, causing invalid yt-dlp JSON output and an unrecovered panic that terminates the process.

### CVE-2026-109960

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T14:17:35.207 |

Froxlor 2.0.0 before 2.3.14 contains a stored cross-site scripting vulnerability that allows authenticated customers to inject HTML and JavaScript by setting a malicious theme value via customer_index.php. Script executes when an administrator views the customer overview with the Theme column enabled, letting attackers abuse the CSRF token to create administrator accounts or change server settings.

### CVE-2026-109676

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T14:17:30.747 |

FreeRDP from 3.0.0-beta1 before 3.32.0 contains a use-after-free vulnerability in smartcard handling that allows attackers to access a freed smartcard handle object after an invalid connect operation. Attackers can trigger an invalid smartcard connect operation to cause reuse of the freed handle, leading to memory corruption or crashes.

### CVE-2026-63316

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T12:17:14.473 |

A SQL injection vulnerability has been identified in Payload CMS. Improper neutralization of input provided by user into "in" and "not_in" query paramethers allows an authenticated attacker to perform SQL Injection attacks.

This issue was fixed in version 3.90.0 and 4.0.0-canary.34.

### CVE-2026-89199

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-13T10:17:21.353 |

A vulnerability has been identified in RUGGEDCOM CROSSBOW (All versions < V6.0). Affected devices do not properly restrict access to sensitive configuration items via specific database queries. This could allow an authenticated attacker to retrieve administrative credentials for various internal systems, leading to unauthorized information disclosure and privilege escalation.

### CVE-2026-89198

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T10:17:21.200 |

A vulnerability has been identified in RUGGEDCOM CROSSBOW (All versions < V6.0). Affected devices do not properly validate or sanitize the filename of firmware files uploaded to the system. This could allow an authenticated attacker with specific privileges to execute arbitrary SQL commands on the underlying database.

### CVE-2026-89197

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T10:17:21.060 |

A vulnerability has been identified in RUGGEDCOM CROSSBOW (All versions < V6.0). Affected devices do not properly validate or sanitize input in the Value field of notification conditions processed during the Notification Profile configuration. This could allow an authenticated attacker with specific privileges to execute arbitrary SQL commands on the underlying database.

### CVE-2026-89196

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T10:17:20.920 |

A vulnerability has been identified in RUGGEDCOM CROSSBOW (All versions < V6.0). Affected devices do not properly validate or sanitize input in facility names processed during the Bulk Import/Export workflow. This could allow an authenticated attacker with specific privileges to execute arbitrary SQL commands on the underlying database.

### CVE-2026-85114

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T10:17:20.640 |

A vulnerability has been identified in .NET Client Library for SIMATIC S7 Webserver API (All versions < V3.3.61). Affected applications do not properly validate filenames received from remote servers during ticket downloads.

This could allow an attacker who can manipulate the ticket response to write arbitrary files outside the intended download directory and, when overwriting is enabled, replace existing files accessible to the application.

### CVE-2026-59241

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-13T10:17:16.623 |

A vulnerability has been identified in SIMATIC WinCC V7.5 (All versions), SIMATIC WinCC V8.0 (All versions < V8.0 Update 11), SIMATIC WinCC V8.1 (All versions < V8.1 Update 7). The affected application does not sufficiently restrict the permissions assigned to a database role.
This could allow an authenticated remote attacker with database access to escalate privileges and execute arbitrary commands on the host system where SIMATIC WinCC is installed, potentially leading to a compromise of the system.

### CVE-2026-102076

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T10:17:14.687 |

A vulnerability has been identified in APOGEE MBC (PPC) (BACnet) (All versions), APOGEE MBC (PPC) (P2 Ethernet) (All versions), APOGEE MEC (PPC) (BACnet) (All versions), APOGEE MEC (PPC) (P2 Ethernet) (All versions), APOGEE PXC Compact (BACnet) (All versions < V3.5.7), APOGEE PXC Compact (P2 Ethernet) (All versions < V2.8.21), APOGEE PXC Modular (BACnet) (All versions < V3.5.7), APOGEE PXC Modular (P2 Ethernet) (All versions < V2.8.21), TALON TC Compact (BACnet) (All versions < V3.5.7), TALON TC Modular (BACnet) (All versions < V3.5.7). The affected product web service does not properly validate user-supplied input in upload code. This could allow an unauthenticated remote attacker to cause a denial of service.

### CVE-2026-102075

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T10:17:14.543 |

A vulnerability has been identified in APOGEE MBC (PPC) (BACnet) (All versions), APOGEE MBC (PPC) (P2 Ethernet) (All versions), APOGEE MEC (PPC) (BACnet) (All versions), APOGEE MEC (PPC) (P2 Ethernet) (All versions), APOGEE PXC Compact (BACnet) (All versions < V3.5.7), APOGEE PXC Compact (P2 Ethernet) (All versions < V2.8.21), APOGEE PXC Modular (BACnet) (All versions < V3.5.7), APOGEE PXC Modular (P2 Ethernet) (All versions < V2.8.21), TALON TC Compact (BACnet) (All versions < V3.5.7), TALON TC Modular (BACnet) (All versions < V3.5.7). The affected product web service does not properly validate user input in multipart handling. This could allow an unauthenticated remote attacker to cause a denial of service.

### CVE-2026-102074

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T10:17:14.400 |

A vulnerability has been identified in APOGEE MBC (PPC) (BACnet) (All versions), APOGEE MBC (PPC) (P2 Ethernet) (All versions), APOGEE MEC (PPC) (BACnet) (All versions), APOGEE MEC (PPC) (P2 Ethernet) (All versions), APOGEE PXC Compact (BACnet) (All versions < V3.5.7), APOGEE PXC Compact (P2 Ethernet) (All versions < V2.8.21), APOGEE PXC Modular (BACnet) (All versions < V3.5.7), APOGEE PXC Modular (P2 Ethernet) (All versions < V2.8.21), TALON TC Compact (BACnet) (All versions < V3.5.7), TALON TC Modular (BACnet) (All versions < V3.5.7). The affected product FTP service does not properly validate the length of user-controllable input. This could allow an unauthenticated remote attacker to cause a denial of service.

### CVE-2026-92883

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T02:17:00.570 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 19.1 before 19.2.8, 19.3 before 19.3.5, and 19.4 before 19.4.2  that, under certain conditions, could have allowed an authenticated user to execute arbitrary JavaScript in the context of other users' browser sessions via a specially crafted repository, due to improper sanitization of HTML attributes in syntax-highlighted output.

### CVE-2026-109667

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-12T23:17:34.210 |

Frappe ERPNext before 15.111.0 and 16.x before 16.22.0 contains a privilege escalation vulnerability in a record-creation endpoint that takes the record type from the request and inserts the record with permission checks disabled. Any authenticated user, including one holding no operational role, can supply a privileged record type to create privileged accounts and take full control of the site.

### CVE-2026-109652

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-10-12T23:17:31.723 |

Frappe ERPNext before 15.119.1 and 16.x before 16.32.0 contains a server-side template injection vulnerability because user-controlled message fields are not validated before template rendering, allowing expressions to run in an unrestricted context. Authenticated attackers holding a common operational role can inject template expressions to read and write arbitrary database data, delete documents, send outbound requests from the server, and send mail from the site.

### CVE-2026-109608

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T23:17:24.497 |

Frappe ERPNext before 15.121.0 and 16.x before 16.34.0 contains an SQL injection vulnerability in several endpoints that lack input validation. Any authenticated user, including one with no assigned roles, can send specially crafted requests to read other users' sensitive information and escalate to a privileged account.

### CVE-2024-58390

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-12T23:17:18.140 |

Frappe before 14.81.4 and 15.x before 15.41.0 contains an improper privilege management vulnerability involving a certain document action that permits escalation from the Website User role to System Manager. Authenticated attackers with Website User access can combine this document action with additional steps to obtain administrative System Manager privileges in the Frappe application.

### CVE-2026-84314

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-862` |
| Published | 2026-10-12T21:17:21.753 |

Nginx UI is a web user interface for the Nginx web server. Prior to 2.4.1, the POST /api/users/:id user-management endpoint permits an authenticated user to change another user's password without passing RequireSecureSession, even though the self-service password-change path requires that step-up. An attacker with an authenticated account can change the initial administrator's password, invalidate existing administrator tokens, and then authenticate as the administrator. This issue is fixed in version 2.4.1.

### CVE-2026-18537

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-12T21:17:16.940 |

IBM Maximo Application Suite - Location Service for Esri Component 9.2, 9.1, and 9.0 is vulnerable to improper input validation due to an unsanitised container image reference in a Kubernetes operator template.

### CVE-2026-18529

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-12T21:17:16.653 |

IBM Maximo Application Suite - Location Service for Esri Component 9.2, 9.1, and 9.0 is vulnerable to command injection due to improper sanitisation of a user-controlled value passed to a shell command in a Kubernetes operator task.

### CVE-2026-109563

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-12T21:17:12.713 |

N3.js before 2.11.1 contains a regular expression denial of service vulnerability in the N3Lexer number pattern that backtracks quadratically on long digit runs. Attackers can supply untrusted Turtle or N3 input containing long runs of digits that do not end a number, blocking the Node.js event loop and causing denial of service.

### CVE-2026-109380

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-10-12T21:17:11.153 |

modern-tar 0.3.5 through 0.8.5 contains a memory exhaustion vulnerability that allows attackers to produce negative entry sizes via non-octal bytes parsed by readOctal(). Attackers can supply a crafted, optionally gzip-compressed, archive to unpackTar() that buffers chunks indefinitely, exhausting process memory and suppressing later entries.

### CVE-2021-48011

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-12T21:17:05.903 |

Servor 1.0.0 through 4.0.2 contains a path traversal vulnerability that allows unauthenticated remote attackers to escape the served root by sending URL-encoded dot segments. Attackers can send %2e%2e/ sequences, which decodeURI() decodes before path.join() in serveStaticFile and serveDirectoryListing, to read arbitrary files and list directories outside the root.

### CVE-2020-37280

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-10-12T21:17:05.733 |

cbor-sync through 1.0.4 contains a resource exhaustion vulnerability in CBOR.decode that trusts declared array and map lengths without checking remaining input. Remote attackers can supply a tiny crafted CBOR payload declaring huge lengths to drive billions of iterations, exhausting CPU and process memory.

### CVE-2026-109363

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-12T17:17:33.953 |

ZcashFoundation Zebra 6.4.0 before 6.4.2 parses version 6 transactions carrying a pre-NU6.3 consensus branch ID, but the size computation during UnminedTx construction treats re-serialization of the Orchard bundle as infallible, so the resulting error trips an expect that aborts zebrad. Unauthenticated peers can send a single pre-handshake tx message to crash the node, and can repeat this after each restart.

### CVE-2026-109359

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-12T17:17:33.327 |

Contrast 1.8.0 before 1.24.1 contains an improper verification vulnerability in Coordinator peer recovery that fails to confirm the serving peer uses the same manifest generation. Attackers with write access to manifest history can replay a superseded history head so withdrawn workloads obtain trusted mesh certificates, or with the secret seed disclose the Mesh CA key.

### CVE-2026-109326

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-527` |
| Published | 2026-10-12T17:17:28.017 |

Grav before 2.1.7 contains an information disclosure vulnerability because bundled nginx, lighttpd, IIS, and Caddy 2 configurations block .git only at document root. Unauthenticated attackers can request nested repositories such as user/.git to retrieve Git config, refs, and objects, reconstructing unpublished history or committed secrets.

### CVE-2026-109325

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-12T17:17:27.860 |

Grav from 2.0.22 before 2.1.7 contains an authentication bypass vulnerability in the Clockwork profiler that trusts loopback REMOTE_ADDR values. Unauthenticated attackers behind a same-host HTTP proxy can read profiler records exposing system and plugin configuration, secrets, request metadata, and queries.

### CVE-2026-109318

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-12T17:17:26.807 |

Grav Git Sync 1.0.2 through 3.4.12 contains a command injection vulnerability that allows authenticated content editors to execute OS commands by injecting shell substitutions into profile fields. When the gravuser or gravfull author mode is enabled, attackers can set a malicious username, full name, or email that reaches PHP exec() via git commit --author, running commands as the web-server account.

### CVE-2026-109308

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-12T17:17:25.227 |

Craft CMS 4.0.0 before 4.18.7 and 5.0.0 before 5.10.14 passes the raw 'updates' request parameter in AppController::actionCacheUpdates to UpdatesModel without Component::cleanseConfig(), allowing behavior and event-handler injection. Authenticated control panel users with the performUpdates permission or Updates-utility access can supply 'as' or 'on' keys, such as an AttributeTypecastBehavior gadget, to execute arbitrary code.

### CVE-2026-109305

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-10-12T17:17:24.773 |

Craft CMS from 5.10.2 before 5.10.14 contains a Twig sandbox bypass that allows non-admin users to invoke PHP callables through the "has some" and "has every" operators. Users with the System Messages permission can supply two-argument callables such as passthru or system in sandboxed templates to execute code as the web user.

### CVE-2026-109398

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-10-12T16:17:05.397 |

Gumlet php-image-resize before 3.0.1 contains a denial of service vulnerability because the ImageResize constructor in lib/ImageResize.php passes images to GD imagecreatefrom* functions without pixel limits. Remote attackers can upload small, highly compressed images that decode to large bitmaps, exhausting PHP memory and terminating the worker process.

### CVE-2026-74037

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-10-13T14:17:40.570 |

Wazuh 4.0.0 before 4.14.8 fails to invalidate issued tokens for run_as users with zero static roles, because check_token never consults the blacklist. Attackers with revoked administrator grants can continue authenticating and self-link the administrator role to permanently retain privileged access.

### CVE-2026-74036

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T14:17:40.410 |

Wazuh from 4.3.0 before 4.14.8 contains a remote code execution vulnerability where SCA policy trust is determined by file path rather than configuration source. Attackers controlling a manager can write unsigned policy files to var/incoming via the upgrade channel and reference them to execute command checks as root on agents.

### CVE-2026-74035

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T14:17:40.253 |

Wazuh versions from 4.6.0 before 4.14.8 contain an authentication bypass vulnerability where security.update_user places the reserved user guard and password policy inside a falsy truthiness check. A delegated user administrator can send an empty password to the user update endpoint, bypassing the reserved user guard to take over the wazuh superuser account and authenticate with empty credentials.

### CVE-2026-65172

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T13:17:33.410 |

NVIDIA AIStore for Linux and Kubernetes contains a missing authorization vulnerability in the ETL management API where an unauthenticated remote attacker may access ETL information or control existing ETL jobs by sending crafted GET or POST requests to an AIStore proxy.

A successful exploit may lead to information disclosure and unauthorized start or stop operations that affect the integrity and availability of ETL data-processing pipelines.

### CVE-2026-65170

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-13T13:17:33.283 |

NVIDIA AIStore for Linux contains a vulnerability in the experimental HT backend where an unauthenticated remote attacker may cause server-side request forgery by supplying a crafted original URL. A successful exploit of this vulnerability may lead to information disclosure.

### CVE-2026-65101

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-13T13:17:31.400 |

NVIDIA AIStore for Linux contains a vulnerability in the distributed sort component where an attacker could cause server-side request forgery by supplying a crafted external key map URL. A successful exploit of this vulnerability might lead to information disclosure.

### CVE-2026-109157

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-10-13T11:17:14.873 |

A vulnerability was found in TRENDnet TEW-432BRP 3.10B20. Affected by this vulnerability is the function formTcpipSetup of the file /goform/formTcpipSetup. Performing a manipulation of the argument Name results in stack-based buffer overflow. It is possible to initiate the attack remotely. The exploit has been made public and could be used. The vendor confirms: "As this router was EOL'd in 2011, we have no way of testing if such vulnerability exists. We will notify our customers of a potential vulnerability on this product." This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-13138

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-602` |
| Published | 2026-10-13T09:17:17.127 |

Client-Side Enforcement of Server-Side Security vulnerability in Divasoft Software and E-Commerce Inc. Biletiva Ticketing Platform allows Manipulating State.

This issue affects Biletiva Ticketing Platform: through 2026-07-23.

### CVE-2026-109108

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-10-13T08:16:59.917 |

A security vulnerability has been detected in Wavlink WL-WN530BE1-A 251117. This affects the function popen of the file /cgi-bin/uploadVpn.cgi. Such manipulation of the argument Type leads to os command injection. The attack may be performed from remote. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-108971

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345;CWE-347` |
| Published | 2026-10-13T06:16:50.090 |

A flaw has been found in D-Link DCS-930L B1.08B4. This impacts the function mpfd_decode of the file bootloader_region.bin of the component Emergency HTTP Recovery Server. Executing a manipulation of the argument firmware can lead to improper verification of cryptographic signature. The attack may be performed from remote. The exploit has been published and may be used.

### CVE-2026-109633

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-12T23:17:28.220 |

Frappe ERPNext before 15.119.1 and 16.x before 16.32.0 contains a stored cross-site scripting vulnerability because content submitted through a public-facing booking page is stored without neutralization. Unauthenticated attackers can submit crafted content that is rendered as raw HTML in a privileged user's session, executing script to act as that user and take over the account.

### CVE-2025-71432

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-12T23:17:19.297 |

Frappe ERPNext before 14.92.1 and 15.x before 15.83.0 contains a reflected cross-site scripting vulnerability due to missing input validation on a certain page, allowing arbitrary JavaScript to execute in authenticated sessions. Remote attackers can lure a logged-in user into opening a crafted URL to run injected script and take over the victim's account.

### CVE-2026-109567

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-12T21:17:13.347 |

Rapyd Admin from 9.0.0 before 9.20.0 contains an improper privilege management vulnerability in the UsersEdit Livewire component that allows users with the edit users permission to assign themselves the admin role. Attackers holding roles such as the shipped operator role can submit the admin role ID for their own account, lifting tenant scoping, bypassing per-record authorization, and enabling impersonation.

### CVE-2026-65954

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-10-12T19:16:39.567 |

PHPCSUtils is a suite of utility functions for use with PHP_CodeSniffer. From 1.0.0-alpha1 until 1.2.3, PHPCSUtils\AbstractSniffs\AbstractArrayDeclarationSniff::getActualArrayKey() evaluates attacker-controlled array-key expressions with eval(), allowing callback-form keys in untrusted PHP code scanned by an extending sniff to execute arbitrary commands on the scanning host. Known reachable paths include Universal.Arrays.DuplicateArrayKey and Universal.Arrays.MixedArrayKeyTypes. This issue is fixed in version 1.2.3.

### CVE-2026-108915

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-10-12T18:17:21.770 |

A vulnerability has been found in Edimax BR-6208AC 1.32. This affects an unknown part of the file /goform/formWlanMP. Such manipulation of the argument ateBW leads to buffer overflow. The attack can be executed remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-109347

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-12T17:17:31.517 |

Adminer before 6.1.1 contains a remote code execution vulnerability that allows authenticated SQLite users to bypass ATTACH and VACUUM INTO restrictions by prefixing statements with a UTF-8 byte-order mark. Attackers can attach a database file at a PHP-served path and create a table named with PHP code to execute it as the web server user.

### CVE-2026-109343

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-12T17:17:30.890 |

SurrealDB before 3.3.0 allows cross-tenant access because the SurrealQL USE statement switches a session to any namespace/database without checking that the caller's authenticated level covers it. Authenticated namespace, database, or record users can switch to another tenant and read, create, update, or delete rows in tables whose PERMISSIONS allow it, such as PERMISSIONS FULL.

### CVE-2026-109334

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-12T17:17:29.363 |

SurrealDB before 3.3.0 does not check the caller-selected namespace or database against the level at which a namespace- or database-level system user authenticated, allowing cross-tenant access. An authenticated attacker can set the Surreal-NS/Surreal-DB headers on /sql or call the RPC use method to read, create, modify, and delete rows and read DEFINE PARAM values in another tenant where table PERMISSIONS allow it.

### CVE-2026-109317

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-12T17:17:26.653 |

Grav grav-plugin-api before 1.0.36 contains a privilege escalation vulnerability that allows delegated user managers to obtain super-admin access by storing positive scalar admin or api parent grants. Attackers with api.users.write can edit account access maps or invitations so the inheriting permission resolver satisfies requireSuper checks, accessing super-only API endpoints.

### CVE-2026-109313

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-12T17:17:26.043 |

Grav Login plugin 2.7.0 before 3.9.9 contains an authentication bypass vulnerability that allows attackers with a valid password to skip two-factor authentication through remember-me cookie restoration. Attackers can obtain a persistent remember-me cookie after the password step and restore it as a fully authorized session without completing the second factor.

### CVE-2026-109312

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-12T17:17:25.890 |

Grav Login plugin 2.7.0 before 3.9.9 contains an authentication bypass in processUserProfile(), which checks that the session user exists but not that a pending front-end 2FA session is fully authorized. Attackers with a victim's password who can publish a page form without an access rule can invoke update_user before completing 2FA to disable twofa_enabled and take over the account.

### CVE-2026-109286

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-10-12T17:17:21.613 |

Open WebUI from 0.7.0 before 0.11.4 contains a cross-origin message handling vulnerability in SyncStatsModal that allows any website to steal a signed-in user's session token by posting unvalidated verify:chat messages. Attackers can supply a path-traversal chat id redirecting the authenticated stats export request to the auths endpoint, receiving the victim's JWT for full API access.

### CVE-2026-109237

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-12T17:17:14.233 |

Crawl4AI from 0.9.0 before 0.9.4 contains an untrusted-config gate bypass that allows non-admin API clients to construct forbidden config objects by wrapping them in dict-type wrappers. Attackers can send a laundered LLMConfig with api_token set to an env reference via /config/dump to read SECRET_KEY and provider keys, enabling admin JWT forgery.

### CVE-2026-108914

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-10-12T17:17:13.890 |

A flaw has been found in Edimax BR-6208AC 1.32. Affected by this issue is some unknown functionality of the file /goform/formWlSiteSurvey. This manipulation of the argument ifname causes buffer overflow. Remote exploitation of the attack is possible. The exploit has been published and may be used. The vendor was contacted early about this disclosure but did not respond in any way. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-92682

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-12T16:17:07.480 |

In @neo4j/graphql versions from 7.0.0 up to but not including 7.6.4, the none quantifier in @authorization filters on relationships and connections is not negated when translated to Cypher, so it behaves like some. A rule such as "none of the related denied users matches the JWT subject" therefore returns exactly the records it was meant to exclude, and excludes those it was meant to return. An authenticated user whom such a rule is meant to deny can read the protected records. This is also the case for mutations, so the impact is that sensitive data could also be created and deleted by users that shouldn't have access according to the typedefs. Fixed in 7.6.4.

### CVE-2026-85954

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-12T16:17:06.940 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 can evaluate user-controlled values supplied to certain higher-order XQuery functions in an elevated security context, which could result in privilege escalation beyond the attacker's granted permissions.

### CVE-2026-109397

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-12T16:17:05.233 |

Thelia before 3.1.2 and 3.2.x before 3.2.1 contains an unrestricted file upload vulnerability that allows authenticated back-office users to upload PHP files by appending a trailing space to filenames. FileProcessorService validates the raw filename but FileManager::sanitizeFileName() strips the space, storing an executable .php file under public/cache/documents/ for code execution as the web server user.

### CVE-2026-108896

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-10-12T15:17:07.423 |

A vulnerability was found in Linksys E1700 1.0.0.4.003. This affects the function setLinksysIpv6 of the file /goform/setLinksysIpv6. The manipulation of the argument _6rd_prefix/_6rd_prefix_len results in os command injection. The attack can be launched remotely. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-108895

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-10-12T15:17:07.227 |

A weakness has been identified in Linksys E1700 1.0.0.4.003. The affected element is the function setDMZ of the file /goform/setDMZ. Executing a manipulation of the argument MAC_addr can lead to os command injection. The attack can be executed remotely. The exploit has been made available to the public and could be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-74043

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T14:17:41.003 |

Wazuh from 4.1.1 before 4.14.8 contains a path traversal vulnerability in upload_list_file, upload_rule_file, and upload_decoder_file that allows malicious cluster workers to write files at arbitrary paths. Attackers holding the cluster key can send DistributedAPI requests with ../ sequences in filename, bypassing REST controller validation, to write files as the wazuh user.

### CVE-2026-101020

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-13T09:17:13.257 |

An incorrect permission assignment for critical resource issue exists in AssetView, AssetView CLOUD, and AssetView Cloud +. If this vulnerability is exploited, a local authenticated attacker who can log in to the Windows system where Management Console or Client Terminal for the product is running may gain SYSTEM privileges.

### CVE-2026-75826

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-13T07:16:32.573 |

Command injection in the backup function in Teltonika Networks RUTOS 7.22 before 7.24.6 and 7.25 before 7.25.2 (RUT, RUTX, RUTM, RUTC, ATRM, CAP, OXA, DAP, TRB, OTD, and EBG devices), RUTOS 7.22 before 7.25.2 (TAP devices), and TSWOS 1.9 before 1.10.4 (TSW and SWM devices) allows a remote authenticated attacker to execute arbitrary OS commands.

### CVE-2026-16301

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T02:16:58.583 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 18.7 before 19.2.8, 19.3 before 19.3.5, and 19.4 before 19.4.2 that, under certain conditions, could have allowed an authenticated user with Developer role to execute CI/CD pipelines on protected branches without authorization due to improper authorization checks in the downstream pipeline creation service.

### CVE-2026-109673

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-12T23:17:35.210 |

Frappe ERPNext before 15.103.0 and 16.x before 16.12.0 contains a stored cross-site scripting vulnerability because the names of certain records are not properly neutralized when rendered on some dashboards, tools, and portals. Authenticated attackers can craft malicious record names that execute scripts in other users' browsers, enabling data access, modification, and token theft, especially against privileged users.

### CVE-2026-109671

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-12T23:17:34.873 |

Frappe ERPNext before 15.113.0 and 16.x before 16.24.0 contains a stored cross-site scripting vulnerability in a profile field that is rendered without escaping into portal pages. Low-privilege attackers can store malicious script in the field that executes in the browser of any administrator viewing those pages, enabling administrator account takeover.

### CVE-2026-109653

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-12T23:17:31.890 |

Frappe ERPNext before 15.119.0 and 16.x before 16.31.0 contains a stored cross-site scripting vulnerability because record fields are rendered into an HTML attribute context without escaping. A low-privilege user can store a malicious payload in a record field that executes in the browser of any privileged user who opens the affected page, enabling account takeover.

### CVE-2026-109612

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-12T23:17:25.157 |

Frappe ERPNext before 15.120.0 and 16.x before 16.33.0 contains a stored cross-site scripting vulnerability in a report view that interpolates stored record names into markup without escaping. Authenticated users able to create records can store crafted record names that execute script in the session of any user who later opens the report.

### CVE-2026-109604

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-12T23:17:24.327 |

Frappe ERPNext before 15.112.0 and 16.x before 16.23.0 contains a stored cross-site scripting vulnerability because a tool view interpolates stored record names into markup without escaping. An authenticated user able to create such records can give them malicious names, executing script in the session of any user who later opens that tool.

### CVE-2026-109558

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-12T21:17:11.940 |

EdgeEver 1.6.0 through 1.112.0 contains a stored cross-site scripting vulnerability in TemplatesPane.tsx that renders template contentMarkdown with raw HTML via dangerouslySetInnerHTML without sanitization. Attackers can write templates containing HTML event handlers through an API or MCP token to run script on preview and access the privileged window.edgeeverDesktop bridge.

### CVE-2026-109358

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-12T17:17:33.177 |

Edgeless Systems Contrast 1.8.0 before 1.24.1 contains an incorrect permissions vulnerability where the node installer writes the containerd config world-writable (0666). Local unprivileged users on the node can modify the containerd config, for example overwriting the runc location, to escalate privileges.

### CVE-2026-109346

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-451` |
| Published | 2026-10-12T17:17:31.367 |

better-auth from 1.3.8-beta.3 before 1.7.0-rc.3 contains a UI misrepresentation vulnerability in the deviceAuthorization plugin because GET /device omits the requesting client_id and scope. Attackers can start a device request via /device/code, trick signed-in users into approving the code, then redeem it at /device/token for a live session token.

### CVE-2026-109329

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-12T17:17:28.500 |

Admidio 4.3.2 through 4.3.17 and 5.0.0 before 5.0.15 contains a broken access control vulnerability that allows role administrators to assign users to roles in other organizations. Attackers can submit crafted assign requests to members_assignment.php with a foreign role UUID to gain privileged membership, log into that organization, and edit its user profiles.

### CVE-2026-109314

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-12T17:17:26.193 |

Grav Login plugin 1.2.0 before 3.9.9 contains an information disclosure vulnerability that allows publishers to obtain password-reset tokens by authoring a page at the reset route. When a victim opens an emailed reset link, the publisher-controlled page rendered by Login::getPage() exposes the username and bearer token, enabling takeover of more privileged accounts.

### CVE-2026-109291

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-12T17:17:22.353 |

Open WebUI from 0.6.33 before 0.11.4 contains a cross-site scripting vulnerability that allows authenticated users to execute script in victims' sessions by storing javascript: URLs in citation embed_url fields. Attackers can share a crafted chat whose citation, when clicked, is passed to window.open, letting them steal localStorage.token and act as the victim.

### CVE-2026-85953

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-22;CWE-269` |
| Published | 2026-10-12T16:17:06.810 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 contain privileged legacy InfoStudio modules that do not sufficiently validate user-controlled file paths and user-context values. Exploitation could result in unauthorized access to server files or execution under an unintended identity.

### CVE-2026-85952

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-12T16:17:06.680 |

Affected Linux-based Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 contain a server-side request forgery vulnerability that could allow an authenticated attacker to access internal cloud services, potentially resulting in unauthorized access to cloud credentials.

### CVE-2026-85951

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-12T16:17:06.553 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 on Azure contain a server-side request forgery vulnerability that could allow an authenticated attacker to access internal cloud services, potentially resulting in unauthorized access to cloud credentials or tokens.

### CVE-2026-74033

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T14:17:39.943 |

Wazuh from 4.1.1 before 4.14.8 contains a path traversal vulnerability in the get_lists() and delete_list_file() CDB list handlers that allows compromised cluster workers to read or delete master files. Attackers can send traversal or absolute-path filenames through the internal cluster RPC path, bypassing REST validation and RBAC to delete files like rbac.db.

### CVE-2026-109965

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T14:17:36.060 |

Serena before 2.0.0 contains an improper link resolution vulnerability that allows attackers to access files outside the project root by committing symlinks inside a repository. Project.is_path_in_project() normalizes paths lexically without resolving symlinks, so file tools like read_file and create_text_file can read or overwrite files such as SSH keys or cloud credentials.

### CVE-2026-109961

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-10-13T14:17:35.407 |

Froxlor 0.10.0 before 2.3.14 contains a newline injection vulnerability that allows authenticated customers to inject arbitrary entries into the root-owned NSS group database via the unvalidated additional_members parameter of the Ftps.add API. Attackers can embed newline characters that the REBUILD_NSSUSERS cron writes unsanitized into /var/lib/extrausers/group, creating privileged group entries for local privilege escalation.

### CVE-2026-89200

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T10:17:21.500 |

A vulnerability has been identified in RUGGEDCOM CROSSBOW (All versions < V6.0). Affected devices do not properly validate or sanitize input in the Name and Value fields for custom file labels. This could allow an authenticated attacker with administrative privileges to execute arbitrary SQL commands on the underlying database.

### CVE-2026-72895

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1394` |
| Published | 2026-10-13T10:17:20.130 |

A vulnerability has been identified in SIMATIC IPC BX-21A (All versions < V31.01.13), SIMATIC IPC RW-543A (All versions < V1.1.4), SIMATIC IPC227G / IPC277G / IPC277G PRO / IPC327G / IPC377G (All versions < V28.01.15). A BIOS vendor test key is present in the UEFI Secure Boot key database. This could allow a local attacker with physical or administrative access to the device to boot an operating system or UEFI application signed with that test key, bypassing UEFI Secure Boot protections even when Secure Boot is enabled, potentially leading to a full loss of confidentiality, integrity, and availability of the device.

### CVE-2026-35001

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T02:16:59.010 |

OpenS100 through commit daa35b contains an integer overflow vulnerability in the S-102 Bathymetric Surface parser that allows remote attackers to cause a heap-based buffer overflow by opening a crafted S-102 HDF5 file with malicious grid dimension metadata. Attackers can exploit the unvalidated multiplication of numPointsLatitudinal and numPointsLongitudinal values in the S102_VG_BathymetryCoverage::Read() function to trigger a 32-bit integer wraparound, resulting in undersized heap buffer allocation and subsequent out-of-bounds writes that lead to application crash or arbitrary code execution.

### CVE-2026-109559

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-12T21:17:12.090 |

EdgeEver Desktop 1.6.26 through 1.112.0 contains a navigation allowlist bypass that lets attackers load arbitrary origins in the main window via string-prefix URL matching. Attackers can embed a link using userinfo syntax after the dev-server prefix, for example in a note-template preview, to obtain the edgeeverDesktop bridge including session token, sidecar RPC, and ACP channels.

### CVE-2026-109557

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-12T21:17:11.790 |

EdgeEver through 1.112.0 contains a stored cross-site scripting vulnerability in setMemoDragPreview that allows attackers to inject script through notebook names or memo titles. Attackers can set malicious names via MCP create_notebook, rename_notebook or create_memo tools, running script on drag with access to the desktop bridge's session token.

### CVE-2026-109290

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-12T17:17:22.210 |

Open WebUI from 0.11.1 before 0.11.4 contains a stored cross-site scripting vulnerability in DocxPreview.svelte that allows authenticated users to execute script by uploading crafted DOCX attachments. Attackers can embed an OOXML altChunk HTML part or script-scheme hyperlink to steal a previewing administrator's session token from local storage and take over the instance.

### CVE-2026-85950

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-12T16:17:06.427 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 contain an authorization flaw that could allow a remote attacker with administrative privileges to access authentication material associated with higher-privileged users, potentially resulting in unauthorized administrative access.

### CVE-2026-109956

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T14:17:34.520 |

NLTK through 3.10.3 contains a path traversal vulnerability in WekaClassifier that allows attackers to bypass nltk.pathsec containment by supplying unvalidated model paths. Attackers controlling the model_filename or model argument can make the weka JVM write files via -d or probe files via -l outside allowed data roots.

### CVE-2026-109954

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T14:17:34.190 |

Parse Server 5.4.0 before 8.6.96 and 9.0.0 before 9.10.2-alpha.5 shares transactional batch state across concurrent requests, letting any client's transactional batch request interfere with other clients' database writes. On PostgreSQL or MongoDB replica sets and sharded clusters, other clients' acknowledged writes are rolled back if the batch fails, and PostgreSQL transactions can remain open indefinitely, causing subsequent writes to fail.

### CVE-2025-58774

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:H/SC:L/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-805` |
| Published | 2026-10-13T14:17:18.580 |

AMI APTIOV contains vulnerabilities
in BIOS where users may cause “Buffer Access with Incorrect Length
Value” by local access. Successful exploitation of this vulnerability could
lead to buffer overflows, memory corruption, and arbitrary code execution, and
also impact Confidentiality, Integrity, and Availability.

### CVE-2026-93886

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T00:17:01.933 |

IBM i 7.3, 7.4, 7.5, and 7.6 could allow a remote authenticated attacker to execute arbitrary script code due to improper validation of user-supplied input.

### CVE-2026-84319

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-10-12T21:17:22.517 |

Nginx UI is a web user interface for the Nginx web server. Prior to 2.4.1, the regular HTTP configuration API rejects restricted Nginx directives such as load_module, js_import, and js_content. However, the MCP configuration interface allows a secondary authenticated user to write and apply equivalent restricted configuration content. This allows the user to load ngx_http_js_module.so, import attacker-controlled JavaScript, reload Nginx, and execute NJS in the Nginx worker context. This issue is fixed in version 2.4.1.

### CVE-2026-84315

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T21:17:21.900 |

Nginx UI is a web user interface for the Nginx web server. Prior to 2.4.1, Nginx UI does not apply RequireSecureSession to multiple authenticated mutation routes even though OTP-enabled users are expected to present a fresh X-Secure-Session-ID for sensitive actions. A stolen authenticated session can therefore create or alter automatic backups, DNS credentials and records, certificates and ACME users, Nginx control settings, and site or stream automation without completing the OTP or passkey step-up. This issue is fixed in version 2.4.1.

### CVE-2026-92877

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-12T15:17:09.890 |

The JAXB factory methods historically relied solely on `FEATURE_SECURE_PROCESSING` to prevent XML External Entity (XXE) resolution. On JAXP implementations where that feature alone does not block external entity resolution, an attacker who can get untrusted XML unmarshalled through JAXB can read local files via out-of-band XXE.

### CVE-2025-58772

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-10-13T14:17:18.327 |

AMI APTIOV contains vulnerabilities in BIOS where users may cause 
“Classic Buffer Overflow” by local access. Successful exploitation of this vulnerability could lead to buffer overflows, memory corruption, and arbitrary code execution, and also impact Confidentiality, Integrity, and Availability.

### CVE-2026-14814

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-625` |
| Published | 2026-10-13T02:16:58.330 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions before 19.2.8, 19.3 before 19.3.5, and 19.4 before 19.4.2 that, under certain conditions, could have allowed a user to poison cached responses for raw repository files, causing targeted users' CI/CD pipelines to execute specially crafted content and potentially exposing protected environment variables, due to improper validation of repository references.

### CVE-2026-19627

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-12T23:17:37.237 |

IBM Planning Analytics 2.0, and 2.1 could allow a remote attacker to read arbitrary host files and overwrite certain application files due to improper validation of file paths.

### CVE-2023-54411

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-12T23:17:17.783 |

Frappe framework before 13.32.0 uses weak authentication for print view access, because the print view key can be derived from data exposed by other whitelisted API endpoints. Attackers can generate a valid key to view documents through the print view without proper permissions.

### CVE-2026-96266

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-12T21:17:24.330 |

IBM Power Systems Firmware FW1060.00 through FW1060.81 is affected by a vulnerability in host firmware configuration parsing. An attacker with authenticated service-level access to the FSP can write specially crafted configuration data to cause memory corruption in the host firmware boot stage during system IPL, compromising the host firmware boot stack and the hypervisor subsequently loaded by it. Successful exploitation results in a confidentiality, integrity, and availability impact to the managed system.

### CVE-2026-96265

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-12T21:17:24.190 |

IBM Power Systems Firmware FW1060.00 through FW1060.81 is affected by a vulnerability in the service processor mailbox interface. An attacker with authenticated service-level access to the FSP can send a specially crafted mailbox message to read or modify arbitrary regions of Hostboot memory, compromising the host firmware boot stack and the hypervisor subsequently loaded by it. Successful exploitation results in a confidentiality, integrity, and availability impact to the managed system.

### CVE-2026-96264

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-12T21:17:24.053 |

IBM Power Systems Firmware FW1060.00 through FW1060.81  is affected by a vulnerability in the service processor mailbox interface. An attacker with authenticated service-level access to the FSP can send a specially crafted mailbox message to overflow host firmware runtime attribute storage, allowing arbitrary code to be executed in the host firmware runtime. This gives the attacker full access to the managed system's memory and hardware interfaces, resulting in a confidentiality, integrity, and availability impact to the managed system.

### CVE-2026-96263

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-12T21:17:23.893 |

IBM Power Systems Firmware FW1120.00 through FW1120.01, FW1110.00 through FW1110.31, and FW1060.00 through FW1060.81 is affected by a vulnerability in the host firmware boot process image validation path. An attacker with service access to the service processor can supply a maliciously crafted code update image, allowing arbitrary code to be executed on the host system. Successful exploitation could result in a confidentiality, integrity, and availability impact to the affected host system.

### CVE-2026-96262

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-12T21:17:23.753 |

IBM Power Systems Firmware FW1060.00 through FW1060.81 is affected by a vulnerability in the service processor mailbox interface. An attacker with authenticated service-level access to the FSP can send a specially crafted mailbox message to overflow host firmware runtime attribute storage, allowing arbitrary code to be executed in the host firmware runtime. This gives the attacker full access to the managed system's memory and hardware interfaces, resulting in a confidentiality, integrity, and availability impact to the managed system.

### CVE-2026-109426

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-312` |
| Published | 2026-10-12T21:17:11.310 |

Telegram-Stremio through 5.1.0 contains an insecure storage vulnerability that allows attackers with access to the MongoDB database, backups, or logs to recover the operator's authenticated Telegram session string, which is protected only by a keyless, reversible encoding transform rather than actual encryption. Attackers can round-trip the stored value through the repository's own decode_string function with no secret key to obtain a fully authenticated Telegram session, granting complete control of the operator's Telegram account even when two-step verification is enabled.

### CVE-2026-109424

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-12T20:17:09.143 |

NetEase Cloud Music client for Windows (cloudmusic.exe) versions 3.1.38 and 3.1.39.205426 contains a weak encryption vulnerability where /eapi/ and /xeapi/ API response bodies are decrypted using a fixed, publicly documented AES-128-ECB key with no integrity credential. Attackers who can intercept or originate server responses can construct valid ciphertext under the known key with PKCS#7 padding, enabling the client to accept forged API responses that serve as a prerequisite for further exploitation such as reaching the os.navigateExternal bridge.

### CVE-2026-109301

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-12T17:17:23.940 |

Parse Server before 8.6.95 and 9.0.0 before 9.10.2-alpha.3 does not resolve file references lacking a URL before passing objects to Cloud Code triggers and LiveQuery, causing an uncaught exception that terminates the process. Attackers able to write to a class with Cloud Code save, find, or delete triggers or LiveQuery enabled, including unauthenticated users when public write access or sign-up is allowed, can crash the server or break subsequent requests.

### CVE-2026-109257

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-12T17:17:17.280 |

FreeRDP before 3.32.0 contains a double-free vulnerability in nsc_context_initialize_encode() that leaves dangling plane pointers after a partial buffer growth failure. Attackers using a crafted RDP client can negotiate NSCodec with a large desktop geometry to trigger allocation failure, crashing the server during context teardown.

### CVE-2026-93907

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-13T14:17:45.277 |

IBM WebSphere Application Server 8.5, and 9.0 could allow a remote attacker to bypass authentication by exploiting a flaw in the CSIv2 inbound propagation handler.

### CVE-2026-65164

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T13:17:33.163 |

NVIDIA AIStore for Linux contains a path traversal vulnerability in the dSort archive extraction component where a remote attacker may cause an improper limitation of a pathname to a restricted directory by supplying crafted archive member names to a dSort job. A successful exploit may lead to arbitrary file creation or overwrite, code execution, information disclosure, data tampering, and denial of service.

### CVE-2026-65103

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T13:17:31.553 |

NVIDIA AIStore for Linux contains a path traversal vulnerability in the target-side object rename handler, where an unauthenticated remote attacker could cause an improper limitation of a pathname to a restricted directory by submitting a crafted rename destination directly to an AIStore target, resulting in the arbitrary creation or overwrite of a file. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, information disclosure, data tampering, and denial of service.

### CVE-2026-93892

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-12T23:17:45.797 |

IBM TRIRIGA Application Platform 5.0.0 through 5.0.8 could allow a remote authenticated attacker to obtain sensitive information due to exposure of session tokens in the HTML response.

### CVE-2026-85457

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-12T23:17:45.167 |

IBM Planning Analytics 2.0, and 2.1 could allow a remote authenticated attacker to execute arbitrary code due to a stack-based buffer overflow.

### CVE-2026-84360

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-12T21:17:22.960 |

Nginx UI is a web user interface for the Nginx web server. Prior to 2.4.1, the HTTP configuration mutation routes require RequireSecureSession, but /mcp and /mcp_message require only ordinary authentication before exposing nginx_config_add and nginx_config_modify. An OTP-enabled user with a normal JWT but no valid X-Secure-Session-ID can therefore create or modify Nginx configuration and trigger reload behavior through MCP, bypassing the intended step-up control. This issue is fixed in version 2.4.1.

### CVE-2026-59977

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-12T19:16:39.417 |

ConvertX is a self-hosted file conversion service. Prior to 0.18.0, the /delete/{id} endpoint uses HTTP GET for permanent deletion without CSRF protection. If an authenticated user visits attacker-controlled content that requests /delete/{id}, the browser sends the user session cookie and the request deletes the targeted job, resulting in unauthorized loss of converted-file history. This issue is fixed in version 0.18.0.

### CVE-2026-59976

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-10-12T19:16:39.260 |

ConvertX is a self-hosted file conversion service. Prior to 0.18.0, the ImageMagick converter uses the unsanitized convert_to parameter to construct an output path. If an authenticated user, or an unauthenticated user when ConvertX is configured to allow unauthenticated access, uploads an extensionless image and supplies directory traversal sequences in convert_to through /convert, the constructed path escapes the intended output directory, allowing the attacker to write converted output to arbitrary container paths, potentially overwriting files or causing denial of service. This issue is fixed in version 0.18.0.

### CVE-2026-108479

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-12T18:17:21.187 |

Cross-Site Request Forgery (CSRF) vulnerability in Patreon Patreon WordPress patreon-connect allows Cross Site Request Forgery.This issue affects Patreon WordPress: from n/a through 1.9.17.

### CVE-2026-85949

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-532` |
| Published | 2026-10-12T16:17:06.303 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 may record security-sensitive information in diagnostic logs under certain configurations. An attacker with access to the affected logs could use this information to obtain unauthorized access to protected resources.

### CVE-2026-95680

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-13T14:17:45.437 |

IBM WebSphere Application Server 8.5, and 9.0 could allow an authenticated attacker to bypass authorization leading to administrative impersonation across the cell.

### CVE-2026-85965

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-12T17:17:37.007 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 contain memory-safety defects in the JavaScript engine integration that could result in memory corruption, controlled process failure, or server instability.

### CVE-2026-65180

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-13T13:17:33.667 |

NVIDIA Megatron-LM contains a vulnerability in checkpoint loading where an Attacker may cause an RCE by convincing a user to load a maliciously crafted file. A successful exploit of this vulnerability may lead to code execution, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-65141

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-10-13T13:17:32.077 |

NVIDIA Isaac Lab contains a vulnerability where an attacker could cause an eval injection. A successful exploit of this vulnerability might lead to code execution, information disclosure, data tampering, and denial of service.

### CVE-2026-65110

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-13T13:17:31.820 |

NVIDIA Megatron-LM contains a vulnerability in checkpoint loading where, an attacker could cause an RCE by convincing a user to load a maliciously crafted file. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-75782

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-10-12T23:17:39.000 |

IBM Aspera Enterprise WebApps 1.0.0 through 1.0.6 could allow a local attacker to gain elevated privileges due to a misconfigured PATH environment variable.

### CVE-2026-95837

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-12T20:17:10.420 |

containerd is an open-source container runtime. From 2.1.0 until 2.2.7 and 2.3.4, containerd's CRI CreateContainer checkpoint restore is vulnerable because CRIU restores process security state from checkpoint data instead of enforcing the destination ContainerConfig. An attacker who can create a container from a crafted checkpoint can supply restored credentials, capabilities, no_new_privs, and seccomp state. The restored process can run as root with full capabilities and no enforced seccomp filters while CRI status reports the requested configuration. Systems that do not use CRI checkpoint restore are not affected. This issue is fixed in versions 2.2.7 and 2.3.4.

### CVE-2026-108094

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-12T15:17:07.080 |

A use-after-free flaw was found in mutter in the Wayland color-management ICC image-description path. A local attacker who can run a malicious Wayland client can destroy a wp_image_description_v1 resource while an asynchronous ICC file read is still in progress. When the read completes, the compositor uses the freed wl_resource, writes into freed memory, and frees a pointer derived from that memory. This can crash the GNOME session and may allow arbitrary code execution within the compositor process.

### CVE-2026-89201

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T10:17:21.650 |

A vulnerability has been identified in RUGGEDCOM CROSSBOW (All versions < V6.0). Affected devices do not properly validate or sanitize input in device group or facility names processed during the Bulk Export workflow. This could allow an authenticated attacker with specific privileges to execute arbitrary SQL commands on the underlying database.

### CVE-2026-78557

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T10:17:20.467 |

A vulnerability has been identified in Industrial Edge App Publisher (All versions < V1.27.9). The application fails to properly sanitize or escape data received from the backend before rendering it in the user interface. Because the front end is integrated with Node.js, this vulnerability allows for the execution of arbitrary JavaScript, which can be leveraged to achieve remote code execution (RCE) on the victim's machine

### CVE-2026-81839

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T02:16:59.927 |

GitLab has remediated an issue in GitLab EE affecting all versions from 18.1 before 19.2.8, 19.3 before 19.3.5, and 19.4 before 19.4.2 that, under certain conditions, could have allowed an authenticated user to execute arbitrary CI/CD pipelines in a transferred project with the new group's privileges due to improper cleanup of scheduled pipeline execution policy records.

### CVE-2026-18517

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-12T21:17:16.517 |

IBM Maximo Application Suite - Location Service for Esri Component 9.2, 9.1, and 9.0 IBM Maximo Application Suite — Location Service for Esri Component is vulnerable to unintended network egress due to a misconfigured Kubernetes NetworkPolicy.

### CVE-2026-109560

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-12T21:17:12.243 |

Continue CLI (@continuedev/cli) through 1.5.47 contains a permission bypass vulnerability that allows attackers to run unapproved commands by chaining them after allowed Bash prefix rules. Attackers can inject instructions into repository files or fetched pages so the agent appends commands after ;, && or | to execute code as the user.

### CVE-2026-18166

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-12T19:16:38.773 |

IBM Db2 11.5.0 through 11.5.9, and 12.1.0 through 12.1.5 for Linux, UNIX and Windows (includes DB2 Connect Server) could allow a remote authenticated attacker to obtain sensitive information due to improper authorization when using the CREATE WRAPPER command.

### CVE-2026-85966

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-12T17:17:37.137 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 do not sufficiently restrict access to certain security-sensitive information. A remote authenticated attacker with limited management permissions could obtain this information, which could result in unauthorized access to protected resources.

### CVE-2026-85964

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-12T17:17:36.877 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 allow an authenticated Query Console user to supply unsafe path values to a privileged filesystem helper, which could result in disclosure of arbitrary server files.

### CVE-2026-75888

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-12T17:17:35.723 |

A flaw was found in the OpenShift console. An authenticated console user can exploit a Server-Side Request Forgery (SSRF) vulnerability by providing a specially crafted Helm chart URL without proper validation. This allows the user to make the console pod fetch arbitrary URLs, potentially leading to the disclosure of sensitive information through error messages or enabling blind port scanning within the cluster.

### CVE-2026-109360

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-12T17:17:33.480 |

MONAI 0.4.0 before 1.6.1 contains a remote code execution vulnerability that allows on-path attackers to execute code by tampering with SENet pretrained weights fetched over plaintext HTTP. Attackers can substitute a crafted .pth file that load_state_dict_from_url unpickles without weights_only=True, executing code when SEResNet50 or other SENet models are constructed with pretrained=True.

### CVE-2026-78556

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-13T10:17:20.277 |

A vulnerability has been identified in Industrial Edge App Publisher (All versions < V1.27.9). The affected software does not properly validate the server certificate when initiating a TLS connection. This allows an attacker to intercept and relay communication (Man-in-the-Middle attack) and to spoof a trusted entity by interfering in the communication path between the client and the intended server.

### CVE-2026-109687

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T09:17:16.437 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Link Whisper INC Link Whisper Free link-whisper allows Blind SQL Injection.This issue affects Link Whisper Free: from n/a through 0.9.7.

### CVE-2026-108179

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T09:17:14.153 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in PluginUs.Net WOLF bulk-editor allows Blind SQL Injection.This issue affects WOLF: from n/a through 1.1.1.

### CVE-2026-93891

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-12T23:17:45.663 |

IBM TRIRIGA Application Platform 5.0.0 through 5.0.8 could allow a remote authenticated attacker to obtain sensitive information due to an XML external entity (XXE) injection flaw.

### CVE-2026-109292

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-12T17:17:22.500 |

Open WebUI from 0.6.27 before 0.11.4 contains an information disclosure vulnerability that allows destination servers to obtain user session cookies by receiving the full browser cookie jar on OAuth-mode connections. Operators of OpenAI-compatible connections, OpenAPI tool servers or terminal servers can capture forwarded session cookies from routine requests and replay them to hijack accounts, including administrators.

### CVE-2026-103499

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-13T14:17:18.873 |

IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.10 and IBM WebSphere Application Server 8.5, and 9.0 Liberty could allow a remote unauthenticated attacker to cause a denial of service due to uncontrolled resource consumption.

### CVE-2026-65161

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T13:17:32.710 |

NVIDIA AIStore for Linux contains a vulnerability in the Promote API where an unauthenticated remote attacker may read files accessible to the target process by supplying a crafted absolute source path. A successful exploit may lead to information disclosure.

### CVE-2026-109832

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-13T12:17:14.033 |

A flaw was found in gnome-remote-desktop as shipped in Red Hat Enterprise Linux. In the VNC TLS I/O handlers, retryable GnuTLS results (GNUTLS_E_AGAIN and GNUTLS_E_INTERRUPTED) are handled with an unbounded busy loop instead of yielding to the event loop. A remote attacker who can reach an enabled VNC TLS listener can cause the event-loop thread to spin at high CPU with no forward progress, resulting in denial of service.

### CVE-2026-58249

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-13T01:16:46.213 |

SAP NetWeaver and SAP Web Dispatcher do not properly validate certain fields in specially crafted requests handled by an internal protocol component. An unauthenticated attacker could send a malicious request that triggers a memory-handling error, causing the affected process to crash. Successful exploitation can therefore result in a high impact on the availability of the affected application. There is no impact on the confidentiality or integrity of the application.

### CVE-2026-75095

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-12T23:17:38.630 |

IBM Aspera Enterprise WebApps 1.0.0 through 1.0.6 could allow a remote attacker to cause a denial of service due to uncontrolled resource consumption.

### CVE-2026-75061

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-12T23:17:38.223 |

IBM Planning Analytics 2.0, and 2.1 could allow a remote attacker to traverse directories on the system. An attacker could send a specially crafted URL request containing "dot dot" sequences (/../) to write arbitrary files on the system.

### CVE-2026-92876

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-12T22:17:05.947 |

IBM Maximo Application Suite - IoT Component 9.2.0, 9.1.0, and 9.0.0 could allow a remote attacker to cause a denial of service due to uncontrolled recursion.

### CVE-2026-90921

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-130` |
| Published | 2026-10-12T22:17:05.813 |

IBM Maximo AI Service 9.1.0, and 9.2.0 could allow a remote attacker to cause a denial of service due to improper handling of malformed frames, resulting in termination of the host process.

### CVE-2026-90912

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-12T22:17:05.550 |

IBM Maximo AI Service 9.1.0, and 9.2.0 SaaS could allow a remote attacker to cause a denial of service due to uncontrolled recursion.

### CVE-2026-90911

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-12T22:17:05.417 |

IBM Maximo AI Service 9.1.0, and 9.2.0 could allow a remote attacker to cause a denial of service due to uncontrolled resource consumption.

### CVE-2026-78673

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-12T21:17:21.463 |

IBM Maximo AI Service 9.1.0, and 9.2.0 could allow a remote attacker to cause a denial of service due to improper input validation.

### CVE-2026-75881

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-12T21:17:21.337 |

IBM Maximo Application Suite - IoT Component 9.2.0, 9.1.0, and 9.0.0 could allow a remote attacker to cause a denial of service due to an infinite parsing loop when processing certain inputs.

### CVE-2026-105052

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-12T21:17:08.300 |

IBM Maximo Application Suite 8.10, 8.11, 9.0, 9.1, and 9.2 could allow a remote attacker to traverse directories on the system. An attacker could send a specially crafted URL request containing "dot dot" sequences (/../) to view arbitrary files on the system.

### CVE-2026-85975

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-319` |
| Published | 2026-10-12T17:17:38.250 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 may use cleartext transport for Amazon S3 connections by default. A network-positioned attacker could intercept data or credentials transmitted through an affected connection.

### CVE-2026-85963

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-321;CWE-918` |
| Published | 2026-10-12T17:17:36.753 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 include deprecated OpsDirector functionality with weaknesses that could allow an unauthenticated remote attacker to make unauthorized requests to internal services or forge trusted requests, potentially resulting in unauthorized access to protected information.

### CVE-2026-85962

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-347` |
| Published | 2026-10-12T17:17:36.627 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 contain an improper authentication vulnerability in SAML processing. In deployments that use SAML authentication, an unauthenticated remote attacker could cause the affected server to accept an assertion that should be rejected, potentially resulting in unauthorized access.

### CVE-2026-85961

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-532` |
| Published | 2026-10-12T17:17:36.500 |

On Azure deployments, Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 may record security-sensitive authentication information in diagnostic logs under certain configurations. An attacker with access to the affected logs could use this information to obtain unauthorized access to protected cloud resources.

### CVE-2026-85960

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-12T17:17:36.373 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 use predictable CSRF tokens in Query Console. A remote attacker who lures an authenticated Query Console user to a malicious page could submit unauthorized requests and execute server-side code with the victim's permissions.

### CVE-2026-85959

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-778` |
| Published | 2026-10-12T17:17:36.247 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 do not consistently record successful authentication events in audit logs, which could limit customers' ability to detect and investigate unauthorized access or credential misuse.

### CVE-2026-85958

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-12T17:17:36.120 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 contain an authentication validation weakness that could allow an attacker to use a token that should not be accepted by the affected server, which could result in unauthorized access.

### CVE-2026-85957

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-12T17:17:35.990 |

Affected Progress MarkLogic Server 11.x releases before 11.3.7 use a SAML parser configuration that can process external DTDs or entities, which could result in unintended network access or information disclosure.

### CVE-2026-109331

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-10-12T17:17:28.843 |

Network-AI from 5.14.0 before 5.15.2 contains a security control bypass vulnerability in the ClaudeHookBridge PreToolUse hook, which matches deny patterns only against the first present candidate field. A prompt-injected agent can place dangerous payloads in fields like Write content or an MCP script parameter beside a benign file_path or command, evading denyPatterns to write web shells or execute scripts.

### CVE-2026-96612

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-12T16:17:07.637 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in hexpm hex allows a malicious package publisher to delete a directory outside the project's deps directory and extract package files into it when a developer fetches dependencies.

A package release's requirements carry an app label that names the dependency's OTP application. Hex takes this label from the repository's signed registry and uses it as the dependency's application name without validating it (Hex.RemoteConverger.deps/2, Hex.Mix.to_lock/1). Mix derives the dependency's checkout directory as deps/<app>, and Hex.SCM.update/1 runs File.rm_rf!/1 on that directory and unpacks the package into it. hex.pm only checks the label's length, so a publisher can set it to a value such as ../../target. When a project depends on such a release directly or transitively, mix deps.get or mix deps.update deletes the directory the label resolves to and writes the labelled package's files there. This happens before any dependency code is compiled.

This issue affects hex: from 0.6.0 before 2.5.2.

### CVE-2026-103060

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-12T16:17:00.873 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in erlang rebar3 allows a malicious package publisher to delete a directory outside the project's _build directory and extract package files into it when a developer fetches dependencies.

A package release's dependencies in a Hex registry carry an app field that names the dependency's OTP application. rebar3 uses this field as the dependency's name without validating it (rebar_packages:parse_deps/1) and builds the dependency's directory from that name (rebar_app_utils:dep_to_app/7). rebar_fetch:download_source_online/2 deletes that directory with rm -rf and moves the fetched package into it. hex.pm didn't restrict the field to a directory name before 2026-10-12, so a publisher could set it to a value such as ../../../../target. When a project depends on such a release directly or transitively, rebar3 get-deps deletes the directory the name resolves to and writes the dependency's files there. This happens before the dependency's own rebar.config.script is evaluated, and get-deps compiles nothing.

This issue affects rebar3: from 3.7.0-rc1 before 3.27.2.

### CVE-2026-84418

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-12T23:17:45.013 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 can allow a man-in-the-middle attacker to present a forged TLS certificate, intercept the connection, and capture the IAM bearer Authorization header automatically attached by the session adapter. The captured token grants full platform-scope tenant API access, enabling the attacker to read and manipulate the victim's DataStage projects, flows, assets, and pipeline definitions. This is client-side SDK code running on the user's own machine, so exploitation requires an external network interceptor rather than a co-tenant in the shared cluster.

### CVE-2026-83535

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-208` |
| Published | 2026-10-12T19:16:39.850 |

A flaw was found in openstack-network-exporter. When an operator configures user authentication but omits or misconfigures Transport Layer Security (TLS), the basic authentication mechanism is silently bypassed. This fail-open design allows an adjacent network attacker to access sensitive Open vSwitch (OVS) and Open Virtual Network (OVN) dataplane metrics without credentials. Consequently, an attacker can enumerate bridge names, port counters, OVN controller state, and host topology, leading to information disclosure.

### CVE-2026-108481

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-12T18:17:21.327 |

Cross-Site Request Forgery (CSRF) vulnerability in Patreon Patreon WordPress patreon-connect allows Cross Site Request Forgery.This issue affects Patreon WordPress: from n/a through 1.10.0.

### CVE-2026-85974

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-297` |
| Published | 2026-10-12T17:17:38.123 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 do not consistently validate TLS certificate hostnames for certain outbound connections. A network-positioned attacker could exploit this weakness to intercept or modify communications with an affected service.

### CVE-2026-85973

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-319` |
| Published | 2026-10-12T17:17:38.000 |

Progress MarkLogic Server 12.x releases before 12.1.0 may use cleartext transport for certain cluster-management communications. A network-positioned attacker could intercept or modify information transmitted through an affected connection.

### CVE-2026-85972

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-303` |
| Published | 2026-10-12T17:17:37.870 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 do not sufficiently verify the identity of a Kerberos authentication service in certain password-based authentication configurations. A network-positioned attacker could impersonate trusted authentication infrastructure, potentially resulting in unauthorized access or modification of protected data.

### CVE-2026-109245

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-12T17:17:15.480 |

FreeRDP 3.0.0 before 3.32.0 contains an improper certificate validation vulnerability in freerdp_http_request() in libfreerdp/utils/http.c that completes TLS handshakes without verifying the server certificate chain. On-path attackers can impersonate login.microsoftonline.com in the Azure AD authentication flow to capture OAuth authorization codes and substitute the OpenID discovery document.

### CVE-2026-65150

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T13:17:32.587 |

NVIDIA DALI contains a vulnerability where an attacker could cause an uncontrolled out-of-bounds read. A successful exploit of this vulnerability mighty lead to information disclosure, data tampering, and denial of service.

### CVE-2026-65149

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T13:17:32.460 |

NVIDIA DALI contains a vulnerability where an attacker could cause an uncontrolled out-of-bounds write. A successful exploit of this vulnerability might lead to denial of service, information disclosure, and data tampering.

### CVE-2026-65148

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T13:17:32.333 |

NVIDIA DALI contains a vulnerability where an attacker could cause a stack-based buffer overflow. A successful exploit of this vulnerability might lead to code execution, information disclosure, data tampering, and denial of service.

### CVE-2026-65147

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T13:17:32.207 |

NVIDIA DALI contains a vulnerability where an attacker could cause an uncontrolled out-of-bounds read. A successful exploit of this vulnerability might lead to information disclosure and denial of service.

### CVE-2026-96893

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-10-13T02:17:00.720 |

GitLab has remediated an issue in GitLab EE affecting all versions from 19.1 before 19.2.8, 19.3 before 19.3.5, and 19.4 before 19.4.2 that, under certain conditions, could have allowed an authenticated user to inject specially crafted content into AI agent instructions, potentially causing unintended command execution attributed to other users, due to improper neutralization of special elements in AI conversation context construction.

### CVE-2026-96261

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-12T21:17:23.620 |

IBM Power Systems Firmware FW1060.00 through FW1060.81 is affected by a vulnerability in host firmware configuration parsing. An attacker with authenticated service-level access to the service processor can write specially crafted configuration data, causing the host firmware boot stack to crash with possible memory corruption during system initialisation, resulting in an integrity and availability impact to the managed system.

### CVE-2026-109556

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-749` |
| Published | 2026-10-12T21:17:11.617 |

EdgeEver Desktop 1.92.0 through 1.112.0 contains a remote code execution vulnerability in the desktop:acp-probe IPC handler, which lacks a sender check and spawns a caller-supplied input.path executable. Attackers with script execution in a renderer, such as via template-preview or drag-preview stored cross-site scripting, can call probeAcpAdapter to launch local executables with the user's privileges.

### CVE-2026-108906

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-125` |
| Published | 2026-10-12T16:17:03.917 |

A vulnerability has been found in Netcore NR268 1.7.121109. This affects the function filter_arp_put_file_cgi of the file /router/filter_arp_put_file.cgi. The manipulation of the argument put_file leads to out-of-bounds read. It is possible to initiate the attack remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-102562

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T08:16:59.263 |

The AcyMailing plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the customField[] parameter of the public frontusers::subscribe endpoint in versions up to, and including, 11.1.0. This is due to insufficient input sanitization and output escaping in the acym_cleanVar() sanitizer, whose HTML-tag stripper only matches complete tags (requiring a closing '>'), together with SubscriberInsertion::replaceUserInformation() and the archive view template, which substitute the stored subscriber field value into the mail body and emit it without HTML encoding. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses the online-archive URL for the poisoned subscriber, including administrators who click the plugin-generated link in the Subscribers → History screen.

### CVE-2026-102007

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T08:16:57.567 |

The Bit integrations – Form Integration, Webhook, Spreadsheets, CRM, LMS & Email Automation plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'field mapped to notification_content (attacker-chosen key, e.g. payload_text)' parameter in all versions up to, and including, 2.10.6 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires a site administrator to have preconfigured a Bit Integrations flow that binds the public Bit Assist webhook to a BuddyBoss "Send Notification" action with a form field mapped to notification_content, and the attacker to know the flow's UUID callback URL.

### CVE-2026-109640

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:29.560 |

Frappe ERPNext before 16.22.0 contains a missing authorization vulnerability that allows authenticated users to modify records by invoking endpoints lacking proper authorization checks. Attackers can call these endpoints to perform operations on records beyond their permitted role, resulting in unauthorized modification of data.

### CVE-2026-109572

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:22.407 |

Open WebUI from 0.8.6 before 0.11.4 contains a privilege escalation vulnerability in the terminal proxy that allows authenticated users to reach the Terminals administrator API with the shared key attached. Attackers can send requests through /api/v1/terminals/{server_id}/{path} to list or stop other users' terminals and modify terminal policies, injecting environment variables into other users' terminals.

### CVE-2026-18513

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-12T21:17:16.380 |

IBM Maximo Application Suite - Location Service for Esri Component 9.2, 9.1, and 9.0 is vulnerable to improper access control due to a schema-less Custom Resource Definition.

### CVE-2026-41510

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:L/A:L` |
| Weaknesses | `CWE-693;CWE-770` |
| Published | 2026-10-12T20:17:09.793 |

OWASP Coraza WAF is a golang modsecurity compatible web application firewall library. From 3.0.0 until 3.8.1, Coraza silently drops arguments after SecArgumentsLimit in internal/corazawaf/transaction.go, while internal/bodyprocessors/urlencoded.go writes ARGS_POST without enforcing the cap. The flaw is triggered when an unauthenticated attacker sends more arguments than SecArgumentsLimit or supplies bodies that expand beyond the configured argument and flattening budgets. An unauthenticated attacker can flood requests with arguments so excess values are silently omitted from ARGS, ARGS_GET, ARGS_NAMES, ARGS_GET_NAMES, ARGS_POST, or ARGS_PATH before security rules inspect them; affected urlencoded and JSON processing can also consume excessive memory. The omission can bypass WAF rules protecting the downstream application, and unbounded or amplified argument processing can cause memory consumption and service degradation. This issue is fixed in version 3.8.1.

### CVE-2026-108361

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-12T20:17:07.900 |

Privasys Remote Attestation TLS Clients provides multi-language utilities for verifying attested TLS connections. Before 0.9.1, an attacker with local access could modify workload code, data, and configuration at any time after successful connection establishment. Once Evidence was successfully appraised and the connection was established, there was a window of vulnerability from the establishment of the connection to the termination of the connection where an attacker could modify the state of the workload and platform at runtime on the TLS endpoint acting as the Attester. This vulnerability was possible because Privasys/ra-tls-clients performed attestation only once in the lifetime of the connection (at connection establishment time), and the verifying peer continued to believe that the state was the same as in the initial Evidence throughout, whereas it could be stale at some point in time. This vulnerability is fixed in 0.9.1.

### CVE-2026-109288

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-12T17:17:21.913 |

Open WebUI before 0.11.4 contains a stored cross-site scripting vulnerability in MarkdownInlineTokens.svelte, which renders markdown link URLs into anchor hrefs without validating their scheme. Authenticated users can embed javascript: links in shared chats that, when clicked by a victim, steal the victim's JWT from local storage, including admins' tokens.

### CVE-2026-103522

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-12T15:17:05.690 |

In Thelia v2.6.0, the store banner upload feature performs insufficient filetype validation that relies exclusively on client‑supplied MIME types. An attacker with administrative access can upload a PHP file disguised as an image to bypass validation and achieve remote code execution on the underlying server.

### CVE-2026-103521

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-12T15:17:05.503 |

In Thelia v2.6.0, the document upload endpoint properly blocks the upload of executable file types, but the document update endpoint does not perform the same validation. An attacker with administrative Thelia permissions can exploit this vulnerability to upload arbitrary executable files, such as malicious PHP scripts, to achieve remote code execution on the underlying server.

### CVE-2026-74047

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-13T14:17:41.317 |

Wazuh from 4.0.0 before 4.14.8 contains an information disclosure vulnerability that allows low-privileged users with agent:read to retrieve the plaintext authd.pass enrollment password via the unmasked agent configuration endpoint. Attackers holding the default readonly role can request the auth component configuration for pseudo-agent ID 000 to obtain the secret and enroll rogue agents against the manager.

### CVE-2026-74045

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T14:17:41.160 |

Wazuh from 3.12.0 before 4.14.8 contains a heap buffer overflow in fim_generate_alert() where full_log is sized from input but written bounded by OS_MAXSTR. An enrolled agent can send a crafted FIM syscheck event to corrupt manager heap memory and deterministically crash wazuh-analysisd, causing a fleet-wide detection outage.

### CVE-2026-109949

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-10-13T14:17:33.410 |

FreeRDP 3.0.0 before 3.32.0 contains an improper restriction of excessive authentication attempts in its virtual smartcard GIDS implementation, which stores the PIN retry counter per-handle. A malicious RDP server can exhaust the counter with VERIFY APDUs, then request a new SCardConnect to reset attempts, enabling unbounded online brute-forcing of the configured smartcard PIN.

### CVE-2026-109947

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-13T14:17:32.993 |

FreeRDP from 3.20.1 before 3.32.0 contains an uncontrolled resource allocation vulnerability that allows malicious RDP servers to exhaust client memory via oversized drive redirection read requests. Attackers can send IRP_MJ_READ with Length 0xffffffff, causing roughly 4 GiB of zeroed allocation on 64-bit builds or an under-reserved buffer on 32-bit builds.

### CVE-2026-109946

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-13T14:17:32.820 |

FreeRDP 3.11.0 before 3.32.0 does not validate that AVC444 and AVC444v2 region widths are even before YUV444 conversion, so an odd width reaches an assertion and aborts the client. A malicious or compromised RDP server can terminate a connected FreeRDP client after RDPGFX AVC444 negotiation by sending an in-bounds region rectangle with an odd width.

### CVE-2026-109944

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-13T14:17:32.523 |

FreeRDP 3.0.0 before 3.32.0 does not remove card handles when Emulate_SCardReleaseContext releases a smartcard-emulation context, so Emulate_SCardTransmit later looks up the deleted parent context and reaches a terminating WINPR_ASSERT. A malicious RDP server can crash a connecting client with smartcard emulation and redirection enabled by releasing a context, establishing another, and issuing SCardTransmit with the stale card handle.

### CVE-2026-109943

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T14:17:32.377 |

FreeRDP 3.29.0 before 3.32.0 contains a double free in the client's async-update message proxy, which shallow-copies the parser-owned PolygonSC or PolygonCB points array when numPoints is zero, so both the queue consumer and parser cleanup free it. A malicious RDP server can send a point-bearing polygon order followed by a zero-point order to crash a client with +async-update enabled.

### CVE-2026-109942

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-13T14:17:32.220 |

FreeRDP 2.3.0 before 3.32.0 dereferences a NULL stream in rdg_process_close_packet in libfreerdp/core/gateway/rdg.c because rdg_process_control_packet accepts a header-only PKT_TYPE_CLOSE_CHANNEL packet and passes the null payload without a check. A malicious or compromised RD Gateway can send an eight-byte CLOSE_CHANNEL header to crash a connecting FreeRDP client.

### CVE-2026-109941

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-13T14:17:32.073 |

FreeRDP from 2.3.0 before 3.32.0 contains an infinite loop vulnerability in http_chuncked_read that allows malicious RD Gateways to hang clients by sending incomplete chunked responses. Attackers can send a partial chunk-size line or footer followed by a clean TLS shutdown, causing zero-byte reads to loop forever and freeze the client decoder thread.

### CVE-2026-109939

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-13T14:17:31.767 |

FreeRDP 3.27.1 before 3.32.0 contains a NULL pointer dereference in update_read_cache_bitmap_v3_order() in libfreerdp/core/orders.c, which accesses the client bitmap cache when the CBR3_DO_NOT_CACHE flag is set, even though the cache is not yet initialized before Demand Active. A malicious or compromised RDP server can send a Cache Bitmap V3 order during connection setup to crash a connecting client that has enabled the non-default Bitmap Cache V3 feature (/cache:codec:<rfx|nsc|jpeg>).

### CVE-2026-109938

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T14:17:31.617 |

Positive mapped-video coordinates overflow and abort FreeRDP clients A malicious or compromised RDP server can terminate a FreeRDP client after the user connects with video redirection enabled.

### CVE-2026-109678

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-13T14:17:31.053 |

FreeRDP 3.0.0-beta1 before 3.32.0, when built with verbose WinPR assertions and using smartcard emulation, has a reachable assertion: the emulated SCardStatusA passes a NULL reader-name destination to scard_copy_strings. A malicious RDP server can send an SCardStatusA request with fmszReaderNamesIsNULL=1 to abort a connecting client.

### CVE-2026-109677

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T14:17:30.897 |

FreeRDP from 2.0.0-beta1 before 3.28.0 contains an out-of-bounds read vulnerability in smartcard_LocateCardsByATRA_Call because the ATR pattern cbAtr byte count is not capped. Malicious RDP servers can send crafted ATR mask arrays to use query timing as an oracle, leaking heap memory bit-by-bit to defeat ASLR and aid RCE exploits.

### CVE-2025-58773

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T14:17:18.460 |

AMI APTIOV contains vulnerabilities in BIOS where users may cause  "Out-of-bounds Write” by local access. Successful exploitation of this vulnerability could lead to buffer overflows, memory corruption, and arbitrary code execution, and also impact Confidentiality, Integrity, and Availability.

### CVE-2025-58771

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T14:17:18.140 |

AMI APTIOV contains vulnerabilities in BIOS
where users may cause “Integer Overflow or Wraparound” by local access. Successful exploitation of this vulnerability could
lead to buffer overflows, memory corruption, and arbitrary code execution, and
also impact Confidentiality, Integrity, and Availability.

### CVE-2026-65104

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-328` |
| Published | 2026-10-13T13:17:31.683 |

NVIDIA Megatron-LM for all platforms contains a vulnerability in inference, where an attacker could cause hash collisions in the cache used for inference requests. A successful exploit of this vulnerability might lead to data tampering and partial information disclosure.

### CVE-2026-89202

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-13T10:17:21.790 |

A vulnerability has been identified in RUGGEDCOM CROSSBOW (All versions < V6.0). Affected devices do not properly perform authorization checks for device disconnection requests. This could allow an authenticated attacker with minimal privileges to disconnect active sessions of other users, including administrators, leading to a denial of service.

### CVE-2026-103316

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-10-13T07:16:30.490 |

The macOS version of the DigiD app is not signed with Hardened Runtime. As a result, a local process can load its own dylib into DigiD via DYLD_INSERT_LIBRARIES.  An attacker with local user-level code execution can execute arbitrary code within the macOS version of the DigiD app, thereby gaining access to DigiD data and cryptographic capabilities that the process normally does not have. Reported by Kun Peeks (@SwayZGl1tZyyy)

### CVE-2026-89120

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-1188` |
| Published | 2026-10-13T01:16:48.813 |

A regression caused by an API change in SAP ABAP Platform reintroduces a previously fixed authorization weakness. The session manager can be opened in single transaction mode, including from FLP. A low-privileged attacker could exploit this to bypass restrictions via specially crafted requests, resulting in high impact on integrity and low impact on confidentiality. There is no impact on availability.

### CVE-2026-17475

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-10-12T23:17:36.443 |

IBM Planning Analytics 2.0, and 2.1 could allow a remote authenticated attacker to delete folders and applications belonging to other users due to improper functional level access control.

### CVE-2026-109674

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T23:17:35.380 |

Frappe ERPNext before 15.98.0 and 16.x before 16.6.0 contains an SQL injection vulnerability in some endpoints caused by missing input validation. Remote authenticated attackers can send specially crafted requests to the affected endpoints to manipulate database queries and extract sensitive information from the database.

### CVE-2026-109672

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:35.040 |

Frappe ERPNext before 15.118.0 and 16.x before 16.27.0 contains a missing authorization vulnerability in certain endpoints that fail to enforce proper authorization checks. Authenticated users can query these endpoints to read financial data beyond what their assigned role permits.

### CVE-2026-109666

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:34.043 |

Frappe ERPNext before 15.110.0 and 16.x before 16.21.0 contains a missing authorization vulnerability in certain endpoints that fail to enforce proper permission checks on inventory records. Authenticated users can send requests to these endpoints to modify inventory data beyond what their assigned role permits.

### CVE-2026-109663

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T23:17:33.550 |

Frappe ERPNext before 15.113.0 and 16.x before 16.22.0 contains an SQL injection vulnerability caused by missing input validation in some endpoints. Authenticated remote attackers can send specially crafted requests to these endpoints to manipulate database queries and extract sensitive information from the database.

### CVE-2026-109661

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:33.213 |

Frappe ERPNext before 15.116.0 and 16.x before 16.27.0 contains a missing authorization vulnerability in certain endpoints that fail to enforce proper authorization checks, exposing financial data. Authenticated attackers with low-privileged accounts can query these endpoints to read financial data beyond their permitted role.

### CVE-2026-109660

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:33.047 |

Frappe ERPNext before 15.112.0 and 16.x before 16.23.0 has certain endpoints that do not enforce proper authorization checks on operations that modify production records. An authenticated low-privileged user can send requests to these endpoints to modify production data beyond what their assigned role permits.

### CVE-2026-109659

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:32.877 |

Frappe ERPNext before 15.113.0 and 16.x before 16.24.0 contains a missing authorization vulnerability in which certain endpoints fail to enforce proper permission checks. Authenticated users can call these endpoints to read financial data beyond what their assigned role permits.

### CVE-2026-109658

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:32.710 |

Frappe ERPNext before 15.115.0 and 16.x before 16.26.0 contains a missing authorization vulnerability in which certain endpoints fail to enforce proper authorization checks. Authenticated users can call these endpoints to read data, including personal data, beyond what their assigned role permits.

### CVE-2026-109656

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:32.387 |

Frappe ERPNext before 15.118.2 and 16.x before 16.30.0 contains a missing authorization vulnerability in which certain endpoints fail to enforce proper authorization checks on item master data. Authenticated attackers with low-privileged accounts can call these endpoints to read item master data beyond their permitted role.

### CVE-2026-109655

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:32.220 |

Frappe ERPNext before 15.115.0 and 16.x before 16.26.0 contains a missing authorization vulnerability in certain endpoints that fail to enforce proper role-based authorization checks. Authenticated low-privileged users can send requests to these endpoints to modify inventory records beyond their permitted role.

### CVE-2026-109650

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:31.390 |

Frappe ERPNext before 15.112.0 and 16.x before 16.23.0 contains a missing authorization vulnerability in certain endpoints that fail to enforce proper authorization checks. Authenticated low-privileged users can send requests to these endpoints to read personal data beyond what their assigned role permits.

### CVE-2026-109649

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T23:17:31.213 |

Frappe ERPNext before 15.102.0 and 16.x before 16.11.0 contains an SQL injection vulnerability in some endpoints due to missing input validation, allowing manipulation of database queries. Authenticated attackers can send specially crafted requests to the affected endpoints to extract sensitive information from the database.

### CVE-2026-109648

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T23:17:31.050 |

Frappe ERPNext before 15.106.0 and 16.x before 16.16.0 contains an SQL injection vulnerability in some endpoints due to missing input validation. Authenticated attackers can send specially crafted requests to inject SQL into database queries and extract sensitive information from the underlying database.

### CVE-2026-109647

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T23:17:30.823 |

Frappe ERPNext before 15.106.0 and 16.x before 16.16.0 contains an SQL injection vulnerability in multiple endpoints caused by missing input validation. Authenticated attackers can send specially crafted requests to these endpoints to manipulate database queries and extract sensitive information from the ERPNext database.

### CVE-2026-109646

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T23:17:30.580 |

Frappe ERPNext before 15.106.0 and 16.x before 16.16.0 contains an SQL injection vulnerability in some endpoints due to missing input validation. Authenticated low-privileged attackers can send specially crafted requests to these endpoints to inject SQL and extract sensitive information from the database.

### CVE-2026-109645

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:30.397 |

Frappe ERPNext before 15.119.0 and 16.x before 16.31.0 contains a missing authorization vulnerability in certain endpoints that fail to enforce proper permission checks. Authenticated attackers can send requests to these endpoints to create records and modify data beyond their permitted role, bypassing intended role-based access restrictions.

### CVE-2026-109644

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:30.220 |

Frappe ERPNext before 15.119.0 and 16.x before 16.31.0 contains a missing authorization vulnerability in certain endpoints that fail to enforce proper authorization checks on valuation data. Authenticated low-privileged users can query these endpoints to read valuation information beyond what their assigned role permits.

### CVE-2026-109643

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:30.057 |

Frappe ERPNext before 15.111.0 and 16.x before 16.22.0 contains a missing authorization vulnerability in certain project-related endpoints that fail to enforce permission checks. Authenticated low-privileged users can call these endpoints directly to read project data beyond what their assigned role permits.

### CVE-2026-109639

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T23:17:29.390 |

Frappe ERPNext before 15.102.0 and 16.x before 16.8.0 contains an SQL injection vulnerability in some endpoints due to missing input validation, allowing manipulation of database queries. Authenticated attackers with low privileges can send specially crafted requests to the affected endpoints to extract sensitive information from the database.

### CVE-2026-109638

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T23:17:29.223 |

Frappe ERPNext before 15.110.0 and 16.x before 16.21.0 contains a SQL injection vulnerability in some endpoints caused by missing input validation. Authenticated attackers can send specially crafted requests to these endpoints to manipulate database queries and extract sensitive information from the database.

### CVE-2026-109637

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:29.060 |

Frappe ERPNext before 16.14.0 contains a missing authorization vulnerability that allows authenticated users to modify master data beyond their permitted role. Attackers can send requests to certain endpoints lacking proper authorization checks to make unauthorized changes to master data records.

### CVE-2026-109636

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:28.900 |

Frappe ERPNext before 15.115.0 and 16.x before 16.26.0 contains a missing authorization vulnerability because certain endpoints fail to enforce proper permission checks. Authenticated attackers with low-privileged accounts can call these endpoints to read financial data beyond their permitted role.

### CVE-2026-109632

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:28.040 |

Frappe ERPNext before 15.121.0 and 16.x before 16.33.0 contains a missing authorization vulnerability in which certain endpoints fail to enforce proper authorization checks. Authenticated users can call these endpoints directly to read data beyond what their assigned role permits.

### CVE-2026-109631

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T23:17:27.870 |

Frappe ERPNext before 15.119.1 and 16.x before 16.32.0 contains an SQL injection vulnerability in some endpoints that lack input validation, allowing crafted input to alter database queries. Authenticated attackers with low privileges can send specially crafted requests to these endpoints to extract sensitive information from the database.

### CVE-2026-109628

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:27.360 |

Frappe ERPNext before 15.121.0 and 16.x before 16.34.0 contains a missing authorization vulnerability in certain endpoints that fail to enforce proper role checks when modifying record status. Authenticated low-privileged attackers can invoke these endpoints to alter data beyond their permitted role, compromising data integrity.

### CVE-2026-109627

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:27.187 |

Frappe ERPNext before 15.120.0 and 16.x before 16.33.0 contains a missing authorization vulnerability in which certain endpoints fail to enforce proper permission checks. Authenticated low-privileged users can request these endpoints directly to read financial data beyond what their assigned role permits.

### CVE-2026-109626

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T23:17:27.023 |

Frappe ERPNext before 16.34.2 contains an SQL injection vulnerability caused by missing input validation in multiple endpoints. Authenticated attackers with low privileges can send specially crafted requests to these endpoints to inject SQL and extract sensitive information from the database.

### CVE-2026-109625

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:26.860 |

Frappe ERPNext before 15.121.3 and 16.x before 16.35.0 contains a missing authorization vulnerability in certain endpoints that fail to enforce role-based authorization checks. Authenticated users can request these endpoints to read financial data beyond the permissions granted by their assigned role.

### CVE-2026-109624

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:26.697 |

Frappe ERPNext before 15.120.0 and 16.x before 16.33.0 contains a missing authorization vulnerability in certain endpoints that fail to enforce proper permission checks. Authenticated low-privileged users can request these endpoints to read personal data beyond what their assigned role permits.

### CVE-2026-109621

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:26.190 |

Frappe ERPNext before 15.120.0 and 16.x before 16.23.0 contains an authorization bypass in an endpoint that honours a caller-supplied flag disabling its own permission enforcement. Authenticated attackers can set this flag when calling the endpoint to skip permission checks and read party records beyond their permitted role.

### CVE-2026-109617

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:26.023 |

Frappe ERPNext before 15.121.0 and 16.x before 16.34.0 contains a missing authorization vulnerability in certain endpoints that fail to enforce proper authorization checks during document creation. Authenticated low-privileged users can send requests to these endpoints to create documents against records beyond their permitted role, bypassing role-based permission restrictions.

### CVE-2026-109616

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:25.857 |

Frappe ERPNext before 15.121.3 and 16.x before 16.35.0 contains a missing authorization vulnerability in which certain endpoints fail to enforce proper authorization checks. Authenticated users can send requests to these endpoints to modify data beyond what their assigned role permits.

### CVE-2026-109615

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:25.687 |

Frappe ERPNext before 15.121.0 and 16.x before 16.34.0 contains a missing authorization vulnerability in certain endpoints that fail to enforce proper permission checks during document creation. Authenticated low-privileged users can call these endpoints to create documents against records beyond their permitted role, bypassing role-based access controls.

### CVE-2026-109614

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:25.527 |

Frappe ERPNext before 16.34.0 contains a missing authorization vulnerability that allows authenticated users to read financial data beyond their permitted role. Attackers can query endpoints lacking proper authorization checks to access sensitive financial records they should not be able to view.

### CVE-2026-109613

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:25.353 |

Frappe ERPNext before 15.121.0 and 16.x before 16.34.0 contains a missing authorization vulnerability in which certain endpoints fail to enforce proper authorization checks on document status modification. Authenticated low-privileged users can call these endpoints to modify data beyond their permitted role, bypassing intended role-based access restrictions.

### CVE-2026-109610

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T23:17:24.830 |

Frappe ERPNext before 15.119.1 and 16.x before 16.32.0 contains a missing authorization vulnerability because certain endpoints fail to enforce proper permission checks. Authenticated low-privileged users can call these endpoints to modify documents and data beyond what their assigned role permits.

### CVE-2026-109609

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T23:17:24.660 |

Frappe ERPNext before 15.119.1 and 16.x before 16.32.0 contains an SQL injection vulnerability in some endpoints that lack input validation. Authenticated attackers with low privileges can send specially crafted requests to these endpoints to inject SQL and extract sensitive information from the ERPNext database.

### CVE-2026-109601

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-10-12T23:17:23.823 |

Frappe Framework before 15.117.0 and 16.x before 16.30.0 contains an arbitrary file read vulnerability in the handling of attributes in outgoing email HTML. Attackers who can supply outgoing email content can set an attribute value referencing a local file path to expose sensitive server files.

### CVE-2023-54412

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-12T23:17:17.953 |

Frappe before 13.46.3 and 14.x before 14.21.1 contains an improper access control vulnerability in Email Template permissions that allows any authenticated non-guest user to create and edit any Email Template. Attackers with low-privileged accounts, including self-registered users when signup is enabled, can modify Email Templates used by the application.

### CVE-2026-84312

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-287;CWE-352` |
| Published | 2026-10-12T22:17:05.263 |

Nginx UI is a web user interface for the Nginx web server. Prior to 2.4.1, GetCasdoorUri uses the configured Casdoor application name as a constant OAuth state value and CasdoorCallback does not compare the submitted state with a value bound to the initiating browser session. An unauthenticated attacker can cause a victim's browser to complete an attacker-controlled Casdoor authorization flow, and the callback can mint a Nginx UI session for the identity returned by that authorization code. This issue is fixed in version 2.4.1.

### CVE-2026-109568

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-12T21:17:13.500 |

Shaark 1.2.13 through 1.2.44 contains a missing authorization vulnerability in the Link, Story, Chest and Album API controllers that skips ownership checks. Authenticated non-admin users can send PUT or DELETE requests to /api/{link,story,chest,album}/{id} with numeric IDs to overwrite or delete other users' content, including private items.

### CVE-2026-109427

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-10-12T21:17:11.460 |

Telegram-Stremio through 5.1.0 contains a broken object-level authorization vulnerability that allows authenticated token holders to access arbitrary chat messages by forging unsigned, unauthenticated stream IDs decoded via encode_string/decode_string functions. Attackers can craft or enumerate sequential msg_id values and set a global flag in the stream_handler endpoint to route requests through the operator's personal Userbot account, exposing private channels, groups, and Saved Messages, while the unauthenticated thumb_handler endpoint further discloses thumbnails from those same chats without any token validation.

### CVE-2026-85971

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-12T17:17:37.750 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 assign overly permissive operating-system permissions to certain log files, which could allow a local user to read or alter log data. The corrected default permissions apply to newly created and rotated logs; existing logs retain their current permissions until remediated.

### CVE-2026-85970

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-12T17:17:37.627 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 enable XML external entity processing by default in multiple server paths, which could allow crafted XML to cause server-side requests or disclosure of local files.

### CVE-2026-85969

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-12T17:17:37.500 |

Progress MarkLogic Server 12.x releases before 12.1.0 and 11.x releases before 11.3.7 contain an out-of-bounds write vulnerability in certain language-processing functionality. A remote authenticated attacker could exploit this vulnerability to cause server instability or limited modification of data.

### CVE-2026-85968

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-12T17:17:37.387 |

Progress MarkLogic Server 12.x releases before 12.1.0 contain an out-of-bounds read vulnerability in certain query-processing functionality. A remote authenticated attacker could exploit this vulnerability to cause server instability or disclose limited information from process memory.

### CVE-2026-109353

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T17:17:32.423 |

LibreNMS before 26.9.0 contains an SQL injection vulnerability that allows unprivileged users to inject SQL by supplying an array-valued notification_id parameter to notifications.inc.php. Attackers can perform cross-table reads of users.password hashes, with results persisted in notifications_attribs and readable through the interface.

### CVE-2026-109351

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-12T17:17:32.123 |

Gitoxide gix-pack before 0.75.0 contains an uncontrolled memory allocation vulnerability that allows remote attackers to abort the process by supplying a huge pack-header object count. Malicious remotes can serve a 12-byte pack header claiming 0xFFFFFFFF objects, forcing Tree::with_capacity to reserve hundreds of gigabytes and crash clone or fetch operations.

### CVE-2026-109350

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-12T17:17:31.973 |

Gitoxide gix-pack before 0.75.0 contains a denial of service vulnerability that allows malicious remotes to crash fetch operations by sending crafted thin-pack OFS_DELTA entries. Attackers can serve a thin pack with a REF_DELTA referencing an existing object followed by an OFS_DELTA whose base_distance exceeds pack_offset, triggering a panic in LookupRefDeltaObjectsIter that aborts the fetch process.

### CVE-2026-109349

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-12T17:17:31.823 |

gitoxide gix-pack before 0.75.0 contains a reachable assertion in BytesToEntriesIter::new_from_header: the pack header decoder accepts version 3, but a release-enabled assert_eq! requires version 2. A malicious remote can send a 12-byte pack header declaring version 3 to panic the client and abort the clone or fetch.

### CVE-2026-109341

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-12T17:17:30.550 |

SurrealDB before 3.3.0 contains an authorization bypass vulnerability that allows callers with table-level write permission to read SELECT-restricted fields by resolving JSON Patch pointers against the unreduced record. Attackers can use PATCH copy or move operations to copy hidden fields into readable destinations, or abuse test mismatch errors as a disclosure oracle.

### CVE-2026-109338

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-12T17:17:30.060 |

SurrealDB before 3.3.0 contains a denial of service vulnerability that allows query-capable users to crash the server by reading non-ASCII header values in embedded JavaScript. Attackers with scripting enabled can read such values via Headers get(), entries(), values(), or getSetCookie(), or return them from fetch() endpoints, aborting the server process.

### CVE-2026-109335

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-12T17:17:29.533 |

SurrealDB from 3.0.0 before 3.3.0 contains an information disclosure vulnerability that allows record users to read values hidden by field-level SELECT permissions through COMPUTED fields. Attackers can select records whose readable COMPUTED fields derive from hidden fields, or use write RETURN clauses with $before/$after to expose hidden values.

### CVE-2026-109333

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T17:17:29.190 |

SurrealDB from 3.0.0 before 3.3.0 contains an authorization bypass vulnerability that allows authenticated record users to read records in other namespaces or databases by resolving record ids through FETCH. Attackers can switch to a foreign namespace/database and name a known record id in a RETURN … FETCH query to read another tenant's data when table PERMISSIONS allow reads.

### CVE-2026-109324

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-10-12T17:17:27.690 |

Grav before 2.1.7 contains a denial of service vulnerability that allows authenticated media authors to exhaust memory by uploading compressed oversized raster images. Attackers can reference a Twig or Markdown transform so GD or Imagick decodes the full source without dimension checks, letting anonymous requests repeatedly cause page unavailability.

### CVE-2026-109315

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-12T17:17:26.340 |

Grav from 2.0.22 before 2.1.7 contains an information disclosure vulnerability that allows page editors to read the Clockwork debugger token because the sandbox redaction list omits system.debugger.token. Attackers can render the token through editor-authored Twig and supply it as X-Clockwork-Auth to read profiler records with configuration, request metadata, and database queries.

### CVE-2026-109311

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-12T17:17:25.730 |

vLLM before 0.29.0 passes uploaded audio to the PyAV/FFmpeg av.open() fallback with only a file-size check, exposing FFmpeg's IAMF parser heap overflow. Authenticated remote attackers can repeatedly upload malformed IAMF containers to /v1/audio/transcriptions, corrupting the heap and crashing the API process.

### CVE-2026-109310

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-12T17:17:25.560 |

SiYuan v3.1.12 before v3.8.6 fails to restrict the Sprig template function map in the /api/icon/getDynamicIcon content parameter, allowing resource exhaustion. A publish reader, or anyone when publish auth is disabled, can use uncapped functions like until to OOM-kill the kernel with one request.

### CVE-2026-109299

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-12T17:17:23.540 |

Open WebUI from 0.9.0 before 0.11.4 contains a denial of service vulnerability that allows authenticated users with automations permission to stall the instance by submitting unsatisfiable recurrence rules. Attackers can repeatedly send rules like February 30th to the automations create or update endpoints, blocking the shared event loop for seconds per request.

### CVE-2026-109298

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-12T17:17:23.390 |

Open WebUI 0.11.0 before 0.11.4 compiles user-chosen grep patterns for its knowledge and chat file search tools with a regex engine that expands nested counted repetition unbounded at compile time and caches the result. Authenticated users can have the model call grep_knowledge_files with short nested-repetition patterns, blocking the event loop and exhausting worker memory.

### CVE-2026-109297

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-12T17:17:23.240 |

Open WebUI 0.11.0 before 0.11.4 contains a denial of service vulnerability in the automation recurrence-rule validator, whose sub-daily frequency guard parses rule text more strictly than the calendar library that executes it. Users permitted to create automations can submit whitespace-folded rules (or, in 0.11.0, lowercase frequencies or omitted RRULE prefixes) that expand per-second synchronously, blocking the shared event loop for minutes per request and on every scheduler poll.

### CVE-2026-109295

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-12T17:17:22.950 |

Open WebUI from 0.11.0 before 0.11.4 contains a regular expression denial of service vulnerability that allows authenticated users to stall server workers via file search patterns. Attackers can instruct the model to call grep_knowledge_files or grep_chat_files with a catastrophically backtracking regex, blocking the event loop for two seconds per repeated call.

### CVE-2026-109294

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-12T17:17:22.800 |

Open WebUI from 0.6.42 before 0.11.4 contains an uncontrolled resource consumption vulnerability that allows authenticated users to exhaust server memory by supplying compressed remote image URLs in chat messages. Attackers can point the image field at a host returning gzip-encoded responses, which get_image_base64_from_url decompresses unbounded, causing denial of service for all users.

### CVE-2026-109293

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-12T17:17:22.650 |

Open WebUI from 0.11.0 before 0.11.4 contains an information disclosure vulnerability that allows authenticated non-admin users with tool export permission to obtain tool source code shared with them read-only. Attackers can request GET /api/v1/tools/export to retrieve the full Python source of read-only shared tools, exposing embedded API keys and credentials.

### CVE-2026-109246

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-12T17:17:15.630 |

FreeRDP before 3.32.0 contains a divide-by-zero vulnerability in the freerdp-shadow-cli shadow server: the frame id in a client's Frame Acknowledge PDU is stored without a range check, so the in-flight frame count in shadow_encoder_inflight_frames() can underflow. An authenticated client can acknowledge a frame id one greater than the last frame sent, causing shadow_encoder_create_frame_id() to divide by zero (SIGFPE) and terminate the process, disconnecting all viewers.

### CVE-2026-109242

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-908` |
| Published | 2026-10-12T17:17:15.023 |

FreeRDP before 3.0.0 and 3.6.0 before 3.32.0 renders uninitialized heap memory from un-decoded progressive tiles because the tile->current buffer is allocated without zeroing. A malicious RDP server can send a crafted WBT_TILE_FIRST then WBT_TILE_UPGRADE sequence to paint heap bytes onscreen or abort the client process.

### CVE-2026-105668

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-10-12T16:17:02.943 |

Protection Mechanism Failure vulnerability in hexpm hex allows the owner of a package, or an attacker who has taken over the owner's account, to get a newly published release past the release-age cooldown.

The cooldown (cooldown config, HEX_COOLDOWN) withholds versions younger than the configured age during dependency resolution. When the release of a package locked in mix.lock is retired or has a security advisory, Hex.RemoteConverger.build_cooldown_bypass/3 and Hex.RemoteConverger.unsafe_lock_bypass/1 lift the cooldown for every version of that package and of every package the locked release depends on, so that mix deps.update can move off the unsafe release. Retiring a release needs the same package owner permission as publishing one. An attacker who publishes a malicious release can retire the currently locked release, and the next mix deps.update that unlocks the package selects the new release regardless of its age. Hex.Registry.Cooldown.versions/2 checks the bypass by package name alone, so the bypass also covers packages with the same name in other repositories. Cooldown configured through an organization dependency policy is not affected.

This issue affects hex: from 2.5.0 before 2.5.2.

### CVE-2026-74031

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T14:17:39.633 |

Wazuh from 4.1.1 before 4.14.8 contains a path traversal vulnerability in the delete_rule_file and delete_decoder_file helpers that allows malicious cluster workers to delete arbitrary files via an unvalidated filename parameter. Attackers holding the cluster key can invoke these helpers through DistributedAPI with traversal sequences to delete ossec.conf, client.keys, or rules as the wazuh user.

### CVE-2026-104355

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-12T19:16:36.900 |

A connected peer cluster can modify a Temporal Server cluster's local namespaces, which are never replicated to that peer, because the receiving cluster applies inbound namespace replication updates to them. In a multi-cluster deployment, each cluster pulls replication tasks from the remote clusters an administrator has registered with connection enabled; the sending side excludes local namespaces, but the receiving side does not apply the same rule. When an inbound task names an existing namespace, the server checks at most that the namespace identifiers match, then overwrites its state, description, owner, retention, archival settings, and cluster list, and its active cluster when the task carries a higher failover version, without checking that the namespace is global. A party that controls a registered peer's replies, by operating or compromising it, can therefore change any local namespace whose name and identifier it can supply, without any credential on the receiving cluster: for example, marking it Deprecated, making the peer its active cluster, and shortening its retention, after which new Workflow starts in that namespace fail. Local namespaces include the built-in temporal-system namespace. Namespace metadata the History service refreshes from the peer while processing its history replication tasks passes through the same logic. A cluster with no remote cluster registered with connection enabled is not exposed.

### CVE-2026-109361

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-12T17:17:33.630 |

MONAI 1.2.0 before 1.6.1 contains an insecure deserialization vulnerability in nnUNetV2Runner that unpickles the postprocessing_file path read from inference_information.json without confining it to the results directory. Attackers who can modify inference_information.json can point it at a malicious pickle elsewhere on the filesystem to execute code when predict_ensemble_postprocessing runs.

### CVE-2026-109250

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-10-12T17:17:16.230 |

FreeRDP 3.0.0 before 3.32.0 contains a heap buffer overflow vulnerability in collect_keys() that allows local attackers to write past the fixed 64-entry keys array during PKCS#11 key enumeration. Attackers controlling smartcard tokens can present more than 64 public key objects across multiple slots to corrupt heap memory with attacker-chosen CKA_ID and CKA_LABEL data during smartcard logon.
