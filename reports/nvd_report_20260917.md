# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-16 15:00 UTC
- **対象期間**: `2026-09-15T15:00:58.000Z` 〜 `2026-09-16T15:00:35.000Z`
- **重要CVE数**: 989 件（Critical 9.0+: 167 件 / High 7.0〜: 822 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公表された CVE の大半は **Oracle Fusion Middleware 系列**（WebLogic、Forms、Internet Directory など）で、CVSS が 10.0 と最高評価のリモートコード実行（RCE）脆弱性が集中しています。  
- 多くは **認証不要・ネットワークから直接 HTTP/LDAP に対して攻撃可能** で、攻撃成功時は機密情報の完全取得（C:H/I:H）だけでなく、システム全体の制御権取得（A:H）も可能です。  
- Oracle 製品以外でも、**HPE EdgeConnect SD‑WAN Orchestrator** の認証済み特権昇格、**MCP / MySQL MCP Server** のサンドボックス回避、**DIRAC** の権限昇格・情報漏洩、そして **スタックオーバーフロー系の root RCE** が報告されており、インフラ全体で「外部からの直接侵入」リスクが顕在化しています。  

---

## 2. 特に注目すべき CVE  

| CVE | 製品・コンポーネント | CVSS | 主な影響 | 注目理由 |
|-----|-------------------|------|----------|----------|
| **CVE‑2026‑83021** | Oracle WebLogic Server – Web Container | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | 認証不要で HTTP 経由により完全リモートコード実行 (RCE) が可能。攻撃者は任意のシェルコードを実行し、管理者権限でシステムを乗っ取れる。 | WebLogic は多くのエンタープライズアプリの基盤。未パッチ環境がそのまま外部からの踏み台になる危険性が極めて高い。 |
| **CVE‑2026‑83099** | Oracle Forms (Fusion Middleware) – Forms Services, C/S, Charmode | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | 認証不要で HTTP 経由により完全 RCE。特に Forms アプリケーションサーバが外部に公開されているケースで致命的。 | Forms は金融・官公庁系システムで根強く使用されており、影響範囲が広い。 |
| **CVE‑2026‑83059** | Oracle Internet Directory – OID LDAP Server | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | LDAP ポートから認証不要で完全 RCE。ディレクトリサービスが侵害されると、全社の認証基盤が崩壊する。 | LDAP は内部認証・シングルサインオンの要で、侵害は横方向展開を容易にする。 |
| **CVE‑2026‑87230** | Oracle Hyperion Financial Management – Security | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | HTTP 経由で認証不要の完全 RCE。財務データベースへの不正アクセス・改ざんが可能。 | 金融系システムは機密性が極めて高く、財務情報改ざんは法的・経営的リスクが甚大。 |
| **CVE‑2026‑76670** | HPE EdgeConnect SD‑WAN Orchestrator – API | 9.9 (AV:N/AC:L/PR:L/UI:N/S:C) | 認証済み低権限ユーザーが API を悪用し管理者権限へ昇格。SD‑WAN の全トラフィック制御が奪取される。 | SD‑WAN は企業ネットワークの中枢。特権昇格はネットワーク全体の機密情報漏洩・改竄につながる。 |

> **共通点**：すべて **ネットワークから直接アクセス可能** なサービスで、**認証不要（または低権限）** という点が最大の危険因子です。特に Oracle 製品は「Web Container」や「LDAP Server」など、内部システム全体の基盤を担うコンポーネントが対象となっているため、早急な対策が必須です。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 | 現行脆弱バージョン | 推奨バージョン（パッチ適用後） | パッケージ名・リリース |
|------|-------------------|------------------------------|------------------------|
| Oracle WebLogic Server | 12.2.1.4.0、14.1.1.0.0、14.1.2.0.0、15.1.1.0.0 | 12.2.1.4.0 **Patch 2026‑83021‑01** 以降、14.1.1.0.0 **Patch 2026‑83021‑02** 以降、… | `wls-server` (Oracle WebLogic Server) |
| Oracle Forms (Fusion Middleware) | 12.2.1.19.0、14.1.2.0.0 | 12.2.1.19.0 **Patch 2026‑83099‑01** 以降、14.1.2.0.0 **Patch 2026‑83099‑01** 以降 | `forms` |
| Oracle Internet Directory | 12.2.1.4.0、14.1.2.1.0 | 12.2.1.4.0 **Patch 2026‑83059‑01** 以降、14.1.2.1.0 **Patch 2026‑83059‑01** 以降 | `oid` |
| Oracle Hyperion Financial Management | 11.2.26.0.000 | 11.2.26.0.000 **Patch 2026‑87230‑01** 以降 | `hyperion-fm` |
| HPE EdgeConnect SD‑WAN Orchestrator | (ベンダー提供の任意バージョン) | 最新リリース（2026‑Q3 以降）にアップデートし、**CVE‑2026‑76670** 修正パッチを適用 | `edgeconnect-orchestrator` |
| MCP (AI gateway) | < 1.0.2 | ≥ 1.0.2 | `mcp` |
| MySQL MCP Server | < 0.4.2 | ≥ 0.4.2 | `mysql-mcp-server` |
| DIRAC | < 8.0.79 / 9.0.22 / 9.1.10 | 8.0.79 以上、9.0.22 以上、9.1.10 以上 | `dirac`

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-87230

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:11.513 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 10.0 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-83099

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:20.007 |

Vulnerability in the Oracle Forms product of Oracle Fusion Middleware (component: Forms Services, C/S, Charmode).  Supported versions that are affected are 12.2.1.19.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Forms.  While the vulnerability is in Oracle Forms, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Forms. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83059

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:14.563 |

Vulnerability in the Oracle Internet Directory product of Oracle Fusion Middleware (component: OID LDAP Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Internet Directory.  While the vulnerability is in Oracle Internet Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Internet Directory. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83021

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:09.777 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Web Container).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebLogic Server.  While the vulnerability is in Oracle WebLogic Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83020

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:09.060 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Platform Security for Java.  While the vulnerability is in Oracle Platform Security for Java, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-71133

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:17:42.343 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-53710

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-693` |
| Published | 2026-09-15T17:17:19.117 |

MCP Context Forge is an AI gateway, registry, and proxy for MCP, A2A, REST, and gRPC APIs. Prior to 1.0.2, the python_sandbox_server in mcp-servers/python/python_sandbox_server/src/python_sandbox_server/server_fastmcp.py exposes raw getattr through safe_builtins, omits a required _getattr_ guard, and relies on validate_code checks for literal dangerous dunder strings. An attacker can construct dunder names at runtime, traverse the Python class hierarchy, reach subprocess.Popen, and execute OS commands with the server process privileges through the execute_code MCP tool. The HTTP/SSE transport can expose this tool without authentication, while stdio-only deployments have reduced network reachability. The issue affects the python_sandbox_server subproject and does not directly affect the core Context Forge gateway or proxy components. This issue is fixed in version 1.0.2.

### CVE-2026-59971

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-346` |
| Published | 2026-09-15T15:17:19.947 |

MySQL MCP Server is a Model Context Protocol server that enables secure interaction with MySQL databases. Prior to 0.4.2, setting MCP_TRANSPORT=sse causes src/mysql_mcp_server/server.py to construct SseServerTransport without security_settings or enable_dns_rebinding_protection, while the Starlette routes /, /sse, and /messages/ have no authentication and the service binds to 0.0.0.0 by default. A network attacker can directly reach execute_sql, or can use DNS rebinding to make a victim's browser relay same-origin requests to a locally bound service, and supply a query that reaches cursor.execute(query). This allows unauthenticated disclosure and modification of the configured database; when the MySQL account has FILE privileges, the same access can read or write server files and may enable code execution. The default stdio transport is not affected. This issue is fixed in 0.4.2.

### CVE-2026-87172

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:04.970 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83282

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:40.820 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).   The supported version that is affected is 12.2.1.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  While the vulnerability is in Oracle Business Intelligence Enterprise Edition, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83058

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:14.450 |

Vulnerability in the Oracle Internet Directory product of Oracle Fusion Middleware (component: OID LDAP Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Internet Directory.  While the vulnerability is in Oracle Internet Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Internet Directory. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83057

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:14.340 |

Vulnerability in the Oracle Internet Directory product of Oracle Fusion Middleware (component: OID LDAP Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Internet Directory.  While the vulnerability is in Oracle Internet Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Internet Directory. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83056

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:14.230 |

Vulnerability in the Oracle Internet Directory product of Oracle Fusion Middleware (component: OID LDAP Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Internet Directory.  While the vulnerability is in Oracle Internet Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Internet Directory. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83055

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:14.113 |

Vulnerability in the Oracle Internet Directory product of Oracle Fusion Middleware (component: OID LDAP Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Internet Directory.  While the vulnerability is in Oracle Internet Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Internet Directory. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83039

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:12.297 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Composer).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83038

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:12.187 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: TopLink Integration).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebLogic Server.  While the vulnerability is in Oracle WebLogic Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83031

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:11.370 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Sites.  While the vulnerability is in Oracle WebCenter Sites, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-82999

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:06.460 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Service Delivery Platform.  While the vulnerability is in Service Delivery Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-82998

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:06.343 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Service Delivery Platform.  While the vulnerability is in Service Delivery Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-82997

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:06.233 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Service Delivery Platform.  While the vulnerability is in Service Delivery Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-76672

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:48.977 |

A vulnerability exists in the SD-WAN Orchestrator that may lead to the exposure of sensitive configuration information. An authenticated remote attacker with read-only privileges could exploit this vulnerability by sending a specially crafted request to the cache synchronization endpoint. Successful exploitation could result in the disclosure of sensitive third-party API tokens and credentials, potentially enabling lateral movement to external security platforms.

### CVE-2026-76670

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:48.833 |

Privilege escalation vulnerabilities exist in the API of HPE Networking EdgeConnect SD-WAN Orchestrator. Successful exploitation could allow a remote low-privileged authenticated user to escalate their privileges to those of an administrative user, leading to complete system compromise.

### CVE-2026-76669

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:48.627 |

Privilege escalation vulnerabilities exist in the API of HPE Networking EdgeConnect SD-WAN Orchestrator. Successful exploitation could allow a remote low-privileged authenticated user to escalate their privileges to those of an administrative user, leading to complete system compromise.

### CVE-2026-73948

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:45.913 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Composer).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-73945

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:45.563 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-71163

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:42.490 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Access Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Access Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Access Manager. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L).

### CVE-2026-61667

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89;CWE-95` |
| Published | 2026-09-15T18:17:27.050 |

DIRAC is an interware, meaning a software framework for distributed computing. Prior to versions 8.0.79, 9.0.22, and 9.1.10, DataManagementSystem/Service/FileCatalogHandler.py checkDataset forwards an authenticated caller-controlled datasets value to DatasetManager.py __checkDataset, where datasetName is interpolated into an FC_MetaDatasets SQL query without parameterization. The injected query can control the returned MetaQuery value, which is passed to Python eval and permits command execution as the account running the DIRAC services. Successful exploitation can expose dirac.cfg, database passwords, stored proxies, and tokens, fully compromise the DIRAC system, and allow alteration of local log evidence. This issue is fixed in versions 8.0.79, 9.0.22, and 9.1.10.

### CVE-2026-45579

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-09-15T18:17:21.427 |

DIRAC is an interware, meaning a software framework for distributed computing. Prior to versions 8.0.79, 9.0.22, and 9.1.10, the RequestManagementSystem/Service/ReqManagerHandler.py export_getRequestCountersWeb function passes an authenticated caller-controlled groupingAttribute to RequestManagementSystem/DB/RequestDB.py getRequestCountersWeb. An unrecognized value is resolved against the Request object and evaluated as Python code, allowing a crafted dunder attribute expression to reach operating-system functions and execute commands as the account running the DIRAC services. Successful exploitation can expose dirac.cfg, database passwords, stored proxies, and tokens, fully compromise the DIRAC system, and allow alteration of local log evidence. This issue is fixed in versions 8.0.79, 9.0.22, and 9.1.10.

### CVE-2026-91843

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-16T14:17:13.947 |

A stack overflow during the unauthenticated login process may allow an attacker to run arbitrary code remotely with root privileges.

### CVE-2026-27565

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T08:16:39.740 |

An unauthenticated remote attacker can upload a malicious IODD file that places and executes a shell script with root privileges. The shell script remains active even after a reboot.

### CVE-2026-27546

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-09-16T08:16:36.850 |

An unauthenticated remote attacker can exploit an authentication bypass in the _account_log function to log in as an admin, even when accounts are properly configured.

### CVE-2026-14349

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T04:17:58.777 |

The TrueBooker – Appointment Booking and Scheduler System plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 1.2.3. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to modify the email address of arbitrary user accounts, including administrators, which can be leveraged to reset the account's password and gain access to it.

### CVE-2026-12793

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-16T04:17:56.110 |

The JetFormBuilder — Dynamic Blocks Form Builder plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 3.6.2. This is due to the plugin not validating that a submitted form ID belongs to a JetFormBuilder form before parsing the referenced post's content as form schema and executing an Advanced Validation server-side callback. This makes it possible for unauthenticated attackers to create a new administrator-level user account.

### CVE-2026-61560

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-15T22:16:58.040 |

`@zereight/mcp-gitlab` is a Model Context Protocol server for GitLab. Prior to version 2.1.27, the SSE transport mode (`SSE=true`) exposes all MCP tools without any authentication. The `upload_markdown` tool reads arbitrary files from the server's local filesystem via an unsanitized `file_path` parameter and uploads them to a GitLab project. Combined, any unauthenticated network-reachable attacker can read `/proc/self/environ` to steal the server's `GITLAB_PERSONAL_ACCESS_TOKEN` and achieve full GitLab account takeover. This is the default configuration for Docker deployments. Version 2.1.27 contains a patch.

### CVE-2026-54337

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-15T21:16:36.920 |

Fireshare facilitates self-hosted media and link sharing. Prior to version 1.6.14, an argument Injection in the video upload function allows unauthenticated attacker to write/overwrite system files. Version 1.6.14 fixes the issue.

### CVE-2026-87188

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:19:06.727 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87184

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:19:06.290 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via SQL to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83462

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:55.030 |

Vulnerability in the Oracle Mobile Application Server product of Oracle E-Business Suite (component: MWA Terminal Server).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Mobile Application Server.  Successful attacks of this vulnerability can result in takeover of Oracle Mobile Application Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83452

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:53.950 |

Vulnerability in the Oracle Document Management and Collaboration product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Document Management and Collaboration.  Successful attacks of this vulnerability can result in takeover of Oracle Document Management and Collaboration. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83355

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:49.020 |

Vulnerability in the Oracle Enterprise Manager for Fusion Middleware product of Oracle Enterprise Manager (component: Metrics).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Enterprise Manager for Fusion Middleware.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager for Fusion Middleware. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83339

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:47.243 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83327

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:45.880 |

Vulnerability in the Oracle Applications Framework product of Oracle E-Business Suite (component: Personalization).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Oracle Applications Framework.  Successful attacks of this vulnerability can result in takeover of Oracle Applications Framework. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83283

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:40.927 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).   The supported version that is affected is 12.2.1.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83269

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:39.290 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle BI Publisher.  Successful attacks of this vulnerability can result in takeover of Oracle BI Publisher. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83261

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:38.403 |

Vulnerability in the Oracle Product Lifecycle Analytics product of Oracle Supply Chain (component: Core).   The supported version that is affected is 3.6.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Product Lifecycle Analytics.  Successful attacks of this vulnerability can result in takeover of Oracle Product Lifecycle Analytics. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83232

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:35.080 |

Vulnerability in the Oracle Data Integrator product of Oracle Fusion Middleware (component: Console / Repository Explorer).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Data Integrator.  Successful attacks of this vulnerability can result in takeover of Oracle Data Integrator. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83151

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:25.857 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83108

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:21.000 |

Vulnerability in the Oracle Forms product of Oracle Fusion Middleware (component: Forms Services, C/S, Charmode).  Supported versions that are affected are 12.2.1.19.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Forms.  Successful attacks of this vulnerability can result in takeover of Oracle Forms. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83100

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:20.113 |

Vulnerability in the Oracle Forms product of Oracle Fusion Middleware (component: Forms Services, C/S, Charmode).  Supported versions that are affected are 12.2.1.19.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Forms.  Successful attacks of this vulnerability can result in takeover of Oracle Forms. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83098

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:19.877 |

Vulnerability in the Oracle Forms product of Oracle Fusion Middleware (component: Forms Services, C/S, Charmode).  Supported versions that are affected are 12.2.1.19.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Forms.  Successful attacks of this vulnerability can result in takeover of Oracle Forms. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83095

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:19.427 |

Vulnerability in the Oracle Forms product of Oracle Fusion Middleware (component: Forms Services, C/S, Charmode).  Supported versions that are affected are 12.2.1.19.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Forms.  Successful attacks of this vulnerability can result in takeover of Oracle Forms. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83094

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:19.313 |

Vulnerability in the Oracle Forms product of Oracle Fusion Middleware (component: Forms Services, C/S, Charmode).  Supported versions that are affected are 12.2.1.19.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Forms.  Successful attacks of this vulnerability can result in takeover of Oracle Forms. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83066

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:15.443 |

Vulnerability in the Oracle Internet Directory product of Oracle Fusion Middleware (component: OID LDAP Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle Internet Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Internet Directory. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83062

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:14.907 |

Vulnerability in the Oracle Internet Directory product of Oracle Fusion Middleware (component: OID LDAP Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Internet Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Internet Directory. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83061

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:14.790 |

Vulnerability in the Oracle Internet Directory product of Oracle Fusion Middleware (component: OID LDAP Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Internet Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Internet Directory. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83060

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:14.680 |

Vulnerability in the Oracle Internet Directory product of Oracle Fusion Middleware (component: OID LDAP Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Internet Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Internet Directory. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83054

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:14.000 |

Vulnerability in the Oracle Internet Directory product of Oracle Fusion Middleware (component: OID LDAP Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Internet Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Internet Directory. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83042

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:12.633 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83037

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:12.077 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83036

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:11.970 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83035

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:11.853 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83000

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:06.570 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-82995

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:06.010 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Oracle Platform Security for Java.  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-82994

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:05.900 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Platform Security for Java.  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-76674

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:49.207 |

Buffer overflow vulnerabilities exist in the underlying operating system of HPE Networking EdgeConnect SD-WAN Gateways that could allow an unauthenticated remote attacker to execute arbitrary code. Successful exploitation could allow an attacker to execute arbitrary commands on the underlying operating system leading to complete system compromise.

### CVE-2026-76673

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:49.090 |

Vulnerabilities have been identified in the API of EdgeConnect SD-WAN Orchestrator that could potentially allow an unauthenticated remote actor to circumvent existing authentication controls. Successful exploitation could allow an attacker to gain administrative privileges leading to complete compromise of the EdgeConnect SD-WAN Orchestrator host.

### CVE-2026-73963

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:17:47.550 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Portlet Services).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-73961

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:17:47.320 |

Vulnerability in the Oracle JDeveloper product of Oracle Fusion Middleware (component: ADF Faces).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle JDeveloper.  Successful attacks of this vulnerability can result in takeover of Oracle JDeveloper. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-73956

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:17:46.780 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Composer).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-73953

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:17:46.457 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Portlet Services).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-73950

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:17:46.133 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-73947

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:17:45.803 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-73940

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:17:44.943 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70913

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:17:41.980 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70757

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:17:41.863 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70756

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:17:41.740 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70748

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:17:41.470 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-19773

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-15T19:17:17.747 |

libwebsockets HTTP/2 HPACK Path Header Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of libwebsockets. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the parsing of HTTP/2 HPACK path header. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-31036.

### CVE-2026-12351

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-09-15T18:17:13.727 |

IBM MQ 9.3.0.0 through 9.3.0.41 LTS, 9.3.0.0 through 9.3.5.1 CD, 9.4.0.0 through 9.4.0.25 LTS, 9.4.0.0 through 9.4.5.1 LTS, and 10.0.0.0 could allow a remote attacker to execute arbitrary code due to unsafe JNDI lookup processing when the IVT application is deployed.

### CVE-2026-55211

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-15T16:17:14.560 |

Surfio is a library for reading and writing surface files. Prior to 0.0.19, surfio does not correctly validate size fields in IRAP files, leading to a buffer overflow when untrusted files are parsed. The severity assumes surfio is used to parse untrusted files in a networking context such as a web service. This issue is fixed in version 0.0.19.

### CVE-2026-63695

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-15T15:17:20.390 |

Dell SmartFabric OS10 Software, versions prior to 10.6.1.3, contains a Session Fixation vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Session theft.

### CVE-2026-91749

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-15T21:16:48.833 |

Use after free in Workers in Google Chrome prior to 153.0.8010.47 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-91738

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-15T21:16:47.397 |

Improper input validation in ANGLE in Google Chrome prior to 153.0.8010.47 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-91729

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-15T21:16:46.263 |

Use after free in DigitalCredentials in Google Chrome prior to 153.0.8010.47 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-91728

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-15T21:16:46.130 |

Integer overflow in V8 in Google Chrome prior to 153.0.8010.47 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-91718

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-15T21:16:44.807 |

Use after free in Core in Google Chrome prior to 153.0.8010.47 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-91716

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-15T21:16:44.563 |

Use after free in Auth in Google Chrome prior to 153.0.8010.47 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-91710

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-15T21:16:43.800 |

Use after free in WebAppInstalls in Google Chrome prior to 153.0.8010.47 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-61568

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-350` |
| Published | 2026-09-15T21:16:41.570 |

`@zereight/mcp-gitlab` is a Model Context Protocol server for GitLab. Versions prior to 2.1.30 expose the Streamable HTTP MCP endpoint without an effective Host or Origin allowlist. A malicious web page can use DNS rebinding to route browser requests to a victim's local MCP listener while preserving an attacker-controlled `Host` and `Origin`. The server accepts those headers and reaches the MCP initialization path instead of rejecting the request at the HTTP boundary. Version 2.1.30 contains a patch.

### CVE-2026-61559

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-15T21:16:41.390 |

`@zereight/mcp-gitlab` is a Model Context Protocol server for GitLab. Starting in version 0.0.1 and prior to version 2.1.27, when the environment variable `ENABLE_DYNAMIC_API_URL=true` is set, the server reads the `X-GitLab-API-URL` HTTP request header and uses it as the base URL for all outbound GitLab API calls made within that request. The server validates that the value is a well-formed URL (`new URL(dynamicApiUrl)`) but applies no allowlist or hostname restriction. The server then attaches the victim's `Private-Token` to every outbound fetch that uses the redirected URL. Any caller who can reach the HTTP transport can set `X-GitLab-API-URL` to an attacker-controlled host. The next GitLab API call the server makes delivers the victim's token to that host. Version 2.1.27 contains a patch.

### CVE-2026-87186

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:06.507 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 9.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83043

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:12.743 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Composer).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-83040

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:12.410 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Portlet Services).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Oracle WebCenter Portal.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-83029

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:11.037 |

Vulnerability in the Oracle Managed File Transfer product of Oracle Fusion Middleware (component: MFT Runtime Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Managed File Transfer.  While the vulnerability is in Oracle Managed File Transfer, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Managed File Transfer accessible data as well as  unauthorized access to critical data or complete access to all Oracle Managed File Transfer accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-73962

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:47.433 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Access Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Access Manager accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-73453

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-16T10:16:52.043 |

An unauthenticated P4Runtime (Programming Protocol-Independent Packet Processors Runtime) client can achieve arbitrary code execution under certain conditions on affected platforms running Arista EOS configured with P4Runtime. P4Runtime is disabled by default in Arista EOS. By crafting a malicious packet during the initiation of a P4Runtime session, an attacker can obtain complete administrative control over the compromised switch.

This issue was discovered internally by Arista, and the company is not aware of any malicious exploitation of this vulnerability in customer networks.

### CVE-2026-15640

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-16T00:17:03.577 |

Under certain conditions a valid SAML IdP response may be used to impersonate another Secret Server user.

### CVE-2026-78225

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-15T22:17:02.870 |

A hardcoded cryptographic server key vulnerability exists in the deployer-ng Update Controller component of Wärtsilä FOS-Onboard.

### CVE-2026-58146

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T12:17:04.980 |

WNC T-Mobile 5G Box IDU router is vulnerable to OS command injection vulnerability. The vulnerability exists within the /cgi-bin/portal.cgi endpoint, specifically through the cli_cookie POST parameter. The cli_cookie parameter value is directly concatenated into a find command string without proper sanitization. This allows a remote, unauthenticated attacker to inject and execute arbitrary shell commands as root on the underlying operating system.

This issue has been fixed in firmware version 1.1.0.651412

### CVE-2026-73461

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-16T09:17:05.147 |

On affected EOS platforms with AAA-based gRPC authorization enabled for OpenConfig, gRPC requests of an authenticated user to OpenConfig may use the wrong privilege level, resulting in an authorization using the wrong AAA method list. This does not impact non-gRPC OpenConfig requests such as NETCONF.

### CVE-2026-73447

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T07:16:37.087 |

A privileged attacker can exploit certain operation to execute arbitrary commands with root privileges, leading to full device compromise. An authenticated user can exploit gRPC Network Security Interface (gNSI) Certz service on Arista EOS-based products to escalate privileges and execute arbitrary OS commands via a crafted Certz Rotate request. The Bootz service is also affected.

### CVE-2026-68491

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-15T21:16:42.423 |

An insufficient check allowed for the overwrite of arbitrary files via a symlink.

### CVE-2026-66890

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-15T21:16:42.090 |

The affected products use hard-coded credentials, which could allow remote access to files with root privileges where FTP is reachable.

### CVE-2026-66887

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-15T21:16:41.930 |

The affected products are missing authorization on state-changing CGIs and session checks are not performed.

### CVE-2026-73172

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T13:18:05.600 |

Nozomi Networks Labs identified a CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability in the edgserver management service of Advantech EKI-1242EIMS in firmware version V1.06.01 that allows a remote unauthenticated attacker to execute arbitrary OS commands as root via crafted requests to TCP port 5058.

### CVE-2026-58147

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T12:17:05.103 |

WNC T-Mobile 5G Box IDU router contains an OS command injection vulnerability in the portal.cgi component's password change functionality. The application improperly neutralizes special elements in the http_passwd_hidden and http_passwdConfirm_hidden parameters, allowing an authenticated attacker to execute arbitrary commands on the underlying operating system with root privileges.This issue has been fixed in firmware version 1.1.0.651412

### CVE-2026-40855

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T12:17:03.673 |

WNC T-Mobile 5G Box IDU router is vulnerable to a command injection. The vulnerability exists in the ping functionality within the /cgi-bin/portal.cgi endpoint, specifically affecting the ping_ip, ping_size, and ping_times POST parameters. The root cause is the failure to verify and sanitize user-supplied input before incorporating it into a system command. This allows an authenticated attacker to execute arbitrary commands on the shell and gain root access to the system.This issue has been fixed in firmware version 1.1.0.651412

### CVE-2026-15639

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-16T00:17:03.453 |

An attacker can craft a malicious link that, if used by a legitimate user, may cause the user's browser to run JavaScript supplied by the attacker.

### CVE-2026-81855

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-15T22:17:03.197 |

A hardcoded cryptographic client authentication key vulnerability exists in the robot testing framework component of Wärtsilä FOS-Onboard.

### CVE-2026-73807

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-15T22:16:58.683 |

The mySCADA myPRO Manager command API does not properly enforce authentication for privileged functions. An unauthenticated attacker with network access to the affected API could exploit this vulnerability to access privileged management functions.

### CVE-2026-91939

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-15T21:16:48.957 |

Cotonti 1.0.0 Comments plugin passes the ci GET parameter to unserialize() without allowed_classes restriction, allowing unauthenticated attackers to instantiate arbitrary PHP classes with attacker-controlled properties. Attackers can exploit PHP object injection through crafted serialized payloads to trigger gadget chains and achieve database manipulation or code execution.

### CVE-2026-89040

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-15T20:19:20.240 |

Tencent Mass Service Engine in Cluster (MSEC) allows a remote, unauthenticated attacker to send a crafted POST request including ../ and gain root access on the target device. An attacker who uploads a webshell can execute arbitrary code as root.

### CVE-2026-83027

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:10.757 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Identity Manager Connector executes to compromise Oracle Identity Manager Connector.  While the vulnerability is in Oracle Identity Manager Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Identity Manager Connector accessible data as well as  unauthorized access to critical data or complete access to all Oracle Identity Manager Connector accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-73957

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:46.887 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Portlet Services).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Portal accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-53459

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-636;CWE-755` |
| Published | 2026-09-15T18:17:22.120 |

Bambuddy is a self-hosted print archive and management system for Bambu Lab 3D printers. Starting in version 0.1.6 and prior to version 0.2.4.4, a fail-open in the authentication code allows any attacker to bypass authentication by flooding a public endpoint to exhaust resources causing database access to fail, granting unauthenticated access to all protected endpoints. Version 0.2.4.4 patches the issue.

### CVE-2026-89026

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-15T17:17:33.510 |

The Issabel Framework, the web framework supporting Issabel PBX software, before commit b97dbaf contains a hard-coded HS256 JWT signing key in the pbxapi index.php file that is identical across every installation, allowing unauthenticated remote attackers to forge valid bearer tokens. Attackers can use the forged token to call the manager originate endpoint with the System application parameter, causing Asterisk to execute arbitrary OS commands as the Asterisk user. Exploitation evidence was first observed by the Shadowserver Foundation on 2026-09-09.

### CVE-2024-58385

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-15T17:17:09.697 |

Yonyou U8 CRM contains an unauthenticated SQL injection vulnerability in the fillbacksettingedit.php configuration endpoint where the DontCheckLogin=1 parameter bypasses authentication and the id parameter is incorporated into SQL queries without sanitization. Attackers can exploit this flaw to execute arbitrary SQL commands and, on Microsoft SQL Server deployments with xp_cmdshell enabled, write backdoor files and execute arbitrary operating system commands. Exploitation evidence was first observed by the Shadowserver Foundation on 2025-02-13.

### CVE-2023-54398

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-15T17:17:08.343 |

Yonyou U8 Cloud contains an unauthenticated Java deserialization vulnerability in the nc.impl.pub.filesystem.FileManageServlet component that allows remote unauthenticated attackers to execute arbitrary OS commands by sending a serialized payload via POST request. Attackers can exploit the doAction method, which passes raw HTTP request body data directly to ObjectInputStream.readObject() without filtering, to achieve remote code execution. Exploitation evidence was first observed by the Shadowserver Foundation on 2025-02-13.

### CVE-2026-39919

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-15T15:17:14.723 |

Ghostscript before 10.08.0 contains a heap-based buffer overflow vulnerability in the JPEG 2000 output adapter (base/sjpx_openjpeg.c) that allows attackers to cause memory corruption by supplying a crafted PDF containing a JPEG 2000 image with mismatched component subsampling factors. When image components declare different subsampling values, the non-samescale sub-byte-depth output path allocates a row buffer sized for packed output but writes a full byte per output column regardless of bit depth, overflowing the allocation and corrupting internal chunk-allocator metadata to achieve code execution.

### CVE-2026-73458

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-303` |
| Published | 2026-09-15T20:17:43.160 |

On affected platforms running Arista EOS with authenticated Bidirectional Forwarding Detection (BFD) sessions configured, a specially crafted packet can cause the BFD session(s) to go down. This may result in undesirable network changes because various routing protocols monitor status on BFD session(s).

### CVE-2026-69204

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-09-15T19:17:37.580 |

Http4s is a Scala interface for HTTP services. Prior to 0.23.35 and 1.0.0-M47, Ember HTTP/1.1 does not reject messages containing both Transfer-Encoding and Content-Length, so an intermediary and Ember can select different body framing rules. When ember-server is behind a keep-alive intermediary that forwards both headers and frames by Content-Length, an unauthenticated attacker can smuggle a second request, bypass intermediary access controls, poison caches, or cause a victim request to be joined to an attacker-controlled prefix. The shared response parser can also desynchronize an ember-client connection when a malicious or compromised upstream sends both headers. This issue is fixed in versions 0.23.35 and 1.0.0-M47.

### CVE-2026-91988

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-09-15T16:17:57.450 |

atomic-agents-stack before 1.1.0 accepts cleartext HTTP schemes in the HTTP MCP server-registry backend factory, allowing network man-in-the-middle attackers to rewrite catalog responses. Attackers can inject arbitrary command and argument values that are spawned as local subprocesses by MCPClientPool to achieve code execution on the agent host.

### CVE-2026-91949

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-15T16:17:48.653 |

FreeRDP server versions before 3.31.0 contain a protocol negotiation bypass vulnerability that allows unauthenticated attackers to establish RDSTLS connections despite server policy disabling them. Attackers can send incompatible protocol requests, receive negotiation failures, then complete TLS handshake and enter RDSTLS to bypass pre-authentication transport restrictions.

### CVE-2026-46495

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-15T15:17:15.493 |

OpenDJ is an LDAPv3 compliant directory service. Prior to 5.1.1, the JMX RMI connector in opendj-server-legacy/src/main/java/org/opends/server/protocols/jmx/RmiConnector.java processes attacker-controlled credential objects before authentication without a restrictive jmx.remote.rmi.server.credentials.filter.pattern, and RmiAuthenticator.authenticate in opendj-server-legacy/src/main/java/org/opends/server/protocols/jmx/RmiAuthenticator.java accepts an unconstrained Object array rather than a two-element String[]. When the JMX Connection Handler is enabled and its TCP listener is reachable, an unauthenticated remote attacker can submit a crafted serialized Java object and achieve code execution in the OpenDJ server process. The handler is disabled by default, and successful exploitation depends on the runtime classpath and Java version; remote code execution was demonstrated against OpenDJ 4.4.15 on JDK 11 with Jackson 2.12.6.1. This issue is fixed in 5.1.1.

### CVE-2026-81642

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Red` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-16T09:17:06.320 |

In NLnet Labs Unbound up to and including 1.26.0, a vulnerability was found in the DNSSEC validator that enables denial of service and possible remote code execution as a result of digesting DNSKEYs. A DNSKEY with an owner compression pointer to its own RDATA can overflow the digest buffer. Remote code execution is possible through attacker controlled data. An adversary can exploit the vulnerability by controlling a malicious zone and querying a vulnerable Unbound.

### CVE-2026-15638

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-327` |
| Published | 2026-09-16T00:17:02.600 |

An unauthenticated user with access to Secret Server could leverage a padding oracle to decrypt or encrypt data using one of the server's cryptographic keys. The key itself is not exposed.

### CVE-2026-87223

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:10.630 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 9.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-87217

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:19:09.983 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87214

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:09.660 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-87189

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:06.840 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows high privileged attacker with network access via Oracle Net to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-87176

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:19:05.403 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87175

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:19:05.297 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87173

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:19:05.073 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87170

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:19:04.747 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87129

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:59.933 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87128

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:59.820 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83268

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:39.180 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle BI Publisher.  While the vulnerability is in Oracle BI Publisher, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle BI Publisher. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83260

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:38.293 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Event Java PX).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows high privileged attacker with network access via T3, IIOP to compromise Oracle Agile PLM.  While the vulnerability is in Oracle Agile PLM, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Agile PLM. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83229

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:34.743 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Siebel Management Console).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Siebel CRM Deployment.  While the vulnerability is in Siebel CRM Deployment, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83202

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:31.763 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Deployment accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Deployment accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83201

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:31.640 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Deployment accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Deployment accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83197

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:31.167 |

Vulnerability in the Siebel Apps - Financial Services product of Oracle Siebel CRM (component: Financial Accounts).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel Apps - Financial Services.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel Apps - Financial Services accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Siebel Apps - Financial Services. CVSS 3.1 Base Score 9.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H).

### CVE-2026-83196

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:31.057 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Siebel CRM Deployment.  While the vulnerability is in Siebel CRM Deployment, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83154

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:26.193 |

Vulnerability in the Siebel CRM End User product of Oracle Siebel CRM (component: Open UI).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Siebel CRM End User.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM End User accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM End User accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83149

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:25.637 |

Vulnerability in Oracle Application Testing Suite.   The supported version that is affected is 13.3.0.1. Easily exploitable vulnerability allows low privileged attacker having Test Manager for Web Apps privilege with network access via HTTP to compromise Oracle Application Testing Suite.  While the vulnerability is in Oracle Application Testing Suite, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Application Testing Suite accessible data as well as  unauthorized update, insert or delete access to some of Oracle Application Testing Suite accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Application Testing Suite. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L).

### CVE-2026-83107

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:20.893 |

Vulnerability in the Oracle Forms product of Oracle Fusion Middleware (component: Forms Services, C/S, Charmode).  Supported versions that are affected are 12.2.1.19.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Forms.  While the vulnerability is in Oracle Forms, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Forms. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83104

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:18:20.553 |

Vulnerability in the Oracle Forms product of Oracle Fusion Middleware (component: Forms Services, C/S, Charmode).  Supported versions that are affected are 12.2.1.19.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Forms.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Forms accessible data as well as  unauthorized access to critical data or complete access to all Oracle Forms accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83103

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:20.440 |

Vulnerability in the Oracle Forms product of Oracle Fusion Middleware (component: Forms Services, C/S, Charmode).  Supported versions that are affected are 12.2.1.19.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Forms.  While the vulnerability is in Oracle Forms, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Forms. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83064

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:15.150 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83006

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:07.223 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83001

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:06.680 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-76675

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:49.320 |

A command injection vulnerability exists in the command line interface of EdgeConnect SD-WAN Gateways. Successful exploitation could allow an authenticated remote attacker with high privileges to execute arbitrary commands on the underlying operating system leading to complete system compromise.

### CVE-2026-73952

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:17:46.347 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Portlet Services).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Portal accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-73946

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:45.670 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-73944

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-15T20:17:45.457 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Access Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Access Manager accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-89022

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-15T17:17:33.360 |

BookStack before 26.05.5 contains an authentication bypass vulnerability in its social login implementation that allows unauthenticated attackers to sign in as arbitrary users by authenticating through a different social provider sharing the same driver_id namespace. Attackers can authenticate at one enabled social provider using a user ID that matches an account linked to a different social provider, bypassing credential verification entirely because the SocialAuthService::handleLoginCallback query ignores the driver column when retrieving linked account records.

### CVE-2026-46488

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-256;CWE-287;CWE-328;CWE-836` |
| Published | 2026-09-15T17:17:15.200 |

motionEye (mEye) is an online interface for a piece of software called "motion," which is a video surveillance program with motion detection. Prior to 0.44.0, motionEye accepts the client-controlled meye_username and meye_password_hash cookies as authentication material without server-side session validation. An unauthenticated attacker who knows a target username and corresponding hash can set the cookies manually or cause them to be loaded by submitting blank credentials through the switch-user authentication flow, after which the server authenticates the attacker as that user. The administrator username and password-hash value are stored in /etc/motioneye/motion.conf, which is globally readable by default, allowing a local shell user to obtain reusable administrator credential material. Successful impersonation can enable account lockout, password changes and persistence, data enumeration, data destruction, and data exfiltration. This issue is fixed in version 0.44.0.

### CVE-2026-63696

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-494` |
| Published | 2026-09-15T15:17:20.527 |

Dell SmartFabric OS10 Software, versions prior to 10.6.1.3, contains a Download of Code Without Integrity Check vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Code execution.

### CVE-2026-55158

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-15T15:17:18.593 |

Conflibot warns in advance when merging a pull request will cause conflicts in other open pull requests. Prior to 1.2.1, src/index.ts builds git checkout, git merge, and git format-patch commands by interpolating the attacker-controlled pull request head.ref value into strings passed to exec. In the documented pull_request_target configuration, an attacker can open a pull request, including from a fork, whose branch name contains shell metacharacters, and the workflow automatically interprets those characters as commands without maintainer interaction. The commands execute on a runner with base-repository secrets and a write-scoped GITHUB_TOKEN, allowing arbitrary command execution, secret or token exfiltration, unauthorized pushes, and other token abuse. The fixed implementations in src/index.ts and src/conflibot.ts use execFile or spawn argument arrays, and the v2 line also uses numeric pull-request refs rather than branch names. This issue is fixed in versions 1.2.1 and 2.0.0.

### CVE-2026-83105

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:20.667 |

Vulnerability in the Oracle Forms product of Oracle Fusion Middleware (component: Forms Services, C/S, Charmode).  Supported versions that are affected are 12.2.1.19.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Forms.  While the vulnerability is in Oracle Forms, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Forms. CVSS 3.1 Base Score 9.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-91932

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-15T16:17:44.030 |

Flowise before 3.1.4 contains a validation bypass vulnerability in MCP server configuration allowing authenticated attackers remote code execution through an unvalidated cwd parameter. Attackers can bypass path validation using clean filenames in the args array while controlling the working directory to execute malicious code.

### CVE-2026-91931

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-15T16:17:43.883 |

Flowise before 3.1.4 contains a remote code execution vulnerability in the Custom MCP node that allows authenticated attackers to execute arbitrary code by supplying npx package names in the mcpServerConfig parameter. Attackers can invoke npx with attacker-controlled npm packages to execute code on the Flowise server.

### CVE-2026-77972

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-15T16:17:24.290 |

Time-of-check Time-of-use (TOCTOU) Race Condition in Slab safeurl allows an attacker who controls a hostname's DNS responses to reach internal network destinations that validation rejected.

Validation returns a verdict and not the address it approved, so the HTTP clients the library ships receive the original hostname and resolve it a second time when the request is made. An attacker who controls the authoritative DNS for a name can answer the first lookup with a permitted address and the second with a blocked one, and the request then reaches a destination validation never approved. The same window opens without an attacker whenever a name legitimately resolves to different addresses across lookups, such as short record lifetimes or rotation between several addresses.

This issue affects safeurl: from 0.1.0 onward.

### CVE-2026-77866

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-636;CWE-918` |
| Published | 2026-09-15T16:17:24.117 |

Server-Side Request Forgery (SSRF) vulnerability in Slab safeurl allows an attacker who controls a validated URL to reach internal network destinations the library is configured to block.

Only IPv4 addresses are matched against the reserved ranges and the blocklist. Every other address is treated as matching nothing, so a destination that is rejected in its IPv4 form is accepted when written as an IPv6 address, IPv6 entries in the blocklist never match, and a host that resolves to no IPv4 address is accepted regardless of where it points. Deployments that rely on the allowlist instead are unaffected, because there an unmatched address is rejected.

This issue affects safeurl: from 0.1.0 onward.

### CVE-2024-14029

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:L/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-09-15T16:17:06.893 |

Tornado before 6.4.1 ignores duplicate Transfer-Encoding: chunked headers, treating requests as having no message body and parsing the chunked body as a subsequent request. Attackers can exploit this inconsistency when Tornado is deployed behind proxies to perform HTTP request smuggling, enabling access control bypass, cache poisoning, or connection desynchronization.

### CVE-2023-54397

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:L/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-09-15T16:17:05.777 |

Tornado before 6.3.3 contains an HTTP request smuggling vulnerability due to improper parsing of Content-Length headers accepting non-standard characters. Attackers can send crafted HTTP requests with these characters to bypass proxy validation and smuggle requests when deployed behind certain proxies.

### CVE-2026-61549

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269;CWE-862` |
| Published | 2026-09-15T15:17:20.110 |

Woodpecker is a CI/CD engine. From 1.0.0 until 3.16.0, pipeline/backend/kubernetes/backend_options.go defines backend_options.kubernetes.serviceAccountName, and the Kubernetes backend in pipeline/backend/kubernetes/pod.go copies that pipeline-step value directly into the pod specification without administrator authorization. Any user with Push permission on a connected repository can therefore run pipeline pods under an arbitrary ServiceAccount in the pipeline namespace and inherit that account's RBAC permissions. When a privileged ServiceAccount is reachable, the attacker can exfiltrate secrets such as database credentials, API keys, and TLS certificates and may take over the cluster. This issue is fixed in version 3.16.0.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-8462

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-16T11:17:11.327 |

SQL injection in ClickHouse-backed meter definitions in OpenMeter OpenMeter before v1.0.0-beta.228 on all platforms allows a remote unauthenticated attacker to access or modify metering event data, and potentially cause denial of service, via crafted user-controlled JSONPath values submitted to meters API.

### CVE-2026-73455

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-130` |
| Published | 2026-09-16T10:16:52.243 |

On affected platforms running Arista EOS with Open Shortest Path First version 3 (OSPFv3) configured, a specially crafted packet can cause the OSPFv3 agent to restart unexpectedly.

### CVE-2026-83304

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:43.307 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Analytics Web General).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  While the vulnerability is in Oracle Business Intelligence Enterprise Edition, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Business Intelligence Enterprise Edition accessible data as well as  unauthorized access to critical data or complete access to all Oracle Business Intelligence Enterprise Edition accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 8.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:L).

### CVE-2026-73173

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-16T13:18:05.733 |

Nozomi Networks Labs identified a CWE-306: Missing Authentication for Critical Function vulnerability in the edgserver management protocol of Advantech EKI-1242EIMS in firmware version V1.06.01 that allows a remote unauthenticated attacker to invoke critical device-management functions, including network reconfiguration, reboot, reset, and firmware upgrade, by sending crafted requests to TCP port 5058.

### CVE-2026-27559

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T08:16:38.827 |

A low-privileged remote attacker can exploit a command injection vulnerability in the /api/status/data endpoint by sending a crafted GET request with user credentials allowing execution of commands with root privileges on the device.

### CVE-2026-27558

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T08:16:38.673 |

A low-privileged remote attacker can exploit a command injection vulnerability in the /index.php/attached_devices_tab/ajax_remove_uploaded_iodd_files endpoint using operator credentials allowing execution of commands with root privileges on the device.

### CVE-2026-27556

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-09-16T08:16:38.370 |

A low-privileged remote attacker can exploit a local file inclusion vulnerability in the /index.php/ajax/save_iodd_parameters endpoint using a valid operator cookie allowing execution of arbitrary PHP code on the device.

### CVE-2026-27555

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-09-16T08:16:38.213 |

A low-privileged remote attacker can exploit a local file inclusion vulnerability in the /index.php/ajax/get_iodd_port_info endpoint using a valid user cookie allowing execution of arbitrary PHP code on the device.

### CVE-2026-27554

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T08:16:38.063 |

A low-privileged remote attacker can exploit a command injection vulnerability in the /index.php/ajax/save_iodd_parameters endpoint using operator credentials allowing execution of commands with root privileges on the device.

### CVE-2026-27551

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T08:16:37.640 |

A low-privileged remote attacker can exploit a command injection vulnerability in the /index.php/ajax/parameterManage endpoint using user credentials allowing execution of commands with root privileges on the device.

### CVE-2026-27550

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T08:16:37.487 |

A low-privileged remote attacker can exploit a command injection vulnerability in the Field_Shadow_Password class using operator credentials allowing execution of commands with root privileges on the device.

### CVE-2026-27549

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T08:16:37.333 |

A low-privileged remote attacker can exploit a command injection vulnerability in the /index.php/attached_devices_tab/do_upload endpoint using operator credentials allowing execution of commands with root privileges on the device.

### CVE-2026-27548

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T08:16:37.180 |

A low-privileged remote attacker can exploit a command injection vulnerability in the /index.php/ajax/get_iodd_port_info endpoint using user or operator credentials allowing execution of commands with root privileges on the device.

### CVE-2026-27547

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T08:16:37.027 |

A low-privileged remote attacker can exploit a command injection vulnerability in the /index.php/ajax/get_iodd_menu_info endpoint using valid user or operator credentials allowing execution of commands with root privileges on the device.

### CVE-2026-78088

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-16T04:18:41.503 |

The Contest Gallery – Upload & Vote Photos, Media, Sell with PayPal & Stripe plugin for WordPress is vulnerable to Unauthenticated Arbitrary File Overwrite in all versions up to, and including, 32.0.1 due to insufficient file path validation in the 'baseUrlForFacebook' parameter. This makes it possible for authenticated attackers, with subscriber-level access and above, to overwrite known files which may lead to remote code execution when certain preconditions are met.

### CVE-2026-85893

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-15T23:19:12.110 |

Use after free in Microsoft Edge (Chromium-based) allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-69486

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-15T23:17:41.633 |

Heap-based buffer overflow in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-91745

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-15T21:16:48.280 |

Use after free in V8 in Google Chrome prior to 153.0.8010.47 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-91741

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-15T21:16:47.770 |

Type confusion in CacheStorage in Google Chrome prior to 153.0.8010.47 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-91737

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-15T21:16:47.270 |

Use after free in PDF in Google Chrome prior to 153.0.8010.47 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-91736

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-15T21:16:47.147 |

Use after free in DOM in Google Chrome prior to 153.0.8010.47 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-91731

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-15T21:16:46.523 |

Type confusion in Compositing in Google Chrome prior to 153.0.8010.47 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-91722

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-15T21:16:45.333 |

Use after free in Input in Google Chrome prior to 153.0.8010.47 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-91721

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-15T21:16:45.180 |

Use after free in Internals in Google Chrome prior to 153.0.8010.47 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-91715

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-15T21:16:44.433 |

Type confusion in ServiceWorker in Google Chrome prior to 153.0.8010.47 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-91711

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-15T21:16:43.923 |

Out of bounds write in ServiceWorker in Google Chrome prior to 153.0.8010.47 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-91709

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-15T21:16:43.673 |

Type confusion in ServiceWorker in Google Chrome prior to 153.0.8010.47 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87238

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:12.477 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via SQL to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87227

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:11.060 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87226

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:10.950 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87224

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:10.737 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87204

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:08.557 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87202

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:08.337 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via SQL to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87201

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:08.227 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87187

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:06.617 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87185

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:06.400 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87182

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:06.067 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-87181

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:05.960 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87180

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:05.850 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87179

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:05.740 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87165

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:04.170 |

Vulnerability in the Oracle Contract Lifecycle Management for Public Sector product of Oracle E-Business Suite (component: ECC For Award and IDV).   The supported version that is affected is V16. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Contract Lifecycle Management for Public Sector.  Successful attacks of this vulnerability can result in takeover of Oracle Contract Lifecycle Management for Public Sector. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87163

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:03.947 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Other issue).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in takeover of Oracle Purchasing. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87162

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:03.823 |

Vulnerability in the Oracle Contract Lifecycle Management for Public Sector product of Oracle E-Business Suite (component: Award/PO).  Supported versions that are affected are 12.2.13-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Contract Lifecycle Management for Public Sector.  Successful attacks of this vulnerability can result in takeover of Oracle Contract Lifecycle Management for Public Sector. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87155

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:02.990 |

Vulnerability in the Oracle Product Hub product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Hub.  Successful attacks of this vulnerability can result in takeover of Oracle Product Hub. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87150

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:02.430 |

Vulnerability in the Oracle Bills of Material product of Oracle E-Business Suite (component: Setup Workbench).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Bills of Material.  Successful attacks of this vulnerability can result in takeover of Oracle Bills of Material. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83479

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:55.587 |

Vulnerability in the Oracle Contracts product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.14-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Contracts.  Successful attacks of this vulnerability can result in takeover of Oracle Contracts. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83456

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:54.387 |

Vulnerability in the Oracle Demand Signal Repository product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Demand Signal Repository.  Successful attacks of this vulnerability can result in takeover of Oracle Demand Signal Repository. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83454

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:54.167 |

Vulnerability in the Oracle Document Management and Collaboration product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Document Management and Collaboration.  Successful attacks of this vulnerability can result in takeover of Oracle Document Management and Collaboration. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83445

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:53.177 |

Vulnerability in the Oracle Complex Maintenance, Repair and Overhaul product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Complex Maintenance, Repair and Overhaul.  Successful attacks of this vulnerability can result in takeover of Oracle Complex Maintenance, Repair and Overhaul. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83444

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:53.067 |

Vulnerability in the Oracle Product Hub product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Hub.  Successful attacks of this vulnerability can result in takeover of Oracle Product Hub. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83423

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:50.907 |

Vulnerability in the Oracle JDeveloper product of Oracle Fusion Middleware (component: Security Framework).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle JDeveloper.  Successful attacks of this vulnerability can result in takeover of Oracle JDeveloper. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83411

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:49.470 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83410

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:49.350 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via multiple protocols to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83348

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:48.247 |

Vulnerability in the RDBMS component of Oracle Database Server.  Supported versions that are affected are 19.3-19.32, 21.3-21.23 and  23.4.0-23.26.3. Easily exploitable vulnerability allows low privileged attacker having Create DB Link privilege with network access via Oracle Net to compromise RDBMS.  Successful attacks of this vulnerability can result in takeover of RDBMS. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83340

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:47.360 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: Security).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83338

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:47.133 |

Vulnerability in the Oracle Applications Manager product of Oracle E-Business Suite (component: Oracle Diagnostics Interfaces).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Applications Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Applications Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83335

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:46.770 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Analytics Server).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83331

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:46.323 |

Vulnerability in the Oracle Applications Framework product of Oracle E-Business Suite (component: Personalization).  Supported versions that are affected are 12.2.9-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Applications Framework.  Successful attacks of this vulnerability can result in takeover of Oracle Applications Framework. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83329

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:46.100 |

Vulnerability in the Oracle Applications Framework product of Oracle E-Business Suite (component: Personalization).  Supported versions that are affected are 12.2.9-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Applications Framework.  Successful attacks of this vulnerability can result in takeover of Oracle Applications Framework. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83315

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:44.520 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via SOAP to compromise Oracle BI Publisher.  Successful attacks of this vulnerability can result in takeover of Oracle BI Publisher. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83306

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:43.530 |

Vulnerability in the Oracle JDeveloper product of Oracle Fusion Middleware (component: Resource Catalog Services).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle JDeveloper.  Successful attacks of this vulnerability can result in takeover of Oracle JDeveloper. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83301

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:42.980 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Service Administration UI).   The supported version that is affected is 12.2.1.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83271

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:39.517 |

Vulnerability in the RDBMS component of Oracle Database Server.  Supported versions that are affected are 19.3-19.32, 21.3-21.23 and  23.4.0-23.26.3. Easily exploitable vulnerability allows low privileged attacker having Execute on DBMS_REDEFINITION privilege with network access via Oracle Net to compromise RDBMS.  Successful attacks of this vulnerability can result in takeover of RDBMS. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83212

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:32.860 |

Vulnerability in the Siebel Apps - Self Service product of Oracle Siebel CRM (component: Helpdesk/Training).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel Apps - Self Service.  Successful attacks of this vulnerability can result in takeover of Siebel Apps - Self Service. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83210

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:32.640 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with network access via SQL to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83209

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:32.537 |

Vulnerability in the Siebel CRM Development product of Oracle Siebel CRM (component: Workflow).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Development.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Development. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83208

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:32.423 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Migration).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with network access via SQL to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83205

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:32.093 |

Vulnerability in the Oracle Applications Framework product of Oracle E-Business Suite (component: Personalization).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Applications Framework.  Successful attacks of this vulnerability can result in takeover of Oracle Applications Framework. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83199

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:31.390 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83194

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:30.830 |

Vulnerability in the Oracle Depot Repair product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.10-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Depot Repair.  Successful attacks of this vulnerability can result in takeover of Oracle Depot Repair. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83189

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:30.280 |

Vulnerability in the Oracle User Management product of Oracle E-Business Suite (component: Proxy User Delegation).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle User Management.  Successful attacks of this vulnerability can result in takeover of Oracle User Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83180

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:29.130 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83168

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:27.773 |

Vulnerability in the Oracle Applications Manager product of Oracle E-Business Suite (component: Oracle Diagnostics Interfaces).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Applications Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Applications Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83165

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:27.447 |

Vulnerability in the Oracle Customer Interaction History product of Oracle E-Business Suite (component: User Interface).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Customer Interaction History.  Successful attacks of this vulnerability can result in takeover of Oracle Customer Interaction History. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83164

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:27.340 |

Vulnerability in the Oracle Customer Interaction History product of Oracle E-Business Suite (component: Outcome-Result).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Customer Interaction History.  Successful attacks of this vulnerability can result in takeover of Oracle Customer Interaction History. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83163

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:27.230 |

Vulnerability in the Oracle Application Object Library product of Oracle E-Business Suite (component: Attachments / File Upload).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Application Object Library.  Successful attacks of this vulnerability can result in takeover of Oracle Application Object Library. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83160

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:26.893 |

Vulnerability in the RDBMS component of Oracle Database Server.  Supported versions that are affected are 23.4.0-23.26.3. Easily exploitable vulnerability allows low privileged attacker having Create Table privilege with network access via Oracle Net to compromise RDBMS.  Successful attacks of this vulnerability can result in takeover of RDBMS. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83153

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:26.087 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83148

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:25.527 |

Vulnerability in Oracle Application Testing Suite.   The supported version that is affected is 13.3.0.1. Easily exploitable vulnerability allows low privileged attacker having Test Manager for Web Apps privilege with network access via HTTP to compromise Oracle Application Testing Suite.  Successful attacks of this vulnerability can result in takeover of Oracle Application Testing Suite. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83137

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:24.413 |

Vulnerability in the Oracle Spares Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Spares Management.  Successful attacks of this vulnerability can result in takeover of Oracle Spares Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83136

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:24.303 |

Vulnerability in the Oracle Spares Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Spares Management.  Successful attacks of this vulnerability can result in takeover of Oracle Spares Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83125

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:22.940 |

Vulnerability in the Oracle Report Manager product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Report Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Report Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83124

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:22.833 |

Vulnerability in the Oracle Sales Online product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales Online.  Successful attacks of this vulnerability can result in takeover of Oracle Sales Online. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83122

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:22.600 |

Vulnerability in the Oracle Report Manager product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Report Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Report Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83121

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:22.490 |

Vulnerability in the Oracle Marketing product of Oracle E-Business Suite (component: Audience).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Marketing.  Successful attacks of this vulnerability can result in takeover of Oracle Marketing. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83120

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:22.377 |

Vulnerability in the Oracle Alert product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Alert.  Successful attacks of this vulnerability can result in takeover of Oracle Alert. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83119

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:22.260 |

Vulnerability in the Oracle User Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.6-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle User Management.  Successful attacks of this vulnerability can result in takeover of Oracle User Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83090

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:18.840 |

Vulnerability in the Oracle Spares Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Spares Management.  Successful attacks of this vulnerability can result in takeover of Oracle Spares Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83086

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:18.393 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.7. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83069

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:15.777 |

Vulnerability in the Oracle Fusion Middleware Control product of Oracle Fusion Middleware (component: Framework).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Fusion Middleware Control.  Successful attacks of this vulnerability can result in takeover of Oracle Fusion Middleware Control. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83053

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:13.890 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83033

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:11.613 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83032

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:11.500 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83017

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:08.563 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Report Distribution).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83013

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:08.047 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83009

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:07.553 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83008

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:07.443 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83005

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:07.117 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-76678

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:49.650 |

A vulnerability in the API endpoint of HPE Networking EdgeConnect SD-WAN Gateways could allow a low-privilege authenticated remote attacker to escalate privileges. Successful exploitation of this vulnerability may enable the attacker to execute arbitrary system commands with root privileges on the underlying operating system.

### CVE-2026-76677

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:49.540 |

A privilege escalation vulnerability exists in the API of EdgeConnect SD-WAN Gateways. Successful exploitation could allow a remote low-privileged authenticated user to achieve administrative privilege on the web-management interface leading to complete system compromise.

### CVE-2026-76676

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:49.433 |

Buffer overflow vulnerabilities exist in the underlying operating system of EdgeConnect SD-WAN Gateways that could allow an unauthenticated adjacent attacker to execute arbitrary code if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to execute arbitrary code as a privileged user on the underlying operating system leading to complete system compromise.

### CVE-2026-73959

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:47.100 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Composer).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-73949

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:46.023 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Portlet Services).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-73942

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:45.160 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71047

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:42.230 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70915

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:42.110 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-58710

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-15T19:17:32.453 |

In DecodeFilmGrainParams of film_grain_dec.cc, there is a possible out-of-bounds write due to a missing bounds check. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58683

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-787` |
| Published | 2026-09-15T19:17:31.700 |

In IP Multimedia Subsystem, there is a possible out-of-bounds write due to improper input validation. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-56997

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-15T19:17:30.323 |

In Av1DecodeFrameTag of vp9hwd_headers.cc, there is a possible out-of-bounds write due to a missing bounds check. This could lead to remote escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-56974

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-787` |
| Published | 2026-09-15T19:17:29.337 |

In Start of AudioRtpPayloadEncoderNode.cpp, there is a possible out-of-bounds write due to improper input validation. This could lead to remote code execution with no additional execution privileges needed. User interaction is needed for exploitation.

### CVE-2026-56942

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-15T19:17:28.357 |

In ReadTileInfo of vp9hwd_headers.cc, there is a possible out-of-bounds write due to a missing bounds check. This could lead to remote escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-56920

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-15T19:17:26.730 |

In s_decode_vui_param of fw_hevc_dec_header.c, there is a possible out-of-bounds write due to a logic error in the code. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-56882

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-15T19:17:24.057 |

In Cellular Modem, there is a possible information disclosure due to a logic error in the code. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55331

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-15T19:17:21.413 |

In IP Multimedia Subsystem, there is a possible out-of-bounds write due to an incorrect bounds check. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55318

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-09-15T19:17:21.217 |

In multiple locations, there is a possible use-after-free due to a race condition. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0200

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-09-15T19:17:15.133 |

In Cellular Modem, there is a possible out-of-bounds write due to a heap buffer overflow. This could lead to remote escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0171

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-15T19:17:14.057 |

In multiple locations, there is a possible out-of-bounds write due to a logic error in the code. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0170

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-15T19:17:13.960 |

In Vp9DecodeFrameTag of vp9hwd_headers.cc, there is a possible out-of-bounds write due to a missing bounds check. This could lead to remote escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0159

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-15T19:17:13.830 |

In Cellular Modem, there is a possible out-of-bounds write due to a missing bounds check. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-52484

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-15T18:17:22.010 |

An issue in MitraStar GPT-2742GX4X5v6-SV GL_g2.5_100XNT0b23_3 allows an authenticated attacker to execute arbitrary code via the /cgi-bin/device-management-utilities-internet.cgi component

### CVE-2026-44300

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-309` |
| Published | 2026-09-15T18:17:21.280 |

OpenCost provides cost monitoring for Kubernetes workloads and cloud costs. Prior to 1.121.0, the POST /serviceKey endpoint in pkg/costmodel/router.go allows a network client to invoke AddServiceKey without mandatory authentication and submit an arbitrary key form value that is written to the GCP service-account key.json file returned by GetGCPAuthSecretFilePath in core/pkg/env/core.go. The attacker controls the file contents but not the CONFIG_PATH-derived directory, the key.json filename, or the file mode. Replacing the credential contents can disrupt GCP cost collection or cause OpenCost to use attacker-selected credentials, and the wildcard Access-Control-Allow-Origin response permits browser-assisted requests when the service is reachable from a browser. This issue is fixed in version 1.121.0.

### CVE-2026-40058

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-15T18:17:20.913 |

CrowdStrike released a security update to address a vulnerability in the Falcon sensor for Windows. The vulnerability only exists when the Microsoft Office File Malicious Macro Removal Windows policy setting is enabled and customers remain protected through the Cloud Anti-malware for Microsoft Office Files settings.




An update is available immediately for versions 7.34 and above, 7.32 LTS, and 7.16 for Windows 7/2008 R2 systems. The Falcon sensor for Mac, Linux, and Legacy Systems are not affected. 




This vulnerability could expose an arbitrary file write to protected locations from an unprivileged context, potentially leading to local privilege escalation.




The CrowdStrike Laroux Malware Cleanup Tool, based off of the same feature in the CrowdStrike Falcon sensor for Windows, is also affected. An update for this tool is also available immediately.

### CVE-2026-12728

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T18:17:14.547 |

IBM MQ 9.1.0.0 through 9.1.0.37 LTS, 9.2.0.0 through 9.2.0.43 LTS, 9.3.0.0 through 9.3.0.41 LTS, 9.3.0.0 through 9.3.5.1 CD, 9.4.0.0 through 9.4.0.25 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 could allow an authenticated attacker to execute arbitrary code due to a deserialization of untrusted data.

### CVE-2026-59160

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-15T17:17:23.410 |

Yeger is a monorepo for npm packages maintained under the yeger scope. Prior to 2.8.9, the turbo-graph package starts its embedded Next.js server from packages/turbo-graph/src/index.ts on all interfaces, including 0.0.0.0:29312 by default, while the GET handler for /api/run in packages/turbo-graph-ui/app/api/run/route.ts has no authentication, authorization, CSRF protection, or task allowlist. The handler accepts the tasks, filter, and force query parameters, and buildResponseFromArgs passes attacker-selected task names to spawn() as Turbo CLI arguments. An adjacent-network attacker can execute any task defined in the victim repository's turbo.json with the privileges of the developer OS user, potentially exposing secrets, modifying files or infrastructure, or causing destructive availability effects. The use of an argument array prevents traditional shell metacharacter injection but does not prevent unauthorized execution of defined tasks. This issue is fixed in version 2.8.9.

### CVE-2026-19780

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-09-15T17:17:11.383 |

Koha Eval Code Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Koha. Authentication is required to exploit this vulnerability.

The specific flaw exists within the web service, which listens on TCP port 8081 by default. The issue results from the lack of proper validation of a user-supplied string before passing it to the eval function. An attacker can leverage this vulnerability to execute code in the context of the service account. Was ZDI-CAN-29165.

### CVE-2026-88616

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-15T15:17:24.887 |

An issue in RuoYi-Vue-Plus 6.0.0 allows a remote attacker to execute arbitrary code via the FlwTaskController.java component, and the FlwTaskServiceImpl.completeTask, CompleteExecuteComponent.process, Warm-Flow TaskService.skip, POST /workflow/task/completeTask components

### CVE-2026-92467

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-620` |
| Published | 2026-09-16T14:17:17.470 |

zlt2000 microservices-platform through 6.0.0 contains an unverified password change vulnerability in the PUT /users/password endpoint that allows authenticated users to change any account password by omitting the current password check. Attackers can supply an arbitrary user id in the request body and a new password to overwrite credentials of any non-administrator account without verification.

### CVE-2026-92466

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T14:17:17.313 |

zlt2000 microservices-platform through 6.0.0 contains a missing authorization vulnerability where the zlt.security.auth.urlPermission.enable flag defaults to false, disabling all permission checks after authentication. Authenticated users with no roles can access administrative APIs including user management, role assignment, and Elasticsearch index operations by bypassing the disabled authorization enforcement.

### CVE-2026-88817

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269;CWE-284` |
| Published | 2026-09-16T13:18:07.837 |

An authenticated, non-guest user of Curiosity Workspace could enroll themselves as an administrator and member of an existing access group without an invitation or approval.



It did not grant application-wide administrator privileges, and the vulnerability could not be used to obtain root access to the application or its underlying host.

### CVE-2026-73174

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-09-16T13:18:05.880 |

Nozomi Networks Labs identified a CWE-319: Cleartext Transmission of Sensitive Information vulnerability in the edgserver management protocol of Advantech EKI-1242EIMS in firmware version V1.06.01 that allows a network-adjacent passive observer to intercept management traffic and recover sensitive device identity and network metadata in cleartext.

### CVE-2026-40854

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-16T12:17:03.540 |

WNC T-Mobile 5G Box IDU router contains an authentication bypass vulnerability in the portal.cgi component. The session verification mechanism improperly validates the sessionid cookie by checking for the existence of a corresponding file in /tmp/login_user. An attacker can bypass authentication by using directory entries such as "." or ".." in the cookie, allowing unauthorized access to the administration panel.This issue has been fixed in firmware version 1.1.0.651412

### CVE-2026-86106

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-16T11:16:43.783 |

An unauthenticated actor with network access to the private HA interconnect may trigger sensitive HA peer functions without verification. This could result in elevated command execution on Edge units where HA is enabled.

### CVE-2026-73464

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-16T09:17:05.463 |

On affected platforms running Arista EOS with gRPC Network Management Interface (gNMI) enabled, a specially crafted request could allow a malicious authenticated client with gRPC Network Management Interface (gNMI) access to execute arbitrary code with root privileges on the switch.

### CVE-2026-92355

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-16T08:16:40.813 |

In affected versions of Octopus Server, a user with permission to modify non built-in external feeds could exploit a path traversal flaw to overwrite arbitrary files on the server, which in some configurations could lead to remote code execution.

### CVE-2026-88263

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-16T08:16:40.303 |

XikeStor Layer3 switches miss authentication for downloading configuration data. Unauthenticated attacker may retrieve the configuration data containing network configurations and passwords to operate the affected product improperly or to exploit the affected product as a jump host.

### CVE-2026-84408

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-782` |
| Published | 2026-09-16T08:16:40.060 |

QND contains an improper access control vulnerability in a named pipe, which may allow a local attacker who is logged in to a Windows PC where the affected product's client is installed to execute arbitrary commands with SYSTEM privileges.

### CVE-2026-76862

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-15T22:17:00.653 |

Netcore NR255-V version 1.5.130703 contains an os command argument injection vulnerability in the Nettools tcpdump launch paths, including ntools_start_set_cgi, ntools_tcpdump_start_set_cgi, exe_default, and ntools_proc components. Attackers can inject crafted arguments into these tcpdump launch routines to manipulate executed system commands on the device.

### CVE-2026-76861

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-15T22:17:00.480 |

Netcore NR255-V version 1.5.130703 contains a stack-based buffer overflow in ntools_tcpdump_start_set.cgi caused by an unsized sprintf call when processing form values. An attacker can submit crafted input to this cgi endpoint to overflow the stack buffer and potentially execute arbitrary code.

### CVE-2026-76860

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-15T22:17:00.307 |

Netcore NR255-V version 1.5.130703 contains a stack-based buffer overflow in wake_up_set.cgi caused by unbounded tokenization of MAC and ID input. Attackers can supply crafted MAC and ID values to the affected endpoint to overflow the stack buffer and corrupt program memory.

### CVE-2026-76852

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-354` |
| Published | 2026-09-15T22:16:58.887 |

Netcore NR268 firmware version 1.7.121109 has an improper integrity verification flaw in mtd_write allowing forged firmware authenticity checks. Attackers can exploit put_file.cgi and check_image_uuid.c to bypass firmware signature validation and load unauthorized firmware images.

### CVE-2026-92000

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-09-15T21:16:49.167 |

adm-zip versions 0.5.14 through 0.6.0 fail to apply zlib decompression output limits when ZIP entries declare zero uncompressed size. Attackers can craft malicious ZIP archives with highly compressible entries declaring zero size to exhaust memory and cause denial of service.

### CVE-2026-79994

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-15T21:16:42.913 |

The guest-to-host Unix-domain socket relay in Docker Sandboxes validates that a socket path is inside an authorized workspace, but later reconnects using the pathname. A malicious guest can replace an intermediate directory with a symlink between validation and connection, causing the host to connect to an arbitrary AF_UNIX socket outside the shared workspace. This can expose data or host-side capabilities provided by the targeted socket.

### CVE-2026-68950

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-15T21:16:42.580 |

The affected products use hard-coded credentials, which could allow an attacker to run the ftpd service as root, providing remote root file access where FTP is reachable.

### CVE-2026-68070

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-15T21:16:42.253 |

The affected products are missing authentication for a critical function, which could allow an attacker to run as root and pass received bytes directly to a system command.

### CVE-2026-87178

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:05.627 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows high privileged attacker with network access via SQL to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-87171

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:04.857 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-83310

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:43.967 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle BI Publisher.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle BI Publisher, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle BI Publisher accessible data as well as  unauthorized access to critical data or complete access to all Oracle BI Publisher accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-83145

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:25.187 |

Vulnerability in the Siebel Apps - Customer Order Management product of Oracle Siebel CRM (component: Order Management).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel Apps - Customer Order Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Siebel Apps - Customer Order Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel Apps - Customer Order Management accessible data as well as  unauthorized access to critical data or complete access to all Siebel Apps - Customer Order Management accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-83144

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:25.077 |

Vulnerability in the Siebel Apps - Customer Order Management product of Oracle Siebel CRM (component: Order Management).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel Apps - Customer Order Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Siebel Apps - Customer Order Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel Apps - Customer Order Management accessible data as well as  unauthorized access to critical data or complete access to all Siebel Apps - Customer Order Management accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-83135

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:24.190 |

Vulnerability in the Oracle iStore product of Oracle E-Business Suite (component: Shopping Cart).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iStore.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle iStore, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle iStore accessible data as well as  unauthorized access to critical data or complete access to all Oracle iStore accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-83025

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:10.473 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Identity Manager Connector.  While the vulnerability is in Oracle Identity Manager Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Identity Manager Connector accessible data as well as  unauthorized access to critical data or complete access to all Oracle Identity Manager Connector accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-73926

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:44.833 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Access Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Access Manager accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-69217

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-09-15T20:17:41.120 |

Http4s is a Scala interface for HTTP services. Prior to 0.23.35 and 1.0.0-M47, Ember’s HTTP/1.1 parser accepts differing duplicate Content-Length headers and uses the last value instead of rejecting the message. When an Ember server is behind a keep-alive intermediary that selects a different occurrence, an unauthenticated attacker can create CL.CL request smuggling that bypasses front-end controls, captures a later user’s headers, or poisons a cache. The shared client parser can also misframe responses from a malicious or compromised upstream when the client acts as a proxy for multiple downstream consumers. This issue is fixed in versions 0.23.35 and 1.0.0-M47.

### CVE-2026-69205

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-09-15T20:17:39.653 |

Http4s is a Scala interface for HTTP services. Prior to 0.23.35 and 1.0.0-M47, Ember’s HeaderP.parse uses a case-sensitive substring test for the Transfer-Encoding value and decodes header bytes with the platform default charset. Values such as Chunked are not recognized, values such as notchunked are incorrectly accepted, and Unicode case folding can turn a Kelvin-sign byte sequence into a match when UTF-8 is used. Intermediaries that apply RFC-compliant token and charset rules can therefore disagree with Ember’s Content-Length or zero-length framing, enabling TE.CL or TE.0 request smuggling, access-control bypass, cross-user request hijacking, and cache poisoning on the server path. Response smuggling through an ember-client gateway requires a malicious or compromised upstream. This issue is fixed in versions 0.23.35 and 1.0.0-M47.

### CVE-2026-82189

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-472;CWE-602` |
| Published | 2026-09-15T19:17:41.980 |

Joomla Extension - j2commerce.com - Any order can be marked Failed by anyone in J2Store 1.0.0-3.3.2, 4.0.0-4.0.22, 4.1.0-4.1.7 - Unauthenticated denial-of-service against the order pipeline: mass-failing pending orders to disrupt revenue and force manual reprocessing, or flipping already-fulfilled orders back to `FAILED` to cause operational confusion (unwarranted refunds/cancellations, customer-support load). Unlike the earlier confirmation-fraud issue, this required no correct payment amount or transaction data at all.

### CVE-2026-81568

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-15T19:17:41.073 |

Joomla Extension - j2commerce.com - Arbitrary file read via `task=download` in J2Store 1.0.0-3.3.2, 4.0.0-4.0.22, 4.1.0-4.1.7 - `J2StoreModelOrderdownloads::getFilePath()` built the on-disk path to a purchased digital download by concatenating the configured attachment folder with the product file's stored `product_file_save_name`, using only `JPath::clean()` (which normalises separators but does not resolve or reject `..` segments) and a plain `JFile::exists()` check — never confirming the resolved path stayed inside the configured attachment folder. If a product file's `product_file_save_name` ever contained a `../` traversal segment — most plausibly via the CSRF-forgeable admin product-file save actions described in Issue 1, but equally by any future integration or bug that writes that field — any customer holding a valid download `token`/`pid` pair for that product file could have the traversal resolve to a path outside the attachment folder and download any file readable by the web server (e.g. `configuration.php`).

### CVE-2026-81567

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-15T19:17:40.947 |

Joomla Extension - j2commerce.com - Unauthenticated blind SQL injection in the storefront product list in J2Store 1.0.0-3.3.2, 4.0.0-4.0.22, 4.1.0-4.1.7 - Unauthenticated, blind extraction of arbitrary database content (e.g. customer records, order data, stored credentials/tokens) via boolean- or time-based inference, reachable on any public storefront that exposes the standard product listing or product-tags filter.

### CVE-2026-54251

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-664` |
| Published | 2026-09-15T18:17:22.780 |

netty-incubator-codec-ohttp implements Oblivious HTTP (OHTTP) gateway and client functionality using Netty. Prior to 0.0.23.Final, the OHTTP gateway decryption path in codec-ohttp/src/main/java/io/netty/incubator/codec/ohttp/OHttpRequestResponseContext.java allocates a pooled direct ByteBuf for decrypted plaintext before the AEAD tag is verified. When an invalid tag causes decryptChunk() to throw CryptoException, OHttpRequestResponseContext.decodeChunk() does not release the ByteBuf because the allocation is not guarded by try/finally. Repeated invalid encrypted requests can therefore leak native off-heap memory until the gateway is unable to continue serving requests. This issue is fixed in version 0.0.23.Final.

### CVE-2026-58201

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-15T17:17:23.260 |

Lokka is a Model Context Protocol server for Microsoft 365, including Microsoft Graph and other services. Prior to 2.1.2, the Lokka-Microsoft tool in src/mcp/src/main.ts uses direct URL string concatenation to append the user-controlled path value to the management.azure.com base URL. A specially crafted path can alter URL authority parsing and cause an Azure Resource Manager bearer token to be sent to an unintended host. This issue is fixed in version 2.1.2.

### CVE-2026-18110

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-15T17:17:11.110 |

Concrete CMS 9 (9.0.0 through 9.5.2) does not perform an authorization check on the user selector autocomplete endpoint (/ccm/system/user/autocomplete), which backs the "Preview as User" panel and other user-selector components. The endpoint validates only a CSRF-style access token that is bound to the selector's display options rather than to the caller's identity or permissions, and that token is issued to anonymous visitors because the selector renders without an authorization check. Because an empty query resolves to a match-all filter, an unauthenticated attacker can submit an empty search and paginate the results to enumerate every backend account, disclosing the internal user ID, username, and email address of all administrative users, including the super-administrator (user ID 1). No password hashes or session material are disclosed The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 8.7 with vector CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N. Thanks thirtythree and YesWeHack for reporting.

### CVE-2026-91990

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-15T16:17:58.147 |

Tornado before 6.5.8 contains a memory amplification vulnerability in parse_multipart_form_data that splits multipart data before validating the max_parts limit. Attackers can send crafted multipart requests with many parts to create large transient lists, exhausting server memory and causing denial of service.

### CVE-2026-91989

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-15T16:17:58.010 |

atomic-agents-stack before 1.1.0 contains a path traversal vulnerability in the dashboard HTTP server that allows remote attackers to read arbitrary files by supplying directory traversal sequences in request paths. Attackers can bypass path containment checks by including '../' segments in requests to the DashboardHandler.do_GET endpoint to access files outside the intended agents_root directory.

### CVE-2026-91985

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-15T16:17:57.010 |

Vikunja before 2.6.0 fails to properly restrict access to the link-share hash field in single-share read endpoints, allowing read-only members to obtain the share's secret credential. Attackers can exchange the disclosed hash for a link-share JWT at the share's permission level to escalate privileges and perform unauthorized writes or administrative actions.

### CVE-2026-91973

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-09-15T16:17:54.230 |

Vikunja before 2.6.0 contains an authentication bypass vulnerability in CalDAV BasicAuth endpoints that lack rate limiting protection. Remote unauthenticated attackers can issue unbounded credential-guessing requests against /dav, /.well-known, and /feeds routes to bypass the instance's anti-brute-force controls and compromise password-only accounts.

### CVE-2026-91972

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-09-15T16:17:54.087 |

Vikunja versions before 2.6.0 fail to apply rate limiting to /api/v2 public authentication endpoints including login, register, password-reset, and OAuth token routes. Remote unauthenticated attackers can perform unbounded credential guessing, account enumeration, and password-reset flooding attacks without throttling restrictions.

### CVE-2026-91965

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-15T16:17:52.643 |

WWBN AVideo through 29.0 fails to enforce user-group restrictions in the plugin/Live/stats.json.php and plugin/Live/calendar.json.php endpoints. Unauthenticated attackers can retrieve restricted live transmission details including stream keys, titles, descriptions, owner information, and direct HLS playback URLs by accessing these endpoints.

### CVE-2026-91964

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-15T16:17:52.480 |

FreeRDP versions before 3.31.0 contain a heap-based buffer overflow in nego_send_negotiation_request when processing Server Redirection PDU messages with attacker-controlled LoadBalanceInfo fields. A malicious RDP server can trigger the overflow by sending an arbitrary-length field that gets written to a fixed 512-byte buffer without validation, causing client crashes or potential code execution when chained with memory disclosure.

### CVE-2026-91941

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T16:17:46.000 |

Crawl4AI before 0.9.3 contains an uncontrolled resource consumption vulnerability in PDFContentScrapingStrategy that allows untrusted clients to cause denial of service. Attackers can select the PDF scraping strategy in POST requests to download large remote PDFs without size or page limits, exhausting disk, CPU, and bandwidth on shared workers.

### CVE-2026-91940

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-15T16:17:45.460 |

crawl4ai before 0.9.3 contains an arbitrary file write vulnerability in PDFContentScrapingStrategy where the _filter_untrusted_fields function fails to validate untrusted configuration fields. Attackers can submit crafted config bodies with malicious image_save_dir paths to write attacker-controlled bytes into any directory accessible to the service account.

### CVE-2026-91937

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-09-15T16:17:45.170 |

Flowise before 3.1.4 fails to sanitize the overrideConfig.sessionId parameter before using it in MongoDB queries within the MongoDBMemory node. Unauthenticated attackers can submit MongoDB operator objects through the prediction API to read chat history records belonging to other users from the shared collection.

### CVE-2026-91935

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-15T16:17:44.867 |

Flowise before 3.1.4 fails to validate baseURL parameters in chat-model nodes, allowing authenticated users to redirect requests to arbitrary hosts. Attackers with chatflows:create or chatflows:update permissions can exfiltrate LLM provider API keys by redirecting requests to cloud metadata services or internal hosts.

### CVE-2026-91934

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-15T16:17:44.317 |

Flowise versions before 3.1.4 fail to validate file paths in the SQL Database Chain node when connecting to SQLite databases, allowing authenticated attackers to write arbitrary files. Attackers can write malicious SQLite databases to system directories or inject files into the web root to execute commands or perform stored XSS attacks.

### CVE-2026-87792

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-862` |
| Published | 2026-09-15T16:17:37.197 |

The "Design Scuole Italia" WordPress theme is affected by multiple Authorization Bypass vulnerabilities in the dsi_pdf_generator and dsi_csv_generator functions, allowing an unauthenticated attacker to access restricted "Circolare" content and registered users' data. An unauthenticated RSS feed at /circolare/feed/ further facilitates exploitation.

### CVE-2026-87791

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-15T16:17:37.060 |

A path traversal vulnerability exists in the reserved_file_check function of the functions.php file in the WordPress Design Scuole Italia theme. The vulnerability allows an unauthenticated attacker to download arbitrary files accessible by the web server process.

### CVE-2026-55887

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-15T16:17:16.667 |

MCP Gateway allows easy and secure running and deployment of MCP servers. From 0.21.0 until 0.42.2, Docker MCP Gateway YAML-unmarshalled the attacker-controlled io.docker.server.metadata OCI image label into the broad catalog.Server structure for direct docker:// references and catalog snapshot imports in pkg/oci/self_contained.go and pkg/workingset/workingset.go. Runtime-shaping fields including Volumes, User, and ExtraHosts were then appended to the docker run argument vector without an origin allowlist, allowing a malicious image author to request host filesystem or Docker socket mounts and UID 0 execution when a victim selected or pulled the image. This container-creation-time boundary bypass can execute arbitrary code on the host and is not prevented by no-new-privileges because no in-container privilege escalation is required. This issue is fixed in version 0.42.2.

### CVE-2026-89025

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-755` |
| Published | 2026-09-15T15:17:26.720 |

Hirschmann HiOS Switch Platform devices contain a denial-of-service vulnerability in the integrated web server due to missing validation of HTTP(S) content. A remote unauthenticated attacker can send a specially crafted HTTP(S) request to a specific endpoint that is processed incorrectly, causing the device to perform an unintended reboot and resulting in a temporary denial-of-service condition. This vulnerability has been addressed in versions 07.1.12, 08.7.10, 09.0.13, 09.3.03, 10.3.08, and 10.5.00.

### CVE-2026-73177

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-16T14:17:08.133 |

Nozomi Networks Labs identified a CWE-345: Insufficient Verification of Data Authenticity vulnerability in the firmware upgrade mechanism of the Advantech EKI-1242EIMS in firmware version V1.06.01. The device accepts firmware images through the authenticated web management interface without performing any cryptographic signature or certificate verification. An authenticated administrator-level attacker can install arbitrary modified firmware on the device, enabling full persistent compromise of the platform.

### CVE-2026-73176

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T13:18:06.163 |

Nozomi Networks Labs identified a CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability in the web management interface of Advantech EKI-1242IEIMS in firmware version V1.06.01 that allows a remote authenticated attacker to execute arbitrary OS commands as root via crafted request parameters.

### CVE-2026-73171

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-16T13:18:05.350 |

Nozomi Networks Labs identified a CWE-73: External Control of File Name or Path vulnerability in the backup-restore workflow of Advantech EKI-1242EIMS in firmware version V1.06.01 that allows a remote authenticated attacker to overwrite arbitrary files on the device filesystem by uploading a crafted backup archive through the web management interface.

### CVE-2026-73170

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-16T13:18:05.220 |

Nozomi Networks Labs identified a CWE-94: Improper Control of Generation of Code ('Code Injection') vulnerability in the Modbus CSV import workflow of Advantech EKI-1242EIMS in firmware version V1.06.01 that allows a remote authenticated attacker to execute arbitrary Lua code on the device via a crafted imported file.

### CVE-2026-73167

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T13:18:04.950 |

Nozomi Networks Labs identified a CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability in the web management interface of Advantech EKI-1242IEIMS in firmware version V1.06.01 that allows a remote authenticated attacker to execute arbitrary OS commands as root via crafted request parameters.

### CVE-2026-73166

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-16T13:18:04.823 |

Nozomi Networks Labs identified a CWE-94: Improper Control of Generation of Code ('Code Injection') vulnerability in the web management interface of Advantech EKI-1242IEIMS in firmware version V1.06.01 that allows a remote authenticated attacker to execute arbitrary code on the device, including OS commands as root.

### CVE-2026-73165

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T13:18:04.693 |

Nozomi Networks Labs identified a CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability in the web management interface of Advantech EKI-1242IEIMS in firmware version V1.06.01 that allows a remote authenticated attacker to execute arbitrary OS commands as root via crafted request parameters.

### CVE-2026-73164

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T13:18:04.543 |

Nozomi Networks Labs identified a CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability in the web management interface of Advantech EKI-1242IEIMS in firmware version V1.06.01 that allows a remote authenticated attacker to execute arbitrary OS commands as root via crafted request parameters.

### CVE-2026-73163

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T13:18:04.373 |

Nozomi Networks Labs identified a CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability in the web management interface of Advantech EKI-1242IEIMS in firmware version V1.06.01 that allows a remote authenticated attacker to execute arbitrary OS commands as root via crafted request parameters.

### CVE-2026-19535

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-16T13:17:20.510 |

Nozomi Networks Labs identified a CWE-352: Cross-Site Request Forgery (CSRF) vulnerability in the LuCI administrative web interface of Advantech EKI-1242IEIMS in firmware version V1.06.01 that allows a remote unauthenticated attacker to perform unauthorized state-changing requests on behalf of a logged-in administrator, enabling unauthorized access to privileged management functions.

### CVE-2026-73454

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-16T09:17:05.020 |

On affected platforms running Arista EOS with gRPC Network Security Interface (gNSI) Credentialz configured, a specially crafted request can cause unintended modifications to the target account's properties. This may result in the account being assigned elevated privileges or access beyond what an administrator intended.

### CVE-2026-76869

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-15T22:17:01.837 |

Netcore NR255-V version 1.5.130703 contains a stack-based buffer overflow in reboot_timer_set.cgi caused by improper sscanf token parsing. Attackers can exploit this flaw by submitting crafted input to the affected endpoint to corrupt stack memory.

### CVE-2026-76866

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-15T22:17:01.337 |

Netcore NR255-V firmware version 1.5.130703 builds root-run command lines from unquoted user-supplied DDNS input in DDNSset_cgi.c and related ddns_Proc.c components, enabling os command argument injection. Attackers can exploit the unsanitized parameters to inject additional command arguments executed with root privileges.

### CVE-2026-87273

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:16.023 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.16. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. CVSS 3.1 Base Score 8.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-83305

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:43.423 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle BI Publisher.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle BI Publisher accessible data as well as  unauthorized update, insert or delete access to some of Oracle BI Publisher accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle BI Publisher. CVSS 3.1 Base Score 8.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-83284

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:41.033 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Oracle BI Publisher.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle BI Publisher as well as  unauthorized update, insert or delete access to some of Oracle BI Publisher accessible data and  unauthorized read access to a subset of Oracle BI Publisher accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H).

### CVE-2026-83203

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:31.870 |

Vulnerability in the Siebel CRM End User product of Oracle Siebel CRM (component: Open UI).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM End User.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM End User accessible data as well as  unauthorized update, insert or delete access to some of Siebel CRM End User accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Siebel CRM End User. CVSS 3.1 Base Score 8.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-83093

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:19.203 |

Vulnerability in the Oracle Forms product of Oracle Fusion Middleware (component: Forms Services, C/S, Charmode).  Supported versions that are affected are 12.2.1.19.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Forms.  While the vulnerability is in Oracle Forms, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Forms accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83074

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:17.027 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via SSH to compromise Siebel CRM Cloud Applications.  While the vulnerability is in Siebel CRM Cloud Applications, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83023

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:10.243 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Identity Manager Connector.  While the vulnerability is in Oracle Identity Manager Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Identity Manager Connector accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-76679

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:49.767 |

Vulnerabilities in HPE Networking EdgeConnect SD-WAN Gateways could allow an unauthenticated adjacent attacker to conduct denial-of-service attacks. Successful exploitation could allow an attacker to crash the system, preventing it from rebooting without manual intervention and disrupting network operations.

### CVE-2026-73941

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:45.050 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Access Manager accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-81240

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-15T18:19:24.630 |

Dell Wyse Management Suite, versions prior to 2605.0.3.683, contain an Unrestricted Upload of File with Dangerous Type vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Remote execution.

### CVE-2026-81239

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-15T18:19:24.513 |

Dell Wyse Management Suite, versions prior to 2605.0.3.683, contain an Unrestricted Upload of File with Dangerous Type vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Remote execution.

### CVE-2026-81236

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-15T18:19:24.147 |

Dell Wyse Management Suite, versions prior to 2605.0.3.683, contain an Unrestricted Upload of File with Dangerous Type vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Remote execution.

### CVE-2026-55691

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-15T17:17:22.187 |

The EmbedVideo Extension is a MediaWiki extension which adds a parser function called #ev and various parser tags for embedding video clips from various video sharing services. Prior to 4.1.0, EmbedHtmlFormatter::toHtml in includes/EmbedService/EmbedHtmlFormatter.php passes the user-supplied class value directly to sprintf while constructing a figure element. A quote in the class value can terminate the class attribute and inject arbitrary HTML attributes or markup into the rendered page. A user able to edit a wiki page can store JavaScript that executes for visitors who render the affected content. This issue is fixed in version 4.1.0.

### CVE-2026-57586

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-15T15:17:19.270 |

CodeRAG is a lightweight semantic code search and distillation utility for AI coding agents. Prior to 1.3.1, the default agent-coderag sync flow in code_rag/entry/cli.py calls sync_dependencies for an indexed path, and code_rag/core/manager.py treats build.gradle or build.gradle.kts as sufficient to invoke _sync_gradle. _sync_gradle prefers a repository-controlled gradlew or gradlew.bat file and passes it directly to asyncio.create_subprocess_exec with the repository root as the working directory; validate_path in code_rag/core/utils.py constrains the directory location but does not validate the executable's content or integrity. A victim who indexes an attacker-controlled Gradle repository therefore executes attacker-supplied code with the victim's operating-system privileges, allowing disclosure, modification, persistence, or denial of service in the user environment. This issue is fixed in 1.3.1.

### CVE-2026-79708

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-16T07:16:37.440 |

GitLab has remediated an issue in GitLab EE affecting all versions from 19.0 before 19.1.8, 19.2 before 19.2.6, and 19.3 before 19.3.2 that, under certain conditions could have allowed an authenticated user with developer permissions to execute a policy test pipeline on projects within their group and access protected CI/CD variables restricted to higher-privileged roles, due to insufficient scope validation.

### CVE-2026-87177

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:05.513 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-87161

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:03.713 |

Vulnerability in the Oracle HRMS (India) product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle HRMS (India).  While the vulnerability is in Oracle HRMS (India), attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle HRMS (India) accessible data as well as  unauthorized update, insert or delete access to some of Oracle HRMS (India) accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-83490

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:56.817 |

Vulnerability in the Oracle iRecruitment product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iRecruitment.  While the vulnerability is in Oracle iRecruitment, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle iRecruitment accessible data as well as  unauthorized update, insert or delete access to some of Oracle iRecruitment accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-83451

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:53.837 |

Vulnerability in the Oracle Product Workbench product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Workbench.  While the vulnerability is in Oracle Product Workbench, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Product Workbench. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83449

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:53.620 |

Vulnerability in the Oracle Bills of Material product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Bills of Material.  While the vulnerability is in Oracle Bills of Material, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Bills of Material accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Bills of Material. CVSS 3.1 Base Score 8.5 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L).

### CVE-2026-83425

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:51.133 |

Vulnerability in the Oracle Complex Maintenance, Repair and Overhaul product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.12-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Complex Maintenance, Repair and Overhaul.  While the vulnerability is in Oracle Complex Maintenance, Repair and Overhaul, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Complex Maintenance, Repair and Overhaul accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Complex Maintenance, Repair and Overhaul. CVSS 3.1 Base Score 8.5 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L).

### CVE-2026-83321

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:45.200 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Analytics Actions).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  While the vulnerability is in Oracle Business Intelligence Enterprise Edition, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Business Intelligence Enterprise Edition accessible data as well as  unauthorized update, insert or delete access to some of Oracle Business Intelligence Enterprise Edition accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-83311

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:44.080 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via SOAP to compromise Oracle BI Publisher.  While the vulnerability is in Oracle BI Publisher, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle BI Publisher accessible data as well as  unauthorized update, insert or delete access to some of Oracle BI Publisher accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-83309

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:43.857 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: Web Server).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle BI Publisher.  While the vulnerability is in Oracle BI Publisher, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle BI Publisher accessible data as well as  unauthorized update, insert or delete access to some of Oracle BI Publisher accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-83303

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:43.193 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via SOAP to compromise Oracle BI Publisher.  While the vulnerability is in Oracle BI Publisher, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle BI Publisher accessible data as well as  unauthorized read access to a subset of Oracle BI Publisher accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N).

### CVE-2026-83302

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:43.090 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Publisher Security).   The supported version that is affected is 12.2.1.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle BI Publisher.  While the vulnerability is in Oracle BI Publisher, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle BI Publisher accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle BI Publisher. CVSS 3.1 Base Score 8.5 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L).

### CVE-2026-83272

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:39.640 |

Vulnerability in the Oracle Text component of Oracle Database Server.  Supported versions that are affected are 19.3-19.32, 21.3-21.23 and  23.4.0-23.26.3. Difficult to exploit vulnerability allows low privileged attacker having Create Index privilege with network access via Oracle Net to compromise Oracle Text.  While the vulnerability is in Oracle Text, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Text. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83267

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:39.063 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Publisher Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle BI Publisher.  While the vulnerability is in Oracle BI Publisher, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle BI Publisher accessible data as well as  unauthorized update, insert or delete access to some of Oracle BI Publisher accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-83172

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:28.210 |

Vulnerability in the Oracle Sales Online product of Oracle E-Business Suite (component: OSO Other).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales Online.  While the vulnerability is in Oracle Sales Online, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Sales Online accessible data as well as  unauthorized update, insert or delete access to some of Oracle Sales Online accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-83083

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:18.067 |

Vulnerability in the Oracle Marketing product of Oracle E-Business Suite (component: Audience).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Marketing.  While the vulnerability is in Oracle Marketing, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Marketing accessible data as well as  unauthorized update, insert or delete access to some of Oracle Marketing accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-83049

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:13.427 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Security Framework).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-83045

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:12.973 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-83007

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:07.330 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Enterprise Capture accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Enterprise Capture accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-83003

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:06.897 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via SOAP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Enterprise Capture accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Enterprise Capture accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-83002

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:06.790 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-82993

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:05.790 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Business Interlink).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  While the vulnerability is in PeopleSoft Enterprise PeopleTools, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PeopleTools accessible data as well as  unauthorized update, insert or delete access to some of PeopleSoft Enterprise PeopleTools accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-76681

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:50.000 |

A vulnerability in the API of EdgeConnect SD-WAN Orchestrator could allow an authenticated remote attacker with low privileges to access sensitive information beyond what is authorized by the user's existing privilege level. Successful exploitation could allow an attacker to retrieve information which could be used to potentially gain further access to network services supported by EdgeConnect SD-WAN Orchestrator.

### CVE-2026-76680

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:49.890 |

Vulnerabilities in the API of EdgeConnect SD-WAN Orchestrator could allow a remote attacker authenticated with low privileges to conduct server-side request forgery (SSRF) attacks. A successful exploit allows an attacker to enumerate information about the internal structure of the EdgeConnect SD-WAN Orchestrator host leading to potential disclosure of sensitive information beyond what is authorized by the user's existing privilege level.

### CVE-2026-88765

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-15T18:19:36.203 |

GitLab has remediated an issue in GitLab EE affecting all versions from 12.3 to 19.1.8, 19.2 before 19.2.6, and 19.3 before 19.3.2 under certain conditions could allow an authenticated user to achieve remote code execution by importing a specially crafted Git project export to overflow the Unicode conversion buffer used in Advanced Search indexing.

### CVE-2026-11729

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-15T18:17:12.393 |

IBM MQ 9.1.0.0 through 9.1.0.37 LTS, 9.2.0.0 through 9.2.0.43 LTS, 9.3.0.0 through 9.3.0.41 LTS, 9.3.0.0 through 9.3.5.1 CD, 9.4.0.0 through 9.4.0.25 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 could allow an authenticated attacker to execute arbitrary code in client applications due to unsafe deserialization that enables JNDI injection attacks.

### CVE-2026-81895

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-15T17:17:27.710 |

In Concrete CMS before 9.5.3, the Document Library block stored the file-set identifiers submitted through fsID[] without validating them as integers, and when the block was configured with setMode set to any it concatenated each stored identifier directly into the file-set filter query instead of casting it or binding it as a parameter. An authenticated user permitted to add or edit a Document Library block could therefore persist SQL syntax in the block configuration (btDocumentLibrary.setIds), and that stored expression was executed every time the published page containing the block was rendered, producing stored, time-based blind SQL injection. The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 8.5 with vector CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N. Thanks Habib Allah for reporting.

### CVE-2026-81894

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-15T17:17:27.543 |

Concrete CMS 9.5.2 and below is vulnerable to stored DOM-based Cross-site Scripting (XSS) via the Gallery block's per-image Caption field because the bundled Magnific Popup lightbox script (concrete/js/features/imagery/frontend.js) re-parses the attribute-decoded caption as HTML through jQuery's .append() in titleSrc instead of inserting it as text. A user with permission to edit a page containing a Gallery block can store a caption that executes in the browser of any visitor who opens that image's lightbox. The Concrete CMS security team gave this vulnerability a CVSS v.4.0 score of 8.5 with vector CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N. Thanks Yonatan Drori (Tenzai) for reporting.

### CVE-2026-18111

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-15T17:17:11.247 |

Concrete CMS 9 before 9.5.3 was vulnerable to stored cross-site scripting (XSS) in the Feature, Feature Link, Hero Image, and Image blocks and before Concrete 8.5.21 in the feature and Image blocks because the external link URL was insufficiently validated by the link filter and was rendered without output escaping. A user with page-editing permissions (such as Add Block combined with Edit Contents on a single page) could store a crafted external link value that broke out of the link markup and injected arbitrary JavaScript. The script executed in the browser session of any user who subsequently viewed, previewed, or edited the affected page, which could lead to session hijacking and escalation of privileges up to full administrative takeover. The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 8.5 with vector CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N. Thanks to KhanMarshai for reporting this issue.

### CVE-2026-59973

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-15T16:17:18.327 |

FrontMCP is a TypeScript-first framework for the Model Context Protocol (MCP). From mcp-from-openapi 2.3.0 until 2.5.0 and from frontmcp and @frontmcp/adapters 1.2.1 until 1.5.0, libs/adapters/src/openapi/openapi.adapter.ts loadOpenAPISpec() forwards untrusted OpenAPI url and spec inputs and loadOptions.refResolution to OpenAPIToolGenerator.fromURL() and OpenAPIToolGenerator.fromJSON(). The external $ref guard checks parsed hostname strings without resolving addresses, pinning validated addresses, revalidating redirect targets, or normalizing IPv4-mapped IPv6. An authenticated user who can import or configure an OpenAPI specification in a hosted or multi-user deployment can use DNS-to-loopback resolution, redirect-to-loopback behavior, or IPv4-mapped IPv6 loopback forms to cause backend-origin requests to internal services. This can expose internal administrative APIs, metadata-like services, and other private network endpoints. The practical impact is lower when only a trusted local administrator can configure OpenAPI specs, and disabling external reference protocols prevents the external $ref request. This issue is fixed in mcp-from-openapi 2.5.0 and frontmcp and @frontmcp/adapters 1.5.0.

### CVE-2026-40857

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-16T12:17:03.910 |

WNC T-Mobile 5G Box IDU router contains a cross-site request forgery (CSRF) vulnerability in the portal.cgi component. The anti-CSRF mechanism fails to validate the csrf_token_value parameter, accepting any arbitrary value as valid. This allows a remote attacker to perform unauthorized actions on the device by tricking an authenticated user into visiting a malicious website.This issue has been fixed in firmware version 1.1.0.651412

### CVE-2026-82717

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-16T09:17:06.550 |

In NLnet Labs Unbound up to and including 1.26.0, a vulnerability was found in that can progressively corrupt heap memory and under certain systems and compilation options could lead to remote code execution. The vulnerability starts when CNAME synthesis during an upstream response needs to enforce(rewrite) a max TTL value in the packet buffer. Coupled with a compression pointer that points to the overwritten value and invalidates the domain name, it leads to an error path that does not properly move the buffer position and allows for the heap buffer overflow. Since this is heavily reliant on heap memory layout, results are memory corruption that eventually leads to a crash and under specific systems and compilation options remote code execution.

### CVE-2026-87259

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:14.603 |

Vulnerability in the Oracle Agile Engineering Data Management product of Oracle Supply Chain (component: Engineering Communication Interface).   The supported version that is affected is 6.2.1. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Agile Engineering Data Management executes to compromise Oracle Agile Engineering Data Management.  While the vulnerability is in Oracle Agile Engineering Data Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Agile Engineering Data Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Agile Engineering Data Management accessible data. CVSS 3.1 Base Score 8.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-87219

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:10.200 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-83264

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:38.737 |

Vulnerability in the Oracle Product Lifecycle Analytics product of Oracle Supply Chain (component: Installation Issues).   The supported version that is affected is 3.6.1. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Product Lifecycle Analytics executes to compromise Oracle Product Lifecycle Analytics.  While the vulnerability is in Oracle Product Lifecycle Analytics, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Product Lifecycle Analytics accessible data as well as  unauthorized access to critical data or complete access to all Oracle Product Lifecycle Analytics accessible data. CVSS 3.1 Base Score 8.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-57441

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-41;CWE-178` |
| Published | 2026-09-15T18:17:25.467 |

MCPVault is a lightweight Model Context Protocol server for safe access to files in an Obsidian vault. Prior to 0.11.4, PathFilter in src/pathfilter.ts compiles restricted-directory patterns case-sensitively and compares paths without canonicalizing filesystem-equivalent segment names. On case-insensitive macOS and Windows filesystems, case variants of .git, .obsidian, or node_modules pass both isAllowed() and isAllowedForListing() even though the operating system opens the restricted directory, and Windows trailing dots or spaces provide the same bypass. An attacker who influences a path selected by an AI agent can use the bypass in read, write, move, search, or listing operations to expose or modify sensitive repository and Obsidian metadata. Vault-root .. containment is not affected. This issue is fixed in version 0.11.4.

### CVE-2026-81896

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-15T17:17:27.863 |

Concrete CMS before 9.5.3 does not apply HTML entity encoding to user-defined Form block question labels when rendering them as column headers in the Dashboard Form Submissions report (concrete/single_pages/dashboard/reports/forms/legacy.php). a rogue editor could store markup or script in a label that then executes in the browser of any administrator who opens the submissions report for the affected form, producing stored cross-site scripting in the Dashboard. The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 8.4 with vector CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N. Thanks Yonatan Drori from Tenzai for reporting.

### CVE-2026-91748

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-15T21:16:48.703 |

Race condition in Extensions in Google Chrome on on Mac prior to 153.0.8010.47 allowed a remote attacker who had compromised the renderer process and leveraged social engineering to potentially execute arbitrary code outside the sandbox via UI Interaction. (Chromium security severity: High)

### CVE-2026-91743

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-15T21:16:48.020 |

Race condition in Core in Google Chrome prior to 153.0.8010.47 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-91735

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-15T21:16:47.020 |

Incorrect authorization in WebUI in Google Chrome prior to 153.0.8010.47 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-91733

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-754` |
| Published | 2026-09-15T21:16:46.770 |

Improper state validation in Skia in Google Chrome prior to 153.0.8010.47 allowed a remote attacker who had compromised the renderer process to read memory outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-91724

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-15T21:16:45.597 |

Use after free in Input in Google Chrome prior to 153.0.8010.47 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-91712

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-15T21:16:44.043 |

Race condition in Extensions in Google Chrome on on Mac prior to 153.0.8010.47 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87210

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:09.220 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-87125

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:59.493 |

Vulnerability in the Oracle Financials for Asia/Pacific product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.8-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Financials for Asia/Pacific.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Financials for Asia/Pacific accessible data as well as  unauthorized access to critical data or complete access to all Oracle Financials for Asia/Pacific accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Financials for Asia/Pacific. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-83307

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:43.640 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle BI Publisher.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle BI Publisher accessible data as well as  unauthorized access to critical data or complete access to all Oracle BI Publisher accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle BI Publisher. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-83285

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:41.153 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: BI Search).   The supported version that is affected is 12.2.1.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Business Intelligence Enterprise Edition accessible data as well as  unauthorized access to critical data or complete access to all Oracle Business Intelligence Enterprise Edition accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-83030

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:11.207 |

Vulnerability in the Oracle Managed File Transfer product of Oracle Fusion Middleware (component: MFT Runtime Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle Managed File Transfer.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Managed File Transfer accessible data as well as  unauthorized read access to a subset of Oracle Managed File Transfer accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Managed File Transfer. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H).

### CVE-2026-83026

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:10.600 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Identity Manager Connector executes to compromise Oracle Identity Manager Connector.  While the vulnerability is in Oracle Identity Manager Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager Connector. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-54549

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-15T18:17:23.073 |

Meta Ads MCP is a Model Context Protocol (MCP) server that lets AI assistants run Meta Ads. Prior to version 1.0.115, the upload_ad_image tool in meta_ads_mcp/core/ads.py passes an attacker-controlled image_url to try_multiple_download_methods() in meta_ads_mcp/core/utils.py, where httpx.AsyncClient uses follow_redirects=True and performs HTTP requests without validating the scheme, host, or resolved IP address. In a streamable-http deployment, a network caller can use any non-empty authorization value because Meta credential validation occurs after the image download, then direct the server to loopback services, private-network addresses, cloud metadata endpoints, or redirect-chained internal targets. The resulting server-side request forgery can expose internal data, invoke state-changing internal services, or disrupt reachable services. This issue is fixed in version 1.0.115.

### CVE-2026-63443

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-863;CWE-918` |
| Published | 2026-09-15T17:17:23.567 |

Coder allows organizations to provision remote development environments via Terraform. Prior to 2.29.19, 2.32.9, 2.33.10, and 2.34.4, agentConn.apiClient() follows redirects while its custom transport accepts the host from the redirected request URL when the port is the workspace agent HTTP API port 4. An authenticated user who controls a modified workspace agent and knows another online agent's UUID can derive the victim's tailnet address and redirect control-plane requests to that agent. HTTP 301, 302, and 303 redirects can redirect read requests, while HTTP 307 and 308 preserve replayable write and process-start requests. The redirected workspace agent file APIs can read or write files as the victim workspace user, and affected versions exposing the workspace agent process API can execute commands after a redirected file write, crossing workspace and tenant boundaries. This issue is fixed in versions 2.29.19, 2.32.9, 2.33.10, and 2.34.4.

### CVE-2026-91943

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-15T16:17:46.290 |

Crawl4AI before 0.9.3 contains a server-side request forgery vulnerability in PDFContentScrapingStrategy where _get_pdf_path() re-downloads targets with Python requests without egress validation. Authenticated attackers can supply URLs that redirect to internal addresses or use DNS rebinding to access internal services, exfiltrating responses through PDF text extraction in crawl results.

### CVE-2026-91936

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-15T16:17:45.013 |

Flowise versions before 3.1.4 contain a script injection vulnerability in Docker image build workflows where workflow_dispatch inputs are directly interpolated into shell run blocks. Attackers with repository write access can inject shell metacharacters through inputs like tag_version and node_version to execute arbitrary commands and steal AWS credentials and Docker Hub tokens.

### CVE-2026-89028

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-09-16T14:17:12.887 |

MikroTik RouterOS before 7.24 contains a heap memory corruption vulnerability in the userspace SMB daemon that allows remote attackers to corrupt adjacent heap memory by supplying a crafted uniPwdLen value in the SMB1 SessionSetupAndX handler. An attacker can send a malformed SMB1 request with a uniPwdLen field that triggers an integer underflow, causing the resulting value to be used as the copy length in a memory copy operation into a smaller heap buffer, corrupting adjacent heap memory.

### CVE-2026-86107

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-16T11:16:43.920 |

The VeloCloud Edge and Gateway exhibit an out-of-bounds write vulnerability when processing tunneled IP fragments between authenticated overlay neighbors. This vulnerability impacts the VeloCloud VCMP tunnel protocol only.

A successful exploit can cause the affected process to terminate and restart, leading to a temporary disruption of traffic. Hosts on the internet that are unauthenticated and unable to form an overlay peer relationship can not trigger the vulnerable logic.

### CVE-2026-78252

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-16T07:16:37.323 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 15.3 before 19.1.8, 19.2 before 19.2.6, and 19.3 before 19.3.2 that, under certain conditions, an authenticated user could have induced a targeted user to perform unintended state-changing HTTP requests due to improper sanitization of user-controlled data in the Markdown JSON table renderer.

### CVE-2026-87266

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:15.260 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Application Server).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Agile PLM accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Agile PLM. CVSS 3.1 Base Score 8.2 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-87229

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:11.310 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized read access to a subset of Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N).

### CVE-2026-87228

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:11.170 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-87200

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:08.113 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.2 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L).

### CVE-2026-87197

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:07.777 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-87196

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:07.660 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-87174

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:05.187 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-83465

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:55.363 |

Vulnerability in the Oracle Mobile Application Server product of Oracle E-Business Suite (component: MWA Terminal Server).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Mobile Application Server.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Mobile Application Server, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Mobile Application Server as well as  unauthorized update, insert or delete access to some of Oracle Mobile Application Server accessible data. CVSS 3.1 Base Score 8.2 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:L/A:H).

### CVE-2026-83461

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:54.927 |

Vulnerability in the Oracle Mobile Application Server product of Oracle E-Business Suite (component: MWA Terminal Server).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Mobile Application Server.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Mobile Application Server accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Mobile Application Server. CVSS 3.1 Base Score 8.2 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-83438

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:52.410 |

Vulnerability in the Oracle Engineering product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Engineering.  While the vulnerability is in Oracle Engineering, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Engineering accessible data as well as  unauthorized access to critical data or complete access to all Oracle Engineering accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-83435

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:52.060 |

Vulnerability in the Oracle Bills of Material product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.13-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Bills of Material.  While the vulnerability is in Oracle Bills of Material, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Bills of Material accessible data as well as  unauthorized access to critical data or complete access to all Oracle Bills of Material accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-83418

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:50.237 |

Vulnerability in the Oracle Communications Cloud Native Core Security Edge Protection Proxy product of Oracle Communications (component: SEPP).  Supported versions that are affected are 26.1.200 and  25.2.201. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Communications Cloud Native Core Security Edge Protection Proxy.  While the vulnerability is in Oracle Communications Cloud Native Core Security Edge Protection Proxy, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Communications Cloud Native Core Security Edge Protection Proxy accessible data as well as  unauthorized access to critical data or complete access to all Oracle Communications Cloud Native Core Security Edge Protection Proxy accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-83343

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:47.690 |

Vulnerability in the Oracle Utilities Network Management System product of Oracle Utilities Applications (component: System Wide).  Supported versions that are affected are 2.5.0.2.0-2.5.0.2.13, 2.6.0.1.0-2.6.0.12B, 2.6.0.2.0-2.6.0.2.10A and  25.12.0.0.0-25.12.0.0.3. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Utilities Network Management System.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Utilities Network Management System accessible data as well as  unauthorized update, insert or delete access to some of Oracle Utilities Network Management System accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-83266

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:38.957 |

Vulnerability in the Oracle JDeveloper product of Oracle Fusion Middleware (component: Resource Catalog Services).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle JDeveloper.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle JDeveloper accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle JDeveloper. CVSS 3.1 Base Score 8.2 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-83265

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:38.847 |

Vulnerability in the Oracle Web Services Manager product of Oracle Fusion Middleware (component: Web Services Agent).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Web Services Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Web Services Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Web Services Manager accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-83248

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:36.963 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager and  unauthorized read access to a subset of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H).

### CVE-2026-83236

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:35.580 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-83234

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:35.340 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-83215

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:33.183 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Deployment accessible data as well as  unauthorized update, insert or delete access to some of Siebel CRM Deployment accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-83181

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:29.247 |

Vulnerability in the Siebel CRM Development product of Oracle Siebel CRM (component: Workspaces).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Development.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Development accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Siebel CRM Development. CVSS 3.1 Base Score 8.2 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-83087

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:18.500 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.7. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  While the vulnerability is in Siebel CRM Cloud Applications, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Cloud Applications accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-83085

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:18.283 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.7. Easily exploitable vulnerability allows low privileged attacker with access to the physical communication segment attached to the hardware where the Siebel CRM Cloud Applications executes to compromise Siebel CRM Cloud Applications.  While the vulnerability is in Siebel CRM Cloud Applications, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data as well as  unauthorized update, insert or delete access to some of Siebel CRM Cloud Applications accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 8.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L).

### CVE-2026-83078

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:17.487 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data as well as  unauthorized update, insert or delete access to some of Siebel CRM Cloud Applications accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-83047

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:13.203 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-76682

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:50.117 |

A vulnerability in the network security monitoring component of intrusion detection systems could allow an unauthenticated remote attacker to exploit a limited buffer overflow. Successful exploitation could allow an attacker to cause a denial-of-service or potentially execute arbitrary code on the system.

### CVE-2026-61544

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-09-15T20:17:35.147 |

libp2p-rust is the official Rust language implementation of the libp2p networking stack. Prior to 0.13.1, libp2p-quic could panic during an inbound QUIC handshake when a remote peer presented a valid short-lived libp2p TLS certificate and delayed the final TLS 1.3 handshake fragment until after the certificate expired. In the Quinn post-handshake upgrade path, transports/quic/src/connection/connecting.rs called libp2p_tls::certificate::parse a second time in remote_peer_id and used expect on the result. The repeated wall-clock validity check could reject the now-expired certificate, causing the expect call to terminate any application exposing an affected libp2p-quic listener. This vulnerability is fixed in 0.13.1.

### CVE-2026-91992

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-15T16:17:58.447 |

Tornado before 6.5.7 contains a credential leak vulnerability in CurlAsyncHTTPClient where pycurl handles are reused across requests without proper state clearing. Attackers can obtain sensitive credentials by issuing requests through the same client instance, allowing TLS certificates or proxy authentication to persist across unintended requests.

### CVE-2026-91955

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-369` |
| Published | 2026-09-15T16:17:49.963 |

FreeRDP before 3.31.0 fails to validate client-supplied DesktopWidth and DesktopHeight values during GCC negotiation, allowing remote attackers to crash the server. Attackers can send crafted RDP packets with zero or oversized dimensions to trigger division-by-zero or assertion failures in multifragment update capability calculations, terminating the server process.

### CVE-2026-54167

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-15T15:17:17.707 |

Pipelines-as-Code is a CI/CD system that lets users define Tekton pipelines in source code repositories. Prior to 0.37.8, 0.39.6, 0.42.1, and 0.48.0, the GitHub App provider accepts X-GitHub-Enterprise-Host as the API host while processing webhook events containing an installation.id, before webhook signature validation or confirmation that the host matches the repository URL in the signed payload. An unauthenticated attacker who can reach the webhook endpoint can select an attacker-controlled host and cause the controller to send a locally signed GitHub App JWT to that service. The exposed JWT may be used to attempt to mint installation access tokens during its validity window, subject to the GitHub App installation and permissions. The incoming webhook installation-lookup path is also affected, but exploitation of that path requires the valid incoming webhook secret for the target Repository CR. This issue is fixed in versions 0.37.8, 0.39.6, 0.42.1, and 0.48.0.

### CVE-2026-27552

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-16T08:16:37.793 |

A low-privileged remote attacker can exploit improper authorization in the /index.php/attached_devices_tab/do_upload endpoint to upload IODD files to the device, potentially altering device behavior or causing system crashes.

### CVE-2026-83408

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T22:17:03.807 |

Vulnerability in the Oracle GraalVM for JDK, Oracle GraalVM product of Oracle Java SE (component: Compiler).   The supported version that is affected is Oracle GraalVM for JDK 17: 23.0.13.1; Oracle GraalVM for JDK 21: 23.1.12.1;  Oracle GraalVM: 25.0.4.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle GraalVM for JDK, Oracle GraalVM.  Successful attacks of this vulnerability can result in takeover of Oracle GraalVM for JDK, Oracle GraalVM. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83357

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T22:17:03.543 |

Vulnerability in the Oracle GraalVM for JDK, Oracle GraalVM product of Oracle Java SE (component: Compiler).   The supported version that is affected is Oracle GraalVM for JDK 17: 23.0.13.1; Oracle GraalVM for JDK 21: 23.1.12.1;  Oracle GraalVM: 25.0.4.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle GraalVM for JDK, Oracle GraalVM.  Successful attacks of this vulnerability can result in takeover of Oracle GraalVM for JDK, Oracle GraalVM. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-91727

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-09-15T21:16:45.980 |

Incorrect reference resolution in Extensions in Google Chrome on on Mac prior to 153.0.8010.47 allowed a local attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a local program. (Chromium security severity: High)

### CVE-2026-87288

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:18.790 |

Vulnerability in the Oracle GraalVM product of Oracle Java SE (component: Compiler).   The supported version that is affected is Oracle GraalVM: 25.0.4.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle GraalVM.  Successful attacks of this vulnerability can result in takeover of Oracle GraalVM. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87287

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:18.680 |

Vulnerability in the Oracle GraalVM product of Oracle Java SE (component: Compiler).   The supported version that is affected is Oracle GraalVM: 25.0.4.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle GraalVM.  Successful attacks of this vulnerability can result in takeover of Oracle GraalVM. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87286

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:18.560 |

Vulnerability in the Oracle GraalVM product of Oracle Java SE (component: Compiler).   The supported version that is affected is Oracle GraalVM: 25.0.4.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle GraalVM.  Successful attacks of this vulnerability can result in takeover of Oracle GraalVM. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87265

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:15.153 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Other issue).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Purchasing accessible data as well as  unauthorized access to critical data or complete access to all Oracle Purchasing accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87241

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:12.807 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87234

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:11.970 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87232

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:11.747 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87231

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:11.630 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87218

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:10.090 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-87168

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:04.503 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: G-Invoicing).  Supported versions that are affected are 12.2.10-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Purchasing accessible data as well as  unauthorized access to critical data or complete access to all Oracle Purchasing accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87167

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:04.390 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: G-Invoicing).  Supported versions that are affected are 12.2.11-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Purchasing accessible data as well as  unauthorized access to critical data or complete access to all Oracle Purchasing accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87166

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:04.280 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Other issue).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Purchasing accessible data as well as  unauthorized access to critical data or complete access to all Oracle Purchasing accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87159

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:03.447 |

Vulnerability in the Oracle HRMS (India) product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle HRMS (India).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle HRMS (India) accessible data as well as  unauthorized access to critical data or complete access to all Oracle HRMS (India) accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87157

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:03.207 |

Vulnerability in the Oracle Order Management product of Oracle E-Business Suite (component: Product Diagnostic Tools).  Supported versions that are affected are 12.2.4-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Order Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Order Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Order Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87154

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:02.883 |

Vulnerability in the Oracle Product Hub product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Hub.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Product Hub accessible data as well as  unauthorized access to critical data or complete access to all Oracle Product Hub accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87153

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:02.770 |

Vulnerability in the Oracle Product Hub product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Hub.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Product Hub accessible data as well as  unauthorized access to critical data or complete access to all Oracle Product Hub accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87152

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:02.660 |

Vulnerability in the Oracle Installed Base product of Oracle E-Business Suite (component: Create Item Instance).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Installed Base.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Installed Base accessible data as well as  unauthorized access to critical data or complete access to all Oracle Installed Base accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83477

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:55.473 |

Vulnerability in the Oracle Work in Process product of Oracle E-Business Suite (component: Workbenches).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Work in Process executes to compromise Oracle Work in Process.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Work in Process accessible data as well as  unauthorized access to critical data or complete access to all Oracle Work in Process accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83464

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:55.250 |

Vulnerability in the Oracle Mobile Application Server product of Oracle E-Business Suite (component: MWA Terminal Server).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Mobile Application Server.  Successful attacks of this vulnerability can result in takeover of Oracle Mobile Application Server. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83457

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:54.493 |

Vulnerability in the Oracle Demand Signal Repository product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Demand Signal Repository.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Demand Signal Repository accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Demand Signal Repository. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-83455

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:54.280 |

Vulnerability in the Oracle Demand Signal Repository product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Demand Signal Repository.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Demand Signal Repository accessible data as well as  unauthorized access to critical data or complete access to all Oracle Demand Signal Repository accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83448

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:53.507 |

Vulnerability in the Oracle Bills of Material product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Bills of Material.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Bills of Material accessible data as well as  unauthorized access to critical data or complete access to all Oracle Bills of Material accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83447

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:53.397 |

Vulnerability in the Oracle Bills of Material product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Bills of Material.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Bills of Material accessible data as well as  unauthorized access to critical data or complete access to all Oracle Bills of Material accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83446

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:53.287 |

Vulnerability in the Oracle Financials Common Modules product of Oracle E-Business Suite (component: Common Components).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Financials Common Modules.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Financials Common Modules accessible data as well as  unauthorized access to critical data or complete access to all Oracle Financials Common Modules accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83439

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:52.520 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: helidon-security-providers-idcs-mapper).  Supported versions that are affected are 3.0.0-3.2.20 and 4.0.0-4.5.4. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data as well as  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83434

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:51.927 |

Vulnerability in the Oracle Product Workbench product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Workbench.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Product Workbench accessible data as well as  unauthorized access to critical data or complete access to all Oracle Product Workbench accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83432

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:51.693 |

Vulnerability in the Oracle Depot Repair product of Oracle E-Business Suite (component: Estimate and Actual Charges).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Depot Repair.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Depot Repair accessible data as well as  unauthorized access to critical data or complete access to all Oracle Depot Repair accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83430

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:51.470 |

Vulnerability in the Oracle Product Workbench product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Workbench.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Product Workbench accessible data as well as  unauthorized access to critical data or complete access to all Oracle Product Workbench accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83429

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:51.357 |

Vulnerability in the Oracle Demand Signal Repository product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Demand Signal Repository.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Demand Signal Repository accessible data as well as  unauthorized access to critical data or complete access to all Oracle Demand Signal Repository accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83428

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:51.247 |

Vulnerability in the Oracle Demand Signal Repository product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Demand Signal Repository.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Demand Signal Repository accessible data as well as  unauthorized access to critical data or complete access to all Oracle Demand Signal Repository accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83422

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:50.623 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Identity Manager.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Identity Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Identity Manager accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N).

### CVE-2026-83412

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:49.583 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Coherence accessible data as well as  unauthorized access to critical data or complete access to all Oracle Coherence accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83351

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:48.580 |

Vulnerability in the RDBMS component of Oracle Database Server.  Supported versions that are affected are 23.4.0-23.26.3. Difficult to exploit vulnerability allows unauthenticated attacker with network access via Oracle Net to compromise RDBMS.  Successful attacks of this vulnerability can result in takeover of RDBMS. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83314

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:44.410 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: Web Service API).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via SOAP to compromise Oracle BI Publisher.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle BI Publisher accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle BI Publisher. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-83308

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:43.747 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via SOAP to compromise Oracle BI Publisher.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle BI Publisher accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle BI Publisher. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-83299

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:42.763 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Analytics Web General).   The supported version that is affected is 12.2.1.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83297

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:42.533 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle BI Publisher.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle BI Publisher accessible data as well as  unauthorized access to critical data or complete access to all Oracle BI Publisher accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83286

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:41.263 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83258

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:38.073 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83256

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:37.860 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83255

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:37.750 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83254

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:37.643 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83246

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:36.733 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83245

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:36.597 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83220

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:33.730 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: Event Publish and Subscribe).  Supported versions that are affected are 23.6-26.7. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Siebel CRM Integration executes to compromise Siebel CRM Integration.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Integration accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Integration accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83192

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:30.610 |

Vulnerability in the Siebel CRM End User product of Oracle Siebel CRM (component: Open UI).  Supported versions that are affected are 17.0-26.7. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM End User.  Successful attacks of this vulnerability can result in takeover of Siebel CRM End User. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83191

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:30.503 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TCP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83177

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:28.790 |

Vulnerability in the Oracle One-to-One Fulfillment product of Oracle E-Business Suite (component: Documents).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle One-to-One Fulfillment.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle One-to-One Fulfillment accessible data as well as  unauthorized access to critical data or complete access to all Oracle One-to-One Fulfillment accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83174

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:28.440 |

Vulnerability in the Oracle CRM Technical Foundation product of Oracle E-Business Suite (component: Application Framework).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle CRM Technical Foundation.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle CRM Technical Foundation accessible data as well as  unauthorized access to critical data or complete access to all Oracle CRM Technical Foundation accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83169

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:27.887 |

Vulnerability in the Oracle One-to-One Fulfillment product of Oracle E-Business Suite (component: Java Server Issues).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle One-to-One Fulfillment.  Successful attacks of this vulnerability can result in takeover of Oracle One-to-One Fulfillment. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83152

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:25.967 |

Vulnerability in the Oracle Project Intelligence product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Project Intelligence.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Project Intelligence accessible data as well as  unauthorized access to critical data or complete access to all Oracle Project Intelligence accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83143

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:24.963 |

Vulnerability in the Siebel Apps - Life Sciences product of Oracle Siebel CRM (component: eDetailing).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel Apps - Life Sciences.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel Apps - Life Sciences accessible data as well as  unauthorized access to critical data or complete access to all Siebel Apps - Life Sciences accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N).

### CVE-2026-83132

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:23.847 |

Vulnerability in the Oracle iStore product of Oracle E-Business Suite (component: Shopping Cart).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iStore.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle iStore accessible data as well as  unauthorized access to critical data or complete access to all Oracle iStore accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83101

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:20.223 |

Vulnerability in the Oracle Forms product of Oracle Fusion Middleware (component: Forms Services, C/S, Charmode).  Supported versions that are affected are 12.2.1.19.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Forms.  Successful attacks of this vulnerability can result in takeover of Oracle Forms. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83089

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:18.733 |

Vulnerability in the Oracle Alert product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Alert.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Alert accessible data as well as  unauthorized access to critical data or complete access to all Oracle Alert accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83073

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:16.247 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.7. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Siebel CRM Cloud Applications executes to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Cloud Applications accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83072

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:16.113 |

Vulnerability in the Oracle Applications Framework product of Oracle E-Business Suite (component: Search Bean [Incl.  Advanced]).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Applications Framework.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Applications Framework accessible data as well as  unauthorized access to critical data or complete access to all Oracle Applications Framework accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83067

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:15.550 |

Vulnerability in the Oracle JDeveloper product of Oracle Fusion Middleware (component: ADF Shared Components).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle JDeveloper.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle JDeveloper accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle JDeveloper. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-83019

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:08.837 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: SQR).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PeopleTools accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 8.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H).

### CVE-2026-83014

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:08.180 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Cube Manager).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise PeopleTools accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-83011

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:07.790 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Platform Security for Java.  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83010

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:07.670 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Enterprise Capture accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Enterprise Capture accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-76685

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:50.453 |

A vulnerability exists in the proxy packet processing logic of the affected component where it improperly processes malformed or truncated input. An unauthenticated remote attacker could exploit this vulnerability by providing specially crafted input that triggers an integer overflow. Successful exploitation could result in a buffer overflow, potentially leading to remote code execution or denial-of-service.

### CVE-2026-76684

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:50.340 |

Vulnerabilities have been identified in the API of HPE Networking EdgeConnect SD-WAN Orchestrator that could potentially allow an unauthenticated remote actor to circumvent existing authentication controls. Successful exploitation could allow an attacker to gain administrative privileges leading to complete compromise of the EdgeConnect SD-WAN Orchestrator host.

### CVE-2026-76683

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:50.227 |

Buffer overflow vulnerabilities exist in the API endpoint of HPE Networking EdgeConnect SD-WAN Gateways that could allow an unauthenticated remote attacker to run arbitrary commands on the underlying host if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to execute arbitrary commands on the underlying operating system leading to complete system compromise.

### CVE-2026-73958

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:46.993 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-73954

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:46.560 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Business Interlink).  Supported versions that are affected are 8.61-8.63. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-73951

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:46.240 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Portlet Services).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-79410

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-15T19:17:39.943 |

Improper validation of the quantity parameter in the add-to-cart path of Webkul Bagisto v2.4.9 allows authenticated attackers to reduce their order total below the legitimate price of shippable goods.

### CVE-2026-61668

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-15T18:17:27.217 |

DIRAC is an interware, meaning a software framework for distributed computing. Prior to versions 8.0.79, 9.0.22, and 9.1.10, WorkloadManagementSystem/Utilities/PilotWrapper.py pilotWrapperScript uses ssl._create_unverified_context to download the second-stage pilot.tar archive without TLS certificate verification and downloads the reference checksum through the same unvalidated channel. An attacker able to redirect or intercept a grid site's network traffic through DNS or routing manipulation can substitute both the executable pilot code and its checksum, causing arbitrary code to run in the pilot context with access to pilot proxy credentials. The fixed implementation validates the server certificate through system trust and X509_CERT_DIR or the grid certificate directory. This issue is fixed in versions 8.0.79, 9.0.22, and 9.1.10.

### CVE-2026-56829

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-15T18:17:24.957 |

Shopper is a Headless e-commerce Admin Panel. Prior to 2.9.2, packages/admin/src/Livewire/Components/Products/VariantStock.php exposes stockAction() without edit_product_variants authorization and leaves public $variant client mutable because it lacks the Livewire Locked attribute. Any authenticated admin-panel user, including staff with only browse_products, can select an arbitrary product variant and inventory location through component state, then submit a positive or negative quantity adjustment. This permits browse-only staff to inflate stock, reduce stock, or force out-of-stock states for variants outside the current page. This issue is fixed in version 2.9.2.

### CVE-2026-56827

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-15T18:17:24.823 |

Shopper is a Headless e-commerce Admin Panel. Prior to 2.9.2, groupedBulkActions in packages/admin/src/Livewire/Pages/Attribute/Browse.php, packages/admin/src/Livewire/Pages/Tag/Index.php, packages/admin/src/Livewire/Pages/Brand/Index.php, packages/admin/src/Livewire/Pages/Category/Index.php, and packages/admin/src/Livewire/Pages/Supplier/Index.php omit server-side authorization while the pages require only browse_attributes, browse_tags, browse_brands, browse_categories, or browse_suppliers. A browse-only staff user can invoke DeleteBulkAction to mass delete attributes or tags and can invoke BulkAction::make('enabled') or BulkAction::make('disabled') to change attribute, brand, category, or supplier visibility. These operations can break product variants and substantially disrupt storefront catalog visibility. Per-record actions and the comparison pages identified by the advisory are correctly authorized and are not affected. This issue is fixed in version 2.9.2.

### CVE-2026-56825

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-15T18:17:24.680 |

Shopper is a Headless e-commerce Admin Panel. Prior to 2.9.2, packages/admin/src/Livewire/Components/Collection/CollectionProducts.php exposes Action::make('delete') and DeleteBulkAction::make() without delete_collections authorization, while public Collection $collection remains client mutable because it lacks the Livewire Locked attribute. An authenticated staff user with only browse_collections can invoke a Livewire removal action, substitute an arbitrary collection identifier, and detach selected products or empty the collection. This can disrupt catalog landing pages and promotions associated with the targeted collection. This issue is fixed in version 2.9.2.

### CVE-2026-12666

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-15T18:17:14.290 |

IBM MQ 9.1.0.0 through 9.1.0.37 LTS, 9.2.0.0 through 9.2.0.43 LTS, 9.3.0.0 through 9.3.0.41 LTS, 9.3.0.0 through 9.3.5.1 CD, 9.4.0.0 through 9.4.0.25 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 Classes for Java could allow an authenticated attacker to obtain sensitive information or cause a denial of service due to XML external entity injection in MQRFH2 header processing.

### CVE-2026-12355

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-09-15T18:17:13.980 |

IBM MQ 9.1.0.0 through 9.1.0.37 LTS, 9.2.0.0 through 9.2.0.43 LTS, 9.3.0.0 through 9.3.0.41 LTS, 9.3.0.0 through 9.3.5.1 CD, 9.4.0.0 through 9.4.0.25 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 could allow an attacker to perform JNDI injection attacks due to insufficient input validation, potentially leading to information disclosure or remote code execution.

### CVE-2026-11728

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-15T18:17:12.257 |

IBM MQ 9.1.0.0 through 9.1.0.37 LTS, 9.2.0.0 through 9.2.0.43 LTS, 9.3.0.0 through 9.3.0.41 LTS, 9.3.0.0 through 9.3.5.1 CD, 9.4.0.0 through 9.4.0.25 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 could allow a remote attacker to cause a denial of service or potentially execute arbitrary code in the client due to a heap buffer overflow when receiving messages from a malicious queue manager or through a man-in-the-middle attack.

### CVE-2026-88619

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-15T16:17:38.933 |

1024-lab SmartAdmin v3.30.0 contains a missing authorization vulnerability in the scheduled-job management module. The AdminSmartJobController exposes scheduled-job management endpoints without method-level permission checks, allowing a low-privileged authenticated user to access functionality intended for authorized administrators.

### CVE-2026-54076

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862;CWE-863` |
| Published | 2026-09-15T16:17:13.560 |

ArcadeDB is a Multi-Model DBMS. Prior to 26.6.1, the fix for CVE-2026-44221 added an UPDATE_SCHEMA authorization check only to LocalDocumentType.createProperty, while the remaining public schema mutators in engine/src/main/java/com/arcadedb/schema/LocalDocumentType.java and engine/src/main/java/com/arcadedb/schema/LocalProperty.java remained unchecked. An authenticated identity, including a read-only API token without UPDATE_SCHEMA permission, can use DROP PROPERTY, ALTER TYPE, or ALTER PROPERTY through the database command/query HTTP endpoints to rename types, change inheritance, alter aliases or buckets, drop properties, and change property constraints. The issue does not directly disclose or write record data, but unauthorized schema mutation can corrupt the meaning of stored records and breach the documented permission model. This issue is fixed in version 26.6.1.

### CVE-2026-79425

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-15T15:17:21.947 |

An authenticated Server-Side Request Forgery (SSRF) in the /adminapi/file/online_upload component of CRMEB v6.0.0 allows attackers to scan internal resources via a crafted POST request.

### CVE-2026-87245

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:13.267 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with access to the physical communication segment attached to the hardware where the Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87243

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:13.033 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.0 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-87164

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:04.060 |

Vulnerability in the Oracle Banking Branch product of Oracle Financial Services Applications (component: Reports).  Supported versions that are affected are 14.5.0.0.0-14.9.0.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Banking Branch.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Banking Branch, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle Banking Branch. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-83483

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:56.030 |

Vulnerability in the Oracle Advanced Benefits product of Oracle E-Business Suite (component: Self-serv What-if Analysis).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Advanced Benefits.  While the vulnerability is in Oracle Advanced Benefits, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Advanced Benefits. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83450

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:53.730 |

Vulnerability in the Oracle Bills of Material product of Oracle E-Business Suite (component: Setup Workbench).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Bills of Material.  While the vulnerability is in Oracle Bills of Material, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Bills of Material. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83178

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:28.910 |

Vulnerability in the Oracle Application Object Library product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Application Object Library.  While the vulnerability is in Oracle Application Object Library, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Application Object Library. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83170

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:27.990 |

Vulnerability in the Oracle One-to-One Fulfillment product of Oracle E-Business Suite (component: Documents).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with access to the physical communication segment attached to the hardware where the Oracle One-to-One Fulfillment executes to compromise Oracle One-to-One Fulfillment.  Successful attacks of this vulnerability can result in takeover of Oracle One-to-One Fulfillment. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83157

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:26.553 |

Vulnerability in the Oracle Applications Manager product of Oracle E-Business Suite (component: Command Line - RapidClone).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Applications Manager.  While the vulnerability is in Oracle Applications Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Applications Manager. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83138

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:24.527 |

Vulnerability in the Oracle Spares Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Spares Management.  While the vulnerability is in Oracle Spares Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Spares Management. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83081

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:17.843 |

Vulnerability in the Oracle Banking Corporate Lending product of Oracle Financial Services Applications (component: Core).  Supported versions that are affected are 14.5.0.0.0-14.9.0.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Banking Corporate Lending executes to compromise Oracle Banking Corporate Lending.  While the vulnerability is in Oracle Banking Corporate Lending, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Banking Corporate Lending accessible data as well as  unauthorized access to critical data or complete access to all Oracle Banking Corporate Lending accessible data. CVSS 3.1 Base Score 8.0 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-58704

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285;CWE-693` |
| Published | 2026-09-15T19:17:32.297 |

In Cellular Modem, there is a possible permission bypass due to a logic error in the code. This could lead to remote (proximal/adjacent) escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-56967

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-15T19:17:28.950 |

In Cellular Modem, there is a possible out-of-bounds write due to a heap buffer overflow. This could lead to remote (proximal/adjacent) code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55343

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-15T19:17:21.600 |

In decodeAmr of ImsMediaAudioPlayer.cpp, there is a possible out-of-bounds write due to a missing bounds check. This could lead to remote code execution with no additional execution privileges needed. User interaction is needed for exploitation.

### CVE-2026-81235

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-325` |
| Published | 2026-09-15T18:19:24.023 |

Dell Wyse Management Suite, versions prior to 2605.0.3.683, contain a Missing Cryptographic Step vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Information tampering.

### CVE-2026-55225

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-441;CWE-250` |
| Published | 2026-09-15T18:17:23.667 |

Strimzi provides a way to run an Apache Kafka cluster on Kubernetes or OpenShift in various deployment configurations. In Strimzi 1.0.0 and earlier, an attacker who can create a Kafka custom resource can set Kafka.spec.entityOperator watchedNamespace to a target namespace, causing the Cluster Operator to create a Role with full Secret CRUD permissions there and bind it to the Entity Operator ServiceAccount in the attacker's namespace. The attacker can mint a token for that ServiceAccount and read or write Secrets in any target namespace where the Cluster Operator has been granted permissions, regardless of STRIMZI_NAMESPACE. This issue is fixed in versions 1.0.1 and 1.1.0.

### CVE-2026-83096

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:19.537 |

Vulnerability in the Oracle Forms product of Oracle Fusion Middleware (component: Forms Services, C/S, Charmode).  Supported versions that are affected are 12.2.1.19.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Forms.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Forms, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Forms accessible data as well as  unauthorized access to critical data or complete access to all Oracle Forms accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Forms. CVSS 3.1 Base Score 7.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:L).

### CVE-2026-83079

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:17.600 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.7. Easily exploitable vulnerability allows high privileged attacker with logon to the infrastructure where Siebel CRM Cloud Applications executes to compromise Siebel CRM Cloud Applications.  While the vulnerability is in Siebel CRM Cloud Applications, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Cloud Applications accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data. CVSS 3.1 Base Score 7.9 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-83022

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:10.120 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle WebCenter Enterprise Capture executes to compromise Oracle WebCenter Enterprise Capture.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 7.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-92248

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-15T22:17:04.190 |

A flaw was found in the file-psd plugin in GIMP. When generating a thumbnail preview for a specially crafted PSD (Photoshop Document) image file, an integer overflow occurs during the multiplication of values from an embedded JPEG header. This leads to an undersized heap allocation, resulting in a heap-based buffer overflow when the image data is decoded. This buffer overflow corrupts adjacent heap objects, allowing for a controlled memory write that can result in an application crash or arbitrary code execution.

### CVE-2026-87272

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:15.917 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.16. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87271

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:15.810 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.16. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. Note: This vulnerability applies to Windows host only. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87270

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:15.700 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.16. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. Note: This vulnerability applies to Windows host only. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87269

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:15.593 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.16. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. Note: This vulnerability applies to Windows host only. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87268

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:15.483 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.16. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. Note: This vulnerability applies to Windows host only. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87216

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:09.873 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83420

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:50.463 |

Vulnerability in the PeopleSoft Enterprise FIN Engineering Brazil product of Oracle PeopleSoft (component: Engineering).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where PeopleSoft Enterprise FIN Engineering Brazil executes to compromise PeopleSoft Enterprise FIN Engineering Brazil.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise FIN Engineering Brazil. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83353

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:48.800 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle WebCenter Content executes to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83342

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:47.580 |

Vulnerability in the Oracle Utilities Network Management System product of Oracle Utilities Applications (component: System Wide).  Supported versions that are affected are 2.4.0.1.0-2.4.0.1.33, 2.5.0.1.0-2.5.0.1.19, 2.5.0.2.0-2.5.0.2.13, 2.6.0.1.0-2.6.0.12B, 2.6.0.2.0-2.6.0.2.10A and  25.12.0.0.0-25.12.0.0.3. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Utilities Network Management System executes to compromise Oracle Utilities Network Management System.  Successful attacks of this vulnerability can result in takeover of Oracle Utilities Network Management System. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83337

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:47.023 |

Vulnerability in the Oracle Middleware Common Libraries and Tools product of Oracle Fusion Middleware (component: Remote Diagnostic Agent).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Middleware Common Libraries and Tools executes to compromise Oracle Middleware Common Libraries and Tools.  Successful attacks of this vulnerability can result in takeover of Oracle Middleware Common Libraries and Tools. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83336

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:46.897 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Analytics Server).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Business Intelligence Enterprise Edition executes to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83317

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:44.750 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Installation).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Business Intelligence Enterprise Edition executes to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83294

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:42.193 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Business Intelligence Enterprise Edition executes to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-83293

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:42.073 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: FNDN).   The supported version that is affected is 12.2.1.4.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Business Intelligence Enterprise Edition executes to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83291

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:41.843 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Business Intelligence Enterprise Edition executes to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83290

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:41.717 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Business Intelligence Enterprise Edition executes to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83288

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:41.487 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: BI Search).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Business Intelligence Enterprise Edition executes to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83253

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:37.533 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Commerce Guided Search / Oracle Commerce Experience Manager executes to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-83249

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:37.080 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Commerce Guided Search / Oracle Commerce Experience Manager executes to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  While the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-83247

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:36.853 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Commerce Guided Search / Oracle Commerce Experience Manager executes to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-83216

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:33.290 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Siebel CRM Deployment executes to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83214

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:33.073 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Siebel CRM Deployment executes to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83211

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:32.750 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Siebel CRM Deployment executes to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83159

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:26.783 |

Vulnerability in the Applications DBA product of Oracle E-Business Suite (component: ADPatch).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Applications DBA executes to compromise Applications DBA.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Applications DBA. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-83147

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:25.410 |

Vulnerability in the PeopleSoft Enterprise FIN Inventory Brazil product of Oracle PeopleSoft (component: Inventory).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where PeopleSoft Enterprise FIN Inventory Brazil executes to compromise PeopleSoft Enterprise FIN Inventory Brazil.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise FIN Inventory Brazil. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83118

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:22.157 |

Vulnerability in the Applications DBA product of Oracle E-Business Suite (component: AD Utilities).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Applications DBA executes to compromise Applications DBA.  Successful attacks of this vulnerability can result in takeover of Applications DBA. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83071

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:16.000 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Machine Learning).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Business Intelligence Enterprise Edition executes to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83024

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:10.360 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Identity Manager Connector executes to compromise Oracle Identity Manager Connector.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager Connector. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83018

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:08.700 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: SQR).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where PeopleSoft Enterprise PeopleTools executes to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-82996

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:06.127 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Platform Security for Java executes to compromise Oracle Platform Security for Java.  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-82992

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:05.677 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Installation).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Siebel CRM Deployment executes to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-92180

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-09-15T19:17:48.487 |

pdfforge PDF Architect activation-service Update Service Uncontrolled Search Path Element Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of pdfforge PDF Architect. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the activation-service process. The product loads a library from an unsecured location. An attacker can leverage this vulnerability to escalate privileges and execute code in the context of SYSTEM. Was ZDI-CAN-29536.

### CVE-2026-92179

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-15T19:17:48.367 |

pdfforge PDF Architect PDF File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of pdfforge PDF Architect. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of PDF files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29219.

### CVE-2026-92178

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-09-15T19:17:48.257 |

pdfforge PDF Architect PDF File Parsing Memory Corruption Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of pdfforge PDF Architect. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of PDF files. The issue results from the lack of proper validation of user-supplied data, which can result in a memory corruption condition. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28916.

### CVE-2026-92177

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-15T19:17:48.130 |

pdfforge PDF Architect PDF File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of pdfforge PDF Architect. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of PDF files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated object. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28673.

### CVE-2026-92176

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-15T19:17:47.993 |

pdfforge PDF Architect App Object Out-Of-Bounds Read Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of pdfforge PDF Architect. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the handling of App objects. The issue results from the lack of proper validation of user-supplied data, which can result in a read past the end of an allocated buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28570.

### CVE-2026-58766

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-15T19:17:33.927 |

In multiple functions of arm-smmu-v3.c, there is a possible escalation of privilege due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58744

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-15T19:17:33.440 |

In multiple locations, there is a possible escalation of privilege due to improper input validation. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58699

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-15T19:17:32.097 |

In Vp9DecEndOfStream of vp9hwd_output.cc, there is a possible out-of-bounds read due to an incorrect bounds check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58695

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-15T19:17:31.900 |

In gmc_phy_lp3_exit_restore_registers of phy_power.c, there is a possible escalation of privilege due to a missing bounds check. This could lead to local escalation of privilege with System execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58691

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-15T19:17:31.800 |

In FsmReleaseKey of fsm.c, there is a possible permission bypass due to improper input validation. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58679

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-15T19:17:31.600 |

In gf_ta_test_set_config of gf_ta_test.c, there is a possible heap buffer overflow due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58678

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-15T19:17:31.503 |

In Bootloader, there is a possible permission bypass due to a logic error in the code. This could lead to local escalation of privilege with System execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-57042

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-09-15T19:17:30.930 |

In multiple functions of DreamPickerReceiver.kt, there is a possible permission bypass due to a confused deputy. This could lead to local escalation of privilege with System execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-57014

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-15T19:17:30.730 |

In phNxpNciHal_ext_process_nfc_init_rsp of phNxpNciHal_ext.cc, there is a possible out-of-bounds write due to a missing bounds check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-57012

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-15T19:17:30.620 |

In the Setup Wizard, there is a possible remote package install due to a missing permission check. This could lead to remote escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-56986

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-09-15T19:17:29.930 |

In multiple files, there is a possible out-of-bounds read due to type confusion. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-56945

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441;CWE-787` |
| Published | 2026-09-15T19:17:28.457 |

In VPU, there is a possible out-of-bounds write due to a confused deputy. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55351

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-09-15T19:17:21.703 |

In VPU, there is a possible out-of-bounds write due to an integer overflow. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55323

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-09-15T19:17:21.317 |

In gf_base_update_finger_base of gf_base.c, there is a possible out-of-bounds write due to a heap buffer overflow. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-19886

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-09-15T19:17:18.353 |

OriginLab Origin Viewer OGM File Parsing Memory Corruption Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab Origin Viewer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OGM files. The issue results from the lack of proper validation of user-supplied data, which can result in a memory corruption condition. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29340.

### CVE-2026-19885

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-15T19:17:18.240 |

OriginLab Origin Viewer OGWU File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab Origin Viewer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OGWU files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated data structure. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29337.

### CVE-2026-19781

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-15T19:17:17.987 |

Ashlar-Vellum Cobalt VS File Parsing Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Ashlar-Vellum Cobalt. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of VS files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28173.

### CVE-2026-0199

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-787` |
| Published | 2026-09-15T19:17:15.033 |

In gf_ta_test_set_config of gf_ta_test.c, there is a possible out-of-bounds write due to improper input validation. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55864

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-15T16:17:16.517 |

GeoNetwork is a catalog application to manage spatially referenced resources. Prior to 4.2.17 and 4.4.12, POST /api/tools/ogc/sld accepted a caller-supplied WMS server URL and performed a server-side HTTP GET without destination validation. An anonymous attacker could make the GeoNetwork server send requests to internal hosts that are not publicly reachable. When the outbound response was XML, the endpoint could store and return the fetched body, making the request forgery non-blind and enabling internal data disclosure, authorization bypass, and network reconnaissance. This issue is fixed in versions 4.2.17 and 4.4.12.

### CVE-2026-86585

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-16T11:16:44.070 |

The lack of signature verification of firmware update packages in VEO and VEO-XS Wi-Fi monitors, in versions prior to 01.48.001, allows an attacker who controls the delivery of an update to install unauthorised firmware.

### CVE-2026-14916

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-241` |
| Published | 2026-09-16T11:16:40.503 |

A JWT signature verification vulnerability affects Kong components that perform JWT validation for MCP OAuth2 or DataKit integrations inside Kong API Gateway Enterprise. The affected code does not properly validate that the JWT signing algorithm is compatible with the type of key used for verification.



As a result, an unauthenticated remote attacker may be able to craft a forged JWT that is incorrectly accepted as valid, leading to authentication bypass and potential compromise of confidentiality, integrity, and availability.

### CVE-2026-86474

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-16T10:16:54.947 |

The lack of TLS certificate validation when downloading firmware updates in VEO and VEO-XS Wi-Fi monitors, in versions prior to 01.48.001, allows an attacker to perform man-in-the-middle attacks on the update channel.

### CVE-2026-14917

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-09-16T10:16:48.373 |

A SAML authentication bypass vulnerability affects the Kong SAML plugin when the validate_assertion_signature option is explicitly set to false. This option is enabled by default. When disabled, the plugin may extract the SAML identity from an unsigned assertion and authenticate the user without verifying a valid cryptographic signature.



As a result, an unauthenticated remote attacker may be able to submit a crafted SAML response and impersonate arbitrary users, including administrators

### CVE-2026-73439

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-842` |
| Published | 2026-09-16T09:17:04.687 |

On affected platforms running Arista EOS, if OpenConfig is configured and running a gNMI server on the system, and if gNSI Pathz is configured and a gNSI Pathz policy is present on the system, then gNMI may fail to correctly enforce the rules in this policy if both a group rule and a user rule for the same path is present in the policy. Under certain conditions, this can lead to an authenticated user gaining unauthorized permission to read or write gNMI paths that the Pathz policy is intended to restrict.

### CVE-2026-87264

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:15.040 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Integration Broker).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  While the vulnerability is in PeopleSoft Enterprise PeopleTools, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise PeopleTools accessible data. CVSS 3.1 Base Score 7.7 (Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N).

### CVE-2026-87257

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:14.383 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: SDK).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile PLM.  While the vulnerability is in Oracle Agile PLM, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Agile PLM accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-87256

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:14.270 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Application Server).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile PLM.  While the vulnerability is in Oracle Agile PLM, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Agile PLM accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-87183

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:06.180 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows high privileged attacker with logon to the infrastructure where Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.7 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-87151

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:02.547 |

Vulnerability in the Oracle Bills of Material product of Oracle E-Business Suite (component: Setup Workbench).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Bills of Material.  While the vulnerability is in Oracle Bills of Material, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Bills of Material accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-87147

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:02.063 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  While the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-87141

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:01.383 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  While the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-87134

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:00.477 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via TCP to compromise Oracle Hyperion Data Relationship Management.  While the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-87127

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:59.713 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: G-Invoicing).  Supported versions that are affected are 12.2.10-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  While the vulnerability is in Oracle Purchasing, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Purchasing accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-87124

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:59.387 |

Vulnerability in the Oracle iRecruitment product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iRecruitment.  While the vulnerability is in Oracle iRecruitment, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle iRecruitment accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83487

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:56.480 |

Vulnerability in the Oracle Product Hub product of Oracle E-Business Suite (component: Item Catalog).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Hub.  While the vulnerability is in Oracle Product Hub, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Product Hub accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83486

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:56.370 |

Vulnerability in the Oracle Product Hub product of Oracle E-Business Suite (component: Item Catalog).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Hub.  While the vulnerability is in Oracle Product Hub, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Product Hub accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83485

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:56.257 |

Vulnerability in the Oracle Product Hub product of Oracle E-Business Suite (component: Item Catalog).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Hub.  While the vulnerability is in Oracle Product Hub, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Product Hub accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83437

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:52.293 |

Vulnerability in the Oracle Engineering product of Oracle E-Business Suite (component: Change Management).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Engineering.  While the vulnerability is in Oracle Engineering, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Engineering accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83356

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:49.130 |

Vulnerability in the Enterprise Command Center Framework product of Oracle E-Business Suite (component: Security).   The supported version that is affected is V16. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Enterprise Command Center Framework.  While the vulnerability is in Enterprise Command Center Framework, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Enterprise Command Center Framework accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83319

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:44.970 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: Web Service API).   The supported version that is affected is 12.2.1.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via SOAP to compromise Oracle BI Publisher.  While the vulnerability is in Oracle BI Publisher, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle BI Publisher accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83313

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:44.300 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle BI Publisher.  While the vulnerability is in Oracle BI Publisher, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle BI Publisher accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83312

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:44.187 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: E-Business Suite - XDO).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle BI Publisher.  While the vulnerability is in Oracle BI Publisher, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle BI Publisher accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83287

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:41.377 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Presentation Services).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via SOAP to compromise Oracle Business Intelligence Enterprise Edition.  While the vulnerability is in Oracle Business Intelligence Enterprise Edition, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Business Intelligence Enterprise Edition accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83243

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:36.353 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  While the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83233

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:35.200 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  While the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83166

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:27.560 |

Vulnerability in the Oracle Customer Interaction History product of Oracle E-Business Suite (component: Outcome-Result).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Customer Interaction History.  While the vulnerability is in Oracle Customer Interaction History, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Customer Interaction History accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83146

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:25.300 |

Vulnerability in the Siebel CRM End User product of Oracle Siebel CRM (component: Open UI).  Supported versions that are affected are 17.0-26.7. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM End User.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Siebel CRM End User, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM End User accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM End User accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-83142

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:24.850 |

Vulnerability in the Oracle Proposals product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Proposals.  While the vulnerability is in Oracle Proposals, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Proposals accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83141

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:24.743 |

Vulnerability in the Oracle Field Service product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Field Service.  While the vulnerability is in Oracle Field Service, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Field Service accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83134

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:24.083 |

Vulnerability in the Oracle iStore product of Oracle E-Business Suite (component: Shopping Cart).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iStore.  While the vulnerability is in Oracle iStore, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle iStore accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83131

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:23.720 |

Vulnerability in the Oracle Web Applications Desktop Integrator product of Oracle E-Business Suite (component: File download).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Web Applications Desktop Integrator.  While the vulnerability is in Oracle Web Applications Desktop Integrator, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Web Applications Desktop Integrator accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83129

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:23.463 |

Vulnerability in the Oracle Sales product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales.  While the vulnerability is in Oracle Sales, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Sales accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83127

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:23.200 |

Vulnerability in the Oracle Sales Offline product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales Offline.  While the vulnerability is in Oracle Sales Offline, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Sales Offline accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83116

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:21.930 |

Vulnerability in the Oracle Order Management product of Oracle E-Business Suite (component: Product Diagnostic Tools).  Supported versions that are affected are 12.2.5-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Order Management.  While the vulnerability is in Oracle Order Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Order Management accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83088

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:18.617 |

Vulnerability in the RDBMS component of Oracle Database Server.  Supported versions that are affected are 23.4.0-23.26.3. Easily exploitable vulnerability allows low privileged attacker having Authenticated User privilege with network access via Oracle Net to compromise RDBMS.  While the vulnerability is in RDBMS, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of RDBMS. CVSS 3.1 Base Score 7.7 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H).

### CVE-2026-83084

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:18.173 |

Vulnerability in the Oracle Marketing product of Oracle E-Business Suite (component: Audience).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Marketing.  While the vulnerability is in Oracle Marketing, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Marketing accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83070

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:15.890 |

Vulnerability in the PeopleSoft Enterprise PRTL Interaction Hub product of Oracle PeopleSoft (component: Enterprise Portal).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise PRTL Interaction Hub.  While the vulnerability is in PeopleSoft Enterprise PRTL Interaction Hub, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PRTL Interaction Hub accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83068

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:15.663 |

Vulnerability in the Oracle Enterprise Manager for Oracle Database product of Oracle Enterprise Manager (component: Core).   The supported version that is affected is 24.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Enterprise Manager for Oracle Database.  While the vulnerability is in Oracle Enterprise Manager for Oracle Database, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Enterprise Manager for Oracle Database accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83048

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:13.313 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83041

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:12.520 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Portlet Services).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-83012

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:07.910 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Enterprise Capture accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-76820

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-15T20:17:57.127 |

OpenCTI is an open source platform for managing cyber threat intelligence knowledge and observables. Prior to 7.260701.0, the synchronizerFetch GraphQL query called fetchRemoteStreams after checking only that a remote stream URL used HTTP or HTTPS. The backend did not apply the ingestion deny list or reject private, loopback, and link-local destinations, allowing an authenticated account with the INGESTION capability to make OpenCTI request internal services and cloud metadata endpoints. Returned connection errors could distinguish open HTTP ports, open non-HTTP ports, and closed ports, enabling internal network scanning, while compatible endpoint responses could disclose internal data. This issue is fixed in version 7.260701.0.

### CVE-2026-13210

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-15T18:17:16.280 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 15.7 before 19.1.8, 19.2 before 19.2.6, and 19.3 before 19.3.2 that under certain conditions could have allowed an authenticated user to access CI/CD variables outside their intended environment scope due to improper input validation in the environment scope pattern matcher.

### CVE-2026-81897

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-352` |
| Published | 2026-09-15T17:17:27.997 |

In Concrete CMS below CMS 9.5.3, the save_control action in the Express entities forms dashboard controller did not validate the anti-CSRF token. By causing an authenticated administrator to submit a forged cross-site request, a remote attacker without credentials could write attacker-controlled headline and body values to an existing Express form Text control. Those values were emitted without output encoding by the Express form Text element, so the injected markup executed as persistent JavaScript for any administrator who later opened the affected entry, resulting in stored cross-site scripting. The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 7.7 with vector CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N. Thanks Yonatan Drori from Tenzai for reporting.

### CVE-2026-91948

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-09-15T16:17:48.503 |

FreeRDP versions before 3.31.0 contain an out-of-bounds write vulnerability in server-side static virtual channel handling when CHANNEL_OPTION_SHOW_PROTOCOL is enabled. Authenticated clients can queue oversized channel messages that cause buffer underflow and corrupt heap memory including live pointers, potentially enabling code execution.

### CVE-2026-91947

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-15T16:17:48.353 |

FreeRDP server versions before 3.31.0 contain a use-after-free vulnerability in the DRDYNVC parser that dereferences a channel pointer after releasing the synchronization lock. Authenticated clients can race AUDIN channel closure messages against DRDYNVC data parsing to trigger heap-use-after-free when accessing freed channel objects.

### CVE-2026-91930

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-15T16:17:43.743 |

Flowise before 3.1.4 fails to scope enterprise organization and workspace membership APIs to the caller's tenant, allowing authenticated users to supply arbitrary organization IDs. Attackers can add themselves as organization owners, create workspaces, and gain administrative access to victim organizations by exploiting insufficient tenant isolation in the organizationuser and workspace endpoints.

### CVE-2026-65831

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-269;CWE-863` |
| Published | 2026-09-15T16:17:22.387 |

ArcadeDB is a Multi-Model DBMS. Prior to 26.7.1, a reader-role user can submit POST /api/v1/command/{database} with language: js because PolyglotQueryEngine.command, PolyglotQueryEngine.analyze, and PolyglotQueryEngine.registerFunctions do not enforce database-administrator authorization. GraalPolyglotEngine also permits scripts to bypass the allowedPackages whitelist by reflecting from the bound database object through database.getClass().getClassLoader().loadClass to arbitrary host classes. These cooperating defects allow a read-only database user to read arbitrary host files outside the database scope. Process creation is already blocked, so OS command execution is not confirmed. The issue is distinct from CVE-2026-44221, CVE-2026-54076, and CVE-2026-54077. This issue is fixed in version 26.7.1.

### CVE-2026-19407

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-330` |
| Published | 2026-09-15T16:17:08.380 |

Bucket Squatting in Google Cloud Gemini Enterprise Agent Platform SDK for Python versions prior to 1.166.1 allows an attacker to achieve Remote Code Execution (RCE) and tenant-project token theft.

### CVE-2026-53957

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-15T15:17:17.367 |

Contentful MCP Server is a Model Context Protocol server for the Contentful Management API. Prior to @contentful/mcp-server 1.7.19 and @contentful/mcp-tools 0.4.5, export_space and import_space in packages/mcp-tools/src/tools/jobs/space-to-space-migration/exportSpace.ts and packages/mcp-tools/src/tools/jobs/space-to-space-migration/importSpace.ts expose host, proxy, rawProxy, and insecure network options to LLM-controlled tool arguments and combine those options with the server's CONTENTFUL_MANAGEMENT_TOKEN. After space_to_space_migration_handler enables the migration tools, a direct MCP call or prompt injection through attacker-controlled Contentful content can redirect Contentful Management API requests and their Authorization header to an attacker-controlled host or proxy. The regular tools that use createToolClient are unaffected because those tools pin the host from server configuration. Exposure of the personal access token permits persistent out-of-band access to every Contentful space within the token's scope. This issue is fixed in @contentful/mcp-server 1.7.19 and @contentful/mcp-tools 0.4.5.

### CVE-2026-92465

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-16T12:17:08.073 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Themeum WP Mega Menu allows Blind SQL Injection.

This issue affects WP Mega Menu: from n/a through 1.4.2.

### CVE-2026-66372

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-337` |
| Published | 2026-09-15T21:16:41.743 |

The affected products use insufficiently random values, which allows web session tokens to be predictable, bounding token entropy to the seed space.

### CVE-2026-87258

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:14.497 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Folders, Files & Attachments).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Agile PLM, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Agile PLM accessible data as well as  unauthorized update, insert or delete access to some of Oracle Agile PLM accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-87250

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:13.830 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-87233

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:11.857 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.6 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L).

### CVE-2026-87144

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:01.723 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-87137

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:00.807 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-87133

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:00.367 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  While the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-87132

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:00.253 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-87131

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:00.147 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-83320

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:45.083 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: Administration).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle BI Publisher.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle BI Publisher, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle BI Publisher accessible data as well as  unauthorized update, insert or delete access to some of Oracle BI Publisher accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-83207

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:32.310 |

Vulnerability in the Siebel CRM Development product of Oracle Siebel CRM (component: Integration - Scripting).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Development.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Siebel CRM Development as well as  unauthorized update, insert or delete access to some of Siebel CRM Development accessible data and  unauthorized read access to a subset of Siebel CRM Development accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:H).

### CVE-2026-83126

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:23.077 |

Vulnerability in the Oracle Sales Online product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales Online.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Sales Online, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Sales Online accessible data as well as  unauthorized update, insert or delete access to some of Oracle Sales Online accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-83091

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:18.957 |

Vulnerability in the Oracle Field Service product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Field Service.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Field Service accessible data as well as  unauthorized update, insert or delete access to some of Oracle Field Service accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Field Service. CVSS 3.1 Base Score 7.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-83052

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:13.770 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-73943

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:45.310 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Identity Manager.  While the vulnerability is in Oracle Identity Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Identity Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Identity Manager accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-91938

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-15T16:17:45.317 |

Flowise versions before 3.1.4 contain a server-side request forgery vulnerability in Cheerio, Playwright, and Puppeteer document loader nodes that bypass SSRF protection. Attackers can provide arbitrary URLs to fetch cloud metadata, internal services, and private network resources with response content returned as document text.

### CVE-2026-91933

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-15T16:17:44.170 |

Flowise before 3.1.4 fails to enforce workspace-level authorization checks in openai-realtime endpoints, allowing authenticated users to access tools from ChatFlows in other workspaces by supplying an unscoped chatflowid. Attackers can invoke GET and POST requests to retrieve tool definitions and execute tools from victim workspaces, triggering external side effects and accessing sensitive tool outputs.

### CVE-2026-91929

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-15T16:17:43.187 |

Flowise versions before 3.1.4 contain cross-tenant authorization gaps in Enterprise endpoints that fail to verify resource ownership before operations. Attackers with Enterprise access can delete arbitrary workspaces, invite themselves into other organizations, modify cross-org roles, and abuse stored SSO secrets.

### CVE-2026-81736

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1050` |
| Published | 2026-09-16T14:17:10.817 |

If a BIND resolver has cached a tree of SVCB/HTTPS AliasMode records, and is then queried for the root of that tree, the resolver will spend disproportionate CPU time constructing the response.
This issue affects BIND 9 versions 9.18.0 through 9.18.50, 9.20.0 through 9.20.27, 9.21.0 through 9.21.25, 9.18.11-S1 through 9.18.50-S1, and 9.20.9-S1 through 9.20.27-S1.

### CVE-2026-81563

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-09-16T14:17:10.543 |

A BIND resolver encountering an SVCB/HTTPS AliasMode record referencing 14 or more SVCB/HTTPS ServiceMode records may fail to properly deallocate internal resources. If this happens repeatedly, resource exhaustion will eventually prevent the resolver from performing new recursive lookups.
This issue affects BIND 9 versions 9.18.0 through 9.18.50, 9.20.0 through 9.20.27, 9.21.0 through 9.21.25, 9.18.11-S1 through 9.18.50-S1, and 9.20.9-S1 through 9.20.27-S1.

### CVE-2026-77692

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-16T14:17:09.647 |

An attacker can cause `named` to abort by sending a crafted DNS-over-HTTPS request with a cryptographically invalid SIG(0) record, and then closing the transport connection prematurely.
This issue affects BIND 9 versions 9.20.0 through 9.20.27, 9.21.0 through 9.21.25, and 9.20.9-S1 through 9.20.27-S1.

### CVE-2026-19667

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-197` |
| Published | 2026-09-16T14:17:05.037 |

If an attacker-controlled authoritative server can produce a negative answer that is exactly 65536 bytes, then a flaw in `named` results in a negative cache entry of 0 bytes. When this entry is subsequently read, `named` aborts.
This issue affects BIND 9 versions 9.11.0 through 9.18.50, 9.20.0 through 9.20.27, 9.21.0 through 9.21.25, 9.11.3-S1 through 9.18.50-S1, and 9.20.9-S1 through 9.20.27-S1.

### CVE-2026-81634

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-16T09:17:06.210 |

In NLnet Labs Unbound up to and including 1.26.0, a 255 length query name with a large TCP response can lead to a heap buffer overflow during the RRSet canonicalisation routine. This is caused by missing to add the first owner name into the buffer length check. A malicious actor operating a malicious name server or tampering with an incoming response to Unbound (canonicalisation happens before DNSSEC validation), can trigger the vulnerability.

### CVE-2026-27557

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-35` |
| Published | 2026-09-16T08:16:38.520 |

An unauthenticated remote attacker can exploit a path traversal vulnerability in the /index.php/view_uploaded_iodd_file endpoint allowing the SSH server's private keys to be read.

### CVE-2026-1168

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-16T07:16:36.827 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 18.4.6 before 19.1.8, 19.2 before 19.2.6, and 19.3 before 19.3.2 that under certain conditions could have allowed an unauthenticated user to cause denial of service due to improper resource allocation limits in the GraphQL complexity calculation logic.

### CVE-2025-14871

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-16T07:16:32.543 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 18.4.6 before 19.1.8, 19.2 before 19.2.6, and 19.3 before 19.3.2 that under certain conditions could have allowed an unauthenticated user to cause denial of service due to improper resource allocation limits in the GraphQL complexity calculation logic.

### CVE-2026-89063

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-16T05:16:47.313 |

The Online Scheduling and Appointment Booking System – Bookly plugin for WordPress is vulnerable to Insecure Direct Object Reference in all versions up to, and including, 28.1 via the 'conversation_id' parameter due to missing validation on a user controlled key. This makes it possible for unauthenticated attackers to read the full AI booking conversation transcript of any customer — leaking names, email addresses, phone numbers, and appointment details echoed by the assistant — and inject arbitrary messages into any victim conversation that are subsequently replayed to the Cloud AI worker along with the full private history. Because AI conversations are stored with no owner, user, or session identifier and conversation IDs are sequential integers, an unauthenticated attacker can enumerate all customer conversations simply by incrementing the conversation_id parameter.

### CVE-2026-86109

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-16T03:17:00.250 |

The VeloCloud Edge software update workflow may accept update bundles without properly validating their signatures because the workflow does not restrict the digest algorithm used for artifact verification. An attacker with either sufficient privileges to upload packages to VeloCloud Orchestrator or credentials permitting direct access to an Edge may be able to install unauthorized software.

### CVE-2026-86108

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T03:17:00.077 |

Insufficient validation of inputs supplied through affected VeloCloud Edge management and configuration workflows may allow an authorized management request or configuration value to be interpreted as an operating-system command. Successful exploitation may allow command execution with elevated privileges on the affected VeloCloud Edge.

### CVE-2026-88065

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-306;CWE-639` |
| Published | 2026-09-15T21:16:43.367 |

`tts-be` is a backend for a timetable selector that aims to help students better choose their class schedules. Versions prior to 2.1.0 have a Broken Access Control vulnerability across several API endpoints (such as `/api/student/{id}/photo` and `/api/course_unit/{id}/exchange/metadata`). By chaining these unauthenticated endpoints, a remote attacker can use the backend as an open proxy to bypass authorization checks, allowing for the enumeration and extraction of sensitive Personally Identifiable Information (PII) from upstream university systems. The exposed data includes full names, student IDs, class schedules, and photos. This issue was fixed in version 2.1.0.

### CVE-2026-61554

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T21:16:41.223 |

emp3r0r is a C2 designed by Linux users for Linux environments. Prior to version 4.2.5, the `http_poll` C2 transport accepts attacker-controlled HTTP polling sessions before CBOR `MsgAuth` authentication is completed. A remote unauthenticated attacker can create arbitrary polling sessions and send request bodies that are forwarded into the C2 dispatch path. This can consume server resources and trigger pre-auth C2 processing. Version 4.2.5 patches the issue.

### CVE-2026-88975

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:19:19.943 |

Http4s is a Scala interface for HTTP services. Prior to 0.23.37 and 1.0.0-M48, Ember’s HTTP/2 read loop parses a frame’s 24-bit declared length but waits to buffer the entire payload before comparing it with SETTINGS_MAX_FRAME_SIZE. An unauthenticated peer can declare a payload near 16 MiB on a connection where Ember advertised 16 KiB and either complete or slowly stream it, causing up to 1024-fold memory amplification per connection before processFrame can reject the frame. The shared H2Connection.readLoop affects withHttp2 servers and clients, while HTTP/2-disabled configurations are unaffected, and the patch rejects oversized frames before buffering their payloads. This issue is fixed in versions 0.23.37 and 1.0.0-M48.

### CVE-2026-87289

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:19:18.897 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: helidon-webserver-static-content).  Supported versions that are affected are 4.0.0-4.5.4. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Helidon. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-87277

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:19:16.460 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.16. Easily exploitable vulnerability allows unauthenticated attacker with network access via RDP to compromise Oracle VM VirtualBox.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-87276

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:16.353 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.16. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-87254

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:14.160 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Folders, Files & Attachments).   The supported version that is affected is 9.3.6. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks of this vulnerability can result in takeover of Oracle Agile PLM. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87247

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:13.500 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87237

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:12.343 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87222

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:19:10.523 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-87221

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:10.420 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-87215

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:19:09.767 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-87211

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:09.337 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-87205

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:08.663 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-87203

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:08.447 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87199

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:19:08.003 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-87194

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:07.430 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-87193

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:07.310 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-87190

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:06.957 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87148

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:19:02.190 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-87140

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:01.267 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87139

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:01.107 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87138

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:19:00.930 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-87136

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:00.697 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-83489

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:56.707 |

Vulnerability in the Oracle Banking Origination product of Oracle Financial Services Applications (component: Onboarding Batch Processes).  Supported versions that are affected are 14.5.0.0.0-14.9.0.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Banking Origination.  Successful attacks of this vulnerability can result in takeover of Oracle Banking Origination. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83463

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:55.140 |

Vulnerability in the Oracle Mobile Application Server product of Oracle E-Business Suite (component: MWA Terminal Server).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Mobile Application Server executes to compromise Oracle Mobile Application Server.  Successful attacks of this vulnerability can result in takeover of Oracle Mobile Application Server. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83424

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:51.020 |

Vulnerability in the Oracle JDeveloper product of Oracle Fusion Middleware (component: Oracle JDeveloper).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle JDeveloper.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle JDeveloper accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-83415

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:49.903 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83350

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:18:48.470 |

Vulnerability in the Oracle Net Services component of Oracle Database Server.  Supported versions that are affected are 21.3-21.23 and  23.4.0-23.26.3. Easily exploitable vulnerability allows unauthenticated attacker with network access via Oracle Net to compromise Oracle Net Services.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Net Services. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-83349

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:18:48.360 |

Vulnerability in the Oracle Net Services component of Oracle Database Server.  Supported versions that are affected are 19.3-19.32, 21.3-21.23 and  23.4.0-23.26.3. Easily exploitable vulnerability allows unauthenticated attacker with network access via Oracle Net to compromise Oracle Net Services.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Net Services. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-83341

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:47.470 |

Vulnerability in the Oracle Applications Manager product of Oracle E-Business Suite (component: Command Line - RapidClone).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Applications Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Applications Manager accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-83333

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:18:46.543 |

Vulnerability in the Oracle Net Services component of Oracle Database Server.  Supported versions that are affected are 23.4.0-23.26.3. Easily exploitable vulnerability allows unauthenticated attacker with network access via Oracle Net to compromise Oracle Net Services.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Net Services. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-83330

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:18:46.207 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: WebSocket).  Supported versions that are affected are 4.0.0-4.5.4. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Helidon. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-83326

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:45.770 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: Open Integration).  Supported versions that are affected are 25.12-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Integration.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Integration accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-83323

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:45.433 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).   The supported version that is affected is 26.01.0.0.0. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Business Intelligence Enterprise Edition executes to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Business Intelligence Enterprise Edition, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-83318

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:44.860 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: Administration).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle BI Publisher.  Successful attacks of this vulnerability can result in takeover of Oracle BI Publisher. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83296

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:42.420 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: BI Search).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83295

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:42.307 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Presentation Services).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via SOAP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83292

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:41.963 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83289

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:41.597 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Analytics Web General).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via SOAP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83281

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:18:40.700 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: helidon-webserver).  Supported versions that are affected are 4.0.0-4.5.4. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Helidon.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Helidon. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-83280

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:18:40.593 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: helidon-webserver-http2).  Supported versions that are affected are 4.0.0-4.5.4. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP/2 to compromise Helidon.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Helidon. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-83276

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:18:40.000 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: helidon-webclient-http2).  Supported versions that are affected are 4.0.0-4.5.4. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP/2 to compromise Helidon.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Helidon. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-83270

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:39.400 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Business Intelligence Enterprise Edition accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-83263

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:38.623 |

Vulnerability in the Oracle Product Lifecycle Analytics product of Oracle Supply Chain (component: Installation Issues).   The supported version that is affected is 3.6.1. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Lifecycle Analytics.  Successful attacks of this vulnerability can result in takeover of Oracle Product Lifecycle Analytics. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83262

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:38.517 |

Vulnerability in the Oracle Product Lifecycle Analytics product of Oracle Supply Chain (component: Installation Issues).   The supported version that is affected is 3.6.1. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Lifecycle Analytics.  Successful attacks of this vulnerability can result in takeover of Oracle Product Lifecycle Analytics. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83257

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:37.970 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83241

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:36.130 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-83235

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:35.460 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-83228

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:18:34.630 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Siebel CRM Deployment. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-83227

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:34.520 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: EAI).  Supported versions that are affected are 17.0-26.7. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Integration.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Integration. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83226

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:34.403 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83225

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:18:34.290 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Siebel CRM Deployment. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-83223

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:34.060 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Siebel Remote).  Supported versions that are affected are 17.0-26.7. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83222

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:18:33.947 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Siebel CRM Deployment. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-83213

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:32.963 |

Vulnerability in the Siebel CRM End User product of Oracle Siebel CRM (component: Reports).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM End User.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM End User accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-83204

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:31.983 |

Vulnerability in the Oracle Sourcing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sourcing.  Successful attacks of this vulnerability can result in takeover of Oracle Sourcing. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83183

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:18:29.470 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Siebel CRM Deployment. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-83182

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:29.357 |

Vulnerability in the Siebel CRM Development product of Oracle Siebel CRM (component: Configuration Tools).  Supported versions that are affected are 17.0-26.7. Difficult to exploit vulnerability allows low privileged attacker with network access via SQL to compromise Siebel CRM Development.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Development. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83167

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:27.670 |

Vulnerability in the Oracle Application Object Library product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Application Object Library.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Application Object Library accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-83156

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:26.417 |

Vulnerability in the Oracle XML Developers Kit component of Oracle Database Server.  Supported versions that are affected are 19.3-19.32, 21.3-21.23 and  23.4.0-23.26.3. Difficult to exploit vulnerability allows low privileged attacker having XDKC privilege with network access via Oracle Net to compromise Oracle XML Developers Kit.  Successful attacks of this vulnerability can result in takeover of Oracle XML Developers Kit. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83133

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:23.970 |

Vulnerability in the Oracle iStore product of Oracle E-Business Suite (component: Shopping Cart).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle iStore.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle iStore accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-83128

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:23.337 |

Vulnerability in the Oracle Sales Offline product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Sales Offline.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Sales Offline accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-83115

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:21.817 |

Vulnerability in the Oracle Applications Manager product of Oracle E-Business Suite (component: Command Line - RapidClone).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Applications Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Applications Manager accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-83114

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:21.703 |

Vulnerability in the Oracle Quality product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Quality.  Successful attacks of this vulnerability can result in takeover of Oracle Quality. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83110

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:21.223 |

Vulnerability in the Oracle Marketing product of Oracle E-Business Suite (component: Audience).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Marketing.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Marketing accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-83106

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:20.783 |

Vulnerability in the Oracle Forms product of Oracle Fusion Middleware (component: Forms Services, C/S, Charmode).  Supported versions that are affected are 12.2.1.19.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Forms.  Successful attacks of this vulnerability can result in takeover of Oracle Forms. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83075

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:17.137 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.7. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-83065

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:15.323 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).   The supported version that is affected is 14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle WebCenter Portal executes to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83051

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:13.657 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-83034

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:11.733 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Sites accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-83028

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:10.903 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Identity Manager Connector executes to compromise Oracle Identity Manager Connector.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager Connector. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-76688

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:50.797 |

Vulnerabilities have been identified in the web-based management interface of EdgeConnect SD-WAN Orchestrator that could potentially allow an unauthenticated remote actor to circumvent existing authentication controls. Successful exploitation could allow an attacker to gain administrative privileges leading to complete compromise of the EdgeConnect SD-WAN Orchestrator host.

### CVE-2026-76687

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:50.683 |

A vulnerability in the API endpoint of HPE Networking EdgeConnect SD-WAN Orchestrator could allow a low-privilege authenticated remote attacker to escalate privileges. Successful exploitation of this vulnerability may enable the attacker to execute arbitrary system commands with root privileges on the underlying operating system.

### CVE-2026-76686

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:50.570 |

A vulnerability exists in the underlying operating system of HPE Networking EdgeConnect SD-WAN Gateways. Successful exploitation could allow an unauthenticated remote attacker to conduct a denial-of-service attack on the affected service.

### CVE-2026-73960

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:17:47.210 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Ren Server).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-69218

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-15T20:17:41.310 |

Http4s is a Scala interface for HTTP services. Prior to 0.23.35 and 1.0.0-M47, When Ember receives an HTTP/2 HEADERS or PUSH_PROMISE frame without END_HEADERS, H2Connection buffers the header block and subsequent CONTINUATION fragments without a size bound. A remote peer can keep an incomplete block open and exhaust heap memory before request decoding, affecting an ember-server or ember-client configured with withHttp2. The remediation tracks accumulated size against SETTINGS_MAX_HEADER_LIST_SIZE derived from EmberServerBuilder.maxHeaderSize or EmberClientBuilder.maxResponseHeaderSize, sends GOAWAY when the limit is exceeded, and applies receiveHeadersTimeout to incomplete blocks. This issue is fixed in versions 0.23.35 and 1.0.0-M47.

### CVE-2026-69210

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835;CWE-1284` |
| Published | 2026-09-15T20:17:40.320 |

Http4s is a Scala interface for HTTP services. Prior to 0.23.35 and 1.0.0-M47, WebSocket FrameTranscoder.bodyLength rejects extended payload lengths above Integer.MAX_VALUE but permits negative 64-bit lengths. A remote client that completes a WebSocket handshake through an Ember server can send such a frame, causing the decoder to return an empty frame without advancing its input. The decode loop then runs indefinitely, pins a worker at full CPU, and grows an ArrayBuffer without bound, resulting in denial of service. This issue is fixed in versions 0.23.35 and 1.0.0-M47.

### CVE-2026-69203

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-09-15T20:17:39.120 |

Http4s is a Scala interface for HTTP services. Prior to 0.23.35 and 1.0.0-M47, An Ember server with HTTP/2 enabled through withHttp2 does not enforce SETTINGS_MAX_CONCURRENT_STREAMS for peer-created streams. One unauthenticated connection can open an unbounded number of streams, each retaining per-stream state until heap exhaustion. The same unchecked allocation is reachable in an ember-client through server-initiated PUSH_PROMISE frames because enablePush is not enforced. This issue is fixed in versions 0.23.35 and 1.0.0-M47.

### CVE-2026-69202

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-09-15T20:17:38.550 |

Http4s is a Scala interface for HTTP services. Prior to 0.23.35 and 1.0.0-M47, Ember’s HTTP/2 flow-control window is replenished according to bytes received from the network rather than bytes consumed by the application, while each stream stores DATA in an unbounded channel. A hostile peer can therefore send a body faster than a slow or non-draining application consumes it, retaining payloads in heap on an ember-server or ember-client configured with withHttp2. The patch bounds the per-stream H2Connection body channel so application consumption applies backpressure. This issue is fixed in versions 0.23.35 and 1.0.0-M47.

### CVE-2026-69213

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-09-15T19:17:38.317 |

Http4s is a Scala interface for HTTP services. Prior to 0.23.35 and 1.0.0-M47, Ember HTTP/2 serializes outbound frames through one unbounded queue consumed by writeLoop. When the peer stops reading, an unauthenticated HTTP/2 client can continue sending PING, SETTINGS, or DATA frames that cause Ember to enqueue acknowledgments or WINDOW_UPDATE frames faster than the writer drains them, exhausting heap memory on a server built with withHttp2. The shared behavior also affects an ember-client connected to a hostile HTTP/2 server, and the patch replaces the unbounded path with bounded, backpressured outbound queues. This issue is fixed in versions 0.23.35 and 1.0.0-M47.

### CVE-2026-69209

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-09-15T19:17:37.870 |

Http4s is a Scala interface for HTTP services. Prior to 0.23.35 and 1.0.0-M47, The shared WebSocket decoder permits unbounded message buffering because defragmentation accumulates fragments without a limit and FrameTranscoder accepts declared lengths up to Int.MaxValue. A remote client that completes a WebSocket handshake against an http4s-blaze-server or http4s-ember-server endpoint can exhaust server memory with oversized frames or fragmented messages. The patched decoder applies a configurable 64 MiB default limit to individual frames and defragmented messages through EmberServerBuilder.withMaxWebSocketMessageSize. This issue is fixed in versions 0.23.35 and 1.0.0-M47.

### CVE-2026-69208

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-401` |
| Published | 2026-09-15T19:17:37.730 |

Http4s is a Scala interface for HTTP services. Prior to 0.23.35 and 1.0.0-M47, the DigestAuth server middleware removes fresh nonces and stops eviction at the first stale nonce because its stale-nonce comparison is inverted. On an application that protects at least one route with DigestAuth, an unauthenticated attacker can repeatedly trigger authentication challenges, causing the persistent nonce map to grow until the JVM exhausts heap memory. This issue is fixed in versions 0.23.35 and 1.0.0-M47.

### CVE-2026-85234

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-15T18:19:34.927 |

A flaw was found in tftp-hpa. When the `in.tftpd` remap engine processes an inverse remap rule that also aborts with a non-empty custom error message, it can pass invalid match offsets to the `genmatchstring()` function. This leads to out-of-bounds read/write operations. A remote, unauthenticated attacker can exploit this vulnerability by sending a specially crafted request, causing the daemon to crash and resulting in a denial of service.

### CVE-2026-81898

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-15T18:19:26.800 |

In Concrete CMS below version 9.5.3, the Address attribute's country-less text formatter skipped HTML-escaping, enabling stored XSS in Express association views. A user able to submit an Address attribute could execute script in the session of any dashboard user who opened the affected entry. The unescaped branch was reachable because a non-required Address attribute accepted a blank country, and because several Express association templates (for example concrete/elements/express/form/view/dashboard/association.php) echoed the association label mask without applying h(). The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 7.5 with vector CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N. Thanks Yonatan Drori from Tenzai for reporting.

### CVE-2026-81238

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-15T18:19:24.400 |

Dell Wyse Management Suite, versions prior to 2605.0.3.683, contain a Missing Authentication for Critical Function vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-58483

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T18:17:25.873 |

mcp-searxng is a Model Context Protocol server that gives AI assistants web search and URL-reading capabilities through SearXNG. Prior to 1.7.1, web_url_read in src/index.ts passes a caller-supplied URL to readUrlContent() in src/url-reader.ts, where checkContentLength() treats a missing Content-Length header as an inconclusive preflight and the normal and error paths then consume the complete body with response.text(). A server that omits Content-Length can therefore bypass URL_READ_MAX_CONTENT_LENGTH_BYTES and force unbounded memory use. The resulting string is also processed by NodeHtmlMarkdown.translate(), increasing CPU consumption and allowing an unauthenticated HTTP client to cause denial of service. This issue is fixed in version 1.7.1.

### CVE-2026-18113

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-15T18:17:17.770 |

In Concrete CMS 9.0 to 9.5.2, the Top Navigation Bar block did not HTML-escape dropdown child page names before writing them into the page, so a user who could create or rename pages could store a script through a child page name and have it run in the browser of any visitor, editor, or administrator who viewed the navigation and opened the affected dropdown. In the Concrete CMS origin,  the script executed with the victim's privileges and could read same-origin content or perform actions available to that user. The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 7.5 with vector CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N. Thanks labixiaoxin97 for reporting.

### CVE-2026-12358

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-15T18:17:14.123 |

IBM Verify Identity Access could allow a remote attacker to cause a denial of service due to insufficient validation of incoming request resources.

### CVE-2026-12354

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-913` |
| Published | 2026-09-15T18:17:13.847 |

IBM MQ 9.1.0.0 through 9.1.0.37 LTS, 9.2.0.0 through 9.2.0.43 LTS, 9.3.0.0 through 9.3.0.41 LTS, 9.3.0.0 through 9.3.5.1 CD, 9.4.0.0 through 9.4.0.25 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 could allow an authenticated attacker to execute arbitrary code on the application server due to improper validation of JNDI names in the Resource Adapter Installation Verification Test application.

### CVE-2026-11929

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-327` |
| Published | 2026-09-15T18:17:13.283 |

IBM Security Verify Identity Access Reverse Proxy in certain configurations may provide weaker than expected cryptographic validation of user supplied data.

### CVE-2026-11926

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T18:17:12.903 |

IBM Verify Identity Access could allow a remote attacker to cause a denial of service due to insufficient validation of incoming request resources.

### CVE-2025-66974

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-15T18:17:12.033 |

An issue in Prolink 13A Smart Plug Model Version: DS-3202M-UKv3 Wi-Fi and Application Version mEzee 2.6.7 allows attackers to cause a Denial of Service (DoS) or connection to an attacker-controlled device via supplying a crafted packet during the provisioning phase.

### CVE-2026-55692

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-15T17:17:22.330 |

The EmbedVideo Extension is a MediaWiki extension which adds a parser function called #ev and various parser tags for embedding video clips from various video sharing services. Prior to 4.1.0, with the default $wgEmbedVideoRequireConsent configuration enabled, includes/EmbedService/EmbedHtmlFormatter.php places JSON returned through includes/EmbedService/AbstractEmbedService.php into the data-mw-iframeconfig attribute without safely escaping single quotes. Attacker-controlled archiveorg identifiers and wistia or sharepoint URLs accepted by the affected service validators can cause getUrl() output to terminate the attribute and inject event-handler attributes into the generated figure element. A user able to edit a wiki page can store JavaScript that executes in the wiki origin when visitors render the page. This issue is fixed in version 4.1.0.

### CVE-2026-55690

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-15T17:17:22.040 |

The EmbedVideo Extension is a MediaWiki extension which adds a parser function called #ev and various parser tags for embedding video clips from various video sharing services. Prior to 4.1.0, EmbedServiceFactory::newFromName in includes/EmbedService/EmbedServiceFactory.php interpolates an attacker-controlled unknown service name into exception text, and includes/EmbedVideo.php returns that text as HTML through the isHtml output path without neutralization. Both the #ev parser function and the evl parser form can reach this error path. A user able to edit a wiki page can inject stored HTML or JavaScript into the error output, causing code to execute in the wiki origin for visitors who render the page. This issue is fixed in version 4.1.0.

### CVE-2026-55149

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-09-15T17:17:21.893 |

Vouch Proxy is an SSO and OAuth/OIDC login solution for Nginx using the auth_request module. Prior to 0.48.0, Cookie in pkg/cookie/cookie.go parses the total part count from an attacker-controlled multipart cookie name and passes the value to make([]string, numParts) without checking that the value is positive or reasonably bounded. Requests to /validate and /_external-auth-:id reach JWTCacheHandler in pkg/jwtmanager/jwtcache.go, FindJWT in pkg/jwtmanager/jwtmanager.go, and the vulnerable cookie reassembly before JWT validation, so no account or valid session is required. A cookie name such as VouchCookie_1of10000000000 causes an attempted slice allocation of roughly 160 GB and a fatal Go runtime out-of-memory condition, allowing one request to crash the authentication proxy and repeated requests to sustain unavailability. This vulnerability is fixed in 0.48.0.

### CVE-2026-55178

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-639;CWE-862` |
| Published | 2026-09-15T15:17:18.747 |

GeoLens is a self-hosted geospatial data catalog with semantic search, OGC and STAC APIs, and a map builder. Prior to 1.2.3, multiple read and link endpoints authorize only the resource named in the request URL and fail to re-authorize a second caller-influenced dataset reached through a relationship, map layer, VRT source, externalId lookup, or request body. When a public map references a private dataset, anonymous callers can use GET /maps/{id} and GET /maps/{id}/style.json to obtain the private layer's metadata, sampled values, or vector tiles. The style response can expose a replayable HMAC tile URL that is bound to neither a user nor a map. When a public source dataset has a relationship to a private target dataset, anonymous callers can use the dataset relationship APIs to enumerate the relationship and read rows from the private target's backing table. Anonymous callers can also use GET /collections/datasets/items with an externalId dataset UUID to obtain metadata for any private, restricted, or unpublished dataset because that lookup performs no visibility check. Authenticated users with the default editor role can mosaic another user's private raster into an owned VRT and read its pixels, and POST /ai/metadata/{summary,keywords,lineage,quality-statement} accepts a body-controlled dataset_id without a visibility check and returns private metadata and sample values. Pre-existing vrt_source_links also expose unauthorized member metadata and health unless each member is filtered at read time. These paths can disclose vector geometries and attributes, raster pixels, table rows, table names, column schemas, feature counts, extents, source URLs and filenames, contacts, and sampled row values. This issue is fixed in version 1.2.3.

### CVE-2026-61590

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306;CWE-668` |
| Published | 2026-09-16T14:17:06.670 |

djust provides Phoenix LiveView-style reactive server-side rendering for Django with Rust-powered performance. Prior to version 1.0.7, djust's observability endpoints expose live view/session state and a remote method-invocation surface (`eval_handler`). The localhost restriction was an opt-in middleware that the documented setup omits; the views themselves enforced only `DEBUG`. In the misconfigured-but-documented scenario (DEBUG on, middleware not installed) a non-localhost client could read live application state and invoke handlers remotely. This issue is fixed in djust 1.0.7. The localhost restriction is enforced in-view on every observability endpoint (no longer dependent on a separately-installed middleware), and `eval_handler` is restricted; gated requests receive a non-disclosing response. As a workaround, ensure `DEBUG=False` in production, and do not expose the observability endpoints to untrusted networks.

### CVE-2026-91734

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-15T21:16:46.900 |

Incorrect authorization in Core in Google Chrome on on Windows prior to 153.0.8010.47 allowed a local attacker to execute arbitrary code outside the sandbox via a local program. (Chromium security severity: High)

### CVE-2026-87242

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:12.920 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TLS to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87235

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:12.097 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via SSH to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87213

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:09.550 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87212

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:09.443 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via SQL to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87206

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:08.773 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87198

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:07.887 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87195

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:07.547 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TLS to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87143

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:01.607 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87130

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:00.037 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via SMTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83334

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:46.660 |

Vulnerability in the Oracle Web Services Manager product of Oracle Fusion Middleware (component: Web Services Security).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via SOAP to compromise Oracle Web Services Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Web Services Manager accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Web Services Manager. CVSS 3.1 Base Score 7.4 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:H).

### CVE-2026-83218

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:33.510 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Deployment accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Deployment accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83184

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:29.580 |

Vulnerability in the Oracle Application Object Library product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Application Object Library.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Application Object Library accessible data as well as  unauthorized access to critical data or complete access to all Oracle Application Object Library accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83162

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:27.120 |

Vulnerability in the Oracle Application Object Library product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Application Object Library.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Application Object Library accessible data as well as  unauthorized access to critical data or complete access to all Oracle Application Object Library accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83102

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:20.333 |

Vulnerability in the Oracle Forms product of Oracle Fusion Middleware (component: Forms Services, C/S, Charmode).  Supported versions that are affected are 12.2.1.19.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Forms.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Forms accessible data as well as  unauthorized access to critical data or complete access to all Oracle Forms accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-54547

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-15T18:17:22.927 |

Meta Ads MCP is a Model Context Protocol (MCP) server that lets AI assistants run Meta Ads. Prior to version 1.0.115, AuthInjectionMiddleware in meta_ads_mcp/core/http_auth_integration.py rejects HTTP MCP requests only when both auth_token and pipeboard_token are absent, while extract_token_from_headers() does not recognize X-Pipeboard-Token as a primary credential. A network caller using the streamable-http transport can therefore send any X-Pipeboard-Token value, pass the guard without establishing authentication context, and cause get_auth_token() to fall back to the server operator's META_ACCESS_TOKEN. Subsequent MCP tools execute with the operator's Meta credentials and can read or modify the operator's Meta Ads data. Deployments using the default stdio transport or without META_ACCESS_TOKEN are not affected. This issue is fixed in version 1.0.115.

### CVE-2026-18115

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-15T18:17:17.893 |

Concrete CMS 9.2.0 to 9.5.2 did not enforce per-field edit_user_properties permissions on the REST API user write endpoints (PUT /ccm/api/1.0/users/{uID} and POST /ccm/api/1.0/users/{uID}/change_password). A user with an update-scoped OAuth token and permission to edit only one non-sensitive field could change another non-superuser's password, username, email, and attributes, taking over that account. The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 7.4 with vector CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N. Thanks riodrwn for reporting.

### CVE-2026-87261

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:14.820 |

Vulnerability in the Oracle Agile Engineering Data Management product of Oracle Supply Chain (component: Engineering Communication Interface).   The supported version that is affected is 6.2.1. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Agile Engineering Data Management executes to compromise Oracle Agile Engineering Data Management.  While the vulnerability is in Oracle Agile Engineering Data Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Agile Engineering Data Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Agile Engineering Data Management accessible data. CVSS 3.1 Base Score 7.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-87260

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:14.713 |

Vulnerability in the Oracle Agile Engineering Data Management product of Oracle Supply Chain (component: Engineering Communication Interface).   The supported version that is affected is 6.2.1. Easily exploitable vulnerability allows low privileged attacker with access to the physical communication segment attached to the hardware where the Oracle Agile Engineering Data Management executes to compromise Oracle Agile Engineering Data Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Agile Engineering Data Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Agile Engineering Data Management accessible data. CVSS 3.1 Base Score 7.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-87145

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:01.840 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized read access to a subset of Oracle Hyperion Data Relationship Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L).

### CVE-2026-83277

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:40.110 |

Vulnerability in the Oracle Agile PLM MCAD Connector product of Oracle Supply Chain (component: CAX Client).   The supported version that is affected is 3.6. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Agile PLM MCAD Connector executes to compromise Oracle Agile PLM MCAD Connector.  While the vulnerability is in Oracle Agile PLM MCAD Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Agile PLM MCAD Connector accessible data as well as  unauthorized read access to a subset of Oracle Agile PLM MCAD Connector accessible data. CVSS 3.1 Base Score 7.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N).

### CVE-2026-83242

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:36.240 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized read access to a subset of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L).

### CVE-2026-83193

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:30.720 |

Vulnerability in the Siebel Apps - Life Sciences product of Oracle Siebel CRM (component: Life Sciences).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Siebel Apps - Life Sciences executes to compromise Siebel Apps - Life Sciences.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Siebel Apps - Life Sciences. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-83190

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:30.397 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Siebel CRM Deployment executes to compromise Siebel CRM Deployment.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-83185

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:29.690 |

Vulnerability in the Oracle Common Applications product of Oracle E-Business Suite (component: CRM User Management Framework).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Common Applications.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Common Applications accessible data as well as  unauthorized access to critical data or complete access to all Oracle Common Applications accessible data. CVSS 3.1 Base Score 7.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N).

### CVE-2026-83155

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:26.307 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with access to the physical communication segment attached to the hardware where the Siebel CRM Deployment executes to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Deployment accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Siebel CRM Deployment. CVSS 3.1 Base Score 7.3 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H).

### CVE-2026-73955

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:46.673 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Charting).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise PeopleTools accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PeopleTools accessible data. CVSS 3.1 Base Score 7.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N).

### CVE-2026-81899

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-15T18:19:26.930 |

Concrete CMS 9.0.0 to 9.5.2 stored group folder names without sanitization and printed them unescaped on the Members > Groups dashboard page, resulting in stored cross-site scripting. The add and edit group-folder handlers stored the submitted folder name without neutralizing HTML, and the group search grid returned it without output encoding, so the Groups dashboard rendered the name as live markup. An authenticated user holding the Add Group Folder permission could store a script payload as a folder name that executed in the session of any administrator who viewed the Groups dashboard, enabling session and token theft and any action available in the administrator's context. The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 7.3 with vector CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N. Thanks Lý Chấn Hưng (hunglyvn) for reporting.

### CVE-2026-85013

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-15T16:17:34.543 |

A flaw was found in environment-modules. A local attacker can exploit this vulnerability by placing a maliciously named modulefile in a location visible to the victim's `MODULEPATH`. When the victim uses Bash completion for `module` or `ml` commands, the malicious module name, containing shell metacharacters, is evaluated as a command. This can lead to arbitrary command execution in the completing user's shell, impacting their confidentiality, integrity, and availability.

### CVE-2026-92469

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-16T14:17:17.767 |

zlt2000 microservices-platform through 6.0.0 contains an authorization bypass vulnerability in the file-center module DELETE /files/{id} endpoint that performs no ownership validation. Authenticated attackers can enumerate file identifiers via GET /files and delete arbitrary users' files and metadata by supplying their identifiers to the delete endpoint.

### CVE-2026-27564

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T08:16:39.583 |

A high-privileged remote attacker can exploit a command injection vulnerability in the /api/datastorage/data endpoint by sending a PUT request with admin credentials allowing execution of commands with root privileges on the device.

### CVE-2026-27563

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T08:16:39.437 |

A high-privileged remote attacker can exploit a command injection vulnerability in the /api/datastorage/data endpoint by sending a crafted GET request with admin credentials allowing execution of commands with root privileges on the device.

### CVE-2026-27562

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T08:16:39.283 |

A high-privileged remote attacker can exploit a command injection vulnerability in the /api/iodd/config endpoint by sending a crafted PUT request with admin credentials allowing execution of commands with root privileges on the device.

### CVE-2026-27561

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T08:16:39.133 |

A high-privileged remote attacker can exploit a command injection vulnerability in the /api/iodd/config endpoint by sending a crafted GET request with admin credentials allowing execution of commands with root privileges on the device.

### CVE-2026-27560

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T08:16:38.977 |

A high-privileged remote attacker can exploit a command injection vulnerability in the /api/status/data endpoint by sending a crafted DELETE request with admin credentials allowing execution of commands with root privileges on the device.

### CVE-2026-18595

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-16T04:18:00.970 |

The WP-Lister Lite for eBay plugin for WordPress is vulnerable to Stored Cross-Site Scripting via AJAX Cron Handler Request Parameter in all versions up to, and including, 3.8.9 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-76853

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-353` |
| Published | 2026-09-15T22:16:59.070 |

Netcore NR268 firmware version 1.7.121109 contains a security check bypass vulnerability in the parame_put_file.cgi restore archive prefix validation. Attackers can exploit the flawed prefix check in put_parame_file_cgi.c to bypass restricted restore archive handling.

### CVE-2026-54544

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-15T21:16:37.083 |

Fireshare facilitates self-hosted media and link sharing. Prior to version 1.6.16, two API endpoints that trigger outbound HTTP requests are missing the @login_required decorator. An unauthenticated attacker can call POST /api/test-discord-webhook or POST /api/test-webhook and cause the Fireshare server to issue an arbitrary HTTP POST to any URL the attacker supplies, including internal network addresses and cloud metadata services. No credentials, session cookies, or prior access are required. Version 1.6.16 contains a patch.

### CVE-2026-87246

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:13.383 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87244

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:13.153 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87239

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:12.590 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-87207

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:08.887 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows high privileged attacker with network access via SQL to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83482

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:55.917 |

Vulnerability in the Oracle Contracts product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.14-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Contracts.  Successful attacks of this vulnerability can result in takeover of Oracle Contracts. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83481

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:55.807 |

Vulnerability in the Oracle Contracts product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.14-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Contracts.  Successful attacks of this vulnerability can result in takeover of Oracle Contracts. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83453

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:54.057 |

Vulnerability in the Oracle Document Management and Collaboration product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Document Management and Collaboration.  Successful attacks of this vulnerability can result in takeover of Oracle Document Management and Collaboration. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83442

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:52.850 |

Vulnerability in the Oracle Product Hub product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Product Hub.  Successful attacks of this vulnerability can result in takeover of Oracle Product Hub. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83440

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:52.637 |

Vulnerability in the Oracle Product Hub product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Product Hub.  Successful attacks of this vulnerability can result in takeover of Oracle Product Hub. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83344

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:47.800 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Database Application Table).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Identity Manager Connector.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager Connector. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83328

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:45.987 |

Vulnerability in the Oracle Applications Framework product of Oracle E-Business Suite (component: Personalization).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Applications Framework.  Successful attacks of this vulnerability can result in takeover of Oracle Applications Framework. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83325

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:45.660 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83322

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:45.310 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83298

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:42.643 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Platform Security).   The supported version that is affected is 12.2.1.4.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle BI Publisher.  Successful attacks of this vulnerability can result in takeover of Oracle BI Publisher. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83273

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:39.763 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).   The supported version that is affected is 26.01.0.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83195

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:30.940 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows high privileged attacker with network access via TCP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83188

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:30.117 |

Vulnerability in the Oracle Depot Repair product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Depot Repair.  Successful attacks of this vulnerability can result in takeover of Oracle Depot Repair. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83176

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:28.670 |

Vulnerability in the Oracle Common Applications product of Oracle E-Business Suite (component: CRM User Management Framework).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Common Applications.  Successful attacks of this vulnerability can result in takeover of Oracle Common Applications. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83117

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:22.043 |

Vulnerability in the Applications DBA product of Oracle E-Business Suite (component: AD Utilities).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Applications DBA.  Successful attacks of this vulnerability can result in takeover of Applications DBA. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83112

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:21.463 |

Vulnerability in the Oracle Lease and Finance Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.7-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Lease and Finance Management.  Successful attacks of this vulnerability can result in takeover of Oracle Lease and Finance Management. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83082

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:17.953 |

Vulnerability in the Oracle Marketing product of Oracle E-Business Suite (component: Audience).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Marketing.  Successful attacks of this vulnerability can result in takeover of Oracle Marketing. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83063

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:15.020 |

Vulnerability in the Oracle Internet Directory product of Oracle Fusion Middleware (component: OID LDAP Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows high privileged attacker with network access via LDAP to compromise Oracle Internet Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Internet Directory. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83016

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:08.423 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: SQR).  Supported versions that are affected are 8.61-8.63. Difficult to exploit vulnerability allows high privileged attacker with logon to the infrastructure where PeopleSoft Enterprise PeopleTools executes to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in PeopleSoft Enterprise PeopleTools, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-83004

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:07.007 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle WebCenter Enterprise Capture executes to compromise Oracle WebCenter Enterprise Capture.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Enterprise Capture accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Enterprise Capture accessible data. CVSS 3.1 Base Score 7.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-76691

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:51.160 |

Buffer overflow vulnerabilities exist in the API endpoint of HPE Networking EdgeConnect SD-WAN Gateways. Successful exploitation could allow an authenticated remote attacker to execute arbitrary commands as a privileged user on the underlying operating system.

### CVE-2026-76690

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:51.043 |

A vulnerability exists in a component of the HPE Networking EdgeConnect SD-WAN Gateways that may allow for arbitrary command execution. An authenticated remote attacker could exploit this vulnerability by providing a specially crafted input to the affected component. Successful exploitation could result in remote code execution as root.

### CVE-2026-76689

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:50.930 |

A vulnerability exists in the configuration processing logic of the affected component where malformed input is improperly processed. An authenticated remote attacker with administrative privileges could exploit this vulnerability by providing specially crafted configuration data. Successful exploitation could result in a stack-based buffer overflow, potentially leading to remote code execution with root privileges or a denial of service due to a system crash.

### CVE-2026-73966

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:17:47.780 |

Vulnerability in the Siebel Apps - Marketing product of Oracle Siebel CRM (component: Marketing).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Siebel Apps - Marketing.  Successful attacks of this vulnerability can result in takeover of Siebel Apps - Marketing. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-11934

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-15T18:17:13.380 |

IBM Verify Identity Access could allow an administrator to execute additional commands they are not entitled to due to improper validation of user supplied input.

### CVE-2026-90650

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-15T15:17:29.117 |

The MotoPress Hotel Booking plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the Stripe Webhook event object 'id' in all versions up to, and including, 6.2.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The premium Stripe webhook listener only verifies the webhook signature when an optional Stripe signing secret has been configured; because that secret is empty by default, a forged webhook is accepted without cryptographic verification, and the attacker-controlled event object 'id' (e.g. a forged 'refund.created' refund id) is written unescaped into the payment log and later echoed unsanitized when an administrator views the payment. An attacker must know a valid Stripe PaymentIntent ID for an existing payment to route the forged webhook to a payment record. Note: The vulnerable webhook handler (webhook-listener.php) is part of the premium Stripe gateway integration and is not present in the lite plugin directory.

### CVE-2026-92468

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-16T14:17:17.620 |

zlt2000 microservices-platform through 6.0.0 contains an authorization bypass vulnerability in the search-center service that allows authenticated attackers to read any Elasticsearch index by specifying the index name in POST /search/{indexName} and GET /agg/requestStat/{indexName}/{routing} path variables. Attackers can query arbitrary indices including sys_user to retrieve sensitive user records and password hashes without proper access controls.

### CVE-2026-61598

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-09-16T14:17:06.827 |

djust provides Phoenix LiveView-style reactive server-side rendering for Django with Rust-powered performance. Prior to version 1.0.7, `djust.mixins.model_binding.ModelBindingMixin` provides a default `update_model` event handler and is part of the LiveView base MRO, so every LiveView exposes it. It `setattr`s a view attribute whose name is client-supplied (`field`), gated only by: reject `_`-prefixed names; reject a 14-entry denylist of framework internals (`FORBIDDEN_MODEL_FIELDS`); optional `allowed_model_fields` which defaults to None = allow all; and `hasattr` existence. As a result, a client can set any public, existing view attribute — not just the fields actually bound with `dj-model=` in the rendered template. The denylist covers framework plumbing but nothing about developer business/authz state, and the allowlist is opt-in (off by default). A developer who binds one `dj-model="search"` input and also keeps `self.account_id` / `self.is_admin` / `self.total_price` as view state does not realize a client can set ALL of them via `{type:event, event:"update_model", params:{field, value}}` over the WebSocket. Type coercion matches the target attribute's type (so `"true"` -> bool True), aiding the attacker. This issue is fixed in djust 1.0.7. As a workaround, set `allowed_model_fields` explicitly on every view using dj-model (or subclassing LiveView) to the minimal list of bindable fields; do not keep authorization/ownership state in public view attributes that share the view with dj-model bindings.

### CVE-2026-73175

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-16T13:18:06.017 |

Nozomi Networks Labs identified a CWE-400: Uncontrolled Resource Consumption vulnerability in the OPC UA gateway component of Advantech EKI-1242EIMS in firmware version V1.06.01 that allows an adjacent unauthenticated attacker to exhaust the server session pool and cause a complete denial of service to all legitimate OPC UA clients by opening multiple anonymous sessions.

### CVE-2026-92463

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T12:17:07.920 |

yshop-crm through 2.1.3 contains an authorization failure in the GET /admin-api/system/user/page endpoint where the @PreAuthorize annotation is commented out, allowing authenticated back-office users without system:user:list permission to enumerate all users. Attackers with valid back-office credentials and a role with data scope ALL can retrieve the complete user directory including login names, nicknames, departments, email addresses, mobile numbers, and last login information.

### CVE-2026-92462

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T12:17:07.777 |

yshop-crm through 2.1.3 fails to enforce authorization checks on the CrmFlowController deleteFlowStep endpoint, allowing any authenticated back-office user to delete arbitrary approval workflow steps. Attackers can invoke the DELETE /admin-api/crm/flow/delete-step endpoint without required permissions to remove approval steps that control contract, receivable, and invoice finalization processes.

### CVE-2026-92460

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T12:17:07.480 |

yshop-crm through 2.1.3 fails to enforce authorization on the GET /admin-api/crm/operatelog/page endpoint, allowing any authenticated back-office user to access the installation-wide audit trail. Attackers can query the operation log to retrieve operator names, display nicknames, client IP addresses, User-Agent strings, request URLs, action details, and customer identifiers without proper permission checks.

### CVE-2026-92459

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T12:17:07.330 |

yshop-crm through 2.1.3 contains a missing authorization vulnerability in the CrmCluesController receiveCustomer endpoint that allows authenticated back-office users to claim sales leads without proper permission checks. Attackers can invoke the lead-claim endpoint to reassign leads from other employees to themselves by overwriting the ownerUserId field, with no access logging or quota validation to prevent bulk lead theft.

### CVE-2026-92457

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T12:17:07.047 |

yshop-crm through 2.1.3 contains a missing authorization vulnerability in the CrmInvoiceController issueInvoice endpoint that allows authenticated back-office users to issue arbitrary invoices. Attackers can call the PUT /admin-api/crm/invoice/issue endpoint without required permissions to modify invoice status, inflate contract invoiced amounts with attacker-chosen values, and trigger invoice emails to arbitrary addresses.

### CVE-2026-92456

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T12:17:06.900 |

yshop-crm through 2.1.3 fails to enforce authorization on the saveRedisSet and getRedisSet endpoints in CrmCustomerController, allowing any authenticated back-office user to read and modify installation-wide lead-allocation and customer auto-recycling policy. Attackers can invoke these endpoints to manipulate shared Redis keys controlling customer auto-recycling behavior, causing mass customer data deletion, disabling lead recycling, or blocking customer creation across the deployment.

### CVE-2026-40856

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-16T12:17:03.790 |

WNC T-Mobile 5G Box IDU router is vulnerable to improper access control. The vulnerability exists in the wnc_maccheck.cgi endpoint, which is accessible without authentication. It allows a remote attacker to retrieve sensitive configuration data, including the administrator web password, WiFi passphrase, and technical device information.This issue has been fixed in firmware version 1.1.0.651412

### CVE-2026-73468

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-670` |
| Published | 2026-09-16T10:16:52.383 |

A specially crafted packet can cause the premature expiry of multicast forwarding state on affected interfaces, potentially resulting in temporary multicast traffic loss during the affected period.

### CVE-2026-19248

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:N/R:U/V:D/RE:L/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-16T07:16:32.943 |

QDomDocument XML parsing is vulnerable to a remotely-triggerable denial-of-service crash when processing untrusted input.

### CVE-2026-92299

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T02:17:39.317 |

@jitsi/electron-sdk before 10.0.5 exposes getDesktopSources() via contextBridge without requiring an active getDisplayMedia() picker, allowing any script in the meeting page to enumerate screens and windows. Attackers can call the jitsi-screen-sharing-get-sources IPC route to retrieve desktop thumbnails at arbitrary resolution without user consent or operating system permission prompts.

### CVE-2026-92256

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-15T22:17:04.530 |

NR255-V version 1.5.130703 contains a sensitive information disclosure vulnerability in l2tpd_config_show_cgi.c, ipsec_show_cgi.c, and mod_vpn_remote/plan.json read handlers. Attackers can query l2tpd_config_show.cgi to expose stored IPsec PSK and RSA key material.

### CVE-2026-76871

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-15T22:17:02.200 |

Netcore NR255-V version 1.5.130703 contains a sensitive information disclosure vulnerability in mod_vpn_remote/plan.json, pptpd_user_show.cgi, pptp_client_config_show.cgi, and l2tpd_user_show.cgi. Attackers can leverage these components to obtain PPTP and L2TP VPN credentials.

### CVE-2026-76870

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-15T22:17:02.030 |

Netcore NR255-V version 1.5.130703 contains an out-of-bounds read vulnerability in the mtd_write pre-flash validation routine triggered by short firmware uploads. Attackers can upload a truncated firmware image via put_file_cgi.c to trigger out-of-bounds reads across main.c, check_image_uuid.c, and oemMD5Update.c.

### CVE-2026-76859

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-15T22:17:00.120 |

Netcore NR255-V version 1.5.130703 contains a sensitive information disclosure vulnerability in the user_pass_show.cgi component. Low-privilege attackers can exploit this flaw via ui_config_2.xml and misc.js to disclose router credentials.

### CVE-2026-76857

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-15T22:16:59.767 |

Netcore NR255-V firmware version 1.5.130703 contains a sensitive information disclosure vulnerability in the ddns_wan_list_show.cgi endpoint and related DDNSset_cgi, IGD_GetCgiHandler, and IGD_CgiCall components. Attackers who reach this CGI handler can obtain plaintext DDNS credentials, exposing sensitive account information.

### CVE-2026-76855

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-359` |
| Published | 2026-09-15T22:16:59.417 |

Netcore NR255-V version 1.5.130703 contains a sensitive information disclosure vulnerability in the audit endpoints handled by l7_web_auth_log_dump_cgi.c, audit_get_cgi.c, and mod_dispatch_auth/plan.json. Attackers can query these audit components to obtain other users' session and browsing history data across sessions.

### CVE-2026-76854

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-15T22:16:59.250 |

Netcore NR255-V version 1.5.130703 contains a sensitive information disclosure vulnerability in l7_web_auth_user_show.cgi related to captive-portal credential handling. Attackers can query this component to obtain captive-portal user credentials, compromising confidentiality of authenticated network access.

### CVE-2026-10144

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-15T22:16:55.387 |

Rsbuild before 2.0.9 contains a command injection vulnerability that allows attackers to execute arbitrary OS commands by supplying a crafted URL containing shell metacharacters to the server.open configuration on macOS. The openBrowser() function in packages/core/src/server/open.ts passes the URL through encodeURI() before interpolating it into a shell command executed via child_process.exec(), but because encodeURI() does not encode dollar signs, parentheses, or semicolons, embedded shell metacharacters are evaluated by /bin/sh, enabling arbitrary command execution.

### CVE-2026-68953

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-15T21:16:42.743 |

The affected products are vulnerable to an authentication bypass that allows unauthenticated remote attackers to disclose sensitive device information, including administrator credentials in plaintext, by sending crafted HTTP(S) requests.

### CVE-2026-19655

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-15T21:16:36.380 |

On affected platforms running Arista EOS with Dynamic Host Configuration Protocol (DHCP) relay/snooping configured with the information option (Option 82), or with the DHCP server configured with match criteria based on the information option, an unauthenticated attacker connected to a client-facing VLAN(s) where the relay is configured can send a specially crafted packet that causes the DHCP Relay service to restart.

### CVE-2026-87262

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:14.930 |

Vulnerability in the Oracle Agile Engineering Data Management product of Oracle Supply Chain (component: Engineering Communication Interface).   The supported version that is affected is 6.2.1. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Agile Engineering Data Management executes to compromise Oracle Agile Engineering Data Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Agile Engineering Data Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Agile Engineering Data Management accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-87249

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:13.717 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L).

### CVE-2026-87236

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:12.217 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-87225

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:10.847 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-87220

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:10.307 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hyperion Financial Management as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H).

### CVE-2026-87209

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:09.107 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-87208

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:08.993 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-87192

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:07.173 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-87191

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:07.060 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-87160

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:03.597 |

Vulnerability in the Oracle HRMS (India) product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle HRMS (India).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle HRMS (India) accessible data as well as  unauthorized update, insert or delete access to some of Oracle HRMS (India) accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-87158

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:03.327 |

Vulnerability in the Oracle Order Management product of Oracle E-Business Suite (component: Enterprise Command Center).   The supported version that is affected is V16. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Order Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Order Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Order Management accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-87156

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:03.093 |

Vulnerability in the Oracle Product Hub product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Hub.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Product Hub accessible data as well as  unauthorized update, insert or delete access to some of Oracle Product Hub accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-87149

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:02.313 |

Vulnerability in the Oracle Contract Lifecycle Management for Public Sector product of Oracle E-Business Suite (component: Award/PO).  Supported versions that are affected are 12.2.8-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Contract Lifecycle Management for Public Sector.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Contract Lifecycle Management for Public Sector accessible data as well as  unauthorized update, insert or delete access to some of Oracle Contract Lifecycle Management for Public Sector accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-87146

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:01.953 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-87142

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:01.497 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Hyperion Data Relationship Management.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L).

### CVE-2026-87135

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:00.590 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-87126

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:59.603 |

Vulnerability in the Oracle Report Manager product of Oracle E-Business Suite (component: Reports Security).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Report Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Report Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Report Manager. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-83484

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:56.147 |

Vulnerability in the Oracle US Federal Human Resources product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle US Federal Human Resources.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle US Federal Human Resources accessible data as well as  unauthorized read access to a subset of Oracle US Federal Human Resources accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N).

### CVE-2026-83436

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:52.180 |

Vulnerability in the Oracle Depot Repair product of Oracle E-Business Suite (component: Recall Management).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Depot Repair.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Depot Repair accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Depot Repair. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-83417

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:50.127 |

Vulnerability in the Oracle Communications Cloud Native Core Security Edge Protection Proxy product of Oracle Communications (component: SEPP).  Supported versions that are affected are 26.1.200 and  25.2.201. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Communications Cloud Native Core Security Edge Protection Proxy executes to compromise Oracle Communications Cloud Native Core Security Edge Protection Proxy.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Communications Cloud Native Core Security Edge Protection Proxy accessible data as well as  unauthorized update, insert or delete access to some of Oracle Communications Cloud Native Core Security Edge Protection Proxy accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-83352

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:48.690 |

Vulnerability in the Oracle XML Gateway product of Oracle E-Business Suite (component: Install).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle XML Gateway.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle XML Gateway accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle XML Gateway. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-83345

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:47.913 |

Vulnerability in the Oracle XML Gateway product of Oracle E-Business Suite (component: Install).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle XML Gateway.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle XML Gateway accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle XML Gateway. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-83332

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:46.440 |

Vulnerability in the Oracle Applications Framework product of Oracle E-Business Suite (component: Personalization).  Supported versions that are affected are 12.2.9-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Applications Framework.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Applications Framework accessible data as well as  unauthorized update, insert or delete access to some of Oracle Applications Framework accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-83324

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:45.547 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  While the vulnerability is in Oracle Business Intelligence Enterprise Edition, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Business Intelligence Enterprise Edition accessible data as well as  unauthorized read access to a subset of Oracle Business Intelligence Enterprise Edition accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:L/I:H/A:N).

### CVE-2026-83300

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:42.873 |

Vulnerability in the Oracle XML Gateway product of Oracle E-Business Suite (component: Install).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle XML Gateway.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle XML Gateway accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle XML Gateway. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-83259

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:38.183 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-83244

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:36.480 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Commerce Guided Search / Oracle Commerce Experience Manager executes to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:H).

### CVE-2026-83240

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:36.017 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Commerce Guided Search / Oracle Commerce Experience Manager executes to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-83238

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:35.800 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-83237

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:35.690 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-83230

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:34.850 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Siebel Management Console).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Deployment accessible data as well as  unauthorized update, insert or delete access to some of Siebel CRM Deployment accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-83224

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:34.177 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Deployment accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Siebel CRM Deployment. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-83221

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:33.840 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: EAI).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with network access via SOAP to compromise Siebel CRM Integration.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Integration accessible data as well as  unauthorized update, insert or delete access to some of Siebel CRM Integration accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-83219

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:33.620 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Siebel CRM Deployment executes to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Deployment accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Deployment accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83217

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:33.400 |

Vulnerability in the Siebel CRM End User product of Oracle Siebel CRM (component: Open UI).  Supported versions that are affected are 17.0-26.7. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM End User.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM End User accessible data as well as  unauthorized update, insert or delete access to some of Siebel CRM End User accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-83206

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:32.203 |

Vulnerability in the Oracle Banking Corporate Lending Process Management product of Oracle Financial Services Applications (component: Base).  Supported versions that are affected are 14.5.0.0.0-14.9.0.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Banking Corporate Lending Process Management.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Banking Corporate Lending Process Management. CVSS 3.1 Base Score 7.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-83187

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:29.937 |

Vulnerability in the Oracle Common Applications Calendar product of Oracle E-Business Suite (component: Applications Calendar).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Common Applications Calendar.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Common Applications Calendar accessible data as well as  unauthorized read access to a subset of Oracle Common Applications Calendar accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N).

### CVE-2026-83186

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:29.803 |

Vulnerability in the Oracle Common Applications Calendar product of Oracle E-Business Suite (component: Applications Calendar).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Common Applications Calendar.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Common Applications Calendar accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Common Applications Calendar. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L).

### CVE-2026-83179

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:29.017 |

Vulnerability in the Oracle Common Applications Calendar product of Oracle E-Business Suite (component: Applications Calendar).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Common Applications Calendar.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Common Applications Calendar accessible data as well as  unauthorized access to critical data or complete access to all Oracle Common Applications Calendar accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Common Applications Calendar. CVSS 3.1 Base Score 7.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-83173

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:28.327 |

Vulnerability in the Oracle One-to-One Fulfillment product of Oracle E-Business Suite (component: Documents).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle One-to-One Fulfillment.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle One-to-One Fulfillment accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle One-to-One Fulfillment. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-83171

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:28.103 |

Vulnerability in the Oracle One-to-One Fulfillment product of Oracle E-Business Suite (component: Documents).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle One-to-One Fulfillment.  While the vulnerability is in Oracle One-to-One Fulfillment, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle One-to-One Fulfillment accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle One-to-One Fulfillment. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:N/A:L).

### CVE-2026-83161

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:27.007 |

Vulnerability in the Oracle Project Intelligence product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Project Intelligence.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Project Intelligence accessible data as well as  unauthorized read access to a subset of Oracle Project Intelligence accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N).

### CVE-2026-83158

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:26.670 |

Vulnerability in the Oracle Applications Manager product of Oracle E-Business Suite (component: Command Line - RapidClone).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Applications Manager executes to compromise Oracle Applications Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Applications Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Applications Manager accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-83130

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:23.590 |

Vulnerability in the Oracle Site Hub product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Site Hub.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Site Hub accessible data as well as  unauthorized read access to a subset of Oracle Site Hub accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N).

### CVE-2026-83123

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:22.720 |

Vulnerability in the Oracle Report Manager product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Report Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Report Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Report Manager. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-83113

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:21.583 |

Vulnerability in the Oracle Quality product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Quality.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Quality accessible data as well as  unauthorized update, insert or delete access to some of Oracle Quality accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-83111

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:21.330 |

Vulnerability in the Oracle Partner Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Partner Management.  While the vulnerability is in Oracle Partner Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Partner Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Partner Management accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-83092

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:19.090 |

Vulnerability in the Oracle Field Service product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Field Service.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Field Service accessible data as well as  unauthorized access to critical data or complete access to all Oracle Field Service accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Field Service. CVSS 3.1 Base Score 7.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-83080

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:17.723 |

Vulnerability in the Oracle Banking Branch product of Oracle Financial Services Applications (component: Reports).  Supported versions that are affected are 14.5.0.0.0-14.9.0.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Banking Branch.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Banking Branch. CVSS 3.1 Base Score 7.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-83050

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:13.540 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-83046

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:13.087 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle WebCenter Portal. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-83044

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:12.853 |

Vulnerability in the Oracle XML Gateway product of Oracle E-Business Suite (component: Install).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle XML Gateway.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle XML Gateway accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle XML Gateway. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-76821

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-09-15T20:17:57.280 |

OpenCTI is an open source platform for managing cyber threat intelligence knowledge and observables. Prior to 7.260706.0, the JSON ingestion mapper's extractWithRegexp formula function compiled a user-supplied regular expression with the JavaScript RegExp engine in opencti-platform/opencti-graphql/src/parser/json-mapper.ts without validating its complexity. An authenticated user with JSON mapper creation permission could provide a catastrophically backtracking pattern and matching ingestion input, blocking the Node.js event loop and making the GraphQL API unavailable to all users. Scheduled ingestion could repeatedly execute the malicious mapper without additional attacker action, and recovery could require disabling the mapper and restarting the process. The issue affects availability and does not expose or modify data. This issue is fixed in version 7.260706.0.

### CVE-2026-76692

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-15T20:17:51.263 |

A vulnerability in HPE Networking EdgeConnect SD-WAN Gateways could allow an unauthenticated adjacent attacker to obtain limited information from memory and disrupt the normal operation of the affected service. Successful exploitation could result in a denial of service (system crash) or the disclosure of uninitialized stack memory.

### CVE-2026-78081

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-15T19:17:39.607 |

Joomla Extension - j2commerce.com - Missing CSRF protection on cart, checkout and myprofile controllers in J2Store 1.0.0-3.3.2, 4.0.0-4.0.22, 4.1.0-4.1.7 - A forged request riding a victim's active checkout session could silently overwrite the billing or shipping address before order confirmation — the most consequential sub-case, since it opens the door to redirecting a paid order's goods to an attacker-controlled address — or tamper with a saved profile address via `saveAddress()`. As before, each forged request executes with only the victim's own session privileges, so there is no cross-account data access.

### CVE-2026-19774

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.0/AV:A/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-15T19:17:17.867 |

BlueZ A2DP Stack-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of BlueZ. An attacker must first obtain the ability to pair a malicious Bluetooth device with the target system in order to exploit this vulnerability.

The specific flaw exists within the handling of the stream endpoints. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a fixed-length stack-based buffer. An attacker can leverage this vulnerability to execute code in the context of root. Was ZDI-CAN-29429.

### CVE-2026-58502

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-15T18:17:26.193 |

githubtoplanguages generates a user's top GitHub languages as an SVG. The .github/workflows/discord-issue.yml workflow runs when an issue is opened or closed and interpolates github.event.issue.title directly into the Bash assignment for ISSUE_TITLE before shell parsing. An issue title containing shell command-substitution syntax can therefore execute commands on the GitHub Actions runner before the title is included in the Discord notification sent through DISCORD_WEBHOOK. Successful exploitation can manipulate or spoof trusted bot notifications and may expose the Discord webhook secret or other workflow environment data, depending on repository permissions. This issue is fixed by commit 6bf9c3a9cb66c937b9047ca266b3d02f2bb11027.

### CVE-2026-58485

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-15T18:17:26.040 |

mcp-searxng is a Model Context Protocol server that gives AI assistants web search and URL-reading capabilities through SearXNG. Prior to 1.7.1, web_url_read receives its caller-controlled URL through src/index.ts and validates only the literal hostname in assertUrlAllowed() within src/url-reader.ts before undiciFetch() performs operating-system DNS resolution. A public-looking attacker-controlled hostname that resolves to a private, loopback, link-local, or cloud-metadata address therefore passes the lexical check and causes the MCP server to connect to the internal destination. In the default HTTP configuration, an unauthenticated network client can use this path to read internal services, expose credentials or service tokens, and enumerate reachable internal hosts; in STDIO deployments, prompt-influenced tool selection can provide the malicious URL. Direct private IP literals are blocked, and MCP_HTTP_ALLOW_PRIVATE_URLS remains an explicit opt-out. This issue is fixed in version 1.7.1.

### CVE-2026-12752

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-15T18:17:15.207 |

IBM Business Automation Workflow containers and traditional is vulnerable to an XML external entity injection (XXE) attack when processing XML data. A remote attacker could exploit this vulnerability to expose sensitive information or consume memory resource.

### CVE-2026-12667

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-15T18:17:14.420 |

IBM MQ 9.1.0.0 through 9.1.0.37 LTS, 9.2.0.0 through 9.2.0.43 LTS, 9.3.0.0 through 9.3.0.41 LTS, 9.3.0.0 through 9.3.5.1 CD, 9.4.0.0 through 9.4.0.25 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 could allow an authenticated attacker to read files from a vulnerable .NET client or cause limited denial of service due to improper handling of XML external entities in RFH2 folder parsing.

### CVE-2026-58200

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-15T17:17:23.113 |

Payload Plugins is a collection of plugins designed to enhance Payload CMS. From 0.3.0 until 0.4.0, @jhb.software/payload-cloudinary-plugin deployments with clientUploads enabled expose POST /api/cloudinary-generate-signature, whose handler in cloudinary/src/getGenerateSignature.ts passes attacker-controlled body.paramsToSign directly to cloudinary.utils.api_sign_request without a key allowlist, collection policy, timestamp freshness check, or configured-folder enforcement. Any authenticated Payload user can obtain a valid Cloudinary HMAC-SHA1 signature for unauthorized parameters such as overwrite, type, notification_url, invalidate, folder, and public_id. The signature can authorize asset replacement, upload visibility changes, callbacks to attacker-selected URLs, cache invalidation, and uploads outside the intended folder. The client-visible Cloudinary API key is expected by the upload design, but the unrestricted server-side signature supplies the authorization value needed to complete these operations. This vulnerability is fixed in 0.4.0.

### CVE-2026-21588

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T17:17:12.020 |

This High severity DoS (Denial of Service) vulnerability was introduced in versions 8.9.0, 9.0.1, 9.1.0, 9.2.0, 9.3.1, 9.4.0, 9.5.1, 10.0.2, 10.1.0, and 10.2.0 of Confluence Data Center.

This DoS (Denial of Service) vulnerability, with a CVSS Score of 7.1, allows an authenticated attacker to cause a resource to be unavailable for its intended users by temporarily or indefinitely disrupting services of a host connected to a network.

Atlassian recommends that Confluence Data Center customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
 Confluence Data Center 9.2: Upgrade to a release greater than or equal to 9.2.24

 Confluence Data Center 10.2: Upgrade to a release greater than or equal to 10.2.17

See the release notes ([https://confluence.atlassian.com/doc/confluence-release-notes-327.html]). You can download the latest version of Confluence Data Center from the download center ([https://www.atlassian.com/software/confluence/download-archives]).

This vulnerability was reported via our Penetration Testing program.

### CVE-2026-21587

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-15T17:17:11.893 |

This High severity Improper Authorization vulnerability was introduced in version 11.3.0 of Jira Service Management Data Center. 
	
	This Improper Authorization vulnerability, with a CVSS Score of 7.1, allows an authenticated attacker to gain unintended access and can lead to the exposure of resources or functionality, possibly providing attackers with sensitive information or even execute arbitrary code. 
	
	Atlassian recommends that Jira Service Management Data Center customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
		
		* Jira Service Management Data Center 11.3: Upgrade to a release greater than or equal to 11.3.11
		
		
	
	See the release notes (https://confluence.atlassian.com/servicemanagement/jira-service-management-release-notes-780083086.html). You can download the latest version of Jira Service Management Data Center from the download center (https://www.atlassian.com/software/jira/service-management/download-archives). 
	
	This vulnerability was reported via our Penetration Testing program.

### CVE-2026-21586

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-15T17:17:11.580 |

This High severity Improper Authorization vulnerability was introduced in versions 7.4.0, 7.13.0, 8.5.0, 8.9.0, 9.0.1, 9.1.0, 9.2.0, 9.3.1, 9.4.0, 9.5.1, 10.0.2, 10.1.0, and 10.2.0 of Confluence Data Center.

This Improper Authorization vulnerability, with a CVSS Score of 7.1, allows an authenticated attacker to gain unintended access and can lead to the exposure of resources or functionality, possibly providing attackers with sensitive information or even execute arbitrary code.

Atlassian recommends that Confluence Data Center customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
 Confluence Data Center 9.2: Upgrade to a release greater than or equal to 9.2.24

 Confluence Data Center 10.2: Upgrade to a release greater than or equal to 10.2.17

See the release notes ([https://confluence.atlassian.com/doc/confluence-release-notes-327.html]). You can download the latest version of Confluence Data Center from the download center ([https://www.atlassian.com/software/confluence/download-archives]).

This vulnerability was reported via our Penetration Testing program.

### CVE-2026-91987

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-15T16:17:57.300 |

atomic-agents-stack before 1.1.0 contains a cost-guardrail bypass in the _estimate_batch_cost function that returns zero cost for unknown models not in the pricing table. Attackers can configure deployments with unknown model identifiers to bypass daily cost caps and exceed budget limits in parallel batch operations.

### CVE-2026-91979

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T16:17:54.793 |

Vikunja before 2.6.0 fails to limit archive expansion during data import, allowing authenticated users to cause denial of service. Attackers can upload highly compressed files that expand to tens of gigabytes in memory and disk, exhausting server resources and crashing the instance.

### CVE-2026-91971

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T16:17:53.947 |

Vikunja before 2.6.0 fails to apply pixel decode limits to avatar and project-background upload endpoints, allowing authenticated users to upload crafted images that decode to excessive pixel counts. Attackers can upload small images with extreme aspect ratios that consume significant CPU and memory during processing, causing denial of service through repeated or concurrent uploads.

### CVE-2026-91970

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-15T16:17:53.803 |

Vikunja versions before 2.6.0 contain a resource exhaustion vulnerability in the Planka migrator that fails to enforce aggregate memory budgets during migration jobs. Authenticated attackers can submit migration requests pointing to attacker-controlled servers advertising numerous size-compliant attachments, exhausting worker memory and causing denial of service for all users.

### CVE-2026-91969

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T16:17:53.647 |

vikunja versions before 2.6.0 contain a resource exhaustion vulnerability in the POST /api/v2/migration/csv/migrate endpoint that fails to limit parsed row cardinality. Authenticated attackers can upload multipart CSV files with millions of tiny records to exhaust process memory and terminate the API service.

### CVE-2026-91968

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-15T16:17:53.093 |

vikunja versions before 2.6.0 contain a resource exhaustion vulnerability in the task-filter endpoint that accepts deeply nested filter expressions without recursion depth limits. Authenticated attackers can supply thousands of nested parentheses in the filter query parameter to exhaust memory and terminate the API process.

### CVE-2026-91963

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-457` |
| Published | 2026-09-15T16:17:51.907 |

FreeRDP versions before 3.31.0 contain an uninitialized heap memory disclosure vulnerability in the urbdrc USB redirection channel. A malicious RDP server can induce failing USB transfers to read uninitialized heap memory from the client, defeating ASLR and enabling remote code execution when chained with memory corruption vulnerabilities.

### CVE-2026-91961

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-15T16:17:51.613 |

FreeRDP before 3.31.0 contains a denial-of-service vulnerability in the URBDRC control-transfer request path that fails to validate OutputBufferSize before forwarding to the libusb backend. A malicious RDP server can send a control-transfer request with OutputBufferSize set to 65536, triggering a reachable assertion that terminates the client process.

### CVE-2026-91960

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-15T16:17:51.070 |

FreeRDP versions before 3.31.0 contain an integer overflow in WinPR's Stream_EnsureRemainingCapacity function that allows remote attackers to cause denial of service. A malicious RD Gateway peer can send a WebSocket Ping frame with a crafted 64-bit extended payload length to trigger integer wraparound, resulting in a double free that crashes the FreeRDP client during connection.

### CVE-2026-91959

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-15T16:17:50.930 |

FreeRDP before 3.31.0 contains a buffer over-read vulnerability in the rts_read_result function within the RPC gateway transport parser. Attackers can send a malicious BIND_ACK PDU with a truncated result entry to trigger an out-of-bounds read causing process abort.

### CVE-2026-91956

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-15T16:17:50.500 |

FreeRDP before 3.31.0 contains an out-of-bounds read vulnerability in the URBDRC channel's func_get_ep_desc function that indexes interface arrays by position instead of protocol field InterfaceNumber. A malicious RDP server can send a crafted SELECT_CONFIGURATION message with permuted InterfaceNumber values to read past allocated heap memory and crash the client.

### CVE-2026-91954

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-15T16:17:49.807 |

FreeRDP before 3.31.0 contains a null pointer dereference vulnerability in gdi_surface_bits when processing Surface Bits commands with NSCodec codec ID. A malicious RDP server can crash a FreeRDP client by sending a crafted Surface Bits command claiming to use NSCodec, even when the codec is disabled.

### CVE-2026-91953

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-15T16:17:49.657 |

FreeRDP versions before 3.31.0 contain a heap buffer overflow vulnerability in nego_send_negotiation_request() that fails to validate the LB_LOAD_BALANCE_INFO field length before writing to a fixed 512-byte buffer. A malicious RDP server or man-in-the-middle can send a Server Redirection PDU with an oversized LB_LOAD_BALANCE_INFO value to overflow the buffer with attacker-controlled content, causing denial of service or heap corruption before authentication completes.

### CVE-2026-91952

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-09-15T16:17:49.490 |

FreeRDP versions before 3.31.0 contain an infinite-loop denial of service in the pool_decode_rect function when decoding AVC444 metablocks with more region rectangles than preallocated worker array size. A malicious RDP server can send crafted AVC444 graphics updates causing the threaded decode path to loop indefinitely, consuming CPU and preventing normal client operation.

### CVE-2026-91951

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-15T16:17:49.340 |

FreeRDP versions before 3.31.0 contain an out-of-bounds write vulnerability in the urbdrc client channel's urb_send_current_frame_number_result() function. A malicious RDP server can send a crafted 28-byte USB redirection message to trigger a 4-byte write past the allocated 16-byte buffer, causing denial of service when verbose asserts are enabled.

### CVE-2026-91950

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-15T16:17:48.800 |

FreeRDP before 3.31.0 contains an out-of-bounds read vulnerability in the rdpdr_dump_packet function due to 32-bit unsigned integer wraparound in buffer bounds validation. A malicious RDP server can send a crafted RDPDR packet with computerNameLen set to 0xFFFFFFF0 to bypass bounds checks and trigger memory reads past the packet buffer, causing client crashes or heap disclosure in logs.

### CVE-2026-91946

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-908` |
| Published | 2026-09-15T16:17:47.990 |

FreeRDP versions before 3.31.0 contain an information disclosure vulnerability in the RDPGFX server's ResetGraphics PDU serializer that fails to initialize padding bytes in the fixed 340-byte wire format. Attackers can receive uninitialized heap memory including live pointers and GLib function addresses transmitted in the PDU, defeating heap ASLR and disclosing the GLib module base address.

### CVE-2026-91945

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-15T16:17:46.657 |

FreeRDP versions before 3.31.0 contain an out-of-bounds read vulnerability in smartcard response decoders that fail to validate ATR length fields against fixed inline arrays. Authenticated RDP clients can send oversized ATR lengths in PAKID_CORE_DEVICE_IOCOMPLETION responses to trigger reads past stack or heap objects, causing process termination.

### CVE-2026-59965

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-15T16:17:17.110 |

Payload Plugins is a collection of plugins designed to enhance Payload CMS. In 0.7.0, @jhb.software/payload-alt-text-plugin exposes POST /api/alt-text-plugin/generate and POST /api/alt-text-plugin/bulk with a default guard that accepts any authenticated user, while alt-text/src/endpoints/generateAltText.ts and alt-text/src/endpoints/bulkGenerateAltTexts.ts call req.payload.findByID and req.payload.update without overrideAccess: false. Payload therefore defaults overrideAccess to true and skips the target collection's read and update access functions. An authenticated low-privilege user can supply id, collection, locale, and update values to read arbitrary protected upload documents and overwrite their alt and keywords fields, even when the collection permits those operations only to administrators. A control Local API call with overrideAccess: false is denied, confirming that the plugin endpoint bypasses otherwise effective collection rules. This vulnerability is fixed in 0.8.0.

### CVE-2026-54077

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-22;CWE-776;CWE-918` |
| Published | 2026-09-15T16:17:13.710 |

ArcadeDB is a Multi-Model DBMS. Prior to 26.6.1, the IMPORT DATABASE statement in engine/src/main/java/com/arcadedb/query/sql/parser/ImportDatabaseStatement.java did not require administrative privileges and passed its source to integration/src/main/java/com/arcadedb/integration/importer/SourceDiscovery.java without validation. An authenticated user with SQL command access through /api/v1/command or /api/v1/query can supply HTTP or HTTPS destinations to make server-side requests to internal services, or file:// paths to read files accessible to the server process and ingest the results as queryable records. The XML importer also permits DTD processing and external entities, enabling entity expansion. The root-only /api/v1/server administration endpoint is not affected. The fix requires updateSecurity permission, blocks local-network import destinations by default through arcadedb.server.security.importBlockLocalNetworks, supports the arcadedb.server.security.importAllowedLocalPaths file allow-list, and disables XML DTD processing and external entities. This issue is fixed in version 26.6.1.

### CVE-2026-53966

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-15T15:17:17.533 |

XWiki Platform is a generic wiki platform. From 13.4-rc-1 until 16.10.17, 17.4.10, 17.10.4, and 18.1.0-rc-1, the Live Data edit REST API allows a user who can edit a page to change that page's rights without executing the normal document-saving authorization checks. The user can grant script right and then execute potentially dangerous Velocity scripts or send unfiltered HTML and JavaScript to clients. The same missing checks can circumvent extension security controls implemented as listeners for UserUpdatingDocumentEvent and related user document events. This issue is fixed in versions 16.10.17, 17.4.10, 17.10.4, and 18.1.0-rc-1.

### CVE-2026-85628

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:P/VC:H/VI:N/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-09-16T10:16:53.670 |

Transmission of the home Wi-Fi credentials without encryption during the pairing process between the DuoxMe application and VEO and VEO-XS Wi-Fi monitors, in versions prior to 4.3.4 of the application and 01.50.001 of the monitor firmware, allows an attacker on the Wi-Fi Direct network to intercept the network password.

### CVE-2026-73438

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-16T10:16:51.690 |

On affected platforms running Arista EOS with Open Shortest Path First version 3 (OSPFv3) configured, an unauthenticated attacker on the same OSPFv3 broadcast domain can send a specially crafted set of packets that can cause the Ospf3 agent to restart unexpectedly. The crash results in the loss of all OSPFv3 adjacencies on the affected device and may disrupt routing across the broader OSPF domain until the agent recovers.

This issue was reported externally by Dravanet Inc., and Arista is not aware of any malicious exploitation of this vulnerability in customer networks.

### CVE-2026-73435

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-16T10:16:51.363 |

On affected platforms running Arista EOS with Open Shortest Path First version 2 (OSPFv2) configured, a specially crafted OSPFv2 packet from an unauthenticated attacker on the same broadcast segment, with OSPFv2 authentication configured can cause adjacency flapping and packet loss. The disruption can affect routing across the broader OSPF domain.

### CVE-2026-73450

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-16T03:16:59.437 |

On affected platforms running Arista EOS with MLAG Dual Primary Detection configured, an unauthenticated attacker with access to the Dual Primary Detection network segment can send specially crafted packets to interfere with the dual-primary state. If the MLAG primary switch fails while these packets are present, the secondary switch incorrectly concludes it is in a dual-primary condition and err-disables its interfaces, leading to a traffic interruption.

### CVE-2026-73460

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-16T00:17:05.397 |

On affected platforms running Arista EOS with IS-IS graceful restart enabled, an unauthenticated attacker who can inject a malformed IS-IS LSP PDU packet can cause the IS-IS graceful restart procedure to terminate prematurely. This may result in traffic loss following a restart event.

### CVE-2026-73459

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-354` |
| Published | 2026-09-16T00:17:05.213 |

On affected platforms running Arista EOS with IS-IS configured, an unauthenticated attacker who can inject a specially crafted IS-IS LSP PDU can cause the legitimate LSP to be unexpectedly purged from the IS-IS link-state database. This may result in traffic loss.

### CVE-2026-73446

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-696` |
| Published | 2026-09-16T00:17:05.000 |

On affected platforms running Arista EOS with IS-IS configured on a broadcast interface, an unauthenticated attacker can send a crafted IS-IS Hello Protocol Data Unit (PDU) that causes the device to tear down an established IS-IS adjacency. This may result in traffic disruption and loss of IP reachability for prefixes advertised through that adjacency.

### CVE-2026-83368

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T22:17:03.670 |

Vulnerability in the Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition, Oracle GraalVM product of Oracle Java SE (component: Compiler).   The supported version that is affected is Oracle GraalVM for JDK 17: 23.0.13.1; Oracle GraalVM for JDK 21: 23.1.12.1; Oracle GraalVM Enterprise Edition: 21.3.19.1; Oracle GraalVM: 25.0.4.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition, Oracle GraalVM.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition, Oracle GraalVM accessible data as well as  unauthorized update, insert or delete access to some of Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition, Oracle GraalVM accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition, Oracle GraalVM. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-76856

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-15T22:16:59.590 |

Netcore NR255-V firmware version 1.5.130703 contains a cross-site request forgery vulnerability affecting the wan_config_set_cgi, wan_num_set_cgi, and lan_ip_change_cgi endpoints. Attackers can craft forged requests to trick authenticated administrators into modifying WAN or LAN network configuration settings without consent.

### CVE-2026-87240

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:19:12.700 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83316

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:44.637 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).   The supported version that is affected is 26.01.0.0.0. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Business Intelligence Enterprise Edition executes to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83252

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:37.417 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-83239

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:35.910 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Commerce Guided Search / Oracle Commerce Experience Manager executes to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83231

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:34.960 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: helidon-dbclient-mongodb).  Supported versions that are affected are 3.0.0-3.2.20 and 4.0.0-4.5.4. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Helidon accessible data as well as  unauthorized update, insert or delete access to some of Helidon accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Helidon. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-83150

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:25.750 |

Vulnerability in Oracle Application Testing Suite.   The supported version that is affected is 13.3.0.1. Difficult to exploit vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Application Testing Suite executes to compromise Oracle Application Testing Suite.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Application Testing Suite. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-83015

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-15T20:18:08.303 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Cube Manager).  Supported versions that are affected are 8.61-8.63. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where PeopleSoft Enterprise PeopleTools executes to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-76693

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-15T20:17:51.773 |

A vulnerability in HPE Networking EdgeConnect SD-WAN Gateways could allow an unauthenticated remote attacker to cause a denial-of-service against certain services running on impacted Gateways.

### CVE-2026-58734

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-787` |
| Published | 2026-09-15T19:17:33.247 |

In google_mba_recv_msg of google_mba_poll.c, there is a possible out-of-bounds write due to a race condition. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58728

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-15T19:17:33.050 |

In ARM64_TLBI of mmu.h, there is a possible memory corruption due to a race condition. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58724

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-09-15T19:17:32.853 |

In multiple locations, there is a possible use-after-free due to a race condition. This could lead to local escalation of privilege with System execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58701

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-787` |
| Published | 2026-09-15T19:17:32.197 |

In trusty_dputc of generic-arm64-smcall.c, there is a possible out-of-bounds write due to a race condition. This could lead to local escalation of privilege with System execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-12150

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-15T18:17:13.597 |

IBM MQ 9.1.0.0 through 9.1.0.37 LTS, 9.2.0.0 through 9.2.0.43 LTS, 9.3.0.0 through 9.3.0.41 LTS, 9.3.0.0 through 9.3.5.1 CD, 9.4.0.0 through 9.4.0.25 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 could allow a remote attacker with a trusted TLS client certificate to cause a denial of service and potentially affect memory contents due to improper validation of deeply nested certificate data during TLS certificate processing.
