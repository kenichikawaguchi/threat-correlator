# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-22 15:01 UTC
- **対象期間**: `2026-07-21T15:00:34.000Z` 〜 `2026-07-22T15:01:25.000Z`
- **重要CVE数**: 891 件（Critical 9.0+: 250 件 / High 7.0〜: 641 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公表された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件以上** に上り、特に **リモートコード実行 (RCE)・OS コマンドインジェクション** が集中しています。  
- IoT デバイス（Autel Maxi Charger）に対する未認証のネットワーク攻撃が複数報告され、**ファームウェア更新が必須**です。  
- Oracle Fusion Middleware 系列製品に対する脆弱性が大量に報告され、対象バージョンは **12.2 系・14.1 系・15.1 系** と広範囲にわたります。  
- いずれも「ネットワークから直接利用可能」かつ「特権（root / 管理者）権限で実行」できる点が共通しており、企業ネットワークへの侵入・横展開の足掛かりとなり得ます。  

---

## 2. 特に注目すべき CVE  

| CVE 番号 | スコア | 主な影響 | 理由・影響範囲 |
|----------|--------|----------|----------------|
| **CVE‑2026‑8985** | 10.0 | Autel Maxi Charger Single の `/test` エンドポイントで OS コマンドインジェクション | 未認証で任意の OS コマンドを実行可能。TCP 9002 が外部に開放されていると、充電ステーション全体が遠隔操作される危険があります。 |
| **CVE‑2026‑8984** | 10.0 | 同上デバイスで RCE（root 権限） | `/test` へ細工したリクエストを送るだけで、攻撃者が任意のファイルをダウンロード・実行できる。ファームウェア更新が行われていない全機種が対象。 |
| **CVE‑2026‑60644** | 10.0 | Oracle WebCenter Content (12.2.1.4.0 / 14.1.2.0.0) のリモートコード実行 | HTTP 経由で未認証にコード実行が可能。WebCenter Content は企業の文書管理・ポータルの中核であり、情報漏洩・改ざんリスクが極めて高い。 |
| **CVE‑2026‑60389** | 10.0 | Oracle Service Delivery Platform (Messaging Enabler) (12.2.1.4.0 / 14.1.2.0.0) の RCE | HTTP 経由で任意コード実行が可能。メッセージング基盤が乗っ取られると、社内システム間の通信がすべて操作対象になる。 |
| **CVE‑2026‑60365** | 10.0 | Oracle WebLogic Server Proxy Plug‑in (15.1.1.0.0) の認証なしリモートコード実行 | WebLogic のプロキシプラグインは多くの Web アプリのフロントエンドに配置されているため、侵入後の横展開が容易になる。 |

> **共通点**：すべて「ネットワークから直接アクセス可能」かつ「認証不要」もしくは「認証回避」でき、影響範囲が **企業全体のインフラ** に波及する点です。特に Oracle 製品は多数のサブシステムで共有ライブラリを使用しているため、1 つの脆弱性が **複数サービス** に波及するリスクがあります。

---

## 3. 推奨アクション  

### 3‑1. Autel Maxi Charger（IoT デバイス）  
- **ファームウェア更新**：ベンダーが提供する **V1.03.52 以降**（またはそれ以降のパッチ）へ即時アップデート。  
- **ネットワーク防御**：TCP **9002** を外部から到達不能にする（ファイアウォールで遮断、VLAN 分離）。  
- **不要サービスの無効化**：`/test` エンドポイントが不要であれば、Web サーバ設定で無効化。  
- **監視**：`/test` へのリクエストログを集中管理し、異常なパラメータ（例：`;`, `` ` ``）が検出されたらアラートを上げる。

### 3‑2. Oracle Fusion Middleware 系列  
| 製品 | 影響バージョン | 対策パッケージ / パッチ |
|------|----------------|------------------------|
| WebCenter Content | 12.2.1.4.0、14.1.2.0.0 | **Oracle Critical Patch Update (CPU) 2026‑Q2** → `p28112371_122140_Generic.zip`（WebCenter Content 修正） |
| Service Delivery Platform (Messaging Enabler) | 12.2.1.4.0、14.1.2.0.0 | **CPU 2026‑Q2** → `p28112371_122140_Generic.zip`（Messaging Enabler 修正） |
| WebLogic Server Proxy Plug‑in | 15.1.1.0.0 | **CPU 2026‑Q2** → `p28112371_151100_Generic.zip`（Proxy Plug‑in 修正） |
| Unified Directory | 12.2.1.4.0、14.1.2.1.0 | **CPU 2026‑Q2** → `p28112371_122140_Generic.zip`（OUD 修正） |
| その他（WebCenter Portal、WebCenter Sites、PeopleSoft 等） | 12.2.1.4.0、14.1.2.0.0、9.1、9.2 など | **CPU 2026‑Q2** の全製品パッチを適用し、**Patch Set Update (PSU) 2026‑Q2** へ統合アップデート |

- **パッチ適用手順**  
  1. Oracle Support から該当パッチをダウンロード。  
  2. 本番環境の **バックアップ**（WLST スクリプト、ドメイン構成、データベース）を取得。  
  3. **スタンドアロンモード** でパッチを適用し、`opatch apply` を実行。  
  4. 必要に応じて **再起動**（WebLogic Server、Managed Server）し、`opatch lspatches` で適用状況を確認。  
  5. パッチ適用後は **

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-8985

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-21T22:19:10.893 |

Autel Maxi Charger Single firmware through V1.03.51 is vulnerable to OS command injection in the /test endpoint exposed on TCP port 9002. An unauthenticated attacker can supply crafted input in the url parameter to execute arbitrary operating system commands.

### CVE-2026-8984

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-21T22:19:10.770 |

Autel Maxi Charger Single firmware through V1.03.51 allows unauthenticated remote code execution via the service listening on TCP port 9002. A crafted request to the /test endpoint can cause the device to download, extract, and execute attacker-controlled files with root privileges.

### CVE-2026-60644

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:05.193 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Web Content Management).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60389

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:41.717 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Service Delivery Platform.  While the vulnerability is in Service Delivery Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60379

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:40.597 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Service Delivery Platform.  While the vulnerability is in Service Delivery Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60365

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:39.860 |

Vulnerability in the Oracle Weblogic Server Proxy Plug-in product of Oracle Fusion Middleware (component: WebLogic Server Proxy Plug-In for Third-Party Web Servers).   The supported version that is affected is 15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Weblogic Server Proxy Plug-in.  While the vulnerability is in Oracle Weblogic Server Proxy Plug-in, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Weblogic Server Proxy Plug-in accessible data as well as  unauthorized access to critical data or complete access to all Oracle Weblogic Server Proxy Plug-in accessible data. CVSS 3.1 Base Score 10.0 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60360

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:39.293 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Unified Directory.  While the vulnerability is in Oracle Unified Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Unified Directory. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60358

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:39.057 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60217

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:23.207 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  While the vulnerability is in Oracle Coherence, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-47056

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:11.370 |

Vulnerability in the Oracle Data Integrator product of Oracle Fusion Middleware (component: Rest Service).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Data Integrator.  While the vulnerability is in Oracle Data Integrator, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Data Integrator. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-8983

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-07-21T21:16:54.837 |

Autel Maxi Charger Single firmware through V1.03.51 contains a hard-coded authentication token that bypasses authorization checks for multiple management endpoints. An attacker can supply the special token value to invoke privileged functionality without valid authentication.

### CVE-2026-8982

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-07-21T21:16:54.710 |

Two undocumented privileged accounts exist in Autel Maxi Charger Single firmware through V1.03.51. The accounts use vendor-defined password derivation mechanisms based on device-specific values, allowing an attacker with knowledge of the algorithm and required inputs to authenticate to the web management interface with administrative privileges.

### CVE-2026-61242

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:55.010 |

Vulnerability in the PeopleSoft Enterprise FIN Common Objects Argentina product of Oracle PeopleSoft (component: Staffing).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Common Objects Argentina.  While the vulnerability is in PeopleSoft Enterprise FIN Common Objects Argentina, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise FIN Common Objects Argentina. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61239

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:54.793 |

Vulnerability in the PeopleSoft Enterprise FIN Common Objects Argentina product of Oracle PeopleSoft (component: eProcurement).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Common Objects Argentina.  While the vulnerability is in PeopleSoft Enterprise FIN Common Objects Argentina, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise FIN Common Objects Argentina accessible data as well as  unauthorized read access to a subset of PeopleSoft Enterprise FIN Common Objects Argentina accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of PeopleSoft Enterprise FIN Common Objects Argentina. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:L).

### CVE-2026-61237

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:54.573 |

Vulnerability in the PeopleSoft Enterprise FIN Common Objects Argentina product of Oracle PeopleSoft (component: Integration).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Common Objects Argentina.  While the vulnerability is in PeopleSoft Enterprise FIN Common Objects Argentina, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise FIN Common Objects Argentina accessible data as well as  unauthorized update, insert or delete access to some of PeopleSoft Enterprise FIN Common Objects Argentina accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of PeopleSoft Enterprise FIN Common Objects Argentina. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:L).

### CVE-2026-61211

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:52.790 |

Vulnerability in the RDBMS component of Oracle Database Server.  Supported versions that are affected are 19.3-19.31 and  23.4.0-23.26.2. Easily exploitable vulnerability allows low privileged attacker having Execute DBMS_CLOUD privilege with network access via Oracle Net to compromise RDBMS.  While the vulnerability is in RDBMS, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of RDBMS. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61209

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:52.560 |

Vulnerability in the PeopleSoft In-Memory Project Discovery product of Oracle PeopleSoft (component: Project Discovery).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft In-Memory Project Discovery.  While the vulnerability is in PeopleSoft In-Memory Project Discovery, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of PeopleSoft In-Memory Project Discovery. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61146

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:45.990 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Content Acquisition System).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  While the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61076

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:38.410 |

Vulnerability in the PeopleSoft Enterprise HCM Talent Acquisition Manager product of Oracle PeopleSoft (component: Job Opening).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise HCM Talent Acquisition Manager.  While the vulnerability is in PeopleSoft Enterprise HCM Talent Acquisition Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise HCM Talent Acquisition Manager. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61072

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:37.980 |

Vulnerability in the PeopleSoft Enterprise FIN Staffing Front Office Brazil product of Oracle PeopleSoft (component: Staffing).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Staffing Front Office Brazil.  While the vulnerability is in PeopleSoft Enterprise FIN Staffing Front Office Brazil, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise FIN Staffing Front Office Brazil. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61041

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:35.047 |

Vulnerability in the Oracle Demantra Demand Management product of Oracle Supply Chain (component: Product Security).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Demantra Demand Management.  While the vulnerability is in Oracle Demantra Demand Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Demantra Demand Management. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60719

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:12.250 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: Web Service API).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle BI Publisher.  While the vulnerability is in Oracle BI Publisher, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle BI Publisher accessible data as well as  unauthorized access to critical data or complete access to all Oracle BI Publisher accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle BI Publisher. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L).

### CVE-2026-60711

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:11.553 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.5. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  While the vulnerability is in Siebel CRM Cloud Applications, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60663

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:07.150 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Web Content Management).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60627

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:03.290 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Installation Security).   The supported version that is affected is 9.2.26.3. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Tools.  While the vulnerability is in JD Edwards EnterpriseOne Tools, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Tools. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60568

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:57.033 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60565

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:56.697 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60562

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:56.350 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60561

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:56.227 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60552

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:55.183 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Sites.  While the vulnerability is in Oracle WebCenter Sites, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60547

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:54.613 |

Vulnerability in the Oracle Managed File Transfer product of Oracle Fusion Middleware (component: MFT Runtime Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Managed File Transfer.  While the vulnerability is in Oracle Managed File Transfer, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Managed File Transfer. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60542

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:54.060 |

Vulnerability in the Oracle Business Process Management Suite product of Oracle Fusion Middleware (component: Human Workflow).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle Business Process Management Suite.  While the vulnerability is in Oracle Business Process Management Suite, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Business Process Management Suite. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60537

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:53.500 |

Vulnerability in the Oracle Managed File Transfer product of Oracle Fusion Middleware (component: MFT Runtime Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Managed File Transfer.  While the vulnerability is in Oracle Managed File Transfer, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Managed File Transfer. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60531

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:52.833 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Identity Manager Connector.  While the vulnerability is in Oracle Identity Manager Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager Connector. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60524

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:52.067 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60461

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:48.530 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60459

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:48.310 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60458

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:48.197 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60457

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:48.087 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60456

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:47.967 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60447

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:47.190 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60445

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:46.967 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60429

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:45.357 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Unified Directory.  While the vulnerability is in Oracle Unified Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Unified Directory. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60422

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:44.557 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).   The supported version that is affected is 14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Unified Directory.  While the vulnerability is in Oracle Unified Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Unified Directory accessible data as well as  unauthorized access to critical data or complete access to all Oracle Unified Directory accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Unified Directory. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L).

### CVE-2026-60402

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:42.717 |

Vulnerability in the TimesTen In-Memory Database product of Oracle TimesTen In-Memory Database (component: Kubernetes Operator).   The supported version that is affected is 26.1.1.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise TimesTen In-Memory Database.  While the vulnerability is in TimesTen In-Memory Database, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of TimesTen In-Memory Database. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60381

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:40.827 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Service Delivery Platform.  While the vulnerability is in Service Delivery Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60377

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:40.350 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Service Delivery Platform.  While the vulnerability is in Service Delivery Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Service Delivery Platform accessible data as well as  unauthorized access to critical data or complete access to all Service Delivery Platform accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Service Delivery Platform. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L).

### CVE-2026-60361

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:39.407 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Unified Directory.  While the vulnerability is in Oracle Unified Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Unified Directory. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60333

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:36.360 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60206

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:21.953 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via SAML to compromise Oracle WebLogic Server.  While the vulnerability is in Oracle WebLogic Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-47392

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-184;CWE-693` |
| Published | 2026-07-21T16:17:12.087 |

PraisonAI is a multi-agent teams system. Prior to version 4.6.40 of PraisonAI, corresponding to version 1.6.40 of praisonaiagents, `execute_code()` in `praisonaiagents/tools/python_tools.py` (v1.6.37, subprocess sandbox mode) can be fully bypassed using `print.__self__` to retrieve the real Python `builtins` module, from which `__import__` can be extracted via `vars()` and runtime string construction. This achieves arbitrary OS command execution on the host, completely defeating the sandbox. This is a novel bypass that survives all patches for CVE-2026-39888 (frame traversal), CVE-2026-34938 (str subclass), and CVE-2026-40158 (`type.__getattribute__` trampoline). PraisonAI version 4.6.40 and praisonaiagents version 1.6.40 contain an updated fix.

### CVE-2026-61245

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:55.343 |

Vulnerability in the PeopleSoft Enterprise FIN Manufacturing Brazil product of Oracle PeopleSoft (component: Integration).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise PeopleSoft Enterprise FIN Manufacturing Brazil.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise FIN Manufacturing Brazil. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61233

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:54.133 |

Vulnerability in the PeopleSoft Enterprise FIN Common Objects Brazil product of Oracle PeopleSoft (component: Integration).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Common Objects Brazil.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise FIN Common Objects Brazil. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61196

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:51.510 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61183

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:50.110 |

Vulnerability in the Oracle Agile Product Lifecycle Management for Process product of Oracle Supply Chain (component: Reporting).   The supported version that is affected is 6.2.4. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Agile Product Lifecycle Management for Process.  Successful attacks of this vulnerability can result in takeover of Oracle Agile Product Lifecycle Management for Process. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61178

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:49.523 |

Vulnerability in the Oracle Agile Product Lifecycle Management for Process product of Oracle Supply Chain (component: Installation).   The supported version that is affected is 6.2.4. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Agile Product Lifecycle Management for Process.  Successful attacks of this vulnerability can result in takeover of Oracle Agile Product Lifecycle Management for Process. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61167

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:48.367 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Security).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks of this vulnerability can result in takeover of Oracle Agile PLM. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61161

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:47.687 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61154

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:46.870 |

Vulnerability in the Oracle Commerce Guided Search Platform Services product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search Platform Services.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search Platform Services. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61145

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:45.880 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Content Acquisition System).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61140

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:45.300 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61131

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:44.393 |

Vulnerability in the Oracle Commerce Platform product of Oracle Commerce (component: Dynamo Application Framework).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61129

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:44.167 |

Vulnerability in the Oracle Commerce Platform product of Oracle Commerce (component: ATG Portals).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61100

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:41.140 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61065

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:37.313 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60999

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:32.240 |

Vulnerability in the Oracle Data Integrator product of Oracle Fusion Middleware (component: Rest Service).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Data Integrator.  Successful attacks of this vulnerability can result in takeover of Oracle Data Integrator. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60880

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:24.480 |

Vulnerability in the Oracle Work in Process product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Work in Process.  Successful attacks of this vulnerability can result in takeover of Oracle Work in Process. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60566

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:56.813 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60555

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:55.517 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60551

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:55.070 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60541

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:53.960 |

Vulnerability in the Oracle SOA Suite product of Oracle Fusion Middleware (component: Enterprise Scheduling System).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle SOA Suite.  Successful attacks of this vulnerability can result in takeover of Oracle SOA Suite. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60538

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:53.613 |

Vulnerability in the Oracle SOA Suite product of Oracle Fusion Middleware (component: Enterprise Scheduling System).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle SOA Suite.  Successful attacks of this vulnerability can result in takeover of Oracle SOA Suite. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60535

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:53.280 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: PeopleSoft Applications).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Identity Manager Connector.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager Connector. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60532

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:52.940 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: PeopleSoft Applications).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Identity Manager Connector.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager Connector. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60463

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:48.743 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise WebCenter Content: Imaging.  Successful attacks of this vulnerability can result in takeover of WebCenter Content: Imaging. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60460

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:48.420 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60446

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:47.077 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60442

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:46.623 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60441

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:46.513 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60435

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:45.947 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60388

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:41.610 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60387

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:41.500 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60386

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:41.387 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60385

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:41.280 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60384

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:41.167 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60380

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:40.713 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60378

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:40.480 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60376

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:40.207 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60375

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:40.097 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60374

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:39.980 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60364

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:39.747 |

Vulnerability in the Oracle Weblogic Server Proxy Plug-in product of Oracle Fusion Middleware (component: WebLogic Server Proxy Plug-In for Third-Party Web Servers).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Weblogic Server Proxy Plug-in.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Weblogic Server Proxy Plug-in accessible data. CVSS 3.1 Base Score 7.5 (Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N).

### CVE-2026-60363

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:39.633 |

Vulnerability in the Oracle HTTP Server product of Oracle Fusion Middleware (component: Apache Plugin).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle HTTP Server.  Successful attacks of this vulnerability can result in takeover of Oracle HTTP Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60362

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:39.527 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Unified Directory. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60355

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:38.713 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60329

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:35.920 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60328

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:35.810 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60308

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:33.490 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60306

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:33.263 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60302

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:32.817 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60300

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:32.603 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60299

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:32.493 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60298

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:32.387 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60297

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:32.277 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60296

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:32.160 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60294

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:31.940 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60292

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:31.713 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60291

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:31.603 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60290

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:31.497 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60289

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:31.387 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60288

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:31.273 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60287

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:31.163 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60286

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:31.053 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60285

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:30.947 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60280

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:30.383 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP/2 to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60279

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:30.270 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60278

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:30.163 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60276

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:29.903 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60275

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:29.793 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60274

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:29.680 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60272

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:29.463 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60269

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:29.053 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60264

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:28.490 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP/2 to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60262

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:28.267 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60259

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:27.933 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60258

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:27.823 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60257

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:27.717 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60256

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:27.593 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60254

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:27.370 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60253

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:27.257 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60251

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:27.033 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60250

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:26.923 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60247

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:26.597 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60246

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:26.490 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60244

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:26.267 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60242

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:26.043 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60241

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:25.937 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60240

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:25.827 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60236

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:25.397 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60234

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:25.170 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60232

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:24.953 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60230

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:24.690 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60229

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:24.567 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60228

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:24.457 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60227

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:24.343 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60226

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:24.233 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60225

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:24.120 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60224

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:24.010 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60221

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:23.667 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60219

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:23.430 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60216

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:23.097 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60215

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:22.977 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60212

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:22.633 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60210

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:22.407 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60209

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:22.297 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60205

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:21.847 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60204

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:21.730 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60202

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:21.520 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60200

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:21.297 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60199

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:21.180 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60198

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:21.073 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60197

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:20.957 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60173

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:18.167 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0 and  12.2.1.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle BI Publisher.  Successful attacks of this vulnerability can result in takeover of Oracle BI Publisher. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-47036

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:09.170 |

Vulnerability in the Siebel CRM Development product of Oracle Siebel CRM (component: Siebel Approval Manager).  Supported versions that are affected are 17.0-26.3. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Development.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Development. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46994

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:04.663 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Agent Next Gen).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46983

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:03.347 |

Vulnerability in the Oracle Retail Integration Bus product of Oracle Retail Applications (component: RIB Kernal).   The supported version that is affected is 16.0.3. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Retail Integration Bus.  Successful attacks of this vulnerability can result in takeover of Oracle Retail Integration Bus. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46982

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:03.240 |

Vulnerability in the Oracle Retail Integration Bus product of Oracle Retail Applications (component: RIB Kernal).   The supported version that is affected is 14.1.3.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Retail Integration Bus.  Successful attacks of this vulnerability can result in takeover of Oracle Retail Integration Bus. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46924

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:02.047 |

Vulnerability in Oracle Application Testing Suite.   The supported version that is affected is 13.3.0.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Application Testing Suite.  Successful attacks of this vulnerability can result in takeover of Oracle Application Testing Suite. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46876

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:01.690 |

Vulnerability in Oracle Application Testing Suite.   The supported version that is affected is 13.3.0.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via Oracle Net to compromise Oracle Application Testing Suite.  Successful attacks of this vulnerability can result in takeover of Oracle Application Testing Suite. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35290

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:01.140 |

Vulnerability in Oracle Application Testing Suite.   The supported version that is affected is 13.3.0.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Application Testing Suite.  Successful attacks of this vulnerability can result in takeover of Oracle Application Testing Suite. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-47410

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-321;CWE-798` |
| Published | 2026-07-21T17:17:09.773 |

PraisonAI Platform is the platform layer for the PraisonAI multi-agent teams system. Versions prior to 0.1.4 have an insecure default cryptographic key. The JWT signing secret defaults to the hardcoded literal `"dev-secret-change-me"` when `PLATFORM_JWT_SECRET` is unset. A safety check exists but only fires when `PLATFORM_ENV != "dev"`; the default value of `PLATFORM_ENV` is `"dev"`, so the check is silently bypassed in any deployment that does not explicitly opt out. The attacker reads the literal from this public source file, mints a JWT with arbitrary `sub` and `email` claims, and authenticates as any existing user (including workspace owners and admins). PraisonAI Platform version 0.1.4 patches the issue.

### CVE-2026-47396

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-306` |
| Published | 2026-07-21T16:17:12.760 |

PraisonAI is a multi-agent teams system. Prior to version 4.6.40, PraisonAI's call server exposes a network-facing agent control API without authentication when `CALL_SERVER_TOKEN` is not configured. The affected component is the `praisonai.api.agent_invoke` router as mounted by `praisonai.api.call`. The authentication helper `verify_token()` fails open when `CALL_SERVER_TOKEN` is unset. Since every sensitive agent-control endpoint depends on this helper, starting the call server without a token allows any reachable client to list agents, inspect agent metadata and instructions, invoke agents, and unregister agents. This is security-relevant because the bundled call server includes the vulnerable router and binds to `0.0.0.0`. As a result, operators who launch the call server without explicitly setting `CALL_SERVER_TOKEN` may unintentionally expose an unauthenticated remote agent control plane. Version 4.6.40 fixes the issue.

### CVE-2026-47393

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-1188` |
| Published | 2026-07-21T16:17:12.270 |

PraisonAI is a multi-agent teams system. CVE-2026-44338 (GHSA-6rmh-7xcm-cpxj) documents that PraisonAI ships a code-generator (`praisonai.deploy.api.generate_api_server_code`) that emits a Flask API server with authentication disabled by default. Users who follow the documented quickstart (`praisonai deploy --type api`) get a server that binds to `0.0.0.0` per the recommended sample YAML, exposes `/chat` and `/agents` endpoints, runs `praisonai.run()` on user-supplied JSON input — LLM orchestration with the API key materials present in the process environment, and does not require any authentication. Versions prior to 4.6.40 still ship the generator with `auth_enabled` defaulting to `False`. The fix shape is opt-in via `APIConfig(auth_enabled=True, auth_token=...)`. Version 4.6.40 fixes the issue.

### CVE-2026-47391

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-95;CWE-306` |
| Published | 2026-07-21T16:17:11.920 |

PraisonAI is a multi-agent teams system. Prior to version 4.6.40, PraisonAI's first-party A2A server example exposes an unauthenticated A2A JSON-RPC endpoint and registers a `calculate(expression)` tool implemented with Python `eval()`. The example also binds to `0.0.0.0`. A remote unauthenticated attacker can send `message/send` to `/a2a`; the request reaches `agent.chat()`, and a real LLM can invoke the registered `calculate` tool. In testing with `gemini/gemini-2.5-flash-lite`, this resulted in arbitrary Python execution in the server process, confirmed by creation of a marker file from an unauthenticated HTTP request. The issue affects deployments following the official A2A example or similar unauthenticated public A2A deployments with unsafe tools. The default unauthenticated A2A surface also exposes task history and task cancellation APIs, increasing confidentiality and integrity impact. Version 4.6.40 patches the issue.

### CVE-2026-16424

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-21T23:17:00.030 |

Use after free in GPU in Google Chrome on Android prior to 150.0.7871.182 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-62549

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-21T22:19:08.543 |

Vulnerability in the Oracle HRMS (UK) product of Oracle E-Business Suite (component: UK Payroll).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle HRMS (UK).  While the vulnerability is in Oracle HRMS (UK), attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle HRMS (UK) accessible data as well as  unauthorized access to critical data or complete access to all Oracle HRMS (UK) accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-61097

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:40.790 |

Vulnerability in the Oracle Banking Trade Finance Process Management product of Oracle Financial Services Applications (component: Common).  Supported versions that are affected are 14.6.0-14.8.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Banking Trade Finance Process Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Banking Trade Finance Process Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Banking Trade Finance Process Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Banking Trade Finance Process Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Banking Trade Finance Process Management. CVSS 3.1 Base Score 9.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:L).

### CVE-2026-60773

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:16.443 |

Vulnerability in the Oracle Application Object Library product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Application Object Library.  While the vulnerability is in Oracle Application Object Library, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Application Object Library accessible data as well as  unauthorized access to critical data or complete access to all Oracle Application Object Library accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60564

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:56.570 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Portal accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60540

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:53.847 |

Vulnerability in the Oracle SOA Suite product of Oracle Fusion Middleware (component: Integration Business Insight).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle SOA Suite.  While the vulnerability is in Oracle SOA Suite, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle SOA Suite accessible data as well as  unauthorized access to critical data or complete access to all Oracle SOA Suite accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60239

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:25.717 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Coherence.  While the vulnerability is in Oracle Coherence, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Coherence accessible data as well as  unauthorized access to critical data or complete access to all Oracle Coherence accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-47416

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-269;CWE-862` |
| Published | 2026-07-21T18:17:00.563 |

PraisonAI Platform is the platform layer for the PraisonAI multi-agent teams system. Versions prior to 0.1.4 are vulnerable to vertical privilege escalation. The `PATCH /workspaces/{workspace_id}/members/{user_id}` endpoint is gated by `require_workspace_member(workspace_id)`, which defaults to `min_role="member"` and is never overridden by the route. The handler then calls `MemberService.update_role(workspace_id, user_id, body.role)` which sets the target member's role to whatever the request body specifies, with no check that the caller has owner-or-admin privilege, no check that the new role is not higher than the caller's own, and no check that the caller is not silently promoting themselves. PraisonAI Platform version 0.1.4 patches the issue.

### CVE-2026-47413

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-269;CWE-862` |
| Published | 2026-07-21T18:17:00.133 |

PraisonAI Platform is the platform layer for the PraisonAI multi-agent teams system. Versions prior to 0.1.4 have aprivilege escalation / cross-tenant member injection. The `POST /workspaces/{workspace_id}/members` endpoint is gated only by `require_workspace_member(workspace_id)` (default `min_role="member"`) and forwards the request body's `user_id` and `role` straight into `MemberService.add(workspace_id, user_id, role)`, which has no caller-permission check. A user with the lowest workspace privilege can add any user (including a new attacker-controlled second account, or an existing account they want to grief) as owner of the workspace. PraisonAI Platform version 0.1.4 patches the issue.

### CVE-2026-8986

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-21T22:19:11.023 |

Autel Maxi Charger Single firmware through V1.03.51 is vulnerable to OS command injection when processing OCPP GetDiagnostics requests. A malicious or compromised OCPP server can supply a crafted diagnostics URL that results in arbitrary command execution on the charging station.

### CVE-2026-63048

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-22T08:16:24.063 |

The Joomla extension Page Builder CK is vulnerable to an authenticated arbitrary file upload, leading to RCE.

### CVE-2026-8987

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-21T22:19:11.143 |

Autel Maxi Charger Single firmware through V1.03.51 contains a heap-based buffer overflow in the set_ap_param command handled by the /localcfg endpoint. An authenticated attacker can supply oversized input, resulting in denial of service and potentially arbitrary code execution.

### CVE-2026-61203

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:52.063 |

Vulnerability in the PeopleSoft Enterprise FIN Expenses product of Oracle PeopleSoft (component: Expenses).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Expenses.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise FIN Expenses accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise FIN Expenses accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of PeopleSoft Enterprise FIN Expenses. CVSS 3.1 Base Score 9.4 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-61186

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:50.470 |

Vulnerability in the Oracle Agile Engineering Data Management product of Oracle Supply Chain (component: Install).   The supported version that is affected is 6.2.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Agile Engineering Data Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Agile Engineering Data Management accessible data as well as  unauthorized read access to a subset of Oracle Agile Engineering Data Management accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Agile Engineering Data Management. CVSS 3.1 Base Score 9.4 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H).

### CVE-2026-64879

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-21T20:17:04.763 |

A filename supplied during file upload is not properly sanitized before being used in system command execution, allowing an attacker to inject shell metacharacters and achieve command injection via the audit file upload functionality.

### CVE-2026-64878

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-21T20:17:04.630 |

Unvalidated input in asset filter parameters allows shell metacharacters to escape command argument handling, resulting in remote code execution as a low-privileged OS user via the Analysis REST endpoint.

### CVE-2026-64877

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-21T19:17:13.340 |

An authenticated non-admin user can exploit a SQL injection flaw in the ticketing REST API to access sensitive data stored in the appliance database.

### CVE-2026-47407

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269;CWE-639;CWE-863` |
| Published | 2026-07-21T17:17:09.363 |

PraisonAI Platform is the platform layer for the PraisonAI multi-agent teams system. Prior to version 0.1.4, the Platform server exposes resources under `/api/v1/workspaces/{workspace_id}/...` and protects them with a `require_workspace_member(workspace_id)` FastAPI dependency. The dependency only checks that the caller is a member of the workspace_id in the URL prefix. The route handlers then look up the inner resource (`agent_id`, `issue_id`, `project_id`, `label_id`, `comment_id`, `dependency_id`) by primary key alone. The resource's own `workspace_id` is never compared to the URL's `workspace_id`. A user can therefore put their own workspace in the URL prefix and any other workspace's resource ID in the path. The auth check passes, since they really are a member of the prefix workspace. The service then returns the cross-tenant resource for read, update, or delete. There is a second bug in the member-management routes (`add_member`, `update_member_role`, `remove_member`, `update_workspace`, `delete_workspace`). Each one inherits the default `min_role="member"` from `require_workspace_member`. Any basic member can therefore promote themselves to admin or owner, demote or remove other members, and delete the workspace. The role hierarchy exists in the schema but is not enforced. Registration is open at `/api/v1/auth/register` with no email verification. The default server bind is `0.0.0.0:8000` (`python -m praisonai_platform`). One curl from any unauthenticated network position is enough to bootstrap into the system. PraisonAI Platform version 0.1.4 patches the issue.

### CVE-2026-8152

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-601` |
| Published | 2026-07-22T13:16:38.423 |

Unblu Spark contains an open redirect vulnerability that can be escalated to a DOM-based cross-site scripting (XSS) attack.


When Unblu Spark is deployed with com.unblu.identifier.siteEmbeddedSetup=true, it runs in the same origin as the host application. Any JavaScript injected through this vulnerability therefore executes with full access to the host application's cookies, DOM, and same-origin APIs — an attacker can reach all resources of the host application, not just Unblu's. This expanded blast radius is the reason on-premises deployments using this configuration are rated CRITICAL.

### CVE-2026-61207

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:52.447 |

Vulnerability in the PeopleSoft Enterprise SCM eProcurement product of Oracle PeopleSoft (component: Manage Requisition Status).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise SCM eProcurement.  While the vulnerability is in PeopleSoft Enterprise SCM eProcurement, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise SCM eProcurement accessible data as well as  unauthorized update, insert or delete access to some of PeopleSoft Enterprise SCM eProcurement accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-61175

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:49.290 |

Vulnerability in the Oracle Product Lifecycle Analytics product of Oracle Supply Chain (component: Installation Issues).   The supported version that is affected is 3.6.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Product Lifecycle Analytics.  While the vulnerability is in Oracle Product Lifecycle Analytics, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Product Lifecycle Analytics accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Product Lifecycle Analytics. CVSS 3.1 Base Score 9.3 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L).

### CVE-2026-60632

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:03.850 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-60631

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:03.733 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-60248

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:26.700 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Coherence executes to compromise Oracle Coherence.  While the vulnerability is in Oracle Coherence, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60220

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:23.540 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Coherence, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Coherence accessible data as well as  unauthorized access to critical data or complete access to all Oracle Coherence accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-47708

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-07-21T21:16:51.477 |

MCP-for-Stata is an MCP server for Stata to integrate Stata into an agent. Prior to version 1.17.3, the `log_file_name` parameter in the `stata_do` API and CLI is directly interpolated into a Stata command string without sanitization. The security guard (`GuardValidator`) only scans the do-file content but does not validate this parameter. An attacker can inject arbitrary Stata commands (including `shell`, `python`, `erase`, etc.) by crafting a malicious `log_file_name` containing quotes, newlines, or Stata command separators. Version 1.17.3 contains a patch for the issue.

### CVE-2016-20096

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-21T19:17:07.357 |

Linknat VOS3000 and VOS2009 through version 2.1.2.0 contain an unauthenticated SQL injection vulnerability that allows remote attackers to execute arbitrary SQL commands by manipulating the name parameter in a POST request to the login endpoint. Attackers can inject malicious SQL through the login form and retrieve injected query results from a subsequent session request, enabling extraction of plaintext credentials and other database content with DBA-level privileges.

### CVE-2026-64824

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-21T16:17:21.433 |

Home Assistant Core before 2026.7.0 contains a path traversal vulnerability in the backup-restore function that allows attackers to write files to arbitrary absolute filesystem paths by supplying a crafted tar archive with a SYMTYPE entry containing a benign member name paired with an absolute linkname pointing outside the extraction directory. Because the official Docker image runs the Home Assistant process as root and the subsequent regular-file entry is written through the unvalidated symlink, attackers can achieve remote code execution by overwriting auto-imported Python paths such as site-packages/sitecustomize.py or custom component directories.

### CVE-2026-65048

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-21T15:16:38.813 |

Ninja Forms plugin for WordPress versions 3.10.4 through 3.14.9 contains an unauthenticated stored cross-site scripting vulnerability in the Repeatable Fieldset feature where parseSubmissionIndex() accepts arbitrary strings as submission indexes without numeric validation, and admin_form_element() interpolates the index directly into HTML without escaping. An unauthenticated attacker can submit a public form with a crafted repeater child key containing malicious script payloads, which execute in an administrator's browser when viewing submissions in the WordPress admin panel, enabling session-cookie theft, creation of administrator accounts, installation of malicious plugins, and arbitrary modification of site content.

### CVE-2026-65318

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-21T22:19:10.490 |

Verba RAG application version 2.1.3 contains an unauthenticated server-side request forgery vulnerability that allows unauthenticated attackers to cause the backend to issue arbitrary HTTP GET requests by supplying attacker-controlled URLs through the WebSocket import endpoint. Attackers can connect to the /ws/import_files WebSocket endpoint without authentication, specify arbitrary URLs in the HTMLReader configuration, and cause the server to fetch internal resources such as co-located database endpoints or cloud instance metadata services to retrieve sensitive credentials.

### CVE-2026-65317

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-21T22:19:10.340 |

Verba RAG application version 2.1.3 contains a server-side request forgery vulnerability combined with a same-origin middleware bypass that allows unauthenticated remote attackers to make the server issue arbitrary HTTP requests by supplying a crafted Origin header and attacker-controlled host and port values. Attackers can bypass the localhost origin check in the API middleware by sending any Origin value prefixed with ' regardless of port, then submit arbitrary host and port parameters to the /api/connect endpoint to cause the server to issue outbound GET requests to attacker-controlled infrastructure.

### CVE-2026-65057

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-21T21:16:54.427 |

Keep (commit 91c75e0) contains a server-side request forgery vulnerability that allows unauthenticated attackers to make the backend issue arbitrary HTTP requests by supplying attacker-controlled host values to the unprotected healthcheck endpoint. Attackers can send a crafted JSON payload with a malicious host parameter to cause the backend to issue outbound requests to internal services or cloud metadata endpoints, enabling theft of cloud credentials and internal network reconnaissance.

### CVE-2026-63764

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-21T21:16:53.350 |

lmdeploy's OpenAI-compatible API server contains a server-side request forgery vulnerability that allows unauthenticated attackers to access internal services and cloud metadata endpoints by supplying a crafted image_url that redirects to internal targets. Attackers can send a POST request to the chat completions endpoint with an image_url pointing to an attacker-controlled server that responds with an HTTP 302 redirect to internal addresses such as loopback or instance-metadata endpoints, bypassing the initial URL safety check because redirects are followed without re-validating each hop through the safety guard.

### CVE-2026-62546

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:08.213 |

Vulnerability in the Oracle Applications Framework product of Oracle E-Business Suite (component: Web Utilities).  Supported versions that are affected are 12.2.8-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Applications Framework.  While the vulnerability is in Oracle Applications Framework, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Applications Framework. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61244

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:55.230 |

Vulnerability in the PeopleSoft Enterprise FIN Manufacturing Argentina product of Oracle PeopleSoft (component: Manufacturing).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Manufacturing Argentina.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise FIN Manufacturing Argentina accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise FIN Manufacturing Argentina accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61238

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:54.687 |

Vulnerability in the PeopleSoft Enterprise FIN Common Objects Argentina product of Oracle PeopleSoft (component: eProcurement).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Common Objects Argentina.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise FIN Common Objects Argentina accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise FIN Common Objects Argentina accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61235

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:54.357 |

Vulnerability in the PeopleSoft Enterprise HCM Global Payroll Switzerland product of Oracle PeopleSoft (component: Global Payroll for Switzerland).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise HCM Global Payroll Switzerland.  While the vulnerability is in PeopleSoft Enterprise HCM Global Payroll Switzerland, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise HCM Global Payroll Switzerland. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61197

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:51.620 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Identity Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Identity Manager accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61184

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:50.233 |

Vulnerability in the Oracle Agile Product Lifecycle Management for Process product of Oracle Supply Chain (component: Product Quality Management).   The supported version that is affected is 6.2.4. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Agile Product Lifecycle Management for Process.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Agile Product Lifecycle Management for Process accessible data as well as  unauthorized access to critical data or complete access to all Oracle Agile Product Lifecycle Management for Process accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61171

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:48.817 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Security).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Agile PLM accessible data as well as  unauthorized access to critical data or complete access to all Oracle Agile PLM accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61156

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:47.110 |

Vulnerability in the Oracle Commerce Guided Search Platform Services product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Commerce Guided Search Platform Services.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search Platform Services accessible data as well as  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search Platform Services accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61155

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:46.977 |

Vulnerability in the Oracle Commerce Guided Search Platform Services product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search Platform Services.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search Platform Services accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Commerce Guided Search Platform Services. CVSS 3.1 Base Score 9.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H).

### CVE-2026-61153

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:46.760 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61130

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:44.280 |

Vulnerability in the Oracle Commerce Platform product of Oracle Commerce (component: Dynamo Application Framework).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Platform.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Platform accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Commerce Platform. CVSS 3.1 Base Score 9.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H).

### CVE-2026-61059

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:36.620 |

Vulnerability in the PeopleSoft Enterprise SCM Order Management product of Oracle PeopleSoft (component: Security).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise SCM Order Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise SCM Order Management accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise SCM Order Management accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60649

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:05.757 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Web Content Management).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60606

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:00.903 |

Vulnerability in the PeopleSoft Enterprise CC Common Application Objects product of Oracle PeopleSoft (component: Common Application Objects).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise CC Common Application Objects.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise CC Common Application Objects accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise CC Common Application Objects accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60567

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:56.927 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Identity Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Identity Manager accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60438

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:46.283 |

Vulnerability in the Oracle HTTP Server product of Oracle Fusion Middleware (component: mod_ssl).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle HTTP Server.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle HTTP Server accessible data as well as  unauthorized access to critical data or complete access to all Oracle HTTP Server accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60326

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:35.593 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Access Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Access Manager accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60267

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:28.827 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TLS to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Coherence accessible data as well as  unauthorized access to critical data or complete access to all Oracle Coherence accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60208

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:22.180 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebLogic Server accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebLogic Server accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60168

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:17.590 |

Vulnerability in the Oracle Hospitality Simphony product of Oracle Food and Beverage Applications (component: POS).  Supported versions that are affected are 19.8-19.8.5, 19.9-19.9.3 and  19.10. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hospitality Simphony.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hospitality Simphony accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hospitality Simphony. CVSS 3.1 Base Score 9.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-47731

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-21T22:17:13.230 |

The AMMOS Instrument Toolkit (Formerly the Bespoke Links to Instruments for Surface and Space (BLISS)) is a Python-based software suite developed to handle Ground Data System (GDS), Electronic Ground Support Equipment (EGSE), commanding, telemetry uplink/downlink, and sequencing for instrument and CubeSat Missions. In versions prior to 2.6.1 and in version 3.1.0, the Binary Stream Capture (BSC) component exposes an unauthenticated HTTP API for dynamically creating packet capture "handlers." Because the code blindly trusts path‑related form fields, a remote client can bypass the configured log root and direct BSC to log to arbitrary filesystem paths (path traversal / directory escape), and append attacker‑controlled data to those files, using the privileges of the`ait-bsc` process. There are two ways for a remote attacker to trigger this. First, if the attacker has access to the network where `ait-bsc` is deployed (a reason for that could be that the ports are publicly accessible), the payloads can be directly sent to the server to trigger the arbitrary file append. This type of attack is demonstrated in `python_poc.py`. Second, even if the attacker does not have direct access to the network because the software is running in a local network, it is possible to exploit this if a bad actor in that network opens an attacker-controlled website (which might be a website created by an attacker, or a third-party website compromised by the attacker). The browser javascript can automatically send the requests necessary to exploit this into the local network. This is even possible if the server is only accessible on `localhost`. This type of attack is demonstrated by `attacker_tcp.py` and `test1.html` (first launch the attacker TCP server, then start a webserver to host `test1.html`, for example using `python3 -m http.server 7000`, and open `test1.html`).This issue affects BSC (Binary Stream Capture) and usage of the ait-bsc server. This impacts AIT-Core versions before 3.1.1, from 2.x before 2.6.1. Users are recommended to upgrade to version 3.1.1 or 2.6.1.

### CVE-2026-47040

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:09.667 |

Vulnerability in the Oracle Net Services component of Oracle Database Server.  Supported versions that are affected are 19.3-19.31, 21.3-21.22 and  23.4.0-23.26.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via Oracle Net to compromise Oracle Net Services.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Net Services accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Net Services. CVSS 3.1 Base Score 9.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H).

### CVE-2026-46989

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:04.037 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: UI Framework).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  While the vulnerability is in Oracle Enterprise Manager Base Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Enterprise Manager Base Platform accessible data as well as  unauthorized update, insert or delete access to some of Oracle Enterprise Manager Base Platform accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L).

### CVE-2026-28321

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-21T16:17:10.293 |

SolarWinds Serv-U is affected by a broken access control vulnerability that could allow arbitrary file read and write, which can then be used to escalate privileges and execute code as root. A domain administrator access is required, and the impact is lower in Windows installations.

### CVE-2026-28317

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-21T16:17:10.157 |

SolarWinds Serv-U is affected by an insecure direct object reference (IDOR) vulnerability that can lead to privilege escalation. This issue requires domain administrator access. The impact is lower in Windows deployments.

### CVE-2026-28316

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-21T16:17:09.943 |

SolarWinds Serv-U is affected by an insecure direct object reference (IDOR) vulnerability that can lead to privilege escalation to a system administrator with the ability to execute commands as the root user. This issue requires a domain account with administrator access. The impact is lower in Windows deployments.

### CVE-2026-28314

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-21T16:17:09.283 |

SolarWinds Serv-U is affected by an insecure direct object reference vulnerability that leads to an account takeover. User authentication is required. The impact is lower in Windows deployments.

### CVE-2026-28313

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-21T16:17:09.147 |

SolarWinds Serv-U is affected by an insecure direct object reference (IDOR) vulnerability that can lead to SMTP hijacking leading to arbitrary account takeover. The impact is lower in Windows deployments.

### CVE-2026-28312

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-21T16:17:09.000 |

SolarWinds Serv-U is affected by a privilege escalation vulnerability. This would elevate a group’s access to system administrator and allow code execution as root. The impact is lower in Windows deployments.

### CVE-2026-28310

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-21T16:17:08.877 |

SolarWinds Serv-U is affected by a privilege escalation vulnerability that allows a domain administrator to escalate their user type to that of a system administrator. The impact is lower in Windows deployments.

### CVE-2026-28309

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-21T16:17:08.743 |

SolarWinds Serv-U is affected by a broken access control vulnerability that allows a domain administrator to create system administrator accounts. The impact is lower in Windows deployments.

### CVE-2026-28308

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-21T16:17:08.577 |

SolarWinds Serv-U is affected by an insecure direct object reference (IDOR) vulnerability that can lead to remote code execution. Domain administrator access is required. The impact is lower in Windows deployments.

### CVE-2026-28307

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-21T16:17:08.443 |

SolarWinds Serv-U is affected by a privilege escalation vulnerability that allows a domain user group to be elevated into an administrator group. The impact is lower in Windows deployments.

### CVE-2026-28306

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-21T16:17:08.317 |

SolarWinds Serv-U is affected by a privilege escalation vulnerability that allows a domain administrator to elevate their privileges to a system administrator. The impact is lower in Windows deployments.

### CVE-2026-28305

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-21T16:17:08.180 |

SolarWinds Serv-U is affected by an insecure direct object reference (IDOR) vulnerability that can lead to remote code execution as root. A domain account with admin privileges and read and write access to the home directory is required. The impact is lower in Windows deployments.

### CVE-2026-28304

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-21T16:17:08.050 |

SolarWinds Serv-U is affected by a remote code execution vulnerability that, when exploited, can allow the arbitrary execution of code remotely as root. The impact is lower in Windows deployments.

### CVE-2026-28302

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-21T16:17:07.903 |

SolarWinds Serv-U is affected by an insecure direct object reference (IDOR) vulnerability that can lead to privilege escalation and remote code execution as root. This issue requires group administrator access. The impact is lower in Windows deployments.

### CVE-2026-61223

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:53.577 |

Vulnerability in the Oracle Communications Converged Application Server product of Oracle Communications (component: Security).  Supported versions that are affected are 8.2 and  8.3. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TCP/IP to compromise Oracle Communications Converged Application Server.  While the vulnerability is in Oracle Communications Converged Application Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Communications Converged Application Server. CVSS 3.1 Base Score 9.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61204

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:52.180 |

Vulnerability in the PeopleSoft Enterprise FIN Program Management product of Oracle PeopleSoft (component: Primavera Integration).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Program Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in PeopleSoft Enterprise FIN Program Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise FIN Program Management. CVSS 3.1 Base Score 9.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-61201

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:51.837 |

Vulnerability in the PeopleSoft Enterprise CRM Common Objects product of Oracle PeopleSoft (component: Common Objects).   The supported version that is affected is 9.2.23. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise CRM Common Objects.  While the vulnerability is in PeopleSoft Enterprise CRM Common Objects, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise CRM Common Objects. CVSS 3.1 Base Score 9.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61174

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:49.170 |

Vulnerability in the Oracle Product Lifecycle Analytics product of Oracle Supply Chain (component: Installation Issues).   The supported version that is affected is 3.6.1. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Product Lifecycle Analytics executes to compromise Oracle Product Lifecycle Analytics.  While the vulnerability is in Oracle Product Lifecycle Analytics, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Product Lifecycle Analytics accessible data as well as  unauthorized access to critical data or complete access to all Oracle Product Lifecycle Analytics accessible data. CVSS 3.1 Base Score 9.0 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60424

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:44.797 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Unified Directory.  While the vulnerability is in Oracle Unified Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Unified Directory. CVSS 3.1 Base Score 9.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60249

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:26.813 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with access to the physical communication segment attached to the hardware where the Oracle Coherence executes to compromise Oracle Coherence.  While the vulnerability is in Oracle Coherence, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-64825

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-21T16:17:21.633 |

Home Assistant Core before 2026.6.0 contains a path traversal vulnerability that allows unauthenticated attackers to write arbitrary files to any directory on the host filesystem by uploading a crafted backup archive during the initial onboarding window. Attackers can manipulate the 'name' field inside the uploaded archive's backup.json to supply an absolute path, causing pathlib.Path.__truediv__ to discard the configured backup directory prefix and write attacker-controlled content to arbitrary locations, with full filesystem access when the process runs as root.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-65598

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-07-22T12:18:20.037 |

n8n before 1.123.64, 2.29.8, and 2.30.1 contains a TOCTOU race condition in the Git node's clone operation that allows authenticated users to bypass path restrictions by swapping a directory for a symlink after the path is validated but before the clone runs. This lets an attacker plant a crafted repository in the community node directory, which n8n loads as a custom node on the next restart, executing arbitrary JavaScript on the server. Both self-hosted and cloud instances are affected.

### CVE-2026-65595

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-22T12:18:19.660 |

n8n before 2.30.1 and 2.29.8 assigns all Public API key scopes to JWTs issued through the Token Exchange module regardless of the acting user's role. On instances where the Token Exchange feature and Public API are enabled, a low-privileged user who can obtain a valid external JWT trusted by a configured issuer can use the resulting access token to invoke administrator-only Public API operations such as role escalation, user creation, and user deletion (role escalation requires an Advanced Permissions license), and, when unverified Community Package installation is enabled, achieve remote code execution.

### CVE-2026-65591

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-917` |
| Published | 2026-07-22T12:18:19.117 |

n8n contains a sanitizer bypass vulnerability in the legacy expression evaluator's computed-member handler. An authenticated user with workflow create or modify permissions can craft a malicious expression to bypass the sanitizer and achieve host-level code execution as the n8n process. The legacy expression engine is the default in affected versions. Fixed in n8n 1.123.64, 2.29.8, and 2.30.1.

### CVE-2026-43947

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-21T22:17:01.560 |

FUXA is a web-based Process Visualization (SCADA/HMI/Dashboard) software. Version 1.3.0 has an unauthenticated Remote Code Execution vulnerability when `secureEnabled` is set to `true`. The `POST /api/runscript` endpoint checks authorization against the stored script's permission by ID, but when `test: true` is set in the request, it compiles and executes attacker-supplied code instead of the stored script's code. An unauthenticated attacker who knows a valid script ID and name may execute arbitrary code via test mode if at least one server-side script exists and is accessible without restrictive permissions. Script IDs and names can be obtained through the unauthenticated information disclosure in `GET /api/project` (reported separately). The only prerequisite is that at least one server-side script exists in the project. Version 1.3.1 fixes the issue.

### CVE-2026-43945

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-284;CWE-288;CWE-863` |
| Published | 2026-07-21T22:17:01.250 |

FUXA is a web-based Process Visualization (SCADA/HMI/Dashboard) software. Versions 1.2.11 until 1.3.1 allow an unauthenticated remote attacker to achieve Full Remote Code Execution (RCE) as root. The exploit succeeds even when the platform is configured in its most secure state (Secure Mode Enabled and Node-RED Secure Auth Enabled). Version 1.3.1 fixes the issue.

### CVE-2026-14551

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-73;CWE-269;CWE-379` |
| Published | 2026-07-22T10:17:13.810 |

The servereye client (also known as sensorhub, technically ClientAgentContainerService) versions 20.15 and earlier are vulnerable to Local Privilege Escalation. The high-privileged service SE3Recovery (EmergencyRecoveryService.exe), running as SYSTEM, periodically monitors the directory %ProgramData%\ServerEye3\update\ for a trigger file named "update_available". Due to insufficient access restrictions on this directory, a local standard user can create the trigger file and provide a path to a directory containing malicious JSON instructions. The service subsequently executes the utility UpdaterAction.exe with SYSTEM privileges, which parses the instructions and performs an unvalidated file copy from a user-controlled source to a protected system destination (e.g., overwriting a service binary). This leads to full system compromise as the service automatically restarts the overwritten binary with SYSTEM privileges.

### CVE-2026-3821

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-22T07:16:35.413 |

Supermicro (SMC) SMASH services contain an Arbitrary code execution issue in X14DBG-DAP and X14DBI.
An authorized attacker can exploit SMASH’s input capability to compromise data integrity or launch a Denial-of-Service (DoS) attack against the BMC.

### CVE-2026-12968

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-22T07:16:34.710 |

The Product Addons and Product Options With Custom Fields  WordPress plugin before 1.6.15 does not restrict an unauthenticated file-upload endpoint and accepts SVG files that are stored and served inline, allowing an unauthenticated attacker to upload a malicious SVG whose embedded script executes in the session of any user (such as an administrator) who later opens the file.

### CVE-2026-16423

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-21T23:16:59.923 |

Use after free in UI in Google Chrome prior to 150.0.7871.182 allowed a remote attacker who convinced a user to engage in specific UI gestures to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-62534

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:07.990 |

Vulnerability in the Oracle Applications Framework product of Oracle E-Business Suite (component: Web Utilities).  Supported versions that are affected are 12.2.11-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Applications Framework.  Successful attacks of this vulnerability can result in takeover of Oracle Applications Framework. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62516

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:06.827 |

Vulnerability in the Oracle Demantra Demand Management product of Oracle Supply Chain (component: Product Security).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via SQL to compromise Oracle Demantra Demand Management.  Successful attacks of this vulnerability can result in takeover of Oracle Demantra Demand Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62498

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:05.830 |

Vulnerability in the Oracle Flow Manufacturing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.7-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Flow Manufacturing.  Successful attacks of this vulnerability can result in takeover of Oracle Flow Manufacturing. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62496

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:05.603 |

Vulnerability in the Oracle Yard Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.6-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Yard Management.  Successful attacks of this vulnerability can result in takeover of Oracle Yard Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62478

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:04.027 |

Vulnerability in the Oracle Public Sector Financials product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Public Sector Financials.  Successful attacks of this vulnerability can result in takeover of Oracle Public Sector Financials. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62476

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:03.913 |

Vulnerability in the Oracle Public Sector Payroll product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Public Sector Payroll.  Successful attacks of this vulnerability can result in takeover of Oracle Public Sector Payroll. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62464

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:02.883 |

Vulnerability in the Oracle Payroll product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Payroll.  Successful attacks of this vulnerability can result in takeover of Oracle Payroll. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62447

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:02.393 |

Vulnerability in the Oracle Trade Management product of Oracle E-Business Suite (component: Claim LOV).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Trade Management.  Successful attacks of this vulnerability can result in takeover of Oracle Trade Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61322

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:00.543 |

Vulnerability in the TeleSales product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise TeleSales.  Successful attacks of this vulnerability can result in takeover of TeleSales. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61320

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:00.430 |

Vulnerability in the Oracle Payables product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.8-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Payables.  Successful attacks of this vulnerability can result in takeover of Oracle Payables. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61311

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:59.873 |

Vulnerability in the Oracle Product Hub product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Hub.  Successful attacks of this vulnerability can result in takeover of Oracle Product Hub. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61289

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:58.747 |

Vulnerability in the Oracle Process Manufacturing Product Development product of Oracle E-Business Suite (component: Quality Management Specs).   The supported version that is affected is 12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Product Development.  Successful attacks of this vulnerability can result in takeover of Oracle Process Manufacturing Product Development. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61243

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:55.123 |

Vulnerability in the PeopleSoft Enterprise FIN Common Objects Argentina product of Oracle PeopleSoft (component: Staffing).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Common Objects Argentina.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise FIN Common Objects Argentina. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61180

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:49.753 |

Vulnerability in the Oracle Agile Product Lifecycle Management for Process product of Oracle Supply Chain (component: Product Quality Management).   The supported version that is affected is 6.2.4. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile Product Lifecycle Management for Process.  Successful attacks of this vulnerability can result in takeover of Oracle Agile Product Lifecycle Management for Process. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61179

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:49.637 |

Vulnerability in the Oracle Agile Product Lifecycle Management for Process product of Oracle Supply Chain (component: Product Quality Management).   The supported version that is affected is 6.2.4. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile Product Lifecycle Management for Process.  Successful attacks of this vulnerability can result in takeover of Oracle Agile Product Lifecycle Management for Process. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61168

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:48.477 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Security).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks of this vulnerability can result in takeover of Oracle Agile PLM. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61166

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:48.250 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: User and User Group).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks of this vulnerability can result in takeover of Oracle Agile PLM. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61149

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:46.320 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61148

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:46.207 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61127

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:43.940 |

Vulnerability in the Oracle Communications Service Catalog and Design product of Oracle Communications (component: Solution Designer).  Supported versions that are affected are 8.0.0.7.0-8.3.0.2.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Communications Service Catalog and Design.  Successful attacks of this vulnerability can result in takeover of Oracle Communications Service Catalog and Design. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61121

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:43.380 |

Vulnerability in the Oracle HRMS (UK) product of Oracle E-Business Suite (component: UK Payroll).  Supported versions that are affected are 12.2.8-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle HRMS (UK).  Successful attacks of this vulnerability can result in takeover of Oracle HRMS (UK). CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61110

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:42.260 |

Vulnerability in the Oracle Applications DBA product of Oracle E-Business Suite (component: ADPatch).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Applications DBA.  Successful attacks of this vulnerability can result in takeover of Oracle Applications DBA. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61099

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:41.023 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61098

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:40.910 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61063

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:37.090 |

Vulnerability in the PeopleSoft Enterprise SCM Supplier Contract Management product of Oracle PeopleSoft (component: Security).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where PeopleSoft Enterprise SCM Supplier Contract Management executes to compromise PeopleSoft Enterprise SCM Supplier Contract Management.  While the vulnerability is in PeopleSoft Enterprise SCM Supplier Contract Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise SCM Supplier Contract Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61062

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:36.977 |

Vulnerability in the PeopleSoft Enterprise FIN Cash Management product of Oracle PeopleSoft (component: Cash Management).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where PeopleSoft Enterprise FIN Cash Management executes to compromise PeopleSoft Enterprise FIN Cash Management.  While the vulnerability is in PeopleSoft Enterprise FIN Cash Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise FIN Cash Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61010

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:32.907 |

Vulnerability in the Oracle Process Manufacturing Systems product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Systems.  Successful attacks of this vulnerability can result in takeover of Oracle Process Manufacturing Systems. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60989

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:32.017 |

Vulnerability in the Oracle Advanced Collections product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Advanced Collections.  Successful attacks of this vulnerability can result in takeover of Oracle Advanced Collections. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60960

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:30.223 |

Vulnerability in the Oracle SDP Number Portability product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle SDP Number Portability executes to compromise Oracle SDP Number Portability.  While the vulnerability is in Oracle SDP Number Portability, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle SDP Number Portability. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60952

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:29.770 |

Vulnerability in the Oracle Transportation Execution product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Transportation Execution.  Successful attacks of this vulnerability can result in takeover of Oracle Transportation Execution. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60932

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:28.227 |

Vulnerability in the Oracle Labor Distribution product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Labor Distribution.  Successful attacks of this vulnerability can result in takeover of Oracle Labor Distribution. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60924

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:27.470 |

Vulnerability in the Oracle Public Sector Payroll product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Public Sector Payroll.  Successful attacks of this vulnerability can result in takeover of Oracle Public Sector Payroll. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60920

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:27.140 |

Vulnerability in the Oracle Customer Care product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Customer Care.  Successful attacks of this vulnerability can result in takeover of Oracle Customer Care. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60901

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:25.910 |

Vulnerability in the Oracle Project Intelligence product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Project Intelligence.  Successful attacks of this vulnerability can result in takeover of Oracle Project Intelligence. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60898

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:25.570 |

Vulnerability in the Oracle Warehouse Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Warehouse Management.  Successful attacks of this vulnerability can result in takeover of Oracle Warehouse Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60897

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:25.463 |

Vulnerability in the Oracle Payroll product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Payroll.  Successful attacks of this vulnerability can result in takeover of Oracle Payroll. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60890

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:24.810 |

Vulnerability in the Oracle Payroll product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Payroll.  Successful attacks of this vulnerability can result in takeover of Oracle Payroll. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60872

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:24.130 |

Vulnerability in the Oracle Order Management product of Oracle E-Business Suite (component: Product Diagnostic Tools).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Order Management.  Successful attacks of this vulnerability can result in takeover of Oracle Order Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60863

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:23.440 |

Vulnerability in the Oracle Advanced Pricing product of Oracle E-Business Suite (component: Pricing Installation).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Advanced Pricing.  Successful attacks of this vulnerability can result in takeover of Oracle Advanced Pricing. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60829

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:20.890 |

Vulnerability in the Oracle Advanced Outbound Telephony product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Advanced Outbound Telephony.  Successful attacks of this vulnerability can result in takeover of Oracle Advanced Outbound Telephony. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60789

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:17.960 |

Vulnerability in the Oracle Sales Offline product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales Offline.  Successful attacks of this vulnerability can result in takeover of Oracle Sales Offline. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60783

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:17.260 |

Vulnerability in the Oracle iReceivables product of Oracle E-Business Suite (component: AR Web Utilities).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iReceivables.  Successful attacks of this vulnerability can result in takeover of Oracle iReceivables. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60738

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:14.227 |

Vulnerability in the Oracle Installed Base product of Oracle E-Business Suite (component: Create Item Instance).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Installed Base.  Successful attacks of this vulnerability can result in takeover of Oracle Installed Base. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60692

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:10.037 |

Vulnerability in the Oracle Enterprise Asset Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Enterprise Asset Management.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Asset Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60681

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:08.910 |

Vulnerability in the Oracle Process Manufacturing Regulatory Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Regulatory Management.  Successful attacks of this vulnerability can result in takeover of Oracle Process Manufacturing Regulatory Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60678

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:08.793 |

Vulnerability in the Oracle General Ledger product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via SOAP to compromise Oracle General Ledger.  Successful attacks of this vulnerability can result in takeover of Oracle General Ledger. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60676

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:08.573 |

Vulnerability in the Oracle Applications Framework product of Oracle E-Business Suite (component: Search Bean).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Applications Framework.  Successful attacks of this vulnerability can result in takeover of Oracle Applications Framework. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60675

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:08.453 |

Vulnerability in the Oracle Applications Framework product of Oracle E-Business Suite (component: Search Bean).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Applications Framework.  Successful attacks of this vulnerability can result in takeover of Oracle Applications Framework. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60664

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:07.270 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60656

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:06.597 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Web Content Management).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60655

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:06.487 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Web Content Management).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60654

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:06.370 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Web Content Management).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60651

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:06.010 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Web Content Management).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60639

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:04.633 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60638

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:04.520 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60637

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:04.410 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60636

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:04.297 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60635

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:04.190 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60634

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:04.077 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60633

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:03.967 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60618

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:02.253 |

Vulnerability in the JD Edwards EnterpriseOne Procurement and Subcontract Management product of Oracle JD Edwards (component: Procurement).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Procurement and Subcontract Management.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Procurement and Subcontract Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60603

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:00.530 |

Vulnerability in the PeopleSoft Enterprise CS Student Records product of Oracle PeopleSoft (component: Australian Features).   The supported version that is affected is 9.2.38. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise CS Student Records.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise CS Student Records. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60602

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:00.413 |

Vulnerability in the PeopleSoft Enterprise CS Student Financials product of Oracle PeopleSoft (component: Billing).   The supported version that is affected is 9.2.38. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise CS Student Financials.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise CS Student Financials. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60594

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:59.500 |

Vulnerability in the PeopleSoft Enterprise CS Campus Community product of Oracle PeopleSoft (component: Integration and Interfaces).   The supported version that is affected is 9.2.38. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise CS Campus Community.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise CS Campus Community. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60583

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:58.710 |

Vulnerability in the Oracle Transportation Management product of Oracle Supply Chain (component: Install).   The supported version that is affected is 6.5.3. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Transportation Management.  Successful attacks of this vulnerability can result in takeover of Oracle Transportation Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60580

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:58.363 |

Vulnerability in the Oracle Enterprise Command Center Framework product of Oracle E-Business Suite (component: Core).   The supported version that is affected is V16. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Enterprise Command Center Framework executes to compromise Oracle Enterprise Command Center Framework.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Command Center Framework. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60563

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:56.460 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60549

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:54.850 |

Vulnerability in the Oracle Managed File Transfer product of Oracle Fusion Middleware (component: MFT Runtime Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Managed File Transfer.  Successful attacks of this vulnerability can result in takeover of Oracle Managed File Transfer. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60545

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:54.393 |

Vulnerability in the Oracle Managed File Transfer product of Oracle Fusion Middleware (component: MFT Runtime Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Managed File Transfer.  Successful attacks of this vulnerability can result in takeover of Oracle Managed File Transfer. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60539

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:53.733 |

Vulnerability in the Oracle SOA Suite product of Oracle Fusion Middleware (component: Integration Business Insight).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle SOA Suite.  Successful attacks of this vulnerability can result in takeover of Oracle SOA Suite. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60503

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:51.370 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise WebCenter Content: Imaging.  Successful attacks of this vulnerability can result in takeover of WebCenter Content: Imaging. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60499

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:51.023 |

Vulnerability in the JD Edwards EnterpriseOne Solution Advisor product of Oracle JD Edwards (component: Solution Advisor).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Solution Advisor.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Solution Advisor. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60493

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:50.327 |

Vulnerability in the JD Edwards EnterpriseOne Human Resources Management product of Oracle JD Edwards (component: Human Resources).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Human Resources Management.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Human Resources Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60490

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:49.987 |

Vulnerability in the JD Edwards EnterpriseOne CRM Foundation product of Oracle JD Edwards (component: CRM Foundation).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise JD Edwards EnterpriseOne CRM Foundation.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne CRM Foundation. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60489

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:49.873 |

Vulnerability in the JD Edwards EnterpriseOne CRM Foundation product of Oracle JD Edwards (component: CRM Foundation).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise JD Edwards EnterpriseOne CRM Foundation.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne CRM Foundation. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60472

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:49.760 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise WebCenter Content: Imaging.  Successful attacks of this vulnerability can result in takeover of WebCenter Content: Imaging. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60465

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:48.963 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise WebCenter Content: Imaging.  Successful attacks of this vulnerability can result in takeover of WebCenter Content: Imaging. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60464

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:48.853 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise WebCenter Content: Imaging.  Successful attacks of this vulnerability can result in takeover of WebCenter Content: Imaging. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60430

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:45.500 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Unified Directory. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60423

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:44.680 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Unified Directory. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60419

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:44.207 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Unified Directory. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60400

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:42.497 |

Vulnerability in Oracle GoldenGate (component: Admin Server Executable).  Supported versions that are affected are 19.1.0.0.0-19.30.0.0, 21.3-21.21 and  23.4-23.26.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle GoldenGate.  Successful attacks of this vulnerability can result in takeover of Oracle GoldenGate. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60398

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:42.277 |

Vulnerability in Oracle GoldenGate (component: Oracle GoldenGate Microservices).  Supported versions that are affected are 19.1.0.0.0-19.30.0.0, 21.3-21.21 and  23.4-23.26.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle GoldenGate.  Successful attacks of this vulnerability can result in takeover of Oracle GoldenGate. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60343

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:37.363 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60334

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:36.473 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60313

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:34.063 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via RMI to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60309

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:33.603 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Coherence executes to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60268

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:28.933 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60261

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:28.153 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Coherence executes to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60218

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:23.320 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60211

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:22.517 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Coherence executes to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60207

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:22.070 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60203

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:21.623 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60175

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:18.397 |

Vulnerability in the RDBMS component of Oracle Database Server.  Supported versions that are affected are 19.3-19.31, 21.3-21.22 and  23.4.0-23.26.2. Easily exploitable vulnerability allows low privileged attacker having Authenticated User privilege with network access via Oracle Net to compromise RDBMS.  Successful attacks of this vulnerability can result in takeover of RDBMS. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60157

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:16.320 |

Vulnerability in Oracle GoldenGate (component: Service Manager).  Supported versions that are affected are 19.1.0.0.0-19.29.0.0, 21.3-21.21 and  23.4-23.26.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle GoldenGate.  Successful attacks of this vulnerability can result in takeover of Oracle GoldenGate. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-47037

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:09.283 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).   The supported version that is affected is 14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-47031

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:08.587 |

Vulnerability in the Oracle Bills of Material product of Oracle E-Business Suite (component: Bill Issues).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Bills of Material.  Successful attacks of this vulnerability can result in takeover of Oracle Bills of Material. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-47004

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:05.797 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Self Update Framework).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46998

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:05.123 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Metadata Plugin).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-46995

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:04.780 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Metadata Plugin).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46992

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:04.423 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Enterprise Config Management).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-55084

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-21T19:17:11.223 |

DHIS2 is a flexible information system for data capture, management, validation, analytics and visualization. A SQL injection vulnerability was identified in the SqlView API endpoint of the DHIS2 application in the `filter` parameter used by the
`/api/sqlViews/{viewId}/data.json` endpoint. An authenticated user with access to a SqlView can inject arbitrary SQL queries inside the `filter` parameter by abusing an expression executed by PostgreSQL and its output is reflected inside the application error message. This behavior enables attackers to extract arbitrary database content using error-based SQL injection.

Affected versions include: 2.37, 2.38, 2.39, 2.40.x before 2.40.11.1/2.40.12, 2.41.x before 2.41.8.2, 2.42.x before 2.42.5.1, 2.43.0 before 2.43.0.1, 2.44 development branch before PR #24162
Patched versions include: 2.37-EOS (2026-06-09), 2.38-EOS (2026-06-09), 2.39-EOS (2026-06-09), 2.40.11.1, 2.40.12, 2.41.8.2, 2.42.5.1, 2.43.0.1, 2.44 development branch after PR #24162

### CVE-2026-44880

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T18:16:58.320 |

A buffer overflow vulnerability was found in the command line interface of AOS-CX. Successful exploitation of these vulnerabilities could allow an remote low-privileged user to execute arbitrary code as a privileged user on the underlying operating system.

### CVE-2026-47405

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-862` |
| Published | 2026-07-21T17:17:09.083 |

PraisonAI Platform is the platform layer for the PraisonAI multi-agent teams system. Versions prior to 0.1.4 have a broken workspace authorization check that allows any authenticated low-privilege workspace member to escalate their own role to `owner`. The issue is caused by privileged workspace-management routes using the shared dependency `require_workspace_member(...)` without requiring `admin` or `owner`. The dependency defaults to `min_role="member"`, so routes that should be administrative are accessible to ordinary workspace members. As a result, a normal workspace member can promote their own account from `member` to `owner`; add arbitrary users as `owner` or `admin`; change other members' roles; remove legitimate owners or members; take over workspace membership completely; and/or perform destructive workspace operations after escalation. This is a broken access control / vertical privilege escalation vulnerability. PraisonAI Platform version 0.1.4 patches the issue.

### CVE-2026-47399

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-639` |
| Published | 2026-07-21T17:17:08.950 |

PraisonAI Platform is the platform layer for the PraisonAI multi-agent teams system. Prior to version 0.1.4, the workspace-scoped REST routes contain a systemic object-level authorization flaw that allows an authenticated user from one workspace to access, modify, and delete objects belonging to another workspace by supplying the victim object's global UUID. The affected pattern appears in workspace-scoped routes such as agents, projects, issues, and comments. The route layer verifies that the caller is a member of the `workspace_id` provided in the URL, but the service layer later resolves the target object by global object ID only. It does not verify that the resolved object actually belongs to the workspace in the URL. As a result, a valid member of `workspace_attacker` can call a route under `/api/v1/workspaces/{workspace_attacker}/...` while supplying an object UUID from `workspace_victim`. The server authorizes the request based on membership in `workspace_attacker`, then fetches or mutates the victim object by global UUID. This breaks the platform's workspace isolation boundary. PraisonAI Platform version 0.1.4 patches the issue.

### CVE-2026-59851

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-21T15:16:37.897 |

A flaw was found in libssh. On servers with GSSAPIKeyExchange enabled, the gssapi-keyex path does not verify whether the authenticated Kerberos principal is authorized for the requested local user, allowing authenticated clients to log in as arbitrary users.

### CVE-2026-65603

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-22T12:18:20.683 |

The Grav Login plugin (grav-plugin-login) versions <= 3.8.11 contain a privilege escalation flaw in the authenticated profile self-update handler (processUserProfile(), the update_user task). Unlike the registration handler, this handler does not strip privilege fields ('groups','access') from user-submitted form data before persisting them. When an administrator has added 'groups' and/or 'access' to plugins.login.user_registration.fields and the default 'regular'/DataUser account backend is in use, a low-privilege authenticated user can POST crafted profile form data (e.g. access[admin][super]=true) to escalate to super-admin, enabling admin panel access, scheduler abuse (RCE), and Twig evaluation. Fixed in 3.8.12.

### CVE-2026-65319

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-21T22:19:10.630 |

Feedbin (commit 739884a) contains an unauthenticated information disclosure vulnerability that allows unauthenticated attackers to retrieve private article content by sending requests to the entries text API endpoint, which skips the authorization before-action filter entirely. Attackers can iterate sequential integer entry IDs through the GET /api/v2/entries/:id/text endpoint to enumerate and extract plain-text content of all stored articles, including private newsletter content, personal page-saves, and articles from any user's private subscriptions.

### CVE-2026-65315

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-07-21T22:19:10.050 |

Ollama (HEAD f0078ae) contains an uncontrolled memory allocation vulnerability in the GGUF metadata parser that allows remote attackers to crash the server by supplying a crafted GGUF file with attacker-controlled length and count fields in string lengths, tensor dimension counts, and metadata array counts that are used as allocation sizes without validation against remaining file size. Attackers can upload a sub-1KB crafted GGUF file via the blob upload and model create or pull API endpoints to trigger unrecoverable Go runtime out-of-memory fatal errors or makeslice panics that bypass recovery middleware and crash the entire server process.

### CVE-2026-61078

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:38.637 |

Vulnerability in the PeopleSoft Enterprise CC Common Application Objects product of Oracle PeopleSoft (component: Common Application Objects).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise CC Common Application Objects.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in PeopleSoft Enterprise CC Common Application Objects, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise CC Common Application Objects accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise CC Common Application Objects accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-60941

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:28.900 |

Vulnerability in the Oracle Service Fulfillment Manager product of Oracle E-Business Suite (component: Fulfillment Engine).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Service Fulfillment Manager.  While the vulnerability is in Oracle Service Fulfillment Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Service Fulfillment Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Service Fulfillment Manager accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60597

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:59.840 |

Vulnerability in the PeopleSoft Enterprise FIN Cash Management product of Oracle PeopleSoft (component: Cash Management).   The supported version that is affected is 9.2. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Cash Management.  While the vulnerability is in PeopleSoft Enterprise FIN Cash Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise FIN Cash Management accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise FIN Cash Management accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60553

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:55.290 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  While the vulnerability is in Oracle WebCenter Sites, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Sites accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Sites accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60523

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:51.953 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-60470

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:49.527 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise WebCenter Content: Imaging.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in WebCenter Content: Imaging, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all WebCenter Content: Imaging accessible data as well as  unauthorized access to critical data or complete access to all WebCenter Content: Imaging accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-60469

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:49.413 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise WebCenter Content: Imaging.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in WebCenter Content: Imaging, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all WebCenter Content: Imaging accessible data as well as  unauthorized access to critical data or complete access to all WebCenter Content: Imaging accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-60448

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:47.300 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60443

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:46.747 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-60437

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:46.170 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows high privileged attacker with network access via LDAP to compromise Oracle Unified Directory.  While the vulnerability is in Oracle Unified Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Unified Directory accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Unified Directory. CVSS 3.1 Base Score 8.7 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:H).

### CVE-2026-60427

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:45.130 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Unified Directory.  While the vulnerability is in Oracle Unified Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Unified Directory accessible data as well as  unauthorized access to critical data or complete access to all Oracle Unified Directory accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60214

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:22.863 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with access to the physical communication segment attached to the hardware where the Oracle Coherence executes to compromise Oracle Coherence.  While the vulnerability is in Oracle Coherence, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Coherence accessible data as well as  unauthorized access to critical data or complete access to all Oracle Coherence accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-56745

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-21T22:17:14.500 |

Netty is a network application framework for development of protocol servers and clients. In versions 4.2.0.Final through 4.2.15.Final and 4.1.0.Final through 4.1.135.Final, the `SpdyHttpDecoder` handler in Netty's SPDY-to-HTTP codec allocates a pooled `ByteBuf` when processing a client-initiated `SYN_STREAM` frame with `FLAG_FIN=0` and stores the partially constructed `FullHttpRequest` in `messageMap`; when the remote peer sends `RST_STREAM` for that stream or the accumulated content exceeds `maxContentLength`, the decoder removes the entry but does not release the pooled `ByteBuf`, causing native memory exhaustion. This issue is fixed in versions 4.1.136.Final and 4.2.16.Final.

### CVE-2026-55851

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-21T22:17:14.340 |

Netty is a network application framework for development of protocol servers and clients. In versions 4.2.0.Final up to (but not including) 4.2.16.Final, and 4.1.0.Final up to (but not including) 4.1.135, the `HAProxyMessageDecoder` in Netty's `codec-haproxy` module performs protocol version detection by reading the 13th byte as a signed Java `byte` and widening it to `int` without masking; a PROXY protocol v2 binary prefix followed by version byte `0xFF` sign-extends to `-1`, collides with the decoder's need-more-data sentinel, and causes `ByteToMessageDecoder` to accumulate inbound bytes in an unbounded `cumulation` buffer until direct memory is exhausted. This issue is fixed in versions 4.1.136.Final and 4.2.16.Final.

### CVE-2026-47017

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:07.337 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Process Scheduler).  Supported versions that are affected are 8.61 and  8.62. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in PeopleSoft Enterprise PeopleTools, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise PeopleTools accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PeopleTools accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-64881

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-21T21:16:53.880 |

The audit file upload handler does not sanitize filenames, allowing shell metacharacters to flow into system command execution. This input validation failure enables command injection when chained with a related vulnerability.

### CVE-2026-15957

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-21T20:16:58.780 |

Smithy-RS is a Rust code generation and runtime framework that generates HTTP clients and servers from Smithy interface definitions, powering the AWS SDK for Rust and custom service implementations.



Uncontrolled recursion in the JSON, CBOR, and XML deserializer functions emitted by Amazon smithy-rs code generation could allow remote attackers to cause a denial of service (process abort via stack exhaustion) via a small request containing deeply nested data for a recursive model shape to a generated SDK or server.



To mitigate this issue, users should upgrade to aws-sdk-rust release-2026-06-02 or later. Users building custom servers with smithy-rs codegen should regenerate from smithy-rs release-2026-06-01 or later.

### CVE-2026-55082

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-21T19:17:11.093 |

DHIS2 is a flexible information system for data capture, management, validation, analytics and visualization. DHIS2 SQL View data endpoints allowed authenticated users with SQL View access to provide crafted filter values that were interpolated into generated SQL. An authenticated user with access to SQL View execution could manipulate SQL generated for SQL View filters and potentially access data outside the intended SQL View result set.

This is distinct from CVE-2026-55084, which tracks the related SQL View filter column-name injection.

Known affected release lines for this advisory: DHIS2 2.37, 2.38, and 2.39 before the 2026-06-09 EOS security updates.
Patched by the 2026-06-09 EOS security updates for 2.37, 2.38, and 2.39. The same value-slot hardening was already present on later supported branches through DHIS2-20174 / PR #22253.

### CVE-2026-15724

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-20;CWE-22;CWE-73` |
| Published | 2026-07-21T17:17:04.703 |

In Progress ShareFile Storage Zones Controller versions prior to 5.12.5 and 6.0.2, an authenticated administrative user can exploit a path traversal vulnerability to read arbitrary files from the server filesystem, write files to arbitrary directories, or determine whether specific files exist on the server.

### CVE-2026-47394

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-200;CWE-862` |
| Published | 2026-07-21T16:17:12.440 |

PraisonAI is a multi-agent teams system. Prior to version 4.6.40, the fix for GHSA-9mqq-jqxf-grvw / CVE-2026-44336 is incomplete. The original advisory description named four vulnerable handlers in `mcp_server/adapters/cli_tools.py`. Commit `68cc9427` ("fix(security): harden MCP rules path handling…") added a `_resolve_rule_path()` helper and applied it to `rules.create`, `rules.show`, and `rules.delete`. `workflow.show` was left unchanged. Two adjacent handlers in the same file have the same pattern, `workflow.validate` and `deploy.validate`. Neither was mentioned in the original advisory. Both remained  unchanged. The original advisory also identified the dispatcher (`server.py:281-298`) as a root cause. It accepts unvalidated `**kwargs` from `params["arguments"]` with no enforcement against the tool's declared `input_schema`. That code is unchanged prior to version 4.6.40. A single unauthenticated MCP `tools/call` to `praisonai.workflow.show` returns the contents of any file the host user can read: `/etc/passwd`, `~/.ssh/id_rsa`, `~/.aws/credentials`, or any project `.env`. Version 4.6.40 contains an updated fix.

### CVE-2026-65052

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-472` |
| Published | 2026-07-21T15:16:39.430 |

Ninja Forms WordPress plugin version 3.14.8 and prior contains an improper input validation vulnerability that allows unauthenticated attackers to inject arbitrary numeric values into form calculations and payment totals by submitting values that do not match any configured option in ListSelect or ListRadio fields. Attackers can tamper with form submission payloads to the ajax submit endpoint, causing the get_calc_value() method to fail open and return attacker-controlled values, enabling manipulation of payment amounts to zero or arbitrary figures and bypassing admin-configured pricing logic.

### CVE-2026-8989

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1191;CWE-1244` |
| Published | 2026-07-21T22:19:11.387 |

Autel Maxi Charger Single firmware through V1.03.51 permits unrestricted access to the NXP i.MX6 recovery mode through exposed hardware recovery pins. An attacker with physical access can boot attacker-controlled code in memory and modify or extract firmware and other sensitive data.

### CVE-2026-8988

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1191` |
| Published | 2026-07-21T22:19:11.270 |

Autel Maxi Charger Single firmware through V1.03.51 exposes an accessible UART interface that permits interruption of the boot process and access to the U-Boot bootloader. An attacker with physical access can modify the boot configuration or file system to obtain operating system access.

### CVE-2026-60671

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:08.093 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Business Intelligence Enterprise Edition as well as  unauthorized update, insert or delete access to some of Oracle Business Intelligence Enterprise Edition accessible data and  unauthorized read access to a subset of Oracle Business Intelligence Enterprise Edition accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H).

### CVE-2026-60559

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:55.997 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Access Manager accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60556

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:55.637 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  While the vulnerability is in Oracle WebCenter Sites, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Sites accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60550

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:54.957 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  While the vulnerability is in Oracle WebCenter Sites, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Sites accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60536

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:53.393 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: PeopleSoft Applications).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Identity Manager Connector.  While the vulnerability is in Oracle Identity Manager Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Identity Manager Connector accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60431

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:45.617 |

Vulnerability in the Oracle HTTP Server product of Oracle Fusion Middleware (component: mod_proxy).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle HTTP Server.  While the vulnerability is in Oracle HTTP Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle HTTP Server accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60359

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:39.177 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Unified Directory.  While the vulnerability is in Oracle Unified Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Unified Directory accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60356

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:38.830 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Access Manager accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60327

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:35.707 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Access Manager accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60293

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:31.827 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: WLS - Web Services).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebLogic Server.  While the vulnerability is in Oracle WebLogic Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebLogic Server accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60235

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:25.280 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).   The supported version that is affected is 15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Coherence as well as  unauthorized update, insert or delete access to some of Oracle Coherence accessible data and  unauthorized read access to a subset of Oracle Coherence accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H).

### CVE-2026-15829

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89;CWE-863` |
| Published | 2026-07-21T17:17:05.350 |

A SQL injection (CWE-89) and security boundary bypass (CWE-863) vulnerability exists in the prebuilt BigQuery forecasting tool (bigquery-forecast) of googleapis/mcp-toolbox.

The tool accepts client-controlled parameters (data_col, timestamp_col, and id_cols) as plain strings and interpolates them unescaped via fmt.Sprintf directly into a generated AI.FORECAST table-valued SELECT statement. While MCP Toolbox utilizes an allowedDatasets mechanism to restrict queries, this defense only validates the history_data parameter; the final assembled query is executed without re-validation.

An attacker can break out of the string literal fields (such as timestamp_col) to inject a valid multi-statement or cross-dataset query block. This allows an unauthorized user to bypass the operator-configured allowedDatasets boundary and read arbitrary BigQuery tables.

### CVE-2026-62513

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:06.493 |

Vulnerability in the Oracle Process Manufacturing Regulatory Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Regulatory Management.  While the vulnerability is in Oracle Process Manufacturing Regulatory Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Process Manufacturing Regulatory Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Process Manufacturing Regulatory Management accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-61312

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:59.983 |

Vulnerability in the Oracle Product Hub product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Hub.  While the vulnerability is in Oracle Product Hub, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Product Hub. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60452

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:47.747 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise WebCenter Content: Imaging.  While the vulnerability is in WebCenter Content: Imaging, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all WebCenter Content: Imaging accessible data as well as  unauthorized update, insert or delete access to some of WebCenter Content: Imaging accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-60444

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:46.853 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-60426

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:45.017 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Unified Directory.  While the vulnerability is in Oracle Unified Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Unified Directory accessible data as well as  unauthorized update, insert or delete access to some of Oracle Unified Directory accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-60420

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:44.320 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Unified Directory.  While the vulnerability is in Oracle Unified Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Unified Directory accessible data as well as  unauthorized update, insert or delete access to some of Oracle Unified Directory accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-60330

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:36.033 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Identity Manager.  While the vulnerability is in Oracle Identity Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60295

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:32.050 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via TCP to compromise Oracle Coherence.  While the vulnerability is in Oracle Coherence, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60193

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:20.497 |

Vulnerability in the MySQL Connectors product of Oracle MySQL (component: Connector/Net).  Supported versions that are affected are 9.7.0-9.7.1. Difficult to exploit vulnerability allows low privileged attacker with network access via multiple protocols to compromise MySQL Connectors.  While the vulnerability is in MySQL Connectors, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of MySQL Connectors. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-47033

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:08.823 |

Vulnerability in the Oracle Contracts Integration product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Contracts Integration.  While the vulnerability is in Oracle Contracts Integration, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Contracts Integration. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-65592

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-22T12:18:19.253 |

n8n before 1.123.64, 2.29.8, and 2.30.1 contains a stored DOM cross-site scripting vulnerability in the Resource Locator component, which passes the workflow-persisted cachedResultUrl parameter to window.open() without scheme validation. An attacker with workflow creation/editing privileges can craft a workflow with a malicious (e.g., javascript:) scheme in cachedResultUrl; when a victim opens the crafted workflow and interacts with external links, the payload executes in the victim's browser.

### CVE-2026-56844

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-22T01:16:26.523 |

A vulnerability in the Veeam Updater component of the Veeam Software Appliance that could allow a local user to elevate their privileges and gain root-level access to the underlying operating system.

### CVE-2026-60837

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:21.647 |

Vulnerability in the Oracle Price Protection product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Price Protection executes to compromise Oracle Price Protection.  While the vulnerability is in Oracle Price Protection, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Price Protection accessible data as well as  unauthorized access to critical data or complete access to all Oracle Price Protection accessible data. CVSS 3.1 Base Score 8.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60763

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:15.720 |

Vulnerability in the Oracle Applications Manager product of Oracle E-Business Suite (component: Command Line - RapidClone).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Applications Manager executes to compromise Oracle Applications Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Applications Manager. CVSS 3.1 Base Score 8.4 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60723

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:12.363 |

Vulnerability in the Oracle Data Integrator product of Oracle Fusion Middleware (component: Market Place).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Data Integrator executes to compromise Oracle Data Integrator.  While the vulnerability is in Oracle Data Integrator, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Data Integrator accessible data as well as  unauthorized access to critical data or complete access to all Oracle Data Integrator accessible data. CVSS 3.1 Base Score 8.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60677

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:08.680 |

Vulnerability in the Oracle Common Application Components product of Oracle E-Business Suite (component: Oracle Common Modules).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Common Application Components.  While the vulnerability is in Oracle Common Application Components, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Common Application Components accessible data as well as  unauthorized access to critical data or complete access to all Oracle Common Application Components accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Common Application Components. CVSS 3.1 Base Score 8.4 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L).

### CVE-2026-60383

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:41.053 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Service Delivery Platform executes to compromise Service Delivery Platform.  While the vulnerability is in Service Delivery Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Service Delivery Platform accessible data as well as  unauthorized access to critical data or complete access to all Service Delivery Platform accessible data. CVSS 3.1 Base Score 8.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60196

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:20.840 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with access to the physical communication segment attached to the hardware where the Oracle WebLogic Server executes to compromise Oracle WebLogic Server.  While the vulnerability is in Oracle WebLogic Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 8.4 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60163

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:17.003 |

Vulnerability in the MySQL Server, MySQL Cluster product of Oracle MySQL (component: Server: Group Replication Plugin).  Supported versions that are affected are MySQL Server: 8.4.0-8.4.10, 9.7.0-9.7.1; MySQL Cluster: 8.0.0-8.0.47, 8.4.0-8.4.10 and  9.7.0-9.7.1. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where MySQL Server, MySQL Cluster executes to compromise MySQL Server, MySQL Cluster.  Successful attacks of this vulnerability can result in takeover of MySQL Server, MySQL Cluster. CVSS 3.1 Base Score 8.4 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-63358

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-07-21T21:16:53.193 |

FileGator accepts arbitrary Unix permission values via the '/chmoditems' API endpoint and passes the value directly to PHP's native 'chmod()' function through 'octdec()' conversion, with no validation. This allows an authenticated user with 'chmod' permission to upgrade their privileges to root.

### CVE-2026-65049

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-21T15:16:38.970 |

Ninja Forms plugin version 3.14.8 and prior for WordPress Multisite contains an incorrect authorization vulnerability that allows a subsite Administrator to trigger network-wide deletion of all Ninja Forms data by exploiting a site-scoped capability check combined with unsafe multisite migration defaults. Attackers can send a crafted POST request to the admin-ajax.php endpoint with the nf_delete_all_data action and a per-site nonce to invoke migration routines that unconditionally iterate all blogs via switch_to_blog(), dropping all nf3_* tables and clearing options and transients across every subsite in the network without requiring super-admin or network-admin privileges.

### CVE-2026-15226

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-250` |
| Published | 2026-07-21T15:16:31.030 |

A sandbox confinement bypass vulnerability exists in Canonical snapd within its internal execution environment compiler (snap-confine). The default seccomp security templates generated by the engine to restrict system calls do not filter or reject process operations capable of creating or manipulating file execution flags with set-user-ID attributes.  Consequently, an application running within a strictly confined snap environment can successfully compile or drop binaries and apply setuid properties to them. If a compromised or malicious process inside the snap sandbox executes these generated setuid binaries, it can potentially circumvent architectural sandboxing assumptions, drop intended restriction policies, or execute privileged actions inside the container namespace that should otherwise be strictly blocked. The vulnerability has been resolved by hardening the seccomp template engine to block the execution and creation of setuid executables by sandboxed snap processes.

### CVE-2026-56817

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-07-21T23:17:52.127 |

Netty is a network application framework for development of protocol servers and clients. In versions 4.2.0.Final through 4.2.15.Final and 4.1.0.Final through 4.1.135.Final, any caller that can deliver bytes to a Netty channel pipeline containing `XmlDecoder` can send XML with a `DOCTYPE` declaration to an `AsyncXMLInputFactory` instantiated with no security configuration, leaving DTD and entity handling active depending on Aalto XML async parser behavior and creating conditional XML external entity risk. This issue is fixed in versions 4.1.136.Final and 4.2.16.Final.

### CVE-2026-62473

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:03.677 |

Vulnerability in the Oracle Installed Base product of Oracle E-Business Suite (component: Create Item Instance).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Installed Base.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Installed Base accessible data as well as  unauthorized access to critical data or complete access to all Oracle Installed Base accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Installed Base. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-60788

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:17.847 |

Vulnerability in the Oracle Sales Offline product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales Offline.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Sales Offline accessible data as well as  unauthorized access to critical data or complete access to all Oracle Sales Offline accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Sales Offline. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-60640

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:04.750 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-60582

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:58.593 |

Vulnerability in the Oracle Enterprise Command Center Framework product of Oracle E-Business Suite (component: Core).   The supported version that is affected is V16. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Enterprise Command Center Framework.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Enterprise Command Center Framework accessible data as well as  unauthorized read access to a subset of Oracle Enterprise Command Center Framework accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Enterprise Command Center Framework. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H).

### CVE-2026-60471

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:49.640 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the WebCenter Content: Imaging executes to compromise WebCenter Content: Imaging.  While the vulnerability is in WebCenter Content: Imaging, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of WebCenter Content: Imaging. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-65056

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-21T21:16:54.287 |

mcp-webresearch 0.1.7 contains a server-side request forgery vulnerability that allows attackers to access internal network services by supplying loopback, link-local, or cloud metadata addresses to the visit_page tool, which only validates the URL protocol without filtering private or reserved IP ranges. Attackers can steer the LLM-controlled URL argument through prompt injection to navigate the server's Playwright browser to internal endpoints such as cloud instance metadata services, causing the server to return sensitive internal page content including credentials into the model context.

### CVE-2026-16317

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-354` |
| Published | 2026-07-21T21:16:49.060 |

Missing validation of the outer content_type byte on TLS 1.3 encrypted records in s2n-tls allows an active man-in-the-middle to silently discard individual application data records without either endpoint detecting the modification. RFC 8446 Section 5.2 requires that the outer content_type of all encrypted TLS 1.3 records must be application_data (0x17). The s2n-tls AEAD implementation hardcodes this value in the additional authenticated data rather than using the actual wire byte, so the outer content_type is not covered by the authentication tag. 



This enables selective suppression of application data. In HTTP pipelining scenarios, dropping a TLS record containing an HTTP request can cause request/response desynchronization, where subsequent responses are delivered to the wrong requests. In write-heavy workloads, a dropped record containing a write request can result in undetectable data loss when the client interprets a subsequent success response as confirmation of the dropped write.



All TLS 1.3 connections are affected. Both TLS clients and servers are affected. TLS 1.2 and QUIC connections are not affected.



We recommend you upgrade s2n-tls to version v1.7.6

### CVE-2026-47419

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-21T18:17:00.990 |

PraisonAI Platform is the platform layer for the PraisonAI multi-agent teams system. Versions prior to 0.1.4 have an* Insecure Direct Object Reference. The agent CRUD endpoints (`GET / PATCH / DELETE /workspaces/{workspace_id}/agents/{agent_id}`) gate access on `require_workspace_member(workspace_id)` only, then resolve `agent_id` through `AgentService.get(agent_id)` which is a primary-key lookup with no workspace constraint. A user who is a member of any workspace `W1` can read, modify, or delete agents that belong to a different workspace `W2` by guessing or harvesting an agent UUID and calling `…/workspaces/W1/agents/<W2-agent-id>`. PraisonAI Platform version 0.1.4 patches the issue.

### CVE-2026-47415

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-21T18:17:00.423 |

PraisonAI Platform is the platform layer for the PraisonAI multi-agent teams system. Versions prior to 0.1.4 have an Insecure Direct Object Reference. The issue CRUD endpoints (`GET / PATCH / DELETE /workspaces/{workspace_id}/issues/{issue_id}`) gate access on `require_workspace_member(workspace_id)` only, then resolve `issue_id` through `IssueService.get(issue_id)` which is a primary-key lookup with no workspace constraint. A user who is a member of any workspace `W1` can read, modify, or delete issues that belong to a different workspace `W2`. PraisonAI Platform version 0.1.4 patches the issue.

### CVE-2026-65597

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-22T12:18:19.913 |

n8n before 1.123.64, 2.x before 2.29.8, and before 2.30.1 contains a DOM-based cross-site scripting vulnerability in the HTML preview, which renders execution output into an iframe srcdoc without the sandbox attribute. A sanitizer bypass allows injected script to execute same-origin as the editor. When a victim opens the preview, the script can call authenticated APIs using the victim's session. An account with global:member privileges can exploit the issue.

### CVE-2026-62456

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:02.770 |

Vulnerability in the Oracle HRMS (UK) product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle HRMS (UK).  While the vulnerability is in Oracle HRMS (UK), attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle HRMS (UK) accessible data as well as  unauthorized access to critical data or complete access to all Oracle HRMS (UK) accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-61240

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:54.907 |

Vulnerability in the PeopleSoft Enterprise FIN Common Objects Argentina product of Oracle PeopleSoft (component: eSettlements).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the PeopleSoft Enterprise FIN Common Objects Argentina executes to compromise PeopleSoft Enterprise FIN Common Objects Argentina.  While the vulnerability is in PeopleSoft Enterprise FIN Common Objects Argentina, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise FIN Common Objects Argentina accessible data as well as  unauthorized update, insert or delete access to some of PeopleSoft Enterprise FIN Common Objects Argentina accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-61205

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:52.303 |

Vulnerability in the PeopleSoft Enterprise SCM Purchasing product of Oracle PeopleSoft (component: Purchasing).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise SCM Purchasing.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise SCM Purchasing accessible data as well as  unauthorized read access to a subset of PeopleSoft Enterprise SCM Purchasing accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N).

### CVE-2026-61101

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:41.247 |

Vulnerability in the Oracle MES for Process Manufacturing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle MES for Process Manufacturing.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle MES for Process Manufacturing, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle MES for Process Manufacturing accessible data as well as  unauthorized update, insert or delete access to some of Oracle MES for Process Manufacturing accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-61089

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:39.880 |

Vulnerability in the PeopleSoft Enterprise SCM Inventory product of Oracle PeopleSoft (component: Security).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise SCM Inventory.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise SCM Inventory accessible data as well as  unauthorized update, insert or delete access to some of PeopleSoft Enterprise SCM Inventory accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60854

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:22.877 |

Vulnerability in the Oracle Quality product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Quality.  While the vulnerability is in Oracle Quality, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Quality accessible data as well as  unauthorized update, insert or delete access to some of Oracle Quality accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Quality. CVSS 3.1 Base Score 8.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:L).

### CVE-2026-60810

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:19.443 |

Vulnerability in the Oracle Supply Chain Trading Connector product of Oracle E-Business Suite (component: Collaboration History).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Supply Chain Trading Connector.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Supply Chain Trading Connector accessible data as well as  unauthorized update, insert or delete access to some of Oracle Supply Chain Trading Connector accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60674

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:08.330 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Business Intelligence Enterprise Edition accessible data as well as  unauthorized update, insert or delete access to some of Oracle Business Intelligence Enterprise Edition accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60668

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:07.747 |

Vulnerability in the PeopleSoft Enterprise HCM Human Resources product of Oracle PeopleSoft (component: French Public Sector Specific).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise HCM Human Resources.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise HCM Human Resources accessible data as well as  unauthorized update, insert or delete access to some of PeopleSoft Enterprise HCM Human Resources accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60665

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:07.380 |

Vulnerability in the PeopleSoft Enterprise HCM Global Payroll Switzerland product of Oracle PeopleSoft (component: Global Payroll for Switzerland).   The supported version that is affected is 9.2. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise HCM Global Payroll Switzerland.  While the vulnerability is in PeopleSoft Enterprise HCM Global Payroll Switzerland, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise HCM Global Payroll Switzerland accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise HCM Global Payroll Switzerland accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60615

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:01.910 |

Vulnerability in the PeopleSoft Enterprise CS Campus Community product of Oracle PeopleSoft (component: Security).   The supported version that is affected is 9.2.38. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise CS Campus Community.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise CS Campus Community accessible data as well as  unauthorized update, insert or delete access to some of PeopleSoft Enterprise CS Campus Community accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60544

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:54.287 |

Vulnerability in the Oracle SOA Suite product of Oracle Fusion Middleware (component: B2B Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle SOA Suite.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle SOA Suite accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle SOA Suite. CVSS 3.1 Base Score 8.2 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-60525

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:52.177 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60428

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:45.247 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Unified Directory accessible data as well as  unauthorized update, insert or delete access to some of Oracle Unified Directory accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60421

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:44.443 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Unified Directory.  While the vulnerability is in Oracle Unified Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Unified Directory accessible data as well as  unauthorized access to critical data or complete access to all Oracle Unified Directory accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60315

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:34.283 |

Vulnerability in the MySQL Server, MySQL Cluster product of Oracle MySQL (component: Server: X Plugin).  Supported versions that are affected are MySQL Server: 8.4.0-8.4.10, 9.7.0-9.7.1; MySQL Cluster: 8.0.0-8.0.47, 8.4.0-8.4.10 and  9.7.0-9.7.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise MySQL Server, MySQL Cluster.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of MySQL Server, MySQL Cluster and  unauthorized read access to a subset of MySQL Server, MySQL Cluster accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H).

### CVE-2026-60284

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:30.833 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Coherence accessible data as well as  unauthorized update, insert or delete access to some of Oracle Coherence accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60255

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:27.480 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Coherence as well as  unauthorized update, insert or delete access to some of Oracle Coherence accessible data. CVSS 3.1 Base Score 8.2 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H).

### CVE-2026-47046

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:10.233 |

Vulnerability in the RDBMS component of Oracle Database Server.  Supported versions that are affected are 23.4.0-23.26.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via Oracle Net to compromise RDBMS.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of RDBMS as well as  unauthorized update, insert or delete access to some of RDBMS accessible data. CVSS 3.1 Base Score 8.2 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H).

### CVE-2026-46993

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:04.540 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Agent Next Gen).  Supported versions that are affected are 13.5 and  24.1. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  While the vulnerability is in Oracle Enterprise Manager Base Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Enterprise Manager Base Platform accessible data as well as  unauthorized access to critical data or complete access to all Oracle Enterprise Manager Base Platform accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-65054

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-21T21:16:54.020 |

MediaCMS 8.2.0 contains an information disclosure vulnerability that allows authenticated users to expose private media metadata belonging to other users by adding arbitrary media tokens to their own playlist without access control checks. Attackers can issue a PUT request to the playlist API endpoint with a known media token to bypass state and ownership validation, then retrieve the playlist to read private media fields including title, description, view count, like count, file size, author username, and encoding status through the unfiltered playlist owner branch in the playlist detail view.

### CVE-2026-47688

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-21T21:16:50.810 |

FOG is a free open-source cloning/imaging/rescue suite/inventory management system. Prior to versions 1.5.10.1832 and 1.6.0-beta.2313, the `clearAES` and `clearPMTasks` methods in `FOGPage` can be invoked by an unauthenticated attacker via a single HTTP GET request through the public `client` node endpoint. This allows remote wiping of host AES encryption credentials and deletion of all power management scheduled tasks, with no login, session, or CSRF token required. Versions 1.5.10.1832 and 1.6.0-beta.2313 fix the issue.

### CVE-2026-21579

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T18:16:57.487 |

This High severity Information Disclosure vulnerability was introduced in versions 7.17.0, 7.19.0, 8.5.0, 8.9.0, 9.0.1, 9.1.0, 9.2.0, 10.0.2, 10.1.0, and 10.2.0 of Confluence Data Center.

This Information Disclosure vulnerability, with a CVSS Score of 8.2, allows an unauthenticated attacker to view sensitive information via an Information Disclosure vulnerability.

Atlassian recommends that Confluence Data Center customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
 Confluence Data Center 9.2: Upgrade to a release greater than or equal to 9.2.22

 Confluence Data Center 10.2: Upgrade to a release greater than or equal to 10.2.14

See the release notes ([https://confluence.atlassian.com/doc/confluence-release-notes-327.html]). You can download the latest version of Confluence Data Center from the download center ([https://www.atlassian.com/software/confluence/download-archives]).

This vulnerability was reported via our Atlassian (Internal) program.

### CVE-2026-15432

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-208` |
| Published | 2026-07-21T17:17:04.563 |

When verifying a mac with a ChunkedMacVerification object, Tink compares the resulting tag with non constant time comparison. This potentially allows an attacker to use timinig information as a side channel in order to get information how many bytes of a given tag match the correct tag. This in turn could allow to find a correct tag bytewise.

### CVE-2026-13190

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-22T14:17:14.667 |

In Progress® Telerik® UI for AJAX prior to v2026.2.708, a deserialization vulnerability in the persistence utilities allows unsafe type instantiation from attacker-influenced persisted state, which can lead to remote code execution.

### CVE-2026-13187

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-07-22T14:17:14.300 |

In Progress® Telerik® UI for AJAX prior to v2026.2.708, DialogHandler provider type input may be tampered with, potentially altering dialog processing and enabling chained exploitation.

### CVE-2026-13186

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-22T14:17:14.180 |

In Progress® Telerik® UI for AJAX prior to v2026.2.708, a path traversal vulnerability in the file-based persistence storage provider can be exploited when the storage key is derived from user-controlled input, enabling attacker-controlled deserialization and remote code execution.

### CVE-2026-13185

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-22T14:17:14.057 |

In Progress® Telerik® UI for AJAX prior to v2026.2.708, applications using cookie-based storage in RadPersistenceManager or RadDockLayout deserialize attacker-controlled cookie content, allowing unauthenticated remote code execution.

### CVE-2026-13181

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-07-22T14:17:13.553 |

In Progress® Telerik® UI for AJAX prior to v2026.2.708, forged upload metadata can influence AsyncUploadTypeName processing and trigger unsafe attacker-controlled type resolution, enabling remote code execution in affected deployments.

### CVE-2026-4773

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-1287` |
| Published | 2026-07-22T12:18:12.587 |

Improper validation of specified type of input vulnerability in Magarsus Consulting Ltd. Co. IDM-MFA allows Authentication Bypass.

This issue affects IDM-MFA: from 2025.11.27 before 2026.03.10.

### CVE-2026-15802

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-07-22T05:17:08.820 |

The WP Foodbakery plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the 'delete_locations_backup_file_callback' function in all versions up to, and including, 4.9. This makes it possible for authenticated attackers, with subscriber-level access and above, to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php).

### CVE-2026-62547

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-07-21T22:19:08.323 |

Vulnerability in the Oracle Workflow product of Oracle E-Business Suite (component: Workflow Notification Mailer).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via SMTP to compromise Oracle Workflow.  Successful attacks of this vulnerability can result in takeover of Oracle Workflow. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62530

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-21T22:19:07.877 |

Vulnerability in the Oracle HRMS (France) product of Oracle E-Business Suite (component: French HR).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle HRMS (France).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle HRMS (France) accessible data as well as  unauthorized access to critical data or complete access to all Oracle HRMS (France) accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62514

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:06.610 |

Vulnerability in the Oracle Process Manufacturing Regulatory Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Regulatory Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Process Manufacturing Regulatory Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Process Manufacturing Regulatory Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62504

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:06.047 |

Vulnerability in the Oracle Time and Labor product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Time and Labor.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Time and Labor accessible data as well as  unauthorized access to critical data or complete access to all Oracle Time and Labor accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62497

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:05.720 |

Vulnerability in the Oracle Flow Manufacturing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.13-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Flow Manufacturing.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Flow Manufacturing accessible data as well as  unauthorized access to critical data or complete access to all Oracle Flow Manufacturing accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62494

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:05.387 |

Vulnerability in the Oracle Time and Labor product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Time and Labor.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Time and Labor accessible data as well as  unauthorized access to critical data or complete access to all Oracle Time and Labor accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62472

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:03.557 |

Vulnerability in the Oracle Installed Base product of Oracle E-Business Suite (component: Create Item Instance).  Supported versions that are affected are 12.2.4-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Installed Base.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Installed Base accessible data as well as  unauthorized access to critical data or complete access to all Oracle Installed Base accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62468

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:03.213 |

Vulnerability in the Oracle Human Resources product of Oracle E-Business Suite (component: Enterprise Command Center).  Supported versions that are affected are 12.2.14-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Human Resources.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Human Resources accessible data as well as  unauthorized access to critical data or complete access to all Oracle Human Resources accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62451

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:02.507 |

Vulnerability in the Oracle Work in Process product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.14-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Work in Process.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Work in Process accessible data as well as  unauthorized access to critical data or complete access to all Oracle Work in Process accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62445

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:02.280 |

Vulnerability in the Oracle Order Management product of Oracle E-Business Suite (component: Product Diagnostic Tools).  Supported versions that are affected are 12.2.4-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Order Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Order Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Order Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61338

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:01.930 |

Vulnerability in the Oracle Contracts Integration product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Contracts Integration.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Contracts Integration accessible data as well as  unauthorized access to critical data or complete access to all Oracle Contracts Integration accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61335

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:01.583 |

Vulnerability in the Oracle Product Workbench product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Workbench.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Product Workbench accessible data as well as  unauthorized access to critical data or complete access to all Oracle Product Workbench accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61333

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:01.353 |

Vulnerability in the Oracle Product Workbench product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Workbench.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Product Workbench accessible data as well as  unauthorized access to critical data or complete access to all Oracle Product Workbench accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61329

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:01.240 |

Vulnerability in the Oracle Price Protection product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Price Protection.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Price Protection accessible data as well as  unauthorized access to critical data or complete access to all Oracle Price Protection accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61327

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:01.010 |

Vulnerability in the Oracle Bills of Material product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.13-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Bills of Material.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Bills of Material accessible data as well as  unauthorized access to critical data or complete access to all Oracle Bills of Material accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61310

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:59.760 |

Vulnerability in the Oracle Product Hub product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Hub.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Product Hub accessible data as well as  unauthorized access to critical data or complete access to all Oracle Product Hub accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61301

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:59.317 |

Vulnerability in the Oracle Process Manufacturing Financials product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Financials.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Process Manufacturing Financials accessible data as well as  unauthorized access to critical data or complete access to all Oracle Process Manufacturing Financials accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61297

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:59.090 |

Vulnerability in the Oracle Customers Online product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Customers Online.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Customers Online accessible data as well as  unauthorized access to critical data or complete access to all Oracle Customers Online accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61287

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:58.640 |

Vulnerability in the Oracle Process Manufacturing Systems product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Systems.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Process Manufacturing Systems accessible data as well as  unauthorized access to critical data or complete access to all Oracle Process Manufacturing Systems accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61225

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:53.800 |

Vulnerability in the Oracle Communications Converged Application Server product of Oracle Communications (component: Core).  Supported versions that are affected are 8.2 and  8.3. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TCP/IP to compromise Oracle Communications Converged Application Server.  Successful attacks of this vulnerability can result in takeover of Oracle Communications Converged Application Server. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61218

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:53.240 |

Vulnerability in the Oracle E-Business Suite Secure Enterprise Search product of Oracle E-Business Suite (component: Search Integration Engine).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle E-Business Suite Secure Enterprise Search.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle E-Business Suite Secure Enterprise Search accessible data as well as  unauthorized access to critical data or complete access to all Oracle E-Business Suite Secure Enterprise Search accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61170

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:48.700 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Security).   The supported version that is affected is 9.3.6. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks of this vulnerability can result in takeover of Oracle Agile PLM. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61163

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:47.910 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61160

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:47.573 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 8.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H).

### CVE-2026-61150

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:46.430 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61137

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:45.070 |

Vulnerability in the Oracle Commerce Platform product of Oracle Commerce (component: Dynamo Application Framework).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Platform. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61122

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:43.487 |

Vulnerability in the Oracle HRMS (UK) product of Oracle E-Business Suite (component: UK Payroll).  Supported versions that are affected are 12.2.9-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle HRMS (UK).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle HRMS (UK) accessible data as well as  unauthorized access to critical data or complete access to all Oracle HRMS (UK) accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61106

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:41.793 |

Vulnerability in Oracle GoldenGate (component: Config Service Executable).  Supported versions that are affected are 23.4-23.26.2. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle GoldenGate.  Successful attacks of this vulnerability can result in takeover of Oracle GoldenGate. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61105

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:41.690 |

Vulnerability in the Oracle Banking Trade Finance product of Oracle Financial Services Applications (component: Infrastructure).  Supported versions that are affected are 14.6.0-14.8.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Banking Trade Finance.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Banking Trade Finance accessible data as well as  unauthorized access to critical data or complete access to all Oracle Banking Trade Finance accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61102

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:41.360 |

Vulnerability in the Oracle Banking Trade Finance product of Oracle Financial Services Applications (component: Infrastructure).  Supported versions that are affected are 14.6.0-14.8.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Banking Trade Finance.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Banking Trade Finance accessible data as well as  unauthorized access to critical data or complete access to all Oracle Banking Trade Finance accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61092

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:40.220 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61074

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:38.193 |

Vulnerability in the PeopleSoft Enterprise FIN Common Objects Brazil product of Oracle PeopleSoft (component: eProcurement).   The supported version that is affected is 9.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Common Objects Brazil.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise FIN Common Objects Brazil. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61037

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:34.827 |

Vulnerability in the Oracle Loans product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Loans.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Loans accessible data as well as  unauthorized access to critical data or complete access to all Oracle Loans accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61031

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:34.490 |

Vulnerability in the Oracle Financials Common Country product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Financials Common Country.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Financials Common Country accessible data as well as  unauthorized access to critical data or complete access to all Oracle Financials Common Country accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61030

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:34.370 |

Vulnerability in the Oracle Process Manufacturing Product Development product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Product Development.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Process Manufacturing Product Development accessible data as well as  unauthorized access to critical data or complete access to all Oracle Process Manufacturing Product Development accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61024

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:33.807 |

Vulnerability in the Oracle iRecruitment product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iRecruitment.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle iRecruitment accessible data as well as  unauthorized access to critical data or complete access to all Oracle iRecruitment accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61020

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:33.573 |

Vulnerability in the Oracle Customers Online product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Customers Online.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Customers Online accessible data as well as  unauthorized access to critical data or complete access to all Oracle Customers Online accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61019

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:33.467 |

Vulnerability in the Oracle Customers Online product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Customers Online.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Customers Online accessible data as well as  unauthorized access to critical data or complete access to all Oracle Customers Online accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61005

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:32.570 |

Vulnerability in the Oracle Process Manufacturing Logistics product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Logistics.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Process Manufacturing Logistics accessible data as well as  unauthorized access to critical data or complete access to all Oracle Process Manufacturing Logistics accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61004

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:32.460 |

Vulnerability in the Oracle Landed Cost Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Landed Cost Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Landed Cost Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Landed Cost Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61000

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:32.350 |

Vulnerability in the Oracle Process Manufacturing Systems product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Systems.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Process Manufacturing Systems accessible data as well as  unauthorized access to critical data or complete access to all Oracle Process Manufacturing Systems accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60997

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:32.130 |

Vulnerability in the Oracle Universal Work Queue product of Oracle E-Business Suite (component: Non-Media Integration issues).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Universal Work Queue.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Universal Work Queue accessible data as well as  unauthorized access to critical data or complete access to all Oracle Universal Work Queue accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60986

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:31.660 |

Vulnerability in the Oracle Project Portfolio Analysis product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Project Portfolio Analysis.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Project Portfolio Analysis accessible data as well as  unauthorized access to critical data or complete access to all Oracle Project Portfolio Analysis accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60982

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:31.330 |

Vulnerability in the Oracle US Federal Human Resources product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle US Federal Human Resources.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle US Federal Human Resources accessible data as well as  unauthorized access to critical data or complete access to all Oracle US Federal Human Resources accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60979

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:31.217 |

Vulnerability in the Oracle Scripting product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Scripting.  Successful attacks of this vulnerability can result in takeover of Oracle Scripting. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60974

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:31.000 |

Vulnerability in the Oracle E-Business Tax product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle E-Business Tax.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle E-Business Tax accessible data as well as  unauthorized access to critical data or complete access to all Oracle E-Business Tax accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60972

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:30.777 |

Vulnerability in the Oracle E-Business Tax product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle E-Business Tax.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle E-Business Tax accessible data as well as  unauthorized access to critical data or complete access to all Oracle E-Business Tax accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60966

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:30.673 |

Vulnerability in the Oracle Public Sector Human Resources product of Oracle E-Business Suite (component: Regression Testing).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Public Sector Human Resources.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Public Sector Human Resources accessible data as well as  unauthorized access to critical data or complete access to all Oracle Public Sector Human Resources accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60965

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:30.567 |

Vulnerability in the Oracle HRMS (France) product of Oracle E-Business Suite (component: French HR).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle HRMS (France).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle HRMS (France) accessible data as well as  unauthorized access to critical data or complete access to all Oracle HRMS (France) accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60963

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:30.453 |

Vulnerability in the Oracle Treasury product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Treasury.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Treasury accessible data as well as  unauthorized access to critical data or complete access to all Oracle Treasury accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60959

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:30.117 |

Vulnerability in the Oracle SDP Number Portability product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle SDP Number Portability.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle SDP Number Portability accessible data as well as  unauthorized access to critical data or complete access to all Oracle SDP Number Portability accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60953

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:29.880 |

Vulnerability in the Oracle Telecommunications Billing Integrator product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Telecommunications Billing Integrator.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Telecommunications Billing Integrator accessible data as well as  unauthorized access to critical data or complete access to all Oracle Telecommunications Billing Integrator accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60951

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:29.600 |

Vulnerability in the Oracle Time and Labor product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Time and Labor.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Time and Labor accessible data as well as  unauthorized access to critical data or complete access to all Oracle Time and Labor accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60948

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:29.380 |

Vulnerability in the Oracle Learning Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Learning Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Learning Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Learning Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60942

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:29.027 |

Vulnerability in the Oracle Service Fulfillment Manager product of Oracle E-Business Suite (component: Fulfillment Engine).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Service Fulfillment Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Service Fulfillment Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Service Fulfillment Manager accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60917

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:26.817 |

Vulnerability in the Oracle Inventory Management product of Oracle E-Business Suite (component: Core Receiving).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Inventory Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Inventory Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Inventory Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60904

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:26.020 |

Vulnerability in the Oracle Installed Base product of Oracle E-Business Suite (component: Create Item Instance).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Installed Base.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Installed Base accessible data as well as  unauthorized access to critical data or complete access to all Oracle Installed Base accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60877

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:24.353 |

Vulnerability in the Oracle Trade Management product of Oracle E-Business Suite (component: Claim LOV).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Trade Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Trade Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Trade Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60875

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:24.243 |

Vulnerability in the Oracle Trade Management product of Oracle E-Business Suite (component: Claim LOV).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Trade Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Trade Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Trade Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60871

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:24.020 |

Vulnerability in the Oracle Risk Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Risk Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Risk Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Risk Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60867

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:23.677 |

Vulnerability in the Oracle Advanced Pricing product of Oracle E-Business Suite (component: Pricing Installation).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Advanced Pricing.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Advanced Pricing accessible data as well as  unauthorized access to critical data or complete access to all Oracle Advanced Pricing accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60857

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:23.107 |

Vulnerability in the Oracle Contracts Integration product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Contracts Integration.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Contracts Integration accessible data as well as  unauthorized access to critical data or complete access to all Oracle Contracts Integration accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60852

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:22.770 |

Vulnerability in the Oracle Lease and Finance Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Lease and Finance Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Lease and Finance Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Lease and Finance Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60848

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:22.647 |

Vulnerability in the Oracle Project Contracts product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Project Contracts.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Project Contracts accessible data as well as  unauthorized access to critical data or complete access to all Oracle Project Contracts accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60844

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:22.200 |

Vulnerability in the Oracle Customer Support product of Oracle E-Business Suite (component: Update Service Request).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Customer Support.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Customer Support accessible data as well as  unauthorized access to critical data or complete access to all Oracle Customer Support accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60840

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:21.867 |

Vulnerability in the Oracle Demand Signal Repository product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via SQL to compromise Oracle Demand Signal Repository.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Demand Signal Repository accessible data as well as  unauthorized access to critical data or complete access to all Oracle Demand Signal Repository accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60817

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:20.113 |

Vulnerability in the Oracle iStore product of Oracle E-Business Suite (component: Shopping Cart).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iStore.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle iStore accessible data as well as  unauthorized access to critical data or complete access to all Oracle iStore accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60793

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:18.187 |

Vulnerability in the Oracle TeleSales product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle TeleSales.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle TeleSales accessible data as well as  unauthorized access to critical data or complete access to all Oracle TeleSales accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60785

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:17.500 |

Vulnerability in the Oracle iReceivables product of Oracle E-Business Suite (component: AR Web Utilities).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle iReceivables.  Successful attacks of this vulnerability can result in takeover of Oracle iReceivables. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60784

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:17.383 |

Vulnerability in the Oracle Trading Community product of Oracle E-Business Suite (component: Party Search UI).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Trading Community.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Trading Community accessible data as well as  unauthorized access to critical data or complete access to all Oracle Trading Community accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60780

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:17.150 |

Vulnerability in the Oracle Workflow product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via SMTP to compromise Oracle Workflow.  Successful attacks of this vulnerability can result in takeover of Oracle Workflow. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60778

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:17.030 |

Vulnerability in the Oracle Payments product of Oracle E-Business Suite (component: File Transmission).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Payments.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Payments accessible data as well as  unauthorized access to critical data or complete access to all Oracle Payments accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60771

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:16.183 |

Vulnerability in the Oracle Complex Maintenance, Repair and Overhaul product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Complex Maintenance, Repair and Overhaul.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Complex Maintenance, Repair and Overhaul accessible data as well as  unauthorized access to critical data or complete access to all Oracle Complex Maintenance, Repair and Overhaul accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60768

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:15.957 |

Vulnerability in the Oracle Applications Framework product of Oracle E-Business Suite (component: Graph / Charting).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Applications Framework.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Applications Framework accessible data as well as  unauthorized access to critical data or complete access to all Oracle Applications Framework accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60764

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:15.840 |

Vulnerability in the Oracle Financials Common Modules product of Oracle E-Business Suite (component: Common Components).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Financials Common Modules.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Financials Common Modules accessible data as well as  unauthorized access to critical data or complete access to all Oracle Financials Common Modules accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60756

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:15.263 |

Vulnerability in the Oracle EDI Gateway product of Oracle E-Business Suite (component: All Miscellaneous EDI Issues).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle EDI Gateway.  Successful attacks of this vulnerability can result in takeover of Oracle EDI Gateway. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60749

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:14.917 |

Vulnerability in the Oracle Assets product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Assets.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Assets accessible data as well as  unauthorized access to critical data or complete access to all Oracle Assets accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60741

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:14.577 |

Vulnerability in the Oracle Cost Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Cost Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Cost Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Cost Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60740

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:14.460 |

Vulnerability in the Oracle Cash Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Cash Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Cash Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Cash Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60736

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:14.103 |

Vulnerability in the Oracle E-Business Intelligence product of Oracle E-Business Suite (component: Definition).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle E-Business Intelligence.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle E-Business Intelligence accessible data as well as  unauthorized access to critical data or complete access to all Oracle E-Business Intelligence accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60735

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:13.987 |

Vulnerability in the Oracle Sales Offline product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales Offline.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Sales Offline accessible data as well as  unauthorized access to critical data or complete access to all Oracle Sales Offline accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60732

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:13.587 |

Vulnerability in the Oracle iReceivables product of Oracle E-Business Suite (component: AR Web Utilities).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iReceivables.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle iReceivables accessible data as well as  unauthorized access to critical data or complete access to all Oracle iReceivables accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60714

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:11.903 |

Vulnerability in the Oracle Price Protection product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Price Protection.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Price Protection accessible data as well as  unauthorized access to critical data or complete access to all Oracle Price Protection accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60710

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:11.440 |

Vulnerability in the Oracle EDI Gateway product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle EDI Gateway.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle EDI Gateway accessible data as well as  unauthorized access to critical data or complete access to all Oracle EDI Gateway accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60708

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:11.210 |

Vulnerability in the Oracle Process Manufacturing Financials product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Financials.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Process Manufacturing Financials accessible data as well as  unauthorized access to critical data or complete access to all Oracle Process Manufacturing Financials accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60706

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:11.053 |

Vulnerability in the Oracle Process Manufacturing Inventory product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Inventory.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Process Manufacturing Inventory accessible data as well as  unauthorized access to critical data or complete access to all Oracle Process Manufacturing Inventory accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60700

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:10.483 |

Vulnerability in the Oracle Universal Work Queue product of Oracle E-Business Suite (component: UWQ Server Issues).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Universal Work Queue.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Universal Work Queue accessible data as well as  unauthorized access to critical data or complete access to all Oracle Universal Work Queue accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N).

### CVE-2026-60691

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:09.923 |

Vulnerability in the Oracle Content Manager product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Content Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Content Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Content Manager accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60686

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:09.360 |

Vulnerability in the Oracle U.S. Federal Financials product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle U.S. Federal Financials.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle U.S. Federal Financials accessible data as well as  unauthorized access to critical data or complete access to all Oracle U.S. Federal Financials accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60670

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:07.980 |

Vulnerability in the Oracle Applications Technology Stack product of Oracle E-Business Suite (component: Client System Analyzer).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Applications Technology Stack.  Successful attacks of this vulnerability can result in takeover of Oracle Applications Technology Stack. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60653

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:06.253 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Web Content Management).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60621

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:02.593 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Web Runtime Security).   The supported version that is affected is 9.2.26.3. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Tools.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Tools. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60599

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:00.070 |

Vulnerability in the PeopleSoft Enterprise CS Student Records product of Oracle PeopleSoft (component: Research Tracking).   The supported version that is affected is 9.2.38. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise PeopleSoft Enterprise CS Student Records.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise CS Student Records accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise CS Student Records accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60560

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:56.110 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: REST WebServices).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Identity Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Identity Manager accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60558

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:55.887 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60543

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:54.173 |

Vulnerability in the Oracle SOA Suite product of Oracle Fusion Middleware (component: B2B Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle SOA Suite.  Successful attacks of this vulnerability can result in takeover of Oracle SOA Suite. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60520

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:51.603 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Unified Directory accessible data as well as  unauthorized access to critical data or complete access to all Oracle Unified Directory accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60462

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:48.640 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60450

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:47.523 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60417

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:43.980 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Unified Directory. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60416

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:43.860 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60323

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:35.250 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Identity Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Identity Manager accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60312

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:33.950 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60281

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:30.490 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Coherence executes to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Coherence accessible data as well as  unauthorized access to critical data or complete access to all Oracle Coherence accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60277

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:30.050 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60273

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:29.573 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60222

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:23.777 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60201

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:21.410 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60192

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:20.383 |

Vulnerability in the MySQL Connectors product of Oracle MySQL (component: Connector/Net).  Supported versions that are affected are 9.7.0-9.7.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise MySQL Connectors.  Successful attacks of this vulnerability can result in takeover of MySQL Connectors. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60169

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:17.703 |

Vulnerability in the Oracle Hospitality Simphony product of Oracle Food and Beverage Applications (component: POS).  Supported versions that are affected are 19.8-19.8.5, 19.9-19.9.3 and  19.10. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hospitality Simphony.  Successful attacks of this vulnerability can result in takeover of Oracle Hospitality Simphony. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-47028

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:08.360 |

Vulnerability in the Oracle Document Management and Collaboration product of Oracle E-Business Suite (component: Attachments).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Document Management and Collaboration.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Document Management and Collaboration accessible data as well as  unauthorized access to critical data or complete access to all Oracle Document Management and Collaboration accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-47019

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:07.567 |

Vulnerability in the Oracle Product Hub product of Oracle E-Business Suite (component: Item Catalog).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Hub.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Product Hub accessible data as well as  unauthorized access to critical data or complete access to all Oracle Product Hub accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-47014

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:06.977 |

Vulnerability in the Oracle Product Workbench product of Oracle E-Business Suite (component: Security).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Workbench.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Product Workbench accessible data as well as  unauthorized access to critical data or complete access to all Oracle Product Workbench accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-10678

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-476;CWE-787` |
| Published | 2026-07-21T22:17:00.047 |

The MCTP-over-I2C+GPIO target binding in Zephyr (subsys/pmci/mctp/mctp_i2c_gpio_target.c) processes pseudo-register writes from an I2C bus master byte-by-byte in mctp_i2c_gpio_target_write_received() without validating the order or the receive buffer. In the affected versions the MCTP_I2C_GPIO_RX_MSG_ADDR (data) handler dereferences and writes through b->rx_pkt without checking that the receive buffer was allocated: a controller that selects the data register and writes a byte without first sending the length register (which is what allocates the buffer) causes a write of an attacker-chosen byte through a NULL/unallocated mctp_pktbuf pointer (i.e. into a small attacker-advanceable offset above address 0), producing memory corruption or a hard fault.

The same handler also performs a write-then-check bounds test, allowing a one-byte heap overflow at data[255] when more than 255 data bytes are sent.

Because the I2C target callback is invoked with raw bytes supplied by whatever device is the bus master and the binding performs no authentication, a malicious or malfunctioning controller on the bus can trigger these without any prior protocol state, leading to memory corruption and/or denial of service on the target device.

The vulnerable code was introduced when the I2C+GPIO target binding was added and shipped in Zephyr v4.3.0 and v4.4.0. The fix defers allocation to the first data byte with a NULL check, treats a missing length as a zero-sized packet rejected by libmctp, and moves the bounds check before the store.

### CVE-2026-47418

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-21T18:17:00.853 |

PraisonAI Platform is the platform layer for the PraisonAI multi-agent teams system. Versions prior to 0.1.4 have an Insecure Direct Object Reference. The project CRUD endpoints (`GET / PATCH / DELETE /workspaces/{workspace_id}/projects/{project_id}` and `GET .../{project_id}/stats`) gate access on `require_workspace_member(workspace_id)` only, then resolve `project_id` through `ProjectService.get(project_id)` / `update(project_id, ...)` / `delete(project_id)` / `get_stats(project_id)`. None of these calls thread `workspace_id` through to constrain the lookup. A user who is a member of any workspace `W1` can read, modify, delete, or read stats for projects that belong to a different workspace `W2`. PraisonAI Platform version 0.1.4 patches the issue.

### CVE-2026-47417

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-21T18:17:00.707 |

PraisonAI Platform is the platform layer for the PraisonAI multi-agent teams system. Versions prior to 0.1.4 have an Insecure Direct Object Reference. The comment endpoints (`POST /workspaces/{workspace_id}/issues/{issue_id}/comments` and `GET .../comments`) gate access on `require_workspace_member(workspace_id)` only, then call `CommentService.create(issue_id=issue_id, ...)` and `CommentService.list_for_issue(issue_id)` without verifying that `issue_id` belongs to `workspace_id`. A user who is a member of any workspace `W1` can read every comment on, and post new comments to, any issue in any other workspace `W2`. PraisonAI Platform version 0.1.4 patches the issue.

### CVE-2026-47412

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-862` |
| Published | 2026-07-21T18:16:59.980 |

PraisonAI Platform is the platform layer for the PraisonAI multi-agent teams system. Versions prior to 0.1.4 have an authorization bypass enabling destructive action. The `DELETE /workspaces/{workspace_id}` endpoint is gated only by `require_workspace_member(workspace_id)` (default `min_role="member"`). Any member of the workspace can issue a single DELETE to wipe the entire workspace, including every project, issue, comment, agent, label, and member record (cascading via the foreign-key relationships). There is no owner-role gate, no confirmation token, no soft-delete window, no recovery path. PraisonAI Platform version 0.1.4 patches the issue.

### CVE-2026-47409

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-862` |
| Published | 2026-07-21T17:17:09.640 |

PraisonAI Platform is the platform layer for the PraisonAI multi-agent teams system. Versions prior to 0.1.4 have an authorization bypass enabling owner lockout. The `DELETE /workspaces/{workspace_id}/members/{user_id}` endpoint is gated only by `require_workspace_member(workspace_id)` (default `min_role="member"`). Any member can remove any other member, including the workspace owner, using a single DELETE. There is no caller-role check, no target-role check, no "cannot remove last owner" guard. PraisonAI Platform version 0.1.4 patches the issue.

### CVE-2026-47406

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-21T17:17:09.220 |

PraisonAI Platform is the platform layer for the PraisonAI multi-agent teams system. Versions prior to 0.1.4 have an Insecure Direct Object Reference. The dependency endpoints (`POST/GET /workspaces/{workspace_id}/issues/{issue_id}/dependencies` and `DELETE .../dependencies/{dep_id}`) gate access on `require_workspace_member(workspace_id)` only, then dispatch to `DependencyService` calls that take URL/body-supplied issue and dependency IDs without verifying any of them belong to the membership-checked workspace. Most damaging: `create_dependency` accepts `body.depends_on_issue_id` from the request body — that ID is checked against nothing — letting an attacker create a "blocks" or "related" link between any two issues anywhere in the database. PraisonAI Platform version 0.1.4 patches the issue.

### CVE-2026-47398

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-829` |
| Published | 2026-07-21T17:17:08.803 |

PraisonAI is a multi-agent teams system. The v4.6.32 chokepoint refactor (which patched CVE-2026-44334 / GHSA-xcmw-grxf-wjhj) added the PRAISONAI_ALLOW_LOCAL_TOOLS env-var gate to the tool_override.py sinks. However, two additional spec.loader.exec_module call sites in praisonai/agents_generator.py were missed and remain completely unguarded in versions prior to 4.6.40. Both functions accept a module_path parameter sourced from YAML configuration and execute it without validation, signature checking, or the env-var gate. Version 4.6.40 fixes the issue.

### CVE-2026-61224

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:53.687 |

Vulnerability in the Oracle Communications Converged Application Server product of Oracle Communications (component: Security).   The supported version that is affected is 8.3. Difficult to exploit vulnerability allows high privileged attacker with network access via TLS to compromise Oracle Communications Converged Application Server.  While the vulnerability is in Oracle Communications Converged Application Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Communications Converged Application Server. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61067

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:37.423 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with access to the physical communication segment attached to the hardware where the Oracle Access Manager executes to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61009

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:32.803 |

Vulnerability in the Oracle Process Manufacturing Logistics product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Logistics.  While the vulnerability is in Oracle Process Manufacturing Logistics, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Process Manufacturing Logistics. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60807

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:19.330 |

Vulnerability in the Oracle Bills of Material product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Bills of Material.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Bills of Material. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60790

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:18.070 |

Vulnerability in the Oracle Sales Offline product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Sales Offline.  While the vulnerability is in Oracle Sales Offline, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Sales Offline. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60652

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:06.137 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Web Content Management).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60650

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:05.870 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Web Content Management).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60648

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:05.643 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Web Content Management).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60646

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:05.417 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Web Content Management).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60643

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:05.083 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60579

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:58.253 |

Vulnerability in the Oracle Enterprise Command Center Framework product of Oracle E-Business Suite (component: Core).   The supported version that is affected is V16. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Enterprise Command Center Framework executes to compromise Oracle Enterprise Command Center Framework.  While the vulnerability is in Oracle Enterprise Command Center Framework, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Enterprise Command Center Framework accessible data as well as  unauthorized access to critical data or complete access to all Oracle Enterprise Command Center Framework accessible data. CVSS 3.1 Base Score 8.0 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60533

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:53.053 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Generic Unix Connector).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Identity Manager Connector executes to compromise Oracle Identity Manager Connector.  While the vulnerability is in Oracle Identity Manager Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Identity Manager Connector accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Identity Manager Connector. CVSS 3.1 Base Score 8.0 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:H).

### CVE-2026-60325

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:35.480 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with access to the physical communication segment attached to the hardware where the Oracle Access Manager executes to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46923

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:01.930 |

Vulnerability in the Oracle Public Sector Financials (International) product of Oracle E-Business Suite (component: Authorization).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Public Sector Financials (International).  While the vulnerability is in Oracle Public Sector Financials (International), attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Public Sector Financials (International). CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-47237

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-07-21T21:16:50.403 |

Kubeflow Community Distribution helps users to install Kubeflow Platform in popular Kubernetes clusters. Prior to version 26.03-rc.1, a Kubeflow setup based on the official manifests or most other packaged Kubeflow distributions is vulnerable to authorization token stealing from any user of the Kubeflow UI or APIs, such as the Dashboard, Pipelines API, or Notebooks. With this token, the attacker can take over the user's account and the data that is processed by that user. The attacker needs a valid user with the ``kubeflow-edit`` role / Contributor role in a random Kubeflow namespace to perform this attack. This is given if _Automatic Profile Creation_ is enabled. Version 26.03-rc.1 fixes the issue.

### CVE-2026-44191

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-22T13:16:37.367 |

A flaw was found in the Visual Studio Code Ansible Lightspeed extension. This command injection vulnerability (CWE-78) arises from improper handling of the ansible.executionEnvironment.containerOptions and ansible.executionEnvironment.volumeMounts settings, allowing an attacker to inject shell separators. This can be triggered automatically during Language Server initialization or manually when executing a playbook. Successful exploitation leads to remote code execution (RCE) on the victim's machine with the privileges of the Visual Studio Code user, potentially resulting in a complete system compromise.

### CVE-2026-65600

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-22T12:18:20.297 |

Traefik versions <= v2.11.51, >= v3.6.0 <= v3.6.22, and >= v3.7.0 <= v3.7.6 contain an authentication bypass via path traversal in the ReplacePathRegex middleware. When ReplacePathRegex is configured with a regex that captures user-controlled path segments without a mandatory path separator (e.g. regex "^/api(.*)", replacement "/$1"), the middleware forwards the replaced path to the backend without validating that it matches its normalized form. An unauthenticated remote attacker can send a crafted request (e.g. GET /api../admin) that produces an un-normalized path such as /../admin, which a backend that normalizes paths resolves to a protected route, bypassing authentication middleware. Fixed in v2.11.52, v3.6.23, and v3.7.7.

### CVE-2026-44190

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-22T12:17:59.940 |

A flaw was found in the Ansible Lightspeed Visual Studio Code extension. This Command Injection vulnerability (CWE-78) allows a remote attacker to execute unauthorized commands on a user's system. The issue occurs because the `ansible.python.activationScript` setting, intended for a virtual environment activation script, does not properly validate user input as a file path. If a user opens or executes a specially crafted project, an attacker could exploit this to gain complete control over the user's system with the privileges of the Visual Studio Code application.

### CVE-2026-44189

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-07-22T12:17:59.817 |

A flaw was found in the Visual Studio Code Ansible Lightspeed extension's AnsiblePlaybookRunProvider. This command injection vulnerability allows an attacker to craft a malicious playbook filename containing special characters. When a victim runs the playbook, these characters are not properly sanitized, leading to the execution of arbitrary code with the privileges of the user running VS Code. This could result in a full system compromise, including the exfiltration of sensitive data, modification of project files, and permanent data loss.

### CVE-2026-62574

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-21T22:19:09.667 |

Vulnerability in the Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition product of Oracle Java SE (component: Install).  Supported versions that are affected are Oracle Java SE: 8u491, 11.0.31, 17.0.19, 21.0.11, 25.0.3, 26.0.1; Oracle GraalVM for JDK: 17.0.19 and  21.0.11; Oracle GraalVM Enterprise Edition: 21.3.18. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition executes to compromise Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62561

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-21T22:19:09.103 |

Vulnerability in the Oracle HRMS (US) product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle HRMS (US) executes to compromise Oracle HRMS (US).  Successful attacks of this vulnerability can result in takeover of Oracle HRMS (US). CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61126

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:43.827 |

Vulnerability in the Oracle Communications Billing and Revenue Management product of Oracle Communications (component: Platform).  Supported versions that are affected are 15.0.0.0.0-15.0.1.0.0 and  15.1.0.0.0-15.2.0.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Communications Billing and Revenue Management executes to compromise Oracle Communications Billing and Revenue Management.  Successful attacks of this vulnerability can result in takeover of Oracle Communications Billing and Revenue Management. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61091

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:40.110 |

Vulnerability in the Oracle Communications Billing and Revenue Management product of Oracle Communications (component: BRM Server).  Supported versions that are affected are 15.0.0.0.0, 15.0.1.0.0, 15.1.0.0.0 and  15.2.0.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Communications Billing and Revenue Management executes to compromise Oracle Communications Billing and Revenue Management.  Successful attacks of this vulnerability can result in takeover of Oracle Communications Billing and Revenue Management. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61090

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:39.997 |

Vulnerability in the Oracle Project Foundation product of Oracle E-Business Suite (component: Miscellaneous).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Project Foundation executes to compromise Oracle Project Foundation.  Successful attacks of this vulnerability can result in takeover of Oracle Project Foundation. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61055

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:36.290 |

Vulnerability in the PeopleSoft Enterprise SCM Order Management product of Oracle PeopleSoft (component: Security).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where PeopleSoft Enterprise SCM Order Management executes to compromise PeopleSoft Enterprise SCM Order Management.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise SCM Order Management. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61053

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:36.177 |

Vulnerability in the Oracle Communications BRM - Elastic Charging Engine product of Oracle Communications (component: Diameter Gateway and SDK).  Supported versions that are affected are 15.0.0.0.0, 15.0.1.0.0, 15.1.0.0.0 and  15.2.0.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Communications BRM - Elastic Charging Engine executes to compromise Oracle Communications BRM - Elastic Charging Engine.  Successful attacks of this vulnerability can result in takeover of Oracle Communications BRM - Elastic Charging Engine. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60973

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:30.890 |

Vulnerability in the Oracle E-Business Tax product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle E-Business Tax executes to compromise Oracle E-Business Tax.  Successful attacks of this vulnerability can result in takeover of Oracle E-Business Tax. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60661

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:07.040 |

Vulnerability in the Oracle Solaris product of Oracle Systems (component: Filesystems).   The supported version that is affected is 11.4. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Solaris executes to compromise Oracle Solaris.  While the vulnerability is in Oracle Solaris, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Solaris. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60625

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:03.060 |

Vulnerability in the Oracle Data Integrator product of Oracle Fusion Middleware (component: Studio).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Data Integrator executes to compromise Oracle Data Integrator.  Successful attacks of this vulnerability can result in takeover of Oracle Data Integrator. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60600

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:00.180 |

Vulnerability in the PeopleSoft Enterprise FIN Project Costing product of Oracle PeopleSoft (component: Projects).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where PeopleSoft Enterprise FIN Project Costing executes to compromise PeopleSoft Enterprise FIN Project Costing.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise FIN Project Costing. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60570

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:57.260 |

Vulnerability in Oracle GoldenGate (component: Libraries).  Supported versions that are affected are 23.4-23.26.1. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle GoldenGate executes to compromise Oracle GoldenGate.  Successful attacks of this vulnerability can result in takeover of Oracle GoldenGate. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60530

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:52.720 |

Vulnerability in the Oracle HTTP Server product of Oracle Fusion Middleware (component: mod_http2.so).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle HTTP Server executes to compromise Oracle HTTP Server.  Successful attacks of this vulnerability can result in takeover of Oracle HTTP Server. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60454

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:47.857 |

Vulnerability in the Oracle HTTP Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle HTTP Server executes to compromise Oracle HTTP Server.  Successful attacks of this vulnerability can result in takeover of Oracle HTTP Server. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60271

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:29.350 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Coherence executes to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60150

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:15.650 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.12. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-47054

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:11.133 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.12. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. Note: This vulnerability applies to Windows host only. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-47047

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:10.343 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.12. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-16493

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-07-21T18:16:57.030 |

A flaw was found in ansible-core. The _extract_collection_from_git() function in ansible-core's concrete_artifact_manager.py constructs git clone commands without a '--' (end-of-options) separator before user-supplied URLs when installing collections from git sources. An attacker who provides a crafted collection source URI containing git argument injection payloads can achieve arbitrary command execution when a user runs 'ansible-galaxy collection install' with the malicious source. This is an incomplete fix for CVE-2026-11332, which hardened the role install path but missed the equivalent collection install code path.

### CVE-2026-8933

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-07-21T15:16:39.563 |

A local privilege escalation vulnerability exists in snap-confine, a set-capabilities core component used internally by Canonical snapd to construct the secure execution environment for snap applications. This vulnerability uniquely affects versions of snap-confine configured with set-capabilities (rather than standard set-uid-root installations).
Due to a flaw in how privilege boundaries or security sandboxes are initialized when the binary runs under limited ambient capabilities, a local, unprivileged attacker can exploit this behavior to bypass intended restrictions and execute arbitrary code. Successful exploitation allows the local user to elevate their privileges to full root authority.

### CVE-2026-65016

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-22T12:18:18.733 |

n8n versions before 1.123.64, 2.29.8, and 2.30.1 contain a privilege escalation vulnerability in Enterprise SSO instance-role provisioning. The provisioning path maps an IdP-asserted role claim to an n8n global role but does not prevent assignment of the global:owner role (unlike the token-exchange identity path, which rejects it). An SSO-authenticated user whose instance-role claim resolves to global:owner is provisioned as instance owner, gaining full administrative control over workflows, credentials, users, and instance configuration. Exploitation requires that Enterprise SSO is configured, instance-role provisioning is enabled via N8N_SSO_SCOPES_PROVISION_INSTANCE_ROLE (disabled by default), and the attacker controls the instance-role claim value issued by the IdP.

### CVE-2026-61390

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-22T12:18:18.137 |

There is a heap buffer overflow vulnerability in some Hikvision cameras, which may allow unauthenticated attackers to cause device malfunction by sending specially crafted packets.

### CVE-2026-62567

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-284` |
| Published | 2026-07-21T22:19:09.553 |

Vulnerability in the Oracle HRMS (UK) product of Oracle E-Business Suite (component: UK Payroll).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle HRMS (UK).  While the vulnerability is in Oracle HRMS (UK), attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle HRMS (UK) accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-62560

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-284` |
| Published | 2026-07-21T22:19:08.987 |

Vulnerability in the Oracle HRMS (Norway) product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle HRMS (Norway).  While the vulnerability is in Oracle HRMS (Norway), attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle HRMS (Norway) accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-61324

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:00.787 |

Vulnerability in the Oracle Advanced Benefits product of Oracle E-Business Suite (component: Internal Operations).   The supported version that is affected is 12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Advanced Benefits.  While the vulnerability is in Oracle Advanced Benefits, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Advanced Benefits accessible data. CVSS 3.1 Base Score 7.7 (Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N).

### CVE-2026-61142

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:45.527 |

Vulnerability in the Oracle Payroll product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Payroll.  While the vulnerability is in Oracle Payroll, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Payroll accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-61125

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:43.710 |

Vulnerability in the Oracle Configure to Order product of Oracle E-Business Suite (component: Supply to Order Workbench).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Configure to Order.  While the vulnerability is in Oracle Configure to Order, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Configure to Order accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-61014

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:33.243 |

Vulnerability in the Oracle Inventory Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Inventory Management.  While the vulnerability is in Oracle Inventory Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Inventory Management accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60923

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:27.360 |

Vulnerability in the Oracle Capacity product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Capacity.  While the vulnerability is in Oracle Capacity, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Capacity accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60824

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:20.340 |

Vulnerability in the Oracle iSupport product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iSupport.  While the vulnerability is in Oracle iSupport, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle iSupport accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60750

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:15.040 |

Vulnerability in the Oracle Payroll product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Payroll.  While the vulnerability is in Oracle Payroll, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Payroll accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60690

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:09.817 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.5. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  While the vulnerability is in Siebel CRM Cloud Applications, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60683

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:09.017 |

Vulnerability in the Oracle Process Manufacturing Regulatory Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Regulatory Management.  While the vulnerability is in Oracle Process Manufacturing Regulatory Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Process Manufacturing Regulatory Management accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60657

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:06.700 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-60586

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:59.050 |

Vulnerability in the MySQL Connectors product of Oracle MySQL (component: Connector/J).  Supported versions that are affected are 9.7.0-9.7.1. Easily exploitable vulnerability allows low privileged attacker with network access via multiple protocols to compromise MySQL Connectors.  While the vulnerability is in MySQL Connectors, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all MySQL Connectors accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60548

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:54.737 |

Vulnerability in the Oracle SOA Suite product of Oracle Fusion Middleware (component: Integration Business Insight).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle SOA Suite.  While the vulnerability is in Oracle SOA Suite, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle SOA Suite accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60534

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:53.170 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: PeopleSoft Applications).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Identity Manager Connector.  While the vulnerability is in Oracle Identity Manager Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Identity Manager Connector accessible data as well as  unauthorized access to critical data or complete access to all Oracle Identity Manager Connector accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60440

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:46.400 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Service Delivery Platform.  While the vulnerability is in Service Delivery Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Service Delivery Platform accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-46987

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:03.810 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Application Service Level Mgmt).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  While the vulnerability is in Oracle Enterprise Manager Base Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Enterprise Manager Base Platform accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-43946

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-21T22:17:01.410 |

FUXA is a web-based Process Visualization (SCADA/HMI/Dashboard) software. Version 1.3.0 has an authorization bypass in the /api/getTagValue endpoint allows unauthenticated access to tag values when the referenced script does not exist. Version 1.3.1 patches the issue.

### CVE-2026-62518

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:07.053 |

Vulnerability in the Oracle Production Scheduling product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Production Scheduling.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Production Scheduling accessible data as well as  unauthorized read access to a subset of Oracle Production Scheduling accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Production Scheduling. CVSS 3.1 Base Score 7.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L).

### CVE-2026-62515

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:06.723 |

Vulnerability in the Oracle Advanced Planning Command Center product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Advanced Planning Command Center.  While the vulnerability is in Oracle Advanced Planning Command Center, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Advanced Planning Command Center accessible data as well as  unauthorized update, insert or delete access to some of Oracle Advanced Planning Command Center accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-61325

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:00.897 |

Vulnerability in the Oracle Advanced Benefits product of Oracle E-Business Suite (component: Internal Operations).   The supported version that is affected is 12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Advanced Benefits.  While the vulnerability is in Oracle Advanced Benefits, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Advanced Benefits accessible data as well as  unauthorized update, insert or delete access to some of Oracle Advanced Benefits accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-61181

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:49.870 |

Vulnerability in the Oracle Agile Product Lifecycle Management for Process product of Oracle Supply Chain (component: Product Quality Management).   The supported version that is affected is 6.2.4. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile Product Lifecycle Management for Process.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Agile Product Lifecycle Management for Process, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Agile Product Lifecycle Management for Process accessible data as well as  unauthorized update, insert or delete access to some of Oracle Agile Product Lifecycle Management for Process accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-61132

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:44.500 |

Vulnerability in the Oracle Commerce Platform product of Oracle Commerce (component: Dynamo Application Framework).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Platform.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Commerce Platform, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Platform accessible data as well as  unauthorized update, insert or delete access to some of Oracle Commerce Platform accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-60886

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:24.593 |

Vulnerability in the Oracle Work in Process product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Work in Process.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Work in Process, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Work in Process accessible data as well as  unauthorized update, insert or delete access to some of Oracle Work in Process accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-60642

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:04.973 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Content accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle WebCenter Content. CVSS 3.1 Base Score 7.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:L).

### CVE-2026-60641

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:04.863 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Content accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle WebCenter Content. CVSS 3.1 Base Score 7.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:L).

### CVE-2026-60584

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:58.823 |

Vulnerability in the Oracle Transportation Management product of Oracle Supply Chain (component: CSV Management).   The supported version that is affected is 6.5.3. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Transportation Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Transportation Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Transportation Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Transportation Management. CVSS 3.1 Base Score 7.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-60578

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:58.140 |

Vulnerability in the Oracle Enterprise Command Center Framework product of Oracle E-Business Suite (component: Core).   The supported version that is affected is V16. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Enterprise Command Center Framework.  While the vulnerability is in Oracle Enterprise Command Center Framework, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Enterprise Command Center Framework accessible data as well as  unauthorized update, insert or delete access to some of Oracle Enterprise Command Center Framework accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-60528

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:52.510 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Console).  Supported versions that are affected are 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle WebLogic Server.  While the vulnerability is in Oracle WebLogic Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebLogic Server accessible data as well as  unauthorized read access to a subset of Oracle WebLogic Server accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:N).

### CVE-2026-60522

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:51.840 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-10680

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-21T22:17:00.303 |

The Classic (BR/EDR) L2CAP signaling handlers l2cap_br_conf_req() and l2cap_br_conf_rsp() in subsys/bluetooth/host/classic/l2cap_br.c validated the minimum command size against buf->len (the bytes remaining in the whole received PDU) instead of len (the per-command data length from the L2CAP signaling header). Because multiple signaling commands can be packed into one PDU, buf->len may exceed a command's len. An attacker can send a CONF_REQ command with a header length smaller than the configuration-request structure (e.g. 0), followed by another command so that buf->len still satisfies the check. The check then passes incorrectly and opt_len = len - sizeof(*req) underflows the uint16_t to a near-0xFFFF value. The configuration-option loop, which lacks an opt_len-versus-buf->len guard, then walks far past the end of the pooled ACL receive buffer using net_buf pull primitives that perform no runtime bounds check, producing an out-of-bounds read of host memory and, when the out-of-bounds option bytes encode an MTU or flush-timeout option, an out-of-bounds write. The BR/EDR signaling channel is processed before pairing/encryption and an L2CAP channel to an L0 service such as SDP can be opened without pairing, so an unauthenticated peer within radio range that can establish an ACL connection can trigger the flaw, leading to memory corruption and denial of service (host/device crash). The defect is present in released versions including v4.4.0. The fix validates against len instead of buf->len in both handlers.

### CVE-2026-47414

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-21T18:17:00.283 |

PraisonAI Platform is the platform layer for the PraisonAI multi-agent teams system. Versions prior to 0.1.4 have an Insecure Direct Object Reference. Five label endpoints — `PATCH /workspaces/{workspace_id}/labels/{label_id}`, `DELETE .../labels/{label_id}`, `POST .../issues/{issue_id}/labels/{label_id}`, `DELETE .../issues/{issue_id}/labels/{label_id}`, `GET .../issues/{issue_id}/labels` — gate access on `require_workspace_member(workspace_id)` only and pass URL-supplied `label_id` and `issue_id` straight through to `LabelService` without verifying either belongs to the workspace. PraisonAI Platform version 0.1.4 patches the issue.

### CVE-2026-62145

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-22T14:17:22.920 |

A vulnerability in Check Point Gaia Portal allows an authenticated attacker with read-only Gaia Portal privileges to execute commands with root privileges.

### CVE-2026-55973

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-22T14:17:21.663 |

In NLnet Labs Unbound 1.23.0 up to and including 1.25.1, when 'dns-error-reporting: yes' is set, the EDNS Report-Channel option (code 18) from the last upstream response is read and uses the option's length as the length of the agent domain. When a domain name check is performed on the agent domain, the returned lenght is not used and if the agent domain is followed by garbage, those bytes are moved onto the tail of the synthetic '_er.' report query name. That query name is later used in the iterator via a subquery to send out the DNS Error Report and when Unbound tries to walk that query name during 'find_closest_of_type()', it strips labels using the query name length rather than stopping at the embedded root, walks one byte past it, and feeds the first garbage byte to 'dname_query_hash()' as a label length writing over the stack variable 'labuf'. One ordinary upstream response from a delegated zone the attacker controls is sufficient to terminate the daemon.

### CVE-2026-44690

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-345` |
| Published | 2026-07-22T14:17:19.153 |

In NLnet Labs Unbound 1.7.0 up to and including 1.25.1, insufficient validation of the RRSIG.Labels field combined with premature cache writes during RFC 8198 aggressive NSEC processing leads to cache poisoning that permits a malicious actor controlling a single delegated zone to poison arbitrary sibling zones under NSEC-signed parent domains. A malicious actor with one registered domain under an NSEC-signed TLD can serve malicious insecure DNS responses for unrelated sibling domains (sharing the same parent zone). Arbitrary delegations that do not exist under the parent domain and are covered by the parent's NSEC chain can be brought into insecure existence by fraudulent wildcard DS records (less labels than expected, unknown algorithm) from the malicious sibling domain. This allows the malicious actor to inject insecure wildcard records for those delegations.

### CVE-2026-40691

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-07-22T14:17:18.437 |

In Unbound 1.9.0 up to and including 1.25.1, when a DNSCrypt query is received over TCP, the routine that encrypts the reply in place fails to bound the reply length against the destination buffer size. The size clamp that protects the UDP path is not applied on the TCP path, so a reply larger than 65504 bytes is shifted forward by 48 bytes inside a buffer of capacity equal to 'msg-buffer-size', writing past the end of the heap allocation. A single malicious encrypted query crashes the resolver and lead to denial of service. This vulnerability needs Unbound to be compiled with DNSCrypt support ('--enable-dnscrypt') and the 'dnscrypt:' clause to be configured and enabled for the listening interfaces.

### CVE-2026-32665

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1284` |
| Published | 2026-07-22T14:17:18.193 |

In NLnet Labs Unbound 1.22.0 up to and including 1.25.1, when downstream DNS-over-QUIC (DoQ) is enabled, the first two bidirectional streams on a new QUIC connection (stream_id 0 and 4) bypass the per-stream 'quic-size' gate entirely, and large input buffers are allocated later, after only the 2-byte length prefix has been received from the initial streams. As a result, a remote client can make Unbound exceed the configured 'quic-size' limit with low-cost input. Using only one connection and two streams, each sending a declared 65535-byte length prefix and then holding the streams open, a client can already trivially make Unbound roughly allocate double that amount. This is a remote availability issue / memory-accounting bypass in the downstream DoQ implementation that leads to denial of service for new DoQ clients. This vulnerability needs Unbound to be compiled with DoQ support ('--with-libngtcp2') and the 'quic-port' to be configured for the listening interfaces.

### CVE-2026-13189

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-36` |
| Published | 2026-07-22T14:17:14.537 |

In Progress® Telerik® UI for AJAX prior to v2026.2.708, insufficient validation of the language parameter in the spell check handler may allow an attacker to influence server-side file path resolution and trigger unintended server-side requests.

### CVE-2026-13184

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-321` |
| Published | 2026-07-22T14:17:13.927 |

In Progress® Telerik® UI for AJAX prior to v2026.2.708, when Telerik.Upload.ConfigurationHashKey is absent and machineKey is not explicitly configured, upload metadata integrity protection may fall back to a predictable default key, enabling attackers to forge protected upload metadata and unlock further exploit chains.

### CVE-2026-13183

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-208` |
| Published | 2026-07-22T14:17:13.807 |

In Progress® Telerik® UI for AJAX prior to v2026.2.708, RadAsyncUpload upload metadata processing may leak cryptographic validity through measurable timing differences, enabling remote attackers to recover protected metadata values.

### CVE-2026-13182

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-209` |
| Published | 2026-07-22T14:17:13.683 |

In Progress® Telerik® UI for AJAX prior to v2026.2.708, RadAsyncUpload client-state processing can distinguish decrypt failures from invalid-JSON parse failures, creating an oracle that reveals protected metadata values to remote attackers.

### CVE-2026-57600

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-22T12:18:16.883 |

Insufficient validation of input parameters in the firmware of some Hikvision cameras allows unauthenticated attackers to retrieve partial sensitive data.

### CVE-2026-63047

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-22T08:16:23.950 |

The Joomla extension Events Booking prior version 5.0-5.8.1 did not properly verify that an actor is allowed to download invoice information.

### CVE-2026-12987

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-22T07:16:35.203 |

The Events Manager  WordPress plugin before 7.3.7 does not safely handle booking-registration data on sites using No-User-Account Booking Mode: a booker-supplied registration field is stored as booking meta and later deserialized without restricting allowed classes, enabling PHP object injection. The resulting gadget chain reaches a database query that is built without parameterisation, so an unauthenticated attacker can read arbitrary database data (e.g. user password hashes, secret keys) when the booking is later loaded.

### CVE-2026-56819

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-401` |
| Published | 2026-07-21T23:17:52.263 |

Netty is a network application framework for development of protocol servers and clients. In versions 4.2.0.Final through 4.2.15.Final and 4.1.0.Final through 4.1.135.Final, a remote unauthenticated peer can leak one direct `ByteBuf` per HTTP/2 `DATA` frame in applications that enable HTTP/2 content decompression via `DelegatingDecompressorFrameListener`. When a `DATA` frame is processed for a stream whose decompressor has already been closed, `Http2Decompressor.decompress(...)` calls `decompressor.writeInbound(data.retain())` and does not release the retained buffer on the error path, eventually exhausting direct memory and crashing the JVM. This issue is fixed in versions 4.1.136.Final and 4.2.16.Final.

### CVE-2026-16422

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-21T23:16:59.817 |

Insufficient validation of untrusted input in Certificate in Google Chrome on Linux prior to 150.0.7871.182 allowed an attacker in a privileged network position to perform domain spoofing via malicious network traffic. (Chromium security severity: High)

### CVE-2026-62521

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:07.280 |

Vulnerability in the Oracle HRMS (US) product of Oracle E-Business Suite (component: US Payroll - General).  Supported versions that are affected are 12.2.7-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle HRMS (US).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle HRMS (US) accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-62495

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:05.497 |

Vulnerability in the Oracle Process Manufacturing Process Execution product of Oracle E-Business Suite (component: Internal Operations).   The supported version that is affected is 12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Process Execution.  Successful attacks of this vulnerability can result in takeover of Oracle Process Manufacturing Process Execution. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62493

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:05.270 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.11-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in takeover of Oracle Purchasing. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61337

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:01.813 |

Vulnerability in the Oracle Lease and Finance Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.11-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Lease and Finance Management.  Successful attacks of this vulnerability can result in takeover of Oracle Lease and Finance Management. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61309

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:59.650 |

Vulnerability in the Oracle In-Memory Cost Management for Discrete Industries product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle In-Memory Cost Management for Discrete Industries.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle In-Memory Cost Management for Discrete Industries accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-61236

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:54.460 |

Vulnerability in the PeopleSoft Enterprise FIN Common Objects Brazil product of Oracle PeopleSoft (component: Staffing).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Common Objects Brazil.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise FIN Common Objects Brazil accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-61232

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:54.023 |

Vulnerability in the PeopleSoft Enterprise FIN Common Objects Brazil product of Oracle PeopleSoft (component: Common Objects).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Common Objects Brazil.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise FIN Common Objects Brazil accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-61226

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:53.917 |

Vulnerability in the Oracle Communications Converged Application Server product of Oracle Communications (component: RTP Proxy).   The supported version that is affected is 8.3. Difficult to exploit vulnerability allows high privileged attacker with logon to the infrastructure where Oracle Communications Converged Application Server executes to compromise Oracle Communications Converged Application Server.  While the vulnerability is in Oracle Communications Converged Application Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Communications Converged Application Server. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61202

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:51.947 |

Vulnerability in the Oracle Solaris product of Oracle Systems (component: Utility).  Supported versions that are affected are 11.3 and  11.4. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Solaris executes to compromise Oracle Solaris.  While the vulnerability is in Oracle Solaris, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Solaris accessible data as well as  unauthorized access to critical data or complete access to all Oracle Solaris accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-61188

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:50.700 |

Vulnerability in the Oracle Agile Product Lifecycle Management for Process product of Oracle Supply Chain (component: Installation).   The supported version that is affected is 6.2.4. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile Product Lifecycle Management for Process.  Successful attacks of this vulnerability can result in takeover of Oracle Agile Product Lifecycle Management for Process. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61172

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:48.940 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Security).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Agile PLM accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-61159

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:47.463 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-61158

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:47.357 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via RMI to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-61157

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:47.243 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-61141

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:45.420 |

Vulnerability in the Oracle Advanced Benefits product of Oracle E-Business Suite (component: Affordable Care Act).  Supported versions that are affected are 12.2.7-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Advanced Benefits.  Successful attacks of this vulnerability can result in takeover of Oracle Advanced Benefits. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61138

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:45.187 |

Vulnerability in the Oracle Complex Maintenance, Repair and Overhaul product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Complex Maintenance, Repair and Overhaul.  While the vulnerability is in Oracle Complex Maintenance, Repair and Overhaul, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Complex Maintenance, Repair and Overhaul accessible data as well as  unauthorized update, insert or delete access to some of Oracle Complex Maintenance, Repair and Overhaul accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-61133

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:44.617 |

Vulnerability in the Oracle Commerce Platform product of Oracle Commerce (component: Dynamo Application Framework).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Commerce Platform.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Platform accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-61116

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:42.923 |

Vulnerability in the Oracle Application Object Library product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Application Object Library.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Application Object Library accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-61114

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:42.707 |

Vulnerability in the Oracle Application Object Library product of Oracle E-Business Suite (component: DB Privileges).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Application Object Library.  Successful attacks of this vulnerability can result in takeover of Oracle Application Object Library. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61088

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:39.763 |

Vulnerability in the PeopleSoft Enterprise SCM Manufacturing product of Oracle PeopleSoft (component: Security).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise SCM Manufacturing.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise SCM Manufacturing accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-61087

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:39.663 |

Vulnerability in the PeopleSoft Enterprise FIN Payables product of Oracle PeopleSoft (component: Security).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Payables.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise FIN Payables accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-61086

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:39.550 |

Vulnerability in the PeopleSoft Enterprise SCM Order Management product of Oracle PeopleSoft (component: Security).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise PeopleSoft Enterprise SCM Order Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise SCM Order Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-61085

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:39.440 |

Vulnerability in the PeopleSoft Enterprise SCM Inventory product of Oracle PeopleSoft (component: Security).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise PeopleSoft Enterprise SCM Inventory.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise SCM Inventory accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-61077

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:38.523 |

Vulnerability in the PeopleSoft Enterprise SCM Mobile Inventory Management product of Oracle PeopleSoft (component: Security).   The supported version that is affected is 9.2. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where PeopleSoft Enterprise SCM Mobile Inventory Management executes to compromise PeopleSoft Enterprise SCM Mobile Inventory Management.  While the vulnerability is in PeopleSoft Enterprise SCM Mobile Inventory Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise SCM Mobile Inventory Management accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise SCM Mobile Inventory Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-61073

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:38.090 |

Vulnerability in the PeopleSoft Enterprise FIN Common Objects Brazil product of Oracle PeopleSoft (component: Purchasing).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Common Objects Brazil.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise FIN Common Objects Brazil accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-61026

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:34.037 |

Vulnerability in the Oracle iRecruitment product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle iRecruitment.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle iRecruitment accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60988

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:31.910 |

Vulnerability in the Oracle Project Portfolio Analysis product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Project Portfolio Analysis.  Successful attacks of this vulnerability can result in takeover of Oracle Project Portfolio Analysis. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60943

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:29.150 |

Vulnerability in the Oracle Service Fulfillment Manager product of Oracle E-Business Suite (component: Fulfillment Engine).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Service Fulfillment Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Service Fulfillment Manager. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60931

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:28.113 |

Vulnerability in the Oracle Public Sector Financials product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Public Sector Financials.  Successful attacks of this vulnerability can result in takeover of Oracle Public Sector Financials. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60927

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:27.783 |

Vulnerability in the Oracle Public Sector Financials product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Public Sector Financials.  Successful attacks of this vulnerability can result in takeover of Oracle Public Sector Financials. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60894

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:25.247 |

Vulnerability in the Oracle Payroll product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Payroll.  Successful attacks of this vulnerability can result in takeover of Oracle Payroll. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60859

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:23.220 |

Vulnerability in the Oracle Quoting product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Quoting.  Successful attacks of this vulnerability can result in takeover of Oracle Quoting. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60855

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:22.993 |

Vulnerability in the Oracle Quality product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Quality.  Successful attacks of this vulnerability can result in takeover of Oracle Quality. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60806

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:19.213 |

Vulnerability in the Oracle Cost Management product of Oracle E-Business Suite (component: Costing Transaction Errors).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Cost Management.  Successful attacks of this vulnerability can result in takeover of Oracle Cost Management. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60770

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:16.067 |

Vulnerability in the Oracle Application Object Library product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Application Object Library.  Successful attacks of this vulnerability can result in takeover of Oracle Application Object Library. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60704

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:10.830 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.5. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60689

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:09.703 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.5. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60658

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:06.817 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60629

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:03.510 |

Vulnerability in the Oracle JDeveloper product of Oracle Fusion Middleware (component: Data Visualization Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle JDeveloper.  While the vulnerability is in Oracle JDeveloper, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle JDeveloper accessible data as well as  unauthorized update, insert or delete access to some of Oracle JDeveloper accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-60622

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:02.717 |

Vulnerability in the Oracle JDeveloper product of Oracle Fusion Middleware (component: Security Framework).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle JDeveloper.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle JDeveloper accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60619

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:02.363 |

Vulnerability in the JD Edwards EnterpriseOne HCM Foundation product of Oracle JD Edwards (component: Time Accounting and HRM Base).   The supported version that is affected is 9.2. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise JD Edwards EnterpriseOne HCM Foundation.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne HCM Foundation. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60605

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:00.757 |

Vulnerability in the PeopleSoft Enterprise CS Student Records product of Oracle PeopleSoft (component: Higher Ed Statistics Agency - UK HESA).   The supported version that is affected is 9.2.38. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise CS Student Records.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise CS Student Records accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60604

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:00.650 |

Vulnerability in the PeopleSoft Enterprise CS Campus Community product of Oracle PeopleSoft (component: Security).   The supported version that is affected is 9.2.38. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise CS Campus Community.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise CS Campus Community. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60598

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:59.957 |

Vulnerability in the PeopleSoft Enterprise CS Student Records product of Oracle PeopleSoft (component: Research Tracking).   The supported version that is affected is 9.2.38. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise CS Student Records.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise CS Student Records. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60593

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:59.383 |

Vulnerability in the PeopleSoft Enterprise FIN Staffing Front Office product of Oracle PeopleSoft (component: Staffing Front Office).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Staffing Front Office.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise FIN Staffing Front Office accessible data. CVSS 3.1 Base Score 7.5 (Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N).

### CVE-2026-60581

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:58.480 |

Vulnerability in the Oracle Enterprise Command Center Framework product of Oracle E-Business Suite (component: Core).   The supported version that is affected is V16. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Enterprise Command Center Framework executes to compromise Oracle Enterprise Command Center Framework.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Command Center Framework. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60554

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:55.407 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Sites accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60498

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:50.917 |

Vulnerability in the JD Edwards EnterpriseOne Human Resources Management product of Oracle JD Edwards (component: Human Resources).   The supported version that is affected is 9.2. Difficult to exploit vulnerability allows low privileged attacker with network access via JDENET to compromise JD Edwards EnterpriseOne Human Resources Management.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Human Resources Management. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60497

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:50.803 |

Vulnerability in the JD Edwards EnterpriseOne CRM Foundation product of Oracle JD Edwards (component: CRM Foundation).   The supported version that is affected is 9.2. Difficult to exploit vulnerability allows low privileged attacker with network access via JDENET to compromise JD Edwards EnterpriseOne CRM Foundation.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne CRM Foundation. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60496

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:50.693 |

Vulnerability in the JD Edwards EnterpriseOne Advanced Pricing - Procurement product of Oracle JD Edwards (component: Advanced Pricing).   The supported version that is affected is 9.2. Difficult to exploit vulnerability allows low privileged attacker with network access via JDENET to compromise JD Edwards EnterpriseOne Advanced Pricing - Procurement.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Advanced Pricing - Procurement. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60495

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:50.577 |

Vulnerability in the JD Edwards EnterpriseOne Requirements Planning product of Oracle JD Edwards (component: Requirements Planning).   The supported version that is affected is 9.2. Difficult to exploit vulnerability allows low privileged attacker with network access via JDENET to compromise JD Edwards EnterpriseOne Requirements Planning.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Requirements Planning. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60467

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:49.190 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise WebCenter Content: Imaging.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of WebCenter Content: Imaging. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60436

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:46.057 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Unified Directory. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-60425

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:44.910 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Unified Directory. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-60382

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:40.940 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Service Delivery Platform. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-60320

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:34.853 |

Vulnerability in the Oracle Data Integrator product of Oracle Fusion Middleware (component: Patchset Assistant).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Data Integrator.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Data Integrator accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60314

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:34.173 |

Vulnerability in the MySQL Router product of Oracle MySQL (component: Router: General).  Supported versions that are affected are 8.4.0-8.4.10 and  9.7.0-9.7.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise MySQL Router.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of MySQL Router. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-60301

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:32.707 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Coherence. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-60263

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:28.383 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Coherence accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60252

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:27.147 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Coherence. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-60223

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:23.897 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Coherence. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-60180

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:18.960 |

Vulnerability in the MySQL Connectors product of Oracle MySQL (component: Connector/C++).  Supported versions that are affected are 9.7.0-9.7.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise MySQL Connectors.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of MySQL Connectors. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-60170

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:17.817 |

Vulnerability in the Oracle Hospitality Simphony product of Oracle Food and Beverage Applications (component: POS).  Supported versions that are affected are 19.8-19.8.5, 19.9-19.9.3 and  19.10. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hospitality Simphony.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hospitality Simphony accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60167

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:17.467 |

Vulnerability in the Oracle Hospitality Simphony product of Oracle Food and Beverage Applications (component: POS).  Supported versions that are affected are 19.8-19.8.5, 19.9-19.9.3 and  19.10. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hospitality Simphony.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hospitality Simphony accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60159

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:16.547 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.12. Difficult to exploit vulnerability allows high privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  While the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60155

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:16.097 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.12. Difficult to exploit vulnerability allows high privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  While the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-56816

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-21T22:17:14.803 |

Netty is a network application framework for development of protocol servers and clients. Prior to 4.2.16.Final, Netty's `Http3FrameCodec` buffers incoming data for HTTP/3 reserved frame types up to the wire-specified payload length without limits; `decodeFrame` trusts `payLoadLength`, allowing an attacker to open multiple QUIC streams and send reserved frames with very large payload lengths to cause memory exhaustion and denial of service. This issue is fixed in version 4.2.16.Final.

### CVE-2026-47247

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-226;CWE-682;CWE-908` |
| Published | 2026-07-21T22:17:12.643 |

libheif is a HEIF and AVIF file format decoder and encoder. Prior to version 1.22.0, two bugs in libheif chain to leak process heap memory as visible pixel values in decoded grid images. An attacker who uploads a crafted AVIF/HEIC file to any server-side image processor (WordPress, Sharp/libvips, ImageMagick, etc.) can recover heap data - including library function pointers sufficient to defeat ASLR, or any other secret - from the publicly-downloadable transcoded JPEG/PNG/WebP output. Local attack vectors are also possible. Version 1.22.0 fixes the issue.

### CVE-2026-47063

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:12.190 |

Vulnerability in the Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition product of Oracle Java SE (component: Libraries).  Supported versions that are affected are Oracle Java SE: 8u491, 8u491-perf, 11.0.31, 17.0.19, 21.0.11, 25.0.3, 26.0.1; Oracle GraalVM for JDK: 17.0.19 and  21.0.11; Oracle GraalVM Enterprise Edition: 21.3.18. Easily exploitable vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition accessible data. Note: This vulnerability can be exploited by using APIs in the specified Component, e.g., through a web service which supplies data to the APIs. This vulnerability also applies to Java deployments, typically in clients running sandboxed Java Web Start applications or sandboxed Java applets, that load and run untrusted code (e.g., code that comes from the internet) and rely on the Java sandbox for security. CVSS 3.1 Base Score 7.5 (Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N).

### CVE-2026-47057

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:11.483 |

Vulnerability in Oracle Java SE (component: Scripting).  Supported versions that are affected are Oracle Java SE: 8u491, 8u491-perf and  11.0.31. Easily exploitable vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise Oracle Java SE.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Java SE. Note: This vulnerability can be exploited by using APIs in the specified Component, e.g., through a web service which supplies data to the APIs. This vulnerability also applies to Java deployments, typically in clients running sandboxed Java Web Start applications or sandboxed Java applets, that load and run untrusted code (e.g., code that comes from the internet) and rely on the Java sandbox for security. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-47018

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:07.450 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.5. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-46941

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:02.283 |

Vulnerability in the Oracle Cost Management product of Oracle E-Business Suite (component: Cost Maintenance).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Cost Management.  Successful attacks of this vulnerability can result in takeover of Oracle Cost Management. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35287

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:01.020 |

Vulnerability in Oracle Application Testing Suite.   The supported version that is affected is 13.3.0.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Application Testing Suite.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Application Testing Suite accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-47690

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-77;CWE-1336` |
| Published | 2026-07-21T21:16:51.067 |

MeltanoHub is the source code for hub.meltano.com, the central place for Meltano plugins. Versions of the repo prior to commit 923820de8f64d753951fbbd54f7282a3d5f75173 were vulnerable to exfiltration of `GITHUB_TOKEN` with write permissions to the repository. The vulnerable workflow used pull_request_target, which runs in the context of the base repository with access to secrets. Commit 923820de8f64d753951fbbd54f7282a3d5f75173 fixes the issue. No known workarounds are available.

### CVE-2026-47667

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401;CWE-789;CWE-1284` |
| Published | 2026-07-21T20:17:01.323 |

CImg Library is a C++ library for image processing. Prior to version 4.0.0 in `_load_analyze()`, the header_size field is read as an `unsigned int` from the first 4 bytes of an Analyze/NIfTI file and passed directly to `new unsigned char[header_size]` without being bounded against the actual file size. A value up to ~4 GB is accepted. If the subsequent `fread` returns `short`  as it will for any malformed file), the function throws a `CImgIOException` and the allocated buffer is never freed. A 6-byte crafted file is sufficient to trigger an allocation of ~1.3 GB per call, with the full allocation leaked on every error path. The issue is reachable via `load_analyze()` and the generic `load()` when the file extension is .hdr, .img, or .nii. Version 4.0.0 fixes the issue.

### CVE-2026-44907

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T17:17:08.227 |

A denial of service vulnerability could be triggered by sending specially crafted HTTP requests to server function endpoints, this could lead to excessive CPU usage; affecting the following packages: react-server-dom-webpack, react-server-dom-parcel, react-server-dom-turbopack (versions 19.0.0 through 19.0.7, 19.1.0 through 19.1.8, and 19.2.0 through 19.2.7).

### CVE-2026-56820

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-07-21T23:17:52.403 |

Netty is a network application framework for development of protocol servers and clients. In versions 4.2.0.Final through 4.2.15.Final and prior to 4.1.135.Final, `OcspClient` does not validate that the `CertificateID` in an OCSP response matches the requested `CertificateID`, which can lead to replay attack. `OcspClient.validateResponse` accepts a legitimately signed `GOOD` status response for an unrelated certificate issued by the same CA, allowing bypass of revocation checks for another certificate. This issue is fixed in versions 4.1.136.Final and 4.2.16.Final.

### CVE-2026-61234

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:54.243 |

Vulnerability in the PeopleSoft Enterprise FIN Common Objects Brazil product of Oracle PeopleSoft (component: eProcurement).   The supported version that is affected is 9.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Common Objects Brazil.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise FIN Common Objects Brazil accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise FIN Common Objects Brazil accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61210

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:52.677 |

Vulnerability in the PeopleSoft Enterprise SCM Manufacturing product of Oracle PeopleSoft (component: Security).   The supported version that is affected is 9.2. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise PeopleSoft Enterprise SCM Manufacturing.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise SCM Manufacturing accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise SCM Manufacturing accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61185

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:50.353 |

Vulnerability in the Oracle Agile Product Lifecycle Management for Process product of Oracle Supply Chain (component: Installation).   The supported version that is affected is 6.2.4. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Agile Product Lifecycle Management for Process executes to compromise Oracle Agile Product Lifecycle Management for Process.  While the vulnerability is in Oracle Agile Product Lifecycle Management for Process, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Agile Product Lifecycle Management for Process accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-61173

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:49.057 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Security).   The supported version that is affected is 9.3.6. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Agile PLM accessible data as well as  unauthorized access to critical data or complete access to all Oracle Agile PLM accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61164

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:48.020 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Content Acquisition System).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61135

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:44.847 |

Vulnerability in the Oracle Commerce Platform product of Oracle Commerce (component: Dynamo Application Framework).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Platform.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Platform accessible data as well as  unauthorized access to critical data or complete access to all Oracle Commerce Platform accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61113

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:42.593 |

Vulnerability in the Oracle Application Object Library product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Application Object Library.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Application Object Library accessible data as well as  unauthorized access to critical data or complete access to all Oracle Application Object Library accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60827

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:20.670 |

Vulnerability in the Oracle iSupport product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle iSupport.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle iSupport, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle iSupport accessible data. CVSS 3.1 Base Score 7.4 (Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N).

### CVE-2026-60823

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:20.227 |

Vulnerability in the Oracle iSupport product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle iSupport.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle iSupport accessible data as well as  unauthorized access to critical data or complete access to all Oracle iSupport accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60725

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:12.617 |

Vulnerability in the MySQL Router product of Oracle MySQL (component: Router: General).  Supported versions that are affected are 8.4.0-8.4.10 and  9.7.0-9.7.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise MySQL Router.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all MySQL Router accessible data as well as  unauthorized access to critical data or complete access to all MySQL Router accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60667

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:07.620 |

Vulnerability in the PeopleSoft Enterprise HCM Human Resources product of Oracle PeopleSoft (component: Core).   The supported version that is affected is 9.2. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TCP to compromise PeopleSoft Enterprise HCM Human Resources.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise HCM Human Resources accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of PeopleSoft Enterprise HCM Human Resources. CVSS 3.1 Base Score 7.4 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-60317

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:34.510 |

Vulnerability in the MySQL Connectors product of Oracle MySQL (component: Connector/Net).  Supported versions that are affected are 9.7.0-9.7.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise MySQL Connectors.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all MySQL Connectors accessible data as well as  unauthorized access to critical data or complete access to all MySQL Connectors accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60179

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:18.847 |

Vulnerability in the MySQL Connectors product of Oracle MySQL (component: Connector/C++).  Supported versions that are affected are 9.7.0-9.7.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise MySQL Connectors.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all MySQL Connectors accessible data as well as  unauthorized access to critical data or complete access to all MySQL Connectors accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-47058

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:11.600 |

Vulnerability in Oracle Java SE (component: Scripting).  Supported versions that are affected are Oracle Java SE: 8u491, 8u491-perf and  11.0.31. Difficult to exploit vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise Oracle Java SE.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Java SE accessible data as well as  unauthorized access to critical data or complete access to all Oracle Java SE accessible data. Note: This vulnerability can be exploited by using APIs in the specified Component, e.g., through a web service which supplies data to the APIs. This vulnerability also applies to Java deployments, typically in clients running sandboxed Java Web Start applications or sandboxed Java applets, that load and run untrusted code (e.g., code that comes from the internet) and rely on the Java sandbox for security. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-47050

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:R/S:C/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:10.677 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.8. Easily exploitable vulnerability allows high privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle VM VirtualBox accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.4 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:H/UI:R/S:C/C:N/I:H/A:H).

### CVE-2026-47026

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:08.137 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: OpenSearch Dashboards).  Supported versions that are affected are 8.61 and 8.62. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in PeopleSoft Enterprise PeopleTools, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PeopleTools accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N).

### CVE-2026-46943

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:02.397 |

Vulnerability in the Oracle Retail EFTLink product of Oracle Retail Applications (component: Core/Plugin).  Supported versions that are affected are 21.0.0-25.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Retail EFTLink.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Retail EFTLink accessible data as well as  unauthorized access to critical data or complete access to all Oracle Retail EFTLink accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61271

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:57.477 |

Vulnerability in the Oracle Document Management and Collaboration product of Oracle E-Business Suite (component: Attachments).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Document Management and Collaboration.  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Oracle Document Management and Collaboration accessible data as well as  unauthorized read access to a subset of Oracle Document Management and Collaboration accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Document Management and Collaboration. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L).

### CVE-2026-61267

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:57.247 |

Vulnerability in the Oracle HCM Configuration Workbench product of Oracle E-Business Suite (component: Spreadsheet Loading).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle HCM Configuration Workbench.  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Oracle HCM Configuration Workbench accessible data as well as  unauthorized read access to a subset of Oracle HCM Configuration Workbench accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle HCM Configuration Workbench. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L).

### CVE-2026-61136

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:44.960 |

Vulnerability in the Oracle Commerce Platform product of Oracle Commerce (component: Dynamo Application Framework).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Platform.  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Oracle Commerce Platform accessible data as well as  unauthorized read access to a subset of Oracle Commerce Platform accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Commerce Platform. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L).

### CVE-2026-60945

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:29.263 |

Vulnerability in the Oracle Learning Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Learning Management.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Learning Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Learning Management accessible data. CVSS 3.1 Base Score 7.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N).

### CVE-2026-60143

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:14.940 |

Vulnerability in the Oracle Workflow product of Oracle E-Business Suite (component: Workflow Notification Mailer).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Workflow.  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Oracle Workflow accessible data as well as  unauthorized read access to a subset of Oracle Workflow accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Workflow. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L).

### CVE-2026-47007

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:06.143 |

Vulnerability in the Oracle Communications Pricing Design Center product of Oracle Communications (component: On-premise Deployment).  Supported versions that are affected are 15.0.0.0.0, 15.0.1.0.0, 15.1.0.0.0 and  15.2.0.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Communications Pricing Design Center executes to compromise Oracle Communications Pricing Design Center.  While the vulnerability is in Oracle Communications Pricing Design Center, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Communications Pricing Design Center accessible data as well as  unauthorized update, insert or delete access to some of Oracle Communications Pricing Design Center accessible data. CVSS 3.1 Base Score 7.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-46990

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:04.173 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Enterprise Config Management).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Oracle Enterprise Manager Base Platform accessible data as well as  unauthorized read access to a subset of Oracle Enterprise Manager Base Platform accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L).

### CVE-2026-47687

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-21T21:16:50.680 |

FOG is a free open-source cloning/imaging/rescue suite/inventory management system. Prior to versions 1.5.10.1832 and 1.6.0-beta.2313, the `selectForm()` helper in `fogpage.class.php` renders `<option>` labels using raw, unescaped user input. An unauthenticated attacker who knows any registered host's MAC address can POST a malicious `sysproduct` value to `/service/inventory.php`, which is stored in the database. When an administrator opens Reports > Inventory, the payload breaks out of the `<option>` element and executes arbitrary JavaScript in the admin's browser. Versions 1.5.10.1832 and 1.6.0-beta.2313 fix the issue.

### CVE-2026-47685

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-21T21:16:50.543 |

FOG is a free open-source cloning/imaging/rescue suite/inventory management system. Prior to versions 1.5.10.1832 and 1.6.0-beta.2313, the unauthenticated inventory service endpoint (`/service/inventory.php`) persists client-supplied values without sanitization, and the Host Management Inventory page renders all static inventory fields into HTML without output encoding, allowing stored cross-site scripting that executes in any administrator's browser. Versions 1.5.10.1832 and 1.6.0-beta.2313 fix the issue.

### CVE-2026-55081

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-21T19:17:10.950 |

DHIS2 is a flexible information system for data capture, management, validation, analytics and visualization. The DHIS2 OpenAPI HTML endpoint reflected values from the `scope` query parameter into the generated HTML document without sufficient sanitization. A crafted `scope` value could be rendered as active HTML or JavaScript in the OpenAPI documentation page. An attacker able to get a user to open a crafted OpenAPI HTML URL could execute JavaScript in that user's browser in the DHIS2 origin.

Affected versions: DHIS2 2.42 and 2.43 before the 2026-06-09 security patch releases, and the development branch for DHIS2 2.44 before the fix was merged.
Patched in 2.42.5.1, 2.43.0.1, the 2.42 and 2.43 line branches, and the 2.44 development branch.

### CVE-2026-15793

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-07-21T17:17:05.220 |

BuildKit custom frontends or clients using the raw low-level API can set git.checkoutbundle=true when checking out Git sources. If the Git source is malicious, this could lead to a crafted command invocation on the host.

### CVE-2026-65015

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-22T12:18:18.587 |

n8n versions before 2.30.1 contain a privilege escalation vulnerability in the AI Agents feature where the node-execution tool lacks proper authorization checks. A Project Viewer user can escalate privileges by chatting with an agent that has node tools enabled, executing arbitrary nodes and accessing credential secrets without proper authorization verification.

### CVE-2026-61391

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-22T12:18:18.247 |

There is a stack-based buffer overflow vulnerability in some Hikvision cameras, which may allow authenticated attackers to cause device malfunction by sending specially crafted packets.

### CVE-2026-62548

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-21T22:19:08.433 |

Vulnerability in the Oracle HRMS (US) product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle HRMS (US).  Successful attacks of this vulnerability can result in takeover of Oracle HRMS (US). CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62466

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:03.103 |

Vulnerability in the Oracle Human Resources product of Oracle E-Business Suite (component: Data Removal Tool).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Human Resources.  Successful attacks of this vulnerability can result in takeover of Oracle Human Resources. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61336

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:01.700 |

Vulnerability in the Oracle Lease and Finance Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.14-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Lease and Finance Management.  Successful attacks of this vulnerability can result in takeover of Oracle Lease and Finance Management. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61314

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:00.090 |

Vulnerability in the Oracle EDI Gateway product of Oracle E-Business Suite (component: All Miscellaneous EDI Issues).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle EDI Gateway.  Successful attacks of this vulnerability can result in takeover of Oracle EDI Gateway. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61285

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:58.520 |

Vulnerability in the Oracle Process Manufacturing Systems product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.11-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Systems.  Successful attacks of this vulnerability can result in takeover of Oracle Process Manufacturing Systems. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61115

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:42.810 |

Vulnerability in the Oracle Order Management product of Oracle E-Business Suite (component: Product Diagnostic Tools).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Order Management.  Successful attacks of this vulnerability can result in takeover of Oracle Order Management. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61107

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:41.900 |

Vulnerability in the Oracle Applications DBA product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Applications DBA.  Successful attacks of this vulnerability can result in takeover of Oracle Applications DBA. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61094

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:40.443 |

Vulnerability in the MySQL Server, MySQL Cluster product of Oracle MySQL (component: Server: Replication).  Supported versions that are affected are MySQL Server: 8.4.0-8.4.10, 9.7.0-9.7.1; MySQL Cluster: 8.0.0-8.0.47, 8.4.0-8.4.10 and  9.7.0-9.7.1. Easily exploitable vulnerability allows high privileged attacker with network access via multiple protocols to compromise MySQL Server, MySQL Cluster.  Successful attacks of this vulnerability can result in takeover of MySQL Server, MySQL Cluster. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61068

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:37.533 |

Vulnerability in the PeopleSoft Enterprise FIN Billing Argentina product of Oracle PeopleSoft (component: Billing).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Billing Argentina.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise FIN Billing Argentina. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61039

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:34.937 |

Vulnerability in the Oracle Advanced Supply Chain Planning product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Advanced Supply Chain Planning.  Successful attacks of this vulnerability can result in takeover of Oracle Advanced Supply Chain Planning. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61035

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:34.607 |

Vulnerability in the Oracle Financials for the Americas product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Financials for the Americas.  Successful attacks of this vulnerability can result in takeover of Oracle Financials for the Americas. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61027

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:34.150 |

Vulnerability in the Oracle Cost Management product of Oracle E-Business Suite (component: Inventory Costing).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Cost Management.  Successful attacks of this vulnerability can result in takeover of Oracle Cost Management. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61025

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:33.920 |

Vulnerability in the Oracle iRecruitment product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle iRecruitment.  Successful attacks of this vulnerability can result in takeover of Oracle iRecruitment. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61006

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:32.680 |

Vulnerability in the Oracle Process Manufacturing Logistics product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Logistics.  Successful attacks of this vulnerability can result in takeover of Oracle Process Manufacturing Logistics. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60926

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:27.687 |

Vulnerability in the Oracle Public Sector Payroll product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Public Sector Payroll.  Successful attacks of this vulnerability can result in takeover of Oracle Public Sector Payroll. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60925

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:27.577 |

Vulnerability in the Oracle Public Sector Payroll product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.4-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Public Sector Payroll.  Successful attacks of this vulnerability can result in takeover of Oracle Public Sector Payroll. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60918

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:26.923 |

Vulnerability in the Oracle Shipping Execution product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.12-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Shipping Execution.  Successful attacks of this vulnerability can result in takeover of Oracle Shipping Execution. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60910

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:26.347 |

Vulnerability in the Oracle Property Manager product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Property Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Property Manager. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60900

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:25.797 |

Vulnerability in the Oracle HCM Configuration Workbench product of Oracle E-Business Suite (component: Rapid Implementation).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle HCM Configuration Workbench.  Successful attacks of this vulnerability can result in takeover of Oracle HCM Configuration Workbench. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60845

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:22.307 |

Vulnerability in the Oracle Mobile Application Server product of Oracle E-Business Suite (component: MWA General Bugs).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Mobile Application Server.  Successful attacks of this vulnerability can result in takeover of Oracle Mobile Application Server. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60836

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:21.533 |

Vulnerability in the Oracle HCM Common Architecture product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle HCM Common Architecture.  Successful attacks of this vulnerability can result in takeover of Oracle HCM Common Architecture. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60828

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:20.780 |

Vulnerability in the Oracle Interaction Blending product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Interaction Blending.  Successful attacks of this vulnerability can result in takeover of Oracle Interaction Blending. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60813

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:19.780 |

Vulnerability in the Oracle iStore product of Oracle E-Business Suite (component: Shopping Cart).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle iStore.  Successful attacks of this vulnerability can result in takeover of Oracle iStore. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60787

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:17.733 |

Vulnerability in the Oracle Receivables product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Receivables.  Successful attacks of this vulnerability can result in takeover of Oracle Receivables. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60786

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:17.617 |

Vulnerability in the Oracle Receivables product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Receivables.  Successful attacks of this vulnerability can result in takeover of Oracle Receivables. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60755

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:15.153 |

Vulnerability in the Oracle Assets product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Assets.  Successful attacks of this vulnerability can result in takeover of Oracle Assets. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60734

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:13.867 |

Vulnerability in the Oracle Trading Community product of Oracle E-Business Suite (component: Party Search UI).  Supported versions that are affected are 12.2.3-12.2.12. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Trading Community.  Successful attacks of this vulnerability can result in takeover of Oracle Trading Community. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60645

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:05.303 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Web Content Management).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60576

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:57.917 |

Vulnerability in the Oracle Enterprise Command Center Framework product of Oracle E-Business Suite (component: Core).   The supported version that is affected is V16. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Enterprise Command Center Framework.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Command Center Framework. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60546

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:54.507 |

Vulnerability in the Oracle SOA Suite product of Oracle Fusion Middleware (component: Integration Business Insight).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle SOA Suite.  Successful attacks of this vulnerability can result in takeover of Oracle SOA Suite. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60529

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:52.623 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Console).  Supported versions that are affected are 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60519

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:51.490 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows high privileged attacker with network access via LDAP to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Unified Directory. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60502

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:51.253 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via T3, IIOP to compromise WebCenter Content: Imaging.  Successful attacks of this vulnerability can result in takeover of WebCenter Content: Imaging. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60466

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:49.080 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise WebCenter Content: Imaging.  Successful attacks of this vulnerability can result in takeover of WebCenter Content: Imaging. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60418

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:44.090 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows high privileged attacker with network access via LDAP to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Unified Directory. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60396

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:42.053 |

Vulnerability in Oracle GoldenGate (component: Distribution Server executable).  Supported versions that are affected are 21.3-21.21 and  23.4-23.26.1. Easily exploitable vulnerability allows high privileged attacker with network access via HTTPS to compromise Oracle GoldenGate.  Successful attacks of this vulnerability can result in takeover of Oracle GoldenGate. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60345

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:37.577 |

Vulnerability in the Oracle JDeveloper product of Oracle Fusion Middleware (component: ADF Shared Components).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle JDeveloper.  Successful attacks of this vulnerability can result in takeover of Oracle JDeveloper. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60340

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:37.137 |

Vulnerability in the Oracle Project Costing product of Oracle E-Business Suite (component: Enterprise Command Center).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Project Costing.  Successful attacks of this vulnerability can result in takeover of Oracle Project Costing. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60335

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:36.587 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60316

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:34.400 |

Vulnerability in the MySQL Server, MySQL Cluster product of Oracle MySQL (component: Server: X Plugin).  Supported versions that are affected are MySQL Server: 8.4.0-8.4.10, 9.7.0-9.7.1; MySQL Cluster: 8.0.0-8.0.47, 8.4.0-8.4.10 and  9.7.0-9.7.1. Easily exploitable vulnerability allows high privileged attacker with network access via multiple protocols to compromise MySQL Server, MySQL Cluster.  Successful attacks of this vulnerability can result in takeover of MySQL Server, MySQL Cluster. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60245

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:26.377 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Coherence executes to compromise Oracle Coherence.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Coherence, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Coherence accessible data as well as  unauthorized access to critical data or complete access to all Oracle Coherence accessible data. CVSS 3.1 Base Score 7.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-60153

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:15.873 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Console).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTPS to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-47006

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:06.027 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Self Update Framework).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows high privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-47005

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:05.913 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Self Update Framework).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows high privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46988

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:03.923 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Connector Framework).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows high privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46981

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:03.123 |

Vulnerability in the Oracle Utilities Network Management System product of Oracle Utilities Applications (component: Mobile).  Supported versions that are affected are 2.5.0.1.0-2.5.0.1.17, 2.5.0.2.0-2.5.0.2.11, 2.6.0.1.0-2.6.0.1.12, 2.6.0.2.0-2.6.0.2.8 and  25.12.0.0.0-25.12.0.0.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Utilities Network Management System.  While the vulnerability is in Oracle Utilities Network Management System, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Oracle Utilities Network Management System accessible data as well as  unauthorized read access to a subset of Oracle Utilities Network Management System accessible data. CVSS 3.1 Base Score 7.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N).

### CVE-2026-46954

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:02.647 |

Vulnerability in the Oracle Human Resources product of Oracle E-Business Suite (component: Data Removal Tool).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Human Resources.  Successful attacks of this vulnerability can result in takeover of Oracle Human Resources. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-44879

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T21:16:49.750 |

A vulnerability in the command line interface of ECOS devices could allow a highly privileged, authenticated remote attacker to perform command injection on certain CLI commands. Successful exploitation could allow an attacker to execute arbitrary commands on the underlying operating system.

### CVE-2026-44878

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T21:16:49.640 |

A vulnerability in the web-based management interface of an ECOS device could allow a highly privileged, authenticated remote attacker to access the device's filesystem. Successful exploitation of this vulnerability could allow an attacker to access sensitive files and tamper with or delete system data.

### CVE-2026-63454

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T19:17:12.467 |

An authenticated path traversal vulnerability exists in AOS-CX. Successful exploitation of this vulnerability allows an attacker to copy arbitrary files to a user readable location from the command line interface of the underlying operating system, which could lead to remote code execution.

### CVE-2026-63453

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T19:17:12.357 |

Buffer overflow vulnerabilities exist in the command line interface of AOS-CX. Successful exploitation of these vulnerabilities could allow a remote high-privileged user to execute arbitrary code as a privileged user on the underlying operating system.

### CVE-2026-46681

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-07-21T15:16:35.177 |

@nevware21/ts-utils is a comprehensive TypeScript/JavaScript utility library. Prior to version 0.14.0, the _copyProps function in lib/src/object/copy.ts uses for...in to iterate over source object properties without an Object.hasOwnProperty check, and does not filter dangerous keys (__proto__, constructor, prototype). This allows an attacker to pollute the prototype chain of all objects in the application. Version 0.14.0 patches the issue.

### CVE-2026-65316

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-21T22:19:10.197 |

XXL-Job version 2.4.2 contains an insecure direct object reference vulnerability that allows authenticated users to read execution log content from job groups they are not authorized to access by supplying arbitrary sequential log IDs to the logDetailCat endpoint. Attackers can enumerate log records across all job groups by calling the logDetailCat endpoint with incremented logId parameter values, bypassing the permission check present in the sibling logDetailPage endpoint, and retrieve sensitive log content from restricted job groups.

### CVE-2026-62565

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-200;CWE-269;CWE-284` |
| Published | 2026-07-21T22:19:09.440 |

Vulnerability in the Oracle HRMS (US) product of Oracle E-Business Suite (component: US Payroll Year End).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle HRMS (US).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle HRMS (US) accessible data as well as  unauthorized update, insert or delete access to some of Oracle HRMS (US) accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-62557

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-21T22:19:08.763 |

Vulnerability in the Oracle HRMS (UK) product of Oracle E-Business Suite (component: UK Payroll).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle HRMS (UK).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle HRMS (UK) accessible data as well as  unauthorized update, insert or delete access to some of Oracle HRMS (UK) accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-62469

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:03.330 |

Vulnerability in the Oracle Human Resources product of Oracle E-Business Suite (component: Enterprise Command Center).  Supported versions that are affected are 12.2.14-12.2.15. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Human Resources executes to compromise Oracle Human Resources.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Human Resources accessible data as well as  unauthorized access to critical data or complete access to all Oracle Human Resources accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62443

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:02.043 |

Vulnerability in the Oracle Contracts Integration product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Contracts Integration.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Contracts Integration accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Contracts Integration. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L).

### CVE-2026-61334

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:19:01.467 |

Vulnerability in the Oracle Price Protection product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Price Protection.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Price Protection accessible data as well as  unauthorized read access to a subset of Oracle Price Protection accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N).

### CVE-2026-61299

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:59.200 |

Vulnerability in the Oracle Process Manufacturing Logistics product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Logistics.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Process Manufacturing Logistics accessible data as well as  unauthorized update, insert or delete access to some of Oracle Process Manufacturing Logistics accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-61165

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:48.140 |

Vulnerability in the Oracle Commerce Guided Search Platform Services product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search Platform Services.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Commerce Guided Search Platform Services and  unauthorized read access to a subset of Oracle Commerce Guided Search Platform Services accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:H).

### CVE-2026-61162

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:47.793 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Commerce Guided Search / Oracle Commerce Experience Manager executes to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61151

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:46.547 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-61119

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:43.153 |

Vulnerability in the Oracle HRMS (UK) product of Oracle E-Business Suite (component: UK Payroll).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle HRMS (UK).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle HRMS (UK) accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle HRMS (UK). CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L).

### CVE-2026-61095

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:40.557 |

Vulnerability in the Oracle Communications Unified Inventory Management product of Oracle Communications (component: Security).  Supported versions that are affected are 7.5.0, 7.5.1, 7.6.0, 7.7.0, 7.8.0 and  8.0.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Communications Unified Inventory Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Communications Unified Inventory Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Communications Unified Inventory Management accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-61049

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:35.730 |

Vulnerability in the Oracle Production Scheduling product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Production Scheduling executes to compromise Oracle Production Scheduling.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Production Scheduling. CVSS 3.1 Base Score 7.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-61012

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:33.020 |

Vulnerability in the Oracle Time and Labor product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Time and Labor.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Time and Labor accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Time and Labor. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L).

### CVE-2026-60987

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:31.797 |

Vulnerability in the Oracle Project Portfolio Analysis product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Project Portfolio Analysis.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Project Portfolio Analysis accessible data as well as  unauthorized read access to a subset of Oracle Project Portfolio Analysis accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N).

### CVE-2026-60985

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:31.547 |

Vulnerability in the Oracle Project Portfolio Analysis product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Project Portfolio Analysis.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Project Portfolio Analysis accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Project Portfolio Analysis. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L).

### CVE-2026-60984

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:31.440 |

Vulnerability in the Oracle Project Portfolio Analysis product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Project Portfolio Analysis.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Project Portfolio Analysis accessible data as well as  unauthorized read access to a subset of Oracle Project Portfolio Analysis accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N).

### CVE-2026-60908

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:26.233 |

Vulnerability in the Oracle Installed Base product of Oracle E-Business Suite (component: Create Item Instance).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Installed Base.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Installed Base accessible data as well as  unauthorized update, insert or delete access to some of Oracle Installed Base accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60870

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:23.910 |

Vulnerability in the Oracle Advanced Pricing product of Oracle E-Business Suite (component: Pricing Installation).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Advanced Pricing.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Advanced Pricing accessible data as well as  unauthorized update, insert or delete access to some of Oracle Advanced Pricing accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60868

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:23.800 |

Vulnerability in the Oracle Advanced Pricing product of Oracle E-Business Suite (component: Pricing Installation).  Supported versions that are affected are 12.2.14-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Advanced Pricing.  While the vulnerability is in Oracle Advanced Pricing, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Advanced Pricing accessible data as well as  unauthorized update, insert or delete access to some of Oracle Advanced Pricing accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-60838

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:21.760 |

Vulnerability in the Oracle Price Protection product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Price Protection.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Price Protection accessible data as well as  unauthorized read access to a subset of Oracle Price Protection accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N).

### CVE-2026-60834

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:21.237 |

Vulnerability in the Oracle Solaris product of Oracle Systems (component: Utility).   The supported version that is affected is 11.4. Difficult to exploit vulnerability allows low privileged attacker with network access via RAD to compromise Oracle Solaris.  While the vulnerability is in Oracle Solaris, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Solaris accessible data as well as  unauthorized update, insert or delete access to some of Oracle Solaris accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-60800

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:18.650 |

Vulnerability in the Oracle Compensation Workbench product of Oracle E-Business Suite (component: Compensation Workbench).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Compensation Workbench.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Compensation Workbench accessible data as well as  unauthorized update, insert or delete access to some of Oracle Compensation Workbench accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60799

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:18.533 |

Vulnerability in the Oracle Compensation Workbench product of Oracle E-Business Suite (component: Compensation Workbench).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Compensation Workbench.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Compensation Workbench accessible data as well as  unauthorized update, insert or delete access to some of Oracle Compensation Workbench accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60774

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:16.560 |

Vulnerability in the Oracle Applications Framework product of Oracle E-Business Suite (component: Search Bean [Incl.  Advanced]).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Applications Framework.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Applications Framework accessible data as well as  unauthorized update, insert or delete access to some of Oracle Applications Framework accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60772

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:16.327 |

Vulnerability in the Oracle Financials Common Modules product of Oracle E-Business Suite (component: Common Components).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Financials Common Modules.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Financials Common Modules accessible data as well as  unauthorized read access to a subset of Oracle Financials Common Modules accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N).

### CVE-2026-60739

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:14.347 |

Vulnerability in the Oracle Field Service product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Field Service.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Field Service accessible data as well as  unauthorized update, insert or delete access to some of Oracle Field Service accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60703

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:10.713 |

Vulnerability in the Oracle Interaction Blending product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Interaction Blending executes to compromise Oracle Interaction Blending.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Interaction Blending accessible data as well as  unauthorized access to critical data or complete access to all Oracle Interaction Blending accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60659

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:06.923 |

Vulnerability in the Oracle Solaris product of Oracle Systems (component: Filesystems).   The supported version that is affected is 11.4. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Solaris executes to compromise Oracle Solaris.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Solaris accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Solaris. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-60647

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:05.533 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Web Content Management).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle WebCenter Content. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-60623

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:02.830 |

Vulnerability in the MySQL Connectors product of Oracle MySQL (component: Connector/J).  Supported versions that are affected are 9.7.0-9.7.1. Difficult to exploit vulnerability allows low privileged attacker with network access via multiple protocols to compromise MySQL Connectors.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all MySQL Connectors accessible data as well as  unauthorized access to critical data or complete access to all MySQL Connectors accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of MySQL Connectors. CVSS 3.1 Base Score 7.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-60614

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:01.793 |

Vulnerability in the PeopleSoft Enterprise CS Campus Community product of Oracle PeopleSoft (component: Person Data).   The supported version that is affected is 9.2.38. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise CS Campus Community.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise CS Campus Community accessible data as well as  unauthorized read access to a subset of PeopleSoft Enterprise CS Campus Community accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of PeopleSoft Enterprise CS Campus Community. CVSS 3.1 Base Score 7.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:H/A:H).

### CVE-2026-60577

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:58.030 |

Vulnerability in the Oracle Enterprise Command Center Framework product of Oracle E-Business Suite (component: Core).   The supported version that is affected is V16. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Enterprise Command Center Framework.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Enterprise Command Center Framework accessible data as well as  unauthorized update, insert or delete access to some of Oracle Enterprise Command Center Framework accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60527

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:52.400 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Console).  Supported versions that are affected are 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle WebLogic Server executes to compromise Oracle WebLogic Server.  While the vulnerability is in Oracle WebLogic Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebLogic Server accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60492

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:50.210 |

Vulnerability in the JD Edwards EnterpriseOne HCM Foundation product of Oracle JD Edwards (component: OW HR PR Foundation).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise JD Edwards EnterpriseOne HCM Foundation.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of JD Edwards EnterpriseOne HCM Foundation and  unauthorized read access to a subset of JD Edwards EnterpriseOne HCM Foundation accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:H).

### CVE-2026-60468

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:49.300 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise WebCenter Content: Imaging.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all WebCenter Content: Imaging accessible data as well as  unauthorized update, insert or delete access to some of WebCenter Content: Imaging accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60451

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:47.637 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise WebCenter Content: Imaging.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all WebCenter Content: Imaging accessible data as well as  unauthorized update, insert or delete access to some of WebCenter Content: Imaging accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60449

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:47.417 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle WebCenter Content executes to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60305

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:33.153 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via TCP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Coherence accessible data as well as  unauthorized read access to a subset of Oracle Coherence accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N).

### CVE-2026-60176

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:18.513 |

Vulnerability in the Oracle Payments product of Oracle E-Business Suite (component: File Transmission).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Payments.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Payments accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Payments. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-47015

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:07.097 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: PIA Core Technology).   The supported version that is affected is 8.62. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in PeopleSoft Enterprise PeopleTools, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of PeopleSoft Enterprise PeopleTools accessible data as well as  unauthorized read access to a subset of PeopleSoft Enterprise PeopleTools accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 7.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L).

### CVE-2026-46996

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:04.897 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Metadata Plugin).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Enterprise Manager Base Platform accessible data as well as  unauthorized read access to a subset of Oracle Enterprise Manager Base Platform accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N).

### CVE-2026-63080

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-21T21:16:52.567 |

Aptabase through commit 5a89368 contains a SQL injection vulnerability in the ClickHouse query backend that allows authenticated attackers to read event data across all tenants by injecting unsanitized filter parameters into Liquid SQL templates. Attackers can supply malicious values through EventName, CountryCode, OsName, DeviceModel, AppVersion, or SessionId parameters to inject a UNION ALL statement that bypasses the app_id tenant isolation filter across thirteen of the fifteen stats API endpoints.

### CVE-2026-56147

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-21T21:16:52.433 |

Authorization Bypass Through User-Controlled Key (CWE-639) in Kibana can lead to unauthorized information disclosure and case attachment integrity compromise via Privilege Abuse (CAPEC-122). An inconsistency in Kibana's file access authorization logic allows a low-privileged authenticated user to retrieve, modify, and delete case attachments that belong to feature areas they are not authorized to access. Because the access control check and the resource retrieval use different resolution mechanisms, an authenticated attacker with limited file management permissions can obtain the contents of, modify, or delete protected case attachments — such as those associated with Security Solution cases — without holding the privileges required to access those features.

### CVE-2026-47697

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-21T21:16:51.340 |

Shelf is a platform for tracking physical assets. Shelf is multi-tenant; data is isolated per organization (workspace). Prior to version 1.20.2, several endpoints accepted entity IDs from request input and `connect`-ed / read / updated them without verifying the IDs belonged to the caller's organization. An authenticated user in Org A who knew or obtained an ID belonging to Org B could act on Org B's data across organization boundaries (a cross-tenant IDOR). A loader-only restriction on personal-workspace bookings was also bypassable via a crafted POST. Version 1.20.2 patches the issue. No known workarounds are available.

### CVE-2026-47695

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-21T21:16:51.210 |

CC: Tweaked is a mod for Minecraft which adds programmable computers, turtles, and more to the game. Prior to version 1.119.0, CC-Tweaked's HTTP API (`http.request`, `http.websocket`) blocks requests to private network ranges to prevent server-side request forgery (SSRF). This protection can be bypassed on IPv6-capable servers using NAT64 well-known prefix addresses (`64:ff9b::/96`). An attacker who can execute Lua code can reach any internal IPv4 service that the filter is intended to block, by addressing it as `http://[64:ff9b::<ipv4-as-hex>]/` instead of its direct IPv4 address. This affects any CC-Tweaked deployment on a network with NAT64 routing — a configuration that is standard on AWS, GCP, and other cloud platforms when using IPv6-only subnets. Version 1.119.0 fixes the issue.

### CVE-2026-64880

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-21T20:17:04.900 |

Unsanitized user-supplied input in report filtering parameters is concatenated directly into SQL queries without proper escaping or parameterized queries, enabling blind SQL injection and unauthorized database read access.

### CVE-2026-47657

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-21T18:17:01.277 |

HumHub is an Open Source Enterprise Social Network. In versions 1.13.0 through 1.18.2, a missing authorization check in the Space member management controller allowed any authenticated user to trigger the removal of all members from any Space, regardless of their own role or membership in that Space. Versions 1.13.0 through 1.18.2 are affected. The vulnerability has been patched in version 1.18.3, and all users are encouraged to upgrade to this version or later immediately. No known workaround is available.

### CVE-2026-21577

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T18:16:57.327 |

This High severity DoS (Denial of Service) vulnerability was introduced in versions 9.0.1, 9.1.0, 9.2.0, 9.3.1, 9.4.0, 9.5.1, 10.0.2, 10.1.0 and 10.2.0 of Confluence Data Center.

This DoS (Denial of Service) vulnerability, with a CVSS Score of 7.1, allows an authenticated attacker to cause a resource to be unavailable for its intended users by temporarily or indefinitely disrupting services of a host connected to a network.

Atlassian recommends that Confluence Data Center customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
 Confluence Data Center 9.2: Upgrade to a release greater than or equal to 9.2.17

 Confluence Data Center 10.2: Upgrade to a release greater than or equal to 10.2.7

See the release notes ([https://confluence.atlassian.com/doc/confluence-release-notes-327.html]). You can download the latest version of Confluence Data Center from the download center ([https://www.atlassian.com/software/confluence/download-archives]).

This vulnerability was reported via our Penetration Testing program.

### CVE-2026-21575

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T18:16:57.170 |

This High severity RCE (Remote Code Execution) vulnerability was introduced in version 3.4.11 of Sourcetree for Mac and Sourcetree for Windows. 
	
	This RCE (Remote Code Execution) vulnerability, with a CVSS Score of 7.1, allows an authenticated attacker to execute arbitrary code which has high impact to confidentiality, high impact to integrity, high impact to availability, and requires user interaction. 
	
	Atlassian recommends that Sourcetree for Mac and Sourcetree for Windows customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
		
		* Sourcetree for Mac and Sourcetree for Windows 3.4: Upgrade to a release greater than or equal to 3.4.13
		
		
	
	See the release notes (https://www.sourcetreeapp.com/download-archives). You can download the latest version of Sourcetree for Mac and Sourcetree for Windows from the download center (https://www.sourcetreeapp.com/download-archives). 
	
	This vulnerability was reported via our Bug Bounty program.

### CVE-2026-47397

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-21T17:17:08.670 |

PraisonAI is a multi-agent teams system. Prior to version 4.6.40, hidden metadata in a webpage causes PraisonAI agents to write attacker-controlled content to arbitrary paths. `write_file` skips path validation when `workspace=None` (always `None` in production). Version 4.6.40 fixes the issue.

### CVE-2026-65050

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-21T15:16:39.147 |

Ninja Forms WordPress plugin version 3.14.8 and prior contains a missing authorization vulnerability in the render callback of the `ninja-forms/submissions-table` Gutenberg block that allows authenticated attackers with Author-level privileges to expose stored form submissions to unauthenticated visitors by embedding the block with an arbitrary formID on a published post. Attackers can retrieve the signed bearer token injected into every page visitor's browser via `wp_localize_script` and use it against the REST API submissions endpoint to access all saved form submission field values, including sensitive personally identifiable information such as names, email addresses, and phone numbers.

### CVE-2026-61120

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:43.263 |

Vulnerability in the Oracle HRMS (US) product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle HRMS (US) executes to compromise Oracle HRMS (US).  Successful attacks of this vulnerability can result in takeover of Oracle HRMS (US). CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61061

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:36.843 |

Vulnerability in the Oracle JDeveloper product of Oracle Fusion Middleware (component: Security Framework).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle JDeveloper executes to compromise Oracle JDeveloper.  Successful attacks of this vulnerability can result in takeover of Oracle JDeveloper. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60833

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:21.120 |

Vulnerability in the Oracle Solaris product of Oracle Systems (component: Utility).   The supported version that is affected is 11.4. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Solaris executes to compromise Oracle Solaris.  Successful attacks of this vulnerability can result in takeover of Oracle Solaris. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60705

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:18:10.940 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.5. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data as well as  unauthorized update, insert or delete access to some of Siebel CRM Cloud Applications accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-60494

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:50.437 |

Vulnerability in the JD Edwards EnterpriseOne General Ledger product of Oracle JD Edwards (component: E1 Foundation).   The supported version that is affected is 9.2. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise JD Edwards EnterpriseOne General Ledger.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of JD Edwards EnterpriseOne General Ledger as well as  unauthorized update, insert or delete access to some of JD Edwards EnterpriseOne General Ledger accessible data and  unauthorized read access to a subset of JD Edwards EnterpriseOne General Ledger accessible data. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H).

### CVE-2026-46999

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-21T22:17:05.237 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Discovery Framework).  Supported versions that are affected are 13.5 and  24.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Enterprise Manager Base Platform accessible data as well as  unauthorized read access to a subset of Oracle Enterprise Manager Base Platform accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:L).
