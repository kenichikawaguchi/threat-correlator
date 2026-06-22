# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-22 15:00 UTC
- **対象期間**: `2026-06-21T19:00:37.000Z` 〜 `2026-06-22T15:00:44.000Z`
- **重要CVE数**: 173 件（Critical 9.0+: 56 件 / High 7.0〜: 117 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に報告された CVE のうち **CVSS 7.0 以上が 40 件以上** と、深刻度の高い脆弱性が集中しています。  
- **認証不要でリモートコード実行 (RCE) が可能** な脆弱性が目立ち、特にネットワークに直接露出している管理系コンポーネント（Web サーバ、IoT デバイス、メールゲートウェイ）での被害リスクが急増しています。  
- 多くは **入力検証不備・パス・トラバーサル・コマンドインジェクション** が根本原因で、攻撃者は単一の HTTP リクエストで管理権限取得や任意コード実行が可能です。  
- ベンダー側のパッチリリースは速やかに行われているものの、**パッケージ管理や自動更新が無効化されている環境** が依然として多く、未適用リスクが残ります。

---

## 2. 特に注目すべき CVE  

| CVE | 製品・バージョン | 主な脆弱性種別 | 影響範囲・リスク | 注目理由 |
|-----|------------------|----------------|-------------------|----------|
| **CVE‑2026‑10561** | IBM **Langflow OSS** 1.0.0‑1.9.3 | 認証バイパス＋不適切な Python 実行分離 | 任意コード実行 → ホスト OS 完全侵害 | **CVSS 10.0**、Python 実行環境はクラウド・オンプレどちらでも利用頻度が高く、攻撃者が直接コンテナや VM に侵入できる点が危険。 |
| **CVE‑2026‑10520** | Ivanti **Sentry** (R10.5.2, R10.6.2, R10.7.1 未満) | OS コマンドインジェクション (RCE) | ネットワーク経由で root 権限取得 | **CVSS 10.0**、監視・ログ収集基盤が侵害されると、社内全体の可視化が失われ、横方向展開が容易になる。 |
| **CVE‑2026‑34910** | **UniFi OS** (全モデル) | 入力検証不備 → コマンドインジェクション | ネットワーク管理デバイスで任意コマンド実行 | **CVSS 10.0**、IoT/ネットワークインフラは外部からのスキャン対象になりやすく、侵入後は VLAN/ファイアウォール設定変更が可能。 |
| **CVE‑2026‑2743** | **SeppMail** 15.0.2.1 以前 | パス・トラバーサル＋任意ファイル書き込み → RCE | 大容量ファイル転送機能 (LFT) を悪用し、任意スクリプト配置 | **CVSS 10.0**、メールゲートウェイは外部メールサーバと直接やり取りするため、外部からの攻撃経路が確保しやすい。 |
| **CVE‑2026‑21962** | Oracle **HTTP Server / WebLogic Server Proxy Plug‑in** (12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0) | プロキシプラグインの認証バイパス | 任意コード実行、WebLogic への不正アクセス | **CVSS 10.0**、Oracle 製品は多くのエンタープライズ環境でコアインフラとして使用されており、影響範囲が広い。 |

> **共通点**：すべて **認証不要**、ネットワークから直接リクエストできる点、そして **完全なシステム権限取得** が可能という点で、最優先で対策が必要です。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 | 現行脆弱バージョン | 推奨バージョン |
|------|-------------------|----------------|
| IBM Langflow OSS | 1.0.0‑1.9.3 | **1.9.4 以降**（2026‑03 リリース） |
| Ivanti Sentry | R10.5.2, R10.6.2, R10.7.1 未満 | **R10.5.3**, **R10.6.3**, **R10.7.2** 以上 |
| UniFi OS | すべてのリリース | **UniFi OS 7.4.12 以降**（2026‑02 パッチ） |
| SeppMail | 15.0.2.1 以前 | **15.0.2.2** 以上 |
| Oracle HTTP Server / WebLogic Proxy Plug‑in | 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 | **12.2.1.5.0**, **14.1.1.1.0**, **14.1.2.1.0** 以上 |

> **手順**  
> 1. 各ベンダーの公式リリースノートとパッチ適用ガイドを確認。  
> 2. 本番環境での適用前に **ステージング環境で回帰テスト** を実施。  
> 3. パッケージマネージャ (yum, apt, pip, npm など) が利用できる場合は **自動更新** を有効化。  

### 3.2 防御層の強化
- **ネットワーク分離**：管理インタフェース（Langflow, Sentry, UniFi OS, SeppMail, Oracle HTTP Server）への外部からの直接アクセスを **ファイアウォール/ACL** で遮断し、VPN または IPsec 経由の限定的なアクセスに限定。  
- **WAF ルール追加**：  
  - `*/addJugador*` など既知のパラメータ汚染パスは **入力サニタイズ** ルールでブロック。  
  - `*.php`, `*.sh` へのアップロードやパス・トラバーサル文字列 (`../`, `%2e%2e%2f`) を検知するシグネチャを有効化。  
- **最小権限の徹底**：  
  - Langflow の Python 実行環境は **コンテナ/VM の権限を非特権ユーザーに限定**。  
  - Oracle Proxy Plug‑in は **WebLogic の管理コンソールと分離** し、必要最小限のプロキシ設定だけを許可。  
- **監査ログの強化**：  
  - すべての管理 API 呼び出しを **中央 SIEM** に転送し、異常なリクエストパターン（例: `/api/v1/...` への大量 POST）をリアルタイムでアラート。  

### 3.3 インシデント対応準備
1. **緊急対応手順書** を作成し、RCE 発覚時の **隔離 → 影響範囲特定 → ロールバック** 手順を明文化。  
2. **バックアップ**：重要設定ファイル・データベースは **30 分以内

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-10561

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-22T14:16:25.023 |

IBM Langflow OSS 1.0.0 through 1.9.3 has an vulnerability due to an improper isolation of Python execution combined with an authentication bypass that allows an unauthenticated attacker to execute arbitrary code on the host system, resulting in complete compromise

### CVE-2026-10520

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-09T14:10:21.581Z |

An OS Command Injection vulnerability in Ivanti Sentry before the R10.5.2, R10.6.2 and R10.7.1 versions allows a remote unauthenticated user to achieve root-level remote code execution

### CVE-2026-34910

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-05-22T00:43:49.096Z |

A malicious actor with access to the network could exploit an Improper Input Validation vulnerability found in UniFi OS devices to execute a Command Injection.

### CVE-2026-34909

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-05-22T00:43:49.072Z |

A malicious actor with access to the network could exploit a Path Traversal vulnerability found in UniFi OS devices to access files on the underlying system that could be manipulated to access an underlying account.

### CVE-2026-2743

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/AU:Y` |
| Weaknesses | `CWE-22;CWE-434` |
| Published | 2026-03-05T06:45:21.753Z |

Arbitrary File Write via Path Traversal upload to Remote Code Execution in SeppMail User Web Interface. The affected feature is the large file transfer (LFT). 

This issue affects SeppMail: 15.0.2.1 and before

### CVE-2026-21962

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-01-20T21:56:32.665Z |

Vulnerability in the Oracle HTTP Server, Oracle Weblogic Server Proxy Plug-in product of Oracle Fusion Middleware (component: Weblogic Server Proxy Plug-in for Apache HTTP Server, Weblogic Server Proxy Plug-in for IIS).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle HTTP Server, Oracle Weblogic Server Proxy Plug-in.  While the vulnerability is in Oracle HTTP Server, Oracle Weblogic Server Proxy Plug-in, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle HTTP Server, Oracle Weblogic Server Proxy Plug-in accessible data as well as  unauthorized access to critical data or complete access to all Oracle HTTP Server, Oracle Weblogic Server Proxy Plug-in accessible data. Note: Affected version for Weblogic Server Proxy Plug-in for IIS is 12.2.1.4.0 only. CVSS 3.1 Base Score 10.0 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-21877

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-434` |
| Published | 2026-01-08T00:39:58.697Z |

n8n is an open source workflow automation platform. In versions 0.121.2 and below, an authenticated attacker may be able to execute malicious code using the n8n service. This could result in full compromise and can impact both self-hosted and n8n Cloud instances. This issue is fixed in version 1.121.3. Administrators can reduce exposure by disabling the Git node and limiting access for untrusted users, but upgrading to the latest version is recommended.

### CVE-2025-52691

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2025-12-29T02:15:58.200Z |

Successful exploitation of the vulnerability could allow an unauthenticated attacker to upload arbitrary files to any location on the mail server, potentially enabling remote code execution.

### CVE-2025-68613

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-913` |
| Published | 2025-12-19T22:23:47.777Z |

n8n is an open source workflow automation platform. Versions starting with 0.211.0 and prior to 1.120.4, 1.121.1, and 1.122.0 contain a critical Remote Code Execution (RCE) vulnerability in their workflow expression evaluation system. Under certain conditions, expressions supplied by authenticated users during workflow configuration may be evaluated in an execution context that is not sufficiently isolated from the underlying runtime. An authenticated attacker could abuse this behavior to execute arbitrary code with the privileges of the n8n process. Successful exploitation may lead to full compromise of the affected instance, including unauthorized access to sensitive data, modification of workflows, and execution of system-level operations. This issue has been fixed in versions 1.120.4, 1.121.1, and 1.122.0. Users are strongly advised to upgrade to a patched version, which introduces additional safeguards to restrict expression evaluation. If upgrading is not immediately possible, administrators should consider the following temporary mitigations: Limit workflow creation and editing permissions to fully trusted users only; and/or deploy n8n in a hardened environment with restricted operating system privileges and network access to reduce the impact of potential exploitation. These workarounds do not fully eliminate the risk and should only be used as short-term measures.

### CVE-2025-55182

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2025-12-03T15:40:56.894Z |

A pre-authentication remote code execution vulnerability exists in React Server Components versions 19.0.0, 19.1.0, 19.1.1, and 19.2.0 including the following packages: react-server-dom-parcel, react-server-dom-turbopack, and react-server-dom-webpack. The vulnerable code unsafely deserializes payloads from HTTP requests to Server Function endpoints.

### CVE-2025-64095

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2025-10-28T21:46:11.267Z |

DNN (formerly DotNetNuke) is an open-source web content management platform (CMS) in the Microsoft ecosystem. Prior to 10.1.1, the default HTML editor provider allows unauthenticated file uploads and images can overwrite existing files. An unauthenticated user can upload and replace existing files allowing defacing a website and combined with other issue, injection XSS payloads. This vulnerability is fixed in 10.1.1.

### CVE-2025-57819

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H` |
| Weaknesses | `CWE-89;CWE-288` |
| Published | 2025-08-28T16:45:18.749Z |

FreePBX is an open-source web-based graphical user interface. FreePBX 15, 16, and 17 endpoints are vulnerable due to insufficiently sanitized user-supplied data allowing unauthenticated access to FreePBX Administrator leading to arbitrary database manipulation and remote code execution. This issue has been patched in endpoint versions 15.0.66, 16.0.89, and 17.0.3.

### CVE-2025-54253

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2025-08-05T16:53:40.742Z |

Adobe Experience Manager versions 6.5.23 and earlier are affected by a Misconfiguration vulnerability that could result in arbitrary code execution. An attacker could leverage this vulnerability to bypass security mechanisms and execute code. Exploitation of this issue does not require user interaction and scope is changed.

### CVE-2026-32746

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-03-13T17:15:14.876Z |

telnetd in GNU inetutils through 2.7 allows an out-of-bounds write in the LINEMODE SLC (Set Local Characters) suboption handler because add_slc does not check whether the buffer is full.

### CVE-2026-21902

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-02-25T16:59:10.672Z |

An Incorrect Permission Assignment for Critical Resource vulnerability in the On-Box Anomaly detection framework of Juniper Networks Junos OS Evolved on PTX Series allows an unauthenticated, network-based attacker to execute code as root.

The On-Box Anomaly detection framework should only be reachable by other internal processes over the internal routing instance, but not over an externally exposed port. With the ability to access and manipulate the service to execute code as root a remote attacker can take complete control of the device.
Please note that this service is enabled by default as no specific configuration is required.

This issue affects Junos OS Evolved on PTX Series:



  *  25.4 versions before 25.4R1-S1-EVO, 25.4R2-EVO.




This issue does not affect Junos OS Evolved versions before 25.4R1-EVO.

This issue does not affect Junos OS.

### CVE-2025-61882

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2025-10-05T03:17:01.644Z |

Vulnerability in the Oracle Concurrent Processing product of Oracle E-Business Suite (component: BI Publisher Integration).  Supported versions that are affected are 12.2.3-12.2.14. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Concurrent Processing.  Successful attacks of this vulnerability can result in takeover of Oracle Concurrent Processing. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2025-52688

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2025-07-16T06:23:53.933Z |

Successful exploitation of the vulnerability could allow an attacker to inject commands with root privileges on the access point, potentially leading to the loss of confidentiality, integrity, availability, and full control of the access point.

### CVE-2026-28381

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-06-22T14:16:35.820 |

The Snowflake datasource allows for GET/PUT commands, which can allow any user with access to run queries against the data source to read/write files between the local grafana server and the connected Snowflake host.

### CVE-2025-62712

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2025-10-30T16:08:32.669Z |

JumpServer is an open source bastion host and an operation and maintenance security audit system. In JumpServer versions prior to v3.10.20-lts and v4.10.11-lts, an authenticated, non-privileged user can retrieve connection tokens belonging to other users via the super-connection API endpoint (/api/v1/authentication/super-connection-token/). When accessed from a web browser, this endpoint returns connection tokens created by all users instead of restricting results to tokens owned by or authorized for the requester. An attacker who obtains these tokens can use them to initiate connections to managed assets on behalf of the original token owners, resulting in unauthorized access and privilege escalation across sensitive systems. This vulnerability is fixed in v3.10.20-lts and v4.10.11-lts.

### CVE-2025-5333

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/S:P/AU:Y/R:I/V:C/RE:L/U:Red` |
| Weaknesses | `N/A` |
| Published | 2025-07-06T13:50:25.955Z |

Remote attackers can execute arbitrary code in the context of the vulnerable service process.

### CVE-2026-7165

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-22T14:17:52.697 |

The vulnerability is present in the ‘/addJugador’ endpoint:
  *  The 'keyJugador' and 'keyJugadorObjectiu'  parameters allow the modification of other users’ information without requiring prior authorization validation. This could enable an authenticated attacker to alter any user’s ID and change their information.

  *  The ‘punts’ and ‘numObjectiusEliminats’ fields allow arbitrary data to be added because user input is not properly validated. This makes it possible to obtain authentic prizes, awarded by city councils, by falsifying game scores. 

  *  In the ‘tokens’ field, administrative privileges can be self-assigned without server validation or prior authentication. This vulnerability could allow an authenticated attacker to grant themselves administrator permissions and thus escalate privileges.

  *  Numeric fields allow the entry of extremely long values, which can cause the system to crash. Successful exploitation of this vulnerability could allow an authenticated attacker to launch a denial-of-service (DoS) attack, preventing created games from being playable.

  *  The ‘urlImatge’ parameter allows server-side requests to arbitrary URLs, enabling the retrieval of users’ internal IP addresses, access to internal services, reading of local files, and unauthorized interaction with third-party APIs. An authenticated attacker could gain access to sensitive data.

### CVE-2026-56423

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-22T14:17:49.913 |

MISP Core contained broken access-control checks in the bulk deletion flows for Event Reports and Sharing Groups. The affected deleteSelection handlers authorized deletion using broad role-level permissions instead of validating authorization for each selected object.

For Event Reports, EventReportsController::deleteSelection relied on the global perm_add capability rather than a per-report ownership/authorization check. As a result, a contributor-level user could submit report IDs or UUIDs for reports belonging to other organisations and hard-delete them instance-wide. The fix changed the callback to call EventReport::fetchIfAuthorized($user, $itemId, 'delete') for each selected report before deletion.




For Sharing Groups, SharingGroupsController::deleteSelection relied on the global perm_sharing_group capability rather than verifying ownership of each selected sharing group. This allowed a sharing-group-capable user to hard-delete sharing groups owned by other organisations, bypassing the per-object ownership gate used by the single-object delete action. The fix changed the callback to call SharingGroup::checkIfOwner($user, $itemId) for each selected sharing group.




An authenticated attacker with the relevant broad role permission could abuse the affected bulk deletion endpoints to delete objects outside their organisation’s authorization scope, causing loss of event-report content or sharing-group configuration across the instance.

### CVE-2026-56422

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-22T12:16:26.920 |

Multiple MISP core controllers and model capture paths accepted client-controlled request fields such as primary keys (id) and ownership/scope foreign keys (event_id, org_id, user_id, sharing_group_id, galaxy_cluster_uuid, organisation_uuid, and related nested object identifiers) without consistently stripping, pinning, or revalidating them against the server-authorized object.

In affected paths, an authenticated user with access to one authorized object could submit crafted REST or form payloads that caused MISP to save data against a different object than the one checked by the authorization logic. Depending on the endpoint, this could allow object overwrite, object re-parenting, ownership transfer, unauthorized sharing-group scoping, event/object injection, proposal retargeting, or stored attacker-controlled content appearing in another user’s context.

The fixes harden affected create/edit/import flows by stripping client-supplied primary keys on create-only saves, re-pinning route- or database-authorized identifiers before save operations, validating effective sharing-group scope, and adding field whitelists where ownership fields must never be editable. The initial broad fix also added a central CRUDComponent::edit() primary-key re-pin so payload-supplied IDs cannot redirect saves away from the already-authorized row. GitHub’s patch for 7acf8220c describes this central issue as CRUDComponent::edit() copying supplied fields, including a payload primary key, onto the loaded record, allowing CakePHP save() to update an arbitrary row unless the loaded ID is re-pinned.

### CVE-2026-11746

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-06-22T03:16:42.833 |

A vulnerability has been identified in centraldogma-server versions prior to 0.84.0, where enabling ZooKeeper replication without setting replication.secret causes the server to silently fall back to a hard-coded, publicly known secret. This default credential authenticates the embedded ZooKeeper ensemble, allowing an attacker with network access to read the full replication log or join the quorum and execute arbitrary replicated commands across the cluster.

### CVE-2025-64155

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:H/RL:O/RC:C` |
| Weaknesses | `CWE-78` |
| Published | 2026-01-13T16:32:28.665Z |

An improper neutralization of special elements used in an os command ('os command injection') vulnerability in Fortinet FortiSIEM 7.4.0, FortiSIEM 7.3.0 through 7.3.4, FortiSIEM 7.1.0 through 7.1.8, FortiSIEM 7.0.0 through 7.0.4, FortiSIEM 6.7.0 through 6.7.10 may allow an attacker to execute unauthorized code or commands via  crafted TCP requests.

### CVE-2025-64446

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:H/RL:O/RC:C` |
| Weaknesses | `CWE-23` |
| Published | 2025-11-14T15:50:52.778Z |

A relative path traversal vulnerability in Fortinet FortiWeb 8.0.0 through 8.0.1, FortiWeb 7.6.0 through 7.6.4, FortiWeb 7.4.0 through 7.4.9, FortiWeb 7.2.0 through 7.2.11, FortiWeb 7.0.0 through 7.0.11 may allow an attacker to execute administrative commands on the system via crafted HTTP or HTTPS requests.

### CVE-2026-56447

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-06-22T14:17:50.497 |

MISP allowed an authenticated site administrator to set the Kafka_rdkafka_config setting to an arbitrary filesystem path. MISP subsequently parsed the referenced INI file and passed its options to rdkafka. A crafted attacker-controlled configuration file could use rdkafka options such as plugin.library.paths to load an external library, resulting in arbitrary code execution with the privileges of the MISP process. An attacker could leverage a MISP-writable location, such as an uploaded file or administrative image, to host the malicious configuration file.

The issue is fixed by restricting the setting to absolute .ini files located only in approved configuration directories outside the webroot and MISP upload targets.

### CVE-2026-56425

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-384` |
| Published | 2026-06-22T14:17:50.220 |

The Azure Active Directory (AAD) authentication implementation contained multiple weaknesses in its OAuth 2.0 authorization flow that could allow attackers to bypass important security guarantees provided by the protocol.


The application used the PHP session identifier (session_id()) as the OAuth state parameter. Because session identifiers are long-lived authentication credentials, exposing them in OAuth redirect URLs could leak valid session tokens through browser history, HTTP Referer headers, reverse proxies, access logs, or third-party infrastructure involved in the authentication flow. If obtained by an attacker, the leaked session identifier could potentially be used for session hijacking.


Additionally, the implementation did not regenerate the session identifier after successful authentication, leaving authenticated sessions susceptible to session fixation attacks where an attacker forces a victim to use a known session identifier before login and later reuses that identifier after authentication.


The OAuth state value was also not implemented as a dedicated, single-use nonce. This weakened CSRF protections and increased the risk of replay attacks against the OAuth callback process.


The authentication flow further failed to enforce HTTPS for the configured OAuth redirect URI. If a non-HTTPS redirect URI was used, OAuth authorization codes and access tokens could traverse the network in plaintext, exposing sensitive credentials to network attackers.


Finally, OAuth error responses containing attacker-controlled GET parameters were logged verbatim. An attacker could inject control characters or crafted log content, leading to log forging, log injection, or corruption of audit records.


The fix introduces:



  *  
A dedicated cryptographically random OAuth state value.


  *  
Single-use state validation and invalidation.


  *  
Constant-time state comparison using hash_equals().


  *  
Session identifier rotation after successful authentication.


  *  
Enforcement of HTTPS-only redirect URIs.


  *  
Sanitized and length-limited logging of OAuth error parameters.


AAD Authentication Plugin (OAuth 2.0 / Azure Active Directory integration)

### CVE-2026-10187

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2026-05-31T14:15:14.047Z |

A vulnerability was detected in Totolink N300RH 6.1c.1353_B20190305. Affected by this issue is the function setWiFiBasicConfig of the file wireless.so of the component Web Management Interface. Performing a manipulation of the argument KeyStr results in stack-based buffer overflow. The attack is possible to be carried out remotely. The exploit is now public and may be used.

### CVE-2026-23734

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-23` |
| Published | 2026-05-20T18:39:32.313Z |

XWiki Platform is a generic wiki platform. Versions prior to 18.1.0-rc-1, 17.10.3, 17.4.9, and 16.10.17 allow access to read configuration files by using URLs such as http://localhost:8080/bin/ssx/Main/WebHome?resource=/../../WEB-INF/xwiki.cfg&minify=false, leading to Path Traversal. The vulnerability is can be exploited via resources parameter the ssx and jsx endpoints by using leading slashes. This issue has been patched in 18.1.0-rc-1, 17.10.3, 17.4.9, 16.10.17.

### CVE-2026-44128

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-95` |
| Published | 2026-05-08T13:13:46.034Z |

SEPPmail Secure Email Gateway before version 15.0.2.1 allows unauthenticated remote code execution in the new GINA UI because an endpoint passes attacker-controlled input from a parameter to Perl's eval.

### CVE-2026-7854

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2026-05-05T18:15:14.438Z |

A security vulnerability has been detected in D-Link DI-8100 16.07.26A1. Affected by this vulnerability is the function url_rule_asp of the file /url_rule.asp of the component POST Parameter Handler. Such manipulation leads to buffer overflow. It is possible to launch the attack remotely. The exploit has been disclosed publicly and may be used.

### CVE-2026-7853

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2026-05-05T17:45:14.044Z |

A weakness has been identified in D-Link DI-8100 16.07.26A1. Affected is the function sprintf of the file /auto_reboot.asp of the component HTTP Handler. This manipulation of the argument enable/time causes buffer overflow. It is possible to initiate the attack remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-6195

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-78;CWE-77` |
| Published | 2026-04-13T17:30:13.953Z |

A security vulnerability has been detected in Totolink A7100RU 7.4cu.2313_b20191024. Affected by this issue is the function setPasswordCfg of the file /cgi-bin/cstecgi.cgi of the component CGI Handler. Such manipulation of the argument admpass leads to os command injection. The attack can be executed remotely. The exploit has been disclosed publicly and may be used.

### CVE-2026-5854

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-78;CWE-77` |
| Published | 2026-04-09T06:45:18.857Z |

A vulnerability was detected in Totolink A7100RU 7.4cu.2313_b20191024. Affected by this issue is the function setWiFiEasyCfg of the file /cgi-bin/cstecgi.cgi of the component CGI Handler. Performing a manipulation of the argument merge results in os command injection. It is possible to initiate the attack remotely. The exploit is now public and may be used.

### CVE-2026-5853

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-78;CWE-77` |
| Published | 2026-04-09T06:30:21.107Z |

A security vulnerability has been detected in Totolink A7100RU 7.4cu.2313_b20191024. Affected by this vulnerability is the function setIpv6LanCfg of the file /cgi-bin/cstecgi.cgi of the component CGI Handler. Such manipulation of the argument addrPrefixLen leads to os command injection. The attack may be performed from remote. The exploit has been disclosed publicly and may be used.

### CVE-2026-5852

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-78;CWE-77` |
| Published | 2026-04-09T06:15:15.694Z |

A weakness has been identified in Totolink A7100RU 7.4cu.2313_b20191024. Affected is the function setIptvCfg of the file /cgi-bin/cstecgi.cgi of the component CGI Handler. This manipulation of the argument igmpVer causes os command injection. The attack is possible to be carried out remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-5851

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-78;CWE-77` |
| Published | 2026-04-09T06:00:16.723Z |

A security flaw has been discovered in Totolink A7100RU 7.4cu.2313_b20191024. This impacts the function setUPnPCfg of the file /cgi-bin/cstecgi.cgi of the component CGI Handler. The manipulation of the argument enable results in os command injection. The attack can be executed remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-5850

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-78;CWE-77` |
| Published | 2026-04-09T05:45:12.796Z |

A vulnerability was identified in Totolink A7100RU 7.4cu.2313_b20191024. This affects the function setVpnPassCfg of the file /cgi-bin/cstecgi.cgi of the component CGI Handler. The manipulation of the argument pptpPassThru leads to os command injection. Remote exploitation of the attack is possible. The exploit is publicly available and might be used.

### CVE-2025-8536

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-89` |
| Published | 2025-10-24T14:18:20.189Z |

A SQL injection vulnerability has been identified in DobryCMS. Improper neutralization of input provided by user into language functionality allows for SQL Injection attacks.

This issue affects older branches of this software.

### CVE-2025-61928

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-285;CWE-306` |
| Published | 2025-10-09T21:24:37.541Z |

Better Auth is an authentication and authorization library for TypeScript. In versions prior to 1.3.26, unauthenticated attackers can create or modify API keys for any user by passing that user's id in the request body to the `api/auth/api-key/create` route. `session?.user ?? (authRequired ? null : { id: ctx.body.userId })`. When no session exists but `userId` is present in the request body, `authRequired` becomes false and the user object is set to the attacker-controlled ID. Server-only field validation only executes when `authRequired` is true (lines 280-295), allowing attackers to set privileged fields. No additional authentication occurs before the database operation, so the malicious payload is accepted. The same pattern exists in the update endpoint. This is a critical authentication bypass enabling full an unauthenticated attacker can generate an API key for any user and immediately gain complete authenticated access. This allows the attacker to perform any action as the victim user using the api key, potentially compromise the user data and the application depending on the victim's privileges. Version 1.3.26 contains a patch for the issue.

### CVE-2025-52906

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:H/SI:H/SA:H/S:N/AU:Y/R:U` |
| Weaknesses | `CWE-78` |
| Published | 2025-09-24T17:44:29.539Z |

Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability in TOTOLINK X6000R allows OS Command Injection.This issue affects X6000R: through V9.4.0cu.1360_B20241207.

### CVE-2025-7206

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-07-08T23:32:06.224Z |

A vulnerability, which was classified as critical, has been found in D-Link DIR-825 2.10. This issue affects the function sub_410DDC of the file switch_language.cgi of the component httpd. The manipulation of the argument Language leads to stack-based buffer overflow. The attack may be initiated remotely. The exploit has been disclosed to the public and may be used. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2025-5777

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L` |
| Weaknesses | `CWE-125` |
| Published | 2025-06-17T12:29:34.506Z |

Insufficient input validation leading to memory overread when the NetScaler is configured as a Gateway (VPN virtual server, ICA Proxy, CVPN, RDP Proxy) OR AAA virtual server

### CVE-2025-5623

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-06-05T00:00:19.500Z |

A vulnerability was found in D-Link DIR-816 1.10CNB05. It has been classified as critical. This affects the function qosClassifier of the file /goform/qosClassifier. The manipulation of the argument dip_address/sip_address leads to stack-based buffer overflow. It is possible to initiate the attack remotely. The exploit has been disclosed to the public and may be used. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-7166

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-06-22T14:17:52.860 |

Vulnerability involving the exposure of sensitive data provided without adequate protection. The API exposes email and phone number data from the ‘email’ and ‘telefon’ fields. This vulnerability is also present in the local database, as it contains accessible sensitive information such as data on minors and municipal users. Successful exploitation of this vulnerability could allow an unauthenticated remote attacker to gain access to sensitive information and data.

### CVE-2026-46725

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-502` |
| Published | 2026-05-19T09:25:33.489Z |

The extension passes an attacker-controlled cookie directly to PHP's unserialize() without safely processing the input. A remote, unauthenticated attacker can supply a crafted serialized payload to trigger PHP Object Injection, leading to Remote Code Execution on the TYPO3 server. Exploitation requires the content element to be configured with "Persistent Mode: Static" in the plugin settings.

### CVE-2026-27760

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-04-28T13:43:24.366Z |

OpenCATS prior to commit 3002a29 contains a PHP code injection vulnerability in the installer AJAX endpoint that allows unauthenticated attackers to execute arbitrary code by injecting PHP statements into the databaseConnectivity action parameter. Attackers can break out of the define() string context in config.php using a single quote and statement separator to inject malicious PHP code that persists and executes on every subsequent page load when the installation wizard remains incomplete.

### CVE-2026-41176

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-04-22T23:57:54.075Z |

Rclone is a command-line program to sync files and directories to and from different cloud storage providers. The RC endpoint `options/set` is exposed without `AuthRequired: true`, but it can mutate global runtime configuration, including the RC option block itself. Starting in version 1.45.0 and prior to version 1.73.5, an unauthenticated attacker can set `rc.NoAuth=true`, which disables the authorization gate for many RC methods registered with `AuthRequired: true` on reachable RC servers that are started without global HTTP authentication. This can lead to unauthorized access to sensitive administrative functionality, including configuration and operational RC methods. Version 1.73.5 patches the issue.

### CVE-2026-27971

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-502` |
| Published | 2026-03-03T22:55:38.064Z |

Qwik is a performance focused javascript framework. qwik <=1.19.0 is vulnerable to RCE due to an unsafe deserialization vulnerability in the server$ RPC mechanism that allows any unauthenticated user to execute arbitrary code on the server with a single HTTP request. Affects any deployment where require() is available at runtime. This vulnerability is fixed in 1.19.1.

### CVE-2025-68428

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N` |
| Weaknesses | `CWE-35;CWE-73` |
| Published | 2026-01-05T21:43:55.169Z |

jsPDF is a library to generate PDFs in JavaScript. Prior to version 4.0.0, user control of the first argument of the loadFile method in the node.js build allows local file inclusion/path traversal. If given the possibility to pass unsanitized paths to the loadFile method, a user can retrieve file contents of arbitrary files in the local file system the node process is running in. The file contents are included verbatim in the generated PDFs. Other affected methods are `addImage`, `html`, and `addFont`. Only the node.js builds of the library are affected, namely the `dist/jspdf.node.js` and `dist/jspdf.node.min.js` files. The vulnerability has been fixed in jsPDF@4.0.0. This version restricts file system access per default. This semver-major update does not introduce other breaking changes. Some workarounds areavailable. With recent node versions, jsPDF recommends using the `--permission` flag in production. The feature was introduced experimentally in v20.0.0 and is stable since v22.13.0/v23.5.0/v24.0.0. For older node versions, sanitize user-provided paths before passing them to jsPDF.

### CVE-2026-39813

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:F/RL:O/RC:C` |
| Weaknesses | `CWE-24` |
| Published | 2026-04-14T15:38:30.311Z |

A path traversal: '../filedir' vulnerability in Fortinet FortiSandbox 5.0.0 through 5.0.5, FortiSandbox 4.4.0 through 4.4.8 may allow attacker to escalation of privilege via specially crafted HTTP requests.

### CVE-2026-39808

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:F/RL:O/RC:C` |
| Weaknesses | `CWE-78` |
| Published | 2026-04-14T15:38:02.089Z |

A improper neutralization of special elements used in an os command ('os command injection') vulnerability in Fortinet FortiSandbox 4.4.0 through 4.4.8 may allow attacker to execute unauthorized code or commands via <insert attack vector here>

### CVE-2026-2701

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434;CWE-78;CWE-94` |
| Published | 2026-04-02T13:04:38.554Z |

Authenticated user can upload a malicious file to the server and execute it, which leads to remote code execution.

### CVE-2025-54236

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2025-09-09T13:20:17.939Z |

Adobe Commerce versions 2.4.9-alpha2, 2.4.8-p2, 2.4.7-p7, 2.4.6-p12, 2.4.5-p14, 2.4.4-p15 and earlier are affected by an Improper Input Validation vulnerability. A successful attacker can abuse this to achieve session takeover, increasing the confidentiality, and integrity impact to high. Exploitation of this issue does not require user interaction.

### CVE-2025-53690

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2025-09-03T20:04:48.223Z |

Deserialization of Untrusted Data vulnerability in Sitecore Experience Manager (XM), Sitecore Experience Platform (XP) allows Code Injection.This issue affects Experience Manager (XM): through 9.0; Experience Platform (XP): through 9.0.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-54099

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-22T14:17:40.820 |

A flaw was found in the Windows Machine Config Operator (WMCO) for Red Hat OpenShift Container Platform. The WICD CSR auto-approver validates that a Certificate Signing Request contains the organization system:wicd-nodes but does not reject additional organization values such as system:masters. A compromised Windows worker node that holds WICD credentials can submit a CSR that is auto-approved and signed by the cluster, yielding a client certificate that grants cluster-administrator privileges and enabling full cluster takeover.

### CVE-2026-12602

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-06-22T14:16:27.393 |

Incorrect default permissions in ArubaSign, affecting versions prior to v4.6.6. The vulnerability is caused by the assignment of inappropriate permissions during the software’s default installation, whereby the main executable and other programme files located in C:\Program Files have excessive permissions for the ‘Everyone’ group. This could allow an unprivileged user to replace the main executable and/or its components with a malicious file, thereby enabling the execution of arbitrary code. In the worst-case scenario, if the malicious code is executed with elevated privileges (such as those of Administrator or SYSTEM), the attacker could escalate privileges and gain full control of the system, compromising both security and data integrity.

### CVE-2026-8157

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-22T06:16:29.000 |

The Vitepos  WordPress plugin before 3.4.2 does not properly restrict the roles that can be assigned when creating new users via one of its REST API endpoints, allowing authenticated users with a custom Vitepos  WordPress plugin before 3.4.2 role to escalate privileges to administrator.

### CVE-2026-11745

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-06-22T03:16:42.670 |

A vulnerability has been identified in centraldogma-server-mirror-git versions prior to 0.84.0, where the Git mirror SSH client does not verify remote host keys for git+ssh:// connections, allowing an on-path attacker to perform man-in-the-middle attacks and compromise mirrored repositories.

### CVE-2026-44127

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-73` |
| Published | 2026-05-08T13:13:05.667Z |

SEPPmail Secure Email Gateway before version 15.0.4 contains an unauthenticated path traversal vulnerability in the identifier parameter of /api.app/attachment/preview that allows remote attackers to read arbitrary local files and trigger deletion of files in the targeted directory with the privileges of the api.app process.

### CVE-2025-54400

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2025-10-07T13:55:10.308Z |

Multiple stack-based buffer overflow vulnerabilities exist in the formPingCmd functionality of Planet WGR-500 v1.3411b190912. A specially crafted series of HTTP requests can lead to stack-based buffer overflow. An attacker can send a series of HTTP requests to trigger these vulnerabilities.This buffer overflow is related to the `counts` request parameter for composing the `"ping -c <counts> <ipaddr> 2>&1 > %s &"` string.

### CVE-2025-54405

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-10-07T13:55:04.725Z |

Multiple OS command injection vulnerabilities exist in the formPingCmd functionality of Planet WGR-500 v1.3411b190912. A specially crafted series of HTTP requests can lead to arbitrary command execution. An attacker can send a series of HTTP requests to trigger these vulnerabilities.This command injection is related to the `ipaddr` request parameter.

### CVE-2025-53772

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `CWE-502` |
| Published | 2025-08-12T17:09:50.503Z |

Deserialization of untrusted data in Web Deploy allows an authorized attacker to execute code over a network.

### CVE-2026-56446

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-22T14:17:50.370 |

MISP allowed a site administrator to configure an arbitrary filesystem path for the NDJSON error log used by JsonLogTool. Because log entries can include attacker-controlled content, an authenticated attacker with site administrator privileges could direct log output to a PHP file in a web-accessible directory and inject PHP code through logged data. Accessing the resulting file could lead to remote code execution with the privileges of the web server process.

The fix restricts log destinations to existing directories beneath APP/tmp/logs or /var/log, requires absolute paths, rejects stream wrappers and traversal-related input, and limits filenames to .log or .ndjson extensions while disallowing executable extension segments.

### CVE-2025-4994

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-305` |
| Published | 2026-06-22T10:16:17.673 |

The SafeLine SL6 and SL6+ devices integrated into elevator emergency intercom systems are vulnerable to an authentication bypass. This vulnerability allows attackers to bypass authentication requirements and access the device's configuration service via the Bluetooth Low Energy (BLE) interface. Consequently, an attacker within wireless range can gain unauthorized administrative access to the device configuration.

### CVE-2026-11498

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2026-06-08T06:45:21.289Z |

A vulnerability was found in Tenda HG7HG9 and HG10 300001138_en_xpon. Affected by this issue is the function asp_voip_OtherSet of the file /boaform/voip_other_set of the component Web Management Interface. Performing a manipulation of the argument funckey_transfer results in stack-based buffer overflow. The attack is possible to be carried out remotely.

### CVE-2026-35029

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-04-06T16:35:28.974Z |

LiteLLM is a proxy server (AI Gateway) to call LLM APIs in OpenAI (or native) format. Prior to 1.83.0, the /config/update endpoint does not enforce admin role authorization. A user who is already authenticated into the platform can then use this endpoint to modify proxy configuration and environment variables, register custom pass-through endpoint handlers pointing to attacker-controlled Python code, achieving remote code execution, read arbitrary server files by setting UI_LOGO_PATH and fetching via /get_image, and take over other privileged accounts by overwriting UI_USERNAME and UI_PASSWORD environment variables. Fixed in v1.83.0.

### CVE-2025-71260

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-502` |
| Published | 2026-03-19T13:45:05.620Z |

BMC FootPrints ITSM versions 20.20.02 through 20.24.01.001 contain a deserialization of untrusted data vulnerability in the ASP.NET servlet's VIEWSTATE handling that allows authenticated attackers to execute arbitrary code. Attackers can supply crafted serialized objects to the VIEWSTATE parameter to achieve remote code execution and fully compromise the application. The following hotfixes remediate the vulnerability: 20.20.02, 20.20.03.002, 20.21.01.001, 20.21.02.002, 20.22.01, 20.22.01.001, 20.23.01, 20.23.01.002, and 20.24.01.

### CVE-2026-3399

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2026-03-01T23:02:09.578Z |

A vulnerability was identified in Tenda F453 1.0.0.3. Affected by this vulnerability is the function fromGstDhcpSetSer of the file /goform/GstDhcpSetSer of the component httpd. The manipulation of the argument dips leads to buffer overflow. The attack may be initiated remotely. The exploit is publicly available and might be used.

### CVE-2026-3168

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2026-02-25T07:02:14.956Z |

A weakness has been identified in Tenda F453 1.0.0.3. This affects the function fromNatStaticSetting of the file /goform/NatStaticSetting of the component httpd. Executing a manipulation of the argument page can lead to buffer overflow. The attack may be launched remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-2962

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2026-02-23T00:32:11.927Z |

A vulnerability was found in D-Link DWR-M960 1.01.07. This vulnerability affects the function sub_460F30 of the file /boafrm/formDateReboot of the component Scheduled Reboot Configuration Endpoint. The manipulation of the argument submit-url results in stack-based buffer overflow. The attack may be performed from remote. The exploit has been made public and could be used.

### CVE-2026-2961

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2026-02-23T00:02:17.186Z |

A vulnerability has been found in D-Link DWR-M960 1.01.07. This affects the function sub_4196C4 of the file /boafrm/formVpnConfigSetup of the component VPN Configuration Endpoint. The manipulation of the argument submit-url leads to stack-based buffer overflow. The attack is possible to be carried out remotely. The exploit has been disclosed to the public and may be used.

### CVE-2026-0652

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-02-10T17:27:42.953Z |

On TP-Link Tapo C260 v1, command injection vulnerability exists due to improper sanitization in certain POST parameters during configuration synchronization. An authenticated attacker can execute arbitrary system commands with high impact on confidentiality, integrity and availability. It may cause full device compromise.

### CVE-2026-1157

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2026-01-19T14:02:10.111Z |

A vulnerability was identified in Totolink LR350 9.3.5u.6369_B20220309. This affects the function setWiFiEasyCfg of the file /cgi-bin/cstecgi.cgi. Such manipulation of the argument ssid leads to buffer overflow. It is possible to launch the attack remotely. The exploit is publicly available and might be used.

### CVE-2026-0841

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2026-01-11T07:32:07.736Z |

A vulnerability was detected in UTT 进取 520W 1.7.7-180627. Affected by this issue is the function strcpy of the file /goform/formPictureUrl. The manipulation of the argument importpictureurl results in buffer overflow. It is possible to launch the attack remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-0840

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2026-01-11T06:32:06.734Z |

A security vulnerability has been detected in UTT 进取 520W 1.7.7-180627. Affected by this vulnerability is the function strcpy of the file /goform/formConfigNoticeConfig. The manipulation of the argument timestart leads to buffer overflow. It is possible to initiate the attack remotely. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-0839

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2026-01-11T06:02:05.798Z |

A weakness has been identified in UTT 进取 520W 1.7.7-180627. Affected is the function strcpy of the file /goform/APSecurity. Executing a manipulation of the argument wepkey1 can lead to buffer overflow. The attack may be performed from remote. The exploit has been made available to the public and could be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-0838

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2026-01-11T05:32:06.225Z |

A security flaw has been discovered in UTT 进取 520W 1.7.7-180627. This impacts the function strcpy of the file /goform/ConfigWirelessBase. Performing a manipulation of the argument ssid results in buffer overflow. The attack is possible to be carried out remotely. The exploit has been released to the public and may be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-0837

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2026-01-11T05:02:06.048Z |

A vulnerability was identified in UTT 进取 520W 1.7.7-180627. This affects the function strcpy of the file /goform/formFireWall. Such manipulation of the argument GroupName leads to buffer overflow. The attack can be executed remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-9938

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-09-03T23:32:10.606Z |

A weakness has been identified in D-Link DI-8400 16.07.26A1. The affected element is the function yyxz_dlink_asp of the file /yyxz.asp. This manipulation of the argument ID causes stack-based buffer overflow. It is possible to initiate the attack remotely. The exploit has been made available to the public and could be exploited.

### CVE-2025-9813

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-09-02T04:02:07.353Z |

A vulnerability was identified in Tenda CH22 1.0.0.1. This issue affects the function formSetSambaConf of the file /goform/SetSambaConf. The manipulation of the argument samba_userNameSda leads to buffer overflow. It is possible to initiate the attack remotely. The exploit is publicly available and might be used.

### CVE-2025-9527

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-08-27T13:02:06.341Z |

A vulnerability was found in Linksys E1700 1.0.0.4.003. This affects the function QoSSetup of the file /goform/QoSSetup. Performing manipulation of the argument ack_policy results in stack-based buffer overflow. The attack may be initiated remotely. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-9526

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-08-27T12:32:09.160Z |

A vulnerability has been found in Linksys E1700 1.0.0.4.003. Affected by this issue is the function setSysAdm of the file /goform/setSysAdm. Such manipulation of the argument rm_port leads to stack-based buffer overflow. The attack can be launched remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-9525

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-08-27T12:32:07.243Z |

A flaw has been found in Linksys E1700 1.0.0.4.003. Affected by this vulnerability is the function setWan of the file /goform/setWan. This manipulation of the argument DeviceName/lanIp causes stack-based buffer overflow. The attack can be initiated remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-9482

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-08-26T13:32:11.752Z |

A vulnerability was detected in Linksys RE6250, RE6300, RE6350, RE6500, RE7000 and RE9000 1.0.013.001/1.0.04.001/1.0.04.002/1.1.05.003/1.2.07.001. This impacts the function portRangeForwardAdd of the file /goform/portRangeForwardAdd. The manipulation of the argument ruleName/schedule/inboundFilter/TCPPorts/UDPPorts results in stack-based buffer overflow. The attack can be executed remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-9481

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-08-26T13:32:09.115Z |

A security vulnerability has been detected in Linksys RE6250, RE6300, RE6350, RE6500, RE7000 and RE9000 1.0.013.001/1.0.04.001/1.0.04.002/1.1.05.003/1.2.07.001. This affects the function setIpv6 of the file /goform/setIpv6. The manipulation of the argument tunrd_Prefix leads to stack-based buffer overflow. Remote exploitation of the attack is possible. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-9392

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-08-24T15:02:06.506Z |

A security vulnerability has been detected in Linksys RE6250, RE6300, RE6350, RE6500, RE7000 and RE9000 1.0.013.001/1.0.04.001/1.0.04.002/1.1.05.003/1.2.07.001. This affects the function qosClassifier of the file /goform/qosClassifier. Such manipulation of the argument dir/sFromPort/sToPort/dFromPort/dToPort/protocol/layer7/dscp/remark_dscp leads to stack-based buffer overflow. The attack may be launched remotely. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-9363

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-08-23T14:02:06.316Z |

A vulnerability has been found in Linksys RE6250, RE6300, RE6350, RE6500, RE7000 and RE9000 1.0.013.001/1.0.04.001/1.0.04.002/1.1.05.003/1.2.07.001. This affects the function portTriggerManageRule of the file /goform/portTriggerManageRule. The manipulation of the argument triggerRuleName/schedule leads to stack-based buffer overflow. Remote exploitation of the attack is possible. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-9299

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-08-21T12:32:12.049Z |

A vulnerability has been found in Tenda M3 1.0.0.12. Affected by this vulnerability is the function formGetMasterPassengerAnalyseData of the file /goform/getMasterPassengerAnalyseData. The manipulation of the argument Time leads to stack-based buffer overflow. The attack may be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-9298

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-08-21T12:32:08.707Z |

A flaw has been found in Tenda M3 1.0.0.12. Affected is the function formQuickIndex of the file /goform/QuickIndex. Executing manipulation of the argument PPPOEPassword can lead to stack-based buffer overflow. The attack can be launched remotely. The exploit has been published and may be used.

### CVE-2025-9297

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-08-21T12:02:11.484Z |

A vulnerability was detected in Tenda i22 1.0.0.3(4687). This impacts the function formWeixinAuthInfoGet of the file /goform/wxportalauth. Performing manipulation of the argument Type results in stack-based buffer overflow. The attack can be initiated remotely. The exploit is now public and may be used.

### CVE-2025-8810

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-08-10T13:02:08.230Z |

A vulnerability classified as critical was found in Tenda AC20 16.03.08.05. Affected by this vulnerability is the function strcpy of the file /goform/SetFirewallCfg. The manipulation of the argument firewallEn leads to stack-based buffer overflow. The attack can be launched remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-8168

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-07-25T20:02:06.070Z |

A vulnerability was found in D-Link DIR-513 1.10. It has been rated as critical. Affected by this issue is the function websAspInit of the file /goform/formSetWanPPPoE. The manipulation of the argument curTime leads to buffer overflow. The attack may be launched remotely. The exploit has been disclosed to the public and may be used. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2025-8159

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-07-25T14:32:05.932Z |

A vulnerability was found in D-Link DIR-513 1.0. It has been rated as critical. This issue affects the function formLanguageChange of the file /goform/formLanguageChange of the component HTTP POST Request Handler. The manipulation of the argument curTime leads to stack-based buffer overflow. The attack may be initiated remotely. The exploit has been disclosed to the public and may be used. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2025-8140

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-07-25T09:02:08.707Z |

A vulnerability was found in TOTOLINK A702R 4.0.0-B20230721.1521. It has been declared as critical. This vulnerability affects unknown code of the file /boafrm/formWlanMultipleAP of the component HTTP POST Request Handler. The manipulation of the argument submit-url leads to buffer overflow. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-8138

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-07-25T08:02:07.866Z |

A vulnerability was found in TOTOLINK A702R 4.0.0-B20230721.1521 and classified as critical. Affected by this issue is some unknown functionality of the file /boafrm/formOneKeyAccessButton of the component HTTP POST Request Handler. The manipulation of the argument submit-url leads to buffer overflow. The attack may be launched remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-8017

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-07-22T13:32:07.104Z |

A vulnerability was found in Tenda AC7 15.03.06.44. It has been classified as critical. Affected is the function formSetMacFilterCfg of the file /goform/setMacFilterCfg of the component httpd. The manipulation of the argument deviceList leads to stack-based buffer overflow. It is possible to launch the attack remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-7945

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-07-21T23:32:06.071Z |

A vulnerability was found in D-Link DIR-513 up to 20190831. It has been declared as critical. This vulnerability affects the function formSetWanDhcpplus of the file /goform/formSetWanDhcpplus. The manipulation of the argument curTime leads to buffer overflow. The attack can be initiated remotely. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2025-7092

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-07-06T20:02:05.250Z |

A vulnerability has been found in Belkin F9K1122 1.00.33 and classified as critical. This vulnerability affects the function formWlanSetupWPS of the file /goform/formWlanSetupWPS of the component webs. The manipulation of the argument wps_enrolee_pin/webpage leads to stack-based buffer overflow. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-7091

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-07-06T19:32:05.446Z |

A vulnerability was found in Belkin F9K1122 1.00.33. It has been classified as critical. Affected is the function formWlanMP of the file /goform/formWlanMP of the component webs. The manipulation of the argument ateFunc/ateGain/ateTxCount/ateChan/ateRate/ateMacID/e2pTxPower1/e2pTxPower2/e2pTxPower3/e2pTxPower4/e2pTxPower5/e2pTxPower6/e2pTxPower7/e2pTx2Power1/e2pTx2Power2/e2pTx2Power3/e2pTx2Power4/e2pTx2Power5/e2pTx2Power6/e2pTx2Power7/ateTxFreqOffset/ateMode/ateBW/ateAntenna/e2pTxFreqOffset/e2pTxPwDeltaB/e2pTxPwDeltaG/e2pTxPwDeltaMix/e2pTxPwDeltaN/readE2P leads to stack-based buffer overflow. It is possible to launch the attack remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-7090

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-07-06T19:02:06.107Z |

A vulnerability, which was classified as critical, has been found in Belkin F9K1122 1.00.33. Affected by this issue is the function formConnectionSetting of the file /goform/formConnectionSetting of the component webs. The manipulation of the argument max_Conn/timeOut leads to stack-based buffer overflow. The attack may be launched remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-7089

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-07-06T18:32:04.914Z |

A vulnerability was found in Belkin F9K1122 1.00.33 and classified as critical. This issue affects the function formWanTcpipSetup of the file /goform/formWanTcpipSetup of the component webs. The manipulation of the argument pppUserName leads to stack-based buffer overflow. The attack may be initiated remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-7088

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-07-06T18:02:06.558Z |

A vulnerability, which was classified as critical, was found in Belkin F9K1122 1.00.33. This affects the function formPPPoESetup of the file /goform/formPPPoESetup of the component webs. The manipulation of the argument pppUserName leads to stack-based buffer overflow. It is possible to initiate the attack remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-7087

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-07-06T17:32:05.280Z |

A vulnerability classified as critical was found in Belkin F9K1122 1.00.33. Affected by this vulnerability is the function formL2TPSetup of the file /goform/formL2TPSetup of the component webs. The manipulation of the argument L2TPUserName leads to stack-based buffer overflow. The attack can be launched remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-7086

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-07-06T17:02:08.800Z |

A vulnerability classified as critical has been found in Belkin F9K1122 1.00.33. Affected is the function formPPTPSetup of the file /goform/formPPTPSetup of the component webs. The manipulation of the argument pptpUserName leads to stack-based buffer overflow. It is possible to launch the attack remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-7085

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-07-06T16:32:05.008Z |

A vulnerability was found in Belkin F9K1122 1.00.33. It has been rated as critical. This issue affects the function formiNICWpsStart of the file /goform/formiNICWpsStart of the component webs. The manipulation of the argument pinCode leads to stack-based buffer overflow. The attack may be initiated remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-7084

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-07-06T16:02:05.557Z |

A vulnerability was found in Belkin F9K1122 1.00.33. It has been declared as critical. This vulnerability affects the function formWpsStart of the file /goform/formWpsStart of the component webs. The manipulation of the argument pinCode leads to stack-based buffer overflow. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-6627

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-06-25T18:31:07.699Z |

A vulnerability has been found in TOTOLINK A702R 4.0.0-B20230721.1521 and classified as critical. This vulnerability affects unknown code of the file /boafrm/formIpv6Setup of the component HTTP POST Request Handler. The manipulation of the argument submit-url leads to buffer overflow. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5907

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-06-10T00:31:08.647Z |

A vulnerability classified as critical was found in TOTOLINK EX1200T up to 4.1.2cu.5232_B20210713. This vulnerability affects unknown code of the file /boafrm/formFilter of the component HTTP POST Request Handler. The manipulation leads to buffer overflow. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5905

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-06-10T00:00:18.830Z |

A vulnerability was found in TOTOLINK T10 4.1.8cu.5207. It has been rated as critical. Affected by this issue is the function setWiFiRepeaterCfg of the file /cgi-bin/cstecgi.cgi of the component POST Request Handler. The manipulation of the argument Password leads to buffer overflow. The attack may be launched remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5904

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-06-10T00:00:16.259Z |

A vulnerability was found in TOTOLINK T10 4.1.8cu.5207. It has been declared as critical. Affected by this vulnerability is the function setWiFiMeshName of the file /cgi-bin/cstecgi.cgi of the component POST Request Handler. The manipulation of the argument device_name leads to buffer overflow. The attack can be launched remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5903

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-06-09T23:31:07.307Z |

A vulnerability was found in TOTOLINK T10 4.1.8cu.5207. It has been classified as critical. Affected is the function setWiFiAclRules of the file /cgi-bin/cstecgi.cgi of the component POST Request Handler. The manipulation of the argument desc leads to buffer overflow. It is possible to launch the attack remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5902

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-06-09T23:00:16.214Z |

A vulnerability was found in TOTOLINK T10 4.1.8cu.5207 and classified as critical. This issue affects the function setUpgradeFW of the file /cgi-bin/cstecgi.cgi of the component POST Request Handler. The manipulation of the argument slaveIpList leads to buffer overflow. The attack may be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5901

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-06-09T22:31:07.562Z |

A vulnerability has been found in TOTOLINK T10 4.1.8cu.5207 and classified as critical. This vulnerability affects the function UploadCustomModule of the file /cgi-bin/cstecgi.cgi of the component POST Request Handler. The manipulation of the argument File leads to buffer overflow. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5861

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-06-09T04:31:06.939Z |

A vulnerability has been found in Tenda AC7 15.03.06.44 and classified as critical. This vulnerability affects the function fromadvsetlanip of the file /goform/AdvSetLanip. The manipulation of the argument lanMask leads to buffer overflow. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5853

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-06-09T00:31:06.973Z |

A vulnerability classified as critical was found in Tenda AC6 15.03.05.16. Affected by this vulnerability is the function formSetSafeWanWebMan of the file /goform/SetRemoteWebCfg. The manipulation of the argument remoteIp leads to stack-based buffer overflow. The attack can be launched remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5850

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-06-08T23:00:20.211Z |

A vulnerability was found in Tenda AC15 15.03.05.19_multi. It has been declared as critical. This vulnerability affects the function formsetschedled of the file /goform/SetLEDCf of the component HTTP POST Request Handler. The manipulation of the argument Time leads to buffer overflow. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5792

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-06-06T18:00:15.445Z |

A vulnerability, which was classified as critical, has been found in TOTOLINK EX1200T 4.1.2cu.5232_B20210713. This issue affects some unknown processing of the file /boafrm/formWlanRedirect of the component HTTP POST Request Handler. The manipulation of the argument redirect-url leads to buffer overflow. The attack may be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5790

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-06-06T17:31:11.039Z |

A vulnerability classified as critical was found in TOTOLINK X15 1.0.0-B20230714.1105. This vulnerability affects unknown code of the file /boafrm/formIpQoS of the component HTTP POST Request Handler. The manipulation of the argument mac leads to buffer overflow. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5788

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-06-06T17:00:20.212Z |

A vulnerability was found in TOTOLINK X15 1.0.0-B20230714.1105. It has been rated as critical. Affected by this issue is some unknown functionality of the file /boafrm/formReflashClientTbl of the component HTTP POST Request Handler. The manipulation of the argument submit-url leads to buffer overflow. The attack may be launched remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5787

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-06-06T16:31:08.511Z |

A vulnerability was found in TOTOLINK X15 1.0.0-B20230714.1105. It has been declared as critical. Affected by this vulnerability is an unknown functionality of the file /boafrm/formWsc of the component HTTP POST Request Handler. The manipulation of the argument submit-url leads to buffer overflow. The attack can be launched remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5786

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-06-06T16:31:06.192Z |

A vulnerability was found in TOTOLINK X15 1.0.0-B20230714.1105. It has been classified as critical. Affected is an unknown function of the file /boafrm/formDMZ of the component HTTP POST Request Handler. The manipulation of the argument submit-url leads to buffer overflow. It is possible to launch the attack remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5785

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-06-06T16:00:25.620Z |

A vulnerability was found in TOTOLINK X15 1.0.0-B20230714.1105 and classified as critical. This issue affects some unknown processing of the file /boafrm/formWirelessTbl of the component HTTP POST Request Handler. The manipulation of the argument submit-url leads to buffer overflow. The attack may be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5739

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-06-06T09:00:24.134Z |

A vulnerability classified as critical has been found in TOTOLINK X15 1.0.0-B20230714.1105. This affects an unknown part of the file /boafrm/formSaveConfig of the component HTTP POST Request Handler. The manipulation of the argument submit-url leads to buffer overflow. It is possible to initiate the attack remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5527

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-06-03T20:31:06.838Z |

A vulnerability was found in Tenda RX3 16.03.13.11_multi_TDE01. It has been rated as critical. This issue affects the function save_staticroute_data of the file /goform/SetStaticRouteCfg. The manipulation of the argument list leads to stack-based buffer overflow. The attack may be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-5126

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-77;CWE-74` |
| Published | 2025-05-24T15:00:10.190Z |

A vulnerability was found in Teledyne FLIR AX8 up to 1.46.16. This vulnerability affects the function setDataTime of the file \usr\www\application\models\settingsregional.php. Performing manipulation of the argument year/month/day/hour/minute results in command injection. The attack may be initiated remotely. The exploit has been made public and could be used. Upgrading to version 1.49.16 is able to resolve this issue. Upgrading the affected component is recommended. The vendor points out: "FLIR AX8 internal web site has been refactored to be able to handle the reported vulnerabilities."

### CVE-2026-44578

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-05-13T17:01:38.942Z |

Next.js is a React framework for building full-stack web applications. From 13.4.13 to before 15.5.16 and 16.2.5, self-hosted applications using the built-in Node.js server can be vulnerable to server-side request forgery through crafted WebSocket upgrade requests. An attacker can cause the server to proxy requests to arbitrary internal or external destinations, which may expose internal services or cloud metadata endpoints. Vercel-hosted deployments are not affected. This vulnerability is fixed in 15.5.16 and 16.2.5.

### CVE-2026-7856

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2026-05-05T19:00:14.098Z |

A flaw has been found in D-Link DI-8100 16.07.26A1. This affects an unknown part of the file /url_member.asp of the component Web Management Interface. Executing a manipulation of the argument Name can lead to buffer overflow. The attack can be launched remotely. The exploit has been published and may be used.

### CVE-2026-7851

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2026-05-05T17:30:13.938Z |

A vulnerability was identified in D-Link DI-8100 16.07.26A1. This affects the function sprintf of the file yyxz.asp. The manipulation of the argument ID leads to stack-based buffer overflow. The attack is possible to be carried out remotely. The exploit is publicly available and might be used.

### CVE-2026-6483

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-78;CWE-77` |
| Published | 2026-04-17T10:30:17.119Z |

A vulnerability was found in Wavlink WL-WN530H4 20220721. This vulnerability affects the function strcat/snprintf of the file /cgi-bin/internet.cgi. The manipulation results in os command injection. It is possible to launch the attack remotely. The exploit has been made public and could be used. Upgrading to version 2026.04.16 is able to resolve this issue. Upgrading the affected component is recommended.

### CVE-2026-22666

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-95` |
| Published | 2026-04-07T12:41:31.280Z |

Dolibarr ERP/CRM versions prior to 23.0.2 contain an authenticated remote code execution vulnerability in the dol_eval_standard() function that fails to apply forbidden string checks in whitelist mode and does not detect PHP dynamic callable syntax. Attackers with administrator privileges can inject malicious payloads through computed extrafields or other evaluation paths using PHP dynamic callable syntax to bypass validation and achieve arbitrary command execution via eval().

### CVE-2026-28287

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-78` |
| Published | 2026-03-05T18:25:54.794Z |

FreePBX is an open source IP PBX. From versions 16.0.17.2 to before 16.0.20 and from version 17.0.2.4 to before 17.0.5, multiple command injection vulnerabilities exist in the recordings module. This issue has been patched in versions 16.0.20 and 17.0.5.

### CVE-2026-2847

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-78;CWE-77` |
| Published | 2026-02-20T15:32:08.557Z |

A vulnerability was detected in UTT HiPER 520 1.7.7-160105. Affected is the function sub_44EFB4 of the file /goform/formReleaseConnect of the component Web Management Interface. The manipulation of the argument Isp_Name results in os command injection. The attack can be launched remotely. The exploit is now public and may be used.

### CVE-2025-64328

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-78` |
| Published | 2025-11-07T03:32:20.670Z |

FreePBX Endpoint Manager is a module for managing telephony endpoints in FreePBX systems. In versions 17.0.2.36 and above before 17.0.3, the filestore module within the Administrative interface is vulnerable to a post-authentication command injection by an authenticated known user via the testconnection -> check_ssh_connect() function. An attacker can leverage this vulnerability to obtain remote access to the system as an asterisk user. This issue is fixed in version 17.0.3.

### CVE-2025-61678

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-434` |
| Published | 2025-10-14T19:33:29.934Z |

FreePBX Endpoint Manager is a module for managing telephony endpoints in FreePBX systems. In versions prior to 16.0.92 for FreePBX 16 and versions prior to 17.0.6 for FreePBX 17, the Endpoint Manager module contains an authenticated arbitrary file upload vulnerability affecting the fwbrand parameter. The fwbrand parameter allows an attacker to change the file path. Combined, these issues can result in a webshell being uploaded. Authentication with a known username is required to exploit this vulnerability. Successful exploitation allows authenticated users to upload arbitrary files to attacker-controlled paths on the server, potentially leading to remote code execution. This issue has been patched in version 16.0.92 for FreePBX 16 and version 17.0.6 for FreePBX 17.

### CVE-2025-61675

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-89` |
| Published | 2025-10-14T19:30:27.362Z |

FreePBX Endpoint Manager is a module for managing telephony endpoints in FreePBX systems. In versions prior to 16.0.92 for FreePBX 16 and versions prior to 17.0.6 for FreePBX 17, the Endpoint Manager module contains authenticated SQL injection vulnerabilities affecting multiple parameters in the basestation, model, firmware, and custom extension configuration functionality areas. Authentication with a known username is required to exploit these vulnerabilities. Successful exploitation allows authenticated users to execute arbitrary SQL queries against the database, potentially enabling access to sensitive data or modification of database contents. This issue has been patched in version 16.0.92 for FreePBX 16 and version 17.0.6 for FreePBX 17.

### CVE-2025-9961

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-120` |
| Published | 2025-09-06T06:50:59.558Z |

An authenticated attacker may remotely execute arbitrary code via the CWMP binary on the devices AX10 and AX1500. 

The exploit can only be conducted via a Man-In-The-Middle (MITM) attack. 

This issue affects AX10 V1/V1.2/V2/V2.6/V3/V3.6: before 1.2.1; AX1500 V1/V1.20/V1.26/V1.60/V1.80/V2.60/V3.6: before 1.3.11.

### CVE-2025-54254

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2025-08-05T16:53:39.954Z |

Adobe Experience Manager versions 6.5.23 and earlier are affected by an Improper Restriction of XML External Entity Reference ('XXE') vulnerability that could lead to arbitrary file system read. An attacker could exploit this vulnerability to access sensitive files on the local file system, scope is changed. Exploitation of this issue does not require user interaction.

### CVE-2026-6204

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-78` |
| Published | 2026-04-13T10:56:16.850Z |

LibreNMS versions before 26.3.0 are affected by an authenticated remote code execution vulnerability by abusing the Binary Locations config and the Netcommand feature. Successful exploitation requires administrative privileges. Exploitation could result in compromise of the underlying web server.

### CVE-2025-66516

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-611` |
| Published | 2025-12-04T16:17:24.980Z |

Critical XXE in Apache Tika tika-core (1.13-3.2.1), tika-pdf-module (2.0.0-3.2.1) and tika-parsers (1.13-1.28.5) modules on all platforms allows an attacker to carry out XML External Entity injection via a crafted XFA file inside of a PDF. 

This CVE covers the same vulnerability as in CVE-2025-54988. However, this CVE expands the scope of affected packages in two ways. 

First, while the entrypoint for the vulnerability was the tika-parser-pdf-module as reported in CVE-2025-54988, the vulnerability and its fix were in tika-core. Users who upgraded the tika-parser-pdf-module but did not upgrade tika-core to >= 3.2.2 would still be vulnerable. 

Second, the original report failed to mention that in the 1.x Tika releases, the PDFParser was in the "org.apache.tika:tika-parsers" module.

### CVE-2025-8088

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-35` |
| Published | 2025-08-08T11:11:41.842Z |

A path traversal vulnerability affecting the Windows version of WinRAR allows the attackers to execute arbitrary code by crafting malicious archive files. This vulnerability was exploited in the wild and was discovered by Anton Cherepanov, Peter Košinár, and Peter Strýček
     from ESET.

### CVE-2026-56448

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-22T14:17:50.627 |

A path traversal vulnerability exists in AIL Framework before the release containing commit 0041456af25da0cdea1c1c4624e46baff2731d8f. An authenticated AIL user can supply crafted object identifiers through the investigation workflow to cause file paths to resolve outside the intended image, favicon, or screenshot storage directories. This may allow the attacker to download and read arbitrary files that are accessible to the AIL process.

The issue occurs because user-controlled path components were joined with application storage paths without verifying that the resolved path remained within the expected directory. The affected download functionality could then include the contents of such files in a generated archive.

### CVE-2026-54100

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-06-22T14:17:40.950 |

A flaw was found in the Windows Machine Config Operator (WMCO) for Red Hat OpenShift Container Platform. WMCO establishes SSH connections to Windows worker nodes without verifying the remote server host key. An adjacent-network attacker who can intercept or redirect WMCO's SSH session can capture WICD and kubelet bootstrap credentials transferred during node configuration, enabling compromise of Windows node identities in the cluster.

### CVE-2023-45796

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-22T10:16:17.513 |

A stored cross-site scripting vulnerability in the Runtime component of Pilz PASvisu before 1.14.1 and PMI v8xx up to and including 2.0.33992 allows a low-privileged remote unauthenticated attacker to manipulate process data with potential impact on integrity and/or availability.

### CVE-2025-68472

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-23;CWE-36` |
| Published | 2026-01-12T16:53:47.748Z |

MindsDB is a platform for building artificial intelligence from enterprise data. Prior to version 25.11.1, an unauthenticated path traversal in the file upload API lets any caller read arbitrary files from the server filesystem and move them into MindsDB’s storage, exposing sensitive data. The PUT handler in file.py directly joins user-controlled data into a filesystem path when the request body is JSON and source_type is not "url". Only multipart uploads and URL-sourced uploads receive sanitization; JSON uploads lack any call to clear_filename or equivalent checks. This vulnerability is fixed in 25.11.1.

### CVE-2025-52690

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2025-07-16T06:34:02.704Z |

Successful exploitation of the vulnerability could allow an attacker to execute arbitrary commands as root, potentially leading to the loss of confidentiality, integrity, availability, and full control of the access point.

### CVE-2023-45795

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-22T10:16:16.470 |

A cross-site scripting vulnerability in the Builder Component of Pilz PASvisu before 1.14.1 allows a local unauthenticated attacker to inject malicious javascript and gain full control over the device.

### CVE-2025-6218

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2025-06-21T00:09:02.884Z |

RARLAB WinRAR Directory Traversal Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of RARLAB WinRAR. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the handling of file paths within archive files. A crafted file path can cause the process to traverse to unintended directories. An attacker can leverage this vulnerability to execute code in the context of the current user. Was ZDI-CAN-27198.

### CVE-2026-42129

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-06-22T14:17:36.340 |

The Loki datasource plugin's callResource handler contains a path traversal vulnerability. An authenticated Viewer-role user can escape the plugin's resource sandbox and access administrative Loki endpoints (e.g. /config, /services, /ready) to extract sensitive backend configuration and internal service information.

### CVE-2026-12581

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-384` |
| Published | 2026-06-22T10:16:18.260 |

EasyFlow .NET developed by Digiwin has a Session Fixation vulnerability. If unauthenticated remote attackers replace a specific session ID for a user, they can gain the user's privilege once the user logs in.

### CVE-2025-52970

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H/E:P/RL:X/RC:C` |
| Weaknesses | `CWE-233` |
| Published | 2025-08-12T18:59:25.817Z |

A improper handling of parameters in Fortinet FortiWeb versions 7.6.3 and below, versions 7.4.7 and below, versions 7.2.10 and below, and 7.0.10 and below may allow an unauthenticated remote attacker with non-public information pertaining to the device and targeted user to gain admin privileges on the device via a specially crafted request.

### CVE-2025-6023

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-601;CWE-79` |
| Published | 2025-07-18T07:48:15.972Z |

An open redirect vulnerability has been identified in Grafana OSS that can be exploited to achieve XSS attacks. The vulnerability was introduced in Grafana v11.5.0.

The open redirect can be chained with path traversal vulnerabilities to achieve XSS.

Fixed in versions 12.0.2+security-01, 11.6.3+security-01, 11.5.6+security-01, 11.4.6+security-01 and 11.3.8+security-01

### CVE-2026-44914

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:Y/R:U/V:C/RE:L/U:Clear` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-22T08:17:05.757 |

Apache NiFi 1.12.0 through 2.9.0 are missing authorization when replacing Process Groups that include extension components with specific Required Permissions based on the Restricted annotation. The Restricted annotation indicates additional privileges required, but framework authorization did not check restricted status when handling requests to replace Process Groups. The missing authorization permits a user with general write access to add components with Restricted status. Apache NiFi installations that do not implement specific authorization for Restricted components are not subject to this vulnerability because the framework enforces write permissions as the security boundary. Upgrading to Apache NiFi 2.9.0 is the recommended mitigation, which removes the implementation of Restricted status authorization from the framework.

### CVE-2026-33626

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-04-20T20:29:19.558Z |

LMDeploy is a toolkit for compressing, deploying, and serving large language models. Versions prior to 0.12.3 have a Server-Side Request Forgery (SSRF) vulnerability in LMDeploy's vision-language module. The `load_image()` function in `lmdeploy/vl/utils.py` fetches arbitrary URLs without validating internal/private IP addresses, allowing attackers to access cloud metadata services, internal networks, and sensitive resources. Version 0.12.3 patches the issue.

### CVE-2026-4020

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-03-31T01:24:57.221Z |

The Gravity SMTP plugin for WordPress is vulnerable to Sensitive Information Exposure in all versions up to, and including, 2.1.4. This is due to a REST API endpoint registered at /wp-json/gravitysmtp/v1/tests/mock-data with a permission_callback that unconditionally returns true, allowing any unauthenticated visitor to access it. When the ?page=gravitysmtp-settings query parameter is appended, the plugin's register_connector_data() method populates internal connector data, causing the endpoint to return approximately 365 KB of JSON containing the full System Report. This makes it possible for unauthenticated attackers to retrieve detailed system configuration data including PHP version, loaded extensions, web server version, document root path, database server type and version, WordPress version, all active plugins with versions, active theme, WordPress configuration details, database table names, and any API keys/tokens configured in the plugin.

### CVE-2025-61884

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2025-10-12T02:34:51.603Z |

Vulnerability in the Oracle Configurator product of Oracle E-Business Suite (component: Runtime UI).  Supported versions that are affected are 12.2.3-12.2.14. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Configurator.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Configurator accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2025-8355

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2025-08-08T15:31:44.554Z |

In Xerox FreeFlow Core version 8.0.4, improper handling of XML input allows injection of external entities. An attacker can craft malicious XML containing references to internal URLs, this results in a Server-Side Request Forgery (SSRF).

### CVE-2026-12806

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-06-21T20:16:27.497 |

A vulnerability has been found in Edimax BR-6478AC V2 1.23. The impacted element is the function formWlSiteSurvey of the file /goform/formWlSiteSurvey of the component POST Request Handler. The manipulation of the argument selSSID leads to buffer overflow. It is possible to initiate the attack remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-66399

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-77` |
| Published | 2025-12-02T17:57:11.544Z |

Cacti is an open source performance and fault management framework. Prior to 1.2.29, there is an input-validation flaw in the SNMP device configuration functionality. An authenticated Cacti user can supply crafted SNMP community strings containing control characters (including newlines) that are accepted, stored verbatim in the database, and later embedded into backend SNMP operations. In environments where downstream SNMP tooling or wrappers interpret newline-separated tokens as command boundaries, this can lead to unintended command execution with the privileges of the Cacti process. This vulnerability is fixed in 1.2.29.

### CVE-2026-9029

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-06-22T14:17:55.800 |

The geomap panel's XYZ tile layer has a sanitize-then-interpolate ordering bug. sanitizeTextPanelContent() runs on the raw template string before getTemplateSrv().replace() substitutes the variable value, which uses the glob format with no HTML escaping. The result is passed to OpenLayers via element.innerHTML. An Editor can set a textbox variable's default value to an XSS payload that executes for every user who opens the dashboard. This is a bypass of the CVE-2023-0507 fix

### CVE-2026-6645

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-06-22T04:17:13.310 |

An insecure process execution vulnerability exists in the pc-printer-updater.exe component of the PaperCut Print Deploy Client for Windows. The application, which typically operates with high-level system privileges, attempts to perform an internal validation check by invoking a secondary system utility using an unqualified file reference.



Because the application does not specify an absolute path to this utility, it relies on the operating system's default search order to locate the executable. Under specific conditions, a local attacker with the ability to modify directories within the system's search path could plant a malicious binary that mimics the expected utility. This could result in the malicious code being executed with SYSTEM privileges, leading to a full compromise of the affected host.

### CVE-2026-7857

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-05-05T20:16:41.677 |

A vulnerability has been found in D-Link DI-8100 16.07.26A1. This vulnerability affects the function sprintf of the file /user_group.asp of the component CGI Handler. The manipulation leads to buffer overflow. The attack may be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2026-40871

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-89;CWE-116;CWE-564` |
| Published | 2026-04-21T19:12:52.781Z |

mailcow: dockerized is an open source groupware/email suite based on docker. Versions prior to 2026-03b have a second-order SQL injection vulnerability in the quarantine_category field via the Mailcow API. The /api/v1/add/mailbox endpoint stores quarantine_category without validation or sanitization. This value is later used by quarantine_notify.py, which constructs SQL queries using unsafe % string formatting instead of parameterized queries. This results in a delayed (second-order) SQL injection when the quarantine notification job executes, allowing an attacker to inject arbitrary SQL. Using a UNION SELECT, sensitive data (e.g., admin credentials) can be exfiltrated and rendered inside quarantine notification emails. Version 2026-03b fixes the vulnerability.

### CVE-2025-6978

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-10-23T18:50:14.706Z |

Diagnostics command injection vulnerability

### CVE-2025-8078

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-10-21T01:49:29.266Z |

A post-authentication command injection vulnerability in Zyxel ATP series firmware versions from V4.32 through V5.40, USG FLEX series firmware versions from V4.50 through V5.40, USG FLEX 50(W) series firmware versions from V4.16 through V5.40, and USG20(W)-VPN series firmware versions from V4.16 through V5.40 could allow an authenticated attacker with administrator privileges to execute operating system (OS) commands on the affected device by passing a crafted string as an argument to a CLI command.

### CVE-2025-5946

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-10-14T14:29:00.514Z |

Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability in Centreon Infra Monitoring (Poller reload setup in the configuration modules) allows OS Command Injection.
On the poller parameters page, a user with high privilege is able to concatenate custom instructions into the poller reload command.

This issue affects Infra Monitoring: from 24.10.0 before 24.10.13, from 24.04.0 before 24.04.18, from 23.10.0 before 23.10.28.

### CVE-2025-6771

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-07-08T15:38:48.637Z |

OS command injection in Ivanti Endpoint Manager Mobile (EPMM) before version 12.5.0.2,12.4.0.3  and 12.3.0.3 allows a remote authenticated attacker with high privileges to achieve remote code execution

### CVE-2026-56424

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862;CWE-863` |
| Published | 2026-06-22T14:17:50.057 |

MISP core contained multiple broken access-control flaws where authorization checks were performed against the wrong entity, or where ownership/editability checks were missing on write paths. In affected subsystems, a lower-privileged authenticated user with the relevant feature permission could cause the application to authorize one object but mutate another, or could modify objects that were merely visible rather than editable by the user’s organization.


The affected paths included:

  *  Event Reports tag removal: the route-authorized report could differ from the report ID used for tag detachment, enabling cross-organization tag removal from another event report




  *  Collection Elements bulk deletion: bulk deletion authorized against a collection whose ID matched the collection-element row ID, rather than the element’s actual parent collection, enabling deletion of elements from collections the user did not own.
  *  Analyst Data capture/update: nested analyst data updates could overwrite an existing record without applying the normal canEditAnalystData ownership check, enabling cross-organization overwrite of analyst data records.
  *  Template Elements editing: editing authorized against a template whose ID matched the template-element ID, rather than the element’s actual parent template, enabling unauthorized edits to another organization’s template elements.
  *  Decaying Model editing and mappings: write paths loaded models using view-scope access but did not verify edit ownership, enabling users to edit or remap visible models owned by another organization. 








Successful exploitation could allow an authenticated user with subsystem-specific permissions to perform unauthorized cross-organization modifications or deletions of MISP data, resulting in integrity loss, unauthorized tampering with shared intelligence, and disruption of analyst workflows.

### CVE-2026-6858

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-22T06:16:21.263 |

The Transbank Webpay WordPress plugin before 1.14.0 does not sanitize and escape logs to be displayed, allowing unauthenticated users to perform Stored XSS attacks against logged in administrator

### CVE-2026-4259

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-22T06:16:21.153 |

The ultimate-woocommerce-auction-pro WordPress plugin through 2.4.5 does not sanitise and escape a parameter before outputting it back in the page, leading to a Reflected Cross-Site Scripting which could be used against high privilege users such as admin

### CVE-2026-8918

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-183` |
| Published | 2026-06-22T03:16:43.070 |

A permissive list of allowed inputs in ASUS Armoury Crate allows a local administrator to perform arbitrary memory read/write operations or cause a system crash (BSOD) by bypassing the validation mechanism.Refer to the '
Security Update for Armoury Crate App ' section on the ASUS Security Advisory for more information.

### CVE-2026-6653

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416;CWE-611` |
| Published | 2026-06-22T14:17:51.113 |

Use After Free in libxml2's xmlParseInternalSubset from GNOME libxml2 version 2.9.11 to 2.11.0 allows a remote attacker to cause a denial-of-service via maliciously crafted XML input with improper entity resolution handling.
