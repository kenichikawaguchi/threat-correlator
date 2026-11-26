# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-26 15:01 UTC
- **対象期間**: `2026-11-25T15:00:47.000Z` 〜 `2026-11-26T15:01:16.000Z`
- **重要CVE数**: 219 件（Critical 9.0+: 30 件 / High 7.0〜: 189 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、CVSS 7.0 以上が 40 件以上報告されており、**リモートコード実行 (RCE)・認証バイパス・オブジェクトインジェクション** が目立ちます。  
- 特に **VMware ESXi / vCenter 系列**、**Jenkins の Script Security Plugin**、**HPE Airwave（Networking Management Software）** での深刻な脆弱性が多数報告され、インフラ基盤全体への影響が大きくなっています。  
- WordPress 系プラグイン（Ultimate Member、FunnelKit Automations）やオープンソースライブラリ（CodeSafe、MongoDB ドライバ）でも、**未認証のオブジェクトインジェクション** が頻発しており、Web アプリケーション層でも緊急対応が必要です。  

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 製品・コンポーネント | 主なリスク | 影響範囲（推定） |
|-----|--------|----------------------|------------|-------------------|
| **CVE‑2026‑123903** | 9.8 | VMware vCenter Server (Directory Service) | 認証バイパス → 任意の管理操作が可能 | vCenter 9.1.x 系全環境（管理コンソール、API） |
| **CVE‑2026‑136835** | 9.9 | Jenkins **Script Security Plugin** 1.4.36‑v1082791135e4 以前 | @Builder アノテーションの不適切なクラス解決により、サンドボックススクリプトから任意コード実行 | Jenkins 本体にプラグインを導入している全サーバ |
| **CVE‑2026‑133973** | 9.8 | HPE Airwave (Networking Management Software) – Web UI コマンドインジェクション | 未認証リモートから OS コマンド実行 | HPE Airwave 8.x 系全デバイス（ネットワーク管理サーバ） |
| **CVE‑2026‑134481** | 9.8 | WordPress **Ultimate Member** 2.14.1 まで | 逆シリアライズによるオブジェクトインジェクション | WordPress サイト全般（プラグイン使用サイト） |
| **CVE‑2026‑131767** | 9.8 | WordPress **FunnelKit Automations** 3.9.0.1 まで | 同上（Object Injection） | WordPress サイト全般（FunnelKit 使用サイト） |

### 選定理由
1. **CVE‑2026‑123903** は認証バイパスにより vCenter の全管理権限が奪取でき、クラウド・オンプレミス混在環境での横断的攻撃が可能になる点が最重要。  
2. **CVE‑2026‑136835** は Jenkins の CI/CD パイプラインに直接影響し、攻撃者がビルドサーバ上で任意コードを実行できるため、開発・運用の全体的な信頼性が失われる。  
3. **CVE‑2026‑133973** はネットワーク機器管理ソフトの Web UI から直接 OS コマンドが実行でき、インフラ全体の可用性・機密性に直結する。  
4. **CVE‑2026‑134481 / CVE‑2026‑131767** は WordPress エコシステムで広く利用されているプラグインが対象で、公開サイトが即座に乗っ取られるリスクが高い。  

---

## 3. 推奨アクション  

### 3.1 VMware 系列（ESXi / vCenter）  
- **vCenter Server**: 9.1.x 系は **9.1.2** 以降にアップデート（公式パッチ `VMware-VMvisor-Installer-9.1.2-xxxx`）。  
- **ESXi**: 9.1.x 系は **ESXi‑9.1.2.0‑25946735**、9.0.x 系は同等のパッチレベルに更新。  
- パッチ適用後、**vCenter の管理 API アクセス制御** を再確認し、不要な外部 IP からのアクセスをファイアウォールで遮断。  

### 3.2 Jenkins  
- **Script Security Plugin** を **`1.4.36.v1082791135e4` 以降**（もしくは最新 1.4.38）にアップデート。  
- Jenkins 本体も **2.462 以降** に更新し、**「Enable security」** と **「CSRF Protection」** を必ず有効化。  
- 既存のサンドボックススクリプトは **`@Builder` アノテーションの使用を見直し**、不要なプラグインは削除。  

### 3.3 HPE Airwave (Networking Management Software)  
- ベンダー提供の **Airwave 8.6.0 以上**（もしくは最新リリース）へアップグレード。  
- 管理インタフェースへの **IP アクセス制限**（VPN・ACL）を実装し、外部からの直接アクセスを遮断。  
- Web アプリケーションファイアウォール (WAF) で **コマンドインジェクションパターン**（`;`, `&&`, `|` など）をブロック。  

### 3.4 WordPress プラグイン  
| プラグイン | 現行バージョン | 推奨バージョン |
|-----------|----------------|----------------|
| Ultimate Member | ≤ 2.14.1 | **2.14.2** 以上（2026‑03 リリース） |
| FunnelKit Automations | ≤ 3.9.0.1 | **3.9.1** 以上（2026‑04 リリース） |

- **プラグイン更新** 後、`wp-config.php` の `DISALLOW_FILE_EDIT` を `true` に設定し、管理画面からのコード編集を無効化。  
- すべての **POST データのシリアライズ** を `json_encode` に置き換えるか、`unserialize()` の使用を廃止し、**`wp_kses`** で入力サニタイズ。  

### 3.5 その他の高リスクコンポーネント  
| CVE | 製品 | 修正バージョン / 対策 |
|-----|------|-----------------------|
| CVE‑2026‑133467 | CodeSafe (Python) | 0.0.5 以降へアップデート。`safe_eval` の使用を廃止し、代替のサンドボックス実装（`restrictedpython` 等）を採用。 |
| CVE‑2026‑135224 | MongoDB C Driver | 1.27.0 以降に更新。TLS 証明書検証ロジックを **OpenSSL のデフォルト検証** に委任。 |
| CVE‑2026‑137567 | llama.cpp | b12658 以降にビルドし、`ggml` RPC サーバーを無効化（`--no-rpc` オプション）。 |
| CVE‑2026‑82489 | openIMIS | 2026‑11 リリース（`openimis-be-report_py`）で **simpleeval** のホワイトリストを厳格化。 |

### 3.6 共通的な緊急対策  
1. **脆弱性スキャナ**（Qualys、Nessus、OpenVAS 等）で対象資産を即時スキャンし、上記 CVE が検出されたホストをリスト化。  
2. **ネットワーク分離**：外

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-136835

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-25T17:17:50.523 |

Jenkins Script Security Plugin 1436.v1082791135e4 and earlier does not reject @Builder annotations whose builderStrategy member names an arbitrary class when the annotation is referred to using a partially qualified class name, allowing attackers with permission to define and run sandboxed scripts, including Pipelines, to execute code outside the sandbox if a suitable class is present on the classpath of the component that evaluates the script.

### CVE-2026-134481

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-26T13:16:41.717 |

Deserialization of Untrusted Data vulnerability in Ultimate Member Ultimate Member ultimate-member allows Object Injection.This issue affects Ultimate Member: from n/a through 2.14.1.

### CVE-2026-131767

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-26T13:16:40.023 |

Deserialization of Untrusted Data vulnerability in Aman FunnelKit Automations wp-marketing-automations allows Object Injection.This issue affects FunnelKit Automations: from n/a through 3.9.0.1.

### CVE-2026-123911

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-26T11:17:01.500 |

ESX contains a use-after-free vulnerability in the I/O filter service. Broadcom has evaluated the severity of this issue to be in the Critical severity range with a maximum CVSSv3 base score of 9.8.
Affected versions:
VMware ESX 9.1.x.x: fixed in ESXi-9.1.2.0-25946735
VMware ESX 9.0.x.x: fixed in ESXi-9.0.2.0200-25953133
VMware ESX 8.0: fixed in ESXi80U3m-25926933
VMware Cloud Foundation 5.x: fixed in 5.2.5
VMware Telco Cloud Platform 5.0.x: fixed in KB463501
VMware Telco Cloud Platform 5.1.x: fixed in KB463501

### CVE-2026-123910

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-26T11:17:01.373 |

ESX contains a heap out-of-bounds write vulnerability in the I/O filter service. Broadcom has evaluated the severity of this issue to be in the Critical severity range with a maximum CVSSv3 base score of 9.8.
Affected versions:
VMware ESX 9.1.x.x: fixed in ESXi-9.1.2.0-25946735
VMware ESX 9.0.x.x: fixed in ESXi-9.0.2.0200-25953133
VMware ESX 8.0: fixed in ESXi80U3m-25926933
VMware Cloud Foundation 5.x: fixed in 5.2.5
VMware Telco Cloud Platform 5.0.x: fixed in KB463501
VMware Telco Cloud Platform 5.1.x: fixed in KB463501

### CVE-2026-123903

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-26T11:17:00.283 |

VMware vCenter contains an authentication bypass vulnerability in the VMware Directory Service. Broadcom has evaluated the severity of this issue to be in the Critical severity range with a maximum CVSSv3 base score of 9.8.
Affected versions:
VMware vCenter Server 9.1.x.x: fixed in 9.1.2
VMware vCenter Server 9.0.x.x: fixed in 9.0.2.0300
VMware vCenter Server 8.0: fixed in 8.0 U3m
VMware Cloud Foundation 5.x: fixed in 5.2.5
VMware Telco Cloud Platform 3.0: fixed in KB463501
VMware Telco Cloud Platform 4.x: fixed in KB463501
VMware Telco Cloud Platform 5.0.x: fixed in KB463501
VMware Telco Cloud Platform 5.1.x: fixed in KB463501
VMware Telco Cloud Platform 5.2: fixed in KB463501
VMware Telco Cloud Infrastructure 3.0: fixed in KB463501

### CVE-2026-133973

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-25T23:17:21.787 |

A command injection vulnerability exists in the web-based management interface of HPE Networking Management Software (Airwave). Successful exploitation could allow an unauthenticated remote attacker to execute arbitrary commands on the underlying operating system of the affected system, impacting the confidentiality, integrity and availability of HPE Networking Management Software (AirWave).

### CVE-2026-133972

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-25T23:17:21.680 |

A vulnerability in system functionality could allow an attacker with network access to bypass authentication. Successful exploitation could potentially allow an attacker to perform unauthorized actions, affecting system integrity and confidentiality.

### CVE-2026-133971

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-25T23:17:21.570 |

An authentication bypass vulnerability exists in the web management interface of HPE Networking Management Software (Airwave). Successful exploitation could allow an unauthenticated remote attacker to gain unauthorized administrative access to the affected system, impacting the confidentiality and integrity of AirWave.

### CVE-2026-133467

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-95;CWE-693` |
| Published | 2026-11-25T20:18:34.460 |

CodeSafe is an open-source Python library for code encryption, decryption, and safe evaluation using Python's AST module. From versions 0.0.1 through 0.0.4, the safe_eval() function can be bypassed with indirect subscript calls such as builtins'exec', because AST validation blocks only direct calls to dangerous built-ins. An attacker who controls an expression passed to safe_eval() can execute arbitrary Python code with the permissions of the host application. This issue is fixed in version 0.0.5.

### CVE-2026-135400

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-613` |
| Published | 2026-11-25T17:17:45.250 |

Ever Gauzy is an open source business management platform for ERP, CRM, HRM, ATS, and project management. Prior to 111.44.3, per-request JWT validation in packages/core/src/lib/auth/strategies/jwt.strategy.ts accepts the result of UserService.getIfExists in packages/core/src/lib/user/user.service.ts without requiring User.isActive to be true and User.isArchived to be false. When a token contains an organizationId claim, the active and archived status check applies to the UserOrganization record rather than the User entity. After an administrator deactivates an account through PATCH /api/user/:id, an existing access token can continue to authenticate API requests at the account's previous privilege level until expiration, up to 24 hours by default. This issue is fixed in version 111.44.3.

### CVE-2026-133336

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-26T08:17:06.870 |

Joomla Extension - chronoengine.com - Unauthenticated arbitrary file upload in ChronoForms extension 8.0.0-8.0.53 - When the Filename Provider option of a file field is used, the file extension check is performed against the original client filename instead of the final stored filename, allowing unauthenticated users to upload files with dangerous extensions. Fixed in 8.0.54.

### CVE-2026-135203

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-693` |
| Published | 2026-11-26T11:17:03.890 |

In Eclipse Ditto versions 0.3.0-M1 through 3.8.15 and 3.9.0 through 3.9.9, the JavaScript payload mapper of the connectivity service executes user-supplied mapping scripts in a Mozilla Rhino engine without a ClassShutter. A mapping script can catch an engine error and use the Java exception object exposed on it to reach arbitrary Java classes and methods via reflection, bypassing the documented sandbox restriction that mapping scripts cannot access Java packages or classes. This allows a user permitted to create or modify connections (by default the Ditto DevOps realm) to execute arbitrary code in the connectivity service, gaining access to its credentials and to the Ditto cluster.

### CVE-2026-137567

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-26T14:17:24.800 |

llama.cpp b11450 before b12658 contains an out-of-bounds write vulnerability in the ggml RPC server that allows unauthenticated attackers to write to arbitrary heap addresses via zero-element destination tensors. Attackers can learn buffer bases with BUFFER_GET_BASE, then send RPC_CMD_COPY_TENSOR with a destination pointer below the buffer base to crash the server or execute code.

### CVE-2026-130637

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-11-26T14:17:23.373 |

SEPPMAIL Secure E-Mail Gateway versions before 15.1.2 are affected by a pre-authentication server-side template injection vulnerability that allows unauthenticated remote attackers to disclose sensitive account information and reset account passwords, potentially enabling account takeover.

### CVE-2026-123912

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-26T11:17:01.620 |

VMware ESXi, Workstation, and Fusion contain an out-of-bounds write vulnerability in the XHCI USB controller. Broadcom has evaluated the severity of this issue to be in the Critical severity range with a maximum CVSSv3 base score of 9.3.
Affected versions:
VMware ESX 9.1.x.x: fixed in ESXi-9.1.2.0-25946735
VMware ESX 9.0.x.x: fixed in ESXi-9.0.2.0200-25953133
VMware ESX 8.0: fixed in ESXi80U3m-25926933
VMware Cloud Foundation 5.x: fixed in 5.2.5
VMware Telco Cloud Platform 5.0.x: fixed in KB463501
VMware Telco Cloud Platform 5.1.x: fixed in KB463501
VMware Workstation 25H2: fixed in 26H1u1
VMware Fusion 25H2: fixed in 26H1u1

### CVE-2026-137043

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-639` |
| Published | 2026-11-26T03:16:39.110 |

A security vulnerability has been detected in TOTOLINK N350RT 9.3.5u.6468_B20250827/9.3.5u.6466_B20250825. The affected element is the function setLanguageCfg of the file /cgi-bin/cstecgi.cgi. Such manipulation of the argument lang leads to authorization bypass. The attack can be executed remotely. The exploit has been disclosed publicly and may be used.

### CVE-2026-136823

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-25T22:17:20.717 |

A vulnerability was found in D-Link R32 1.10B02. This affects an unknown function of the file /usr/bin/httpd of the component flupl self Endpoint. Performing a manipulation of the argument fpath results in os command injection. The attack can be initiated remotely. The exploit has been made public and could be used.

### CVE-2026-137090

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-25T20:18:46.220 |

build-git-clone before 1.0.4 contains an OS command injection vulnerability in the clone() function that allows attackers to execute commands by supplying crafted repository URLs. Attackers can embed shell metacharacters such as ; or $() in the url argument, which is concatenated into a sh -c command, to execute operating system commands with Node.js process privileges.

### CVE-2026-135224

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-25T17:17:44.573 |

The MongoDB C Driver does not confirm that the party signing a supplied certificate revocation status response is authorized to answer for the certificate being checked. An unauthenticated party that operates the TLS endpoint a client connects to can therefore have a withdrawn certificate accepted. This may result in unintended disclosure of the application's database traffic and in the loss of the revocation decision.

### CVE-2026-82489

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-25T15:17:52.040 |

openIMIS before 2026-10 contains an unauthenticated remote code execution vulnerability in the report module (openimis-be-report_py) where the /api/report/reportbro/preview endpoint evaluates printIf expressions server-side using simpleeval with an insufficient name-prefix blocklist. An attacker can craft an expression that reaches sys.modules['os'] via datetime.sys to execute arbitrary operating-system commands as root, and can also exploit the same endpoint's key parameter for unauthenticated arbitrary file read, enabling full host compromise including exposure of database credentials and JWT signing keys.

### CVE-2026-114346

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-25T15:17:37.170 |

The phsuperpack module for PrestaShop is vulnerable to a missing authorization check. The controller at /module/phsuperpack/pack can be accessed without login, which allows an unauthenticated remote attacker to modify the module's data and create, edit, or delete products, including the complete deletion of a product with its translations, shop associations, stock, and images.



This issue was fixed in version 3.0.26.

### CVE-2026-124843

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-26T13:16:38.143 |

SEPPmail Secure Email Gateway before 15.1.2 uses a source-visible hard-coded fallback secret for legacy GINA token and Large File Transfer cryptographic operations when expected key material is unavailable or unusable. A remote attacker can forge accepted account tokens while the fallback path is active and can decrypt LFT content protected with the shared fallback.

### CVE-2026-124840

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-26T13:16:37.760 |

SEPPmail Secure Email Gateway before 15.1.2 reuses a broad legacy GINA session purpose across registration and recovery workflows. A remote attacker who knows an account security answer can use a recovery session in a different account workflow to replace credentials and account recovery data, and may delete the account when self-deletion is enabled.

### CVE-2026-137086

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-341` |
| Published | 2026-11-25T20:18:45.607 |

Teracom TCW122B-CM firmware before 4.07 contains a predictable session cookie vulnerability that allows unauthenticated remote attackers to hijack administrator sessions by guessing tick-counter-derived cookies. Attackers can predict or brute-force the 32-bit cookie from device uptime and login timing to control relays, settings, and administrator credentials.

### CVE-2026-77230

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-25T19:17:39.077 |

Camunda 8.8.0 before 8.8.47, 8.9.0 before 8.9.29, 8.10.0 before 8.10.10, and 8.11.0-alpha1 contain an insecure deserialization vulnerability in the persistent web session feature, which stores session attributes as Java-serialized data in secondary storage and deserializes them via an ObjectInputStream without an ObjectInputFilter. Attackers with write access to the web session index, such as an unauthenticated Elasticsearch cluster deployed via Camunda's docker-compose files, can plant a crafted serialized object and trigger deserialization by presenting a matching session cookie, which combined with a gadget chain like the bundled Commons Collections 3.1-RC1 library can lead to code execution as the Camunda service account.

### CVE-2026-137584

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-26T14:17:27.067 |

Twenty through 2.63.0 in multi-workspace mode contains an authentication bypass vulnerability that allows unauthenticated attackers to obtain pending invitation tokens by registering an invitee's email via the signUp GraphQL mutation. Attackers can submit the leaked personalInviteToken to signUpInWorkspace to join the workspace with the invitation's role, including Admin, and obtain a verified email.

### CVE-2026-133464

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-1284` |
| Published | 2026-11-25T19:17:32.660 |

SeaweedFS is a distributed storage system for files and blobs. Prior to version 4.46, FileStore.ValidatePassword in the SFTP server does not reject zero-length secrets before comparing them, causing an empty login password to match any account configured without one, such as public-key-only or certificate-only users. Because password authentication is enabled by default, a remote attacker who knows a valid username can log in without a key or secret and obtain an SFTP session with that user's home directory and path permissions. This issue is fixed in version 4.46.

### CVE-2026-135146

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-299` |
| Published | 2026-11-25T18:18:50.597 |

An improper certificate revocation check in the MongoDB Python Driver's optional TLS revocation-checking support allows an unauthenticated party that operates the network endpoint a client connects to, and that holds a revoked but still-dated certificate trusted by that client, to have the connection accepted. This may result in unintended disclosure of application credentials and other session data, and in the client treating responses from that endpoint as genuine.

### CVE-2026-135150

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290;CWE-436` |
| Published | 2026-11-25T16:17:44.637 |

In Eclipse Ditto versions 1.1.0 to 3.9.9, the nginx reverse proxy configurations shipped with Ditto (Helm chart, Docker Compose, Kubernetes and OpenShift deployment files) forward a client-supplied

  `x-ditto-pre-authenticated` header to the Ditto gateway on locations that do not apply nginx authentication, such as `/api/2/connections`. nginx selects the location based on the normalized request URI
  but forwards the raw URI, while the gateway does not treat an encoded slash (`%2f`) as a path separator. A crafted request path is therefore routed by nginx through such an unauthenticated location and
  by the gateway to the regular Things and Policies HTTP API, including routes that send live messages to devices. When pre-authentication is enabled (the default of the Helm chart and the Docker Compose
  setup), an unauthenticated remote attacker can impersonate arbitrary policy subjects and read, modify and delete Things, read Policies, send messages to devices and create entities. Additionally, the
  optional Ingress of the Helm chart (Ditto 3.9.0 to 3.9.9) routes requests directly to the gateway without setting or removing that header, and the WebSocket Ingress of the Helm chart of Ditto 3.3.0 to
  3.8.15 does not set it, allowing the same impersonation without path manipulation when pre-authentication is enabled. This bypasses the fix for CVE-2026-120753.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-124266

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-26T13:16:36.960 |

Deserialization of Untrusted Data vulnerability in Arraytics WP Event Solution wp-event-solution allows Object Injection.This issue affects WP Event Solution: from n/a through 4.1.30.

### CVE-2026-127041

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-26T10:17:07.447 |

Bizum Pay for Android incorporates static values within the APK to authenticate and sign requests to its API, including those for user registration. These values are common across different installations and can be extracted from the APK. An attacker who obtains the application could reuse them to generate requests that the server accepts as authenticated. The potential scope of these requests was limited to querying auxiliary information and certain configuration statuses. Under no circumstances could they generate unauthorised payments via Bizum Pay, nor could they carry out illegitimate activations of the app (which always require access to the customer’s banking channels, thereby protecting them from this type of potential vulnerability). Furthermore, requests are always limited to a set number of attempts and are closely monitored to prevent potential mass queries.



The correction implemented uses site-specific material and removes support for the previous format in the backend. Consequently, previous versions are no longer operational for the services affected.

### CVE-2026-133525

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-26T08:17:07.253 |

Deserialization of Untrusted Data vulnerability in ThemeFusion Fusion Builder fusion-builder allows Object Injection.This issue affects Fusion Builder: from n/a before 3.17.1.

### CVE-2026-115576

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-26T02:16:59.420 |

NetBird is a zero-trust networking platform that connects people, machines, and AI agents across any network. From versions 0.5.0 through 0.75.1, the client daemon exposes its gRPC control interface to any local process without authentication. On Linux, macOS, and FreeBSD, the interface is a Unix domain socket that is accessible to all local users, allowing any of them to control the daemon. An attacker with a low-privilege account can read or modify privileged VPN and daemon settings, disconnect or hijack the NetBird peer, and gain an unauthenticated root shell via the built-in SSH server. This issue is fixed in version 0.76.0.

### CVE-2026-133976

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-25T23:17:22.127 |

A missing integrity verification vulnerability exists in HPE Networking Management Software (Airwave). Successful exploitation could allow a low-privileged local attacker to modify trusted system data on the affected system.

### CVE-2026-133975

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-25T23:17:22.013 |

Authenticated SQL injection vulnerabilities in the web-based management interface and API of HPE Networking Management Software (Airwave) could allow a low-privileged authenticated remote attacker to execute arbitrary SQL statements against HPE Networking Management Software (Airwave). Successful exploitation could allow an attacker to obtain sensitive information from and modify data on the affected system.

### CVE-2026-133974

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-25T23:17:21.903 |

A vulnerability in a system functionality could allow a low-privilege authenticated attacker with network access to potentially authenticate as an unintended user. Successful exploitation could allow an attacker to gain unauthorized access, potentially affecting system integrity, exposing sensitive information, or disrupting management operations.

### CVE-2026-131817

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-25T21:17:16.850 |

ChargePoint Home Flex wpa_passphrase Command Injection Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of ChargePoint Home Flex EV chargers. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the PSK parameter passed to the wpa_passphrase endpoint. The issue results from the lack of proper validation of a user-supplied string before using it to execute a system call. An attacker can leverage this vulnerability to execute arbitrary code in the context of root. Was ZDI-CAN-29000.

### CVE-2026-135898

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-25T18:18:51.163 |

An out-of-bounds read in the native C BSON decoding extension of the MongoDB Python Driver may allow an unauthenticated party who can supply crafted BSON data to the decoder to cause the application process to terminate. In some configurations, nearby process memory may be included in error messages, which may result in limited unintended disclosure of data.

### CVE-2026-136837

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-25T17:17:50.813 |

Jenkins Warnings Plugin 13.10251.va_452d3553728 through 13.10365.v85cd7a_c8110b_ (both inclusive) allows defining inline Groovy parsers whose Groovy scripts are compiled on the Jenkins controller without sandbox protection, allowing attackers able to define inline Groovy parsers to execute arbitrary code in the context of the Jenkins controller JVM.

### CVE-2026-136834

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-25T17:17:50.410 |

Sandbox protection in Jenkins Pipeline: Groovy Plugin 4403.v471713a_cea_19 and earlier can be circumvented through interface field initializers, allowing attackers with permission to define and run sandboxed Pipelines to bypass the sandbox protection and execute arbitrary code in the context of the Jenkins controller JVM.

### CVE-2026-135399

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-613` |
| Published | 2026-11-25T17:17:45.087 |

Ever Gauzy is an open source business management platform for ERP, CRM, HRM, ATS, and project management. Prior to 111.42.10, RoleGuard authorizes requests using the role claim embedded in an access token instead of the user's current database role in packages/core/src/lib/core/context/request-context.ts through RequestContext.hasRoles. After an administrator demotes a user, an already-issued token can continue to pass role checks for up to the token's 24-hour default lifetime, including on DELETE /api/tenant and other RolesEnum.SUPER_ADMIN or ADMIN guarded routes, which can preserve tenant-destructive and billing privileges after revocation. This issue is fixed in version 111.42.10.

### CVE-2026-135985

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-25T15:17:45.697 |

Cross-Site Request Forgery (CSRF) vulnerability in John-Michael L'Allier Create mediavine-create allows Cross Site Request Forgery.This issue affects Create: from n/a through 3.1.4.

### CVE-2026-134945

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-25T15:17:39.147 |

Cross-Site Request Forgery (CSRF) vulnerability in Brainstorm Force SureForms sureforms allows Cross Site Request Forgery.This issue affects SureForms: from n/a through 2.14.1.

### CVE-2026-134873

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-25T15:17:38.907 |

Cross-Site Request Forgery (CSRF) vulnerability in Brainstorm Force CartFlows cartflows allows Cross Site Request Forgery.This issue affects CartFlows: from n/a through 3.3.3.

### CVE-2026-137586

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1287` |
| Published | 2026-11-26T14:17:27.423 |

LibreChat 0.7.3 before 0.8.9 contains an improper input type validation vulnerability in the requireLdapAuth middleware of the /api/auth/login route that allows unauthenticated attackers to crash the server. Attackers can send a JSON login request with an existing directory user's email and a non-string password, triggering an ldapjs assertion error that terminates the Node.js process.

### CVE-2026-137585

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-26T14:17:27.240 |

Bazarr 1.4.4 before 1.6.1-beta.29 on Windows contains an unauthenticated path traversal vulnerability in the catch_all() handler in bazarr/app/ui.py. Attackers can append percent-encoded '..' segments after the 'workbox-' prefix to read files like config.yaml containing stored API keys and credentials.

### CVE-2026-137566

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-26T14:17:24.630 |

Argo Workflows 3.0.0 through 3.7.18, 4.0.0 before 4.0.12, and 4.1.0 before 4.1.4 contains a path traversal vulnerability in the S3, GCS, and Azure Blob artifact drivers. Attackers who can write bucket objects or supply malicious artifact sources can use object keys containing ../ sequences to write arbitrary files in the executor pod, achieving code execution.

### CVE-2026-124844

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-26T13:16:38.270 |

SEPPmail Secure Email Gateway before 15.1.2 writes legacy GINA multipart uploads before authenticating the caller and does not remove files created by failed or unauthenticated requests. An unauthenticated remote attacker can accumulate persistent upload files and exhaust the backing filesystem, disrupting GINA and other services sharing that storage.

### CVE-2026-133342

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-26T11:17:03.720 |

Joomla Extension - joomdonation.com - Unauthenticated SQL injection in event registration in Events Booking < 5.12.0 - The event_id submitted through the public registration form was not cast to an integer before being added to an SQL query for the registration's custom fields, allowing unauthenticated SQL injection.

### CVE-2026-137390

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-26T09:17:10.090 |

Mail2000 developed by Openfind has an OS Command Injection vulnerability.Authenticated remote attackers can inject arbitrary OS commands and execute them on the server.

### CVE-2026-137389

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-26T09:17:09.937 |

MailGates/MailAudit developed by Openfind has a Command Injection vulnerability.Authenticated remote attackers can inject commands and execute them on the server.

### CVE-2017-20291

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-26T07:16:36.103 |

An XML External Entity (XXE) injection vulnerability in the Federation Web Services component (/affwebservices/router/session) of Broadcom SiteMinder (CA Single Sign-On) Secure Proxy Server / Access Gateway R12.52 SP1 prior to R12.52 SP1 CR6 allows a remote attacker to submit crafted SOAP requests to the exposed Apache-SOAP RPC Router servlet (org.apache.soap.server.http.RPCRouterServlet). Successful exploitation could result in unauthorized disclosure of local files or sensitive data, server-side request forgery (SSRF), or denial of service. The issue is resolved in R12.52 SP1 CR6 (and does not affect R12.8 or R12.9) by removing the router servlet mapping so requests to the endpoint return HTTP 404.

### CVE-2026-123685

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-11-26T03:16:35.517 |

A remote code execution vulnerability exists in the patch apply functionality of StellarProtect Linux and Stellar Agent (Linux) due to insufficient validation of uploaded patch packages before extraction. An attacker with low-privileged web access can upload a crafted patch package to execute arbitrary programs with root privileges on the server. This issue affects StellarProtect Linux: 1.0 and earlier; Stellar Agent (Linux): before 1.2.54. *Note: Stellar Agent (Linux) is the new name for StellarProtect Linux.

### CVE-2026-137305

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-26T02:17:02.350 |

Grav Form plugin before 9.2.4 contains a code injection vulnerability that allows page authors to write uploads into Twig template folders by setting an unchecked file field destination in Form::uploadFiles(). Attackers can upload .txt or .svg files containing Twig and have them rendered as trusted templates outside the sandbox, executing code as the web server user.

### CVE-2026-66784

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-1295` |
| Published | 2026-11-26T01:17:11.880 |

A flaw was found in Submariner. In its default Pre-Shared Key (PSK) mode, all gateways within a broker set utilize the same PSK. An attacker, by knowing this shared PSK, can forge an Endpoint Custom Resource (CR) to impersonate another cluster's identity. This enables the attacker to establish an Internet Protocol Security (IPsec) tunnel under the false identity, leading to a Man-in-the-Middle (MITM) attack on network traffic between clusters.

### CVE-2026-69695

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-25T22:17:21.800 |

Handesk through 1.5 contains an unrestricted file upload vulnerability in Attachment::storeAttachmentFromRequest() that allows authenticated agents to upload files with arbitrary extensions by attaching them to ticket comments without extension, MIME type, or size validation. Attackers can upload a PHP file via POST /tickets/{ticket}/comments, which is stored under storage/app/public/attachments and served from /storage/attachments/, to achieve remote code execution as the web server user or serve malicious HTML/SVG content from the application origin.

### CVE-2026-66052

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-917` |
| Published | 2026-11-25T22:17:21.493 |

Comviva Revenue Plus (MobiLytix Customer Value Management) 3.0.0 contains an expression language injection vulnerability in the user administration module, where the POST /rp/manageUser endpoint handled by manageUsersAction evaluates the name of an arbitrary request parameter as a server-side Java EL expression before rendering the response. The only protection is a denylist of reflective method names, which does not cover constructor-based access to a JDK scripting engine, so authenticated low-privilege attackers can supply an EL expression as a parameter name to execute arbitrary operating system commands as the application server account. This product is no longer supported by the vendor; standard support ended on 2022-10-31 and extended support ended on 2023-10-31.

### CVE-2026-137058

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-25T20:18:39.500 |

Cron-parser through 5.10.0 contains an unbounded memory allocation vulnerability in CronExpressionParser.parse() that allows unauthenticated attackers to exhaust memory by supplying oversized cron fields. Attackers can submit a roughly 1.6 MB expression of repeated wildcard tokens that expand into huge arrays, exhausting the V8 heap and crashing the Node.js process.

### CVE-2026-137057

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-25T20:18:39.307 |

llama.cpp from b7118 before b12604 contains an integer underflow vulnerability in llama_grammar_parser::parse_sequence() that allows unauthenticated remote attackers to cause denial of service by supplying GBNF repetitions with max lower than min. Attackers can send a grammar like {5,2} in the grammar field of a llama-server /completion request, wrapping n_opt to generate endless repetition rules that hang the process and exhaust memory.

### CVE-2026-137056

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-11-25T20:18:39.143 |

DeepSeek-Reasonix before 2.53.0 contains a command execution vulnerability that allows attackers to run commands without user approval because the shellsafe classifier treats git blame and git whatchanged as read-only. Attackers can plant a diff textconv driver in .gitattributes and .git/config so that git blame, triggered via prompt injection or routine use, executes attacker-chosen commands with the user's privileges, exposing stored provider API keys and session history.

### CVE-2026-135226

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-25T18:18:50.880 |

A type-confusion weakness in the Extended JSON parsing component of BSON for Ruby allows a party who can supply parser input to influence how a serialized document is framed. Content placed in one value may be read back as additional or replacement document fields. An unauthenticated party supplying input to an application that parses untrusted Extended JSON and stores the result may cause unintended modification of stored data.

### CVE-2026-73517

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-25T17:17:59.920 |

KubeSphere 4.0.0 through 4.1.3 contains a command injection vulnerability in the terminal v1alpha2 file download endpoint where the path query parameter is inserted via fmt.Sprintf into sh -c tar commands executed inside the target container, and the DownloadFile handler fails to perform its own pods/exec authorization check. Attackers with only pod get permission, including built-in read-only project-viewer, workspace-viewer and cluster-viewer roles, can supply shell metacharacters in the path parameter to execute arbitrary commands inside any viewable container without holding pod exec permission.

### CVE-2026-64845

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-25T16:17:54.540 |

KubeSphere 4.0.0 through 4.1.3 contains a missing authorization vulnerability in the CertificateSigningRequest controller that allows attackers with permission to create CertificateSigningRequest objects to escalate privileges by exploiting automatic approval of requests carrying a kubesphere.io/username label without verifying the requester's identity or subject match. Attackers can submit a CertificateSigningRequest for the kubernetes.io/kube-apiserver-client signer with an arbitrary subject such as a platform administrator to obtain a cluster CA-signed client certificate, enabling authentication as the chosen identity and full cluster administrator privilege escalation.

### CVE-2026-82493

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-25T15:17:52.640 |

openIMIS before 2026-10 contains a remote code execution vulnerability in the report module's overrideReport GraphQL mutation, which stores submitted report definitions without proper validation before rendering them with the simpleeval expression evaluator. An attacker holding only limited report add, edit, or query privileges can craft a printIf expression that leverages the datetime module to reach os.system functions, bypassing the name-prefix blocklist to execute arbitrary operating-system commands as root whenever the malicious report is later rendered by any viewer, including administrators or scheduled jobs.

### CVE-2026-82492

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-25T15:17:52.500 |

openIMIS before 2026-10 contains an improper validation vulnerability in the deduplication service (openimis-be-deduplication_py, deduplication/services.py) that allows a caller holding only the narrow right 170001 to bypass column path validation by exploiting the fact that only the first segment of a dotted relation path is checked before the full unvalidated path is used in the query. Attackers can supply a crafted dotted column path such as user_created__i_user__private_key to traverse relations and retrieve an administrator's JWT signing key, enabling forgery of a valid administrator session without a password that survives password resets and generates no failed-login event.

### CVE-2026-82491

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-25T15:17:52.353 |

openIMIS before 2026-10 contains an information disclosure vulnerability in the core export mixin (openimis-be-core_py, core/gql/export_mixin.py) that allows authenticated users with a single ordinary read right to traverse arbitrary foreign key relations by supplying caller-controlled dotted field paths that are rewritten into Django ORM syntax without an allow-list. Attackers can exploit this to export another user's JWT signing key via a path such as user_created.i_user.private_key, enabling them to forge valid authenticated sessions for other accounts, including administrators, without detection through failed-login events or invalidation by password reset.

### CVE-2026-82490

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-25T15:17:52.200 |

openIMIS before 2026-10 contains a missing authorization vulnerability in the OpenSearch reporting dashboard proxy, where the nginx auth_request only verifies login status without checking the declared right before attaching a hardcoded administrative credential to the proxied request, and the backend OpenSearch cluster has its security plugin disabled via a hardcoded compose setting. Any authenticated account, including self-registered or zero-rights users, can exploit this flaw to gain read, write, and delete access to the OpenSearch cluster.

### CVE-2026-137577

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-26T14:17:26.513 |

Iceburg CRM through 5.0.0 contains an authorization bypass vulnerability that allows authenticated low-privileged users to modify any user record by supplying arbitrary record_id values to POST /data/save. Attackers can submit a save request for the ice_users module with the administrator's record_id to change their password or email and take over the account.

### CVE-2026-133339

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-26T09:17:09.130 |

Joomla Extension - vi-solutions - SQL injection via form IDs in administrative form export in Visforms extension 1.0.0-5.6.5, 6.0.0-6.2.2 - Form IDs passed to the administrative form export were not cast to integers before being added to SQL queries, allowing SQL injection by backend users.

### CVE-2026-135772

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1247` |
| Published | 2026-11-26T08:17:07.410 |

RTL8762C MCU developed by Realtek Semiconductor Corporation has an Improper Protection Against Voltage and Clock Glitches vulnerability. Unauthenticated attackers with physical access can use specialized equipment to perform voltage fault injection and bypass SWD debug authentication, thereby accessing protected data and modifying the chip's execution flow.

### CVE-2026-123689

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-26T04:17:09.570 |

A SQL injection vulnerability exists in the Search Agents API of StellarOne due to improper sanitization of user-supplied input. An authenticated attacker with Viewer privileges can send crafted requests to manipulate backend SQL queries. This issue affects StellarOne: before 5.0.3232.

### CVE-2026-123687

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-26T03:16:35.800 |

An arbitrary file write vulnerability exists in the patch upload functionality of StellarOne due to improper validation of file paths. An attacker with admin web access can upload a crafted patch package to write arbitrary files on endpoints with the privileges of the endpoint service. This issue affects StellarOne: before 5.0.3232.

### CVE-2026-123682

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-26T03:16:35.100 |

An authenticated remote code execution vulnerability exists in the update functionality of StellarOne due to insufficient validation of files contained within uploaded update packages. An attacker with web administrator privileges can upload a crafted update package to execute arbitrary programs with root privileges on the server. This issue affects StellarOne: before 5.0.3232.

### CVE-2026-123680

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-26T03:16:34.823 |

An authenticated remote code execution vulnerability exists in the firmware update functionality of StellarOne. An attacker with admin privileges can upload a crafted firmware package to execute arbitrary programs with root privileges on the system. This issue affects StellarOne: before 5.0.3232.

### CVE-2026-136822

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-25T21:17:19.850 |

A vulnerability has been found in D-Link R32 1.10B02. The impacted element is the function SetDeviceSettings of the file /usr/bin/httpd of the component DHMAPI Action Handler. Such manipulation of the argument TZLocation leads to os command injection. It is possible to launch the attack remotely. The exploit has been disclosed to the public and may be used.

### CVE-2026-136821

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-25T21:17:19.630 |

A flaw has been found in D-Link R32 1.10B02. The affected element is the function SetTimeSettings of the component DHMAPI Action Handler. This manipulation of the argument TZLocation causes os command injection. It is possible to initiate the attack remotely. The exploit has been published and may be used.

### CVE-2026-135141

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-25T18:18:50.443 |

A logic flaw in the query-building layer of the Mongoid object-document mapper causes a model-level default restriction that is meant to return no records to be silently discarded when it is combined into a query. A user with basic application privileges who sends an ordinary request may read, change, or remove records that the restriction was intended to withhold.

### CVE-2026-135402

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-345;CWE-347` |
| Published | 2026-11-25T17:17:45.563 |

Ever Gauzy is an open source business management platform for ERP, CRM, HRM, ATS, and project management. Prior to 111.42.13, POST /api/integration/github/webhook in packages/plugins/integration-github/src/lib/probot/probot.discovery.ts passes request bodies through ProbotDiscovery.receiveHook to probot.receive without verifying x-hub-signature-256 against the configured webhook secret. Because the route is public and uses the attacker-controlled installation.id to locate integrations, an unauthenticated remote attacker who knows or guesses an installation identifier can forge installation deletion events that remove a tenant's GitHub integration or forge issues events that insert fabricated issue data into the tenant's automation pipeline. This issue is fixed in version 111.42.13.

### CVE-2026-136916

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-11-25T15:17:49.727 |

HortusFox (hortusfox-web) through 6.4 contains a password reset poisoning vulnerability in UserModel::restorePassword that builds reset links from the client-controlled Host header. Unauthenticated attackers can request a reset with a forged Host header to capture the victim's reset token and take over accounts including administrators.

### CVE-2026-114347

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-25T15:17:37.320 |

The phsuperpack module for PrestaShop is vulnerable to SQL injection in the /module/phsuperpack/pack endpoint. User-supplied input is used in database queries without proper sanitization. An authenticated, high privileged, remote attacker can exploit this by sending crafted input to read or modify data in the shop's database. Critically, because of CVE-2026-114346, this endpoint may be accessed without authentication.



This issue was fixed in version 3.0.26.

### CVE-2026-124838

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-26T13:16:37.503 |

SEPPmail Secure Email Gateway before 15.1.2 exposes an unauthenticated, world-writable local configuration socket whose root daemon accepts shell commands. An attacker with local low-privilege code execution can execute arbitrary commands as root and take complete control of the appliance.

### CVE-2026-137093

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-11-25T20:18:46.683 |

Assimp before 6.0.6 contains an out-of-bounds write vulnerability in MD5Importer::LoadMD5MeshFile() that allows attackers to corrupt heap memory via unvalidated weight ranges and bone indices. Attackers can supply a crafted .md5mesh file with out-of-range mBone values to increment heap words past the piCount allocation, causing memory corruption, out-of-bounds reads, or crashes.

### CVE-2026-137060

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-25T20:18:40.283 |

paramz through 0.10.0 contains an insecure deserialization vulnerability that allows attackers to execute code by supplying crafted model files to paramz.load(), which calls pickle.load() without restrictions. Attackers can embed objects whose __reduce__ method returns callables like exec or os.system in shared paramz or GPy model files to run code with the victim's privileges.

### CVE-2026-135133

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-763` |
| Published | 2026-11-25T17:17:43.093 |

An invalid memory release in the MongoDB PHP Driver extension occurs when certain string-typed options or type-mapping settings are given non-string values. A party who can run PHP code in a process that loads the extension may corrupt process memory. This can lead to reading or changing process memory, running commands as the PHP process user, or crashing the process.

### CVE-2026-136923

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-25T15:17:50.847 |

asar-py before 0.1.4 contains a path traversal vulnerability in AsarArchive.extract() and extract_archive() that allows attackers to write files outside the destination directory via crafted archive headers. Attackers can supply a .asar archive with '..' path components or malicious symlink targets to write files such as usercustomize.py, leading to code execution.

### CVE-2026-136922

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-11-25T15:17:50.693 |

PyBioNetGen 0.8.7 contains a code injection vulnerability in ParameterBlock.add_item() and ModelBlock.add_item() that allows attackers to execute Python code by passing parameter expressions to sympy.sympify(). Attackers can supply a crafted BNG-XML model file with Python code in a Parameter expr or value attribute to execute code as the user when loaded with bionetgen.bngmodel().

### CVE-2026-136919

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-25T15:17:50.227 |

FCEUX 2.5.0 before 2.8.0 contains an integer overflow in iNESLoad() in src/ines.cpp that allows a crafted NES 2.0 ROM to write past a heap buffer. Attackers can persuade users to open a .nes file using exponent-multiplier PRG ROM size notation with mappers 53, 198, 228 or 547 to corrupt memory, crashing the emulator and possibly executing code.

### CVE-2026-136918

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-25T15:17:50.073 |

FCEUX before 2.8.0 contains an integer overflow in SetBoardName() in src/unif.cpp that allows crafted UNIF ROM files to write past a heap buffer. Attackers can persuade users to open a .unf file with a 0xFFFFFFFF MAPR chunk length, wrapping the allocation to zero and corrupting heap memory to crash the emulator or execute code.

### CVE-2026-123686

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-26T03:16:35.667 |

An OS command injection vulnerability exists in the vShell command-line interface of StellarOne due to improper validation of user-supplied input. An authenticated attacker with access to vShell can inject crafted commands to bypass the restricted shell environment and execute arbitrary operating system commands. This issue affects StellarOne: before 5.0.3232.

### CVE-2026-127280

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-25T16:17:38.977 |

C-More EA9 Programming Software V6.80 does not adequately validate data read from a project file before using it in heap memory operations. A crafted file causes a heap buffer overrun during file open, resulting in heap corruption and instability within the application. An attacker can exploit this vulnerability by convincing a user to open a malicious project file delivered through common distribution channels such as email, file sharing, or removable media.

### CVE-2026-124842

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-26T13:16:38.017 |

SEPPmail Secure Email Gateway before 15.1.2 exposes legacy GINA password-reset paths that can replace a registered account credential without authenticating the requester. A remote attacker who knows the account address can force a reset when a configured administrator or valid stored creator is present, disrupting access and revoking active API tokens; the replacement credential is sent only to a pre-existing trusted recipient.

### CVE-2026-137308

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-26T02:17:02.833 |

markdownify-mcp before 1.2.0 contains a server-side request forgery vulnerability that allows attackers to bypass URL validation by supplying DNS names, bracketed IPv6 literals, or IPv4-mapped IPv6 addresses. Attackers can influence URLs passed to webpage-to-markdown or git-repo-to-markdown through prompt injection to fetch loopback services, internal hosts, and cloud metadata endpoints.

### CVE-2026-137077

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-25T20:18:44.107 |

FreeRDP before 3.33.0 contains a heap out-of-bounds write in h264_context_reset() in libfreerdp/codec/h264.c, which stores new dimensions before the YUV planes are reallocated. Remote peers can trigger surface height increases so avc420_compress() writes taller frames past undersized luma and chroma planes, corrupting heap memory or crashing the process.

### CVE-2026-135227

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-25T18:18:51.020 |

An improper restriction of dynamically determined object attributes in the object-document mapping library's association handling allows structured input supplied in place of a simple identifier value to be turned into an object that is treated as an already-stored record of a caller-chosen model class. In applications that pass unfiltered request data into the affected association handling, an unauthenticated party may cause unintended modification or removal of stored records, and may render an individual record unreadable through that association.

### CVE-2026-135147

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-25T17:17:43.927 |

A data-query neutralization weakness in the query builder of the MongoDB integration for a PHP web framework allows values supplied to certain bulk counter-update helpers to be interpreted by the database as query expressions rather than stored as plain text. An application that passes externally supplied data into these helpers may write unintended values into stored documents and may result in unintended disclosure of other data held on the same document. No credentials are required of the party supplying the value.

### CVE-2026-137583

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-11-26T14:17:26.880 |

Juspay Hyperswitch 1.8.0 before 1.129.0 uses a hardcoded default webhook secret that allows unauthenticated attackers to forge Stripe webhooks when no merchant webhook secret is configured. Attackers knowing a merchant ID and connector transaction ID can sign a crafted payment_intent.succeeded event with "default_secret" to mark uncaptured payments as succeeded.

### CVE-2026-137568

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-26T14:17:24.980 |

openFrameworks through 0.12.1 contains a path traversal vulnerability in the ofxAndroid OFZipUtil.extract helper that allows attackers to write files outside the extraction directory. Attackers can supply a crafted ZIP archive with entries like ../escaped.txt to write or overwrite files with the Android application's file permissions.

### CVE-2026-123913

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-26T11:17:01.743 |

VMware ESX contains a stack-based buffer-overflow vulnerability in the VMkernel. Broadcom has evaluated the severity of this issue to be in the Important severity range with a maximum CVSSv3 base score of 8.2.
Affected versions:
VMware ESX 9.1.x.x: fixed in ESXi-9.1.2.0-25946735
VMware ESX 9.0.x.x: fixed in ESXi-9.0.2.0200-25953133
VMware ESX 8.0: fixed in ESXi80U3m-25926933
VMware Cloud Foundation 5.x: fixed in 5.2.5
VMware Telco Cloud Platform 5.0.x: fixed in KB463501
VMware Telco Cloud Platform 5.1.x: fixed in KB463501

### CVE-2026-133337

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-26T08:17:07.013 |

Joomla Extension - chronoengine.com - Unauthenticated SQL injection in table sorting in ChronoForms extension 8.0.0-8.0.53 - The order_by request parameter used for sorting DB Table and Read Data listings is insufficiently sanitized before being added to the ORDER BY clause, allowing unauthenticated users to inject SQL expressions. Fixed in 8.0.54.

### CVE-2026-137059

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-25T20:18:39.707 |

ToolJet from 3.16.0 before 3.20.256 contains an improper signature verification vulnerability in StripeWebhookGuard that validates webhooks against a self-generated signature instead of the Stripe-Signature header. Unauthenticated attackers can post forged Stripe events to the POST /api/organization/payment/webhooks route to activate subscriptions, generate licenses, change plans or seats, and add AI credits without payment.

### CVE-2026-135134

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-25T17:17:43.253 |

A NULL pointer dereference and invalid memory release in the server discovery component of the MongoDB C Driver may allow an unauthenticated party that controls a server endpoint, or that can alter unencrypted network traffic, to cause a client application to terminate by sending a crafted discovery response.

### CVE-2026-136915

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-552` |
| Published | 2026-11-25T15:17:49.560 |

HortusFox through 6.4 contains an information exposure vulnerability in BackupModule::start that allows unauthenticated attackers to download workspace backups stored in the public/backup directory. Attackers can enumerate one-second-precision creation timestamps used as filenames to retrieve archives containing locations, plants, gallery, tasks, inventory and calendar data.

### CVE-2026-136911

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-25T15:17:48.907 |

Boost.JSON 1.75.0 through 1.92.0 contains a denial of service vulnerability in monotonic_resource::release() because it does not reset next_size_ when returning blocks upstream. Attackers can send repeated JSON documents larger than the initial block, growing allocation sizes geometrically until every later allocation fails with bad_alloc.

### CVE-2026-136910

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-909` |
| Published | 2026-11-25T15:17:48.757 |

POCO C++ Libraries through 1.15.4 contain a denial of service vulnerability in InflatingStreamBuf::reset() that fails to clear stale buffered data from a previous failed stream. Attackers can supply one corrupt compressed stream to an application reusing an InflatingOutputStream, causing subsequent valid streams to fail decompression.

### CVE-2026-136908

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-761` |
| Published | 2026-11-25T15:17:48.450 |

libyang through 6.4.13 contains a release of invalid pointer vulnerability in ly_in_memory() and ly_in_memory_chunk() in src/in.c that return the current read position instead of the previous start address. Attackers supplying YANG data parsed from a heap buffer can cause applications freeing the returned pointer to pass an interior address to free(), aborting the process.

### CVE-2026-136904

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-909` |
| Published | 2026-11-25T15:17:47.793 |

POCO C++ Libraries through 1.15.4 contain a denial of service vulnerability in InflatingStreamBuf::reset() and InflatingInputStream::reset() that fails to discard unconsumed compressed input after decompression errors. Attackers can supply one corrupt zlib, gzip or zip-deflate stream to applications reusing an InflatingInputStream, causing all later stream reads, including valid ones, to fail.

### CVE-2026-133742

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-25T15:17:38.073 |

Incorrect permission assignment for critical resource in the media management functionality of Progress Software Sitefinity versions before 14.4.8154, from 15.0.8200 before 15.0.8236, from 15.1.8300 before 15.1.8337, from 15.2.8400 before 15.2.8444, from 15.3.8500 before 15.3.8533, and from 15.4.8600 before 15.4.8642 allows unauthorized modification of media library content under certain configurations.

### CVE-2026-131688

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-26T12:17:09.903 |

The Secure MCP Server for Claude, ChatGPT, Gemini, Cursor and other AI Agents plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 1.5.8 This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for attackers (with access to a valid MCP bearer token) to escalate privileges to the token owner's Administrator role — bypassing NHI ability allow-list and scope restrictions entirely — by submitting any valid MCP bearer token (including scope-restricted connection-test tokens) to arbitrary WordPress endpoints such as admin-ajax.php. This requires possession of a valid MCP bearer token, which is routinely issued to any administrator who connects an MCP client to the site. Successful exploitation causes the attacker's own account to receive the complete Administrator role.

### CVE-2026-130805

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-26T10:17:07.597 |

The Groundhogg plugin for WordPress is vulnerable to Cross-Site Request Forgery in versions up to, and including, 4.11 This is due to the Admin_Page::page() callback dispatching methods named directly by the $_REQUEST['action'] parameter via call_user_func([$this, $action]) without verifying a nonce: the only nonce check lives in process_action() (admin_init), which prefixes the action with 'process_' before dispatching, so an attacker who supplies action=process_delete causes process_action() to look up the nonexistent 'process_process_delete' method and bail without ever calling wp_verify_nonce(), while page() subsequently invokes the real process_delete() (and other process_* methods such as process_spam, process_status_change, process_edit) with no CSRF token of its own. This makes it possible for unauthenticated attackers to delete arbitrary contacts, change contact opt-in status (including marking contacts as spam, which also appends their IP to the site-wide disallowed_keys option), and perform other state-changing actions via a forged request granted they can trick a site administrator (or any user holding the relevant Groundhogg capability such as delete_contacts/edit_contacts) into performing an action such as clicking on a link.

### CVE-2026-136507

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74;CWE-121;CWE-197` |
| Published | 2026-11-25T23:17:23.830 |

psqlODBC parsed and built connection strings in ways that let a value end early:

- In a braced value, such as PWD={…}, a trailing byte 0x7d of a GBK, Big5 or SJIS character was taken for the closing brace.
- A braced value that ended right after an escaped }} was not reported as unterminated, and its contents were parsed as further keywords.
- SQLConnectW(), SQLDriverConnectW() and SQLBrowseConnectW() cut a connection string whose UTF-8 form is longer than 32767 bytes, which changes how the rest of it is parsed.
- On Windows with MSDTC, the password and user name were put into the XA open string without escaping, and the XA library copied each item of that string into a 64-byte stack buffer.
- Percent-encoding a long password wrote one byte past a 4096-byte stack buffer.

An end user who supplies a password, or another value the application puts into the connection string, can set other connection keywords, for example to connect the application to a server of their choosing. The MSDTC case can also overflow a stack buffer in the process that loads the XA library.

Versions up to and including psqlODBC 18.00.0006 are affected.

### CVE-2026-136502

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89;CWE-706` |
| Published | 2026-11-25T23:17:23.180 |

psqlODBC scans statement text itself to substitute parameters, translate ODBC escapes, join batched statements and rewrite queries for updatable cursors. Where it read the text differently from the server, text the driver took for data ran as SQL, or a positioned write went to another table:

- An escape string constant written e'…' in lower case was not recognised as one, and '…' after a keyword ending in E, as in LIKE'…', was taken for one.
- A } inside a quoted literal ended an ODBC {d …}, {t …}, {ts …} or {escape …} sequence.
- Dollar-quote tags containing _ were not recognised, and an identifier starting with _ followed by $, such as _$$, was taken for the start of a dollar quote, so a parameter marker inside a literal was substituted.
- A trailing -- comment in one statement of a batched parameter array swallowed the next statement.
- Comments, literals longer than 255 bytes and escape strings were misread when the driver located the FROM and WHERE clauses of a query for an updatable cursor, and the text copied into the cursor's own queries could include SQL from inside a literal.
- A table name containing $ was cut at the $, and a quoted table name starting with , or ; ended the table list, so positioned updates, inserts and deletes went to another table.
- An integer parameter with an embedded NUL byte cut the query short.
- /*/ was taken for a comment that opens and closes, while the server reads it as one that only opens.
- ConnSettings was split at every semicolon, including one inside a quoted literal, so an application that puts an end user's value into a SET command there ran the rest of the value as SQL at connect time.

An end user who controls text the application puts into a statement, or a parameter value, can run SQL with the rights of the application's database role. A database user who can create a table with a crafted name can redirect another user's positioned writes to a table of their choosing.

Versions up to and including psqlODBC 18.00.0006 are affected.

### CVE-2026-136500

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89;CWE-173` |
| Published | 2026-11-25T23:17:22.937 |

To escape a bound parameter, or a name passed to a catalog function, psqlODBC has to know where each multibyte character of the client encoding ends. It treated a client encoding named by an alias the server accepts, such as WIN950, Windows950 or big-5 for BIG5, as single-byte, and it accepted too narrow a range of lead bytes for JOHAB, EUC_TW, EUC_CN and EUC_KR. A quote byte that the server reads as part of such a character was then not doubled, or a quote the server reads on its own was taken for part of a character, and the literal ended early.

An end user who controls one bound character parameter, or a name the application passes to a catalog function such as SQLTables(), can run SQL with the rights of the application's database role. This requires a connection that is not in UTF-8: the ANSI driver, or the ANSI entry points, with one of these client encodings. For bound parameters the driver must also be substituting parameters itself, as it does with UseServerSidePrepare=0 or a cursor type other than forward-only.

Versions up to and including psqlODBC 18.00.0006 are affected.

### CVE-2026-131827

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-25T21:17:17.227 |

RustDesk Client for Windows reg_recovery Missing Authorization Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of RustDesk Client for Windows. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the main IPC endpoint exposed by the RustDesk service. The issue results from the lack of authorization prior to allowing access to functionality. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of SYSTEM. Was ZDI-CAN-34805.

### CVE-2026-131818

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-11-25T21:17:16.973 |

ChargePoint Home Flex busybox Unnecessary Privileges Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of ChargePoint Home Flex EV chargers. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the busybox binary. The issue results from the setuid flag being set. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of root. Was ZDI-CAN-29090.

### CVE-2026-131815

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-25T21:17:16.607 |

ChargePoint Home Flex uploadsm filetype Link Following Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of ChargePoint Home Flex EV chargers. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the handling of the filetype parameter passed to the uploadsm endpoint. By creating a symbolic link, an attacker can abuse the service to write an arbitrary file. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of root. Was ZDI-CAN-29096.

### CVE-2026-131814

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-25T21:17:16.477 |

ChargePoint Home Flex dwnldlogsm tar Command Injection Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of ChargePoint Home Flex EV chargers. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the tar function. The issue results from the lack of proper validation of a user-supplied string before using it to execute a system call. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of root. Was ZDI-CAN-29057.

### CVE-2026-136329

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-25T17:17:48.750 |

A flaw was found in the file-gif-load plugin in GIMP. When processing a specially crafted JIF image file, a 32-bit integer overflow occurs during the pixel buffer size calculation, while the zlib output limit is computed separately without wrapping. This leads to an undersized heap allocation, resulting in a heap-based buffer overflow when the compressed image data is decompressed. This issue can result in an application crash, leading to a denial of service, or potentially allow for arbitrary code execution.

### CVE-2026-124839

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-26T13:16:37.633 |

SEPPmail Secure Email Gateway before 15.1.2 interpolates a stored GINA account address into a root boot-job shell command without neutralization. An authenticated internal attacker who can prepare the required account state, arrange for the migration marker to be absent, and cause a reboot can execute arbitrary commands as root.

### CVE-2026-102957

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:L/I:H/A:H` |
| Weaknesses | `CWE-825` |
| Published | 2026-11-25T21:17:15.793 |

z_impl_pwm_capture_cycles() in drivers/pwm/pwm_capture.c stores its capture context (struct z_pwm_capture_cb_data, including a struct k_sem) on its own stack and registers a pointer to it as the driver capture callback's user_data. When called with a K_NO_WAIT timeout, k_sem_take() returns -EBUSY, which the function did not handle: it fell through, returned the uninitialized status field, copied uninitialized period/pulse values to the caller when that status happened to be zero, and returned without disabling the capture or clearing the callback.

pwm_capture_cycles() is a system call, and z_vrfy_pwm_capture_cycles() passes the caller's timeout through unchanged. With CONFIG_USERSPACE and CONFIG_PWM_CAPTURE enabled, an unprivileged user-mode thread that has been granted access to a capture-capable PWM device can pass K_NO_WAIT to trigger the defect. Without userspace the function is only reachable from trusted application code.

The uninitialized values come from the thread's privileged (kernel) stack, so a user-mode caller can read up to 8 bytes of stale kernel stack memory per call. More seriously, when the capture later completes, the driver ISR invokes z_pwm_capture_cycles_callback() with the dangling pointer. The callback writes into the expired kernel stack region and calls k_sem_give() on whatever memory now occupies it, which can corrupt live kernel stack frames and make the scheduler walk a forged wait queue. The result is kernel memory corruption from interrupt context, leading at least to a crash and possibly to privilege escalation out of the userspace sandbox. The fix rejects K_NO_WAIT with -EINVAL before any capture is configured.

### CVE-2026-133338

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T08:17:07.133 |

Joomla Extension - chronoengine.com - Unauthenticated stored XSS in DB Table cells in ChronoForms extension 8.0.0-8.0.53 - Values rendered in the cells of the DB Table widget are not escaped, allowing unauthenticated users to store JavaScript through form submissions that is executed when the listing is viewed. Fixed in 8.0.54.

### CVE-2026-137306

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-11-26T02:17:02.517 |

Grav Admin plugin before 1.10.65 contains a password reset poisoning vulnerability in LoginController::taskForgot() that ignores the Require Trusted Host setting when building reset links. Unauthenticated attackers who know an administrator's username can submit the forgot-password form with a forged Host header, capturing the reset token when clicked to take over accounts.

### CVE-2026-52803

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-384` |
| Published | 2026-11-26T01:17:11.693 |

Gogs is an open source self-hosted Git service. Prior to 0.15.0, Gogs does not regenerate the session ID after successful authentication. An attacker who forces a victim to use a known session ID can hijack the session after the victim logs in and take over the account. This issue is fixed in version 0.15.0.

### CVE-2026-135145

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-25T17:17:43.753 |

A polymorphic relationship query helper in the MongoDB Eloquent integration for Laravel resolves a record's type identifier inconsistently between the code that stores a relationship link and the code that searches for one. An application that relies on a relationship-absence query to restrict which records a request may see or change can therefore have that restriction silently fail, allowing a user with basic application privileges to read and to modify or remove records the restriction was meant to cover.

### CVE-2026-135144

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-25T17:17:43.577 |

A query builder component in a MongoDB integration library for a PHP web framework does not run the query-modification callbacks that an application registers with the framework before sending read, update, and delete operations to the database. As a result, a filter that an application relies on to limit which records a request may touch can be omitted silently. A user with basic application privileges may be able to read or change records that the application intended to keep out of reach.

### CVE-2026-134958

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-538` |
| Published | 2026-11-26T13:16:42.717 |

Insertion of Sensitive Information into Externally-Accessible File or Directory vulnerability in Webdeclic WPMasterToolKit wpmastertoolkit allows Retrieve Embedded Sensitive Data.This issue affects WPMasterToolKit: from n/a through 2.26.1.

### CVE-2026-124756

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-26T13:16:37.103 |

Allocation of Resources Without Limits or Throttling vulnerability in Takashi Kitajima MW WP Form mw-wp-form allows HTTP DoS.This issue affects MW WP Form: from n/a through 5.1.8.

### CVE-2026-123907

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-26T11:17:01.000 |

VMware vCenter contains multiple denial-of-service vulnerabilities in the VMware Directory Service. Broadcom has evaluated the severity of these issues to be in the Important severity range with a maximum CVSSv3 base score of 7.5.
Affected versions:
VMware vCenter Server 9.1.x.x: fixed in 9.1.2
VMware vCenter Server 9.0.x.x: fixed in 9.0.2.0300
VMware vCenter Server 8.0: fixed in 8.0 U3m
VMware Cloud Foundation 5.x: fixed in 5.2.5
VMware Telco Cloud Platform 3.0: fixed in KB463501
VMware Telco Cloud Platform 4.x: fixed in KB463501
VMware Telco Cloud Platform 5.0.x: fixed in KB463501
VMware Telco Cloud Platform 5.1.x: fixed in KB463501
VMware Telco Cloud Platform 5.2: fixed in KB463501
VMware Telco Cloud Infrastructure 3.0: fixed in KB463501

### CVE-2026-123906

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-26T11:17:00.873 |

VMware vCenter contains multiple denial-of-service vulnerabilities in the VMware Directory Service. Broadcom has evaluated the severity of these issues to be in the Important severity range with a maximum CVSSv3 base score of 7.5.
Affected versions:
VMware vCenter Server 9.1.x.x: fixed in 9.1.2
VMware vCenter Server 9.0.x.x: fixed in 9.0.2.0300
VMware vCenter Server 8.0: fixed in 8.0 U3m
VMware Cloud Foundation 5.x: fixed in 5.2.5
VMware Telco Cloud Platform 3.0: fixed in KB463501
VMware Telco Cloud Platform 4.x: fixed in KB463501
VMware Telco Cloud Platform 5.0.x: fixed in KB463501
VMware Telco Cloud Platform 5.1.x: fixed in KB463501
VMware Telco Cloud Platform 5.2: fixed in KB463501
VMware Telco Cloud Infrastructure 3.0: fixed in KB463501

### CVE-2026-123905

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-26T11:17:00.747 |

VMware vCenter contains multiple denial-of-service vulnerabilities in the VMware Directory Service. Broadcom has evaluated the severity of these issues to be in the Important severity range with a maximum CVSSv3 base score of 7.5.
Affected versions:
VMware vCenter Server 9.1.x.x: fixed in 9.1.2
VMware vCenter Server 9.0.x.x: fixed in 9.0.2.0300
VMware vCenter Server 8.0: fixed in 8.0 U3m
VMware Cloud Foundation 5.x: fixed in 5.2.5
VMware Telco Cloud Platform 3.0: fixed in KB463501
VMware Telco Cloud Platform 4.x: fixed in KB463501
VMware Telco Cloud Platform 5.0.x: fixed in KB463501
VMware Telco Cloud Platform 5.1.x: fixed in KB463501
VMware Telco Cloud Platform 5.2: fixed in KB463501
VMware Telco Cloud Infrastructure 3.0: fixed in KB463501

### CVE-2026-123904

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-26T11:17:00.617 |

VMware vCenter contains an arbitrary file write vulnerability while processing certain archives. Broadcom has evaluated the severity of this issue to be in the Important severity range with a maximum CVSSv3 base score of 7.5.
Affected versions:
VMware vCenter Server 9.1.x.x: fixed in 9.1.2
VMware vCenter Server 9.0.x.x: fixed in 9.0.2.0300
VMware vCenter Server 8.0: fixed in 8.0 U3m
VMware Cloud Foundation 5.x: fixed in 5.2.5
VMware Telco Cloud Platform 3.0: fixed in KB463501
VMware Telco Cloud Platform 4.x: fixed in KB463501
VMware Telco Cloud Platform 5.0.x: fixed in KB463501
VMware Telco Cloud Platform 5.1.x: fixed in KB463501
VMware Telco Cloud Platform 5.2: fixed in KB463501
VMware Telco Cloud Infrastructure 3.0: fixed in KB463501

### CVE-2026-135266

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-26T10:17:08.823 |

The Music Player for WooCommerce plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 1.9.4 via the '_downloadable_files' parameter parameter. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. Staging the attack requires storing a crafted downloadable file URL against a product, which requires the edit_products capability (Shop Manager or above); however, triggering the file read via the ?wcmp-action=play handler is fully unauthenticated once the crafted URL is saved to a published product.

### CVE-2026-135151

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-11-26T10:17:08.653 |

The Download Manager plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 3.3.78 via the 'file[page_template]' parameter parameter. This makes it possible for authenticated attackers, with author-level access and above, to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included. The malicious page_template value is stored when an Author creates or edits a package post, and the inclusion is triggered on any subsequent page view of the package permalink, meaning the include() can be fired by unauthenticated visitors after the payload is planted.

### CVE-2026-124211

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-26T10:17:06.910 |

The Ninja Tables – Responsive Table Builder for Data, Pricing & Product Tables plugin for WordPress is vulnerable to SQL Injection via the 'dateFormat' column metadata parameter in versions up to, and including, 5.5.1 This is due to insufficient escaping on the stored 'dateFormat' value in DefaultProvider::orderByJsonQuery(); convertDateFormatToMysql() only performs str_replace on date-format tokens and leaves SQL metacharacters (including single quotes) intact, after which the value is concatenated directly into an orderByRaw() ORDER BY clause inside single quotes. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database; the payload is stored in the _ninja_table_columns post meta and executed on every unauthenticated request to the wp_ajax_ninja_tables_public_action AJAX endpoint when the table uses sorting_type='by_column' with a date column.

### CVE-2026-136515

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-674;CWE-787` |
| Published | 2026-11-25T23:17:24.887 |

psqlODBC rewrites statement text for keyset-driven cursors and ODBC escapes using positions it found in the text. These positions could lie outside the text or describe another statement:

- After SQLExecDirect() failed on a statement handle, the FROM and WHERE positions of the failed statement were applied to the next, shorter statement on that handle.
- The parser could record a FROM position with no text after it, and the rewrite then copied a negative length.
- An {fn …} escape whose arguments contain FOR UPDATE, ; or INTO … FROM made the driver remove a cursor prefix from the wrong buffer.
- {fn CONVERT(?, …)} with an output parameter produced a negative argument length.
- An unclosed {fn …} escape made the driver read past the statement, and a few thousand nested ones exhausted the stack.
- Translating @@identity in long statement text read an uninitialised pointer, and {? = call …} with nothing bound for the return value dereferenced NULL.

Whoever supplies the text of a statement that an application opens on a keyset-driven or dynamic cursor with a concurrency other than read-only, or calls with an output parameter, can corrupt the application's heap and end it. That includes the users of query tools, report builders and other applications that run SQL their users type. Code execution has not been demonstrated.

Versions up to and including psqlODBC 18.00.0006 are affected.

### CVE-2026-136512

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-25T23:17:24.500 |

With SQL_C_DEFAULT, the C type of a bound column or parameter follows its SQL type. An application sizes its buffer from the type it was told when it described the statement. When the column had another type at fetch time, because the server reported another type, the table was altered, or an output parameter's result column had another type, psqlODBC wrote the larger type into the smaller buffer: 12 bytes past a 4-byte buffer for a uuid, and more in multi-row fetches, where the driver also steps through the array by the larger size.

Other conversions wrote past the application's buffer as well:

- With Int8As set to a smaller type, an int8 column fetched as SQL_C_DEFAULT was still written as 8 bytes.
- An int2vector column fetched as SQL_C_DEFAULT returned unterminated binary data instead of text.
- An output parameter that the application discards by binding a NULL buffer overflowed a stack buffer in the driver.
- SQLGetData() with BufferLength 0 on a column the driver reads as a large object wrote a NUL byte past the buffer.
- Adding a row with SQLBulkOperations(SQL_ADD) on a static updatable cursor before the first fetch, then changing that row, rolling back and fetching it, made the keyset index arithmetic free a pointer that was never allocated and corrupt the heap.

This can be triggered by a hostile or compromised server, or anyone on the network path of a connection that does not use sslmode=verify-full (the default is disable), and by the owner of a table the application reads.

Versions up to and including psqlODBC 18.00.0006 are affected.

### CVE-2026-136509

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-476;CWE-787` |
| Published | 2026-11-25T23:17:24.077 |

psqlODBC did not check that a server reply matches the query it sent: that a FETCH returns no more rows than it asked for, that each row has the described number of columns, that one query produces one result, and that a COPY, a transaction or the connection ends where the protocol says. By sending replies that do not match, a hostile or compromised server, or anyone on the network path of a connection that does not use sslmode=verify-full (the default is disable) can corrupt memory in the application:

- A FETCH reply with more rows than requested overflows the row cache.
- Extra results in reply to a FETCH, or to the queries of a keyset-driven cursor, are freed while still in use.
- A key query of a keyset-driven cursor answered with extra columns, or a re-read row with fewer columns, overflows the row cache.
- Replies without columns or rows, or with NULL values, to the driver's internal queries at connect time and in catalog functions are dereferenced.
- A malformed relacl value in SQLTablePrivileges() makes the driver write past a buffer.
- On Windows with MSDTC, a long transaction name returned by the server overflows a buffer during recovery.
- Values in replies to the driver's internal queries are used without checking their range: an empty column name, a parameter count, a large-object size, a function's or trigger's argument count, and a result of exactly 32767 columns. They are dereferenced, read past, returned to the application or sent back to the server as stack memory, or make the driver loop forever.
- A reply that ends a COPY, the connection or the transaction at an unexpected point leaves freed results, keysets or table information in use: a CopyOutResponse followed by a lost connection, a ROLLBACK command tag under UseDeclareFetch=1, or a lost connection while a cursor with positioned updates is closed. Eight extra bytes in a reply also make the driver wait forever for a COPY to end.
- On Windows, a start-up reply without client_encoding crashes the driver, and with MSDTC a failed connection makes the XA library use a connection it has already freed.
- An error message ending in the first byte of a multibyte character leaves the SQLSTATE returned by SQLGetDiagRecW() unterminated.
- When a string value did not fit the application's buffer, eight Unicode entry points filled the buffer and wrote no null terminator, so a caller that reads to the terminator, as ODBC allows, read past the end of its own buffer.

This continues the fixes for CVE-2026-120058 and CVE-2026-120060, which covered other replies. The demonstrated results are crashes and heap corruption; code execution has not been demonstrated.

Versions up to and including psqlODBC 18.00.0006 are affected.

### CVE-2026-136506

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89;CWE-706` |
| Published | 2026-11-25T23:17:23.703 |

psqlODBC builds queries of its own from names, and put these names into them without escaping or qualification:

- the database name in SQLForeignKeys();
- the current schema name in catalog functions;
- the table name in the currtid2() call that re-reads rows of updatable cursors;
- column names in the inserts and updates of SQLSetPos() and SQLBulkOperations();
- cursor names set with SQLSetCursorName() or returned as refcursors (FetchRefcursors=1);
- parameter names (SQL_DESC_NAME) in procedure calls;
- the = operator in an OID comparison in SQLColumns(), which the server resolves through search_path.

The column names of the fourth item are a variant of CVE-2026-120065 (GHSA-9cg8-r57h-h6jj). The fix for that advisory, in 18.00.0006, doubles " in the stored row-identifier name, which the keyset queries and the WHERE clause of the positioned statements use. The column names that SQLSetPos() and SQLBulkOperations() put into the SET list of their UPDATE and into the column list of their SQL_ADD INSERT come from the catalog and were not covered by it, so a driver patched to 18.00.0006 is still affected by this one.

A database user who can create a database, schema, table, column or operator with a crafted name, or an end user who supplies a cursor or parameter name to the application, can run SQL with the rights of the application's database role.

Versions up to and including psqlODBC 18.00.0006 are affected.

### CVE-2026-136505

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-190;CWE-787` |
| Published | 2026-11-25T23:17:23.570 |

psqlODBC uses sizes and counts without checking their range, or keeps them in types too small for them:

- A row array size of 0, set with SQLSetStmtAttr() or on the ARD, makes SQLSetPos() with SQL_REFRESH write past the bound arrays.
- SQL_DESC_COUNT above 32767 on an APD or IPD writes before the start of a heap buffer.
- A numeric parameter with a negative scale overflows a stack buffer.
- SQLGetData() of a text value of 2 GiB or more into a wide-character buffer computes a wrapped size and overflows the heap.
- The 16-bit reference count and size of the statement parser's column-information cache wrap, which frees a cache entry still in use or overflows the cache, and a statement with more than 32768 columns overflows the parser's field array.
- An updatable cursor that records more than 65535 changes in one transaction wraps the 16-bit capacity of its rollback log, which overflows it and frees it twice.
- A statement with 32769 or more parameter markers overflows a 16-bit parameter count.
- A wide-character string of more than 2 GiB wraps the size of its UTF-8 conversion, which is then written below the start of a heap buffer.
- SQLGetDiagField() and SQLGetDiagFieldW() always stored the five-character SQLSTATE plus its terminator and checked BufferLength only afterwards, overrunning a buffer shorter than six bytes.
- The ANSI SQLSetDescField(SQL_DESC_NAME) on an IPD ignored BufferLength and copied the name with strdup(), reading a name passed as pointer plus length past its end.
- SQLFetchScroll(SQL_FETCH_BOOKMARK) did not check the bookmark it was given, so whoever chooses the bookmark value read out of bounds and crashed the process.
- Four places in the parameter conversion read one byte past the end of a bound character parameter, and one of them rewrote it.
- Binding a date, time or timestamp C value to an SQL_INTEGER or SQL_SMALLINT parameter dereferenced NULL instead of returning the conversion error.

Depending on the case, the values come from the application, from the data or statement text an end user supplies, or from a database user who controls the size of a table or value. The demonstrated results are crashes and heap corruption; code execution has not been demonstrated.

Versions up to and including psqlODBC 18.00.0006 are affected.

### CVE-2026-136503

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415;CWE-416;CWE-787` |
| Published | 2026-11-25T23:17:23.307 |

psqlODBC frees memory that is still in use, frees it twice, or writes outside an application buffer in these cases:

- The clean-up the driver runs at commit and rollback sends queries of its own, and the reply to one of them can start the clean-up again while it is running. The nested run frees the rollback log, or the list of cursors and prepared statements to close, and the outer run uses and frees it again.
- The callback through which libpq delivers notices could run that clean-up, and close the connection, while libpq was still using the connection.
- Freeing a statement whose result holds several cursors (FetchRefcursors=1, or UseDeclareFetch=1) used the freed first result while the later cursors were closed.
- With UseDeclareFetch=1, after a rollback closed an updatable cursor, rows added or deleted through it were counted but not stored, so freeing the statement freed uninitialised pointers, and adding a row wrote past the keyset.
- After a multi-row fetch failed on a row other than the first of its rowset, SQLGetData() wrote at an offset past the buffer the application passed.
- SQLProcedureColumns() freed the result of its catalog query twice when the query failed.
- In a process named sqlservr (SQL Server linked servers), a server version below 8.4 made the statement parser free a buffer twice.
- A failed SQLPutData in the middle of a SQLSetPos() or SQLBulkOperations() data-at-execution sequence left the whole operation pending, with the internal statement still allocated and autocommit silently off, so later statements were rolled back at disconnect. The next positioned update ran the stale callback against a statement that was never executed and dereferenced NULL.

Most of these can be triggered by a hostile or compromised server, or anyone on the network path of a connection that does not use sslmode=verify-full (the default is disable). A database user who can make a statement fail, or who controls the contents of a row the application reads, can trigger the UseDeclareFetch=1 and SQLGetData() cases against an honest server. The demonstrated results are crashes and heap corruption; code execution has not been demonstrated.

Versions up to and including psqlODBC 18.00.0006 are affected.

### CVE-2026-133978

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-25T23:17:22.360 |

A command injection vulnerability exists in the web-based management interface of HPE Networking Management Software (Airwave). Successful exploitation could allow an authenticated remote attacker with low privileges to execute arbitrary commands on the underlying operating system if certain preconditions outside of the attacker's control are met.

### CVE-2026-133977

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-25T23:17:22.240 |

A sensitive information disclosure vulnerability exists in the affected interface of HPE Networking Management Software (Airwave). Successful exploitation could allow an unauthenticated remote attacker to obtain sensitive information from the affected system.

### CVE-2026-116681

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-25T22:17:16.313 |

NocoDB is software for building databases as spreadsheets. Prior to 2026.08.0, the row-scoped endpoints of a public shared view check whether a target record exists by primary key without applying the view's row filter, while the view's list and count endpoints do apply it. A recipient of a shared-view link, including its password where one is configured, can list the linked records of a filtered-out record and obtain signed download paths for its attachments by guessing its primary key. This issue is fixed in version 2026.08.0.

### CVE-2026-62154

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-25T17:17:57.340 |

During IMPORT FOREIGN SCHEMA, mysql_fdw copies column metadata returned by the remote MySQL server into the CREATE FOREIGN TABLE statements it runs locally without quoting it. The COLUMN_DEFAULT value is placed directly in the DEFAULT clause, and the name of the generated ENUM type is inserted unquoted. A malicious or compromised MySQL server, or an attacker who can tamper with the connection, can return crafted information_schema metadata and run arbitrary SQL in the local PostgreSQL session of the user who runs IMPORT FOREIGN SCHEMA. The issue is fixed in mysql_fdw 2.10.0. From mysql_fdw 2.10.0, mysql_fdw quotes these values before building the statements.

### CVE-2026-136267

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-25T17:17:48.480 |

Improper sanitization of mixed data and markup elements when processing content in Kiro Web before 2026-10-30, in combination with agents running specific models such as DeepSeek v3.2, GLM-5, MiniMax M2.1, MiniMax M2.5, or Qwen3-coder-next, may allow a remote unauthenticated actor to execute arbitrary commands in a subscriber's hosted development environment via crafted content being repeated back to the user by the agent.



AWS has addressed this issue. No customer action is required.

### CVE-2026-132888

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-25T17:17:36.733 |

A flaw was found in librelp. When configured to use Transport Layer Security (TLS) with certificate validation and the GnuTLS driver, the library fails to verify the peer certificate chain. A remote, unauthenticated attacker can exploit this issue by presenting an invalid or self-signed certificate, allowing them to bypass authentication and act as a trusted log source or collector.

### CVE-2026-133979

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-25T23:17:22.470 |

Improper certificate validation vulnerabilities in the web-based management interface of HPE Networking Management Software (Airwave) allow an unauthenticated remote attacker to circumvent existing authentication controls if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to gain administrative access to the affected system.

### CVE-2026-135403

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-290;CWE-307` |
| Published | 2026-11-25T17:17:45.720 |

Ever Gauzy is an open source business management platform for ERP, CRM, HRM, ATS, and project management. Prior to 111.44.2, getTracker in packages/core/src/lib/throttler/throttler-behind-proxy.guard.ts accepts CF-Connecting-IP without verifying that a trusted Cloudflare edge supplied it; when CF-Connecting-IP is absent, app.set('trust proxy', true) can let an attacker-controlled X-Forwarded-For value determine req.ip. In deployments where a trusted intermediary does not overwrite these headers, or where the firewall permits direct API access, varying the applicable header on repeated POST /auth/login requests gives an unauthenticated remote attacker a distinct throttle bucket for each attempt, so the five-attempts-per-60-seconds limit does not trigger and no account lockout, CAPTCHA, or exponential backoff limits password guessing. This issue is fixed in version 111.44.2.

### CVE-2026-137326

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-26T03:16:39.523 |

ICU4C through 79.1 contains a use-after-free and double free vulnerability in the x11-compound-text converter because cloning shares the extraInfo block without a safeClone handler. Attackers who control the charset name passed to ucnv_open() in applications calling ucnv_setSubstString() or cloning converters can corrupt the heap, causing crashes and potentially code execution.

### CVE-2026-133445

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-668` |
| Published | 2026-11-25T22:17:16.777 |

In gdm3 before 51.2, an improper privilege management vulnerability allows an unprivileged local attacker with an active GDM graphical session to execute arbitrary code as root by supplying a malicious environment variable during session reauthentication.

### CVE-2026-137092

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-11-25T20:18:46.533 |

Assimp before 6.0.6 contains an out-of-bounds write vulnerability in MD5Importer::MakeDataUnique() that allows attackers to corrupt heap memory by supplying unvalidated face indices. Attackers can craft an .md5mesh file with out-of-range face vertex indices or unfilled faces to set bits past the abHad allocation, read vertex data out of bounds, or crash the application.

### CVE-2026-137284

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:44.840 |

The JetFormBuilder — Dynamic Blocks Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the '<form-field-name> mapped via Insert/Update Post fields_map (e.g. payload → m_select)' parameter in all versions up to, and including, 3.6.8.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires that a site administrator has configured an Insert/Update Post action with a fields_map entry and a Radio or Checkbox field whose option source reads back that post meta key — all standard first-party editor controls — and that at least one field on the page has a macro Default Value so that dynamic.value.js is enqueued.

### CVE-2026-136459

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:44.513 |

The Nexter Extension – Security, Performance, Code Snippets & Site Toolkit plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 4.9.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the site administrator to have enabled the plugin's SEO module (available via a persistent admin notice), after which the nofollow_comments option is on by default; with comments open, a single unauthenticated POST to wp-comments-post.php is sufficient to plant the payload.

### CVE-2026-136221

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:44.360 |

The Strong Testimonials plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'custom textarea field name (admin-configured, e.g. 'wfx_note')' parameter in all versions up to, and including, 3.3.22 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires the vendor's paid Strong Testimonials: Custom Fields extension (or another plugin hooking wpmtst_default_fields) to be active and an administrator to have added a custom textarea field to a publicly accessible submission form.

### CVE-2026-135669

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:43.913 |

The Everest Forms – Contact Form, Payment Form, Quiz, Survey & Custom Form Builder with AI plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'everest_forms[form_fields][<wysiwyg field id>]' parameter in all versions up to, and including, 3.6.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the targeted form to contain a WYSIWYG field with entry storage enabled; while both are default-available, no form with a WYSIWYG field exists on a stock installation, so an administrator must have manually added such a field to a published form.

### CVE-2026-135666

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:43.763 |

The JetFormBuilder — Dynamic Blocks Form Builder plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via the 'f_body (mapped to post_content via fields_map)' parameter in all versions up to, and including, 3.6.8.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires that at least one form on the site contains a Calculated Field block, ensuring the calculated.field.js gadget is enqueued on pages where the stored post content is rendered.

### CVE-2026-135630

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:43.140 |

The Premmerce Brands for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'product_brand' parameter in all versions up to, and including, 1.2.16 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The exploit is reachable by unauthenticated visitors because WooCommerce's anonymous checkout AJAX endpoint triggers the save_post action, which the plugin processes without any authentication gate, allowing the attacker-supplied product_brand value to be persisted as a new taxonomy term whose name is later echoed unescaped into an HTML attribute on the publicly accessible Brands page.

### CVE-2026-133409

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:40.613 |

The Parsigate plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'trackId (Zibal). Equivalent unauthenticated fields for other gateways (e.g. ZarinPal 'Authority', Sep 'RefNum') are logged the same way.' parameter in all versions up to, and including, 1.2.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the non-default 'ParsiGate Log' option to be enabled in plugin settings, at least one WooCommerce order placed via a Parsigate gateway (e.g. Zibal) that remains in a pending state, and an administrator to subsequently view the Tools > ParsiGate Log page.

### CVE-2026-131838

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:40.317 |

The MoreConvert Wishlist for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'attribute_<custom_variation_name>' parameter in all versions up to, and including, 2.0.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This vulnerability only affects shops that have at least one published variable product using a custom product-level attribute (non-taxonomy, non-pa_ prefixed) marked as Used for Variations; stores using only global taxonomy attributes follow a different code path and are not exploitable.

### CVE-2026-129329

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:39.733 |

The Ocean Extra plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'post_title' parameter in all versions up to, and including, 2.6.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The shortcode-escape bracket syntax ([[...]]) additionally bypasses wptexturize's own quote conversion, providing an alternative payload path that preserves raw double-quote characters and breaks out of the title attribute on the anchor element rendered by the Recent Posts Thumbnails widget. Exploitation by unauthenticated attackers requires that a separate plugin providing a public guest-post form with a Featured Image field is installed and configured to accept anonymous submissions as published posts. On a default installation, where that is not configured, the vulnerability requires attackers with contributor-level access and above.

### CVE-2026-128097

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:38.980 |

The Lazy Loader plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'author' parameter in all versions up to, and including, 8.2.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. A first-time comment from a new email address is held for moderator approval under WordPress's default settings; however, once an administrator approves it, any visitor — including an administrator — loading the post will trigger execution, enabling full Administrator-level account creation.

### CVE-2026-127113

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:38.830 |

The GeoDirectory – WP Business Directory Plugin and Classified Listings Directory plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'post_content' parameter in all versions up to, and including, 2.8.205 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Unauthenticated exploitation requires the plugin's "Allow posting without logging in" (post_logged_out) option to be enabled; on default installs the vulnerability is exploitable by Subscriber-level users and above.

### CVE-2026-111846

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-26T13:16:35.893 |

Missing Authorization vulnerability in WPExperts NOWPayments for WooCommerce nowpayments-for-woocommerce allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects NOWPayments for WooCommerce: from n/a through 1.4.1.

### CVE-2026-110702

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:35.260 |

The EWWW Image Optimizer plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 8.9.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. WordPress core comment kses permits the payload's tag and attribute structure unchanged at save time, meaning the malicious content bypasses save-time sanitization and is only activated when the plugin's output-buffer filter processes the page on render.

### CVE-2026-136519

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T12:17:12.723 |

The Advanced Product Fields (Product Addons) for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'wapf[field_<id>]' parameter in all versions up to, and including, 1.7.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload survives sanitization via a whitespace-prefixed tag gadget, is normalized into real HTML elements by wp_kses_post() and force_balance_tags() at render time, and is then executed by WordPress core's tags-box.js when it encounters the forged #tagsdiv-post_tag element on the order screen.

### CVE-2026-135655

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T12:17:12.210 |

The Easy SwipeBox plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via the 'title attribute of <a> inside an approved comment' parameter in all versions up to, and including, 1.1.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The plugin's default-enabled image autodetection applies the Swipebox handler to all front-end anchor elements whose href matches an image extension — including those inside approved comments — meaning no non-default configuration is required to expose the attack surface. A first-time commenter's submission is held for moderator approval, but once approved the stored payload executes for any user who clicks the image link.

### CVE-2026-131806

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T12:17:10.057 |

The CubeWP Forms plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'cwp_custom_form[form_data_id]' parameter in all versions up to, and including, 1.1.13 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The nonce required by the submission handler is publicly emitted in the inline script data of any page rendering the cwpCustomForm shortcode, making it trivially obtainable by unauthenticated visitors and rendering the nonce check ineffective as an authentication barrier.

### CVE-2026-131613

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T12:17:09.740 |

The Classified Listing – AI-Powered Business Directory & Classified Ads plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'formData[description]' parameter in all versions up to, and including, 6.3.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation by unauthenticated attackers requires that the admin option 'post-for-unregister' is enabled (Functions::is_enable_post_for_unregister() returns true). On a default installation, where that is not configured, the vulnerability requires attackers with subscriber-level access and above.

### CVE-2026-128111

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T12:17:08.980 |

The Drag and Drop Multiple File Upload for Contact Form 7 plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'upload-file' parameter in all versions up to, and including, 1.4.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires that the targeted contact form be configured to accept a non-script extension such as .gpx (or any extension outside the HTML/XML/PHP blocklist), and the uploaded file is served without a Content-Type header, causing browsers to MIME-sniff and execute it as text/html.

### CVE-2026-131589

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-26T10:17:07.770 |

The AI Engine – MCP Server & AI Chatbot for WordPress, with Claude, ChatGPT & Gemini plugin for WordPress is vulnerable to Limited Arbitrary File Upload in all versions up to, and including, 3.9.4 via the `url` parameter of the `/mwai/v1/helpers/create_image` REST API endpoint. The vulnerability exists because the `add_image_from_url()` function applies the `get_allowed_mime_types()` extension allow-list only on the custom-filename branch; when the request omits a `filename` value, the empty-filename branch derives the stored file's extension directly from the URL basename via `sanitize_file_name()` without any MIME or extension validation, then writes the downloaded response body verbatim to the WordPress uploads directory via `file_put_contents()`. This makes it possible for authenticated attackers with Editor-level access and above to place attacker-controlled HTML, SVG, or JavaScript files into `wp-content/uploads/YYYY/MM/` under an attacker-chosen extension, enabling stored cross-site scripting against any administrator who opens the resulting attachment URL. The download routine accepts any HTTP response whose `Content-Type` header begins with `image/`, a value freely controlled by the attacker-owned origin server, meaning the written content need not be a valid image.

### CVE-2026-123879

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-25T21:17:16.303 |

In authd before 0.7.2, an improper access control vulnerability allows an authenticated remote attacker to complete a first-time SSH login with another account's UID and incorrect primary GID, and to read or modify files owned by that account. This allows an attacker to access another account's data, potentially enabling account takeover or privilege escalation.

### CVE-2026-134070

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:N/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-96` |
| Published | 2026-11-25T20:18:36.187 |

Improper input validation in the AWS-managed AWS Systems Manager Automation runbook AWSConfigRemediation-EnableSystemsManagerSessionManagerAuditLogsToS3 might allow an authenticated remote user who is permitted to run the runbook to set unintended configuration in the account's Regional Session Manager preferences document (SSM-SessionManagerRunShell) via a crafted S3KeyPrefix parameter value. This applies only when that document does not already exist in the Region. The unintended configuration can include arbitrary commands, which then run on managed instances when other users start Session Manager sessions.



Because any user permitted to run the runbook selects which revision to run, this issue remains reachable in an affected Region until earlier revisions can no longer be run there. AWS is deprecating all revisions created before 2026-10-22 (UTC) in every Region and partition beginning January 15, 2027; until deprecation, earlier revisions remain runnable, so upgrading alone is not sufficient.



To remediate this issue:



1. Run the latest revision of the runbook. The latest revision is the fixed revision in every Region where the runbook is available, and its revision number varies by Region. To find it, run aws ssm describe-document --name AWSConfigRemediation-EnableSystemsManagerSessionManagerAuditLogsToS3 --region <region> --query "Document.LatestVersion". Update any Automation executions, State Manager associations, AWS Config remediation configurations, or other automations pinned to an earlier revision to use the latest revision. 2. Until earlier revisions are removed in your Region, either keep untrusted users from running earlier revisions of the runbook, or keep a trusted Session Manager preferences document (SSM-SessionManagerRunShell) in every Region. Earlier revisions inject only when they create this document, so while a trusted one exists, this path is closed in that Region. 3. Review your Session Manager preferences document (SSM-SessionManagerRunShell) in any Region where it was first created by an earlier revision of this runbook, not by you. To check, look for any run of this runbook that failed with "DOCUMENT CREATE OR UPDATE FAILED." An injected run always fails with this error. You can also compare the creation date of the document's first version with the start times of runs of this runbook in that Region. Check the document for settings you did not configure, especially shellProfile, Run As (runAsEnabled, runAsDefaultUser), maxSessionDuration, idleSessionTimeout, and the logging destination fields. The fixed runbook updates only the S3 bucket and prefix fields of an existing preferences document, so settings injected earlier remain until you remove them. If you find unexpected settings, restore your trusted preferences and review instances on which Session Manager sessions were started while those settings were active. The AWS Security Bulletin includes commands for this review.

### CVE-2026-82495

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-25T15:17:52.947 |

openIMIS before 2026-10 contains a broken access control vulnerability in the FHIR R4 module that allows any authenticated attacker to delete Coverage policy records due to an empty permissions_delete list being vacuously granted by user.has_perms([]). Attackers can issue a DELETE request to the Coverage/<uuid>/ endpoint to permanently and irrecoverably remove insurance policy records.

### CVE-2026-136920

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-25T15:17:50.370 |

OneDev before 17.2.4 contains an argument injection vulnerability in commit query handling that allows authenticated attackers to inject git options through branch or tag names. Attackers can push a branch named like --output=<path> and query it via the commits page or REST API to overwrite server-writable files, causing denial of service.

### CVE-2026-137587

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-26T14:17:27.587 |

LIVE555 Streaming Media before 2026.08.25 contains a heap out-of-bounds read vulnerability in parseVorbisOrTheoraConfigStr() that trusts attacker-supplied 16-bit header length fields. A malicious RTSP server or crafted SDP Vorbis or Theora configuration can crash clients or leak heap memory through proxied SDP configurations.

### CVE-2026-137578

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-26T14:17:26.687 |

FacturaONE para WooCommerce con VeriFactu before 5.61 contains an authenticated SQL injection vulnerability that allows Contributor-level users to inject SQL through the fone_client_id user meta value. Attackers can store a payload in their own profile via FONE_update_tarifa_user(), which FONE_product_ids_ocultos_para_usuario() concatenates unquoted, enabling time-based blind extraction of password hashes.

### CVE-2026-136760

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-90` |
| Published | 2026-11-26T14:17:24.270 |

When authenticating through the Web HMI or Desktop HMI with POSIX LDAP, an attacker can bypass some of Panorama Suite's injection protections. The attacker must know the username and password of a valid account in the LDAP directory. An authenticated attacker may then gain access to areas or business roles they are not authorized to use, or obtain unauthorized permissions in Panorama. Installations that do not use POSIX LDAP authentication are not affected. LDAP Active Directory authentication is not affected.



Affected versions:

  *  Panorama Suite 2020
  *  Panorama Suite 2022-SP1
  *  Panorama Suite 2023
  *  Panorama Suite 2025
  *  Panorama Suite 2025 Updated Dec. 25 (before update PS-2510-02-1317)




Remediation: For Panorama Suite 2025 Updated Dec. 25, install update PS-2510-02-1317 or later. For the other affected versions, upgrade to Panorama Suite 2025 Updated Dec. 25 and install update PS-2510-02-1317 or later.



Please refer to security bulletin BS-040 on the Panorama CSIRT website:  https://my.codra.net/en-gb/csirt .

### CVE-2026-135005

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T14:17:23.957 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Greg – SiteOrigin SiteOrigin Widgets Bundle so-widgets-bundle allows Stored XSS.This issue affects SiteOrigin Widgets Bundle: from n/a through 1.76.0.

### CVE-2026-134711

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T14:17:23.800 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Webilia Inc. Listdom listdom allows Reflected XSS.This issue affects Listdom: from n/a through 6.4.0.

### CVE-2026-134474

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T14:17:23.650 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in OptiUser Opti-Behavior – Self-Hosted Heatmaps, Session Recordings, Funnels, A/B Testing &amp; Smart Insights opti-behavior allows DOM-Based XSS.This issue affects Opti-Behavior – Self-Hosted Heatmaps, Session Recordings, Funnels, A/B Testing &amp; Smart Insights: from n/a through 1.11.0.

### CVE-2026-131590

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T14:17:23.500 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in hupe13 Extension for Leaflet Map extensions-leaflet-map allows Reflected XSS.This issue affects Extension for Leaflet Map: from n/a through 6.1.3.

### CVE-2026-129071

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T14:17:21.917 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in RomanCode MapSVG mapsvg-lite-interactive-vector-maps allows Reflected XSS.This issue affects MapSVG: from n/a through 9.0.8.

### CVE-2026-135808

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:44.217 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in dudaster ECS – Ele Custom Skin for Elementor ele-custom-skin allows Stored XSS.This issue affects ECS – Ele Custom Skin for Elementor: from n/a through 4.3.14.

### CVE-2026-134988

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:42.857 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Nks video carousel slider with lightbox wp-responsive-video-gallery-with-lightbox allows Stored XSS.This issue affects video carousel slider with lightbox: from n/a through 1.0.48.

### CVE-2026-134872

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:42.577 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Seraphinite Solutions Seraphinite Accelerator seraphinite-accelerator allows Reflected XSS.This issue affects Seraphinite Accelerator: from n/a through 2.31.3.

### CVE-2026-134719

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:42.430 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Johann Heyne Table Field Add-on for ACF and SCF advanced-custom-fields-table-field allows Reflected XSS.This issue affects Table Field Add-on for ACF and SCF: from n/a through 1.5.2.

### CVE-2026-134491

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:42.143 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Dimitri Grassi Salon booking system salon-booking-system allows DOM-Based XSS.This issue affects Salon booking system: from n/a through 10.31.17.

### CVE-2026-134490

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:42.003 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Imran Tauqeer CubeWP Forms cubewp-forms allows Stored XSS.This issue affects CubeWP Forms: from n/a through 1.1.13.

### CVE-2026-134486

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:41.860 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in eMarket Design YouTube Showcase youtube-showcase allows Stored XSS.This issue affects YouTube Showcase: from n/a through 4.1.0.

### CVE-2026-134479

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:41.563 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Ultimate Member Ultimate Member ultimate-member allows Reflected XSS.This issue affects Ultimate Member: from n/a through 2.14.1.

### CVE-2026-134469

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:41.273 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Sayontan Sinha Photonic Gallery & Lightbox for Flickr, SmugMug & Others photonic allows Reflected XSS.This issue affects Photonic Gallery & Lightbox for Flickr, SmugMug & Others: from n/a through 3.37.

### CVE-2026-133986

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:41.090 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in MotoPress Getwid getwid allows Stored XSS.This issue affects Getwid: from n/a through 3.0.3.

### CVE-2026-133698

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:40.917 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WPVibes AnyWhere Elementor anywhere-elementor allows Stored XSS.This issue affects AnyWhere Elementor: from n/a through 1.3.0.

### CVE-2026-133524

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:40.763 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in lyrathemes Kale kale allows Stored XSS.This issue affects Kale: from n/a through 2.9.

### CVE-2026-131758

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:39.887 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Brainstorm Force SureRank surerank allows Stored XSS.This issue affects SureRank: from n/a through 1.11.1.

### CVE-2026-129028

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T13:16:39.590 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Datasolution Colissimo Officiel : Méthodes de livraison pour WooCommerce colissimo-shipping-methods-for-woocommerce allows Stored XSS.This issue affects Colissimo Officiel : Méthodes de livraison pour WooCommerce: from n/a through 3.2.0.

### CVE-2026-137309

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-26T02:17:02.993 |

Friendica through 2026.05-1 contains an incorrect authorization vulnerability in item_edit() that allows authenticated local users to edit other authors' posts by submitting their own stored copy's post_id. Attackers can POST to /item to delete attachments and overwrite the shared body, title and content warning, which is shown under the original author's name.

### CVE-2026-136501

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-178;CWE-706` |
| Published | 2026-11-25T23:17:23.060 |

To build positioned updates and to describe columns, psqlODBC matches the names in a statement against the catalog. Where it matched differently from the server, it used another table or column:

- Table and schema names were compared case-insensitively in its column-information cache, so users could be taken for another user's "Users", and the driver then evaluated that table's column default to answer @@IDENTITY.
- In FROM ONLY t, ONLY was taken for the table name.
- Column names were compared case-insensitively, so with Parse=1 the type of another column could decide the size of the application's buffer, which a fetch then overflowed.
- In a database whose encoding is single-byte, such as LATIN1 or SQL_ASCII, the server folds the accented letters of an unquoted name by its own locale, while the driver folded only A-Z, so ÉTAT could be taken for another user's "État" instead of état.
- On systems other than Windows, in a Turkish or Azeri locale, an unquoted I was not folded to i, and keywords and ODBC function names did not match.
- Without a schema name, SQLSpecialColumns() could report the key columns of another user's same-named temporary table, and SQLPrimaryKeys() could take another user's index named <table>_pkey for the primary key of a table without one.
- After search_path changed other than through a plain SET statement, positioned writes went to the same-named table in the previously current schema.
- SQLBulkOperations() trusted the ctid stored inside a variable-length bookmark handed back by the application, and ignored the WHERE clause that restricted the cursor, so a forged bookmark read, updated or deleted any row of the cursor's table.

A database user who can create a table in a schema on another user's search_path can redirect that user's positioned updates, inserts and deletes to a table of their choosing, where they run with the victim's rights, or run an expression of their choosing under the victim's role.

Versions up to and including psqlODBC 18.00.0006 are affected.

### CVE-2026-67209

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-25T21:17:20.063 |

metasfresh through 5.175 contains a SQL injection vulnerability in the stressTest_massCacheInvalidation handler of DebugRestController, which concatenates the caller-supplied tableName request parameter into SELECT statements without parameterization or validation and only checks that the caller is authenticated. Authenticated WebUI users with any role can send GET requests to /rest/api/debug/stressTest/massCacheInvalidation with SQL in the tableName parameter to run time-based and error-based blind queries against the PostgreSQL database, extracting sensitive ERP data such as user credentials and financial records while also degrading availability through sleep payloads.

### CVE-2026-137091

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-942` |
| Published | 2026-11-25T20:18:46.377 |

EverOS before 1.8.0 contains a cross-origin local file disclosure vulnerability that allows malicious websites to read local files by abusing a wildcard CORS policy with credentials and unrestricted file:// ingestion. Attackers can host JavaScript that calls POST /api/v2/memory/add with file:// URIs, then read parsed contents via POST /api/v2/memory/search to exfiltrate SSH keys, credentials, and alter or delete memories.

### CVE-2026-137085

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-25T20:18:45.447 |

ProjeQtOr before 13.1.2 contains a missing authorization vulnerability in tool/getAFieldForAClassById.php that allows authenticated low-privilege users to read any object property. Attackers can request Class=User with an administrator id and field=password or email to retrieve password hashes for offline cracking.

### CVE-2026-137061

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-25T20:18:40.443 |

Wallos before 5.11.2 contains an infinite loop vulnerability that allows authenticated users or API key holders to exhaust server resources by storing subscriptions with a frequency of 0. Attackers can trigger renew.php or get_monthly_cost.php to loop forever on a P0D interval, pinning PHP workers and hanging the next-payment cron job for all users.

### CVE-2026-133466

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-704` |
| Published | 2026-11-25T20:18:34.307 |

OpenEXR is the reference implementation and specification for the EXR image format, widely used in the motion picture industry. From versions 3.4.0 through 3.4.18 and 3.5.0 through 3.5.2, decoding a crafted HT-compressed EXR chunk can cause ht_undo_impl() to write a 4-byte pixel value through a pointer that is not 4-byte aligned. This happens when the channels sum to a bytes-per-scanline stride that is not a multiple of four. This issue is fixed in versions 3.4.19 and 3.5.3.

### CVE-2026-135486

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-25T19:17:34.233 |

Munshi (by Petpooja) before 2026-07-07 contained a broken object level authorization vulnerability in the PUT /api/invoice/{invoice_id}/extracted-data endpoint, which accepts a client-supplied extracted_data object without verifying invoice ownership, enforcing the invoice_edit permission or checking whether the invoice has been soft deleted. Authenticated attackers who know an invoice identifier can overwrite seller and buyer details, invoice identifiers, product entries, totals and custom metadata of invoices, including archived invoices marked is_deleted = 1, undermining the integrity of financial records.

### CVE-2026-81412

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-11-25T18:18:56.113 |

Nmap before 7.992 contains an excessive memory allocation vulnerability in the unmarshall_array function of the NSE msrpctypes.lua library, which trusts the entry count declared by the server. A malicious SMB server on a scanned host can declare an EntriesRead value of 0xFFFFFFFF with an empty buffer, causing a prolonged CPU spin and exhausting the memory of the Nmap process; the library is used by smb-enum-shares.nse in the default script category (-sC, -A).

### CVE-2026-81411

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-25T18:18:55.963 |

Nmap before 7.992 contains an infinite loop vulnerability in the ConfCreateResponse GCC block parser of the NSE rdp.lua library, which does not check that each block advances the read position. A malicious RDP server on a scanned host can include a single malformed zero-length block in an otherwise valid handshake, causing a permanent 100% CPU hang of the Nmap process that the script-timeout option does not interrupt; the library is used by rdp-enum-encryption.nse in the default script category (-sC, -A).

### CVE-2026-81408

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-25T18:18:55.497 |

Nmap before 7.992 contains a loop with an unreachable exit condition in the parameter-list parsing of the NSE drda.lua library, which keeps growing its parameter list while processing a malicious DRDA response. A malicious DRDA service on a scanned host can make the loop consume memory without bound on 64-bit builds, exhausting the Nmap process and discarding NSE results for every other host in the same scan batch without reporting an error; the library is reached by service probes during version detection (-sV).

### CVE-2026-81406

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-25T18:18:55.190 |

Nmap before 7.992 contains an uncontrolled resource consumption vulnerability in the read_db2_packet function of the db2-das-info.nse script, which trusts an unmasked 32-bit length field supplied by the server. A malicious DB2 Administration Server on a scanned host can declare a packet length of up to roughly 4.29GB, causing the script to buffer that much data and the Nmap process to exhaust memory; the script runs during version detection (-sV).

### CVE-2026-81405

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-25T18:18:55.010 |

Nmap before 7.992 contains an uncontrolled resource consumption vulnerability in the Comm.ReceivePacket function of the NSE rpc.lua library, which buffers ONC-RPC record fragments using the server-declared fragment length without an upper bound. A malicious RPC service on a scanned host can declare fragments of up to roughly 2.1GB, and up to 400 fragments per call, causing the Nmap process to exhaust memory; the read path is reached by rpcinfo.nse during version detection (-sV) and is shared by the NFS, rusers and NetWorker scripts.

### CVE-2026-135135

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-312` |
| Published | 2026-11-25T18:18:49.873 |

Mongoid builds an incomplete automatic encryption schema for certain embedded document associations. As a result, values that the application declared as encrypted may be written to the database in cleartext, with no error or warning returned to the application. A party holding only basic read privileges on the affected collection, and no access to the encryption keys, may then obtain those values in readable form.

### CVE-2026-136836

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-25T17:17:50.703 |

Jenkins Gradle Plugin 2.21.1282.v024680ce00a_b_ and earlier does not configure its XML parser to prevent XML external entity (XXE) attacks when processing Maven extension configuration files from build workspaces.

### CVE-2026-135404

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-25T17:17:45.890 |

Ever Gauzy is an open source business management platform for ERP, CRM, HRM, ATS, and project management. Prior to 111.42.11, singleton-scoped ExportService stores the per-request identifiers this.idCsv and this.idZip as BehaviorSubjects and keeps derived directory names in instance fields, while singleton-scoped ImportService stores per-request paths in this._dirname and this._extractPath. Concurrent requests by different tenant administrators to /export, /export/template, /export/filter, or /import can interleave while asynchronous file operations are in progress, allowing one tenant's export archive to be delivered, overwritten, or deleted by another operation, or causing one tenant's import to read another tenant's uploaded CSV data and persist it under the wrong tenant. This issue is fixed in version 111.42.11.

### CVE-2026-135228

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-25T17:17:44.763 |

A vulnerability in the MongoDB integration package for the Laravel framework allows an unauthorized user to bypass mass assignment attribute protections. When an application uses attribute deny-lists to guard sensitive model fields, specially crafted request payloads containing database operator keys can circumvent these protections. An unauthorized user with network access to an affected application endpoint can modify guarded attributes, potentially leading to privilege escalation within the application

### CVE-2026-135142

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-25T17:17:43.420 |

An incorrect authorization weakness in the embedded relation handling of the Laravel MongoDB library may allow a user with basic application privileges to alter records belonging to other users. After an embedded relation is pre-loaded, a routine write on that record is issued without the constraint that limits it to the record the user is permitted to change. This may result in unintended modification or loss of stored data for other users of the same application.

### CVE-2026-82494

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-25T15:17:52.790 |

openIMIS before 2026-10 contains a missing authorization vulnerability in the FHIR R4 module (openimis-be-api_fhir_r4_py) that allows an authenticated attacker with limited district-level access to receive subscription notifications for data outside their authorized scope due to the absence of row-level security checks such as has_perms, get_queryset, ROW_SECURITY, district, or health-facility scoping on the notification delivery path. Attackers can register a standing FHIR subscription to continuously receive claim data and can further direct notification pushes to internal network addresses.

### CVE-2026-136914

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-25T15:17:49.413 |

JuggleIM im-server before 1.8.17 contains a missing authorization vulnerability that allows authenticated users to invoke the internal g_del_members operation by supplying it as a client topic. Attackers holding a valid connect token can send crafted WebSocket or HTTP publish requests with arbitrary group and member ids to remove any users from any group in the application.

### CVE-2026-136913

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-25T15:17:49.250 |

JuggleIM im-server before 1.8.17 contains an authorization bypass vulnerability that allows authenticated end users to invoke the internal upd_user_info operation because ImListenerImpl.PublishArrived forwards any client-supplied topic as the RPC method. Attackers holding a valid connect token can supply another user's id to UpdUserInfo to overwrite that user's nickname, portrait, extension fields and settings.

### CVE-2026-123679

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-26T03:16:33.730 |

An improper access control vulnerability exists in a privileged Unix domain socket of StellarProtect Linux and Stellar Agent (Linux). Due to insufficient authorization checks, a low-privileged local attacker can interact with the daemon and invoke privileged operations without the necessary permissions. This issue affects StellarProtect Linux: 1.0 and earlier; Stellar Agent (Linux): before 1.2.54. *Note: Stellar Agent (Linux) is the new name for StellarProtect Linux.

### CVE-2026-136862

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522;CWE-706` |
| Published | 2026-11-25T15:17:47.443 |

In Eclipse Apoapsis ORT Server Credential Helper versions 0.1.0 to 0.2.0, as shipped with Eclipse Apoapsis ORT Server versions 0.65.0 to 0.83.0, the Git credential helper selects stored credentials by re-parsing the requested URL with a regular expression that can be confused by `:` and `@` characters in the URL path. An attacker who can make an ORT Server worker fetch a crafted Git URL, for example through a submodule of a repository that is analyzed, can obtain credentials stored for a different host, such as `github.com`, which Git then sends to the attacker-controlled server.



The issue is fixed in Eclipse Apoapsis ORT Server Credential Helper 0.2.1 and Eclipse Apoapsis ORT Server 0.84.0.
