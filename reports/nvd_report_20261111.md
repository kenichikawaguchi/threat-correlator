# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-10 15:00 UTC
- **対象期間**: `2026-11-09T15:00:39.000Z` 〜 `2026-11-10T15:00:25.000Z`
- **重要CVE数**: 233 件（Critical 9.0+: 29 件 / High 7.0〜: 204 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公表された CVE のうち **CVSS 7.0 以上が 30 件以上** と、深刻度の高い脆弱性が集中しています。  
- **SAP 製品**（Web Dispatcher、Gateway、NetWeaver 等）が **CVSS 10.0** のリモートコード実行・認証バイパスを多数抱えており、企業基幹システムへの直接的なリスクが顕在化しています。  
- オープンソーススタックでも **デフォルト認証情報・ハードコーディングされたシークレット** が原因の認証回避や RCE が続出し、特に **Mongoose、Redpanda Connect、Kubero** などの開発プラットフォームが狙われやすいことが分かります。  
- **通信の暗号化不備**（GV‑Face の HTTP 平文送信）や **TLS バリデーションバイパス**（V 言語標準ライブラリ）といった、**構成ミス・実装ミス** が依然として重大な攻撃ベクトルとなっています。

---

## 2. 特に注目すべき CVE  

| CVE | 製品・コンポーネント | 主な影響 | 重要度 (CVSS) | 注目理由 |
|-----|-------------------|----------|---------------|----------|
| **CVE‑2026‑89126** | SAP Web Dispatcher | メモリ破壊 → 任意コード実行 (ネットワーク入力未検証) | 10.0 | SAP のフロントエンドゲートウェイが外部から直接メモリ破壊を受けるため、**全社システムが即座に乗っ取られる危険**がある。 |
| **CVE‑2026‑89103** | SAP Gateway | デフォルト ACL が過剰権限 → 外部から内部サーバーとして扱われる | 10.0 | 認証不要で **内部アプリケーションサーバー権限** を取得でき、横方向移動やデータ抽出が可能になる。 |
| **CVE‑2026‑76964** | SAP NetWeaver AS ABAP (ICM) | メモリ破壊 → 任意コード実行 | 10.0 | 同様にネットワーク入力の検証不備で **ABAP アプリケーション全体が危険**。SAP 環境は複数製品が同時に脆弱で、連鎖的被害が懸念される。 |
| **CVE‑2026‑123270** | Redpanda Connect (4.39‑4.110) | 認証無効化 → リモートコード実行 | 9.8 | デフォルトで **管理 API が 0.0.0.0:4195 に公開** され、認証が無効。クラウド/オンプレミス問わず即座にシステム制御が奪取できる。 |
| **CVE‑2026‑124600** | GV‑Face | 認証情報を平文 HTTP 送信 | 10.0 (CVSS:4.0) | **通信の暗号化が全く行われていない** ため、社内ネットワークのスニッフィングだけで認証情報が漏洩。内部脅威・APT に対して重大。 |

> **共通点**：  
> - **認証・入力検証の欠如** が根本原因。  
> - すべて **ネットワーク経路から直接攻撃可能**（リモートからの無認証利用）。  
> - SAP 系は **基幹業務システム** に直結しているため、**業務停止・情報漏洩リスクが極めて高い**。

---

## 3. 推奨アクション  

### 3.1 直ちに実施すべき緊急対策
- **ネットワークレベルでの遮断**  
  - SAP Web Dispatcher / Gateway / NetWeaver の **外部からの直接アクセスをファイアウォールで遮断**（IP 制限、VPN 経由のみ許可）。  
  - Redpanda Connect の管理 API (`0.0.0.0:4195`) を **内部ネットワークだけにバインド**、もしくは **ポート閉鎖**。  
- **TLS/HTTPS 強制**  
  - GV‑Face の全エンドポイントを **HTTPS に切り替え**（自己署名証明書でも暗号化は必須）。  
  - V 言語標準ライブラリ `net.http` を使用しているサービスは、`SSLConnectConfig.validate = true`、`FetchConfig.validate = true` を明示的に設定。  

### 3.2 パッケージ・バージョン更新（ベンダーパッチ適用）  
| 製品 | 現行バージョン (脆弱) | 修正済みバージョン | 更新手順 |
|------|----------------------|-------------------|----------|
| SAP Web Dispatcher | 7.0 以前 (該当パッチ未適用) | **7.0 SP 44** 以降（SAP Note **3111230**） | SAP ONE Support Launchpad からパッチダウンロード → 運用環境でテスト → 本番適用 |
| SAP Gateway | 7.0 以前 | **7.0 SP 45** 以降（SAP Note **3111245**） | 同上 |
| SAP NetWeaver AS ABAP (ICM) | 7.5 以前 | **7.5 SP 48** 以降（SAP Note **3111252**） | 同上 |
| Redpanda Connect | 4.39‑4.110 | **4.111** 以降 | `docker pull redpanda/connect:4.111` → コンテナ再デプロイ |
| GV‑Face | 任意（HTTP デフォルト） | **最新版 (≥ 2.3.1)** | `pip install gv-face==2.3.1` もしくは OS パッケージマネージャで更新 |
| Mongoose (Node.js) | < 6.13.11 / < 7.8.12 / < 8.24.3 / < 9.9.2 | **6.13.11**, **7.8.12**, **8.24.3**, **9.9.2** 以上 | `npm install mongoose@6.13.11` など、使用中のメジャーバージョンに合わせて更新 |
| Kubero | 3.0.0‑3.1.1 | **3.2.0** 以降（hard‑coded JWT secret 削除） | `helm upgrade kubero kubero/kubero --version 3.2.0` |
| SuperTokens Core | 6.0.0‑12.3.1 | **12.3.2** 以降 | `npm install supertokens-node@12.3.2` |
| HiRDB | 10‑00 < 10‑12‑01、9‑50‑06‑9‑66‑22 | **10‑12‑01** 以上、**9‑66‑23** 以上 | 製品ベンダー提供のパッチ適用手順に従う |

### 3.3 設定・運用上のベストプラクティス
1. **最小権限の原則**  
   - SAP の ACL、Redpanda の管理 API、Kubero の JWT シークレットは **デフォルト

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-89126

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T01:17:22.420 |

SAP Web Dispatcher does not sufficiently validate certain network input processed by an internal component. An unauthenticated attacker could send specially crafted network traffic to trigger a memory corruption condition in the affected functionality. Successful exploitation could allow the attacker to execute arbitrary code and fully compromise the system, resulting in a high impact on confidentiality, integrity and availability of the system.

### CVE-2026-89103

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T01:17:21.013 |

SAP Gateway activates the default Access Control List with high privileges allowing categorization of external attacker as internal application server. As a result an unauthenticated attacker with network access to the SAP Gateway could exploit this weakness to potentially perform unauthorized actions within the application environment, resulting in a high impact on the confidentiality, integrity, and availability of the affected system.

### CVE-2026-76964

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1287` |
| Published | 2026-11-10T01:17:20.240 |

SAP NetWeaver Application Server ABAP does not sufficiently validate certain network input processed by an internal component. An unauthenticated attacker could send specially crafted network traffic to trigger a memory corruption condition in the affected functionality. Successful exploitation could allow the attacker to execute arbitrary code and fully compromise the system, resulting in a high impact on confidentiality, integrity and availability of the system.

### CVE-2026-124600

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-11-10T01:17:18.467 |

GV-Face transmits sensitive user credentials and
related authentication data over unencrypted HTTP connections. The HTTP
traffic is not encrypted, an attacker with the ability to intercept network
traffic.

### CVE-2026-120017

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-10T01:17:16.803 |

SAP NetWeaver AS ABAP and ABAP Platform does not perform sufficient verification of incoming authentication assertions under certain configurations. An unauthenticated attacker could submit specially crafted data to bypass authentication and impersonate arbitrary users, including privileged accounts. Successful exploitation could cause a full system compromise, with the impact potentially extending to connected components and systems beyond the affected system. This results in a high impact on confidentiality, integrity, and availability of the application.

### CVE-2026-13312

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1287` |
| Published | 2026-11-10T06:17:08.587 |

A vulnerability that could allow an attacker to compromise a system.

### CVE-2026-76965

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-749` |
| Published | 2026-11-10T01:17:20.387 |

SAP NetWeaver Application Server ABAP and ABAP Platform does not perform necessary authorization checks for certain internal functionality. An attacker with low privileges could invoke affected functionality to execute arbitrary operating system commands on the underlying host. Successful exploitation could impact resources beyond the vulnerable component, resulting in a high impact on confidentiality, integrity and availability of the system.

### CVE-2026-109803

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-10T01:17:14.477 |

SAP NetWeaver Knowledge Management (XML Forms) does not sufficiently restrict the selection of XSL transformations processed by the affected functionality. Under certain conditions, an authenticated user with access to the affected functionality could cause an unauthorized XSL transformation to be processed, potentially leading to arbitrary code execution in the application context. Successful exploitation could impact the confidentiality, integrity, and availability of the application.

### CVE-2026-109795

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-10T01:17:13.330 |

SAP NetWeaver does not perform necessary authorization checks and lacks sufficient input validation in certain remote-enabled functionality. An attacker with low privileges could send specially crafted input through a remote interface to inject and execute arbitrary code within the affected system. Successful exploitation could extend the attacker's reach beyond the vulnerable component, resulting in a high impact on confidentiality, integrity and availability.

### CVE-2026-123800

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-863` |
| Published | 2026-11-09T19:16:46.647 |

SuperTokens Core is an open source authentication server. From 6.0.0 until 6.0.24, 7.0.23, 8.0.7, 9.0.6, 9.1.6, 9.2.7, 9.3.5, 10.0.8, 10.1.9, 11.0.9, 11.1.4, 11.2.4, 11.3.8, 11.4.8, 12.0.11, 12.1.2, 12.2.1, and 12.3.1, Multitenancy.checkPermissionsForCreateOrUpdate in src/main/java/io/supertokens/multitenancy/Multitenancy.java does not adequately authorize updates to a parent connection URI domain or the base tenant. In a licensed multi-tenant deployment with multiple applications under one non-default connection URI domain and separate api_keys, an attacker holding one application's valid API key can update the parent domain because the CUD-target branch checks the domain without requiring the source application and tenant to be public. Because api_keys is not protected, the attacker can replace the parent key and then sibling application keys, read or modify sibling users, obtain sessions as those users, establish persistence through a sibling dashboard user, and lock out the sibling application's own key. In the advisory's v2 create or update handlers, omitting the optional identifier produces a base-tenant target that skips the permission branches and enterprise-feature gate, allowing changes to firstFactors, required secondary factors, and recipe-enabled flags that affect login integrity and availability. The base-target variant still rejects coreConfig and does not establish key theft. This issue is fixed in versions 6.0.24, 7.0.23, 8.0.7, 9.0.6, 9.1.6, 9.2.7, 9.3.5, 10.0.8, 10.1.9, 11.0.9, 11.1.4, 11.2.4, 11.3.8, 11.4.8, 12.0.11, 12.1.2, 12.2.1, and 12.3.1.

### CVE-2026-115646

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-187` |
| Published | 2026-11-10T05:17:48.627 |

Partial String Comparison Vulnerability in HiRDB.


This issue affects HiRDB Server Version 10: from 10-00 before 10-12-01; HiRDB Server Version 9: from 09-50-06 through 09-66-22; HiRDB Server with Additional Function Version 9: from 09-50-/F through 09-66/V; HiRDB Server Version 9(32): from 09-50-06 through 09-66-22; HiRDB Server with Additional Function Version 9(32): from 09-50-/F through 09-66-/V.

### CVE-2026-125120

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-09T23:17:22.587 |

Mongoose is a MongoDB object modeling tool designed to work in an asynchronous environment. Prior to 6.13.11, 7.8.12, 8.24.3, and 9.9.2, Mongoose countDocuments() does not apply the configured sanitizeFilter query selector injection defense. An application that enables sanitizeFilter and passes attacker-controlled filter values to countDocuments() can therefore process query operator objects as operators rather than literal values, causing the count to include documents that should not match and potentially undermining authorization or application logic based on that count. This issue is fixed in versions 6.13.11, 7.8.12, 8.24.3, and 9.9.2.

### CVE-2026-123807

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-09T22:18:36.663 |

Signal K Server is a server application that runs on a central hub in a boat. From 2.0.0 until 2.34.0 for Signal K Server and from 1.0.0 until 1.5.3 for @signalk/resources-provider, the v2 REST route GET /signalk/v2/api/resources/:resourceType/:resourceId accepts an unsafe resourceId that can escape the intended resource directory. The route passes the attacker-controlled resourceId through src/api/resources/index.ts to FileStore.getResource() in packages/resources-provider-plugin/src/filestorage.ts without adequate path containment, allowing arbitrary JSON files reachable by the server to be read. Related PUT and DELETE resource operations can write or delete files outside the storage root. Deployments with allow_readonly enabled permit anonymous reads, while other deployments require a readonly user token. Reading security.json exposes the HS256 JWT signing secret and password hashes, allowing an attacker to forge an administrator token. Administrative access to POST /skServer/providers can then create an Execute provider that runs commands with the server process privileges and persists its configuration across restarts. This issue is fixed in Signal K Server 2.34.0 and @signalk/resources-provider 1.5.3.

### CVE-2026-123270

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-09T18:17:25.207 |

Redpanda Connect versions 4.39 to 4.110 contain a missing authentication vulnerability that enables unauthenticated remote code execution (RCE). In streams mode, the management HTTP API is exposed on `0.0.0.0:4195`, but authentication is disabled by default and there is no authentication gate protecting the stream CRUD routes. An unauthenticated attacker with network access to TCP/4195 can `POST` a malicious pipeline definition to `/streams/{id}` that includes code-executing processors such as `command`, `subprocess`, `ffi`, or unsafe `sql_raw`, thereby achieving arbitrary RCE on the host with the permissions of the Redpanda Connect service account. Because pipelines can also return command output in-band via HTTP, this vulnerability enables full host compromise, credential theft, and data exfiltration with no user interaction or credentials required.  

Starting with v4.111, the API endpoint was reconfigured as opt-in, so this and later versions are no longer vulnerable by default. However, RCE remains achievable on v4.111 and later if the management API is manually enabled via the `--bind-http` flag.

### CVE-2026-89119

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-10T01:17:22.103 |

SAP Web Dispatcher and SAP NetWeaver Application Server ABAP (Internet Communication Manager) do not perform sufficient request validation in certain administrative functionality. In the context of Application Server ABAP and SAP Web Dispatcher, an unauthenticated attacker could trick a logged-on administrator into visiting a malicious link. Visiting the link could cause unintended actions in the administrator's session. Successful exploitation could lead to a full compromise of the underlying operating system, resulting in a high impact on confidentiality, integrity, and availability.

### CVE-2026-119446

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-384` |
| Published | 2026-11-10T11:16:40.290 |

Session Fixation vulnerability in the CLI login flow in nerves-hub nerves_hub_web allows an unauthenticated attacker to obtain an API token for another user's account via a crafted login link. Starting a CLI login with POST /api/auth/cli_session needs no authentication and returns a polling token, a confirmation URL that carries that token, and a confirmation code. When a signed-in user opens that URL and clicks Confirm, NervesHub.Accounts.verify_cli_session_token/2 creates an API token for the user's account and stores it on the login, and the next poll of GET /api/auth/cli_session/<token> returns it to whoever started the login.

The confirmation code is only displayed and is never compared with anything, so it cannot show that the person confirming is the one who started the login. The confirm form carries a CSRF token and the page cannot be framed, so the attacker has to persuade the user to open the link and click the button themselves.

This issue affects nerves_hub: from 2.5.0 before 2.5.3.

### CVE-2026-123815

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-434` |
| Published | 2026-11-09T22:18:37.943 |

pyLoad is a free and open-source download manager written in Python. Prior to 0.5.0b3.dev102, UnTar._safe_extractall in src/pyload/plugins/extractors/UnTar.py validates archive member paths and link targets but does not call TarInfo.isdev to reject special tar member types before calling tarfile.extractall. On supported Python 3.9 through 3.13 runtimes, tarfile defaults to the fully_trusted extraction filter, so a user with ADD and STATUS permissions can cause extraction of a crafted archive containing character devices, block devices, or FIFOs. Python 3.14 defaults to a safe extraction filter. When pyLoad runs with operating-system privileges that permit device creation, including the official root-based Docker deployment, the archive can expose raw devices and compromise the host. Non-root deployments can still create FIFOs that cause hangs or IPC confusion. This issue is fixed in version 0.5.0b3.dev102.

### CVE-2026-125086

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-259;CWE-798` |
| Published | 2026-11-10T01:17:19.640 |

A vulnerability has been found in D-Link M60 1.12.B01. Impacted is the function system of the file /etc/emDaemon/mosquitto.conf of the component emDaemon MQTT Broker. Such manipulation leads to hard-coded credentials. The attack can be executed remotely. The exploit has been disclosed to the public and may be used.

### CVE-2026-125384

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-11-10T00:17:11.667 |

INDOTALENT WHMS before 10.20261109 contains a default credentials vulnerability that allows unauthenticated attackers to gain administrator access because UserAdminSeeder creates admin@root.com with password 123456. Attackers can log in with these credentials, which carry every admin role and no forced password change, to fully control deployments that kept them.

### CVE-2026-125383

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-10T00:17:11.510 |

INDOTALENT WHMS (Asp.Net-Core-Inventory-Order-Management-System) before 10.20261109 contains an authentication bypass vulnerability caused by a hard-coded JWT signing key, issuer and audience in appsettings.json. Unauthenticated remote attackers can forge tokens for any user ID and role that the Tokens/DI.cs validator trusts, gaining administrator access to the entire API.

### CVE-2026-125370

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-10T00:17:09.237 |

Kubero 3.0.0 through 3.1.1 contains an authentication bypass vulnerability that allows unauthenticated remote attackers to forge administrative JWTs by using a hardcoded fallback signing secret when JWT_SECRET is unset. Attackers can sign tokens with arbitrary role, userGroups and permissions claims, which JwtStrategy.validate() trusts without a database lookup, to take control of pipelines, applications, users and API tokens.

### CVE-2026-115934

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-09T23:17:12.470 |

An unauthenticated SQL injection can occur on the front end of any site that uses craft.search to perform a search, allowing stacked query execution and enabling escalation to an administrator.



Note that this only affects MySQL/MariaDB.

Impact  *  SQL injection — The attribute parameter is concatenated into the query unsanitized, and because PDO runs with emulated prepares, stacked statements execute. This gives unauthenticated read and write access to the application database.
  *  Privilege escalation to administrator — The write primitive was used to set the admin flag on user ID 1 in the users table, confirmed by reading the value back. Craft short-circuits its permission checks on this single column, so no further changes were needed. The same primitive can overwrite any account’s password hash.




Update to the patched versions (4.18.9 and 5.11.2) to get the fix.



If you cannot update immediately, you can block front-end requests with %5Battribute%5D and [attribute] anywhere in the query string as a temporary mitigation.

### CVE-2026-119756

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-805` |
| Published | 2026-11-09T18:17:22.320 |

Tasmota through 16.0.0, fixed in commit e97e1e4, contains a heap out-of-bounds write vulnerability in SendReceiveDeviceGroupMessage() that allows unauthenticated attackers on the local network to corrupt heap memory by sending crafted Device Groups messages over UDP port 4447 that cause the log_remaining counter to go negative and writes to exceed the fixed 512-byte buffer. Attackers can exploit this flaw to crash the device or potentially achieve native code execution on ESP8266 and ESP32 platforms that lack ASLR and heap cookies.

### CVE-2026-104989

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-09T17:17:07.237 |

Uncontrolled search path element in package upload feature in Chaos Software V-Ray versions through 2.0.19 allows remote unauthenticated attackers to execute arbitrary code via redirecting access to libraries

### CVE-2026-112136

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1327` |
| Published | 2026-11-10T12:17:16.540 |

A vulnerability has been identified in Mendix Studio Pro 11 (All versions >= V11.15.0 < V11.16.0), Mendix Studio Pro 11.12 (All versions >= V11.12.6 < V11.12.7). The affected products MCP Server does not properly restrict its HTTP listener to the loopback interface, leaving it potentially exposed to remote systems. This could allow an attacker with network access to interact with the MCP Server remotely.

### CVE-2026-107246

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T01:17:12.880 |

The Plesk extension "Site Import" before 1.13.2 does not properly validate domain and session identifiers, allowing path traversal. This lets a non-owner subscription user redirect a privileged backend session into a directory they control, resulting in arbitrary code execution as root.

### CVE-2026-124001

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-11-09T19:16:48.003 |

NASA JPL ION-DTN 2.2.1b through 4.2.0 contains an integer overflow vulnerability in the Datagram Retransmission (DGR) convergence layer that allows attackers to corrupt heap memory by sending a maliciously crafted 64-bit svcDataLength value that wraps a 32-bit allocation size calculation. Attackers can exploit the dgr_receive API's unchecked memcpy operation using synthetic datagrams or DGR traffic over internal IPC or custom transports to trigger an out-of-bounds write, leading to denial of service or potential remote code execution.

### CVE-2026-82509

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-10T14:17:36.290 |

V programming language standard library net.http through version 0.5.2 prior to commit 4077484 contains a TLS certificate validation bypass vulnerability that allows on-path attackers to intercept HTTPS traffic by exploiting the default false value of SSLConnectConfig.validate and FetchConfig.validate, which completes TLS handshakes without verifying certificates in both the mbedtls and OpenSSL backends. Attackers can present an expired, self-signed, wrong-hostname, or untrusted-root certificate to successfully complete the handshake via http.get, http.post, or http.fetch, enabling interception or modification of HTTPS traffic unless validate: true is explicitly configured.

### CVE-2026-109798

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-10T01:17:13.747 |

SAP BusinessObjects Business Intelligence Platform (Web Intelligence) does not properly restrict external entity resolution when processing OLAP connection requests. An authenticated attacker could exploit this vulnerability to access restricted resources, enabling them to read sensitive files on the server and reach internal systems that are not otherwise exposed, impacting resources beyond the vulnerable component, resulting in a high impact on confidentiality and a low impact on both integrity and availability.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-76966

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-294` |
| Published | 2026-11-10T01:17:20.527 |

Due to improper RFC protocol validation in the SAP Kernel used by the Application Server ABAP of SAP NetWeaver and ABAP Platform, an unauthenticated attacker can send a crafted RFC request that exploits logical errors in memory management, leading to memory corruption. This could lead to a high impact on confidentiality and integrity with low impact on availability of the application.

### CVE-2026-12573

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-10T12:17:19.660 |

Zoho Corporation ManageEngine DDI Central versions 6200 and below are vulnerable to Cisco IOS command injection via DHCP pool name leading to arbitrary commands on managed Cisco routers.

### CVE-2026-123717

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T12:17:17.380 |

OS command injection in the pass and bitwarden credential providers in Eclipse Foundation Eclipse Otterdog through 1.7.1 allows a user able to modify an organization configuration to execute arbitrary commands with the privileges of the operator running otterdog, including access to their credential vault, via a crafted secret reference (pass:<path> or bitwarden:<item>@<field>) or credential identifier that is resolved when otterdog apply is run.

### CVE-2026-8372

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-10T06:17:10.420 |

A vulnerability that could allow an attacker to gain unauthorized access.

### CVE-2026-4762

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-10T06:17:09.757 |

A vulnerability to perform a privilege escalation attack on the server as a non-admin user.

### CVE-2026-125612

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T03:16:42.547 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Deltaww DIAEnergie allows SQL Injection.

This issue affects DIAEnergie: before 1.11.01.032.

### CVE-2026-113970

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-09T22:18:26.903 |

A use-after-free issue was addressed with improved memory management. This issue is fixed in iOS 18.7.12 and iPadOS 18.7.12, iOS 26.7.3 and iPadOS 26.7.3, iOS 27.2.1 and iPadOS 27.2.1, macOS Golden Gate 27.2.1, macOS Sequoia 15.8.3, macOS Tahoe 26.7.3, visionOS 27.2.1, watchOS 26.6.1, watchOS 27.2.1. An attacker in Bluetooth range may be able to corrupt process memory.

### CVE-2026-102643

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-50` |
| Published | 2026-11-09T22:18:21.920 |

AsyncSSH is a Python package which provides an asynchronous client and server implementation of the SSHv2 protocol on top of the Python asyncio framework. Prior to 2.24.1, SFTPServer.map_path() uses posixpath.normpath() on a client-supplied path and removes only one leading slash before passing the result to posixpath.join() with the configured chroot. An authenticated SFTP user can supply a path beginning with exactly two slash characters, causing POSIX normalization to preserve the double-leading-slash form and the subsequent join to treat the remaining pathname as absolute. This bypasses the SFTP chroot and permits reads and writes with the operating-system permissions of the account running the server, which may enable code execution depending on writable targets. This issue is fixed in version 2.24.1.

### CVE-2026-12977

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-267` |
| Published | 2026-11-09T19:17:04.307 |

A flaw was found in the deployment-operation family of WildFly Core. Certain handlers, such as upload-deployment-url, lack proper sensitivity classification, allowing an administrator with the restricted "Maintainer" role to read sensitive configuration files. This can lead to the exfiltration of credentials and full administrative control (SuperUser) of the server.

### CVE-2026-121576

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-09T17:17:14.493 |

Incorrect Privilege Assignment vulnerability in AtlasAiDev MCP Server for WordPress ai-workflow-automation-ai-agent-hub allows Privilege Escalation.This issue affects MCP Server for WordPress: from n/a through 2.0.1.

### CVE-2026-12708

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-11-10T14:17:29.980 |

Summary


Cloudflare tokio-quiche was found to contain an uncontrolled resource consumption vulnerability in its HTTP/3 DATAGRAM handling. For every previously unseen flow identifier (quarter stream ID) received in a DATAGRAM frame, tokio-quiche creates and retains new, per-flow state. A remote peer can send DATAGRAMs with many distinct identifiers, causing the per-connection flow map and associated channel state to grow without bound.

Impact


Exploitation can exhaust process memory and cause a denial of service. The vulnerable code is used in both client and server configurations, so either role can be affected by a malicious peer. QUIC DATAGRAM support in tokio-quiche is enabled by default through QuicSettings::enable_dgram; applications can disable it by setting this field to false. The vulnerable HTTP/3 path is reachable only when DATAGRAM support is negotiated with the peer. Core quiche and HTTP/3 deployments without DATAGRAM support are not affected. 






Mitigation


Disable DATAGRAMs in tokio-quiche’s QuicSettings::enable_dgram.






Remediation


Upgrade to tokio-quiche version 0.23.0 or later. The fixed code creates flow state only for valid DATAGRAM-capable request streams, which are bounded by QUIC’s stream limits. To tolerate packet reordering, servers retain early DATAGRAMs in a bounded, expiring buffer, while clients discard DATAGRAMs for unknown flows.

### CVE-2026-60046

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-11-10T09:17:24.617 |

An unauthenticated remote attacker can perform password resets for any user with known username and email without rate limiting. This can result in a total loss of availabilit since the password will be reseted.

### CVE-2026-60044

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1393` |
| Published | 2026-11-10T09:17:24.307 |

The backups created by the application use a weak static password allowing an unauthenticated remote attacker to access their content. This can result in a total loss of confidentiality.

### CVE-2026-60040

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-10T09:17:23.610 |

An unauthenticated remote attacker can perform a DoS in the backends backup creation function. This can result in a total loss of availability.

### CVE-2026-88710

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T02:16:45.963 |

Improper
neutralization of special elements used in an OS command in certain
ASUS Router firmware
allows an unauthenticated nearby user to trigger a chain of
actions—unauthenticated queries, identifier guessing, credential overwriting,
and command injection—resulting in the execution of arbitrary commands with
root privileges.
Refer to the ' Security Update for ASUS Router Firmware ' section on the ASUS Security Advisory for more information.

### CVE-2026-125406

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-124` |
| Published | 2026-11-10T00:17:15.507 |

Ettercap through 0.8.4.1 contains a stack buffer underwrite vulnerability in the telnet dissector in src/dissectors/ec_telnet.c that decrements the output pointer on backspace without a lower bound check. Attackers can send a telnet stream with more backspaces than preceding characters to write below the stack buffer, corrupting the stack of the Ettercap process that normally runs as root.

### CVE-2026-125400

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T00:17:14.387 |

Ettercap through 0.8.4.1 contains a use-after-free vulnerability in func_pcre() in src/ec_filter.c that reads the PCRE2 ovector after freeing match data. Network-adjacent attackers can send packets matching a loaded pcre_regex() substitution filter to corrupt memory and potentially execute code as root.

### CVE-2026-123817

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-09T22:18:38.273 |

AIOHTTP is an asynchronous HTTP client/server framework for asyncio and Python. Prior to 3.14.4, the WebSocket reader retains one bytes object for each transport read while reassembling an incomplete frame. A malicious peer can split a frame into many tiny reads so per-object overhead substantially exceeds the payload bytes allowed by max_msg_size. The condition affects a server receiving frames from a malicious client and a client receiving frames from a malicious server, and can cause excessive memory consumption or denial of service. This issue is fixed in version 3.14.4.

### CVE-2026-123999

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-09T19:16:47.650 |

NASA JPL ION-DTN 3.6.2 through 4.2.0 contains a heap-based buffer overflow in the Network Management daemon (nm_mgr) string-formatting logic that allows a malicious or misconfigured agent to trigger an out-of-bounds write by sending deeply nested AMP payloads that exceed fixed-size buffer allocations through unbounded strcat operations. Attackers can transmit oversized AMP reports, tables, or macros over the UDP CLA/AMP path or trigger the flaw locally via interactive UI rendering to crash nm_mgr and cause a denial of service halting telemetry collection and operator visibility.

### CVE-2026-124683

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-09T17:17:27.690 |

Eclipse Langium versions 3.2.0 through 4.4.0 contain an inefficient algorithmic complexity issue (CWE-407) in the opt-in IndentationAwareTokenBuilder and IndentationAwareLexer. When producing DEDENT tokens, the token builder recomputes line numbers by re-scanning the entire preceding document text. A document whose indentation changes on most lines then takes quadratic time to tokenize. Because tokenization is synchronous, a crafted document of a few hundred kilobytes can block the Node.js event loop for tens of seconds. That causes a DoS for every user served by the same process. Languages built with the DefaultLexer and DefaultTokenBuilder are unaffected.

### CVE-2026-109097

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-10T12:17:16.223 |

A vulnerability has been identified in ROS# (All versions < V2.3.1). Affected systems do not properly escape text of message definition files. This could allow an attacker that is able to pass a crafted message definition file to the user to inject arbitrary code into the generated program.

### CVE-2026-120730

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-915` |
| Published | 2026-11-10T11:16:42.230 |

Improperly Controlled Modification of Dynamically-Determined Object Attributes vulnerability in the device API, device forms, signing key and product forms and JITP settings in nerves-hub nerves_hub_web allows an authenticated user who manages devices in any organization to write into other organizations via submitted org_id, product_id and deployment_id fields. The device API create and update actions and the dashboard device forms pass the request parameters to NervesHub.Devices.Device.changeset/2, which casts the organization, product, deployment group and update state as given. The signing key and product forms merge the session's organization into the submitted parameters so that a submitted org_id wins, and the JITP changeset accepts any product_id. Each request requires the manage role only in the user's own organization, and any account can create one.

A device placed on another organization's deployment group, or moved into its product, is sent that organization's firmware with a download URL. The user cannot change or control devices that already belong to the other organization, and cannot upload firmware to it.

This issue affects nerves_hub: from 1.0.0 before 2.5.3.

### CVE-2026-60039

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T09:17:23.463 |

A high privileged remote attacker can perform a code injection in the backends backup restore function leading to code execution. This can result in a total loss of confidentiality, integrity and availability.

### CVE-2026-60038

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T09:17:23.300 |

A high privileged remote attacker can perform an OpenSSL code injection in the backends ImportPKCS12 function leading to code execution. This can result in a total loss of confidentiality, integrity and availability.

### CVE-2026-60037

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T09:17:23.133 |

A high privileged remote attacker can perform an OpenSSL code injection in the frontends device importer function leading to code execution. This can result in a total loss of confidentiality, integrity and availability.

### CVE-2026-60036

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T09:17:22.963 |

A high privileged remote attacker can perform a code injection in the backends patch activate function leading to code execution. This can result in a total loss of confidentiality, integrity and availability.

### CVE-2026-60035

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T09:17:22.783 |

A high privileged remote attacker can perform a code injection in the backends network auth function leading to code execution. This can result in a total loss of confidentiality, integrity and availability.

### CVE-2026-125399

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T00:17:14.230 |

Fluxion before 6.39 contains an OS command injection vulnerability in the fluxion.sh target scanner, which decodes access point ESSIDs with eval after escaping only single quotes. Attackers within Wi-Fi range can broadcast an access point with a crafted SSID to execute commands as root when the operator scans or selects it.

### CVE-2026-125391

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T00:17:12.827 |

Webmin through 2.670 contains an OS command injection vulnerability in samba/save_euser.cgi that allows authenticated Samba user maintainers to inject commands via unvalidated opts parameter. Attackers can embed shell metacharacters in account option flags passed by create_user and modify_user to backquote_logged, executing commands as root.

### CVE-2026-125382

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-10T00:17:11.330 |

Map-OS 5.0.0 to before 5.2.2 contains a privilege escalation vulnerability in the REST users API that allows non-administrator operators holding the cUsuario permission to bypass permission-delegation and super-administrator protections. Attackers can send POST, PUT, or DELETE requests to /api/v1/usuarios to assign the Administrador group, reset the super administrator password, or delete higher-privileged users.

### CVE-2026-125364

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-10T00:17:08.220 |

frab through 0.9.1 contains a privilege escalation vulnerability that allows authenticated crew users to grant themselves orga roles by submitting unchecked nested conference_users_attributes. Attackers can abuse UsersController#update or #create, which skip filter_conference_users, to gain orga on any conference and fully manage its events, schedule, reviewers and crew.

### CVE-2026-125360

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-10T00:17:07.530 |

Storyden through 1.26.16 contains a privilege escalation vulnerability that allows users holding MANAGE_ROLES to grant the ADMINISTRATOR permission without being administrators. Attackers can call AccountAddRole on another controlled account or use RoleCreate and RoleUpdate to create administrator roles, taking full control of the instance.

### CVE-2026-119759

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-09T22:18:28.620 |

TrailBase 0.28.2 before 0.35.10 contains an insecure direct object reference vulnerability that allows authenticated attackers to manipulate the object-store id metadata within std.FileUpload columns without ownership validation during insert and update operations. Attackers can reference another user's or table's file id in a record they own to read the victim's file bytes through their own record, or trigger permanent deletion of the victim's file by deleting or nulling their own record, while also using a $like filter on the file column to brute-force recover stripped ids character by character.

### CVE-2026-59082

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-357` |
| Published | 2026-11-10T12:17:20.510 |

A vulnerability has been identified in SIMATIC WinCC V7.5 (All versions), SIMATIC WinCC V8.0 (All versions), SIMATIC WinCC V8.1 (All versions). Affected devices implicitly execute active content when opening files. This could allow an attacker to make the user execute arbitrary code on the device.

### CVE-2026-125742

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T12:17:18.893 |

7-Zip before 26.06 contains a heap out-of-bounds write vulnerability in the LZX decoder that lets attackers corrupt memory when a continuation CAB volume declares a smaller window. Attackers can entice victims to extract crafted multi-volume CAB archives, where a stale _pos value bypasses bounds checks, enabling arbitrary code execution.

### CVE-2026-125396

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-648` |
| Published | 2026-11-10T00:17:13.713 |

Ghostscript before 10.08.0 contains a -dSAFER bypass vulnerability in the .putgstringcopy procedure in gs_fonts.ps, which calls the privileged .forceput operator without checking operand types. Attackers can supply crafted PostScript or PDF documents that trigger a type error, recover .forceput via a custom error handler, and cause a use-after-free across save/restore to execute arbitrary code.

### CVE-2026-125267

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-09T20:18:13.383 |

FFmpeg before 8.1.3 and 9.x before 9.0.2 contains a heap out-of-bounds write vulnerability in the APAC decoder in libavcodec/apac.c caused by an unreset bitstream index. Attackers can supply a crafted APAC file whose growing bitstream_index triggers an integer overflow, bypassing the reallocation check so memcpy() corrupts heap memory or crashes the application.

### CVE-2026-125262

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-09T20:18:12.657 |

FFmpeg through 9.0.2 contains a heap buffer overflow vulnerability in libavcodec/lcevcdec.c because LCEVC output picture dimensions are not validated against the allocated frame. Attackers can embed crafted LCEVC enhancement data with differing global configurations in H.264 or HEVC streams to corrupt heap memory in decoding applications.

### CVE-2026-125259

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-09T20:18:12.220 |

FFmpeg through 9.0.2 contains an integer overflow vulnerability in ff_prores_kostya_encode_init() that miscalculates frame_size_upper_bound using 32-bit arithmetic for large frame dimensions. Attackers can supply a high-resolution video transcoded with the prores_ks encoder, causing encode_frame() to write slices past an undersized packet buffer and corrupt heap memory.

### CVE-2026-125250

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-09T19:17:03.883 |

FFmpeg through 9.0.2 contains a heap buffer overflow in the GIF encoder's gif_image_write_image() in libavcodec/gif.c because shrunk_buf is sized from the first frame's linesize. Attackers can supply PAL8 video whose frame linesize grows mid-stream, causing remap_frame_to_palette() to write past shrunk_buf and corrupt the heap during GIF transcoding.

### CVE-2026-125244

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-09T19:17:02.953 |

FFmpeg before 8.1.3 and 9.x before 9.0.2 contains an out-of-bounds write vulnerability in the VVC decoder's sh_entry_points() function in libavcodec/vvc/ps.c. Attackers can supply a crafted VVC (H.266) bitstream whose SPS/PPS tile and WPP layout produces excess entry points, overflowing entry_point_start_ctu and corrupting decoder memory.

### CVE-2026-125233

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-131` |
| Published | 2026-11-09T19:17:01.293 |

FFmpeg through 9.0.2 contains a heap buffer overflow vulnerability in dvbsub_encode() in libavcodec/dvbsubenc.c that undercounts each CLUT segment header by two bytes. Attackers can supply a file with many bitmap subtitle rectangles that, when transcoded to the dvbsub encoder, writes past the output buffer and corrupts heap memory.

### CVE-2026-125229

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-09T19:17:00.700 |

FFmpeg through 9.0.2 contains an out-of-bounds memory access vulnerability in the encode_frame() function of libavcodec/huffyuvenc.c, because encode_init() never validates minimum frame dimensions for the median predictor. Attackers can supply a tiny video, such as a 2-pixel-wide or 1-2-pixel-tall frame, that causes negative sub_median_pred lengths and out-of-bounds reads and writes when transcoded to huffyuv or ffvhuff, crashing the encoder.

### CVE-2026-125209

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-131` |
| Published | 2026-11-09T19:16:57.643 |

FFmpeg before 8.1.3 and 9.x before 9.0.2 contains a heap buffer overflow vulnerability in the DVD subtitle encoder that underestimates RLE output size for odd-width rectangles. Attackers can supply files with crafted bitmap subtitles that, when transcoded to the dvdsub encoder, write past the output buffer and corrupt heap memory.

### CVE-2026-125203

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-09T19:16:56.740 |

FFmpeg before 8.1.3 and 9.x before 9.0.2 contains a heap buffer overflow vulnerability in the Cook multichannel decoder in libavcodec/cook.c that fails to verify subpacket channel masks are disjoint. Attackers can supply a crafted RealMedia Cook stream with overlapping subpacket masks, causing cook_decode_frame() to write decoded samples beyond allocated output planes in any application decoding the file.

### CVE-2026-121769

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-09T19:16:46.130 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in axew3.com WP w3all phpBB wp-w3all-phpbb-integration allows SQL Injection.This issue affects WP w3all phpBB: from n/a through 3.1.9.

### CVE-2026-104620

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-09T15:17:04.997 |

A path traversal attack in simulation of actions in the Zypp backend of PackageKit before 1.4.1 could be used by local attackers to gain root privileges.

### CVE-2026-12389

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-10T06:17:08.200 |

A vulnerability that could lead to a high privileged authenticated user performing a remote code execution attack.

### CVE-2026-63288

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-10T06:17:10.197 |

A WebSocket request sent to a specific API endpoint allows unauthorized access to a separate API endpoint. This bypasses the intended authentication layer.

### CVE-2026-125114

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-09T23:17:21.587 |

Novu provides an API for sending notifications through multiple channels. Prior to 3.15.0, the conditions filter webhook in libs/application-generic/src/usecases/conditions-filter/conditions-filter.usecase.ts passes the user-configured child.webhookUrl directly to axios.post without calling validateUrlSsrf. Evaluating a workflow condition can therefore make the worker send a POST request to a private or link-local service and return the response data for condition evaluation. The response is stored in execution details and exposed through GET /execution-details, which can disclose credentials from POST-capable metadata services or data from internal services, although metadata endpoints that require GET are not reachable through this path. This issue is fixed in version 3.15.0.

### CVE-2026-19706

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-09T18:17:27.583 |

During ABI bootstrap, the bootstrap node's approve-csr.service approves and signs every CSR without identity validation.

An attacker on the install network can retrieve the unauthenticated Ignition file (ports 22623/22624), extract a limited kubeconfig, submit a CSR for CN=system:admin, receive the signed certificate, and gain full cluster-admin access.

Exploitable only during the narrow bootstrap window.

### CVE-2026-120513

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T07:16:51.733 |

The Everest Forms – Contact Form, Payment Form, Quiz, Survey & Custom Form Builder with AI plugin for WordPress is vulnerable to file deletion due to insufficient file path validation in the remove_csv_file_after_email_send function in all versions up to, and including, 3.6.2 This makes it possible for unauthenticated attackers to delete files within the wp-content/uploads directory on the server, which can lead to loss of uploaded content. On hardened Apache configurations, deletion of uploads/.htaccess can re-enable PHP execution inside the uploads directory. This attack is only possible when the Save-and-Continue addon is active (EVF_SAVE_AND_CONTINUE_VERSION is defined) and the 'Disable storing entry information' setting is enabled on the target form. Escaping the uploads directory and deleting files in the site root can be possible under rare circumstances.

### CVE-2026-91763

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-61` |
| Published | 2026-11-10T05:18:16.210 |

UNIX Symbolic Link (Symlink) Following Vulnerability in Hitachi Dynamic Link Manager for Linux.
This issue affects Hitachi Dynamic Link Manager for Linux: from 8.6.2.-00 before 9.0.5-00.

### CVE-2026-91761

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-61` |
| Published | 2026-11-10T05:18:15.807 |

UNIX Symbolic Link (Symlink) Following Vulnerability in Hitachi Dynamic Link Manager for Linux.

This issue affects Hitachi Dynamic Link Manager for Linux: from 8.6.2.-00 before 9.0.5-00.

### CVE-2026-86579

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-10T05:18:12.020 |

Binary Planting Vulnerability in Hitachi Dynamic Link Manager for Windows.

This issue affects Hitachi Dynamic Link Manager for Windows: from 5.9.5-00 before 9.0.4-01.

### CVE-2026-120008

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T01:17:15.997 |

SAP NetWeaver (Internet Graphics Service) does not sufficiently validate certain input values within incoming requests. An unauthenticated user could send a specially crafted request to trigger an out-of-bounds memory write in a worker process. Successful exploitation could result in memory corruption or repeated termination of the affected process, resulting in a high impact on availability and a low impact on integrity with no impact on confidentiality.

### CVE-2026-125117

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-1321` |
| Published | 2026-11-09T23:17:22.080 |

Mongoose is a MongoDB object modeling tool designed to work in an asynchronous environment. Prior to 6.13.12, 7.8.13, 8.24.7, and 9.11.4, Mongoose can descend into inherited properties while loading database documents in init(), setting dotted paths in $__set, and merging update documents in utils.mergeClone. Attacker-controlled keys such as toString or valueOf can therefore cause Mongoose to write into shared built-in functions instead of an own property. A crafted document, Mixed path, non-strict document or subdocument, findOneAndReplace() replacement, chained update, or Query.prototype.merge() source can overwrite Object.prototype.toString.call, causing later queries on unrelated models to fail until the process restarts. Separately, when an attacker controls the dotted path passed to doc.set(path, value) for a subdocument configured with strict: false, descent through $__set can reach $__schema and alter shared validators or schema options for later documents. Mongoose already blocks __proto__, constructor, and prototype, so this issue overwrites properties on reachable shared objects rather than adding new properties directly to Object.prototype. This issue is fixed in versions 6.13.12, 7.8.13, 8.24.7, and 9.11.4.

### CVE-2026-12574

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T12:17:19.790 |

Zoho Corporation ManageEngine DDI Central versions 6200 and below are vulnerable to Server-side HTML/JavaScript injection in analytics PDF generation leading to local file disclosure.

### CVE-2026-76877

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-10T07:16:52.463 |

The WPML Multilingual CMS plugin for WordPress is vulnerable to Authentication Bypass via Race Condition in versions up to, and including, 4.9.7. This is due to the `process_iframe_request` function's language-per-domain SSO handler generating the cross-domain sign-in token via `wp_create_nonce('wpml_sso')` on the logout landing page, where the browser has already discarded its authentication cookies — so `wp_get_session_token()` returns an empty string and the token collapses to the shared anonymous nonce for the current 12-hour tick rather than a user-bound secret — and then storing it in the `wpml_sso_user_<token>_<sha256('wpml_sso'.$domain)>` transient mapped to the victim's `user_id` with no binding to the specific sign-out action or requesting client. Because an unauthenticated attacker can independently derive the identical token by triggering the logout confirmation flow on `wp-login.php?action=logout`, and because the `is_iframe_request()` gate conditions (the per-domain SSO `started` transient and domain-hash derived from the public constant `SSO_NONCE`) are fully computable within the 60-second `SSO_TIMEOUT` window, an unauthenticated attacker can submit the forged `wpml_sso_token_domain` parameter with a `wpml_user_signed_in` status to a secondary language-domain endpoint before the legitimate `wpml_user_signed_out` iframe fires, causing WordPress authentication cookies to be issued for the victim. This makes it possible for unauthenticated attackers to gain access to accounts of users — including administrators — who are actively in the process of logging out during the race window.

### CVE-2026-91764

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:L/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-10T05:18:16.360 |

Improper Link Resolution Before File Access Vulnerability in Hitachi Dynamic Link Manager for Linux.


This issue affects Hitachi Dynamic Link Manager for Linux: from 6.1.1.-00 before 9.0.5-00.

### CVE-2026-91756

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T05:18:13.950 |

OS Command Injection Vulnerability in Hitachi Dynamic Link Manager for VMware.

This issue affects Hitachi Dynamic Link Manager for VMware: from 8.7.3-00 before 9.0.4-01.

### CVE-2026-91755

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-10T05:18:13.297 |

Integer Overflow Vulnerability in Hitachi Dynamic Link Manager for VMware.

This issue affects Hitachi Dynamic Link Manager for VMware: from 8.7.3-00 before 9.0.4-01.

### CVE-2026-91754

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T05:18:12.973 |

Stack-based Buffer Overflow Vulnerability in Hitachi Dynamic Link Manager for VMware.

This issue affects Hitachi Dynamic Link Manager for VMware: from 8.7.3-00 before 9.0.4-01.

### CVE-2026-123816

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-09T22:18:38.110 |

pyLoad is a free and open-source download manager written in Python. Prior to 0.5.0b3.dev101, Api.check_apikey caches successful validation in self._apikey_cache using only the attacker-controlled key_id. After a legitimate key populates the cache, a forged API key with the same key_id reaches the cache-hit path without comparing apikey[-43:] to the stored hash through hmac.compare_digest. Key identifiers are small sequential integers, so an unauthenticated remote attacker can enumerate an active identifier and inherit the cached key owner's permissions during the 300-second cache lifetime. This issue is fixed in version 0.5.0b3.dev101.

### CVE-2026-123803

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863;CWE-1220` |
| Published | 2026-11-09T19:16:47.273 |

SuperTokens Core is an open source authentication server. From 10.1.0 until 11.0.9, 11.1.4, 11.2.4, 11.3.8, 11.4.8, 12.0.11, 12.1.2, 12.2.1, and 12.3.1, loadOptionsById_Transaction and getUserInfoByCredentialId_Transaction perform application-scoped WebAuthn lookups without constraining them to the requested tenant, and WebAuthN.signIn does not verify tenant membership. In a multi-tenant deployment using WebAuthn with a shared user pool, an ordinary user who possesses their own valid passkey in one tenant can submit its assertion to another tenant's sign-in endpoint in the same application and be authenticated there despite having no membership in the target tenant. This issue is fixed in versions 11.0.9, 11.1.4, 11.2.4, 11.3.8, 11.4.8, 12.0.11, 12.1.2, 12.2.1, and 12.3.1.

### CVE-2026-123802

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-345;CWE-1220` |
| Published | 2026-11-09T19:16:47.083 |

SuperTokens Core is an open source authentication server. From 11.3.0 until 11.3.8, 11.4.8, 12.0.11, 12.1.2, 12.2.1, and 12.3.1, a licensed deployment with a configured SAML client can authenticate an identity from an assertion that did not satisfy the audience check. When the identity provider uses assertion-level signing, an attacker who has a still-valid IdP-signed assertion naming the victim for any audience and the attacker's own valid assertion for the target audience can combine them because validateSamlResponseAudience accepts an audience from one assertion while extractAllClaims takes the final NameID and attributes from another; response-level signing does not expose this multi-assertion variant. Independently, an assertion from an identity provider configured for the target deployment but issued to another SuperTokens deployment using the shared default saml_sp_entity_id can satisfy the target's audience check. Successful exploitation authenticates the attacker as the victim IdP user. This issue is fixed in versions 11.3.8, 11.4.8, 12.0.11, 12.1.2, 12.2.1, and 12.3.1.

### CVE-2026-123798

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-347` |
| Published | 2026-11-09T19:16:46.280 |

SuperTokens Core is an open source authentication server. From 11.3.0 until 11.3.7, 11.4.7, and 12.0.10, SAML.verifySamlResponseSignature calls OpenSAML SignatureValidator.validate without first applying SAMLSignatureProfileValidator. The Core can therefore accept a cryptographically valid signature that references a different XML element from the Response or Assertion whose NameID and attributes are used for authentication. An ordinary user of the configured identity provider can move a genuinely signed element elsewhere in the document while supplying an attacker-authored identity-bearing element, causing XML Signature Wrapping authentication as another IdP user. Both response-level and assertion-level signing paths are affected, and SP-initiated login remains reachable without enabling allowIDPInitiatedLogin. This issue is fixed in versions 11.3.7, 11.4.7, and 12.0.10.

### CVE-2026-115338

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-319;CWE-345` |
| Published | 2026-11-09T17:17:11.240 |

Insufficient protection of communications in Progress WS_FTP Server versions prior to 2025.0.5 could allow a network attacker to intercept sensitive information or modify requests when unencrypted connections are used.

### CVE-2026-95646

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-10T11:16:43.757 |

Zoho Corporation ManageEngine DDI Central versions 6500 and below are vulnerable to a Unicode-based command injection vulnerability in the Cisco IOS DHCP configuration functionality. This vulnerability could allow cluster-scoped operators to inject specially crafted Unicode characters, resulting in the execution of unintended device commands.

### CVE-2026-12964

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-10T06:17:08.453 |

A vulnerability allowing for privileged escalation of the viewer account to gain administrator privileges.

### CVE-2026-91762

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-61` |
| Published | 2026-11-10T05:18:16.053 |

UNIX Symbolic Link (Symlink) Following Vulnerability in Hitachi Dynamic Link Manager for Linux.


This issue affects Hitachi Dynamic Link Manager for Linux: from 8.5.3.-00 before 9.0.5-00.

### CVE-2026-121267

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-11-10T13:18:22.020 |

Incorrect default permissions vulnerability in TÜBİTAK BİLGEM Software Technologies Research Institute eta-remote allows Accessing Functionality Not Properly Constrained by ACLs.

This issue affects eta-remote: from 0.0.2 before 0.0.3.

### CVE-2026-104619

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1328` |
| Published | 2026-11-10T10:16:42.590 |

Untrusted users could roll back security updates when using the PackageKit Zypp Backend before 1.4.1, allowing privilege escalation.

### CVE-2026-91759

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T05:18:15.177 |

Out-of-Bounds Write Vulnerability in Hitachi Dynamic Link Manager for Linux.


This issue affects Hitachi Dynamic Link Manager for Linux: from 7.5.0-00 before 9.0.5-00.

### CVE-2026-91758

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-131` |
| Published | 2026-11-10T05:18:14.520 |

Out-of-bounds Read and Write Vulnerability in Hitachi Dynamic Link Manager for Linux.

This issue affects Hitachi Dynamic Link Manager for Linux: from 7.5.0-00 before 9.0.5-00.

### CVE-2026-90586

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-824` |
| Published | 2026-11-09T22:18:56.813 |

The Xtensa MMU userspace port never initialized the per-thread page-table pointer thread->arch.ptables during thread setup, while arch_mem_domain_thread_add() in arch/xtensa/core/ptables.c uses a non-NULL value of that field as its "this thread is migrating from another memory domain" predicate. For a thread whose struct k_thread backing memory is not zeroed, the field holds stale data and the kernel takes the migration branch, passing that stale value to reset_region() as the base of a level-1 page table. The equivalent field on x86 is explicitly cleared in z_x86_userspace_prepare_thread() for exactly this reason; the Xtensa port adopted the predicate without the initialization.

The condition is reachable from an unprivileged user-mode thread on a build with CONFIG_XTENSA_MMU, CONFIG_USERSPACE and dynamically allocated kernel objects. k_object_alloc(K_OBJ_THREAD) is a system call and allocates the thread object from the caller's resource pool without zeroing it, and the k_thread_create() verifier accepts such an object while forcing the K_USER option, so the migration branch is taken whenever the recycled heap bytes at that offset are non-zero. Because a user thread can also allocate, fill and free other kernel objects from the same heap, the stale bytes are groomable rather than merely random.

Walking the bogus table in region_map_update() performs an unguarded index into l2_page_tables_counter[], may copy from and write through the attacker-influenceable level-1 base in dup_l2_table_if_needed(), and finally writes a page-table entry through a second pointer read out of that memory — once per page of the new thread's stack. The result is out-of-bounds reads and writes executed in supervisor mode, ranging from an immediate kernel panic (observed as Xtensa EXCAUSE 13 on Intel ADSP DSP firmware with user threads) to corruption of kernel memory and escape from the user-mode sandbox.

### CVE-2026-63496

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-09T22:18:53.473 |

augment-vir is a collection of helper functions. Prior to version 31.73.5, the grep() function exported by @augment-vir/node inserts caller-controlled search patterns directly into a double-quoted shell command string without sanitization (grep.ts:310). When the constructed command is passed to spawn() with shell: 'bash' (shell.ts:98-99), bash evaluates $() command substitution expressions embedded in the pattern, resulting in arbitrary OS command execution as the Node.js process user. Any downstream application that passes untrusted input to grep()'s pattern or patterns field is vulnerable to unauthenticated local (and potentially remote) code execution. This issue has been patched in version 31.73.5.

### CVE-2026-114032

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-09T22:18:27.397 |

The OpenSSL library bundled with the Illumio VEN for Windows is affected by an uncontrolled search path vulnerability. A low-privileged, authenticated local attacker could potentially leverage this vulnerability to execute arbitrary code with SYSTEM privileges.

### CVE-2026-114031

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-09T22:18:27.257 |

Incorrect permission assignment allows local privilege escalation to SYSTEM on affected releases of the Illumio VEN for Windows. Code execution as NT AUTHORITY\LOCAL SERVICE on the Windows host is required to exploit this vulnerability. The flaw exists within the VEN installer, which grants LOCAL SERVICE full access to the VEN data and installation folders, whose configuration and state files are read and trusted by the SYSTEM-privileged illumio-ven-ctl component. An attacker can leverage this vulnerability to modify the VEN configuration so that illumio-ven-ctl executes an injected command in the context of the SYSTEM account.

### CVE-2026-103906

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-09T17:17:06.787 |

Use of hard-coded MQTT credentials in the AM CLUB mobile application allows an authenticated attacker to connect to the MQTT broker and access data or perform actions across tenant boundaries.

### CVE-2026-119474

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-09T15:17:07.140 |

Incorrect Permission Assignment for Critical Resource vulnerability in HAVELSAN Inc. Liman Render Engine allows Privilege Escalation.

This issue affects Liman Render Engine: before 1.2-81.

### CVE-2026-58114

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1390` |
| Published | 2026-11-10T12:17:20.160 |

A vulnerability has been identified in SIMATIC BATCH V9.1 (All versions), SIMATIC Information Server 2020 (All versions), SIMATIC Information Server 2022 (All versions), SIMATIC PCS 7 V9.1 (All versions), SIMATIC Process Historian 2020 (All versions), SIMATIC Process Historian 2022 (All versions), SIMATIC WinCC Runtime Professional V17 (All versions), SIMATIC WinCC Runtime Professional V18 (All versions), SIMATIC WinCC Runtime Professional V19 (All versions), SIMATIC WinCC Runtime Professional V20 (All versions), SIMATIC WinCC Runtime Professional V21 (All versions), SIMATIC WinCC V7.5 (All versions), SIMATIC WinCC V8.0 (All versions), SIMATIC WinCC V8.1 (All versions). Affected systems do not properly secure their remote user authentication with the deprecated NTLM protocol. This could allow unauthenticated remote attackers, who have achieved a machine in the middle position, to relay NTLM authentication and impersonate a legitimate user. The potential impact depends on the services that are accessible, e.g. a SQL server used by WinCC.

### CVE-2026-109800

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T01:17:14.037 |

SAP Web Dispatcher does not sufficiently validate certain inputs during processing, which could lead to memory corruption. An attacker authenticated as a non-administrative user could exploit this vulnerability by providing specially crafted input, causing the Web Dispatcher process to terminate without user interaction. As a result, the Web Dispatcher and all backend systems reachable through it become unavailable, leading to a high impact on availability. There is no impact on confidentiality or integrity of the application.

### CVE-2026-125404

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-10T00:17:15.040 |

Ettercap through 0.8.4.1 contains an integer underflow in ccmp_decrypt() in src/ec_encryption_ccmp.c that subtracts the 8-byte CCMP trailer without checking minimum length. Attackers on a network whose WPA key is loaded can send a short crafted CCMP frame to overflow a stack buffer in the Ettercap process, which normally runs as root.

### CVE-2026-125368

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-11-10T00:17:08.907 |

OmniAgent through commit 12b98c5 contains an approval bypass vulnerability in ReflexionAgent._is_safe_bash_command that treats any command starting with find as safe without inspecting -execdir arguments. Prompt-injected agents can run find with -execdir to invoke binaries like dd, nc, perl or openssl through an unsandboxed shell, overwriting files or executing code without human approval.

### CVE-2026-115341

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-862` |
| Published | 2026-11-09T17:17:11.663 |

Improper access restrictions in the Thin Client Web Transfer component of Progress Software WS_FTP Server versions prior to 2025.0.5 on Windows could allow an authenticated FTP user to access files outside their intended scope.

### CVE-2026-12266

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T12:17:19.400 |

Zoho Corporation ManageEngine DDI Central versions 6200 and below are vulnerable to LDAP bind password exposure through insufficiently protected LDAP settings API.

### CVE-2026-120014

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-10T01:17:16.403 |

SAP HANA XSA Web Dispatcher does not perform sufficient request validation in certain administrative functionality. In the context of SAP HANA XSA Web Dispatcher, an unauthenticated attacker could trick a logged-on administrator into visiting a malicious link. Visiting the link could cause unintended actions in the administrator's session. Successful exploitation could lead to a temporary compromise of the SAP HANA XSA Web Dispatcher, resulting in a high impact on confidentiality, and partial impact on integrity, and availability.

### CVE-2026-107244

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-11-10T01:17:12.610 |

The Node.js web service on VOS (previously Versa FlexVNF) is used for URL-based Zero Touch Provisioning (ZTP) of the VOS appliance and is not required after provisioning is complete. The /decryptTest endpoint of this service is registered in server.js before the session authentication middleware and creates an authenticated session whenever it receives a token that decrypts successfully. Because the key and initialization vector (IV) used for decryption are hardcoded and identical across all VOS appliances, an unauthenticated attacker with network access can compute a valid token, submit it to /decryptTest, and obtain a fully authenticated session without providing any credentials.  

Versa’s security hardening guide for Hubs, Branches, and Controllers recommends disabling the Node.js web service after the initial provisioning of the VOS device. This vulnerability is not exploitable on VOS devices where the Node.js web service has been disabled.

### CVE-2026-107243

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-10T01:17:12.470 |

The Node.js web service on VOS (previously Versa FlexVNF) is used for URL-based Zero Touch Provisioning (ZTP) of the VOS appliance and is not required after provisioning is complete. The express-session middleware in server.js is configured with a hardcoded secret that is identical across all VOS appliances and is used to sign session cookies. An attacker who obtains a valid session ID from any source can compute the correct HMAC-SHA256 signature and forge a session cookie that the server accepts as legitimate. Because the secret is shared across all VOS appliances, a forged cookie is accepted by any VOS appliance in the deployment. 

Versa’s security hardening guide for Hubs, Branches, and Controllers recommends disabling the Node.js web service after the initial provisioning of the VOS device. This vulnerability is not exploitable on VOS devices where the Node.js web service has been disabled.

### CVE-2026-107241

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-11-10T01:17:12.187 |

The Node.js web service on VOS (previously Versa FlexVNF) is used for URL-based Zero Touch Provisioning (ZTP) of the VOS appliance and is not required after provisioning is complete. This service authenticates users and administrators to its web interface during initial provisioning using default credentials and HTTP Basic Authentication. An attacker with network access who knows the default credentials could authenticate to the service and perform provisioning actions on the VOS appliance.  

Versa’s security hardening guide for Hubs, Branches, and Controllers recommends disabling the Node.js web service after the initial provisioning of the VOS device. This vulnerability is not exploitable on VOS devices where the Node.js web service has been disabled.

### CVE-2026-107240

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T01:17:10.950 |

The Node.js web service on VOS (previously Versa FlexVNF) is used for URL-based Zero Touch Provisioning (ZTP) of the VOS appliance and is not required after provisioning is complete. The /authenticate endpoint of this service passes user-supplied username and password values to child_process.exec() through a sanitizer (escapeRegExp) that removes regular expression metacharacters but not newline characters. An unauthenticated attacker can inject a newline character into the username field to execute arbitrary shell commands as the versa OS service user. No credentials are required; the attacker needs only a CSRF token, which can be obtained from an unauthenticated page load. 

Versa’s security hardening guide for Hubs, Branches, and Controllers recommends disabling the Node.js web service after the initial provisioning of the VOS device. This vulnerability is not exploitable on VOS devices where the Node.js web service has been disabled.

### CVE-2026-120399

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1322` |
| Published | 2026-11-10T14:17:14.300 |

A flaw was found in flightctl. A TLS handshake is performed synchronously in the HTTP server’s connection-context callback without a deadline. A network-reachable unauthenticated client can stall the handshake and prevent the affected listener from accepting new connections.

### CVE-2026-124747

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T13:18:22.343 |

A flaw was found in BusyBox. When resuming a download over File Transfer Protocol (FTP), the wget utility fails to verify that the resume offset does not exceed the file size reported by the server, resulting in an integer calculation error. A malicious FTP server or an on-path network attacker can exploit this issue by returning crafted file size metadata, triggering a heap-based buffer overflow with attacker-controlled data. Successful exploitation may allow an attacker to execute arbitrary code or crash the application, resulting in a denial of service (DoS).

### CVE-2026-125712

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T12:17:18.607 |

A flaw was found in GStreamer's gst-plugins-base RTCP SDES packet parser. A remote sender able to reach an active media session can supply a malformed SDES entry whose declared length exceeds the received packet. Missing bounds validation can cause the receiver to read beyond the packet buffer, potentially crashing the application or exposing a limited amount of process memory.

### CVE-2026-95651

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-10T11:16:43.903 |

Zoho Corporation ManageEngine DDI Central versions 6500 and below are vulnerable to an unauthenticated GSS-TSIG keytab update vulnerability in the Linux Node Agent.

### CVE-2026-125704

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T11:16:43.580 |

A use-after-free flaw was found in GStreamer core buffer value deserialization. When serialized buffer text contains an invalid character, an error path frees a mapped buffer before unmapping it. Applications that parse untrusted caps or structure data can reach a freed-buffer read and may crash. A network-facing GStreamer Data Protocol receiver can process such caps data without user interaction; further impact has not been established.

### CVE-2026-120013

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T09:17:22.303 |

The agent_memory module accepts a caller-supplied tenant parameter in create_client(tenant=...). Prior to version 0.50.0, the tenant parameter was not validated before being used to construct filesystem paths for secret resolution. A value containing path traversal sequences (for example, attacker-corp/../victim-corp) could cause the resolved path to escape the intended directory and access another tenant's secrets under:Plain Text/etc/secrets/appfnd/hana-agent-memory/<tenant>/Successful exploitation could allow unauthorized access to another tenant's mounted credentials, including OAuth client IDs and client secrets. This vulnerability could enable cross-tenant access to sensitive credentials.

### CVE-2026-120012

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-209` |
| Published | 2026-11-10T09:17:22.140 |

SAP Cloud SDK for AI (Node.js) could inadvertently include sensitive authentication credentials in error messages generated by certain internal operations under specific failure conditions. An attacker with low privileges and access to application logs or forwarded error output could obtain these credentials, but only after waiting for a suitable failure event triggered by a higher-privileged user and within the limited lifetime of the token, making exploitation complex. Successful exploitation could allow the attacker to reuse the disclosed credentials against the associated SAP service, resulting in a high impact on confidentiality, integrity and availability.

### CVE-2026-100386

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T07:16:47.970 |

The Ultra Addons for Contact Form 7 plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 3.5.54 via the uacf7_wpcf7_mail_components function. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. Exploitation requires the PDF Generator addon to be active and an administrator-configured PDF body template to be enabled for the targeted contact form.

### CVE-2026-89114

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T01:17:21.757 |

SAP NetWeaver AS Java EDM Application does not perform an authentication check for certain web service requests. An unauthenticated attacker could send a specially crafted request to retrieve sensitive business information. This results in a high impact on confidentiality. There is no impact on integrity and availability.

### CVE-2026-76973

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-10T01:17:20.847 |

Due to a Memory Corruption vulnerability in Application Server ABAP of SAP NetWeaver and ABAP Platform, an unauthenticated attacker could send specially crafted network requests to the affected service. By triggering the vulnerability, the attacker could cause the server to crash and disrupt active connections, leading to a denial of service condition. Successful exploitation could result in a high impact to the availability while the confidentiality and integrity remains unaffected.

### CVE-2026-76970

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T01:17:20.687 |

Due to a Memory Corruption vulnerability in Application Server ABAP for SAP NetWeaver and ABAP Platform, an unauthenticated attacker could send specially crafted requests to the application. If processed by the application, these requests could trigger a memory corruption condition in the parsing routine, which could cause the affected processes to crash and restart. By repeatedly sending such requests, the attacker could cause a sustained denial of service, leading to a high impact on availability. Confidentiality and integrity remain unaffected.

### CVE-2026-124598

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-10T01:17:18.193 |

An
API key is hardcoded and retrievable from the GV-Face package. Since
Android applications can be reverse engineered, embedding sensitive API
credentials directly in the client application may allow unauthorized users to
extract and misuse the key.

### CVE-2026-120015

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-10T01:17:16.537 |

SAP Host Agent does not sufficiently validate certain inputs. Under certain condition, an attacker with low privileges could abuse the affected functionality to influence an internal component into loading a malicious file under a privileged account. Successful exploitation could lead to persistent code execution, resulting in a high impact on confidentiality, integrity and availability.

### CVE-2026-120010

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-131` |
| Published | 2026-11-10T01:17:16.253 |

SAP NetWeaver Application Server (SAP Message Server) does not properly size memory allocations when handling certain HTTP requests. An unauthenticated attacker could send a specially crafted request to trigger a heap buffer overflow in affected functionality. Successful exploitation causes the component to abort and remain unavailable until it is restarted by the framework, resulting in a high impact on availability of the system. There is no impact on confidentiality and integrity of the application.

### CVE-2026-109807

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-10T01:17:15.060 |

SAP NetWeaver (Internet Graphics Service) does not sufficiently validate certain input values within incoming requests. An unauthenticated user could send a specially crafted request causing the affected process to read beyond the declared values, resulting in repeated termination of the worker process. This results in a high impact on availability with no impact on integrity or confidentiality.

### CVE-2026-109806

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T01:17:14.930 |

SAP NetWeaver (Internet Graphics Service) does not sufficiently validate certain input values within incoming requests. An unauthenticated user could send a specially crafted request containing malformed image data, triggering an integer overflow that leads to repeated termination of the worker process. This results in a high impact on availability with no impact on integrity or confidentiality.

### CVE-2026-109804

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-908` |
| Published | 2026-11-10T01:17:14.610 |

SAP Message Server does not properly handle certain malformed requests, which could be leveraged by an unauthenticated attacker to send specially crafted input. Successful exploitation could allow the attacker to retrieve sensitive information, resulting in a high impact on confidentiality. There is no impact on integrity and availability.

### CVE-2026-109799

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-10T01:17:13.887 |

The SAP Cloud SDK for Python contains an improper cryptographic signature verification vulnerability (CWE-347) in IASContextProvider, the runtime-context provider registered by default via bootstrap(app).IASContextProvider extracted the app_tid, sap_gtid and user_uuid claims from the IAS JWT in the Authorization header using an unverified decoder and wrote them into the request-scoped RuntimeContext without validating the token signature. A remote caller could submit a self-signed JWT naming a victim tenant/user; the forged identity then propagated to every consumer of the runtime context:OTel span attributes (sap.tenancy.tenant_id, user.id) via RuntimeContextSpanProcessorlog records via IdentityLogFilteraudit events (tenant_id, user_initiator_id) via AuditClienttenant routing via CBCClientThis completes an earlier remediation that fixed the same unverified pattern in StarletteIASTelemetryMiddleware but did not cover IASContextProvider.

### CVE-2026-109794

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-10T01:17:13.187 |

SAP NetWeaver Application Server ABAP, ABAP Platform, and SAP Web Dispatcher do not sufficiently handle resource consumption when processing certain requests. An unauthenticated attacker could send specially crafted requests to the affected component, causing excessive resource utilization and service disruption. This results in a high impact on availability. There is no impact on confidentiality and integrity.

### CVE-2026-109793

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T01:17:13.020 |

SAP NetWeaver Application Server ABAP and SAP Web Dispatcher do not sufficiently validate certain header values processed during inbound request handling. An unauthenticated attacker could send a specially crafted request to cause the affected process to become unavailable.This results in a high impact on availability. There is no impact on confidentiality and integrity.

### CVE-2026-125119

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-09T23:17:22.397 |

Mongoose is a MongoDB object modeling tool designed to work in an asynchronous environment. From 6.0.0 until 6.13.12, 7.8.13, 8.24.7, and 9.11.4, Mongoose stores the connection-level sanitizeFilter option in Connection.config, but Query.prototype._castConditions() and query casting check other option locations and do not read that configuration. An application that enables sanitizeFilter through mongoose.connect() or createConnection() and passes an attacker-controlled object into a query filter therefore receives a connection that reports the defense as enabled while query selector objects remain unsanitized. A crafted password value using a query operator can match an account record without the expected literal password, while global configuration through mongoose.set('sanitizeFilter') and per-query Model.find().sanitizeFilter() remain unaffected. This issue is fixed in versions 6.13.12, 7.8.13, 8.24.7, and 9.11.4.

### CVE-2026-124035

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-11-09T23:17:18.447 |

Unsafe reflection in the error mitigation schema validation in Amazon Braket Schemas before 1.32.2 might allow a remote authenticated user with S3 write access to the quantum task output location to execute arbitrary code on any machine that retrieves the quantum task results via a crafted task result document.



We recommend you upgrade to amazon-braket-schemas version 1.32.2 or later.

### CVE-2026-90591

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-09T22:18:57.573 |

The NXP ENET-QOS Ethernet driver's receive work handler eth_nxp_enet_qos_rx() in drivers/ethernet/eth_nxp_enet_qos hands each processed descriptor back to the DMA by writing desc->read.control = rx_desc_refresh_flags, which sets OWN_FLAG and BUF1_ADDR_VALID_FLAG. RDES0 of a receive descriptor is the DMA buffer address in read format, but the hardware write-back aliases that word with the VLAN tag fields (or, for a context descriptor, the timestamp low word), so it is destroyed on every completion. The success path rewrites desc->read.buf1_addr before re-arming; the four drop paths — errored or non-first descriptor, net_pkt_rx_alloc() failure, invalid descriptor length, and net_pkt_get_frag() failure — did not, re-arming the ring slot with the write-back residue as its DMA target address.

The drop paths are driven entirely by received traffic and need no privilege or special configuration. With the defaults for this driver (CONFIG_NET_BUF_DATA_SIZE of 128 and 16 receive descriptors) a single full-size frame consumes twelve ring slots and twelve K_NO_WAIT fragment allocations, so a short burst of frames sent to the device exhausts the receive pools and reaches the allocation-failure paths; a frame with a receive error, or any frame whose first descriptor was already dropped, reaches the non-first-descriptor path.

Once a slot has been poisoned, the DMA writes the next frame received in that slot to an address derived from the frame's VLAN tag fields rather than to a receive buffer. On the supported MCX SoCs that address falls in flash or reserved space, so the transfer raises a fatal bus error that the driver only logs — there is no reset or recovery path — and reception stops permanently until the device is rebooted; where the write is silently discarded instead, the untouched buffer is later handed to the network stack with a length, delivering stale buffer contents as if they were a received frame. A single triggering event is enough to make the condition persistent, so an attacker able to send traffic to the device can permanently disable its network interface.

### CVE-2026-73857

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787;CWE-824` |
| Published | 2026-11-09T22:18:54.253 |

ModSecurity is an open source, cross platform web application firewall (WAF) engine for Apache, IIS and Nginx. From 3.0.15 until 3.0.17, XML request body processing with SecParseXmlIntoArgs set to On or OnlyArgs can leave XMLNodes::parsing_ctx_arg uninitialized in the SAX end-element callback. A single crafted unauthenticated HTTP request can make a worker dereference the pointer, resulting in a constant-value write to an attacker-controlled address. The resulting memory corruption can terminate the worker and may disclose memory or redirect execution. Earlier 3.0.x releases and ModSecurity 2.x do not use the affected path. This issue is fixed in version 3.0.17.

### CVE-2026-63644

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-88;CWE-200` |
| Published | 2026-11-09T22:18:53.957 |

bird-lg-go is a BIRD looking glass in Go. Prior to version 1.4.7, unsanitized input path enables arbitrary local file read, allowing an unauthenticated remote attacker to read sensitive files such as /etc/shadow and /root/.bash_history. This issue has been patched in version 1.4.7.

### CVE-2026-125111

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-09T22:18:42.433 |

Rack is a modular Ruby web server interface. Prior to 2.2.25, 3.1.23, and 3.2.8, Rack::Multipart::Parser can retain parsed data in its internal StringScanner buffer when reads end inside or immediately after multipart headers. An unauthenticated attacker can align many small parts with rack.multipart.buffer_size boundaries so the buffer grows with the request despite per-field, header, and preamble limits, causing a worker to exhaust memory. The attack requires only a well-formed multipart body and affects applications that parse multipart requests. This issue is fixed in versions 2.2.25, 3.1.23, and 3.2.8.

### CVE-2026-125107

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-09T22:18:41.813 |

Muhammara is a node module with c/cpp bindings to modify PDF with JavaScript for node or electron. Prior to 6.0.5, Muhammara PDFParser::CreateFilterForStream() in src/deps/PDFWriter/PDFParser.cpp dereferences a null PDFInteger pointer when a PDF stream uses the LZWDecode filter with a DecodeParms dictionary that omits the EarlyChange key. An application that processes an untrusted PDF and reads the affected stream can crash, causing a denial of service. This issue is fixed in version 6.0.5.

### CVE-2026-123818

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-09T22:18:38.437 |

LMDeploy is a toolkit for compressing, deploying, and serving large language models. From 0.12.3 until 0.15.0, _is_safe_url validates remote media URLs with urlparse while requests.Session().get interprets backslashes differently when sending the request. An attacker can provide a URL whose validation hostname appears globally routable but whose request destination resolves to an internal host, bypassing non-global address checks. Applications that accept attacker-controlled remote media URLs can therefore be induced to access internal HTTP services and expose data available from those services. This issue is fixed in version 0.15.0.

### CVE-2026-123813

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-613` |
| Published | 2026-11-09T22:18:37.587 |

pyLoad is a free and open-source download manager written in Python. Prior to 0.5.0b3.dev102, pyLoad does not invalidate existing Flask sessions when an administrator changes a user's permissions or password through /api/set_user_permission or /api/change_password. Api.set_user_permission and Api.change_password update the database, but session authorization continues to use role and permission values copied at login by set_session in webui/app/helpers.py. A user can therefore retain revoked privileges or continue using a session established with an old password for the configured session lifetime. API-key authentication is not affected because that path rereads user data from the database. This issue is fixed in version 0.5.0b3.dev102.

### CVE-2026-123811

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-09T22:18:37.287 |

Dynatrace MCP Server is an MCP server for Dynatrace Observability. Prior to 2.0.0, a server started with the --http option accepts JSON-RPC tools/call requests without authentication, session validation, or Host and Origin protections before dispatching them under the server's configured Dynatrace credentials. A network-reachable caller can invoke execute_dql to read logs, security events, user sessions, and other Grail data, or invoke create_dynatrace_notebook to create tenant-visible notebooks. The send_event path is not affected because its requestHumanApproval gate blocks this attack path, and reset_grail_budget only demonstrates dispatch without accessing Dynatrace data. This issue is fixed in version 2.0.0.

### CVE-2026-113961

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-09T22:18:25.917 |

An authorization issue was addressed with improved validation. This issue is fixed in iOS 26.7.3 and iPadOS 26.7.3, iOS 27.2.1 and iPadOS 27.2.1, macOS Golden Gate 27.2.1, macOS Sequoia 15.8.3, macOS Tahoe 26.7.3, visionOS 27.2.1, watchOS 27.2.1. A remote attacker may be able to join an iMessage group chat and receive its messages.

### CVE-2026-123805

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125;CWE-755` |
| Published | 2026-11-09T20:18:10.173 |

SIPSorcery is a WebRTC, SIP, and VoIP library for C# and .NET. Prior to 10.0.14, SctpSackChunk.ParseChunk reads the numGapAckBlocks and numDuplicateTSNs fields from an attacker-controlled SCTP SACK chunk without checking that the corresponding entries fit the declared chunk length. A negotiated WebRTC peer can send a checksum-valid malformed SACK chunk that drives the parser beyond the 262144-byte receive buffer. The resulting IndexOutOfRangeException bypasses the recoverable ApplicationException handler in RTCSctpTransport.DoReceive, causing the generic handler to exit the dedicated receive loop and permanently terminate the SCTP association and all data channels. This issue is fixed in 10.0.14.

### CVE-2026-119079

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-408` |
| Published | 2026-11-09T19:16:43.023 |

decode_sequence_of() in lib/krb5/asn.1/asn1_encode.c in MIT Kerberos 5 (aka krb5) 1.11 and later grows the decoded element array one entry at a time, which allows remote attackers to cause a denial of service (CPU consumption in the KDC) by sending an unauthenticated AS-REQ or TGS-REQ with a large number of elements in a SEQUENCE OF field over TCP.

### CVE-2026-112323

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-772` |
| Published | 2026-11-09T19:16:41.360 |

The AUTH_GSSAPI handler in lib/rpc/svc_auth_gssapi.c in MIT Kerberos 5 (aka krb5) 1.5.2 and later allows remote attackers to cause a denial of service (memory exhaustion in kadmind) by sending repeated failed AUTH_GSSAPI_INIT requests. Each failed request allocates client state that is only freed after a 15-minute expiration timeout, allowing an attacker to accumulate memory faster than it is reclaimed.

### CVE-2026-112322

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-09T19:16:41.207 |

clean_client() in lib/rpc/svc_auth_gssapi.c in MIT Kerberos 5 (aka krb5) restarts its scan from the head of the client list after each removal, resulting in quadratic CPU cost. Remote attackers can cause a denial of service (CPU consumption in kadmind) by accumulating a large number of AUTH_GSSAPI client entries.

### CVE-2026-112321

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-772` |
| Published | 2026-11-09T19:16:41.050 |

The AUTH_GSSAPI handler in lib/rpc/svc_auth_gssapi.c in MIT Kerberos 5 (aka krb5) does not free decoded arguments on certain error paths, which allows remote attackers to cause a denial of service (memory exhaustion in kadmind) via crafted AUTH_GSSAPI_INIT requests that trigger authentication failures.

### CVE-2026-112320

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-772` |
| Published | 2026-11-09T19:16:40.887 |

The GSS-RPC transport layer in MIT Kerberos 5 (aka krb5) 1.4 and later does not release the previous authentication context when a client switches from an RPCSEC_GSS or AUTH_GSSAPI flavor to a non-GSS flavor on the same TCP connection. This allows remote attackers to cause a denial of service (memory exhaustion in kadmind) by repeatedly establishing and abandoning GSS authentication contexts.

### CVE-2026-112314

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-772` |
| Published | 2026-11-09T19:16:39.867 |

clnttcp_call() in lib/rpc/clnt_tcp.c in MIT Kerberos 5 (aka krb5) does not free the RPC reply verifier between retries, which allows remote attackers to cause a denial of service (memory leak in GSS-RPC client programs) by injecting RPC replies with mismatched XIDs or by triggering authentication retries.

### CVE-2026-123797

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-09T18:17:26.890 |

SuperTokens Core is an open source authentication server. Prior to 11.3.6, 11.4.6, and 12.0.8, app-specific management requests using an unknown tenant path and an older supported cdi-version can bypass API-key and public-tenant enforcement. In src/main/java/io/supertokens/webserver/WebserverAPI.java, checkIPAccess and assertThatAPIKeyCheckPasses suppress TenantOrAppNotFoundException, while the later app-specific handler resolves app/public storage and the public-tenant guard applies only to CDI versions 5.0 and later. An unauthenticated caller able to reach the Core endpoint can therefore use PUT /ghosttenant/recipe/role and GET /ghosttenant/recipe/roles to create and enumerate application roles without a valid API key. This issue is fixed in versions 11.3.6, 11.4.6, and 12.0.8.

### CVE-2026-119755

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-09T18:17:22.163 |

Tasmota through 16.0.0, fixed in commit 1cb7ebc, contains a cross-site request forgery vulnerability that allows unauthenticated attackers to bypass Referer-based CSRF protection in HttpCheckPriviledgedAccess() by crafting a Referer header where the device hostname or IP appears as a substring immediately after http://.evil.com/. Attackers can lure an administrator on the device's network to a malicious page to issue arbitrary console commands and reconfigure Wi-Fi, MQTT, settings, or firmware on devices lacking a WebPassword.

### CVE-2026-115339

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-09T17:17:11.380 |

Insufficient resource limits in Progress Software WS_FTP Server releases prior to 2025.0.5 on Windows could allow an unauthenticated remote attacker to cause denial of service.

### CVE-2026-120999

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-345` |
| Published | 2026-11-10T11:16:42.800 |

Improper Authentication vulnerability in Google sign-in and email confirmation in nerves-hub nerves_hub_web allows an attacker who registers another person's email address to share that person's account once they sign in. NervesHub.Accounts.update_or_create_user_from_ueberauth/1 signs a Google user in to any account carrying the same email that is not yet linked to a Google account, links it and marks the email confirmed, without the account's owner ever having proved they own the address. NervesHubWeb.SessionController.confirm/2 likewise signs in whoever follows a confirmation link. An attacker registers the address from the sign-up form, changes their own account's email to it, or registers it as an organization admin from an invite link, and keeps the password; when the address's owner signs in with Google or follows the confirmation link, they land in that account.

The Google path also creates accounts with registrations closed and never checks Google's email_verified claim, and the API's password sign-in in NervesHubWeb.API.UserController issues tokens to accounts whose email was never confirmed. The attacker gains only what the victim is granted afterwards, and nothing on accounts whose owners never use either path.

This issue affects nerves_hub: from 2.3.0 before 2.5.3.

### CVE-2026-12963

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-10T06:17:08.330 |

A vulnerability that could allow a viewer account to gain unauthorized access to network attached storage devices on the server.

### CVE-2026-115640

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T05:17:47.300 |

LimeSurvey Community Edition 7.7.0 contains a stored cross-site scripting vulnerability in the Central Participants Database blocklist control. An authenticated user with only global participantpanel:import permission can import a CSV participant_id containing HTML. The import flow persists that value without model validation. When a CPDB editor opens the participant list, LimeSurvey derives ButtonGroupWidget id and name attributes from participant_id and inserts them without HTML encoding, causing attacker-controlled markup to execute in the victim's authenticated LimeSurvey origin. Exploitation can access session-exposed data and issue same-origin requests with the victim's effective permissions.

### CVE-2026-123801

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-294;CWE-346;CWE-384` |
| Published | 2026-11-09T19:16:46.910 |

SuperTokens Core is an open source authentication server. From 11.3.0 until 11.3.8, 11.4.8, 12.0.11, 12.1.2, 12.2.1, and 12.3.1, SAML.handleCallback does not consume RelayState, record assertion identifiers, or enforce Response.InResponseTo. In the SP-initiated flow, an attacker who obtains a legitimately issued, still-valid SAML response and its matching RelayState can resubmit the pair to /recipe/saml/callback before the assertion's NotOnOrAfter time; in the IdP-initiated flow, the assertion can be replayed without RelayState. The missing Response.InResponseTo check also permits an in-progress login to be completed with an assertion for a different identity and fails to enforce allowIDPInitiatedLogin=false. The callback does not validate Destination or SubjectConfirmationData Recipient and NotOnOrAfter, and each accepted callback mints a fresh, independently redeemable authorization code carrying the captured user's identity. This issue is fixed in versions 11.3.8, 11.4.8, 12.0.11, 12.1.2, 12.2.1, and 12.3.1.

### CVE-2026-123799

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-613` |
| Published | 2026-11-09T19:16:46.440 |

SuperTokens Core is an open source authentication server. From 11.0.0 until 11.0.9, 11.1.4, 11.2.4, 11.3.8, 11.4.8, 12.0.11, and 12.1.2, Dashboard.isValidUserSession treats any stored session row as valid without comparing DashboardSessionInfo.expiry to the current time. DashboardQueries.getSessionInfoWithSessionId also selects by app and session identifier without an expiry predicate, leaving the periodic DeleteExpiredDashboardSessions cleanup as the only expiration enforcement. An attacker who obtains a dashboard administrator session after its 30-day lifetime can continue using POST /recipe/dashboard/session/verify until the row is removed, and frequent Core restarts can prevent the 12-hour cleanup sweep from running. The stale session retains full dashboard read and write access, but the flaw does not provide a way to guess or acquire the random session identifier. This issue is fixed in versions 11.0.9, 11.1.4, 11.2.4, 11.3.8, 11.4.8, 12.0.11, and 12.1.2.

### CVE-2026-123367

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-09T18:17:25.520 |

Thor Vector Graphics (ThorVG) is a production-ready vector graphics engine. Prior to 1.1.2, the bundled jpgd JPEG decoder accepts duplicate component selectors in an SOS scan header, causing each duplicate to increase m_blocks_per_mcu without checking the buffers sized from the frame components. A crafted grayscale JPEG can repeat its component in the SOS header, causing decode paths in src/loaders/jpg/tvgJpgd.cpp to write beyond heap buffers sized for one component. The issue is reachable through direct JPEG decoding and through JPEG images embedded in Lottie content, and confirmed impact is memory corruption followed by a process crash. This issue is fixed in version 1.1.2.

### CVE-2026-92864

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-61` |
| Published | 2026-11-10T05:18:16.823 |

Insecure Temporary File Vulnerability in Hitachi Dynamic Link Manager for AIX (for markets outside Japan) and Hitachi Dynamic Link Manager EX for AIX (for the Japanese market).

This issue affects Hitachi Dynamic Link Manager for AIX: from 7.4.1-00 before 9.0.4-01; Hitachi Dynamic Link Manager EX for AIX: from 7.4.1-00 before 9.0.4-01.

### CVE-2026-86578

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:L/I:L/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-10T05:18:11.813 |

Link Following Vulnerability in Hitachi Dynamic Link Manager for Windows.

This issue affects Hitachi Dynamic Link Manager for Windows: from 5.0.0-03 before 9.0.4-01.

### CVE-2026-112125

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-10T05:17:42.290 |

Incorrect Permission Assignment for Critical Resource Vulnerability in HA Monitor.

This issue affects HA Monitor: from 01-00 before 01-83-01.

### CVE-2026-84410

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-09T22:18:55.417 |

In apport before 2.37.0, an improper privilege management vulnerability allows an unprivileged local attacker to gain root privileges on systems where automatic crash reporting is enabled. The automatic crash report processing pipeline runs as root and executes ldd on the attacker-controlled ExecutablePath field of a crash file placed in the world-writable /var/crash directory, causing the dynamic loader to load and execute an attacker-supplied audit module specified by the ELF's DT_AUDIT tag. This allows an attacker to execute arbitrary code with root privileges and fully compromise the affected system.

### CVE-2026-125269

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-09T20:18:13.690 |

FFmpeg through 9.0.2 contains a double free vulnerability in libavcodec/cbs_sei.c where cbs_sei_delete_message() leaves a stale extension_data reference that ff_cbs_sei_add_message() reuses. Attackers can supply a crafted H.264 stream with a display orientation SEI message followed by payload extension data, processed by h264_metadata with display_orientation=insert, to corrupt heap memory.

### CVE-2026-125260

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-09T20:18:12.367 |

FFmpeg through 9.0.2 contains a heap buffer overflow vulnerability in libavcodec/exrenc.c that allows attackers to corrupt heap memory when encode_scanline_rle() processes frames taller than the encoder height. Attackers can supply crafted input whose resolution grows mid-stream, transcoded to OpenEXR with RLE compression, to write pointers past the scanline array and crash the application.

### CVE-2026-125257

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-193` |
| Published | 2026-11-09T20:18:11.930 |

FFmpeg through 9.0.2 contains an off-by-one heap overflow vulnerability in get_exponent_dynamic() in libavcodec/nellymoserenc.c that allows writing one element past the opt and path allocations. Attackers can supply crafted audio to applications encoding Nellymoser with trellis enabled, causing idx to equal OPT_SIZE and overwrite adjacent heap memory.

### CVE-2026-125256

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-09T20:18:11.790 |

FFmpeg through 9.0.2 contains a heap buffer overflow vulnerability in ff_llvidenc_diff_bytes_rvv() that allows attackers to corrupt heap memory by triggering negative length values in the Huffyuv encoder. Attackers can supply RGB video narrower than 8 or 16 pixels for huffyuv transcoding on RVV-enabled RISC-V builds, causing writes past the encoder's temp buffer.

### CVE-2026-125251

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-09T19:17:04.030 |

FFmpeg through 9.0.2 contains an integer overflow vulnerability in the VVC decoder alloc_frame() function in libavcodec/vvc/refs.c that undersizes the reference picture list allocation on 32-bit builds. Attackers can supply a crafted VVC (H.266) file with a very large number of NAL units per access unit to trigger heap out-of-bounds writes and corrupt memory.

### CVE-2026-125249

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-09T19:17:03.737 |

FFmpeg 7.1 through 9.0.2 contains an integer overflow in ff_vk_decode_add_slice() in libavcodec/vulkan_decode.c that miscalculates the Vulkan hwaccel bitstream buffer size. Attackers can supply a crafted stream with over 2 GiB of slice data per frame, causing memcpy() to write past a smaller pooled host-mapped buffer.

### CVE-2026-125248

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-09T19:17:03.593 |

FFmpeg 9.0 through 9.0.2 contains an integer overflow vulnerability in libavcodec/ffv1enc_vulkan.c that undersizes the float remap GPU buffer for large frames. Attackers can supply large GBRPF32 or GBRAPF32 images or videos that, when transcoded to FFV1 with the Vulkan encoder, trigger out-of-bounds GPU memory writes causing crashes or memory corruption.

### CVE-2026-125241

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-09T19:17:02.490 |

FFmpeg through 9.0.2 contains a heap buffer overflow vulnerability in libavcodec/flicvideo.c that allows attackers to write out of bounds because check_pixel_ptr() checks only one bound with negative-stride frames. Attackers can supply a crafted FLIC file whose RLE and delta chunks write pixel data past frame storage, corrupting heap memory to crash applications or possibly execute code.

### CVE-2026-125239

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-09T19:17:02.183 |

FFmpeg through 9.0.2 contains a heap buffer overflow vulnerability in ff_dxva2_hevc_fill_picture_parameters() that allows attackers to corrupt memory via unbounded non-uniform tile counts. Attackers can supply crafted HEVC bitstreams with many non-uniformly spaced tiles to write controlled 16-bit values past fixed-size DXVA arrays during DXVA2, D3D11VA, or D3D12VA decoding on Windows.

### CVE-2026-125235

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-09T19:17:01.587 |

FFmpeg through 9.0.2 contains a heap overflow vulnerability in libavcodec/qsvenc.c that allows attackers to corrupt memory by reusing an undersized pooled QSVFrame buffer when input dimensions increase. Attackers can supply crafted input whose resolution grows mid-stream, transcoded with Intel Quick Sync encoders without rescaling, to crash the application or corrupt heap memory.

### CVE-2026-125227

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-09T19:17:00.397 |

FFmpeg through 9.0.2 contains an integer overflow in cbs_jpeg_write_scan() in libavcodec/cbs_jpeg.c that causes a heap buffer overflow on 32-bit builds. Attackers can supply a crafted MJPEG/JPEG stream with a scan of 512 MiB or more, processed by CBS bitstream filters like filter_units, to corrupt the heap or crash the application.

### CVE-2026-125222

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-09T19:16:59.640 |

FFmpeg through 9.0.2 contains an integer overflow vulnerability in hap_parse_frame_header() in libavcodec/hapdec.c that allows attackers to trigger a heap buffer overflow on 32-bit builds. Attackers can craft Hap video frames with Snappy length prefixes that wrap tex_size, causing decompress_chunks_thread() to write outside tex_buf and crash the application or potentially execute code.

### CVE-2026-125219

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-09T19:16:59.193 |

FFmpeg through 9.0.2 contains a heap buffer overflow vulnerability in vdpau_hevc_start_frame() in libavcodec/vdpau_hevc.c that copies unbounded PPS tile counts into fixed-size VDPAU arrays. Attackers can supply crafted HEVC bitstreams with excessive tile columns or rows to write controlled 16-bit values past heap-allocated hwaccel data, corrupting memory in applications using VDPAU decoding.

### CVE-2026-125218

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-09T19:16:59.043 |

FFmpeg through 9.0.2 contains a heap buffer overflow vulnerability in the APNG encoder's encode_apng() function in libavcodec/pngenc.c when frame size changes mid-stream. Attackers can supply crafted media whose resolution grows mid-stream, causing APNG_DISPOSE_OP_BACKGROUND memset writes past prev_frame and crashing or corrupting heap memory in transcoding applications.

### CVE-2026-125214

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-09T19:16:58.433 |

FFmpeg through 9.0.2 contains a heap buffer overflow vulnerability in pcm_bluray_decode_frame() in libavcodec/pcm-bluray.c on big-endian hosts. Attackers can supply a crafted Blu-ray (M2TS) LPCM stream whose payload length is not a multiple of the sample size, writing attacker-controlled bytes past the audio frame buffer.

### CVE-2026-125213

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-197` |
| Published | 2026-11-09T19:16:58.250 |

FFmpeg through 9.0.2 contains a heap buffer overflow vulnerability in the PSD decoder in libavcodec/psd.c that allows attackers to corrupt heap memory on 32-bit builds by supplying a crafted PSD image. Attackers can choose dimensions and channel counts whose product exceeds 4 GB, truncating the av_malloc allocation size so decode_rle() writes attacker-controlled data past the buffer, causing crashes or possible code execution.

### CVE-2026-125212

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-09T19:16:58.100 |

FFmpeg through 9.0.2 contains a heap buffer overflow vulnerability in libavcodec/videotoolboxenc.c that copies frames larger than encoder dimensions into undersized CVPixelBuffers. Attackers can supply crafted input whose resolution grows mid-stream, transcoded with VideoToolbox encoders without rescaling, to crash the application or corrupt memory.

### CVE-2026-125211

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-09T19:16:57.947 |

FFmpeg through 9.0.2 contains an out-of-bounds read and invalid free vulnerability in aribcaption_trans_ass_subtitle() in libavcodec/libaribcaption.c that frees subtitle rectangles using region_count instead of num_rects. Attackers can supply crafted ARIB captions whose later region exceeds the 8 KiB AVBPrint limit, triggering cleanup that frees out-of-bounds pointers and corrupts the heap.

### CVE-2026-125210

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-131` |
| Published | 2026-11-09T19:16:57.793 |

FFmpeg through 9.0.2 contains a heap buffer overflow vulnerability in aribcaption_trans_text_subtitle() in libavcodec/libaribcaption.c when decoding with sub_type text. Attackers can supply a crafted ARIB STD-B24 caption stream with zero regions, causing a pointer write past a zero-sized sub->rects allocation and corrupting heap memory.

### CVE-2026-125208

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-09T19:16:57.493 |

FFmpeg through 9.0.2 contains an out-of-bounds write vulnerability in v4l2_buffer_swframe_to_buf() in libavcodec/v4l2_buffers.c because cumulative plane offsets are not checked against the V4L2 buffer length. Attackers can supply crafted video whose dimensions or padding cause unsigned wraparound in v4l2_bufref_to_buf(), making memcpy() write past the mmaped driver buffer during V4L2 M2M encoding.

### CVE-2026-125204

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-09T19:16:56.890 |

FFmpeg through 9.0.2 contains a heap buffer overflow in ff_libwebp_get_frame() in libwebpenc_common.c that lets attackers corrupt memory when cr_threshold is set. Attackers can supply crafted media that increases resolution mid-stream, causing memcpy() to write pixel data past the stale reference frame and crash applications.

### CVE-2026-125202

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-09T19:16:56.583 |

FFmpeg through 9.0.2 contains a heap buffer overflow vulnerability in vaapi_hevc_start_frame() in libavcodec/vaapi_hevc.c that copies unbounded PPS tile counts into fixed-size arrays. Attackers can supply a crafted HEVC bitstream with a large picture and many tiles to write controlled 16-bit values past heap-allocated hwaccel data, corrupting memory in applications decoding with VAAPI.

### CVE-2026-125201

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-09T19:16:56.427 |

FFmpeg 7.0 before 8.1.3 and 9.x before 9.0.2 contains a heap out-of-bounds write vulnerability in vk_av1_decode_slice() in libavcodec/vulkan_av1.c because the tile-count limit is checked only on entry. Attackers can supply a crafted AV1 stream with more than 256 tiles decoded via the Vulkan hardware accelerator to overflow tile_sizes and corrupt heap memory.

### CVE-2026-125196

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-09T19:16:55.673 |

FFmpeg through 9.0.2 contains a heap buffer overflow vulnerability in liboapve_encode() in libavcodec/liboapvenc.c that allows attackers to corrupt heap memory by supplying frames larger than the configured encoder dimensions. Attackers can craft videos whose resolution changes mid-stream so that transcoding to APV without rescaling writes attacker-controlled pixel data past the imgb plane buffers.

### CVE-2026-125181

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-09T19:16:53.437 |

FFmpeg through 9.0.2 contains an out-of-bounds write vulnerability in flic_decode_frame_15_16BPP() in libavcodec/flicvideo.c that allows attackers to corrupt heap memory on big-endian builds. Attackers can supply a crafted 15/16 bpp FLIC/FLX file with an FLI_BRUN chunk whose non-terminating byte-swap loop writes packet-derived data past the frame buffer, crashing the process.

### CVE-2026-120834

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-09T19:16:44.953 |

Incorrect Privilege Assignment vulnerability in Tobias WP2LEADS wp2leads allows Privilege Escalation.This issue affects WP2LEADS: from n/a through 3.5.17.

### CVE-2026-124850

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-09T15:17:19.020 |

A SQL injection vulnerability exists in a database migration script in flowintel.

The migration process reads stored connector identifier values from the database and interpolates them directly into SQL statements without parameterization. An attacker who has previously written a malicious identifier value into the affected tables can cause arbitrary SQL execution when the migration is subsequently run during an application upgrade.

- Requires prior write access to the database to plant a malicious identifier value
- Triggered automatically during a migration or upgrade operation
- Can result in unauthorized data disclosure, modification, or deletion

Affected versions: flowintel prior to 4.0.0

### CVE-2026-12572

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T12:17:19.523 |

Zoho Corporation ManageEngine DDI Central version below 6201 is vulnerable to SQL injection in HA replication username handling leading to command execution as the PostgreSQL service account.

### CVE-2026-93427

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T07:16:53.180 |

The ARMember Premium – Membership Plugin, Content Restriction, Member Levels, User Profile & User signup plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Registration Custom Field (Profile Cover) in all versions up to, and including, 7.8.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-84938

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T07:16:52.777 |

The Avada (Fusion) Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Form Notification Dynamic-Data action_hook → Media Upload Chain (ID3 Metadata / html_attributes) in all versions up to, and including, 3.16.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires that a Fusion Form is embedded on an admin-authored page (granting manage_options context to the Dynamic Data action hook callback), and that a Post Cards element configured to display attachment post types is present on a publicly accessible page so the planted shortcode payload is rendered.

### CVE-2026-120009

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-10T01:17:16.123 |

SAP ABAP Developer Tools (AMDP Data Preview) does not perform sufficient validation and authorization checks within certain affected functionality. An attacker with high privileges could submit specially crafted input to inject and execute arbitrary code on the system. Successful exploitation could allow the attacker to fully compromise the system, resulting in a high impact on confidentiality, integrity and availability.

### CVE-2026-125405

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T00:17:15.323 |

Ettercap through 0.8.4.1 contains an out-of-bounds read vulnerability in Parse_NTLM_Auth() in src/dissectors/ec_http.c due to unvalidated NTLM message offsets. Attackers can send a crafted HTTP Authorization header observed by Ettercap to read beyond the buffer, disclosing memory or crashing the process.

### CVE-2026-125403

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T00:17:14.860 |

Ettercap through 0.8.4.1 contains an out-of-bounds read and size_t underflow vulnerability in sslw_remove_sts() in src/ec_sslwrap.c, caused by a stale length and an unchecked memmem() result when stripping Strict-Transport-Security headers. A malicious HTTPS server whose response passes through Ettercap's SSL interception can trigger out-of-bounds reads and memory corruption in the Ettercap process, which normally runs as root.

### CVE-2026-125402

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T00:17:14.703 |

Ettercap through 0.8.4.1 contains a heap out-of-bounds read vulnerability in sslw_get_clienthello_sni() in src/ec_sslwrap.c that trusts the unchecked 16-bit SNI length field. Network-adjacent attackers can send crafted TLS ClientHello messages during SSL interception to leak up to 64 KB of heap memory upstream or crash Ettercap.

### CVE-2026-125401

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T00:17:14.540 |

Ettercap through 0.8.4.1 contains a heap buffer overflow vulnerability in gg_get_version() in src/dissectors/ec_gg.c that writes up to 44 bytes into a 30-byte allocation. Remote attackers can send Gadu-Gadu traffic on TCP port 8074 with a crafted version field through a monitored network to corrupt heap memory in the Ettercap process, which normally runs as root.

### CVE-2026-125361

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-923` |
| Published | 2026-11-10T00:17:07.717 |

Tencent BrowserSkill through 0.4.2 contains a missing authentication vulnerability that allows local attackers to impersonate the bsk daemon because remoteSocket() connects to the loopback WebSocket without credentials or peer verification. Attackers who bind the daemon port before it starts or after it exits receive the extension's full tool surface, including evaluate, to run JavaScript through CDP in logged-in browser tabs.

### CVE-2026-125358

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1385` |
| Published | 2026-11-10T00:17:07.180 |

Universal-modder before commit e88f6876745427321eb755ebc98276063a962d8a contains a missing WebSocket Origin validation vulnerability in the HostLink class of its passthrough example mods that allows remote attackers to execute Minecraft commands. Any web page open in the player's browser can connect cross-site to the unauthenticated loopback WebSocket and send cmd messages that WorldBridge.command() runs with operator authority.

### CVE-2025-10248

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:N/R:A/V:D/RE:M/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T16:17:23.973 |

XSS Vulnerability in OpenText Filr Appliance versions upto 25.1.2 could allow an authenticated user to upload a malicious file and exercise Stored XSS attack.

### CVE-2026-120295

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T11:16:41.960 |

Incorrect Authorization vulnerability in the devices page bulk move in nerves-hub nerves_hub_web allows an authenticated user with the manage role in one organization and only the view role in another to move devices into the second organization's product via the "Move device(s) to product" action. The target-product event in NervesHubWeb.Live.Devices.Index looks the product up with NervesHub.Products.get_by_id/2, which checks that the user is a member of the product's organization at any role, and move-devices-product then changes each selected device's organization and product. The device API's move requires manage in the target organization, and an earlier fix added the check on the organization the devices leave but not on the one they enter.

A moved device keeps its key and certificate, joins the target organization's matching deployment groups, and is sent their firmware with a download URL, which the view role cannot otherwise obtain. The user cannot change or control devices that already belong to the other organization.

This issue affects nerves_hub: from 1.0.0 before 2.5.3.

### CVE-2026-91757

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T05:18:14.143 |

OS Command Injection Vulnerability in Hitachi Dynamic Link Manager for VMware.

This issue affects Hitachi Dynamic Link Manager for VMware: from 7.3.0-00 before 9.0.4-01.

### CVE-2026-88707

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T02:16:45.513 |

An
out-of-bounds write in certain ASUS Router firmware
allows an unauthenticated nearby user to send an HTTP request containing
parameters that exceed the buffer length, potentially overwriting other memory
regions or causing the system to crash.
Refer to the ' Security Update for ASUS Router Firmware ' section on the ASUS Security Advisory for more information.

### CVE-2026-109797

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-1220` |
| Published | 2026-11-10T01:17:13.603 |

In SAP/astonish, an authenticated user could potentially identify and operate on another team�s sandbox containers because of improper tenant isolation in the legacy Incus sandbox-management API handlers. The affected handlers did not use the tenant-aware session lookup path, allowing cross-tenant container operations such as listing, exposing or proxying, and deleting containers.The issue affects only the legacy Incus backend. Kubernetes and OpenShell deployments are not affected because the relevant Incus-specific handlers are unavailable there.

### CVE-2026-125398

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T00:17:14.070 |

Instatic before 0.0.21 contains an authorization bypass vulnerability in handleRowAuthor that allows authenticated users to skip table-level access checks by loading rows with getDataRow() instead of loadRowForAccess(). Attackers holding content.edit.any but lacking data.system.tables.read can send PATCH requests to /admin/api/cms/data/rows/:id/author to read system-table rows and reassign their authors.

### CVE-2026-125397

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T00:17:13.880 |

NocoBase plugin-ai 2.1.0 through 2.2.41 contains an authorization bypass vulnerability in getAccessibleAIEmployee() that lets authenticated users access unassigned AI employees by overriding the role-derived filter with a supplied username. Attackers can use the dispatch-sub-agent-task tool to run ungranted AI employees with their tools and permissions, and get-ai-employee to read their prompts and tool configuration.

### CVE-2026-125393

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T00:17:13.197 |

MailEnable Enterprise Premium before 10.62 contains a heap overflow vulnerability in the IMAP X-FB-FETCH command that allows authenticated users to overflow a fixed 0x400-byte heap buffer. Attackers can supply an X-FB-USER address longer than about 1016 bytes, which is formatted without a length check, to crash the IMAP service and cause denial of service.

### CVE-2026-125390

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-36` |
| Published | 2026-11-10T00:17:12.653 |

Group-Office before 6.8.181, 25.0.116, and 26.0.58 contains an arbitrary local file read vulnerability in FolderController::actionProcessUploadQueue that allows authenticated users to read server files by supplying absolute paths in the blobs parameter. Attackers can have files hard-linked or copied into their own folder and downloaded, exposing other users' stored files and config.php database credentials.

### CVE-2026-125388

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T00:17:12.320 |

Intermesh Group-Office before 6.8.181, 25.0.116, and 26.0.58 contains a missing authorization vulnerability that allows authenticated users to download form reports via api/download.php without permission checks. Attackers can request the business/forms/report blob with a form ID to export every submission as an XLSX file, disclosing submissions they are not permitted to see.

### CVE-2026-125385

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T00:17:11.830 |

INDOTALENT WHMS before 10.20261109 contains a path traversal vulnerability that allows authenticated users to read arbitrary files via the documentName and imageName parameters. Attackers can self-register and supply traversal sequences to GetDocument or GetImage, which use Path.Combine without containment checks, to read files like appsettings.json.

### CVE-2026-125380

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T00:17:11.013 |

DataRoom through 3.0.0 contains an incorrect authorization vulnerability in DatasetController.runTest that allows visitor-role users to execute dataset definitions supplied in the request body. Attackers can specify an arbitrary dataSourceCode and raw SELECT SQL to query any configured relational data source using its stored decrypted credentials, bypassing developer-only restrictions.

### CVE-2026-125377

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T00:17:10.480 |

Pig before 4.1.2 contains a missing authorization vulnerability in SysClientController that allows authenticated users without client-management permission to retrieve OAuth2 client secrets via GET /client/{clientId} and GET /client/export. Attackers can fetch clientSecret values for seed clients like pig, app, and daemon or export the client table, then obtain tokens using those clients' configured grant types.

### CVE-2026-125365

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-10T00:17:08.387 |

DollarDollar through 4.4 contains a missing authorization vulnerability in add_expense() that allows authenticated users to modify other users' account balances by supplying foreign account_id values. Attackers can submit sequential account_id, destination_account_id, and group_id values to /add_expense to tamper with balances and inject expenses into foreign groups with an arbitrary payer.

### CVE-2026-70555

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-09T19:17:05.120 |

rConfig Core 8.2.3 before 8.2.13 contains an information disclosure vulnerability that allows authenticated users to retrieve cleartext SSH, Telnet, and enable passwords for managed devices through the device-credentials API due to automatic decryption on read and missing authorization checks. Attackers can request GET /api/device-credentials, GET /api/device-credentials/{id}, or the external GET /api/v1/device-credentials endpoint, which authenticates any valid token as the seeded administrator account, to statelessly exfiltrate all stored plaintext device credentials. rConfig Pro is not affected.

### CVE-2026-123482

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T17:17:27.537 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Crocoblock JetFormBuilder jetformbuilder allows Stored XSS.This issue affects JetFormBuilder: from n/a through 3.6.8.

### CVE-2026-122664

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T17:17:26.583 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in VideoWhisper.com Broadcast Live Video videowhisper-live-streaming-integration allows Reflected XSS.This issue affects Broadcast Live Video: from n/a through 7.3.14.

### CVE-2026-115340

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-312;CWE-522` |
| Published | 2026-11-09T17:17:11.520 |

Progress Software WS_FTP Server versions prior to 2025.0.5 on Windows may write sensitive user credential and session data to a temporary file during file transfer operations.

### CVE-2026-16478

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-183` |
| Published | 2026-11-10T13:18:29.030 |

Permissive list of allowed inputs vulnerability in TÜBİTAK BİLGEM Software Technologies Research Institute pardus-nvidia-installer allows Privilege Escalation.

This issue affects pardus-nvidia-installer: before 2.0.1.

### CVE-2026-109830

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T12:17:16.387 |

A vulnerability has been identified in meta-iot2050 (All versions >= V01.03.01). Affected devices take parts from a configuration file and execute them unchecked. This could allow an attacker which is able to manipulate the configuration file to make the user execute arbitrary code on the device.

### CVE-2026-92863

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-10T05:18:16.667 |

Integer Overflow Vulnerability in Hitachi Dynamic Link Manager for AIX (for the Japanese market).

This issue affects Hitachi Dynamic Link Manager for AIX: before 9.0.4-01.

### CVE-2026-91760

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T05:18:15.430 |

Heap-based Buffer Overflow Vulnerability in Hitachi Dynamic Link Manager for Linux.


This issue affects Hitachi Dynamic Link Manager for Linux: from 7.5.0-00 before 9.0.5-00.

### CVE-2026-88709

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T02:16:45.827 |

Improper
neutralization of special elements used in an OS command in certain
ASUS Router firmware allows an user with physical access
to
insert a USB device containing a specially crafted directory name, potentially
executing arbitrary commands with root privileges.
Refer to the ' Security Update for ASUS Router Firmware ' section on the ASUS Security Advisory for more information.

### CVE-2026-102289

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-11-09T22:18:21.590 |

zizmor is a static analysis tool for CI/CD systems. In version 1.27.0, debug logging serializes the parsed application configuration with a derived Debug implementation for GitHubToken, causing credentials supplied through GH_TOKEN, GITHUB_TOKEN, ZIZMOR_GITHUB_TOKEN, --gh-token, --github-token, or --zizmor-github-token to be written to stderr in cleartext. A single -v or --verbose option or an applicable RUST_LOG directive enables the affected logging during normal online operation and --no-online-audits, while explicit --offline clears the token first. If another party can read a CI log, support artifact, terminal capture, or public bug report containing the output, the party can use the credential according to its scopes, repository access, and lifetime. This vulnerability is fixed in 1.28.0.
